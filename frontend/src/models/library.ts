import { z } from 'zod';

export const addToShelfSchema = z.object({
	id_libro: z.number()
});
export const removeFromShelfSchema = z.object({
	id_libro: z.number()
});
export const shelfSchema = z.object({
	nombre: z.string().min(1)
});

export type Shelf = z.infer<typeof shelfSchema>;
