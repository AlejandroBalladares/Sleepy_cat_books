<script lang="ts">
	import * as Alert from '$lib/components/ui/alert';
	import CircleAlert from 'lucide-svelte/icons/circle-alert';

	let { title = 'Error!', description = 'Hubo un error inesperado.' } = $props();
</script>

<Alert.Root variant="destructive">
	<CircleAlert class="h-4 w-4" />
	<Alert.Title>{title}</Alert.Title>
	<Alert.Description>{description}</Alert.Description>
</Alert.Root>
