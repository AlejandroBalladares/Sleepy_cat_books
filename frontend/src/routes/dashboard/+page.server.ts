import { getPopularBooks } from '$lib/server/books';

export const load = async () => {
	const popularBooks = await getPopularBooks();

	return { popularBooks };
};
