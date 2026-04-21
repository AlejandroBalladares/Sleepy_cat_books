import type { User } from '$models/user.js';

export const load = async ({ locals }) => {
	return {
		user: locals.user as User | undefined // Esto es para que aparezca el usuario en { data } = $props();
	};
};
