<script lang="ts">
	import { client } from '$lib/typed-fetch-client';
	import { goto } from '$app/navigation';
	import { Button, Label, Input, Fileupload } from 'flowbite-svelte';
	import type { components } from '../../generated/api.d.ts';

	type RegisterForm = components['requestBodies']['EtoroForm'];

	let email = '';
	let password = '';
	let profilePicture: FileList | undefined = undefined;
	let errorMessage = '';
	let successMessage = '';

	async function handleRegister() {
		errorMessage = '';
		successMessage = '';

		const formData = new FormData();
		formData.append('email', email);
		formData.append('password', password);
		if (profilePicture && profilePicture.length > 0) {
			formData.append('profile_picture', profilePicture[0]);
		}

		try {
			const response = await client.POST('/api/register', {
				body: formData as unknown as RegisterForm
			});

			if (response.error) {
				errorMessage = response.error[0]?.msg || 'Registration failed';
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

<div class="flex min-h-screen flex-col items-center justify-center">
	<form
		on:submit|preventDefault={handleRegister}
		class="w-full max-w-md space-y-6 rounded-lg p-8 shadow-md"
	>
		<h2 class="text-center text-2xl font-bold  text-white">Register</h2>

		{#if errorMessage}
			<p class="text-center text-red-500">{errorMessage}</p>
		{/if}
		{#if successMessage}
			<p class="text-center text-green-500">{successMessage}</p>
		{/if}

		<div>
			<Label for="email" class="mb-2 block text-sm font-medium  text-white"
				>Your email</Label
			>
			<Input type="email" id="email" bind:value={email} required class="h-12 w-full px-4 py-2" />
		</div>

		<div>
			<Label for="password" class="mb-2 block text-sm font-medium  text-white"
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

		<div>
			<Label for="profile_picture" class="mb-2 block text-sm font-medium  text-white"
				>Profile Picture (Optional)</Label
			>
			<Fileupload
				id="profile_picture"
				bind:files={profilePicture}
				accept="image/*"
				class="h-12 w-full px-4 py-2"
			/>
		</div>

		<Button type="submit" class="w-full">Register</Button>

		<p class="text-center text-sm  ">
			Already have an account? <a
				href="/login"
				class="text-primary-600 text-primary-500 font-medium hover:underline">Login here</a
			>
		</p>
	</form>
</div>
