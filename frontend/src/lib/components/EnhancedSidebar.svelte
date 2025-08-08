<script lang="ts">
	import {
		HomeOutline,
		ChartOutline,
		UserOutline,
		ArrowRightToBracketOutline,
		ArrowLeftToBracketOutline,
		UserAddOutline,
		ArrowLeftOutline,
		ArrowRightOutline,
		CodeOutline
	} from 'flowbite-svelte-icons';
	import { isSidebarCollapsed } from '../stores/sidebarStore';

	// Props for authentication state
	let { isLoggedIn, userProfilePicture, handleLogout } = $props();

	// Toggle sidebar state
	function toggleSidebar() {
		isSidebarCollapsed.update((collapsed) => !collapsed);
	}

	let initialLoad = true;
	$effect(() => {
		// After the first render, set initialLoad to false
		// This ensures the transition class is only applied after the initial render
		initialLoad = false;
	});
</script>

<aside
	class="sticky top-0 flex h-screen flex-col bg-gradient-to-b from-[#0a0f1c] to-[#141e30] shadow-lg {initialLoad
		? ''
		: 'transition-all duration-300'} {$isSidebarCollapsed ? 'w-20' : 'w-64'}"
>
	<!-- Sidebar header with toggle button -->
	<div class="flex items-center justify-between border-b border-gray-700 p-4">
		{#if !$isSidebarCollapsed}
			<h2 class="text-xl font-bold text-white">Dashboard</h2>
		{/if}
		<button
			onclick={toggleSidebar}
			class="text-gray-300 hover:text-white focus:outline-none"
			title={$isSidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
			type="button"
		>
			{#if $isSidebarCollapsed}
				<ArrowRightOutline class="h-6 w-6" />
			{:else}
				<ArrowLeftOutline class="h-6 w-6" />
			{/if}
		</button>
	</div>

	<!-- Navigation items -->
	<nav class="mt-6 flex-1 space-y-1 px-2">
		<!-- Home link -->
		<a
			href="/"
			class="flex items-center rounded-lg p-3 text-gray-300 transition-colors duration-200 hover:bg-gray-700 hover:text-white"
			class:justify-center={$isSidebarCollapsed}
		>
			<HomeOutline class="h-6 w-6 flex-shrink-0" />
			{#if !$isSidebarCollapsed}
				<span class="ml-3 text-base font-medium">Home</span>
			{/if}
		</a>

		<!-- Portfolio link -->
		<a
			href="/portfolio"
			class="flex items-center rounded-lg p-3 text-gray-300 transition-colors duration-200 hover:bg-gray-700 hover:text-white"
			class:justify-center={$isSidebarCollapsed}
		>
			<ChartOutline class="h-6 w-6 flex-shrink-0" />
			{#if !$isSidebarCollapsed}
				<span class="ml-3 text-base font-medium">Portfolio</span>
			{/if}
		</a>

		<!-- API Documentation link -->
		<a
			href="/api/openapi/swagger"
			class="flex items-center rounded-lg p-3 text-gray-300 transition-colors duration-200 hover:bg-gray-700 hover:text-white"
			class:justify-center={$isSidebarCollapsed}
			target="_blank"
			rel="noopener noreferrer"
		>
			<CodeOutline class="h-6 w-6 flex-shrink-0" />
			{#if !$isSidebarCollapsed}
				<span class="ml-3 text-base font-medium">API Docs</span>
			{/if}
		</a>

		<!-- User Profile section -->
		<div class="mt-8 border-t border-gray-700 pt-8">
			{#if isLoggedIn}
				<!-- User Profile Picture -->
				<a
					href="/profile"
					class="flex items-center rounded-lg p-3 text-gray-300 transition-colors duration-200 hover:bg-gray-700 hover:text-white"
					class:justify-center={$isSidebarCollapsed}
				>
					{#if userProfilePicture}
						<img
							src={userProfilePicture}
							alt="User Profile"
							class="h-6 w-6 flex-shrink-0 rounded-full"
						/>
					{:else}
						<UserOutline class="h-6 w-6 flex-shrink-0" />
					{/if}
					{#if !$isSidebarCollapsed}
						<span class="ml-3 text-base font-medium">Profile</span>
					{/if}
				</a>
			{:else}
				<!-- User Profile link (when not logged in) -->
				<a
					href="/profile"
					class="flex items-center rounded-lg p-3 text-gray-300 transition-colors duration-200 hover:bg-gray-700 hover:text-white"
					class:justify-center={$isSidebarCollapsed}
				>
					<UserOutline class="h-6 w-6 flex-shrink-0" />
					{#if !$isSidebarCollapsed}
						<span class="ml-3 text-base font-medium">Profile</span>
					{/if}
				</a>
			{/if}

			<!-- Login/Logout/Register links -->
			{#if isLoggedIn}
				<!-- Logout link -->
				<button
					onclick={handleLogout}
					class="flex w-full items-center rounded-lg p-3 text-gray-300 transition-colors duration-200 hover:bg-gray-700 hover:text-white"
					class:justify-center={$isSidebarCollapsed}
				>
					<ArrowLeftToBracketOutline class="h-6 w-6 flex-shrink-0" />
					{#if !$isSidebarCollapsed}
						<span class="ml-3 text-base font-medium">Logout</span>
					{/if}
				</button>
			{:else}
				<!-- Login link -->
				<a
					href="/login"
					class="flex items-center rounded-lg p-3 text-gray-300 transition-colors duration-200 hover:bg-gray-700 hover:text-white"
					class:justify-center={$isSidebarCollapsed}
				>
					<ArrowRightToBracketOutline class="h-6 w-6 flex-shrink-0" />
					{#if !$isSidebarCollapsed}
						<span class="ml-3 text-base font-medium">Login</span>
					{/if}
				</a>

				<!-- Register link -->
				<a
					href="/register"
					class="flex items-center rounded-lg p-3 text-gray-300 transition-colors duration-200 hover:bg-gray-700 hover:text-white"
					class:justify-center={$isSidebarCollapsed}
				>
					<UserAddOutline class="h-6 w-6 flex-shrink-0" />
					{#if !$isSidebarCollapsed}
						<span class="ml-3 text-base font-medium">Register</span>
					{/if}
				</a>
			{/if}
		</div>
	</nav>
</aside>
