<script lang="ts">
	import { Label, Fileupload, Helper, Heading, A, Range, Spinner } from 'flowbite-svelte';
	import { client } from '../../lib/typed-fetch-client';
	import type { components } from '../../generated/api.js';
	import BarChart from '$lib/components/BarChart.svelte';
	import { ArrowRightOutline } from 'flowbite-svelte-icons';

	type EtoroData = components['schemas']['EtoroAnalysisResponse'];
	type Precision = components['schemas']['PrecisionEnum'];
	const precision_values: Array<[string, Precision]> = [
		['Year', 'Y'],
		['Month', 'M'],
		['Day', 'D']
		// ['Minute', 'min'],
		// ['Second', 's']
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
	<div class="flex justify-center">
		<Label for="precision-range" class="mb-2 block">{precision_values[precision_index][0]}</Label>
		<Range
			id="precision-range"
			min="0"
			max={precision_values.length}
			step="1"
			bind:value={precision_index}
		/>
	</div>
{:else if error}
	<Helper color="red">{error}</Helper>
{:else}
	<Heading tag="h2" customSize="text-4xl font-extrabold mt-6">Step 1:</Heading>
	<A
		aClass="inline-flex items-center font-medium hover:underline"
		href={`https://www.etoro.com/documents/accountstatement/2015-1-1/${now.getFullYear()}-${now.getMonth()}-${now.getDay()}`}
		target="_blank"
		rel="noopener noreferrer"
	>
		Download excel report from Etoro
		<ArrowRightOutline class="ms-2 h-6 w-6" />
	</A>
	<Heading tag="h2" customSize="text-4xl font-extrabold mt-6">Step 2:</Heading>
	<Label class="pb-2">Upload file</Label>
	<Fileupload
		accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
		id="etoro-excel"
		bind:files
	/>
{/if}

{#if loading}
	<Spinner size={8} />
{/if}
