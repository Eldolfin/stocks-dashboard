<script lang="ts">
	import HistoryChart from '$lib/components/HistoryChart.svelte';
	import { Button, ButtonGroup } from 'flowbite-svelte';
	import { page } from '$app/stores';
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
		let query = new URLSearchParams($page.url.searchParams.toString());

		query.set('period', newValue);

		goto(`?${query.toString()}`, { replaceState: true });
	};
</script>

<p class="text-2xl dark:text-white">{data.ticker}</p>
<div>
	<div class="flex justify-center">
		<HistoryChart
			title={`Price: ${data.history?.query.period}`}
			dataset={data.history?.candles}
			yValuesIndex="Close"
		/>
	</div>
	<div class="flex justify-center">
		<ButtonGroup>
			{#each ranges as range}
				<Button onclick={() => changeRange(range.value)} outline color="dark">{range.label}</Button>
			{/each}
		</ButtonGroup>
	</div>
</div>
