<script lang="ts">
	import * as Select from '$lib/components/ui/select';
	import type { Shelf } from '$models/library';
	import { superForm, type SuperValidated } from 'sveltekit-superforms/client';

	let { shelves, data }: { shelves: Shelf[]; data: SuperValidated<Shelf> } = $props();
	const { form, submitting, enhance } = superForm(data);

	let formElementRemoveFromShelf: HTMLFormElement;
	let selectedShelf = $state('');

	const handleSubmit = () => {
		$form.nombre = selectedShelf;
		formElementRemoveFromShelf.requestSubmit();
	};
</script>

<form
	bind:this={formElementRemoveFromShelf}
	method="post"
	action="?/removeFromShelf"
	class="space-y-6"
	use:enhance
>
	<input type="hidden" name="nombre" bind:value={selectedShelf} />

	<Select.Root type="single" name="shelf" allowDeselect={false} bind:value={selectedShelf}>
		<Select.Trigger class="w-[180px]">Eliminar de</Select.Trigger>
		<Select.Content>
			<Select.Group>
				{#each shelves as shelf}
					<Select.Item
						value={shelf.nombre}
						class="cursor-pointer pl-4 [&>span]:hidden"
						onclick={handleSubmit}
						disabled={$submitting}
					>
						{shelf.nombre}
					</Select.Item>
				{/each}
			</Select.Group>
		</Select.Content>
	</Select.Root>
</form>
