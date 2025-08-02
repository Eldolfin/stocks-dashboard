<script lang="ts">
	import { client } from '../../lib/typed-fetch-client';
	import type { components } from '../../generated/api.js';
	import BarChart from '$lib/components/BarChart.svelte';

	type EtoroData = components['schemas']['EtoroAnalysisResponse'];
	type Precision = components['schemas']['PrecisionEnum'];
	const precision_values: Array<[string, Precision]> = [
		['Year', 'Y'],
		['Month', 'M'],
		['Day', 'D']
	];

	let files: FileList | undefined = $state(undefined);
	let error: string | undefined = $state(undefined);
	let data: EtoroData | undefined = $state(undefined);
	let precision_index: number = $state(1); // 'M'
	let loading = $state(false);

	const now = new Date();

	$effect(() => {
		(async () => {
			if (files) {
				loading = true;
				const formData = new FormData();
				formData.append('file', files[0]);
				formData.append('precision', precision_values[precision_index][1]);
				const res = await client.POST('/api/etoro_analysis', {
					body: formData as any // FIXME?
				});

				error = res.error?.toString();
				data = res.data;

				if (data) error = undefined;
				loading = false;
			}
		})();
	});
</script>

<div class="p-8">
{#if data !== undefined}
	<div class="flex justify-center">
		<BarChart
			title="Profit over time"
			dataset={new Map([
				['profit (USD)', new Array(...data.profit_usd)],
				['closed trades', new Array(...data.closed_trades)]
			])}
			color="green"
			dates={data.close_date}
		/>
	</div>
	<div class="flex flex-col items-center mt-4">
		<label for="precision-range" class="mb-2 block text-white">{precision_values[precision_index][0]}</label>
		<input
			type="range"
			id="precision-range"
			min="0"
			max={precision_values.length - 1}
			step="1"
			bind:value={precision_index}
			class="w-64 h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer dark:bg-gray-700"
		/>
	</div>
{:else if error}
	<div class="text-red-500 text-center">{error}</div>
{:else}
	<h2 class="text-4xl font-bold mt-6 text-white">Step 1:</h2>
	<a
		class="inline-flex items-center font-medium hover:underline text-brand"
		href={`https://www.etoro.com/documents/accountstatement/2015-1-1/${now.getFullYear()}-${now.getMonth()}-${now.getDay()}`}
		target="_blank"
		rel="noopener noreferrer"
	>
		Download excel report from Etoro
		<svg class="ms-2 h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
	</a>
	<h2 class="text-4xl font-bold mt-6 text-white">Step 2:</h2>
	<label class="pb-2 block text-white">Upload file</label>
	<input
		type="file"
		accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
		id="etoro-excel"
		bind:files
		class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-brand file:text-black hover:file:bg-brand-dark"
	/>
{/if}

{#if loading}
	<div class="flex justify-center items-center mt-4">
		<div class="animate-spin rounded-full h-8 w-8 border-b-2 border-brand"></div>
	</div>
{/if}
</div>