<script lang="ts">
	import type { Book } from '$models/books';
	import GenresBadges from './genres-badges.svelte';
	let { book }: { book: Book } = $props();

	const fallbackImage = 'https://picsum.photos/200/300';

	const handleImageError = (event: Event) => {
		const img = event.target as HTMLImageElement;
		img.src = fallbackImage;
	};
</script>

<article class="grid h-40 grid-cols-[80px_1fr] gap-x-4 rounded border p-4 hover:scale-105">
	<div class="max-h-40 w-20 overflow-hidden">
		<img
			src={book.portada}
			alt={book.nombre + ' ' + book.portada}
			class="object-contain"
			onerror={handleImageError}
		/>
	</div>
	<div class="space-y-1">
		<h3 class="line-clamp-2 font-semibold tracking-wide hover:underline">
			<a href="books/{book.id}" class="block">{book.nombre}</a>
		</h3>
		<h4>{new Date(book.fecha_publicacion).toLocaleDateString('es-AR')}</h4>
		<GenresBadges genres={book.generos} />
	</div>
</article>
