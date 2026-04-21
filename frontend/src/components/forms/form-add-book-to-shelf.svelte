<script lang="ts">
	import * as Select from '$lib/components/ui/select';
	import type { Shelf } from '$models/library';
	import { toast } from 'svelte-sonner';
	import { superForm, type SuperValidated } from 'sveltekit-superforms/client';

	let { shelves, data }: { shelves: Shelf[]; data: SuperValidated<Shelf> } = $props();
	const { form, submitting, enhance } = superForm(data, {
		onUpdated: ({ form }) => {
			if (form.message) {
				toast.success(form.message);
			} else if (form.errors) {
				var msg = (form.errors._errors && form.errors._errors[0]) || 'Error desconocido';
				toast.error(msg);
			}
		}
	});

	let formElementAddToShelf: HTMLFormElement;
	let selectedShelf = $state('');

	const handleSubmit = () => {
		$form.nombre = selectedShelf;
		formElementAddToShelf.requestSubmit();
	};
</script>

<form
	bind:this={formElementAddToShelf}
	method="post"
	action="?/addToShelf"
	class="space-y-6"
	use:enhance
>
	<input type="hidden" name="nombre" bind:value={selectedShelf} />

	<Select.Root type="single" name="shelf" allowDeselect={false} bind:value={selectedShelf}>
		<Select.Trigger class="w-[180px]">Agregar a</Select.Trigger>
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
