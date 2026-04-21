<script lang="ts">
	let { error }: { error: string[] | undefined } = $props();
</script>

{#if error}
	<p aria-live="polite" class="mt-1 text-sm text-red-500">{error.join('\n')}</p>
{/if}
