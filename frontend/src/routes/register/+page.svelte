<script lang="ts">
    import { client } from '$lib/typed-fetch-client';
    import { goto } from '$app/navigation';
    import { Button, Label, Input, Fileupload } from 'flowbite-svelte';
	import type { components } from '../../generated/api';

    let email = '';
    let password = '';
    let profilePicture: FileList | undefined = undefined;
    let errorMessage = '';
    let successMessage = '';

    async function handleRegister() {
        errorMessage = '';
        successMessage = '';

        const body: components["schemas"]["RegisterForm"] = {
            email,
            password,
            profile_picture: null
        };

        if (profilePicture && profilePicture.length > 0) {
            body.profile_picture = profilePicture[0] as any;
        }

        try {
            const response = await client.POST('/api/register', {
                body: body as any,
            });

            if (response.error) {
                errorMessage = (response.error as any).message || 'Registration failed';
            } else if (response.data) {
                successMessage = 'Registration successful! You can now log in.';
                goto('/login');
            }
        } catch (error) {
            errorMessage = 'An unexpected error occurred.';
            console.error('Registration error:', error);
        }
    }
</script>

<div class="flex flex-col items-center justify-center min-h-screen">
    <form on:submit|preventDefault={handleRegister} class="w-full max-w-md p-8 space-y-6 rounded-lg shadow-md">
        <h2 class="text-2xl font-bold text-center text-gray-900 dark:text-white">Register</h2>

        {#if errorMessage}
            <p class="text-red-500 text-center">{errorMessage}</p>
        {/if}
        {#if successMessage}
            <p class="text-green-500 text-center">{successMessage}</p>
        {/if}

        <div>
            <Label for="email" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Your email</Label>
            <Input type="email" id="email" bind:value={email} required class="w-full h-12 px-4 py-2" />
        </div>

        <div>
            <Label for="password" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Your password</Label>
            <Input type="password" id="password" bind:value={password} required class="w-full h-12 px-4 py-2" />
        </div>

        <div>
            <Label for="profile_picture" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Profile Picture (Optional)</Label>
            <Fileupload id="profile_picture" bind:files={profilePicture} accept="image/*" class="w-full h-12 px-4 py-2" />
        </div>

        <Button type="submit" class="w-full">Register</Button>

        <p class="text-sm text-center text-gray-500 dark:text-gray-400">
            Already have an account? <a href="/login" class="font-medium text-primary-600 hover:underline dark:text-primary-500">Login here</a>
        </p>
    </form>
</div>
