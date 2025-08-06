<script lang="ts">
	import { client } from '../../lib/typed-fetch-client';
	import type { components } from '../../generated/api.js';
	import { onMount } from 'svelte'; // Import onMount
	import { goto } from '$app/navigation';

	type Precision = components['schemas']['PrecisionEnum'];
	type EtoroForm = components['schemas']['EtoroForm'];

	const precision_values: Array<[string, Precision]> = [
		['Year', 'Y'],
		['Month', 'M'],
		['Day', 'D']
	];

	let files: FileList | undefined = $state(undefined);
	let error: string | undefined = $state(undefined);
	let precision_index: number = $state(1); // 'M'
	let loading = $state(false);
	let uploadedReports: string[] = $state([]); // New state for uploaded reports

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
			error = `An error occurred while fetching uploaded reports: ${err}`;
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
				const res = await client.POST('/api/etoro/upload_report', {
					body: formData as unknown as EtoroForm
				});
				loading = false;

				if (res.error) {
					error = res.data!["error"];
				} else {
					error = undefined;
					// Always refresh the list of reports on successful upload
					await fetchUploadedReports();
				}
			}
		})();
	});

	// Function to handle re-analysis of a selected report
	async function reAnalyzeReport(reportName: string) {
		goto(`/portfolio/analysis/${reportName}`);
	}
</script>

<div class="p-8">
	{#if error}
		<div class="text-center text-red-500">{error}</div>
	{:else}
		<div class="p-8">
	{#if error}
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
	{/if}

	{#if loading}
		<div class="mt-4 flex items-center justify-center">
			<div class="border-brand h-8 w-8 animate-spin rounded-full border-b-2"></div>
		</div>
	{/if}
</div>
