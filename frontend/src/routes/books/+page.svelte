<script>
	import { page } from '$app/stores';
	import BookPreview from '$components/book-preview.svelte';
	import Title from '$components/common/title.svelte';
	import Button, { buttonVariants } from '$lib/components/ui/button/button.svelte';
	import { SearchX } from 'lucide-svelte';
	import Search from 'lucide-svelte/icons/search';

	let { data } = $props();
	const title = $page.url.searchParams.get('title');
	const genre = $page.url.searchParams.get('genre');
	const author_name = $page.url.searchParams.get('author_name');
	const author_surname = $page.url.searchParams.get('author_surname');
	const books = data.books;
	const genres = data.genres;
</script>

<Title>Libros</Title>

<section class="my-6 space-x-4 rounded border py-4">
	<form method="get" data-sveltekit-reload>
		<input name="title" value={title} placeholder="Buscar por título" />
		<select name="genre" value={genre || ''} class="px-4 py-2">
			<option value="">Buscar por género</option>
			{#each genres as genre}
				<option value={genre.nombre}>{genre.nombre}</option>
			{/each}
		</select>
		<input name="author_name" value={author_name} placeholder="Buscar por nombre de autor" />
		<input
			name="author_surname"
			value={author_surname}
			placeholder="Buscar por apellido de autor"
		/>
		<Button type="submit" size="icon" title="Filtrar libros"><Search class="size-6" /></Button>
		<a
			href="/books"
			data-sveltekit-reload
			class={buttonVariants({ size: 'icon', variant: 'secondary' })}
			title="Limpiar filtros"
			><SearchX class="size-6" />
		</a>
	</form>
</section>

<ul class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
	{#each books as book}
		<li>
			<BookPreview {book} />
		</li>
	{:else}
		<p>No se encontraron libros.</p>
	{/each}
</ul>

<style type="text/css">
	:root {
		--rad: 0.7rem;
		--dur: 0.3s;
		--bez: cubic-bezier(0, 0, 0.43, 1.49);
	}
	input {
		background: var(--color-light);
		padding: 0 1.6rem;
		border-radius: var(--rad);
		appearance: none;
		transition: all var(--dur) var(--bez);
		transition-property: width, border-radius;
		z-index: 1;
		position: relative;
	}
</style>
