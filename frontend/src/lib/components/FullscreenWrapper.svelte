<script lang="ts">
	let {
		title,
		chartComponent,
		chartProps
	}: { title: string; chartComponent: any; chartProps: any } = $props();
	let fullscreen = $state(false);

	const toggleFullscreen = () => (fullscreen = !fullscreen);
	const ChartComponent = chartComponent;
</script>

<div
	class={fullscreen
		? 'bg-opacity-90 fixed top-0 left-0 z-50 flex h-screen w-screen flex-col bg-gray-900 p-8'
		: 'relative h-full w-full rounded-lg bg-gray-800 p-4'}
>
	<div class="flex items-center justify-between">
		<h2 class="text-2xl font-bold text-white">{title}</h2>
		<button
			class="rounded-lg bg-gray-700 p-2 text-white transition hover:bg-gray-600"
			onclick={toggleFullscreen}
			aria-label="Toggle fullscreen"
		>
			{#if fullscreen}
				<!-- Close icon -->
				<svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M6 18L18 6M6 6l12 12"
					/>
				</svg>
			{:else}
				<!-- Fullscreen icon -->
				<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"
					/>
				</svg>
			{/if}
		</button>
	</div>

	<div class="flex-1 overflow-hidden">
		<ChartComponent {...chartProps} />
	</div>
</div>
