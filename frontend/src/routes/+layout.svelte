<script lang="ts">
	import MainContainer from '$components/layout/main-container.svelte';
	import { Toaster } from '$lib/components/ui/sonner';
	import '../app.css';

	let { children } = $props();
</script>

<svelte:head>
	<title>Sleepy Cat Books</title>
	<meta
		name="description"
		content="Descubrí nuevos libros y autores. Promocioná tus propias obras!"
	/>
</svelte:head>

<MainContainer>
	<Toaster richColors closeButton />
	{@render children()}
</MainContainer>
