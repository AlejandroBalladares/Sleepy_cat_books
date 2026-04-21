<script lang="ts">
	import { cn } from '$lib/utils';
	import type { Snippet } from 'svelte';

	let { children, class: className }: { children: Snippet; class?: string | null } = $props();
</script>

<h2 class={cn('text-center text-xl font-semibold text-gray-700 dark:text-gray-200', className)}>
	{@render children()}
</h2>
