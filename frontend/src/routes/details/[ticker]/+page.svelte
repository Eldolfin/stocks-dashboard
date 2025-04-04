<script lang="ts">
	import HistoryChart from '$lib/components/HistoryChart.svelte';
	import { Button, ButtonGroup, Card } from 'flowbite-svelte';
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
	const kpis = [
		{ label: 'Previous Close', value: 'previousClose' },
		{ label: "Today's Range", value: 'regularMarketDayRange' },
		{ label: '52-Week Range', value: 'fiftyTwoWeekRange' },
		{ label: 'Return on Equity (ROE)', value: 'returnOnEquity' },
		{ label: 'Market Capitalization', value: 'marketCap' },
		{ label: 'EBITDA', value: 'ebitda' },
		{ label: 'Trailing P/E Ratio', value: 'trailingPE' },
		{ label: 'Forward P/E Ratio', value: 'forwardPE' },
		{ label: 'Earnings Growth', value: 'earningsGrowth' },
		{ label: 'Revenue Growth', value: 'revenueGrowth' },
		{ label: 'Payout Ratio', value: 'payoutRatio' },
		{ label: 'Profit Margins', value: 'profitMargins' },
		{ label: 'Free Cash Flow', value: 'freeCashflow' },
		{ label: 'Dividend Rate', value: 'dividendRate' },
		{ label: 'Dividend Yield', value: 'dividendYield' },
		{ label: 'Shares Outstanding', value: 'sharesOutstanding' }

		// MAIN:
		// ratioPE: float
		// freeCashflowYield: float
	];
	const changeRange = (newValue: string) => {
		let query = new URLSearchParams($page.url.searchParams.toString());

		query.set('period', newValue);

		goto(`?${query.toString()}`, { replaceState: true });
	};

	function roundPrecision(value: number, precision: number) {
		let factor = Math.pow(10, precision);
		return Math.round(value * factor) / factor;
	}
	function formatPercent(ratio: number) {
		return `${roundPrecision(ratio * 100, 2)}%`;
	}
	const ratioColor = () => {
		if (data.history?.delta! > 0) {
			return 'green';
		} else if (data.history?.delta! < 0) {
			return 'red';
		} else {
			return 'gray';
		}
	};
</script>

<div class="flex justify-center">
	<p class="text-8xl dark:text-white">
		{data.ticker}
	</p>
</div>
<div>
	<div class="flex justify-center">
		<p class={`text-1xl dark:text-white`} style={`color: ${ratioColor()}`}>
			{formatPercent(data.history?.delta!)}
		</p>
	</div>
	<div class="flex justify-center">
		<HistoryChart
			title={`Price: ${data.history?.query.period}`}
			dataset={data.history?.candles}
			yValuesIndex="Close"
			color={ratioColor()}
		/>
	</div>
	<div class="flex justify-center">
		<ButtonGroup>
			{#each ranges as range}
				<Button onclick={() => changeRange(range.value)} outline color="dark">{range.label}</Button>
			{/each}
		</ButtonGroup>
	</div>

	<div class="mt-10 flex w-full justify-center">
		<Card class="w-full max-w-screen-lg" shadow={true}>
			<div class="grid grid-cols-3 gap-x-11 gap-y-3 text-xl">
				{#each kpis as kpi}
					{#if data.summary.info[kpi.value] !== null}
						<div>
							<strong>{kpi.label}</strong>
							<br />
							<span>{data.summary.info[kpi.value]}</span>
						</div>
					{/if}
				{/each}
			</div>
		</Card>
	</div>
</div>
