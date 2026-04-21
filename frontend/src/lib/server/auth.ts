import { PUBLIC_BACKEND_URL } from '$env/static/public';
import type { LoginResponse, User, UserLogin, UserRegister } from '$models/user';

const BASE_URL = PUBLIC_BACKEND_URL + '/users';

export async function login(user: UserLogin): Promise<LoginResponse> {
	const formData = new FormData();

	formData.append('username', user.username);
	formData.append('password', user.password);

	const res = await fetch(`${PUBLIC_BACKEND_URL}/login/access-token`, {
		method: 'POST',
		body: formData
	});

	const data = await res.json();

	if (!res.ok) {
		throw new Error(data.detail);
	}

	return data;
}

export async function register(user: Omit<UserRegister, 'confirmPassword'>) {
	console.log('BASE URL: ', BASE_URL);
	const res = await fetch(`${BASE_URL}/signup`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(user)
	});

	const data = await res.json();

	if (!res.ok) {
		throw new Error(data.detail);
	}

	return data;
}

export async function getUser(access_token: string): Promise<User> {
	const res = await fetch(`${BASE_URL}/me`, {
		headers: {
			Authorization: 'Bearer ' + access_token
		}
	});

	const data = await res.json();

	if (!res.ok) {
		throw new Error(data.detail);
	}

	return data;
}
