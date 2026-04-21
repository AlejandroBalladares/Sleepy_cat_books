<script>
	import Title from '$components/common/title.svelte';
	import FormCreateCommunity from '$components/forms/form-create-community.svelte';
	import * as Card from '$lib/components/ui/card';

	let { data } = $props();
</script>

<Title>Crear nueva comunidad</Title>

<Card.Root class="mx-auto mt-6 max-w-md">
	<Card.Header>
		<Card.Title class="text-center text-xl">Completa los campos</Card.Title>
	</Card.Header>
	<Card.Content>
		<FormCreateCommunity data={data.form} />
	</Card.Content>
	<Card.Footer></Card.Footer>
</Card.Root>
