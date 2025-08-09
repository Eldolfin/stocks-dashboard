<script lang="ts">
	interface Props {
		availableTickers: string[];
		selectedTickers: string[]; // Change from SvelteSet to array
	}

	// Props (with binding capability)
	let { availableTickers, selectedTickers = $bindable() }: Props = $props();

	let searchText = $state('');

	// Filter available tickers based on search text
	let filteredTickers = $derived(
		availableTickers.filter((ticker) =>
			ticker.toLowerCase().includes(searchText.toLowerCase())
		)
	);

	function handleTickerSelect(ticker: string) {
		const index = selectedTickers.indexOf(ticker);
		if (index >= 0) {
			// Remove ticker
			selectedTickers.splice(index, 1);
		} else {
			// Add ticker
			selectedTickers.push(ticker);
		}
		// Trigger reactivity
		selectedTickers = [...selectedTickers];
	}

	function isTickerSelected(ticker: string): boolean {
		return selectedTickers.includes(ticker);
	}
</script>

<div class="mt-4">
	<!-- Search Input -->
	<input
		bind:value={searchText}
		type="text"
		placeholder="Search tickers..."
		class="focus:ring-brand w-full rounded-full bg-gray-800 px-4 py-2 text-white shadow focus:ring-2 focus:outline-none"
	/>

	<!-- Dropdown -->
	{#if searchText && filteredTickers.length > 0}
		<div class="mt-2 max-h-40 overflow-y-auto rounded-lg bg-gray-800 shadow-lg">
			{#each filteredTickers as ticker (ticker)}
				<button
					onclick={() => handleTickerSelect(ticker)}
					class="block w-full px-4 py-2 text-left text-white transition hover:bg-gray-700"
				>
					{ticker}
					{#if isTickerSelected(ticker)}
						<span class="text-brand ml-2">✓</span>
					{/if}
				</button>
			{/each}
		</div>
	{/if}

	<!-- Selected Tickers List -->
	{#if selectedTickers.length > 0}
		<div class="mt-4 rounded-2xl bg-gradient-to-tr from-[#121f3d] to-[#1f2f50] p-4 shadow-lg">
			<h3 class="mb-2 font-semibold text-white">Selected Tickers:</h3>
			<ul class="space-y-1 text-sm text-gray-300">
				{#each selectedTickers as ticker (ticker)}
					<li class="flex items-center justify-between">
						<span>{ticker}</span>
						<button
							onclick={() => handleTickerSelect(ticker)}
							class="text-gray-400 transition hover:text-white"
						>
							&times;
						</button>
					</li>
				{/each}
			</ul>
		</div>
	{/if}
</div>
