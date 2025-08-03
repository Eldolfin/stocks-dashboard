<script lang="ts">
    import { client } from '$lib/typed-fetch-client';
    import { goto, invalidate } from '$app/navigation';
    import { Button, Label, Input } from 'flowbite-svelte';

    let email = '';
    let password = '';
    let errorMessage = '';

    async function handleLogin() {
        errorMessage = '';
        try {
            const response = await client.POST('/api/login', {
                body: {
                    email,
                    password
                }
            });

            if (response.error) {
                errorMessage = response.error.message || 'Login failed';
            } else if (response.data) {
                goto('/', {invalidate:["data:user_auth"]});
            }
        } catch (error) {
            errorMessage = 'An unexpected error occurred.';
            console.error('Login error:', error);
        }
    }
</script>

<div class="flex flex-col items-center justify-center min-h-screen">
    <form on:submit|preventDefault={handleLogin} class="w-full max-w-md p-8 space-y-6 rounded-lg shadow-md">
        <h2 class="text-2xl font-bold text-center text-gray-900 dark:text-white">Login</h2>

        {#if errorMessage}
            <p class="text-red-500 text-center">{errorMessage}</p>
        {/if}

        <div>
            <Label for="email" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Your email</Label>
            <Input type="email" id="email" bind:value={email} required class="w-full h-12 px-4 py-2" />
        </div>

        <div>
            <Label for="password" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Your password</Label>
            <Input type="password" id="password" bind:value={password} required class="w-full h-12 px-4 py-2" />
        </div>

        <Button type="submit" class="w-full">Login</Button>

        <p class="text-sm text-center text-gray-500 dark:text-gray-400">
            Don't have an account? <a href="/register" class="font-medium text-primary-600 hover:underline dark:text-primary-500">Register here</a>
        </p>
    </form>
</div>
