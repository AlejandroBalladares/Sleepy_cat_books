import { fail } from '@sveltejs/kit';
import { message, setError, superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import type { Actions } from './$types';
import { bookEditSchema, type BookEdit } from '$models/books';
import { editBook, getOne } from '$lib/server/books';

export const load = async ({ params }) => {
	const id = +params.id;

	const book = await getOne(id);

	const bookEdit: BookEdit = {
		nombre: book.nombre,
		descripcion: book.descripcion,
		portada: book.portada,
		imagenes_ilustrativas: book.imagenes_ilustrativas.map(
			(imagen_ilustrativa) => imagen_ilustrativa.url
		)
	};

	const form = await superValidate(bookEdit, zod(bookEditSchema));

	return { book, form };
};

export const actions = {
	editBook: async ({ cookies, request, params }) => {
		const form = await superValidate(request, zod(bookEditSchema));
		const id = +params.id;
		const session = cookies.get('session') as string;

		console.log('form editBook:', form);

		if (!form.valid) {
			return fail(400, { form });
		}

		try {
			await editBook(id, form.data, session);
		} catch (e) {
			console.error(e);
			return setError(form, (e as Error).message);
		}

		return message(form, 'Libro editado correctamente');
	}
} satisfies Actions;
