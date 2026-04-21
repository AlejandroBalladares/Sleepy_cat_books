<script lang="ts">
	import FormEditCommunity from '$components/forms/form-edit-community.svelte';
	import * as Card from '$lib/components/ui/card';

	let { data } = $props();
</script>

<Card.Root class="mx-auto mt-6 max-w-md">
	<Card.Header>
		<Card.Title class="text-center text-xl">Editar Comunidad</Card.Title>
	</Card.Header>
	<Card.Content>
		<FormEditCommunity data={data.form} />
	</Card.Content>
</Card.Root>
