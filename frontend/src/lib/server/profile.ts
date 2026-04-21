import { PUBLIC_BACKEND_URL } from '$env/static/public';
import type { UserEdit } from '$models/user';

const BASE_URL = PUBLIC_BACKEND_URL;

export async function editProfile(user: UserEdit, access_token: string) {
	const res = await fetch(`${BASE_URL}/users/me`, {
		method: 'PATCH',
		headers: {
			'Content-Type': 'application/json',
			Authorization: 'Bearer ' + access_token
		},
		body: JSON.stringify(user)
	});

	const data = await res.json();

	if (!res.ok) {
		throw new Error(data.detail);
	}

	return data;
}
