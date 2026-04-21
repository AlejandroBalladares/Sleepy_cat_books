import { PUBLIC_BACKEND_URL } from '$env/static/public';
import type { Community, CommunityCreate, CommunityEdit } from '$models/communities';
import type { Post, PostCreate } from '$models/posts';
import type { User } from '$models/user';

const BASE_URL = PUBLIC_BACKEND_URL + '/communities';

export async function getAll(access_token: string): Promise<Community[]> {
	const res = await fetch(BASE_URL, {
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

export async function create(community: CommunityCreate, access_token: string) {
	const res = await fetch(BASE_URL, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Authorization: 'Bearer ' + access_token
		},
		body: JSON.stringify(community)
	});

	const data = await res.json();

	if (!res.ok) {
		console.log(data);
		throw new Error(data.detail);
	}

	return data;
}

export async function getOne(id: number): Promise<Community> {
	const res = await fetch(BASE_URL + '/' + id);

	const data = await res.json();

	if (!res.ok) {
		throw new Error(data.detail);
	}

	return data;
}

export async function editCommunity(id: number, community: CommunityEdit, access_token: string) {
	const res = await fetch(BASE_URL + '/' + id, {
		method: 'PATCH',
		headers: {
			'Content-Type': 'application/json',
			Authorization: 'Bearer ' + access_token
		},
		body: JSON.stringify(community)
	});

	const data = await res.json();

	if (!res.ok) {
		throw new Error(data.detail);
	}

	return data;
}

export async function getMembers(id: number): Promise<User[]> {
	const res = await fetch(BASE_URL + '/' + id + '/members');

	const data = await res.json();

	if (!res.ok) {
		throw new Error(data.detail);
	}

	return data;
}

export async function addMember(id: number, access_token: string): Promise<Community> {
	const res = await fetch(BASE_URL + '/' + id + '/members', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Authorization: 'Bearer ' + access_token
		},
		body: JSON.stringify('')
	});

	const data = await res.json();

	if (!res.ok) {
		console.log(data);
		throw new Error(data.detail);
	}

	return data;
}

export async function createPost(
	post: PostCreate,
	id: number,
	access_token: string
): Promise<Post> {
	console.log('FORM: ' + JSON.stringify(post));
	const res = await fetch(BASE_URL + '/' + id + '/posts', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Authorization: 'Bearer ' + access_token
		},
		body: JSON.stringify(post)
	});

	const data = await res.json();

	if (!res.ok) {
		console.log(data);
		throw new Error(data.detail);
	}

	return data;
}

export async function getPosts(id: number): Promise<Post[]> {
	const res = await fetch(BASE_URL + '/' + id + '/posts');

	const data = await res.json();

	if (!res.ok) {
		console.log(data);
		throw new Error(data.detail);
	}

	return data;
}
