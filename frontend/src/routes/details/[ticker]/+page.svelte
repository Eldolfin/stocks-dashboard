<script lang="ts">
	import HistoryChart from '$lib/components/HistoryChart.svelte';
	import FullscreenChartModal from '$lib/components/FullscreenChartModal.svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import {
		formatPercent,
		ratioColor,
		formatCurrency,
		formatLargeNumber,
		roundPrecision
	} from '$lib/format-utils';
	import type { components } from '../../../generated/api.js';
	import { SvelteURLSearchParams } from 'svelte/reactivity';
	import { client } from '$lib/typed-fetch-client';

	let { data } = $props();

	// State for current chart data and loading
	let currentHistory = $state(data.history as components['schemas']['TickerResponse']);
	let isLoadingHistory = $state(false);

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
		{
			group: 'Valuation',
			items: [
				{ label: 'Previous Close', value: 'info.previousClose', format: formatCurrency },
				{ label: 'Market Cap', value: 'info.marketCap', format: formatLargeNumber },
				{
					label: 'Trailing P/E',
					value: 'info.trailingPE',
					format: (val: number) => roundPrecision(val, 2)
				},
				{
					label: 'Forward P/E',
					value: 'info.forwardPE',
					format: (val: number) => roundPrecision(val, 2)
				},
				{
					label: 'P/E ratio',
					value: 'main.ratioPE',
					format: (val: number) => roundPrecision(val, 2)
				}
			]
		},
		{
			group: 'Performance',
			items: [
				{ label: "Today's Range", value: 'info.regularMarketDayRange' },
				{ label: '52-Week Range', value: 'info.fiftyTwoWeekRange' },
				{ label: 'ROE', value: 'info.returnOnEquity', format: formatPercent },
				{ label: 'EBITDA', value: 'info.ebitda', format: formatLargeNumber }
			]
		},
		{
			group: 'Dividends',
			items: [
				{ label: 'Payout Ratio', value: 'info.payoutRatio', format: formatPercent },
				{
					label: 'Dividend Rate',
					value: 'info.dividendRate',
					format: (val: number) => roundPrecision(val, 2)
				},
				{ label: 'Dividend Yield', value: 'info.dividendYield', format: formatPercent },
				{ label: 'Free CF Yield', value: 'main.freeCashflowYield', format: formatPercent }
			]
		},
		{
			group: 'Growth',
			items: [
				{ label: 'Revenue Growth', value: 'info.revenueGrowth', format: formatPercent },
				{ label: 'Earnings Growth', value: 'info.earningsGrowth', format: formatPercent },
				{ label: 'Free Cash Flow', value: 'info.freeCashflow', format: formatLargeNumber },
				{ label: 'Profit Margins', value: 'info.profitMargins', format: formatPercent }
			]
		}
	];
	const changeRange = async (newValue: string) => {
		const currentPeriod = $page.url.searchParams.get('period') || 'ytd';

		// Don't fetch if it's the same period
		if (currentPeriod === newValue) {
			return;
		}

		let query = new SvelteURLSearchParams($page.url.searchParams.toString());
		query.set('period', newValue);

		// Update URL first
		goto(`?${query.toString()}`, { replaceState: true });

		// Fetch new data
		isLoadingHistory = true;
		try {
			const history_res = await client.GET('/api/ticker/', {
				params: {
					query: {
						period: newValue,
						ticker_name: data.ticker
					}
				}
			});

			if (history_res.response.ok && history_res.data) {
				currentHistory = history_res.data;
			}
		} catch (error) {
			console.error('Failed to fetch new history data:', error);
		} finally {
			isLoadingHistory = false;
		}
	};

	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	const deep_value = function (obj: any, path: string) {
		for (let i = 0, segments = path.split('.'), len = segments.length; i < len; i++) {
			obj = obj[segments[i]];
		}
		return obj;
	};

	const summary = data.summary as components['schemas']['KPIResponse'];
	const historical_kpis = data.historical_kpis as components['schemas']['HistoricalKPIs'] | null;

	// Fullscreen modal state
	let fullscreenChart: {
		show: boolean;
		title: string;
		dataset: { [key: string]: number[] };
		dates: string[];
		color: string;
	} = $state({
		show: false,
		title: '',
		dataset: {},
		dates: [],
		color: ''
	});

	const openFullscreen = (kpiName: string, kpiData: components['schemas']['HistoricalKPI']) => {
		fullscreenChart = {
			show: true,
			title: `${kpiName} - Historical Data`,
			dataset: { [kpiName]: kpiData.values },
			dates: kpiData.dates,
			color: '#8884d8'
		};
	};

	const openMainChartFullscreen = () => {
		fullscreenChart = {
			show: true,
			title: `${data.ticker} - Price Chart (${currentHistory.query.period})`,
			dataset: { price: currentHistory.candles, ...currentHistory.smas },
			dates: currentHistory.dates,
			color: ratioColor(currentHistory.delta)
		};
	};

	const closeFullscreen = () => {
		fullscreenChart = {
			...fullscreenChart,
			show: false
		};
	};
