<script lang="ts">
	import { dev } from '$app/environment';
	import ErrorDialog from '$components/form/error-dialog.svelte';
	import ErrorLabel from '$components/form/error-label.svelte';
	import SubmitButton from '$components/form/submit-button.svelte';
	import TextField from '$components/form/text-field.svelte';
	import PasswordField from '$components/password-field.svelte';
	import Label from '$lib/components/ui/label/label.svelte';
	import * as RadioGroup from '$lib/components/ui/radio-group';
	import type { UserRegister } from '$models/user';
	import SuperDebug, { dateProxy, superForm, type SuperValidated } from 'sveltekit-superforms';

	let { data }: { data: SuperValidated<UserRegister> } = $props();
	const { form, constraints, errors, enhance, submitting } = superForm(data);
	const proxyFechaNacimiento = dateProxy(form, 'fecha_nacimiento', { format: 'date' });
</script>

<form method="post" action="?/register" class="space-y-6" use:enhance>
	<div class="flex justify-between">
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
	<div class="flex">
		<TextField
			name="nombre_de_usuario"
			label="Nombre de Usuario"
			errors={$errors.nombre_de_usuario}
			constraints={$constraints.nombre_de_usuario}
			bind:value={$form.nombre_de_usuario}
		/>
		<div class="ml-8 self-center">
			<Label for="rol">Rol</Label>
			<RadioGroup.Root bind:value={$form.rol} class="mt-2 flex items-center">
				<div>
					<RadioGroup.Item value="LECTOR" id="lector" />
					<label for="lector">Lector</label>
				</div>
				<div>
					<RadioGroup.Item value="AUTOR" id="autor" class="ml-4" />
					<label for="autor">Autor</label>
				</div>
			</RadioGroup.Root>
		</div>
	</div>
	<TextField
		name="fecha_nacimiento"
		label="Fecha de Nacimiento"
		type="date"
		errors={$errors.fecha_nacimiento}
		constraints={$constraints.fecha_nacimiento}
		bind:value={$proxyFechaNacimiento}
	/>
	<TextField
		name="email"
		label="Correo Electrónico"
		type="email"
		errors={$errors.email}
		constraints={$constraints.email}
		bind:value={$form.email}
	/>
	<div>
		<Label for="contraseña">Contraseña</Label>
		<PasswordField {form} {constraints} name="contraseña" />
		<ErrorLabel error={$errors.contraseña} />
	</div>
	<div>
		<Label for="confirmPassword">Repetir Contraseña</Label>
		<PasswordField {form} {constraints} name="confirmPassword" />
		<ErrorLabel error={$errors.confirmPassword} />
	</div>

	{#if $errors._errors}
		<ErrorDialog title="Error al iniciar sesión" description={$errors._errors.join('\n')} />
	{/if}

	<SubmitButton disabled={$submitting}>Registrarse</SubmitButton>
</form>

{#if dev}
	<SuperDebug data={$form} label="Contenido del formulario" />
{/if}
