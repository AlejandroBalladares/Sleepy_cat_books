<script lang="ts">
	import * as Avatar from '$lib/components/ui/avatar';
	let { foto_de_perfil, nombre }: { foto_de_perfil?: string; nombre: string } = $props();
	const iniciales = nombre
		.split(' ')
		.map((n) => n[0].toUpperCase())
		.join('');
</script>

<Avatar.Root>
	<Avatar.Image src={foto_de_perfil} alt="profile avatar" />
	<Avatar.Fallback>{iniciales}</Avatar.Fallback>
</Avatar.Root>
