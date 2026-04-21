import { z } from 'zod';
import { UserSchema } from './user';

export const reviewCreateSchema = z.object({
	contenido: z.string().min(1)
});

export const reviewSchema = reviewCreateSchema.extend({
	usuario: UserSchema
});

export type ReviewCreate = z.infer<typeof reviewCreateSchema>; // los tipos van con mayúscula

export type Review = z.infer<typeof reviewSchema>;
