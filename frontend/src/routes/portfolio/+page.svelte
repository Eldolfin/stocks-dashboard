<script lang="ts">
	import { Label, Fileupload, Helper, Heading, A } from 'flowbite-svelte';
	import { client } from '../../lib/typed-fetch-client';
	import type { components } from '../../generated/api.js';
	import BarChart from '$lib/components/BarChart.svelte';
	import { ArrowRightOutline } from 'flowbite-svelte-icons';
	import HistoryChart from '$lib/components/HistoryChart.svelte';

	type EtoroData = components['schemas']['EtoroAnalysisResponse'];

	let files: FileList | undefined = $state(undefined);
	let error: string | undefined = $state(undefined);
	let data: EtoroData | undefined = $state(undefined);

	const now = new Date();

	$effect(() => {
		(async () => {
			if (files) {
				const formData = new FormData();
				formData.append('file', files[0]);
				const res = await client.POST('/api/etoro_analysis', {
					body: formData as any // FIXME?
				});

				error = res.error?.toString();
				data = res.data;

				if (data) error = undefined;
			}
		})();
	});
</script>

{#if data !== undefined}
	<div class="flex justify-center">
		<BarChart
			title="Profit over time"
			dataset={new Map([['profit (USD)', data['Profit(USD)']]])}
			color="green"
			dates={data['Close Date']}
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
