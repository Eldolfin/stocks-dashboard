<script lang="ts">
	import HistoryChart from '$lib/components/HistoryChart.svelte';
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

<div class="flex flex-col items-center">
  <h1 class="text-4xl sm:text-5xl font-bold animate-fade-in">{data.ticker}</h1>
  <p class="text-brand text-lg sm:text-xl mt-2 animate-fade-in" style={`color: ${ratioColor(data.history?.delta)}`}>
    {formatPercent(data.history!.delta!)}
  </p>
  <p class="text-sm text-gray-400">Price / ∇</p>

  <div class="my-8 h-56 sm:h-64 bg-gradient-to-r from-[#0d182b] to-[#102139] rounded-2xl shadow-xl flex items-center justify-center text-gray-500 w-full max-w-screen-lg">
    <HistoryChart
      title={`Price: ${data.history?.query.period}`}
      dataset={{ price: data.history!.candles, ...data.history!.smas }}
      dates={data.history!.dates}
      color={ratioColor(data.history?.delta)}
    />
  </div>

  <div class="flex flex-wrap justify-center gap-2 mb-8">
    {#each ranges as range}
      <button class="px-4 py-1 rounded-full bg-gray-800 text-white shadow hover:scale-105 transition" onclick={() => changeRange(range.value)}>{range.label}</button>
    {/each}
  </div>

  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 w-full max-w-screen-lg">
    {#each kpis as kpi}
      {#if deep_value(data.summary, kpi.value) !== null}
        <div class="p-5 bg-gradient-to-tr from-[#121f3d] to-[#1f2f50] rounded-2xl shadow-lg hover:scale-[1.02] transition">
          <h2 class="font-semibold text-white mb-2">{kpi.label}</h2>
          <ul class="space-y-1 text-sm text-gray-300">
            <li><span class="text-brand">{deep_value(data.summary, kpi.value)}</span></li>
          </ul>
        </div>
      {/if}
    {/each}
  </div>
</div>