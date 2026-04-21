import { z } from 'zod';

const tipoComunidad = ['Publico', 'Privado'] as const;

const baseCommunitySchema = z.object({
	nombre: z.string().min(1, 'El nombre es obligatorio').max(100),
	descripcion: z.string().max(500).optional(),
	imagen: z.string().url().nullable().optional(),
	tipo: z.enum(tipoComunidad).default('Publico')
});

export const communityCreateSchema = baseCommunitySchema.extend({
	// alguna propiedad adicional
});

export const communitySchema = baseCommunitySchema.extend({
	id: z.number(),
	tipo: z.enum(tipoComunidad),
	id_creador: z.number()
});

export const communityEditSchema = baseCommunitySchema.extend({
	tipo: z.enum(tipoComunidad)
});

export type CommunityCreate = z.infer<typeof communityCreateSchema>;

export type Community = z.infer<typeof communitySchema>;

export type CommunityEdit = z.infer<typeof communityEditSchema>;
