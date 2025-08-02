<script lang="ts">
	import { client } from '$lib/typed-fetch-client';
	import { formatCurrency, formatPercent } from '$lib/format-utils';
	import { debounce } from 'chart.js/helpers';
  import type { components } from '../generated/api';

	type Ticker = components['schemas']['Quote'];

	let searchResult = $state<Ticker[] | undefined>(undefined);
	const defaultSearch = import.meta.env.DEV ? 'apple' : '';
	let searchText = $state(defaultSearch);
	let pendingRequest = $state(0);
	let comparedTickers = $state(new Set<Ticker>());
	const onSearch = async () => {
		if (!searchText) {
			searchResult = undefined;
			return;
		}
		pendingRequest += 1;
		const res = await client
			.GET('/api/search/', {
				params: {
					query: {
						query: searchText
					}
				}
			})
			.finally(() => (pendingRequest -= 1));

		const newResults = res.data?.quotes || [];
		// Merge new results with already compared tickers to keep them visible
		const mergedResults = new Map<string, Ticker>();
		comparedTickers.forEach(ticker => mergedResults.set(ticker.raw.symbol, ticker));
		newResults.forEach(ticker => mergedResults.set(ticker.raw.symbol, ticker));
		searchResult = Array.from(mergedResults.values());
	};
	if (import.meta.env.DEV) {
		onSearch();
	}
	const comparedTickersUrl = () =>
		Array.from(comparedTickers)
			.map((t) => t.raw.symbol)
			.join(',');
</script>

<!-- Header -->
<div class="text-center">
  <h1 class="text-4xl sm:text-5xl font-bold animate-fade-in">Search</h1>
</div>


<form class="my-8">
  <input
    oninput={debounce(onSearch, 300)}
    bind:value={searchText}
    id="search"
    type="text"
    placeholder="Apple, Microsoft, ..."
    class="w-full px-4 py-2 rounded-full bg-gray-800 text-white shadow focus:outline-none focus:ring-2 focus:ring-brand"
  />
</form>


<!-- Stat Cards -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
  {#if searchResult !== undefined}
    {#each searchResult as quote}
      <div class="p-5 bg-gradient-to-tr from-[#121f3d] to-[#1f2f50] rounded-2xl shadow-lg hover:scale-[1.02] transition">
          <a href="/details/{quote.raw.symbol}" class="flex items-center">
            {#if quote.icon_url}
                              <img src={quote.icon_url} alt="" class="w-6 h-6 mr-2 rounded-full" onerror={() => { this.style.display='none' }} />
            {/if}
            <h2 class="font-semibold text-white mb-2">{quote.raw.longname}</h2>
            <ul class="space-y-1 text-sm text-gray-300">
              <li>Price: <span class="text-brand">{formatCurrency(quote.info.currentPrice)}</span></li>
              <li>Today's P&L: <span class="text-brand">{formatPercent(quote.today_change)}</span></li>
            </ul>
          </a>
          <div class="flex justify-end mt-2">
            <input
              type="checkbox"
              onchange={(e) => {
                if (e.target.checked) {
                  comparedTickers.add(quote);
                } else {
                  comparedTickers.delete(quote);
                }
                comparedTickers = comparedTickers; // Trigger reactivity
              }}
              class="form-checkbox h-5 w-5 text-brand rounded border-gray-300"
              checked={comparedTickers.has(quote)}
            />
          </div>
        </div>
    {/each}
  {/if}
</div>

{#if comparedTickers.size > 0}
  <div class="mt-8 p-5 bg-gradient-to-tr from-[#121f3d] to-[#1f2f50] rounded-2xl shadow-lg">
    <h2 class="font-semibold text-white mb-2">Selected for Comparison:</h2>
    <ul class="space-y-1 text-sm text-gray-300">
      {#each Array.from(comparedTickers) as quote (quote.raw.symbol)}
        <li class="flex items-center justify-between">
          <a href="/details/{quote.raw.symbol}" class="flex items-center">
            {#if quote.icon_url}
              <img src={quote.icon_url} alt="" class="w-6 h-6 mr-2 rounded-full" onerror={() => { this.style.display='none' }} />
            {/if}
            {quote.raw.longname}
          </a>
          <button
            onclick={() => {
              comparedTickers.delete(quote);
              comparedTickers = comparedTickers; // Trigger reactivity
            }}
            class="text-gray-400 hover:text-white transition"
          >
            &times;
          </button>
        </li>
      {/each}
    </ul>
    <div class="flex justify-end mt-4">
      <a
        href="/compare/{comparedTickersUrl()}"
        class="px-4 py-2 rounded-full bg-brand text-black font-semibold shadow hover:scale-105 transition {comparedTickers.size < 2 ? 'opacity-50 cursor-not-allowed' : ''}"
        class:cursor-not-allowed={comparedTickers.size < 2}
        class:opacity-50={comparedTickers.size < 2}
        aria-disabled={comparedTickers.size < 2}
      >
        Compare Selected ({comparedTickers.size})
      </a>
    </div>
  </div>
{/if}