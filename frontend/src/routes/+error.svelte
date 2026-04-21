<script>
	import { dev } from '$app/environment';
	import { page } from '$app/stores';
	import SubTitle from '$components/common/subtitle.svelte';
	import Title from '$components/common/title.svelte';
	import SuperDebug from 'sveltekit-superforms';
</script>

{#if $page.status === 404}
	<Title>404</Title>
	<SubTitle>La página que buscas no existe.</SubTitle>
{:else}
	<Title>Hubo un error inesperado!</Title>
	<SubTitle>{$page.status}: {$page.error?.message}</SubTitle>
{/if}

<div class="text-center">
	<a href="/" class="text-blue-600">Volver al inicio</a>
</div>

{#if dev}
	<div class="mx-auto mt-8 max-w-lg">
		<SuperDebug data={$page} label="Error recibido" />
	</div>
{/if}
