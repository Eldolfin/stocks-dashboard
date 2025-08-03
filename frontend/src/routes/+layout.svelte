<script lang="ts">
	import '../app.css';
	import { client } from '$lib/typed-fetch-client';
	import { goto, invalidate } from '$app/navigation';
	import { onMount } from 'svelte';
	import { baseUrl } from '../lib/typed-fetch-client';

	let { data, children } = $props();

	async function handleLogout() {
		try {
			await client.POST('/api/logout');
			data.isLoggedIn = false;
			data.userProfilePicture = null;
			invalidate('data:user_auth');
		} catch (error) {
			console.error('Logout failed:', error);
		}
	}
</script>

<div class="flex min-h-screen flex-col lg:flex-row">
	<!-- Sidebar -->
	<aside
		class="flex w-full flex-row items-center justify-around bg-gradient-to-b from-[#0a0f1c] to-[#141e30] py-4 shadow-lg lg:w-20 lg:flex-col lg:justify-start lg:space-y-6 lg:py-6"
	>
		{#if data.userProfilePicture}
			<div class="h-8 w-8 overflow-hidden rounded-full shadow-inner">
				<img src={data.userProfilePicture} alt="Profile" class="h-full w-full object-cover" />
			</div>
		{:else}
			<div class="bg-brand h-8 w-8 animate-pulse rounded-full shadow-inner"></div>
		{/if}
		<a href="/" title="Home" class="transition-transform hover:scale-110">🏠</a>
		<a href="/portfolio" title="Portfolio" class="transition-transform hover:scale-110">📊</a>
		{#if data.isLoggedIn}
			<button onclick={handleLogout} title="Logout" class="transition-transform hover:scale-110"
				>🔓</button
			>
		{:else}
			<a href="/login" title="Login" class="transition-transform hover:scale-110">🔐</a>
			<a href="/register" title="Register" class="transition-transform hover:scale-110">📝</a>
		{/if}
	</aside>

	<!-- Main -->
	<main class="flex-1 bg-gradient-to-br from-[#0a0f1c] to-[#1c2b4a] px-4 py-6 sm:px-6">
		{@render children()}
	</main>
</div>
