<script lang="ts">
	import { dev } from '$app/environment';
	import { enhance } from '$app/forms';
	import Title from '$components/common/title.svelte';
	import ErrorDialog from '$components/form/error-dialog.svelte';
	import SuccessDialog from '$components/form/success-dialog.svelte';
	import ErrorLabel from '$components/form/error-label.svelte';
	import SubmitButton from '$components/form/submit-button.svelte';
	import * as Card from '$lib/components/ui/card';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import * as Select from '$lib/components/ui/select';
	import { Textarea } from '$lib/components/ui/textarea';
	import SuperDebug, { dateProxy, superForm } from 'sveltekit-superforms';

	let isSubmitting = $state(false);
	let { data } = $props();
	const { form, constraints, errors, message } = superForm(data.form);
	const proxyFechaPublicacion = dateProxy(form, 'fecha_publicacion', { format: 'date' });
	const genres = data.genres;
</script>

<Title>Crear nuevo libro</Title>

<Card.Root class="mx-auto mt-6 max-w-md">
	<Card.Header>
		<Card.Title class="text-center text-xl">Completa los campos</Card.Title>
	</Card.Header>
	<Card.Content>
		{@render bookCreateForm()}
	</Card.Content>
	<Card.Footer></Card.Footer>
</Card.Root>

{#if dev}
	<SuperDebug data={$form} label="Contenido del formulario" />
{/if}

{#snippet bookCreateForm()}
	<form
		method="post"
		action="?/new"
		class="space-y-6"
		use:enhance={() => {
			isSubmitting = true;

			return async ({ update }) => {
				await update();
				isSubmitting = false;
			};
		}}
	>
		<div>
			<Label for="nombre">Nombre</Label>
			<Input
				name="nombre"
				id="nombre"
				placeholder="Don Quijote de la Mancha"
				bind:value={$form.nombre}
				{...$constraints.nombre}
			/>
			<ErrorLabel error={$errors.nombre} />
		</div>
		<div>
			<Label for="isbn">ISBN</Label>
			<Input
				name="isbn"
				id="isbn"
				type="number"
				placeholder="9789295055025"
				bind:value={$form.isbn}
				{...$constraints.isbn}
			/>
			<ErrorLabel error={$errors.isbn} />
		</div>
		<div>
			<Label for="fecha_publicacion">Fecha de Publicación</Label>
			<Input
				name="fecha_publicacion"
				id="fecha_publicacion"
				type="date"
				bind:value={$proxyFechaPublicacion}
				{...$constraints.fecha_publicacion}
			/>
			<ErrorLabel error={$errors.fecha_publicacion} />
		</div>
		<div>
			<Label for="portada">Portada</Label>
			<Input name="portada" id="portada" bind:value={$form.portada} {...$constraints.portada} />
			<ErrorLabel error={$errors.portada} />
		</div>
		<div>
			<Label for="descripcion">Descripción</Label>
			<Textarea
				name="descripcion"
				id="descripcion"
				bind:value={$form.descripcion}
				{...$constraints.descripcion}
			/>
			<ErrorLabel error={$errors.descripcion} />
		</div>
		<div>
			<Label for="generos">Generos</Label>
			<Select.Root
				bind:value={$form.generos}
				name="generos"
				{...$constraints.generos}
				type="multiple"
			>
				<Select.Trigger class="w-full">
					{$form.generos.length === 0
						? 'Selecciona uno o más géneros'
						: $form.generos.map((nombre) => {
								const genre = genres.find((g) => g.nombre === nombre);
								return genre!.nombre;
							})}
				</Select.Trigger>
				<Select.Content>
					{#each genres as genre}
						<Select.Item value={genre.nombre}>{genre.nombre}</Select.Item>
					{/each}
				</Select.Content>
			</Select.Root>
			<ErrorLabel error={$errors.generos?._errors} />
		</div>
		{#if $errors._errors}
			<ErrorDialog title="Error al crear el libro" description={$errors._errors.join('\n')} />
		{/if}
		{#if $message}
			<SuccessDialog title="Éxito" description={$message} />
		{/if}
		<SubmitButton disabled={isSubmitting}>Crear</SubmitButton>
	</form>
{/snippet}
