<script lang="ts">
	import HistoryChart from '$lib/components/HistoryChart.svelte';
	import FullscreenChartModal from '$lib/components/FullscreenChartModal.svelte';
	import { page } from '$app/state';
	import { SvelteURLSearchParams } from 'svelte/reactivity';

	let { data } = $props();

	const ranges = [
		{ label: '1 Day', value: '1d' },
		{ label: '1 Week', value: '7d' },
		{ label: '1 month', value: '1mo' },
		{ label: '3 month', value: '3mo' },
		{ label: 'YTD', value: 'ytd' },
		{ label: '1 year', value: '1y' },
		{ label: '3 year', value: '3y' },
		{ label: 'MAX', value: 'max' }
	];
	const changeRange = (newValue: string) => {
		let query = new SvelteURLSearchParams(page.url.searchParams.toString());
		query.set('period', newValue);
		window.history.replaceState(history.state, '', `?${query}`);
	};

	const historyData = data.history_data;

	// Fullscreen modal state
	let fullscreenChart: {
		show: boolean;
		title: string;
		dataset: { [key: string]: number[] };
		dates: string[];
		color: string;
	} = $state({
		show: false,
		title: '',
		dataset: {},
		dates: [],
		color: ''
	});

	const openMainChartFullscreen = () => {
		fullscreenChart = {
			show: true,
			title: `Growth Comparison: ${data.tickers
				.split(',')
				.map((t: string) => t.trim())
				.join(' vs ')}`,
			dataset: historyData.candles,
			dates: historyData.dates,
			color: 'var(--color-gray)'
		};
	};

	const closeFullscreen = () => {
		fullscreenChart = {
			...fullscreenChart,
			show: false
		};
	};
</script>

<div class="flex flex-col items-center">
	<h1 class="animate-fade-in text-4xl font-bold sm:text-5xl">{data.tickers}</h1>
	<div
		class="relative my-8 flex h-56 w-full max-w-screen-lg items-center justify-center rounded-2xl bg-gradient-to-r from-[#0d182b] to-[#102139] text-gray-500 shadow-xl sm:h-64"
	>
		<!-- Fullscreen button for main chart -->
		<button
			class="absolute top-2 right-2 z-10 rounded-lg bg-gray-800 p-2 text-white transition hover:bg-gray-700"
			onclick={openMainChartFullscreen}
			aria-label="View growth comparison chart in fullscreen"
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

		<HistoryChart
			title="Growth compare"
			dataset={historyData.candles}
			dates={historyData.dates}
			color="gray"
		/>
	</div>
	<div class="mb-8 flex flex-wrap justify-center gap-2">
		{#each ranges as range (range.label)}
			<button
				class="rounded-full bg-gray-800 px-4 py-1 text-white shadow transition hover:scale-105"
				onclick={() => changeRange(range.value)}>{range.label}</button
			>
		{/each}
	</div>
</div>

<!-- Fullscreen Chart Modal -->
<FullscreenChartModal
	show={fullscreenChart.show}
	title={fullscreenChart.title}
	dataset={fullscreenChart.dataset}
	dates={fullscreenChart.dates}
	color={fullscreenChart.color}
	onClose={closeFullscreen}
/>
