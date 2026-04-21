<script lang="ts">
	import FormEditBook from '$components/forms/form-edit-book.svelte';
	import * as Card from '$lib/components/ui/card';

	let { data } = $props();
</script>

<Card.Root class="mx-auto mt-6 max-w-md">
	<Card.Header>
		<Card.Title class="text-center text-xl">Editar Libro</Card.Title>
	</Card.Header>
	<Card.Content>
		<FormEditBook data={data.form} />
	</Card.Content>
</Card.Root>
