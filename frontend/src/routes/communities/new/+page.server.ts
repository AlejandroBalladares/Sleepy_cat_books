import { communityCreateSchema } from '$models/communities';
import { message, setError, superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import { fail, redirect, type Actions } from '@sveltejs/kit';
import { create as createCommunity } from '$lib/server/communities';

export const load = async () => {
	const form = await superValidate(zod(communityCreateSchema));

	return { form };
};

export const actions = {
	new: async ({ request, locals }) => {
		const form = await superValidate(request, zod(communityCreateSchema));
		console.log(form);

		if (!form.valid) {
			return fail(400, { form });
		}

		const session = locals.session;

		if (!session) {
			redirect(403, '/');
		}

		try {
			await createCommunity(form.data, session);
		} catch (e) {
			console.error(e);
			return setError(form, 'Hubo un error al crear la Comunidad.');
		}

		return message(form, 'Comunidad creado correctamente');
	}
} satisfies Actions;
