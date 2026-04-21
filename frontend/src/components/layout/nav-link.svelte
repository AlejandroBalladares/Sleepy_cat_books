<script lang="ts">
	import { page } from '$app/stores';
	import { cn } from '$lib/utils';
	import type { Snippet } from 'svelte';

	let { href, children }: { href: string; children: Snippet } = $props();
	let active = $derived($page.url.pathname === href);
</script>

<a {href} class={cn('text-white hover:text-blue-300', active && 'font-bold underline')}>
	{@render children()}
</a>
