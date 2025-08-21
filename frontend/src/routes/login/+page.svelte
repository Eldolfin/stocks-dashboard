<script lang="ts">
	import { getUserContext } from '$lib/contexts/user.svelte';
	import { client } from '$lib/typed-fetch-client';
	import { Button, Label, Input } from 'flowbite-svelte';
	import { goto } from '$app/navigation';

	let email = '';
	let password = '';
	let errorMessage = '';
	let userContext = getUserContext();

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
				// FIXME: ??
				errorMessage = 'Login failed';
			} else if (response.data) {
				userContext.loggedIn = true;
				goto('/');
			}
		} catch (error) {
			errorMessage = 'An unexpected error occurred.';
			console.error('Login error:', error);
		}
	}
</script>

<div class="flex min-h-screen flex-col items-center justify-center">
	<form
		on:submit|preventDefault={handleLogin}
		class="w-full max-w-md space-y-6 rounded-lg p-8 shadow-md"
	>
		<h2 class="text-center text-2xl font-bold text-gray-900 text-white">Login</h2>

		{#if errorMessage}
			<p class="text-center text-red-500">{errorMessage}</p>
		{/if}

		<div>
			<Label for="email" class="mb-2 block text-sm font-medium text-gray-900 text-white"
				>Your email</Label
			>
			<Input type="email" id="email" bind:value={email} required class="h-12 w-full px-4 py-2" />
		</div>

		<div>
			<Label for="password" class="mb-2 block text-sm font-medium text-gray-900 text-white"
				>Your password</Label
			>
			<Input
				type="password"
				id="password"
				bind:value={password}
				required
				class="h-12 w-full px-4 py-2"
			/>
		</div>

		<Button type="submit" class="w-full">Login</Button>

		<p class="text-center text-sm text-gray-500 text-gray-400">
			Don't have an account? <a
				href="/register"
				class="text-primary-600 text-primary-500 font-medium hover:underline">Register here</a
			>
		</p>
	</form>
</div>
