<script lang="ts">
	import { enhance } from '$app/forms';
	import SubmitButton from '$components/form/submit-button.svelte';
	import TextareaField from '$components/form/textarea-field.svelte';
	import Button from '$lib/components/ui/button/button.svelte';
	import type { ReviewCreate } from '$models/reviews';
	import { toast } from 'svelte-sonner';
	import { superForm, type SuperValidated } from 'sveltekit-superforms';

	let { data, closeModal }: { data: SuperValidated<ReviewCreate>; closeModal: () => void } =
		$props();
	const {
		form: reviewForm,
		constraints,
		errors,
		submitting
	} = superForm(data, {
		onUpdated: ({ form }) => {
			if (form.message) {
				handleCloseReview();
				toast.success(form.message);
			} else if (form.errors) {
				var msg = (form.errors._errors && form.errors._errors[0]) || 'Error desconocido';
				toast.error(msg);
			}
		}
	});

	function handleCloseReview() {
		closeModal();
		$reviewForm.contenido = '';
	}
</script>

<form method="post" action="?/createReview" class="space-y-6" use:enhance>
	<TextareaField
		name="contenido"
		bind:value={$reviewForm.contenido}
		constraints={$constraints.contenido}
		errors={$errors.contenido}
		class="h-[10em] w-[40em] resize-none text-wrap p-2 text-lg"
		placeholder="Deje su opinión"
	/>
	<div class="flex justify-between">
		<Button onclick={handleCloseReview}>Cerrar</Button>
		<SubmitButton disabled={$submitting}>Publicar</SubmitButton>
	</div>
</form>
