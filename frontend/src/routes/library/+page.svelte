<script>
	import BookPreview from '$components/book-preview.svelte';
	import Title from '$components/common/title.svelte';
	let { data } = $props();
	const books = data.books;
	const unread = data.books_unread;
</script>

<Title>Biblioteca personal</Title>
<p class="favorite-books">Visualiza tus libros favoritos</p>

<ul class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
	{#each books as book}
		<li>
			<BookPreview {book} />
		</li>
	{/each}
</ul>

<p class="favorite-books">Visualiza los libros que quieras leer a futuro</p>

<ul class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
	{#each unread as book}
		<li>
			<BookPreview {book} />
		</li>
	{/each}
</ul>

<style type="text/css">
	.favorite-books {
		margin-bottom: 10px;
		font-size: large;
	}
</style>