</script>

<div class="flex flex-col items-center">
	<h1 class="animate-fade-in text-4xl font-bold sm:text-5xl">{data.ticker}</h1>
	<p
		class="text-brand animate-fade-in mt-2 text-lg sm:text-xl"
		style={`color: ${ratioColor(currentHistory.delta)}`}
	>
		{formatPercent(currentHistory.delta!)}
	</p>
	<p class="text-sm text-gray-400">Price / ∇</p>

	<div
		class="relative my-8 flex h-56 w-full max-w-screen-lg items-center justify-center rounded-2xl bg-gradient-to-r from-[#0d182b] to-[#102139] text-gray-500 shadow-xl sm:h-64"
	>
		<!-- Fullscreen button for main chart -->
		{#if !isLoadingHistory}
			<button
				class="absolute top-2 right-2 z-10 rounded-lg bg-gray-800 p-2 text-white transition hover:bg-gray-700"
				onclick={openMainChartFullscreen}
				aria-label="View price chart in fullscreen"
			>
				<!-- Fullscreen icon -->
				<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"
					/>
				</svg>
			</button>
		{/if}

		{#if isLoadingHistory}
			<div class="flex items-center space-x-2">
				<div
					class="h-4 w-4 animate-spin rounded-full border-2 border-blue-500 border-t-transparent"
				></div>
				<span class="text-gray-400">Loading chart data...</span>
			</div>
		{:else}
			<HistoryChart
				title={`Price: ${currentHistory.query.period}`}
				dataset={{ price: currentHistory.candles, ...currentHistory.smas }}
				dates={currentHistory.dates}
				color={ratioColor(currentHistory.delta)}
			/>
		{/if}
	</div>

	<div class="mb-8 flex flex-wrap justify-center gap-2">
		{#each ranges as range (range.label)}
			<button
				class="rounded-full bg-gray-800 px-4 py-1 text-white shadow transition hover:scale-105 disabled:cursor-not-allowed disabled:opacity-50"
				disabled={isLoadingHistory}
				onclick={() => changeRange(range.value)}>{range.label}</button
			>
		{/each}
	</div>

	<div class="grid w-full max-w-screen-lg grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
		{#each kpis as group (group.group)}
			<div
				class="rounded-2xl bg-gradient-to-tr from-[#121f3d] to-[#1f2f50] p-5 shadow-lg transition hover:scale-[1.02]"
			>
				<h2 class="mb-2 font-semibold text-white">{group.group}</h2>
				<ul class="space-y-1 text-sm text-gray-300">
					{#each group.items as kpi (kpi.label)}
						{#if deep_value(summary, kpi.value) !== null}
							<li>
								{kpi.label}:
								<span class="text-brand"
									>{kpi.format
										? kpi.format(deep_value(summary, kpi.value))
										: deep_value(summary, kpi.value)}</span
								>
							</li>
						{/if}
					{/each}
				</ul>
			</div>
		{/each}
	</div>

	{#if historical_kpis}
		<h2 class="mt-8 text-2xl font-bold text-white">Historical KPIs</h2>
		<div class="grid w-full max-w-screen-lg grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
			{#each Object.entries(historical_kpis.kpis) as [kpiName, kpiData] (kpiName)}
				<div
					class="relative rounded-2xl bg-gradient-to-tr from-[#121f3d] to-[#1f2f50] p-4 shadow-lg transition hover:scale-[1.02]"
				>
					<!-- Fullscreen button -->
					{#if kpiData && kpiData.dates && kpiData.values}
						<button
							class="absolute top-2 right-2 z-10 rounded-lg bg-gray-800 p-2 text-white transition hover:bg-gray-700"
							onclick={() => openFullscreen(kpiName, kpiData)}
							aria-label="View {kpiName} in fullscreen"
						>
							<!-- Fullscreen icon -->
							<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"
								/>
							</svg>
						</button>
					{/if}

					<h3 class="mb-3 text-center font-semibold text-white">{kpiName}</h3>
					{#if kpiData && kpiData.dates && kpiData.values}
						<div class="h-48">
							<HistoryChart
								title=""
								dataset={{ [kpiName]: kpiData.values }}
								dates={kpiData.dates}
								color="#8884d8"
							/>
						</div>
					{:else}
						<div class="flex h-48 items-center justify-center">
							<p class="text-sm text-gray-400">Data not available for this KPI</p>
						</div>
					{/if}
				</div>
			{/each}
		</div>
	{:else}
		<p class="mt-8 text-lg text-gray-400">Historical data not available for this ticker.</p>
	{/if}
</div>

<!-- Fullscreen Chart Modal -->
<FullscreenChartModal
	show={fullscreenChart.show}
	title={fullscreenChart.title}
	dataset={fullscreenChart.dataset}
	dates={fullscreenChart.dates}
	color={fullscreenChart.color}
	onClose={closeFullscreen}
/>
