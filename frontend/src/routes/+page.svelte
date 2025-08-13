<script lang="ts">
	export const ssr = false;
	import { client } from '$lib/typed-fetch-client';
	import { formatPercent } from '$lib/format-utils';
	import type { components } from '../generated/api';
	import { SvelteSet, SvelteMap, SvelteURLSearchParams } from 'svelte/reactivity';
	import { page } from '$app/state';
	import { browser } from '$app/environment';
	type Ticker = components['schemas']['Quote'];

	let searchResult = $state<Ticker[] | undefined>(undefined);
	const defaultSearch = import.meta.env.DEV ? 'apple' : '';
	let searchText = $state(defaultSearch);
	let pendingRequest = $state(0);

	// Store selected ticker symbols
	let comparedTickers = new SvelteSet<string>();
	// Cache all loaded ticker objects to retrieve details later
	let tickerCache = new SvelteMap<string, Ticker>();

	// Derived state for the full objects of selected tickers
	let selectedTickerObjects = $derived(
		Array.from(comparedTickers)
			.map((symbol) => tickerCache.get(symbol))
			.filter(Boolean) as Ticker[]
	);

	const onSearch = async () => {
		if (!searchText) {
			searchResult = undefined;
			return;
		}
		pendingRequest += 1;
		const { data } = await client
			.GET('/api/search/', {
				params: {
					query: {
						query: searchText
					}
				}
			})
			.finally(() => (pendingRequest -= 1));

		if (data) {
			const newResults = data.quotes || [];
			// Update cache with new results
			newResults.forEach((ticker: Ticker) => tickerCache.set(ticker.symbol, ticker));
			searchResult = newResults;

			if (browser && page.url.pathname == '/') {
				// change url param
				let query = new SvelteURLSearchParams(page.url.searchParams.toString());
				query.set('q', data.query.query);
				window.history.replaceState(history.state, '', `?${query}`);
			}
		}
	};

	if (import.meta.env.DEV) {
		onSearch();
	}

	const comparedTickersUrl = () => Array.from(comparedTickers).join(',');
	function handleCompareChange(e: Event, quote: Ticker) {
		const target = e.target as HTMLInputElement;
		const symbol = quote.symbol;

		if (target.checked) {
			comparedTickers.add(symbol);
		} else {
			comparedTickers.delete(symbol);
		}
	}
</script>

<!-- Header -->
<div class="text-center">
	<h1 class="animate-fade-in text-4xl font-bold sm:text-5xl">WallStreet Bets 💸</h1>
</div>

<form class="my-8">
	<input
		oninput={onSearch}
		bind:value={searchText}
		id="search"
		type="text"
		placeholder="Apple, Microsoft, ..."
		class="focus:ring-brand w-full rounded-full bg-gray-800 px-4 py-2 text-white shadow focus:ring-2 focus:outline-none"
	/>
</form>

<!-- Stat Cards -->
<div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
	{#if searchResult !== undefined}
		{#each searchResult as quote (quote.symbol)}
			<div
				class="flex h-full flex-col justify-between rounded-2xl bg-gradient-to-tr from-[#121f3d] to-[#1f2f50] p-5 shadow-lg transition hover:scale-[1.02]"
			>
				<div>
					<a href="/details?ticker={quote.symbol}" class="flex flex-col items-center text-center">
						{#if quote.icon_url}
							<img src={quote.icon_url} alt="" class="mb-2 h-12 w-12 rounded-full" />
						{/if}
						<h2 class="text-lg font-semibold text-white">{quote.long_name}</h2>
					</a>
				</div>
				<div class="mt-auto">
					<ul class="space-y-1 text-center text-sm text-gray-300">
						<!--<li>
							Price: <span class="text-brand">{formatCurrency(quote.currentPrice)}</span>
						</li>-->
						{#if quote.today_change}
							<li>
								Today's P&L: <span class="text-brand">{formatPercent(quote.today_change)}</span>
							</li>
						{/if}
					</ul>
					<div class="mt-2 flex justify-end">
						<input
							type="checkbox"
							onclick={(e) => handleCompareChange(e, quote)}
							class="form-checkbox text-brand h-5 w-5 rounded border-gray-300"
							checked={comparedTickers.has(quote.symbol)}
						/>
					</div>
				</div>
			</div>
		{/each}
	{/if}
</div>

{#if selectedTickerObjects.length > 0}
	<div class="mt-8 rounded-2xl bg-gradient-to-tr from-[#121f3d] to-[#1f2f50] p-5 shadow-lg">
		<h2 class="mb-2 font-semibold text-white">Selected for Comparison:</h2>
		<ul class="space-y-1 text-sm text-gray-300">
			{#each selectedTickerObjects as quote (quote.symbol)}
				<li class="flex items-center justify-between">
					<a href="/details?ticker={quote.symbol}" class="flex items-center">
						{#if quote.icon_url}
							<img
								src={quote.icon_url}
								alt=""
								class="mr-2 h-6 w-6 rounded-full"
								onerror={(e) => {
									(e.target as HTMLImageElement).style.display = 'none';
								}}
							/>
						{/if}
						{quote.long_name}
					</a>
					<button
						onclick={() => {
							comparedTickers.delete(quote.symbol);
						}}
						class="text-gray-400 transition hover:text-white"
					>
						&times;
					</button>
				</li>
			{/each}
		</ul>
		<div class="mt-4 flex justify-end">
			<a
				href="/compare?tickers={comparedTickersUrl()}"
				class="bg-brand rounded-full px-4 py-2 font-semibold text-black shadow transition hover:scale-105 {comparedTickers.size <
				2
					? 'cursor-not-allowed opacity-50'
					: ''}"
				class:cursor-not-allowed={comparedTickers.size < 2}
				class:opacity-50={comparedTickers.size < 2}
				aria-disabled={comparedTickers.size < 2}
			>
				Compare Selected ({comparedTickers.size})
			</a>
		</div>
	</div>
{/if}
