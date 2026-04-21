<script lang="ts">
	import { dev } from '$app/environment';
	import ErrorDialog from '$components/form/error-dialog.svelte';
	import ErrorLabel from '$components/form/error-label.svelte';
	import SubmitButton from '$components/form/submit-button.svelte';
	import TextField from '$components/form/text-field.svelte';
	import PasswordField from '$components/password-field.svelte';
	import { Label } from '$lib/components/ui/label';
	import type { UserLogin } from '$models/user';
	import SuperDebug, { superForm, type SuperValidated } from 'sveltekit-superforms';

	let { data }: { data: SuperValidated<UserLogin> } = $props();
	const { form, constraints, errors, enhance, submitting } = superForm(data);
</script>

<form method="post" action="?/login" class="space-y-6" use:enhance>
	<TextField
		label="E-mail"
		type="email"
		name="username"
		placeholder="jkrowling@magician.com"
		bind:value={$form.username}
		constraints={$constraints.username}
		errors={$errors.username}
	/>
	<div>
		<Label for="password">Contraseña</Label>
		<PasswordField {form} {constraints} />
		<ErrorLabel error={$errors.password} />
	</div>

	{#if $errors._errors}
		<ErrorDialog title="Error al iniciar sesión" description={$errors._errors.join('\n')} />
	{/if}

	<SubmitButton disabled={$submitting}>Iniciar Sesión</SubmitButton>
</form>

<SuperDebug data={$form} label="Contenido del formulario" display={dev} />
