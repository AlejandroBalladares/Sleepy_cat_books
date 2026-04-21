<script lang="ts">
	import { cn } from '$lib/utils';
	import type { Snippet } from 'svelte';

	let { children, class: className }: { children: Snippet; class?: string | null } = $props();
</script>

<h1 class={cn('text-center text-2xl font-bold text-gray-800 dark:text-gray-200', className)}>
	{@render children()}
</h1>
