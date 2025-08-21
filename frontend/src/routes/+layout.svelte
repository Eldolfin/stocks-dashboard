<script lang="ts">
	import '../app.css';
	import { client } from '$lib/typed-fetch-client';
	import EnhancedSidebar from '$lib/components/EnhancedSidebar.svelte';
	import { onMount } from 'svelte';
	import { setUserContext } from '$lib/contexts/user.svelte';

	let user = setUserContext();

	onMount(async () => {
		try {
			const { data, error: err } = await client.GET('/api/user');
			if (data) {
				user.profilePicture = data.profile_picture
					? `/api/profile/pictures/${data.profile_picture}`
					: null;
				user.loggedIn = true;
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
			user.logout();
		} catch (error) {
			console.error('Logout failed:', error);
		}
	}

	let { children } = $props();
</script>

<div class="flex min-h-screen">
	<!-- Enhanced Sidebar -->
	<EnhancedSidebar {user} {handleLogout} />

	<!-- Main Content -->
	<main class="flex-1 bg-gradient-to-br from-[#0a0f1c] to-[#1c2b4a] px-4 py-6 sm:px-6">
		{@render children()}
	</main>
</div>
