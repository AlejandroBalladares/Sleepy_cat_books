<script lang="ts">
	import { page } from '$app/stores';
	// import DarkmodeToggle from '$components/darkmode-toggle.svelte';
	import logo from '$lib/assets/logo.png';
	import NavLink from './nav-link.svelte';
</script>

<header class="flex items-center justify-around bg-blue-600 p-6 dark:bg-slate-700">
	<a class="text-2xl font-bold text-white" href="/">
		<img src={logo} alt="Logo Sleepy Cat Books" class="logo" />
		Sleepy Cat Books
	</a>
	<nav class="space-x-4">
		{#if !$page.data.user}
			<NavLink href="/login">Iniciar Sesión</NavLink>
			<NavLink href="/register">Registrarse</NavLink>
		{:else}
			<NavLink href="/books">Libros</NavLink>
			<NavLink href="/communities">Comunidades</NavLink>
			<NavLink href="/library">Librería</NavLink>
			<NavLink href="/profile">Perfil</NavLink>
			<NavLink href="/logout">Cerrar Sesión</NavLink>
		{/if}
		<!-- <DarkmodeToggle /> -->
	</nav>
</header>

<style type="text/css">
	.logo {
		width: 35px;
		height: auto;
		float: left;
		border-radius: 50%;
		margin-right: 10px;
		border: 1px solid #ccc;
		transition: transform 0.7s ease-in-out;
	}

	.logo:hover {
		transform: rotate(360deg);
	}
</style>
