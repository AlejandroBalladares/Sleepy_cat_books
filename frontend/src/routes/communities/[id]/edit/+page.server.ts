// Carga y acciones para edición de una comunidad

import { fail } from '@sveltejs/kit';
import { message, setError, superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import type { Actions } from './$types';
import { communityEditSchema, type CommunityEdit } from '$models/communities';
import { editCommunity, getOne } from '$lib/server/communities';

export const load = async ({ params, locals }) => {
	const id = +params.id;

	const community = await getOne(id);

	if (!community) {
		throw fail(404, { error: 'Comunidad no encontrada' });
	}

	const user = locals.user;
	if (!user || community.id_creador !== user.id) {
		throw fail(403, { error: 'No tienes permiso para editar esta comunidad' });
	}

	const communityEdit: CommunityEdit = {
		nombre: community.nombre,
		descripcion: community.descripcion,
		imagen: community.imagen,
		tipo: community.tipo
	};

	const form = await superValidate(communityEdit, zod(communityEditSchema));

	return { community, form };
};

export const actions = {
	editCommunity: async ({ cookies, request, params, locals }) => {
		const form = await superValidate(request, zod(communityEditSchema));
		const id = +params.id;
		const session = cookies.get('session') as string;

		console.log('form editCommunity:', form);

		if (!form.valid) {
			return fail(400, { form });
		}

		const user = locals.user;
		if (!user) {
			return fail(401, { error: 'Usuario no autenticado' });
		}

		const community = await getOne(id);
		if (!community || community.id_creador !== user.id) {
			return fail(403, { error: 'No tienes permiso para editar esta comunidad' });
		}

		try {
			await editCommunity(id, form.data, session);
		} catch (e) {
			console.error(e);
			return setError(form, (e as Error).message);
		}

		return message(form, 'Comunidad editada correctamente');
	}
} satisfies Actions;
