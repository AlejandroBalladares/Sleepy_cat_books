import { getUser } from '$lib/server/auth';
import { userEditSchema } from '$models/user';
import { fail } from '@sveltejs/kit';
import { message, setError, superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import type { Actions } from './$types';
import { editProfile } from '$lib/server/profile';

export const load = async ({ cookies }) => {
	const session = cookies.get('session')!;

	const user = await getUser(session);

	const form = await superValidate(user, zod(userEditSchema));

	return { user, form };
};

export const actions = {
	editProfile: async ({ cookies, request }) => {
		const form = await superValidate(request, zod(userEditSchema));
		const session = cookies.get('session') as string;

		console.log(form);

		if (!form.valid) {
			return fail(400, { form });
		}

		try {
			await editProfile(form.data, session);
		} catch (e) {
			console.error(e);
			return setError(form, (e as Error).message);
		}

		return message(form, 'Perfil editado correctamente');
	}
} satisfies Actions;
