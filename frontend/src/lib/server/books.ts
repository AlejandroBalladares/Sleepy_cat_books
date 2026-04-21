import { PUBLIC_BACKEND_URL } from '$env/static/public';
import type { Book, BookCreate, BookEdit } from '$models/books';

const BASE_URL = PUBLIC_BACKEND_URL + '/books';

export async function create(book: BookCreate, access_token: string) {
	const res = await fetch(BASE_URL, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Authorization: 'Bearer ' + access_token
		},
		body: JSON.stringify(book)
	});

	const data = await res.json();

	if (!res.ok) {
		console.log(data);
		throw new Error(data.detail);
	}

	return data;
}

export async function getAll(
	genero?: string | null,
	titulo?: string | null,
	autor_nombre?: string | null,
	autor_apellido?: string | null
): Promise<Book[]> {
	const searchParams = new URLSearchParams();
	if (genero) searchParams.append('genre', genero);
	if (titulo) searchParams.append('title', titulo);
	if (autor_nombre) searchParams.append('author_name', autor_nombre);
	if (autor_apellido) searchParams.append('author_surname', autor_apellido);

	const res = await fetch(BASE_URL + '?' + searchParams.toString());

	const data = await res.json();

	if (!res.ok) {
		throw new Error(data.detail);
	}

	return data;
}

export async function getOne(id: number): Promise<Book> {
	const res = await fetch(BASE_URL + '/' + id);

	const data = await res.json();

	if (!res.ok) {
		throw new Error(data.detail);
	}

	return data;
}

export async function editBook(id: number, book: BookEdit, access_token: string) {
	const res = await fetch(BASE_URL + '/' + id, {
		method: 'PATCH',
		headers: {
			'Content-Type': 'application/json',
			Authorization: 'Bearer ' + access_token
		},
		body: JSON.stringify(book)
	});

	const data = await res.json();

	if (!res.ok) {
		throw new Error(data.detail);
	}

	return data;
}

export async function getPopularBooks() {
	const res = await fetch(BASE_URL + '/popular');

	const data = await res.json();

	if (!res.ok) {
		throw new Error(data.detail);
	}

	return data;
}

export async function getRelatedBooks(id: number): Promise<Book[]> {
	const res = await fetch(BASE_URL + '/' + id + '/related');

	const data = await res.json();

	if (!res.ok) {
		throw new Error(data.detail);
	}

	return data;
}
