<script lang="ts">
	import { client } from '$lib/typed-fetch-client';
	import { goto } from '$app/navigation';
	import { Button, Label, Input, Fileupload, Modal } from 'flowbite-svelte';
	import type { components } from '../../generated/api.js';

	interface Props {
		show: boolean;
		onClose: () => void;
	}

	const { show, onClose }: Props = $props();

	type RegisterForm = components['requestBodies']['EtoroForm'];

	// Login form state
	let loginEmail = $state('');
	let loginPassword = $state('');
	let loginErrorMessage = $state('');

	// Register form state
	let registerEmail = $state('');
	let registerPassword = $state('');
	let profilePicture: FileList | undefined = $state(undefined);
	let registerErrorMessage = $state('');
	let registerSuccessMessage = $state('');

	// Modal state
	let isLogin = $state(true); // true for login, false for register

	// Handle modal close events
	function handleModalClose() {
		onClose();
	}

	async function handleLogin() {
		loginErrorMessage = '';
		try {
			const response = await client.POST('/api/login', {
				body: {
					email: loginEmail,
					password: loginPassword
				}
			});

			if (response.error) {
				loginErrorMessage = 'Login failed';
			} else if (response.data) {
				// Successful login, reload page to update auth state
				goto('/portfolio', { invalidate: ['data:user_auth'] });
				onClose();
			}
		} catch (error) {
			loginErrorMessage = 'An unexpected error occurred.';
			console.error('Login error:', error);
		}
	}

	async function handleRegister() {
		registerErrorMessage = '';
		registerSuccessMessage = '';

		const formData = new FormData();
		formData.append('email', registerEmail);
		formData.append('password', registerPassword);
		if (profilePicture && profilePicture.length > 0) {
			formData.append('profile_picture', profilePicture[0]);
		}

		try {
			const response = await client.POST('/api/register', {
				body: formData as unknown as RegisterForm
			});

			if (response.error) {
				registerErrorMessage = response.error[0]?.msg || 'Registration failed';
			} else if (response.data) {
				registerSuccessMessage = 'Registration successful! You can now log in.';
				// Switch to login tab after successful registration
				isLogin = true;
				// Pre-fill login email
				loginEmail = registerEmail;
			}
		} catch (error) {
			registerErrorMessage = 'An unexpected error occurred.';
			console.error('Registration error:', error);
		}
	}

	// Reset form state when modal opens/closes
	$effect(() => {
		if (!show) {
			// Reset all form state when modal closes
			loginEmail = '';
			loginPassword = '';
			loginErrorMessage = '';
			registerEmail = '';
			registerPassword = '';
			profilePicture = undefined;
			registerErrorMessage = '';
			registerSuccessMessage = '';
			isLogin = true;
		}
	});
</script>

<Modal open={show} size="md" autoclose={false} class="w-full">
	<div class="space-y-6">
		<!-- Tab switcher -->
		<div class="flex space-x-1 rounded-lg bg-gray-100 p-1 dark:bg-gray-800">
			<button
				class="w-full rounded-md px-3 py-2 text-sm font-medium transition-colors {isLogin
					? 'bg-white text-gray-900 shadow-sm dark:bg-gray-700 dark:text-white'
					: 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200'}"
				onclick={() => (isLogin = true)}
			>
				Login
			</button>
			<button
				class="w-full rounded-md px-3 py-2 text-sm font-medium transition-colors {!isLogin
					? 'bg-white text-gray-900 shadow-sm dark:bg-gray-700 dark:text-white'
					: 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200'}"
				onclick={() => (isLogin = false)}
			>
				Register
			</button>
		</div>

		{#if isLogin}
			<!-- Login Form -->
			<form
				onsubmit={(e) => {
					e.preventDefault();
					handleLogin();
				}}
				class="space-y-4"
			>
				<h3 class="text-xl font-semibold text-gray-900 dark:text-white">Login to your account</h3>

				{#if loginErrorMessage}
					<p class="text-center text-red-500">{loginErrorMessage}</p>
				{/if}

				<div>
					<Label for="login-email" class="mb-2 block text-sm font-medium">Your email</Label>
					<Input
						type="email"
						id="login-email"
						bind:value={loginEmail}
						required
						class="h-12 w-full px-4 py-2"
					/>
				</div>

				<div>
					<Label for="login-password" class="mb-2 block text-sm font-medium">Your password</Label>
					<Input
						type="password"
						id="login-password"
						bind:value={loginPassword}
						required
						class="h-12 w-full px-4 py-2"
					/>
				</div>

				<Button type="submit" class="w-full">Login</Button>
			</form>
		{:else}
			<!-- Register Form -->
			<form
				onsubmit={(e) => {
					e.preventDefault();
					handleRegister();
				}}
				class="space-y-4"
			>
				<h3 class="text-xl font-semibold text-gray-900 dark:text-white">Create new account</h3>

				{#if registerErrorMessage}
					<p class="text-center text-red-500">{registerErrorMessage}</p>
				{/if}
				{#if registerSuccessMessage}
					<p class="text-center text-green-500">{registerSuccessMessage}</p>
				{/if}

				<div>
					<Label for="register-email" class="mb-2 block text-sm font-medium">Your email</Label>
					<Input
						type="email"
						id="register-email"
						bind:value={registerEmail}
						required
						class="h-12 w-full px-4 py-2"
					/>
				</div>

				<div>
					<Label for="register-password" class="mb-2 block text-sm font-medium">Your password</Label
					>
					<Input
						type="password"
						id="register-password"
						bind:value={registerPassword}
						required
						class="h-12 w-full px-4 py-2"
					/>
				</div>

				<div>
					<Label for="register-profile-picture" class="mb-2 block text-sm font-medium"
						>Profile Picture (Optional)</Label
					>
					<Fileupload
						id="register-profile-picture"
						bind:files={profilePicture}
						accept="image/*"
						class="h-12 w-full px-4 py-2"
					/>
				</div>

				<Button type="submit" class="w-full">Register</Button>
			</form>
		{/if}

		<!-- Close button -->
		<div class="flex justify-center">
			<Button color="alternative" onclick={handleModalClose}>Cancel</Button>
		</div>
	</div>
</Modal>
