<script lang="ts">
	import type { Snippet } from 'svelte';
	import Footer from './footer.svelte';
	import Header from './header.svelte';
	import { ModeWatcher } from 'mode-watcher';

	let { children }: { children: Snippet } = $props();
</script>

<div class="flex min-h-screen flex-col">
	<Header />
	<main class="container mx-auto flex-grow px-4 py-8 sm:px-6 lg:px-8">
		{@render children()}
	</main>
	<Footer />

	<ModeWatcher />
</div>
