<script>
	import Title from '$components/common/title.svelte';
	import CommunityPreview from '$components/community-preview.svelte';
	import Button from '$lib/components/ui/button/button.svelte';

	let { data } = $props();
	const communities = data.communities;
</script>

<Title>¡Encontrá las comunidades que más te representen!</Title>

<div class="text-right">
	<Button href="/communities/new">Crear comunidad</Button>
</div>

<div class="communities-container">
	<ul>
		{#each communities as community}
			<li class="community-container">
				<CommunityPreview {community} />
			</li>
		{:else}
			<p class="text-center">No se encontraron comunidades.</p>
		{/each}
	</ul>
</div>

<style type="text/css">
	.communities-container {
		margin-left: auto;
		margin-right: auto;
		max-width: 50%;
	}

	.community-container {
		margin: 10px 0;
	}
</style>
