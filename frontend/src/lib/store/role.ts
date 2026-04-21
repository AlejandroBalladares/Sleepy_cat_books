// Para almacenar el rol del usuario AUTOR en el frontend
import { writable } from 'svelte/store';

export const localRole = writable<'AUTOR' | 'LECTOR'>('AUTOR'); // Valor inicial
