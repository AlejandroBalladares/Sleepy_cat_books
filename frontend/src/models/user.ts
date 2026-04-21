import { z } from 'zod';

const roles = ['AUTOR', 'LECTOR'] as const;

const userBaseSchema = z.object({
	nombre: z.string().min(2),
	apellido: z.string().min(2),
	email: z.string().email(),
	nombre_de_usuario: z.string().min(6),
	fecha_nacimiento: z.date().max(new Date()).min(new Date('1900-01-01')),
	rol: z.enum(roles)
});

export const userLoginSchema = z.object({
	username: z.string().email(),
	password: z.string()
});

export const userRegisterSchema = userBaseSchema
	.extend({
		contraseña: z.string().min(8),
		confirmPassword: z.string().min(8)
	})
	.refine((data) => data.contraseña === data.confirmPassword, {
		message: 'Las contraseñas no coinciden',
		path: ['confirmPassword']
	});

export const UserSchema = userBaseSchema.extend({
	id: z.number(),
	descripcion: z.string().optional(),
	foto_de_perfil: z.string().optional()
});

export const userEditSchema = z.object({
	nombre: z.string().min(2),
	apellido: z.string().min(2),
	email: z.string().email(),
	descripcion: z.string().nullable().optional(),
	foto_de_perfil: z.string().url().nullable().optional()
});

export type UserRegister = z.infer<typeof userRegisterSchema>;

export type UserLogin = z.infer<typeof userLoginSchema>;

export type UserEdit = z.infer<typeof userEditSchema>;

export type User = z.infer<typeof UserSchema>;

export type LoginResponse = {
	access_token: string;
	token_type: 'bearer';
};

// Logica roles!
export function canChangeRole(user: User): boolean {
	return user.rol === 'AUTOR';
}

export function toggleRole(user: User): User {
	if (user.rol === 'AUTOR') {
		return { ...user, rol: 'LECTOR' };
	} else if (user.rol === 'LECTOR') {
		return { ...user, rol: 'AUTOR' };
	}
	return user; // Si no cumple ninguna condición, devuelve el usuario sin cambios
}
