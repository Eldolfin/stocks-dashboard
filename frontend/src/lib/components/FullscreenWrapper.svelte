<script lang="ts">
	import type { ComponentType } from 'svelte';

	let { title, chartComponent, chartProps }: { title: string; chartComponent: any; chartProps: any } = $props();
	let fullscreen = $state(false);

	const toggleFullscreen = () => {
		fullscreen = !fullscreen;
	};

	const ChartComponent = chartComponent;
</script>

<div class="relative h-full w-full">
	<div class="absolute top-2 left-2 z-10">
		<button
			class="rounded-lg bg-gray-800 p-2 text-white transition hover:bg-gray-700"
			onclick={toggleFullscreen}
			aria-label="Toggle fullscreen"
		>
			<!-- Fullscreen icon -->
			<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"
				/>
			</svg>
		</button>
	</div>

	{#if fullscreen}
		<div
			class="fixed top-0 left-0 z-50 flex h-screen w-screen flex-col items-center justify-center bg-gray-900 bg-opacity-90"
		>
			<div class="h-full w-full max-w-screen-lg rounded-lg bg-gray-800 p-8">
				<div class="flex items-center justify-between">
					<h2 class="text-2xl font-bold text-white">{title}</h2>
					<button
						class="rounded-lg bg-gray-700 p-2 text-white transition hover:bg-gray-600"
						onclick={toggleFullscreen}
						aria-label="Close fullscreen"
					>
						<!-- Close icon -->
						<svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M6 18L18 6M6 6l12 12"
							/>
						</svg>
					</button>
				</div>
				<div class="mt-4 h-[calc(100%-4rem)] w-full">
					<ChartComponent {...chartProps} />
				</div>
			</div>
		</div>
	{/if}

	<div class="h-full w-full">
		<ChartComponent {...chartProps} />
	</div>
</div>
