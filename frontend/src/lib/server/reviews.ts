import { PUBLIC_BACKEND_URL } from '$env/static/public';
import type { Review, ReviewCreate } from '$models/reviews';

const BASE_URL = PUBLIC_BACKEND_URL + '/books';

export async function createReview(review: ReviewCreate, id_libro: number, access_token: string) {
	const res = await fetch(BASE_URL + '/' + id_libro + '/reviews', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Authorization: 'Bearer ' + access_token
		},
		body: JSON.stringify(review)
	});

	const data = await res.json();

	if (!res.ok) {
		console.log(data);
		throw new Error(data.detail);
	}

	return data;
}

export async function getReviews(id: number): Promise<Review[]> {
	const res = await fetch(BASE_URL + '/' + id + '/reviews');

	const data = await res.json();

	if (!res.ok) {
		console.log(data);
		throw new Error(data.detail);
	}

	return data;
}
