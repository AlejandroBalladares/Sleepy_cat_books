<script lang="ts">
	import * as Avatar from '$lib/components/ui/avatar';
	let { logo, nombre }: { logo?: string | null; nombre: string } = $props();
	const iniciales = nombre
		.split(' ')
		.map((n) => n[0].toUpperCase())
		.join('');
</script>

<Avatar.Root>
	<Avatar.Image src={logo} alt="profile avatar" />
	<Avatar.Fallback>{iniciales}</Avatar.Fallback>
</Avatar.Root>
