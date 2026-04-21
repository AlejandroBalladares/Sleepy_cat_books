import { PUBLIC_BACKEND_URL } from '$env/static/public';
import type { Genre } from '$models/genres';

const BASE_URL = PUBLIC_BACKEND_URL + '/books/generos';

export async function getAll(): Promise<Genre[]> {
	const res = await fetch(BASE_URL);

	const data = await res.json();

	if (!res.ok) {
		throw new Error(data.detail);
	}

	return data;
}
