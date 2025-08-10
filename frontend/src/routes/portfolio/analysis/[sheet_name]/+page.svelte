<script lang="ts">
	import { client } from '../../../../lib/typed-fetch-client';
	import type { components } from '../../../../generated/api.js';
	import BarChart from '$lib/components/BarChart.svelte';
	import HistoryChart from '$lib/components/HistoryChart.svelte';
	import { page } from '$app/stores'; // Import page store

	type EtoroData = components['schemas']['EtoroAnalysisResponse'];
	type EtoroEvolutionData = components['schemas']['EtoroEvolutionResponse'];
	type Precision = components['schemas']['PrecisionEnum'];

	const precision_values: Array<[string, Precision]> = [
		['Year', 'Y'],
		['Month', 'M'],
		['Day', 'D']
	];

	let trades_data: EtoroData | undefined = $state(undefined);
	let evolution_data: EtoroEvolutionData | undefined = $state(undefined);
	let precision_index: number = $state(1); // 'M'
	let loading = $state(false);
	let error: string | undefined = $state(undefined);

	// Function to fetch analysis data
	async function fetchAnalysisData(reportName: string, precision: Precision) {
		loading = true;
		error = undefined; // Clear previous errors

		const res_trades_analysis = await client.GET('/api/etoro_analysis_by_name', {
			params: {
				query: {
					filename: reportName,
					precision: precision
				}
			}
		});
		const res_evolution_analysis = await client.GET('/api/etoro_evolution_by_name', {
			params: {
				query: {
					filename: reportName,
					precision: precision
				}
			}
		});
		loading = false;

		if (res_trades_analysis.error) {
			error = (res_trades_analysis.error as components['schemas']['NotFoundResponse']).message;
			trades_data = undefined;
		} else if (res_trades_analysis.data) {
			trades_data = res_trades_analysis.data;
		}

		if (res_evolution_analysis.error) {
			// If trades_analysis already set an error, don't overwrite unless this is more specific
			if (!error) {
				error = (res_evolution_analysis.error as components['schemas']['NotFoundResponse']).message;
			}
			evolution_data = undefined;
		} else if (res_evolution_analysis.data) {
			evolution_data = res_evolution_analysis.data;
		}
	}

	// React to changes in sheet_name or precision_index
	$effect(() => {
		const sheetName = $page.params.sheet_name;
		const currentPrecision = precision_values[precision_index][1];
		if (sheetName) {
			fetchAnalysisData(sheetName, currentPrecision);
		}
	});
</script>

<div class="p-8">
	{#if trades_data !== undefined}
		<div class="flex justify-center">
			<BarChart
				dataset={new Map([
					['profit (USD)', new Array(...trades_data.profit_usd)],
					['closed trades', new Array(...trades_data.closed_trades)]
				])}
				dates={trades_data.close_date}
			/>
		</div>
		<div class="mt-4 flex flex-col items-center">
			<label for="precision-range" class="mb-2 block text-white"
				>{precision_values[precision_index][0]}</label
			>
			<input
				type="range"
				id="precision-range"
				min="0"
				max={precision_values.length - 1}
				step="1"
				bind:value={precision_index}
				class="h-2 w-64 cursor-pointer appearance-none rounded-lg bg-gray-700 dark:bg-gray-700"
			/>
		</div>
	{:else if error}
		<div class="text-center text-red-500">{error}</div>
	{/if}
	{#if evolution_data !== undefined}
		<div class="flex justify-center">
			<HistoryChart
				color="green"
				title="Total profits evolution overtime"
				showTickerSelector={true}
				defaultShown={['Total', 'Closed Positions', 'Deposits', 'P&L']}
				dataset={evolution_data['evolution']['parts']}
				dates={evolution_data['evolution']['dates']}
			/>
		</div>
	{:else if error}
		<div class="text-center text-red-500">{error}</div>
	{/if}

	{#if loading}
		<div class="mt-4 flex items-center justify-center">
			<div class="border-brand h-8 w-8 animate-spin rounded-full border-b-2"></div>
		</div>
	{/if}
</div>
