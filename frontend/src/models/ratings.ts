import { z } from 'zod';

export const ratingCreateSchema = z.object({
	puntuacion: z.number()
});

export const ratingSchema = ratingCreateSchema.extend({
	id_usuario: z.number()
});

export type RatingCreate = z.infer<typeof ratingCreateSchema>;

export type Rating = z.infer<typeof ratingSchema>;
