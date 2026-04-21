<script lang="ts">
	import { Label } from '$lib/components/ui/label';
	import Textarea from '$lib/components/ui/textarea/textarea.svelte';
	import type { HTMLTextareaAttributes } from 'svelte/elements';
	import type { InputConstraint } from 'sveltekit-superforms';
	import ErrorLabel from './error-label.svelte';

	type Props = HTMLTextareaAttributes & {
		label?: string;
		errors: string[] | undefined;
		constraints?: InputConstraint;
		name: string;
		value: string | null | undefined;
	};

	let { value = $bindable(), label, errors, constraints, name, ...restProps }: Props = $props();
	let id = restProps.id || name;
</script>

<div>
	{#if label}
		<Label for={id}>{label}</Label>
	{/if}

	<Textarea
		bind:value
		aria-invalid={errors ? 'true' : undefined}
		{name}
		{id}
		{...constraints}
		{...restProps}
	/>
	<ErrorLabel error={errors} />
</div>
