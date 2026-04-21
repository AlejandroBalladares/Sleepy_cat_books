<script lang="ts">
	import { dev } from '$app/environment';
	import ErrorDialog from '$components/form/error-dialog.svelte';
	import ErrorLabel from '$components/form/error-label.svelte';
	import SubmitButton from '$components/form/submit-button.svelte';
	import SuccessDialog from '$components/form/success-dialog.svelte';
	import TextField from '$components/form/text-field.svelte';
	import { Label } from '$lib/components/ui/label';
	import { Textarea } from '$lib/components/ui/textarea';
	import type { CommunityCreate } from '$models/communities';
	import SuperDebug, { superForm, type SuperValidated } from 'sveltekit-superforms';

	let { data }: { data: SuperValidated<CommunityCreate> } = $props();

	const { form, constraints, errors, enhance, submitting, message } = superForm(data);
</script>

<form method="post" action="?/new" class="space-y-6" use:enhance>
	<TextField
		label="Nombre"
		name="nombre"
		bind:value={$form.nombre}
		constraints={$constraints.nombre}
		errors={$errors.nombre}
	/>
	<TextField
		label="Logo"
		name="imagen"
		bind:value={$form.imagen}
		constraints={$constraints.imagen}
		errors={$errors.imagen}
	/>
	<div>
		<Label for="descripcion">Descripción</Label>
		<Textarea
			name="descripcion"
			id="descripcion"
			placeholder="La mejor comunidad..."
			bind:value={$form.descripcion}
			{...$constraints.descripcion}
		/>
		<ErrorLabel error={$errors.descripcion} />
	</div>

	<SubmitButton disabled={$submitting}>Crear</SubmitButton>
</form>

{#if $errors._errors}
	<ErrorDialog title="Error al crear la comunidad" description={$errors._errors.join('\n')} />
{/if}

{#if $message}
	<SuccessDialog title="Éxito" description={$message} />
{/if}

{#if dev}
	<SuperDebug data={$form} label="Contenido del formulario" />
{/if}
