
<script lang="ts">
    import "../app.css";
    import { client } from '$lib/typed-fetch-client';
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { baseUrl } from '../lib/typed-fetch-client';

    let isLoggedIn = false;
    let userProfilePicture: string | null = null;

    async function fetchUserProfile() {
        try {
            const response = await client.GET('/api/user');
            if (response.data) {
                userProfilePicture = response.data.profile_picture ? `${baseUrl}/api/profile/pictures/${response.data.profile_picture}` : null;
                isLoggedIn = true;
            } else if (response.error) {
                isLoggedIn = false;
                userProfilePicture = null;
            }
        } catch (error) {
            console.error('Failed to fetch user profile:', error);
            isLoggedIn = false;
            userProfilePicture = null;
        }
    }

    onMount(() => {
        fetchUserProfile();
    });

    async function handleLogout() {
        try {
            await client.POST('/api/logout');
            isLoggedIn = false;
            userProfilePicture = null;
            goto('/login');
        } catch (error) {
            console.error('Logout failed:', error);
        }
    }
</script>

<div class="flex flex-col lg:flex-row min-h-screen">
    <!-- Sidebar -->
    <aside class="lg:w-20 w-full flex lg:flex-col flex-row items-center justify-around lg:justify-start lg:space-y-6 py-4 lg:py-6 bg-gradient-to-b from-[#0a0f1c] to-[#141e30] shadow-lg">
        {#if userProfilePicture}
            <div class="w-8 h-8 rounded-full overflow-hidden shadow-inner">
                <img src={userProfilePicture} alt="Profile" class="w-full h-full object-cover" />
            </div>
        {:else}
            <div class="w-8 h-8 bg-brand rounded-full shadow-inner animate-pulse"></div>
        {/if}
        <a href="/" title="Home" class="hover:scale-110 transition-transform">🏠</a>
        <a href="/portfolio" title="Portfolio" class="hover:scale-110 transition-transform">📊</a>
        {#if isLoggedIn}
            <button on:click={handleLogout} title="Logout" class="hover:scale-110 transition-transform">🔓</button>
        {:else}
            <a href="/login" title="Login" class="hover:scale-110 transition-transform">🔐</a>
            <a href="/register" title="Register" class="hover:scale-110 transition-transform">📝</a>
        {/if}
    </aside>

    <!-- Main -->
    <main class="flex-1 px-4 sm:px-6 py-6 bg-gradient-to-br from-[#0a0f1c] to-[#1c2b4a]">
        <slot />
    </main>
</div>
