<script lang="ts">
	import { Input } from '$lib/components/ui/input';
	import { Eye, EyeClosed } from 'lucide-svelte';

	let passwordType = $state<'text' | 'password'>('password');
	const togglePasswordVisibility = () => {
		passwordType = passwordType === 'password' ? 'text' : 'password';
	};

	let { form, constraints, name = 'password' } = $props();
</script>

<div class="relative">
	<Input
		type={passwordType}
		{name}
		id={name}
		placeholder="*******"
		bind:value={$form[name]}
		{...$constraints[name]}
	/>
	{#if passwordType === 'password'}
		<EyeClosed
			class="absolute right-3 top-2.5 cursor-pointer text-gray-700"
			size={20}
			onclick={togglePasswordVisibility}
		/>
	{:else}
		<Eye
			class="absolute right-3 top-2.5 cursor-pointer text-gray-700"
			size={20}
			onclick={togglePasswordVisibility}
		/>
	{/if}
</div>
