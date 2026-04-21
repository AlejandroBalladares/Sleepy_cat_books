import { getAll } from '$lib/server/books';

export const load = async ({ url }) => {
	const genero = url.searchParams.get('genre');
	const titulo = url.searchParams.get('title');
	const autor_nombre = url.searchParams.get('author_name');
	const autor_apellido = url.searchParams.get('author_surname');

	const books = await getAll(genero, titulo, autor_nombre, autor_apellido);

	return { books };
};
