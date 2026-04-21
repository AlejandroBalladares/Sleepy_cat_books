<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import type { Snippet } from 'svelte';

	let { disabled = false, children, ...props }: { children: Snippet; disabled: boolean } = $props();
</script>

<Button variant="default" type="submit" {disabled} {...props}>
	{@render children()}
</Button>
