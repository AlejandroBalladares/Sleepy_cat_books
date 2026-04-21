<script>
	import FormEditProfile from '$components/forms/form-edit-profile.svelte';
	import * as Card from '$lib/components/ui/card';

	let { data } = $props();
</script>

<Card.Root class="mx-auto mt-6 max-w-md">
	<Card.Header>
		<Card.Title class="text-center text-xl">Editar Perfil</Card.Title>
	</Card.Header>
	<Card.Content>
		<FormEditProfile data={data.form} />
	</Card.Content>
</Card.Root>
