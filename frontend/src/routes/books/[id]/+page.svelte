<script lang="ts">
	import Modal from '$components/common/modal.svelte';
	import Subtitle from '$components/common/subtitle.svelte';
	import Title from '$components/common/title.svelte';
	import FormAddBookToShelf from '$components/forms/form-add-book-to-shelf.svelte';
	import FormCreateReview from '$components/forms/form-create-review.svelte';
	import FormRemoveBookFromShelf from '$components/forms/form-remove-book-from-shelf.svelte';
	import GenresBadges from '$components/genres-badges.svelte';
	import UserAvatar from '$components/user-avatar.svelte';
	import Button from '$lib/components/ui/button/button.svelte';
	import { timeAgo } from '$lib/relative-date';
	import { cn } from '$lib/utils.js';
	import BookRating from './book-rating.svelte';
	import { localRole } from '$lib/store/role';
	import BookPreviewRelated from '$components/book-preview-related.svelte';

	let { data } = $props();

	const { book, userHasReview, id, user, shelves, relatedBooks } = data;

	let modalVisible = $state(false);
	let showMore = $state(false);
	let modalIllustrationsVisible = $state(false);

	function closeModal() {
		modalVisible = false;
	}

	function toggleShowMore() {
		showMore = !showMore;
	}

	function showModal() {
		modalVisible = true;
	}

	function showIllustrationsModal() {
		modalIllustrationsVisible = !modalIllustrationsVisible;
	}
</script>

<div class="mb-6 flex gap-x-8">
	<div class="flex flex-col content-between gap-y-4">
		<img src={book.portada} class="book-cover self-baseline" alt="Portada Libro" />
		{#if user}
			<div>
				<Subtitle class="mb-2">Puntuá este libro</Subtitle>
				<BookRating data={data.ratingForm}></BookRating>
			</div>
		{/if}
	</div>
	<div class="prose flex-[0.7] dark:prose-invert">
		<h1>{book.nombre}</h1>
		{#if user}
			<div class="flex gap-x-4">
				<FormAddBookToShelf {shelves} data={data.shelfForm} />
				<FormRemoveBookFromShelf {shelves} data={data.shelfForm} />
			</div>
		{/if}
		<p>Fecha de publicación: {timeAgo(book.fecha_publicacion)}</p>
		<GenresBadges genres={book.generos} />
		<p class={cn(!showMore && 'line-clamp-6', 'book-description')}>
			{book.descripcion}
		</p>
		<button onclick={toggleShowMore} class="underline">
			{showMore ? 'Mostrar menos' : 'Mostrar más'}
		</button>
	</div>
	{#if user && book.id_autor == user.id && $localRole === 'AUTOR'}
		<div class="book-edit">
			<Button href={'/books/' + id + '/edit'}>Editar libro</Button>
		</div>
	{/if}
</div>

<Modal bind:showModal={modalVisible}>
	{#snippet header()}
		<h2>
			{book.nombre}
		</h2>
		<br />
	{/snippet}
	<FormCreateReview data={data.reviewForm} {closeModal} />
</Modal>

<Modal bind:showModal={modalIllustrationsVisible}>
	{#snippet header()}
		<h2>
			{book.nombre}
		</h2>
		<br />
	{/snippet}
	<div class="row">
		{#each book.imagenes_ilustrativas as imagen_ilustrativa, i}
			<img
				src={imagen_ilustrativa.url}
				class="book-illustration self-baseline"
				alt="Imagen Ilustrativa {i}"
			/>
		{:else}
			<div class="book-illustration-empty">No hay imágenes ilustrativas que mostrar.</div>
		{/each}
	</div>
	<div class="flex justify-between">
		<Button onclick={showIllustrationsModal}>Cerrar</Button>
	</div>
</Modal>

<Button onclick={showIllustrationsModal}>Ilustraciones</Button>

<Title>También te pueden interesar</Title>

<ul class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
	{#each relatedBooks as book}
		<li>
			<BookPreviewRelated {book} />
		</li>
	{/each}
</ul>

<Title>Reseñas</Title>

{#if !userHasReview}
	<Button onclick={showModal}>Escribir reseña</Button>
{/if}

<div class="mt-6">
	<ul>
		{#each data.reviews as review}
			<div class="flex gap-x-3 border-b-2 border-b-gray-500 p-3 dark:border-b-white">
				<UserAvatar
					foto_de_perfil={review.usuario.foto_de_perfil}
					nombre={review.usuario.nombre_de_usuario}
				/>
				<div>
					<p class="text-lg font-bold">{review.usuario.nombre_de_usuario}</p>
					<p class="text-lg">{review.contenido}</p>
				</div>
			</div>
		{:else}
			<p class="text-center text-lg">No hay reseñas para este libro.</p>
		{/each}
	</ul>
</div>

<style>
	.book-cover {
		object-fit: scale-down;
		max-width: 300px;
		max-height: fit-content;
	}

	.book-description {
		text-align: justify;
	}

	.book-illustration {
		object-fit: scale-down;
		max-width: 300px;
		max-height: fit-content;
		float: left;
		border: 5px solid black;
		margin: 20px;
	}

	.book-illustration-empty {
		margin: 20px;
	}

	.row::after {
		content: '';
		clear: both;
		display: table;
	}
</style>
