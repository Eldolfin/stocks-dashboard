<script lang="ts">
	import { Helper } from 'flowbite-svelte';
	import { Label, Fileupload } from 'flowbite-svelte';
	import { client } from '../../lib/typed-fetch-client';
	import type { components } from '../../generated/api.js';
	import BarChart from '$lib/components/BarChart.svelte';

	type EtoroData = components['schemas']['EtoroAnalysisResponse'];

	let files: FileList | undefined = $state(undefined);
	let error: string | undefined = $state(undefined);
	let data: EtoroData | undefined = $state(undefined);

	const data_profits = $derived(data!['Close Date']);

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

{#if data}
	<div class="flex justify-center">
		<BarChart
			title="Profit over time"
			dataset={new Map([['profit (USD)', data_profits]])}
			color="green"
			dates={data['Close Date']}
		/>
	</div>
{:else if error}
	<Helper color="red">{error}</Helper>
{:else}
	<Label class="pb-2">Upload file</Label>
	<Fileupload
		accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
		id="etoro-excel"
		bind:files
	/>
	<Helper>EXCEL FILE (MAX. 800x400px).</Helper>
{/if}
