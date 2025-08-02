<script lang="ts">
	import HistoryChart from '$lib/components/HistoryChart.svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { formatPercent, ratioColor } from '$lib/format-utils';
	import type { components } from '../../../generated/api.js';

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
		let query = new URLSearchParams($page.url.searchParams.toString());

		query.set('period', newValue);

		goto(`?${query.toString()}`, { replaceState: true });
	};
</script>

<div class="flex flex-col items-center">
	<h1 class="text-4xl sm:text-5xl font-bold animate-fade-in">{data.tickers}</h1>
	<div class="my-8 h-56 sm:h-64 bg-gradient-to-r from-[#0d182b] to-[#102139] rounded-2xl shadow-xl flex items-center justify-center text-gray-500 w-full max-w-screen-lg">
		<HistoryChart
			title={`Growth compare`}
			dataset={data.history_data!.candles}
			dates={data.history_data!.dates}
			color={'gray'}
		/>
	</div>
	<div class="flex flex-wrap justify-center gap-2 mb-8">
		{#each ranges as range}
			<button class="px-4 py-1 rounded-full bg-gray-800 text-white shadow hover:scale-105 transition" onclick={() => changeRange(range.value)}>{range.label}</button>
		{/each}
	</div>
</div>