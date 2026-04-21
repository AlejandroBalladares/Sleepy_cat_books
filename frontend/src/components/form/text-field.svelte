<script lang="ts">
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import type { HTMLInputAttributes } from 'svelte/elements';
	import type { InputConstraint } from 'sveltekit-superforms';
	import ErrorLabel from './error-label.svelte';

	type Props = HTMLInputAttributes & {
		label?: string;
		errors: string[] | undefined;
		constraints?: InputConstraint;
		name: string;
		value: string | null | undefined;
	};

	let {
		value = $bindable(),
		label,
		errors,
		constraints,
		name,
		type = 'text',
		...restProps
	}: Props = $props();
	let id = restProps.id || name;
</script>

<div>
	{#if label}
		<Label for={id}>{label}</Label>
	{/if}

	<Input
		{type}
		bind:value
		aria-invalid={errors ? 'true' : undefined}
		{name}
		{id}
		{...constraints}
		{...restProps}
	/>
	<ErrorLabel error={errors} />
</div>
