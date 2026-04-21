<script lang="ts">
	import Title from '$components/common/title.svelte';
	import DarkmodeToggle from '$components/darkmode-toggle.svelte';
	import defaultIcon from '$lib/assets/default-profile.webp';
	import { Badge } from '$lib/components/ui/badge';
	import Button from '$lib/components/ui/button/button.svelte';
	import { localRole } from '$lib/store/role.js';

	let { data } = $props();
	const user = data.user;
	if (user.rol === 'LECTOR') {
		localRole.set('LECTOR');
	}

	// logica rol
	function toggleRole() {
		localRole.update((role) => (role === 'AUTOR' ? 'LECTOR' : 'AUTOR'));
	}
</script>

<Title>Perfil</Title>

{#if user.foto_de_perfil}
	<img class="profile-icon" src={user.foto_de_perfil} alt="Imagen de perfil" color="red" />
{:else}
	<img class="profile-icon" src={defaultIcon} alt="Imagen de perfil" color="red" />
{/if}

<p class="profile-name">{user.nombre} {user.apellido}</p>

<p class="profile-username">
	{user.nombre_de_usuario}
	<Badge>{$localRole}</Badge>
</p>

<p class="profile-birthdate">
	Fecha de nacimiento: {new Date(user.fecha_nacimiento).toLocaleDateString('es-AR')}
</p>

<p class="profile-description">{user.descripcion}</p>

<div class="text-center">Tema: <DarkmodeToggle /></div>

<div class="profile-edit">
	<Button href="/profile/edit">Editar perfil</Button>
</div>

{#if user.rol === 'AUTOR'}
	<div class="role-toggle">
		<Button onclick={toggleRole}>Cambiar a {$localRole === 'AUTOR' ? 'LECTOR' : 'AUTOR'}</Button>
	</div>
{/if}

<style type="text/css">
	.profile-icon {
		border-radius: 50%;
		justify-content: center;
		margin-left: auto;
		margin-right: auto;
		display: block;
		object-fit: scale-down;
		width: 200px;
		margin-top: 20px;
	}

	.profile-name {
		margin-top: 20px;
		font-size: larger;
		text-align: center;
		font-weight: bold;
	}

	.profile-username {
		font-size: larger;
		text-align: center;
		font-weight: bold;
	}

	.profile-birthdate {
		font-size: large;
		text-align: center;
	}

	.profile-description {
		font-size: large;
		text-align: center;
	}

	.profile-edit {
		justify-content: center;
		text-align: center;
		margin: auto;
		display: flex;
		display: grid;
		margin-top: 20px;
	}

	.role-toggle {
		justify-content: center;
		text-align: center;
		margin: auto;
		display: flex;
		display: grid;
		margin-top: 20px;
	}
</style>
