import { z } from 'zod';

export const genreSchema = z.object({
	id: z.number(),
	nombre: z.string()
});

export type Genre = z.infer<typeof genreSchema>;
