import { getUser, login as loginUser } from '$lib/server/auth';
import { userLoginSchema } from '$models/user';
import { fail, redirect } from '@sveltejs/kit';
import { setError, superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import type { Actions } from './$types';

export const load = async () => {
	const form = await superValidate(zod(userLoginSchema));

	return { form };
};

export const actions = {
	login: async ({ request, url, cookies }) => {
		const form = await superValidate(request, zod(userLoginSchema));
		console.log(form);

		if (!form.valid) {
			return fail(400, { form });
		}

		let res_login;
		try {
			res_login = await loginUser(form.data);
		} catch (e) {
			console.error(e);
			return setError(form, 'Hubo un error al iniciar sesión');
		}

		cookies.set('session', res_login.access_token, {
			// Habilitado para todas las rutas
			path: '/',
			// 7 días de vigencia
			maxAge: 60 * 60 * 24 * 7,
			// solo se envía en el servidor
			httpOnly: true
		});

		let res_user;

		try {
			res_user = await getUser(res_login.access_token);
		} catch (e) {
			console.error(e);
			return setError(form, 'Hubo un error al iniciar sesión');
		}

		//* Necesitaría q devuelvan tambien los datos del usuario
		console.log(res_user);
		cookies.set('user', JSON.stringify(res_user), { path: '/' });

		if (url.searchParams.has('redirect')) {
			redirect(303, url.searchParams.get('redirect')!);
		} else {
			redirect(303, '/dashboard');
		}
	}
} satisfies Actions;
