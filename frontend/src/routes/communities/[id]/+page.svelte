<script lang="ts">
	import Title from '$components/common/title.svelte';
	import SubmitButton from '$components/form/submit-button.svelte';
	import Button from '$lib/components/ui/button/button.svelte';
	import ErrorDialog from '$components/form/error-dialog.svelte';
	import SuccessDialog from '$components/form/success-dialog.svelte';
	import Badge from '$lib/components/ui/badge/badge.svelte';
	import FormCreatePost from '$components/forms/form-create-post.svelte';
	import Modal from '$components/common/modal.svelte';
	import CommunityPost from '$components/community-post.svelte';

	let { data, form } = $props();

	const community = data.community;
	const user = data.user;
	const members = data.members;

	let modalVisible = $state(false);

	const fallbackImage =
		'https://as2.ftcdn.net/v2/jpg/07/88/47/29/1000_F_788472997_veh0YJMqImyc7iNPy2pcpz4D3TSlcMR5.jpg';

	function isMember() {
		if (!user) {
			return false;
		}

		for (let i = 0; i < members.length; i++) {
			if (members[i].id == user.id) {
				return true;
			}
		}

		return false;
	}

	function closeModal() {
		modalVisible = false;
	}

	function showModal() {
		modalVisible = true;
	}

	const handleImageError = (event: Event) => {
		const img = event.target as HTMLImageElement;
		img.src = fallbackImage;
	};
</script>

<div>
	<div class="community-header">
		<img
			src={community.imagen ? community.imagen : fallbackImage}
			alt={community.nombre}
			class="community-logo"
			onerror={handleImageError}
		/>
		<Title>{community.nombre}</Title>
	</div>
	<div class="flex justify-end gap-3">
		<form method="POST" action="?/joinCommunity">
			<SubmitButton disabled={isMember() ? true : false}
				>{isMember() ? 'Ya eres miembro' : 'Unirse'}</SubmitButton
			>
		</form>
		<Button onclick={showModal} disabled={isMember() ? false : true}>Crear publicación</Button>
	</div>
	{#if form?.error}
		<ErrorDialog title="Error" description={form.error} />
	{/if}
	{#if form?.message}
		<SuccessDialog title="Éxito" description={form.message} />
	{/if}
	<div class="community-main">
		<article class="community-posts">
			<Title>Publicaciones</Title>
			{#each data.posts as post}
				<CommunityPost {post} />
			{/each}
		</article>
		<div class="community-right-panel">
			<Title>Descripción</Title>
			<p class="community-description">{community.descripcion}</p>
			<Badge>{community.tipo}</Badge>
			<p class="my-4">Miembros: {members.length}</p>
			{#if user && user.id === community.id_creador}
				<Button href="/communities/{community.id}/edit">Editar</Button>
			{/if}
		</div>
	</div>
</div>

<Modal bind:showModal={modalVisible}>
	{#snippet header()}
		<h2>Crear publicación</h2>
		<br />
	{/snippet}
	<FormCreatePost data={data.postForm} {closeModal} />
</Modal>

<style type="text/css">
	.community-logo {
		width: 150px;
		height: 150px;
		border-radius: 50%;
		object-fit: cover;
		float: left;
		border: 3px solid #ccc;
	}

	.community-header {
		display: flex;
		align-items: center;
		justify-content: center;
		grid-template-columns: 1fr 1fr 1fr;
		column-gap: 5px;
		margin-bottom: 40px;
	}

	.community-posts {
		float: left;
		margin-right: 50px;
		padding: 10px;
		max-width: 75%;
		min-width: 50%;
	}

	.community-right-panel {
		position: sticky;
		top: 10px;
		padding: 10px;
		height: fit-content;
		max-width: 30%;
	}

	.community-description {
		margin-bottom: 10px;
	}

	.community-main {
		display: flex;
		justify-content: center;
	}
</style>
