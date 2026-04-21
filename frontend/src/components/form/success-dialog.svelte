<script lang="ts">
	import * as Alert from '$lib/components/ui/alert';
	import PartyPopper from 'lucide-svelte/icons/party-popper';

	let { title = 'Éxito!', description = 'Operación ejecutada correctamente' } = $props();
</script>

<Alert.Root variant="success">
	<PartyPopper class="h-4 w-4" />
	<Alert.Title>{title}</Alert.Title>
	<Alert.Description>{description}</Alert.Description>
</Alert.Root>
