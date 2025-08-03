<script lang="ts">
	import HistoryChart from '$lib/components/HistoryChart.svelte';
	import { page } from '$app/state';
	import { goto } from '$app/navigation';

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
		let query = new URLSearchParams(page.url.searchParams.toString());

		query.set('period', newValue);

		goto(`?${query.toString()}`, { replaceState: true });
	};

	const historyData = data.history_data;
</script>

<div class="flex flex-col items-center">
	<h1 class="animate-fade-in text-4xl font-bold sm:text-5xl">{data.tickers}</h1>
	<div
		class="my-8 flex h-56 w-full max-w-screen-lg items-center justify-center rounded-2xl bg-gradient-to-r from-[#0d182b] to-[#102139] text-gray-500 shadow-xl sm:h-64"
	>
		<HistoryChart
			title={`Growth compare`}
			dataset={historyData.candles}
			dates={historyData.dates}
			color={'gray'}
		/>
	</div>
	<div class="mb-8 flex flex-wrap justify-center gap-2">
		{#each ranges as range}
			<button
				class="rounded-full bg-gray-800 px-4 py-1 text-white shadow transition hover:scale-105"
				onclick={() => changeRange(range.value)}>{range.label}</button
			>
		{/each}
	</div>
</div>
