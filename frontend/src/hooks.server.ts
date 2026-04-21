import type { User } from '$models/user';

export const handle = async ({ event, resolve }) => {
	const session = event.cookies.get('session');

	if (!session) {
		// if there is no session load page as normal
		return await resolve(event);
	}
	event.locals.session = session;

	const userString = event.cookies.get('user');
	if (userString) {
		const user: User = JSON.parse(userString);
		event.locals.user = user;
	}

	// load page as normal
	return await resolve(event);
};
