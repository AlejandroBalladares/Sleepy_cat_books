import { getOne, getRelatedBooks } from '$lib/server/books';
import { getShelves, addToShelf as newShelf, removeFromShelf } from '$lib/server/library';
import { createRating, deleteRating, getRatings, updateRating } from '$lib/server/ratings';
import { createReview, getReviews } from '$lib/server/reviews';
import { shelfSchema, type Shelf } from '$models/library';
import { ratingCreateSchema } from '$models/ratings';
import { reviewCreateSchema } from '$models/reviews';
import { error, fail } from '@sveltejs/kit';
import { message, setError, superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';

export const load = async ({ params, locals }) => {
	const id = +params.id;
	let book, reviews, ratings, relatedBooks;
	try {
		[book, reviews, ratings, relatedBooks] = await Promise.all([
			getOne(id),
			getReviews(id),
			getRatings(id),
			getRelatedBooks(id)
		]);
	} catch (e) {
		console.error(e);
		error(404, 'Libro no encontrado');
	}

	const user = locals.user;

	let userHasReview = false;
	let userRating = 0;
	let shelves: Shelf[] = [];

	if (user) {
		shelves = await getShelves(locals.session as string);

		for (let i = 0; i < reviews.length; i++) {
			if (reviews[i].usuario.id === user.id) {
				userHasReview = true;
				break;
			}
		}
		for (let i = 0; i < ratings.length; i++) {
			if (ratings[i].id_usuario === user.id) {
				userRating = ratings[i].puntuacion;
				break;
			}
		}
	} else {
		userHasReview = true; // The user is not logged in so can't add a review
	}

	const reviewForm = await superValidate(zod(reviewCreateSchema));
	const ratingForm = await superValidate({ puntuacion: userRating }, zod(ratingCreateSchema));
	const shelfForm = await superValidate({ nombre: 'favoritos' }, zod(shelfSchema)); // default favoritos

	return {
		book,
		id,
		reviewForm,
		reviews,
		userHasReview,
		ratingForm,
		shelfForm,
		shelves,
		relatedBooks
	};
};

export const actions = {
	createReview: async ({ request, params, cookies }) => {
		const id_libro = +params.id;
		const session = cookies.get('session') as string;
		const form = await superValidate(request, zod(reviewCreateSchema));

		if (!form.valid) {
			return fail(400, { form });
		}

		try {
			await createReview(form.data, id_libro, session);
		} catch (e) {
			console.error(e);
			return setError(form, (e as Error).message);
		}

		// Mando así y no con message(form, "...") porque quiero que se muestre en el form de $props()
		// y no en el de cada uno
		const msg = 'Reseña creada correctamente';
		return message(form, msg);
	},
	createRating: async ({ request, params, cookies }) => {
		const id_libro = +params.id;
		const session = cookies.get('session') as string;
		const form = await superValidate(request, zod(ratingCreateSchema));

		if (!form.valid) {
			return fail(400, { form });
		}

		try {
			await createRating(form.data, id_libro, session);
		} catch (e) {
			console.error(e);
			return setError(form, (e as Error).message);
		}

		const msg = 'Puntuado correctamente';
		return message(form, msg);
	},
	updateRating: async ({ request, params, cookies }) => {
		const id_libro = +params.id;
		const session = cookies.get('session') as string;
		const form = await superValidate(request, zod(ratingCreateSchema));

		if (!form.valid) {
			return fail(400, { form });
		}

		try {
			await updateRating(form.data, id_libro, session);
		} catch (e) {
			console.error(e);
			return setError(form, (e as Error).message);
		}

		const msg = 'Puntuación actualizada';
		return message(form, msg);
	},
	deleteRating: async ({ request, params, cookies }) => {
		const id = +params.id;
		const session = cookies.get('session') as string;
		const form = await superValidate(request, zod(ratingCreateSchema));

		if (!form.valid) {
			return fail(400, { form });
		}

		try {
			await deleteRating(id, session);
		} catch (e) {
			console.error(e);
			return setError(form, (e as Error).message);
		}

		const msg = 'Puntuación eliminada';
		return message(form, msg);
	},
	addToShelf: async ({ request, params, cookies }) => {
		const id = +params.id;
		const session = cookies.get('session') as string;
		const form = await superValidate(request, zod(shelfSchema));

		if (!form.valid) {
			return fail(400, { form });
		}

		const shelfName = form.data.nombre;

		try {
			await newShelf(id, session, shelfName);
		} catch (e) {
			console.error(e);
			return setError(form, (e as Error).message);
		}

		const msg = 'Libro añadido correctamente';
		return message(form, msg);
	},
	removeFromShelf: async ({ request, params, cookies }) => {
		const id = +params.id;
		const session = cookies.get('session') as string;
		const form = await superValidate(request, zod(shelfSchema));
		const shelfName = form.data.nombre;

		try {
			await removeFromShelf(id, session, shelfName);
		} catch (e) {
			console.error(e);
			return setError(form, (e as Error).message);
		}

		const msg = 'Libro eliminado correctamente';
		return message(form, msg);
	}
};
