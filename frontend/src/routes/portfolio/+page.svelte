<script lang="ts">
	import { client } from '../../lib/typed-fetch-client';
	import type { components } from '../../generated/api.js';
	import BarChart from '$lib/components/BarChart.svelte';
	import HistoryChart from '$lib/components/HistoryChart.svelte';
	import { onMount } from 'svelte'; // Import onMount

	type EtoroData = components['schemas']['EtoroAnalysisResponse'];
	type EtoroNetWorthData = components['schemas']['EtoroNetWorthResponse'];
	type Precision = components['schemas']['PrecisionEnum'];
	type EtoroForm = components['schemas']['EtoroForm'];

	const precision_values: Array<[string, Precision]> = [
		['Year', 'Y'],
		['Month', 'M'],
		['Day', 'D']
	];

	let files: FileList | undefined = $state(undefined);
	let error: string | undefined = $state(undefined);
	let data: EtoroData | undefined = $state(undefined);
	let netWorthData: EtoroNetWorthData | undefined = $state(undefined);
	let precision_index: number = $state(1); // 'M'
	let loading = $state(false);
	let uploadedReports: string[] = $state([]); // New state for uploaded reports
	let viewMode: 'profit' | 'networth' = $state('profit'); // Toggle between views

	const now = new Date();

	// Function to fetch uploaded reports
	async function fetchUploadedReports() {
		try {
			const response = await client.GET('/api/etoro/reports');
			if (response.data) {
				uploadedReports = response.data.reports;
			} else {
				console.error('Failed to fetch uploaded reports');
			}
		} catch (err) {
			console.error('An error occurred while fetching uploaded reports:', err);
		}
	}

	// Fetch reports on component mount
	onMount(() => {
		fetchUploadedReports();
	});

	$effect(() => {
		(async () => {
			if (files) {
				loading = true;
				const formData = new FormData();
				formData.append('file', files[0]);
				formData.append('precision', precision_values[precision_index][1]);
				
				// Fetch both profit and net worth data
				const [profitRes, netWorthRes] = await Promise.all([
					client.POST('/api/etoro_analysis', {
						body: formData as unknown as EtoroForm // FIXME: ???
					}),
					client.POST('/api/etoro_net_worth', {
						body: formData as unknown as EtoroForm // FIXME: ???
					})
				]);

				if (profitRes.data && netWorthRes.data) {
					data = profitRes.data;
					netWorthData = netWorthRes.data;
					error = undefined;
					// After successful upload, refresh the list of reports
					await fetchUploadedReports();
				} else {
					error = 'Failed to fetch data';
				}
				loading = false;
			}
		})();
	});

	// Function to handle re-analysis of a selected report (placeholder for now)
	async function reAnalyzeReport(reportName: string) {
		loading = true;
		
		const [profitRes, netWorthRes] = await Promise.all([
			client.GET('/api/etoro_analysis_by_name', {
				params: {
					query: {
						filename: reportName,
						precision: precision_values[precision_index][1]
					}
				}
			}),
			client.GET('/api/etoro_net_worth_by_name', {
				params: {
					query: {
						filename: reportName,
						precision: precision_values[precision_index][1]
					}
				}
			})
		]);

		if (profitRes.error || netWorthRes.error) {
			error = 'Failed to fetch data';
		} else if (profitRes.data && netWorthRes.data) {
			data = profitRes.data;
			netWorthData = netWorthRes.data;
			error = undefined;
		}
		loading = false;
	}
</script>

<div class="p-8">
	{#if data !== undefined && (viewMode === 'profit' || (viewMode === 'networth' && netWorthData !== undefined))}
		<!-- View Mode Toggle -->
		<div class="mb-6 flex justify-center">
			<div class="inline-flex rounded-lg bg-gray-700 p-1">
				<button
					class="rounded-md px-4 py-2 text-sm font-medium transition-colors {viewMode === 'profit'
						? 'bg-brand text-black'
						: 'text-gray-300 hover:text-white'}"
					onclick={() => (viewMode = 'profit')}
				>
					Profit Analysis
				</button>
				<button
					class="rounded-md px-4 py-2 text-sm font-medium transition-colors {viewMode === 'networth'
						? 'bg-brand text-black'
						: 'text-gray-300 hover:text-white'}"
					onclick={() => (viewMode = 'networth')}
				>
					Net Worth Over Time
				</button>
			</div>
		</div>

		<div class="flex justify-center">
			{#if viewMode === 'profit'}
				<BarChart
					dataset={new Map([
						['profit (USD)', new Array(...data.profit_usd)],
						['closed trades', new Array(...data.closed_trades)]
					])}
					dates={data.close_date}
				/>
			{:else if netWorthData}
				<HistoryChart
					title="Net Worth Over Time"
					dataset={{ 'Net Worth (USD)': netWorthData.net_worth }}
					dates={netWorthData.dates}
					color="#00ff88"
				/>
			{/if}
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
	{:else}
		<h2 class="mt-6 text-4xl font-bold text-white">Step 1:</h2>
		<a
			class="text-brand inline-flex items-center font-medium hover:underline"
			href={`https://www.etoro.com/documents/accountstatement/2015-1-1/${now.getFullYear()}-${now.getMonth()}-${now.getDay()}`}
			target="_blank"
			rel="noopener noreferrer"
		>
			Download excel report from Etoro
			<svg
				class="ms-2 h-6 w-6"
				fill="none"
				stroke="currentColor"
				viewBox="0 0 24 24"
				xmlns="http://www.w3.org/2000/svg"
				><path
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M17 8l4 4m0 0l-4 4m4-4H3"
				></path></svg
			>
		</a>
		<h2 class="mt-6 text-4xl font-bold text-white">Step 2:</h2>
		<label for="etoro-excel" class="block pb-2 text-white">Upload file</label>
		<input
			type="file"
			accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
			id="etoro-excel"
			bind:files
			class="file:bg-brand hover:file:bg-brand-dark block w-full text-sm text-gray-500 file:mr-4 file:rounded-full file:border-0 file:px-4 file:py-2 file:text-sm file:font-semibold file:text-black"
		/>

		<!-- New section for previously uploaded reports -->
		{#if uploadedReports.length > 0}
			<h2 class="mt-6 text-4xl font-bold text-white">Previously Uploaded Reports:</h2>
			<ul class="list-inside list-disc text-white">
				{#each uploadedReports as report (report)}
					<li>
						<button onclick={() => reAnalyzeReport(report)} class="text-blue-400 hover:underline">
							{report}
						</button>
					</li>
				{/each}
			</ul>
		{/if}
	{/if}

	{#if loading}
		<div class="mt-4 flex items-center justify-center">
			<div class="border-brand h-8 w-8 animate-spin rounded-full border-b-2"></div>
		</div>
	{/if}
</div>
