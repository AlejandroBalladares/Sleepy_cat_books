import { getFavorites, getProximaLecturas } from '$lib/server/library';

import { redirect } from '@sveltejs/kit';

export const load = async ({ cookies }) => {
	const session = cookies.get('session');
	if (!session) {
		redirect(403, '/login');
	}

	const books = await getFavorites(session);

	const books_unread = await getProximaLecturas(session);

	return { books, books_unread };
};
