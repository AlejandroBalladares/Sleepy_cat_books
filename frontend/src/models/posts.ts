import { z } from 'zod';
import { UserSchema } from './user';

export const postBaseSchema = z.object({
	contenido: z.string().min(1)
});

export const postCreateSchema = postBaseSchema.extend({
	imagenes: z.array(z.string().nullable().optional()).min(1).default([''])
});

export const postSchema = postBaseSchema.extend({
	id: z.number(),
	usuario: UserSchema,
	imagenes: z
		.object({
			url: z.string(),
			id: z.number()
		})
		.array(),
	fecha: z.date()
});

export type PostCreate = z.infer<typeof postCreateSchema>;

export type Post = z.infer<typeof postSchema>;
