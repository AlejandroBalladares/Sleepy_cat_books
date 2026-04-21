<script lang="ts">
	import FormLogin from '$components/forms/form-login.svelte';
	import * as Card from '$lib/components/ui/card';

	let { data } = $props();
</script>

<Card.Root class="mx-auto mt-6 max-w-md">
	<Card.Header>
		<Card.Title class="text-center text-xl">Iniciar Sesión</Card.Title>
	</Card.Header>
	<Card.Content>
		<FormLogin data={data.form} />
	</Card.Content>
	<Card.Footer>
		<p>¿No tenés cuenta? <a class="underline" href="/register">Registrate</a></p>
	</Card.Footer>
</Card.Root>
