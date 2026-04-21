import { create as createBook } from '$lib/server/books';
import { getAll as getAllGenres } from '$lib/server/genres';
import { bookCreateSchema } from '$models/books';
import { fail, redirect } from '@sveltejs/kit';
import { message, setError, superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';

export const load = async () => {
	const form = await superValidate(zod(bookCreateSchema));

	let genres;
	try {
		genres = await getAllGenres();
	} catch {
		genres = [{ id: 1, nombre: 'Error al cargar los géneros' }];
	}

	return { form, genres };
};

export const actions = {
	new: async ({ request, locals }) => {
		const form = await superValidate(request, zod(bookCreateSchema));
		console.log(form);

		if (!form.valid) {
			return fail(400, { form });
		}

		const session = locals.session;

		if (!session) {
			redirect(403, '/');
		}

		try {
			await createBook(form.data, session);
		} catch (e) {
			console.error(e);
			return setError(form, 'Hubo un error al crear el libro.');
		}

		return message(form, 'Libro creado correctamente');
	}
};
