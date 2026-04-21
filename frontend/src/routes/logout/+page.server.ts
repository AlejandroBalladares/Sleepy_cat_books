import { redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ locals }) => {
	if (!locals?.user) {
		redirect(302, '/login');
	}
};

export const actions = {
	logout: async ({ locals, cookies }) => {
		cookies.delete('session', { path: '/' });
		cookies.delete('user', { path: '/' });
		locals.session = null;
		locals.user = null;
		redirect(302, '/login');
	}
} satisfies Actions;
