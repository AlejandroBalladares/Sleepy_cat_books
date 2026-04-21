<script lang="ts">
	import { dev } from '$app/environment';
	import ErrorDialog from '$components/form/error-dialog.svelte';
	import SubmitButton from '$components/form/submit-button.svelte';
	import SuccessDialog from '$components/form/success-dialog.svelte';
	import TextField from '$components/form/text-field.svelte';
	import TextareaField from '$components/form/textarea-field.svelte';
	import type { UserEdit } from '$models/user';
	import SuperDebug, { superForm, type SuperValidated } from 'sveltekit-superforms';

	let { data }: { data: SuperValidated<UserEdit> } = $props();

	const { form, constraints, errors, enhance, submitting, message } = superForm(data);
</script>

<!-- Cambiar method a patch? -->
<!-- Los forms en html solo aceptan POST y GET -->
<form method="post" action="?/editProfile" class="space-y-6" use:enhance>
	<div class="flex justify-between gap-x-4">
		<TextField
			name="nombre"
			label="Nombre"
			errors={$errors.nombre}
			constraints={$constraints.nombre}
			bind:value={$form.nombre}
		/>
		<TextField
			name="apellido"
			label="Apellido"
			errors={$errors.apellido}
			constraints={$constraints.apellido}
			bind:value={$form.apellido}
		/>
	</div>
	<TextField
		name="email"
		label="Correo Electrónico"
		type="email"
		errors={$errors.email}
		constraints={$constraints.email}
		bind:value={$form.email}
	/>
	<TextField
		label="Foto de Perfil"
		name="foto_de_perfil"
		bind:value={$form.foto_de_perfil}
		constraints={$constraints.foto_de_perfil}
		errors={$errors.foto_de_perfil}
		placeholder="https://foto.com"
	/>
	<TextareaField
		label="Descripción"
		name="descripcion"
		bind:value={$form.descripcion}
		constraints={$constraints.descripcion}
		errors={$errors.descripcion}
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
