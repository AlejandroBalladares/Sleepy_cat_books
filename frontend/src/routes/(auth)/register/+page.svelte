<script>
	import FormRegister from '$components/forms/form-register.svelte';
	import * as Card from '$lib/components/ui/card';

	let { data } = $props();
</script>

<Card.Root class="mx-auto mt-6 max-w-md">
	<Card.Header>
		<Card.Title class="text-center text-xl">Crear una cuenta</Card.Title>
	</Card.Header>
	<Card.Content>
		<FormRegister data={data.form} />
	</Card.Content>
	<Card.Footer>
		<p>Ya tenés cuenta? <a class="underline" href="/login">Iniciá sesión</a></p>
	</Card.Footer>
</Card.Root>
