<script lang="ts">
	import { dev } from '$app/environment';
	import ErrorDialog from '$components/form/error-dialog.svelte';
	import SubmitButton from '$components/form/submit-button.svelte';
	import SuccessDialog from '$components/form/success-dialog.svelte';
	import TextField from '$components/form/text-field.svelte';
	import TextareaField from '$components/form/textarea-field.svelte';
	import type { CommunityEdit } from '$models/communities';
	import SuperDebug, { superForm, type SuperValidated } from 'sveltekit-superforms';

	let { data }: { data: SuperValidated<CommunityEdit> } = $props();

	const { form, constraints, errors, enhance, submitting, message } = superForm(data, {
		resetForm: false,
		dataType: 'json'
	});
</script>

<form method="post" action="?/editCommunity" class="space-y-6" use:enhance>
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
		label="Logo"
		name="imagen"
		bind:value={$form.imagen}
		constraints={$constraints.imagen}
		errors={$errors.imagen}
	/>
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
