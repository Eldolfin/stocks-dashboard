<script lang="ts">
	import { client } from '$lib/typed-fetch-client';
	import { goto } from '$app/navigation';
	import { Button, Label, Input, Fileupload } from 'flowbite-svelte';
	import { fade, fly } from 'svelte/transition';
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

	// Handle escape key to close modal
	const handleKeydown = (e: KeyboardEvent) => {
		if (e.key === 'Escape') {
			onClose();
		}
	};

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

<svelte:window on:keydown={handleKeydown} />

{#if show}
	<!-- Modal backdrop with blur -->
	<div
		class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm"
		transition:fade={{ duration: 300 }}
		onclick={(e) => e.target === e.currentTarget && handleModalClose()}
		onkeydown={(e) => e.key === 'Enter' && e.target === e.currentTarget && handleModalClose()}
		role="dialog"
		aria-modal="true"
		aria-labelledby="modal-title"
		tabindex="-1"
	>
		<!-- Modal content -->
		<div
			class="relative mx-4 w-full max-w-md rounded-2xl bg-white/95 shadow-2xl backdrop-blur-md dark:bg-gray-900/95"
			transition:fly={{ y: 20, duration: 400, opacity: 0 }}
			role="main"
		>
			<!-- Decorative gradient border -->
			<div
				class="absolute -inset-0.5 rounded-2xl bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 opacity-20 blur-sm"
			></div>

			<!-- Main modal content -->
			<div class="relative rounded-2xl bg-white p-8 dark:bg-gray-900">
				<div class="space-y-6">
					<!-- Tab switcher with improved styling -->
					<div class="relative flex space-x-1 rounded-xl bg-gray-100 p-1 dark:bg-gray-800">
						<!-- Moving background indicator -->
						<div
							class="absolute top-1 h-8 rounded-lg bg-white shadow-sm transition-transform duration-200 ease-out dark:bg-gray-700"
							style="width: calc(50% - 4px); transform: translateX({isLogin
								? '2px'
								: 'calc(100% + 2px)'})"
						></div>

						<button
							class="relative z-10 w-full rounded-lg px-3 py-2 text-sm font-medium transition-colors {isLogin
								? 'text-gray-900 dark:text-white'
								: 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200'}"
							onclick={() => (isLogin = true)}
						>
							Login
						</button>
						<button
							class="relative z-10 w-full rounded-lg px-3 py-2 text-sm font-medium transition-colors {!isLogin
								? 'text-gray-900 dark:text-white'
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
							<div class="text-center">
								<h3 class="text-2xl font-bold text-gray-900 dark:text-white">Welcome back</h3>
								<p class="mt-1 text-sm text-gray-600 dark:text-gray-400">Sign in to your account</p>
							</div>

							{#if loginErrorMessage}
								<div
									class="rounded-lg border border-red-200 bg-red-50 p-3 dark:border-red-800 dark:bg-red-900/20"
								>
									<p class="text-center text-sm text-red-600 dark:text-red-400">
										{loginErrorMessage}
									</p>
								</div>
							{/if}

							<div class="space-y-4">
								<div>
									<Label for="login-email" class="mb-2 block text-sm font-medium"
										>Email address</Label
									>
									<Input
										type="email"
										id="login-email"
										bind:value={loginEmail}
										required
										class="h-12 w-full rounded-lg border-gray-300 px-4 py-2 transition-all focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
										placeholder="Enter your email"
									/>
								</div>

								<div>
									<Label for="login-password" class="mb-2 block text-sm font-medium">Password</Label
									>
									<Input
										type="password"
										id="login-password"
										bind:value={loginPassword}
										required
										class="h-12 w-full rounded-lg border-gray-300 px-4 py-2 transition-all focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
										placeholder="Enter your password"
									/>
								</div>
							</div>

							<Button
								type="submit"
								class="h-12 w-full transform rounded-lg bg-gradient-to-r from-blue-600 to-purple-600 font-medium text-white transition-all duration-200 hover:scale-[1.02] hover:from-blue-700 hover:to-purple-700"
							>
								Sign in
							</Button>
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
							<div class="text-center">
								<h3 class="text-2xl font-bold text-gray-900 dark:text-white">Create account</h3>
								<p class="mt-1 text-sm text-gray-600 dark:text-gray-400">Join us to get started</p>
							</div>

							{#if registerErrorMessage}
								<div
									class="rounded-lg border border-red-200 bg-red-50 p-3 dark:border-red-800 dark:bg-red-900/20"
								>
									<p class="text-center text-sm text-red-600 dark:text-red-400">
										{registerErrorMessage}
									</p>
								</div>
							{/if}
							{#if registerSuccessMessage}
								<div
									class="rounded-lg border border-green-200 bg-green-50 p-3 dark:border-green-800 dark:bg-green-900/20"
								>
									<p class="text-center text-sm text-green-600 dark:text-green-400">
										{registerSuccessMessage}
									</p>
								</div>
							{/if}

							<div class="space-y-4">
								<div>
									<Label for="register-email" class="mb-2 block text-sm font-medium"
										>Email address</Label
									>
									<Input
										type="email"
										id="register-email"
										bind:value={registerEmail}
										required
										class="h-12 w-full rounded-lg border-gray-300 px-4 py-2 transition-all focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
										placeholder="Enter your email"
									/>
								</div>

								<div>
									<Label for="register-password" class="mb-2 block text-sm font-medium"
										>Password</Label
									>
									<Input
										type="password"
										id="register-password"
										bind:value={registerPassword}
										required
										class="h-12 w-full rounded-lg border-gray-300 px-4 py-2 transition-all focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
										placeholder="Create a password"
									/>
								</div>

								<div>
									<Label for="register-profile-picture" class="mb-2 block text-sm font-medium">
										Profile Picture <span class="text-gray-500">(Optional)</span>
									</Label>
									<Fileupload
										id="register-profile-picture"
										bind:files={profilePicture}
										accept="image/*"
										class="h-12 w-full rounded-lg border-gray-300 px-4 py-2 transition-all focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
									/>
								</div>
							</div>

							<Button
								type="submit"
								class="h-12 w-full transform rounded-lg bg-gradient-to-r from-green-600 to-blue-600 font-medium text-white transition-all duration-200 hover:scale-[1.02] hover:from-green-700 hover:to-blue-700"
							>
								Create account
							</Button>
						</form>
					{/if}

					<!-- Close button with improved styling -->
					<div class="flex justify-center pt-2">
						<Button
							color="alternative"
							onclick={handleModalClose}
							class="rounded-lg border-gray-300 px-6 py-2 text-gray-600 transition-all duration-200 hover:text-gray-800 dark:border-gray-600 dark:text-gray-400 dark:hover:text-gray-200"
						>
							Cancel
						</Button>
					</div>
				</div>
			</div>
		</div>
	</div>
{/if}
