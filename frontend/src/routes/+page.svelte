
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
		searchResult = res.data?.quotes;
	};
	if (import.meta.env.DEV) {
		onSearch();
	}
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
        <a href="/details/{quote.raw.symbol}">
          <h2 class="font-semibold text-white mb-2">{quote.raw.longname}</h2>
          <ul class="space-y-1 text-sm text-gray-300">
            <li>Price: <span class="text-brand">{formatCurrency(quote.info.currentPrice)}</span></li>
            <li>Today's P&L: <span class="text-brand">{formatPercent(quote.today_change)}</span></li>
          </ul>
        </a>
      </div>
    {/each}
  {/if}
</div>
