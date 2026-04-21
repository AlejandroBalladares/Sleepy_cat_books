import { getAll } from '$lib/server/genres';

export const load = async () => {
	const genres = await getAll();

	return { genres };
};
