import { register as registerUser } from '$lib/server/auth';
import { userRegisterSchema } from '$models/user';
import { fail, redirect } from '@sveltejs/kit';
import { setError, superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import type { Actions } from './$types';

export const load = async () => {
	const form = await superValidate(zod(userRegisterSchema));

	return { form };
};

export const actions = {
	register: async ({ request, url }) => {
		const form = await superValidate(request, zod(userRegisterSchema));
		console.log(form);

		if (!form.valid) {
			return fail(400, { form });
		}

		try {
			await registerUser(form.data);
		} catch (e) {
			console.error(e);
			return setError(form, 'Hubo un error al registrarse');
		}

		if (url.searchParams.has('redirect')) {
			redirect(303, '/login?redirect=' + url.searchParams.get('redirect')!);
		} else {
			redirect(303, '/login');
		}
	}
} satisfies Actions;
