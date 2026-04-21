<script lang="ts">
	import BookPreview from '$components/book-preview.svelte';
	import Title from '$components/common/title.svelte';
	import { localRole } from '$lib/store/role.js';

	let { data } = $props();
	const user = data.user!;
	const popularBooks = data.popularBooks;
</script>

<article class="prose dark:prose-invert">
	<h1>Inicio</h1>

	<p>Busca libros <a href="/books">aquí</a></p>

	<p>Interactúa con otros usuarios en las <a href="/communities">comunidades</a></p>

	{#if user.rol === 'AUTOR' && $localRole === 'AUTOR'}
		<p>Puedes agregar un libro <a href="/books/new">aquí</a></p>
	{/if}
</article>

<Title class="mb-6 mt-12">¡Consulta los libros más populares!</Title>
{#if popularBooks.length > 0}
	<ul class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
		{#each popularBooks as book}
			<li>
				<BookPreview {book} />
			</li>
		{/each}
	</ul>
{:else}
	<p class="text-center text-lg">
		No encontramos libros populares para recomendarte, vuelve más tarde.
	</p>
{/if}
