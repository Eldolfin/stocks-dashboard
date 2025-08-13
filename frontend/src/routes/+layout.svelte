<script lang="ts">
	import '../app.css';
	import { client } from '$lib/typed-fetch-client';
	import { invalidate } from '$app/navigation';
	import EnhancedSidebar from '$lib/components/EnhancedSidebar.svelte';
	import { onMount } from 'svelte';

	let isLoggedIn = $state(false);
	let userProfilePicture: string | null = $state(null);

	onMount(async () => {
		try {
			const { data, error: err } = await client.GET('/api/user');
			if (data) {
				userProfilePicture = data.profile_picture
					? `/api/profile/pictures/${data.profile_picture}`
					: null;
				isLoggedIn = true;
			} else if (err) {
				// not logged in
			}
		} catch (e) {
			console.error('Failed to fetch user profile:', e);
		}
	});

	async function handleLogout() {
		try {
			await client.POST('/api/logout');
			isLoggedIn = false;
			userProfilePicture = null;
			invalidate('data:user_auth');
		} catch (error) {
			console.error('Logout failed:', error);
		}
	}

	let { children } = $props();
</script>

<div class="flex min-h-screen">
	<!-- Enhanced Sidebar -->
	<EnhancedSidebar
		isLoggedIn={isLoggedIn}
		userProfilePicture={userProfilePicture}
		{handleLogout}
	/>

	<!-- Main Content -->
	<main class="flex-1 bg-gradient-to-br from-[#0a0f1c] to-[#1c2b4a] px-4 py-6 sm:px-6">
		{@render children()}
	</main>
</div>
