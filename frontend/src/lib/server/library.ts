import { PUBLIC_BACKEND_URL } from '$env/static/public';
import type { Book } from '$models/books';
import type { Shelf } from '$models/library';

const BASE_URL = PUBLIC_BACKEND_URL + '/library';

export async function getFavorites(session: string): Promise<Book[]> {
	const res = await fetch(BASE_URL + '/favoritos', {
		headers: {
			Authorization: 'Bearer ' + session
		}
	});

	const data = await res.json();

	if (!res.ok) {
		throw new Error(data.detail);
	}

	return data;
}

export async function getProximaLecturas(session: string): Promise<Book[]> {
	const res = await fetch(BASE_URL + '/proximas lecturas', {
		headers: {
			Authorization: 'Bearer ' + session
		}
	});

	const data = await res.json();

	if (!res.ok) {
		throw new Error(data.detail);
	}

	return data;
}

export async function addToShelf(id_libro: number, session: string, shelfName: string) {
	console.log('id: ' + id_libro);
	console.log('session: ' + session);
	console.log('ShelfName: ' + shelfName);
	const res = await fetch(BASE_URL + '/' + shelfName, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Authorization: 'Bearer ' + session
		},
		body: JSON.stringify({ id_libro })
	});

	const data = await res.json();

	if (!res.ok) {
		throw new Error(data.detail);
	}

	return data;
}

export async function removeFromShelf(id_libro: number, session: string, shelfName: string) {
	const res = await fetch(BASE_URL + '/' + shelfName + '/' + id_libro, {
		method: 'DELETE',
		headers: {
			'Content-Type': 'application/json',
			Authorization: 'Bearer ' + session
		}
	});

	const data = await res.json();

	if (!res.ok) {
		throw new Error(data.detail);
	}

	return data;
}

export async function getShelves(session: string): Promise<Shelf[]> {
	const res = await fetch(BASE_URL, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			Authorization: 'Bearer ' + session
		}
	});

	const data = await res.json();

	if (!res.ok) {
		throw new Error(data.detail);
	}

	return data;
}
/*
export async function addToUnread(id_libro: number, session: string) {
	console.log('id: ' + id_libro);
	console.log('session: ' + session);
	const res = await fetch(BASE_URL + '/unreads', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Authorization: 'Bearer ' + session
		},
		body: JSON.stringify({ id_libro })
	});

	const data = await res.json();

	if (!res.ok) {
		throw new Error(data.detail);
	}

	return data;
}

export async function removeFromUNreads(id_libro: number, session: string) {
	const res = await fetch(BASE_URL + '/unreads/' + id_libro, {
		method: 'DELETE',
		headers: {
			'Content-Type': 'application/json',
			Authorization: 'Bearer ' + session
		}
	});

	const data = await res.json();

	if (!res.ok) {
		throw new Error(data.detail);
	}

	return data;
}


export async function getProximaLecturas(session: string): Promise<Book[]> {
	const res = await fetch(BASE_URL + '/proxima lecturas', {
		headers: {
			Authorization: 'Bearer ' + session
		}
	});

	const data = await res.json();

	if (!res.ok) {
		throw new Error(data.detail);
	}

	return data;
}*/
