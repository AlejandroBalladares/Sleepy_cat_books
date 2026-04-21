import { addMember, createPost, getMembers, getOne, getPosts } from '$lib/server/communities';
import { postCreateSchema } from '$models/posts.js';
import { error } from '@sveltejs/kit';
import { fail, superValidate, setError, message } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';

export const load = async ({ params }) => {
	const id = +params.id;
	let community, members, posts;

	try {
		community = await getOne(id);
		members = await getMembers(id);
		posts = await getPosts(id);
	} catch (e) {
		console.error(e);
		error(404, 'Comunidad no encontrada');
	}

	const postForm = await superValidate(zod(postCreateSchema));

	posts.sort((a, b) => (a.fecha > b.fecha ? -1 : 1));

	return { community, members, postForm, posts };
};

export const actions = {
	joinCommunity: async ({ params, cookies }) => {
		const id = +params.id;
		const session = cookies.get('session') as string;

		try {
			await addMember(id, session);
		} catch (e) {
			console.error(e);
			return fail(400, { error: (e as Error).message });
		}

		const msg = 'Usuario unido a comunidad correctamente';
		return { message: msg };
	},
	createPost: async ({ request, params, cookies }) => {
		const id = +params.id;
		const session = cookies.get('session') as string;
		const form = await superValidate(request, zod(postCreateSchema));

		try {
			await createPost(form.data, id, session);
		} catch (e) {
			console.error(e);
			return setError(form, (e as Error).message);
		}

		const msg = 'Publicación agregada correctamente';
		return message(form, msg);
	}
};
