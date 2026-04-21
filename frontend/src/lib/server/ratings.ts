import { PUBLIC_BACKEND_URL } from '$env/static/public';
import type { Rating, RatingCreate } from '$models/ratings';

const BASE_URL = PUBLIC_BACKEND_URL + '/books';

export async function createRating(rating: RatingCreate, id_libro: number, access_token: string) {
	const res = await fetch(BASE_URL + '/' + id_libro + '/ratings', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Authorization: 'Bearer ' + access_token
		},
		body: JSON.stringify(rating)
	});

	const data = await res.json();

	if (!res.ok) {
		console.log(data);
		throw new Error(data.detail);
	}

	return data;
}

export async function updateRating(rating: RatingCreate, id_libro: number, access_token: string) {
	const res = await fetch(BASE_URL + '/' + id_libro + '/ratings', {
		method: 'PATCH',
		headers: {
			'Content-Type': 'application/json',
			Authorization: 'Bearer ' + access_token
		},
		body: JSON.stringify(rating)
	});

	const data = await res.json();

	if (!res.ok) {
		console.log(data);
		throw new Error(data.detail);
	}

	return data;
}

export async function getRatings(id: number): Promise<Rating[]> {
	const res = await fetch(BASE_URL + '/' + id + '/ratings');

	const data = await res.json();

	if (!res.ok) {
		console.log(data);
		throw new Error(data.detail);
	}

	return data;
}

export async function deleteRating(id_libro: number, session: string) {
	const res = await fetch(BASE_URL + '/' + id_libro + '/ratings', {
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
