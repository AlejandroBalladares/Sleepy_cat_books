<script lang="ts">
	import ErrorLabel from '$components/form/error-label.svelte';
	import SubmitButton from '$components/form/submit-button.svelte';
	import Button from '$lib/components/ui/button/button.svelte';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import Textarea from '$lib/components/ui/textarea/textarea.svelte';
	import type { PostCreate } from '$models/posts';
	import { Plus, Trash } from 'lucide-svelte';
	import { superForm, type SuperValidated } from 'sveltekit-superforms';
	import { enhance } from '$app/forms';
	import { toast } from 'svelte-sonner';

	let { data, closeModal }: { data: SuperValidated<PostCreate>; closeModal: () => void } = $props();
	const { form, constraints, errors, submitting } = superForm(data, {
		onUpdated: ({ form }) => {
			if (form.message) {
				handleCloseForm();
				toast.success(form.message);
			} else if (form.errors) {
				var msg = (form.errors._errors && form.errors._errors[0]) || 'Error desconocido';
				toast.error(msg);
			}
		}
	});

	function handleCloseForm() {
		closeModal();
		$form.contenido = '';
	}

	function addField() {
		$form.imagenes = [...$form.imagenes, ''];
	}

	const removeField = (index: number) => () => {
		$form.imagenes = $form.imagenes.filter((_, i) => i !== index);
	};
</script>

<form method="post" action="?/createPost" class="space-y-6" use:enhance>
	<div>
		<Textarea
			name="contenido"
			id="contenido"
			bind:value={$form.contenido}
			{...$constraints.contenido}
			class="h-[10em] w-[40em] resize-none text-wrap p-2 text-lg"
		/>
		<ErrorLabel error={$errors.contenido} />
	</div>
	<div class="space-y-2">
		<Label for="imagenes">Imágenes</Label>
		{#each $form.imagenes as imagen, i}
			<div class="flex gap-x-2">
				<Input
					name="imagenes"
					id="imagenes-{i}"
					placeholder={imagen ? imagen : 'https://imagenes-' + (i + 1).toString() + '.com'}
					bind:value={$form.imagenes[i]}
					{...$constraints.imagenes}
				/>
				<Button
					type="button"
					disabled={i === 0}
					onclick={removeField(i)}
					variant="destructive"
					size="icon"
				>
					<Trash />
				</Button>
			</div>
			<ErrorLabel error={$errors.imagenes?.[i]} />
		{/each}

		<Button type="button" onclick={addField} size="icon"><Plus /></Button>
	</div>
	<div class="flex justify-between">
		<Button onclick={handleCloseForm}>Cerrar</Button>
		<SubmitButton disabled={$submitting}>Publicar</SubmitButton>
	</div>
</form>
