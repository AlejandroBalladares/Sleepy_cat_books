import { getAll } from '$lib/server/communities.js';
import { redirect } from '@sveltejs/kit';

export const load = async ({ cookies }) => {
	const session = cookies.get('session');
	if (!session) {
		redirect(403, '/login');
	}

	const communities = await getAll(session);

	return { communities };
};
