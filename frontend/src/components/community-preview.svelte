<script lang="ts">
	import { Badge } from '$lib/components/ui/badge';
	import type { Community } from '$models/communities';
	// import CommunityLogo from './community-logo.svelte';
	let { community }: { community: Community } = $props();

	// const fallbackImage = 'https://picsum.photos/200/300';
	const fallbackImage =
		'https://as2.ftcdn.net/v2/jpg/07/88/47/29/1000_F_788472997_veh0YJMqImyc7iNPy2pcpz4D3TSlcMR5.jpg';

	// Por alguna razón no funciona
	const handleImageError = (event: Event) => {
		const img = event.target as HTMLImageElement;
		img.src = fallbackImage;
	};
</script>

<article class="h-38 grid grid-cols-[80px_1fr] gap-x-4 rounded border p-4 hover:scale-105">
	<img
		src={community.imagen ? community.imagen : fallbackImage}
		alt={community.nombre}
		class="community-logo"
		onerror={handleImageError}
	/>
	<!-- <CommunityLogo logo={community.imagen} nombre={community.nombre} /> -->
	<!-- <img src={fallbackImage} alt={community.nombre} class="w-20" /> -->
	<div class="space-y-1">
		<h3 class="line-clamp-2 font-semibold tracking-wide hover:underline">
			<a href="communities/{community.id}" class="block">{community.nombre}</a>
		</h3>
		<Badge>{community.tipo}</Badge>
		<p class="line-clamp-1">{community.descripcion}</p>
	</div>
</article>

<style type="text/css">
	.community-logo {
		width: 70px;
		height: 70px;
		border-radius: 50%;
		object-fit: cover;
		border: 2px solid #ccc;
	}
</style>
