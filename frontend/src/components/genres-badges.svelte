<script lang="ts">
	import { Badge } from '$lib/components/ui/badge';
	import type { Genre } from '$models/genres';

	let { genres }: { genres: Genre[] } = $props();
</script>

<div class="flex flex-wrap gap-2">
	{#each genres as genero}
		<Badge>{genero.nombre}</Badge>
	{/each}
</div>
