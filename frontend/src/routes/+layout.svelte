<script lang="ts">
	import '../app.css';
	import { client } from '$lib/typed-fetch-client';
	import { invalidate } from '$app/navigation';
	import EnhancedSidebar from '$lib/components/EnhancedSidebar.svelte';

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

<div class="flex min-h-screen">
	<!-- Enhanced Sidebar -->
	<EnhancedSidebar
		isLoggedIn={data.isLoggedIn}
		userProfilePicture={data.userProfilePicture}
		{handleLogout}
	/>

	<!-- Main Content -->
	<main class="flex-1 bg-gradient-to-br from-[#0a0f1c] to-[#1c2b4a] px-4 py-6 sm:px-6">
		{@render children()}
	</main>
</div>
