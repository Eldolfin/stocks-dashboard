<script lang="ts">
	import { client } from '../../lib/typed-fetch-client';
	import type { components } from '../../generated/api.js';
	import { onMount } from 'svelte'; // Import onMount
	import { goto } from '$app/navigation';
	import { SvelteDate } from 'svelte/reactivity';

	let { data } = $props();

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
	let showLoginMessage = $state(false); // State for showing login required message

	// Calculate yesterday's date since we want a full day
	const getYesterdayUrl = () => {
		const now = new SvelteDate();
		const yesterday = new SvelteDate(now);
		yesterday.setDate(yesterday.getDate() - 1);
		return `https://www.etoro.com/documents/accountstatement/2015-1-1/${yesterday.getFullYear()}-${yesterday.getMonth() + 1}-${yesterday.getDate()}`;
	};

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
		// Check if user is logged in, show message and redirect to login if not
		if (!data.isLoggedIn) {
			showLoginMessage = true;
			// Redirect after 3 seconds to allow user to read the message
			setTimeout(() => {
				goto('/login');
			}, 3000);
			return;
		}
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
					error = res.data!['error'];
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
	{#if showLoginMessage}
		<div
			class="mb-6 rounded-lg border-l-4 border-blue-500 bg-blue-100 p-4 text-blue-700 dark:border-blue-400 dark:bg-blue-900 dark:text-blue-200"
		>
			<div class="flex items-center">
				<svg
					class="mr-2 h-5 w-5"
					fill="currentColor"
					viewBox="0 0 20 20"
					xmlns="http://www.w3.org/2000/svg"
				>
					<path
						fill-rule="evenodd"
						d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
						clip-rule="evenodd"
					></path>
				</svg>
				<div>
					<p class="font-medium">Login Required</p>
					<p class="text-sm">
						You need to be logged in to access portfolio analysis features. Redirecting to login
						page...
					</p>
				</div>
			</div>
		</div>
	{/if}

	{#if error}
		<div class="text-center text-red-500">{error}</div>
	{:else if !showLoginMessage}
		<div class="p-8">
			{#if error}
				<div class="text-center text-red-500">{error}</div>
			{:else}
				<h2 class="mt-6 text-4xl font-bold text-white">Step 1:</h2>
				<a
					class="text-brand inline-flex items-center font-medium hover:underline"
					href={getYesterdayUrl()}
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
								<button
									onclick={() => reAnalyzeReport(report)}
									class="text-blue-400 hover:underline"
								>
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

	{#if loading && !showLoginMessage}
		<div class="mt-4 flex items-center justify-center">
			<div class="border-brand h-8 w-8 animate-spin rounded-full border-b-2"></div>
		</div>
	{/if}
</div>
