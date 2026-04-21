import { getUser } from '$lib/server/auth';

export const load = async ({ cookies }) => {
	const session = cookies.get('session')!;

	const user = await getUser(session);

	return { user };
};
