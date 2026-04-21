<script lang="ts">
	import type { Post } from '$models/posts';
	import UserAvatar from './user-avatar.svelte';
	let { post }: { post: Post } = $props();
	let currentImage = $state(0);
	console.log('fecha', post.fecha);

	function plusImage(n: number) {
		let len = post.imagenes.length;
		let res = currentImage + n;

		if (res >= len) {
			currentImage = 0;
		} else if (res < 0) {
			currentImage = len - 1;
		} else {
			currentImage = res;
		}
	}
</script>

<div class="community-post">
	<div class="post-text gap-x-3">
		<UserAvatar
			foto_de_perfil={post.usuario.foto_de_perfil}
			nombre={post.usuario.nombre_de_usuario}
		/>
		<div>
			<p class="text-lg font-bold">{post.usuario.nombre_de_usuario}</p>
			<p class="community-post-date">
				{new Date(post.fecha + 'Z').toLocaleString('es-AR', {
					hour12: false,
					dateStyle: 'medium',
					timeStyle: 'short'
				})}
			</p>
			<p class="community-post-content">{post.contenido}</p>
		</div>
	</div>
	{#if post.imagenes.length > 0}
		<div class="post-image-container">
			<div class="post-image-number">{currentImage + 1} / {post.imagenes.length}</div>
			<img
				class="community-post-image-background"
				src={post.imagenes[currentImage].url}
				alt="{post.usuario.nombre_de_usuario}-{post.fecha}-background-image-{post.imagenes[
					currentImage
				].id}"
			/>
			<img
				class="community-post-image"
				src={post.imagenes[currentImage].url}
				alt="{post.usuario.nombre_de_usuario}-{post.fecha}-image-{post.imagenes[currentImage].id}"
			/>
			{#if post.imagenes.length > 1}
				<button class="prev-image" onclick={() => plusImage(-1)}>&#10094;</button>
				<button class="next-image" onclick={() => plusImage(1)}>&#10095;</button>
			{/if}
		</div>
	{/if}
</div>

<style type="text/css">
	.community-post {
		border: 1px solid #ccc;
		padding: 10px 40px 10px 10px;
		border-radius: 5px;
		margin: 5px;
		width: 100%;
		min-width: fit-content;
	}

	.post-text {
		display: flex;
	}

	.community-post-content {
		text-align: justify;
		font-size: 18px;
		max-width: 100%;
	}

	.community-post-date {
		color: #888888;
		font-size: 12px;
	}

	.community-post-image {
		width: 100%;
		object-fit: contain;
		max-height: 100%;
		display: flex;
		min-height: 100%;
		min-width: 100%;
	}

	.community-post-image-background {
		filter: blur(64px);
		z-index: -1;
		position: absolute;
		width: 100%;
		min-width: 100%;
		height: 400px;
		object-fit: cover;
	}

	.post-image-container {
		border: 1px solid #ccc;
		position: relative;
		overflow: hidden;
		display: flex;
		align-items: center;
		height: 400px;
		width: 100%;
		min-width: 500px;
		border-radius: 0.5%;
		margin: 5px 0px 0px 5px;
	}

	.prev-image,
	.next-image {
		cursor: pointer;
		position: absolute;
		top: 50%;
		width: auto;
		margin-top: -22px;
		padding: 16px;
		font-weight: bold;
		font-size: 18px;
		transition: 0.6s ease;
		border-radius: 0 3px 3px 0;
		user-select: none;
	}

	.next-image {
		right: 0;
		border-radius: 3px 0 0 3px;
	}

	.post-image-number {
		font-size: 14px;
		padding: 8px 12px;
		position: absolute;
		top: 0;
		opacity: 90%;
		border-radius: 50%;
	}
</style>
