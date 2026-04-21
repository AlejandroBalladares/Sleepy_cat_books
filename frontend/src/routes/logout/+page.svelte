<script>
	import SubmitButton from '$components/form/submit-button.svelte';
</script>

<div class="m-auto mt-6 max-w-md rounded-lg border p-6 shadow-md">
	<form method="POST" action="?/logout" class="space-y-4">
		<p>¿Seguro que quieres cerrar sesión?</p>
		<SubmitButton disabled={false}>Cerrar Sesión</SubmitButton>
	</form>
</div>
