<script lang="ts">
	import CatIcon from '$components/cat-icon.svelte';
	import type { RatingCreate } from '$models/ratings';
	import { superForm, type SuperValidated } from 'sveltekit-superforms';
	import { enhance } from '$app/forms';
	import { toast } from 'svelte-sonner';

	let { data }: { data: SuperValidated<RatingCreate> } = $props();

	const { form } = superForm(data, {
		onUpdated: ({ form }) => {
			if (form.message) {
				toast.success(form.message);
			} else if (form.errors) {
				var msg = (form.errors._errors && form.errors._errors[0]) || 'Error desconocido';
				toast.error(msg);
			}
		}
	});

	let isSubmitting = $state(false);

	let confirmedRating = $state($form.puntuacion);
	let hoverRating = $state(0);
	let deleteRating = $state(false);

	let formElement: HTMLFormElement;

	function pickAction() {
		if (confirmedRating == 0) {
			return '?/createRating';
		} else if (!deleteRating) {
			return '?/updateRating';
		} else {
			return '?/deleteRating';
		}
	}

	function handleClick(event: MouseEvent) {
		const input = event.target as HTMLInputElement;
		const newRating = Number(input.value);

		if (confirmedRating == newRating) {
			deleteRating = true;
		}

		formElement.action = pickAction();

		formElement.requestSubmit();
	}
</script>

{@render ratingSection()}

{#snippet ratingSection()}
	<form
		method="post"
		action={pickAction()}
		class="mb-5 space-y-6"
		use:enhance={() => {
			isSubmitting = true;
			return async ({ update, result }) => {
				isSubmitting = false;

				if (result.type == 'success') {
					confirmedRating = $form.puntuacion;
					if (deleteRating) {
						confirmedRating = 0;
						deleteRating = false;
					}
				}

				await update({ reset: true });
			};
		}}
		bind:this={formElement}
	>
		<div class="flex justify-between">
			{#each Array(5) as _, i}
				{console.log(_)}
				<label style="cursor: pointer;">
					<input
						disabled={isSubmitting}
						name="puntuacion"
						value={i + 1}
						type="radio"
						bind:group={$form.puntuacion}
						onclick={handleClick}
						style="display: none;"
					/>
					<CatIcon
						onmouseenter={() => (hoverRating = i + 1)}
						onmouseleave={() => (hoverRating = 0)}
						fill={i + 1 <= (hoverRating || confirmedRating) ? '#ffc107' : 'grey'}
						size={35}
					/>
				</label>
			{/each}
		</div>
	</form>
{/snippet}
