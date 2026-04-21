<script lang="ts">
	import { dev } from '$app/environment';
	import ErrorDialog from '$components/form/error-dialog.svelte';
	import ErrorLabel from '$components/form/error-label.svelte';
	import SubmitButton from '$components/form/submit-button.svelte';
	import SuccessDialog from '$components/form/success-dialog.svelte';
	import TextField from '$components/form/text-field.svelte';
	import TextareaField from '$components/form/textarea-field.svelte';
	import Button from '$lib/components/ui/button/button.svelte';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import type { BookEdit } from '$models/books';
	import { Plus, Trash } from 'lucide-svelte';
	import SuperDebug, { superForm, type SuperValidated } from 'sveltekit-superforms';

	let { data }: { data: SuperValidated<BookEdit> } = $props();

	const { form, constraints, errors, enhance, submitting, message } = superForm(data, {
		resetForm: false,
		dataType: 'json'
	});

	function addField() {
		if ($form.imagenes_ilustrativas.length < 3) {
			$form.imagenes_ilustrativas = [...$form.imagenes_ilustrativas, ''];
		}
	}

	const removeField = (index: number) => () => {
		// 🍛
		$form.imagenes_ilustrativas = $form.imagenes_ilustrativas.filter((_, i) => i !== index);
	};
</script>

<form method="post" action="?/editBook" class="space-y-6" use:enhance>
	<TextField
		label="Nombre"
		name="nombre"
		bind:value={$form.nombre}
		constraints={$constraints.nombre}
		errors={$errors.nombre}
	/>
	<TextareaField
		label="Descripción"
		name="descripcion"
		bind:value={$form.descripcion}
		constraints={$constraints.descripcion}
		errors={$errors.descripcion}
	/>
	<TextField
		label="Portada"
		name="portada"
		bind:value={$form.portada}
		constraints={$constraints.portada}
		errors={$errors.portada}
	/>

	<div class="space-y-2">
		<Label for="imagenes_ilustrativas">Imágenes ilustrativas</Label>
		{#each $form.imagenes_ilustrativas as imagen_ilustrativa, i}
			<div class="flex gap-x-2">
				<Input
					name="imagenes_ilustrativas"
					id="imagenes_ilustrativas-{i}"
					placeholder={imagen_ilustrativa
						? imagen_ilustrativa
						: 'https://imagenes-ilustrativas-' + (i + 1).toString() + '.com'}
					bind:value={$form.imagenes_ilustrativas[i]}
					{...$constraints.imagenes_ilustrativas}
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
			<ErrorLabel error={$errors.imagenes_ilustrativas?.[i]} />
		{/each}

		<Button
			type="button"
			onclick={addField}
			size="icon"
			disabled={$form.imagenes_ilustrativas.length >= 3}><Plus /></Button
		>
	</div>
	<SubmitButton disabled={$submitting}>Confirmar</SubmitButton>
</form>

{#if $errors._errors}
	<ErrorDialog title="Error" description={$errors._errors.join('\n')} />
{/if}

{#if $message}
	<SuccessDialog title="Éxito" description={$message} />
{/if}

{#if dev}
	<SuperDebug data={$form} label="Contenido del formulario" />
{/if}
