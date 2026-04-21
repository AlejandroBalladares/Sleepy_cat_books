import { z } from 'zod';
import { genreSchema } from './genres';

const bookBaseSchema = z.object({
	nombre: z.string().min(2),
	descripcion: z.string().min(10)
});

export const bookCreateSchema = bookBaseSchema.extend({
	isbn: z.string().min(10).max(13),
	fecha_publicacion: z.date(),
	portada: z.string().url(),
	generos: z.array(z.string()),
	id_autor: z.number()
});

export const bookSchema = bookCreateSchema.extend({
	id: z.number().positive(),
	generos: z.array(genreSchema),
	imagenes_ilustrativas: z
		.object({
			url: z.string(),
			id: z.number()
		})
		.array()
});

export const bookEditSchema = bookBaseSchema.extend({
	portada: z.string().url().nullable().optional(),
	imagenes_ilustrativas: z.array(z.string().nullable().optional()).min(1).default([''])
});

export type BookCreate = z.infer<typeof bookCreateSchema>;

export type Book = z.infer<typeof bookSchema>;

export type BookEdit = z.infer<typeof bookEditSchema>;
