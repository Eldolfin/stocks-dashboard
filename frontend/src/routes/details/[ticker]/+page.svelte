<script lang="ts">
	import HistoryChart from '$lib/components/HistoryChart.svelte';
	import { Button, ButtonGroup, Card } from 'flowbite-svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { formatPercent, ratioColor } from '$lib/format-utils';

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
		{ label: 'Previous Close', value: 'info.previousClose' },
		{ label: "Today's Range", value: 'info.regularMarketDayRange' },
		{ label: '52-Week Range', value: 'info.fiftyTwoWeekRange' },
		{ label: 'Return on Equity (ROE)', value: 'info.returnOnEquity' },
		{ label: 'Market Capitalization', value: 'info.marketCap' },
		{ label: 'EBITDA', value: 'info.ebitda' },
		{ label: 'Trailing P/E Ratio', value: 'info.trailingPE' },
		{ label: 'Forward P/E Ratio', value: 'info.forwardPE' },
		{ label: 'Earnings Growth', value: 'info.earningsGrowth' },
		{ label: 'Revenue Growth', value: 'info.revenueGrowth' },
		{ label: 'Payout Ratio', value: 'info.payoutRatio' },
		{ label: 'Profit Margins', value: 'info.profitMargins' },
		{ label: 'Free Cash Flow', value: 'info.freeCashflow' },
		{ label: 'Dividend Rate', value: 'info.dividendRate' },
		{ label: 'Dividend Yield', value: 'info.dividendYield' },
		{ label: 'Shares Outstanding', value: 'info.sharesOutstanding' },
		{ label: 'P/E ratio', value: 'main.ratioPE' },
		{ label: 'Free Cash Flow Yield', value: 'main.freeCashflowYield' }
	];
	const changeRange = (newValue: string) => {
		let query = new URLSearchParams($page.url.searchParams.toString());

		query.set('period', newValue);

		goto(`?${query.toString()}`, { replaceState: true });
	};
	const deep_value = function (obj: any, path: string) {
		for (let i = 0, segments = path.split('.'), len = segments.length; i < len; i++) {
			obj = obj[segments[i]];
		}
		return obj;
	};
</script>

<div class="flex justify-center">
	<p class="text-8xl dark:text-white">
		{data.ticker}
	</p>
</div>
<div>
	<div class="flex justify-center">
		<p class={`text-1xl dark:text-white`} style={`color: ${ratioColor(data.history?.delta)}`}>
			{formatPercent(data.history!.delta!)}
		</p>
	</div>
	<div class="flex justify-center">
		<HistoryChart
			title={`Price: ${data.history?.query.period}`}
			dataset={{ price: data.history!.candles, ...data.history!.smas }}
			dates={data.history!.dates}
			color={ratioColor(data.history?.delta)}
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
					{#if deep_value(data.summary, kpi.value) !== null}
						<div>
							<strong>{kpi.label}</strong>
							<br />
							<span>{deep_value(data.summary, kpi.value)}</span>
						</div>
					{/if}
				{/each}
			</div>
		</Card>
	</div>
</div>
