<script lang="ts">
	import {
		Avatar,
		Button,
		Checkbox,
		Progressbar,
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell
	} from 'flowbite-svelte';
	import { Label, Input } from 'flowbite-svelte';
	import { ArrowRightOutline, CirclePlusSolid, SearchOutline } from 'flowbite-svelte-icons';
	import type { components } from '../generated/api';
	import { client } from '$lib/typed-fetch-client';
	import { formatCurrency, formatPercent } from '$lib/format-utils';
	import { debounce } from 'chart.js/helpers';

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
	const comparedTickersUrl = () =>
		Array.from(comparedTickers)
			.map((t) => t.info.symbol)
			.join(',');
</script>

<div class="p-8">
	<Label for="input-group-1" class="mb-2 block">Search a ticker</Label>

	<form>
		<Input
			oninput={debounce(onSearch, 300)}
			bind:value={searchText}
			id="search"
			type="text"
			placeholder="Apple, Microsoft, ..."
		>
			<SearchOutline slot="left" />
		</Input>
	</form>

	{#if pendingRequest > 0}
		<Progressbar animate={true} tweenDuration={1500} progress={100} />
	{/if}
	{#if searchResult !== undefined}
		<Table class="mt-10" hoverable={true}>
			<TableHead>
				<TableHeadCell>Stock name</TableHeadCell>
				<TableHeadCell>Logo</TableHeadCell>
				<TableHeadCell>Price</TableHeadCell>
				<TableHeadCell>Today's P&L</TableHeadCell>
				<TableHeadCell>
					<Button disabled={comparedTickers.size < 2} href="/compare/{comparedTickersUrl()}"
						>Compare</Button
					>
				</TableHeadCell>
			</TableHead>
			<TableBody tableBodyClass="divide-y">
				{#each searchResult as quote}
					{#if !comparedTickers.has(quote)}
						<TableBodyRow>
							<TableBodyCell>
								<a href="/details/{quote.raw.symbol}">
									{quote.raw.longname}
								</a>
							</TableBodyCell>
							<TableBodyCell>
								<a href="/details/{quote.raw.symbol}">
									<Avatar src={quote.icon_url!} rounded />
								</a>
							</TableBodyCell>
							<TableBodyCell>
								<a href="/details/{quote.raw.symbol}">
									{formatCurrency(quote.info.currentPrice)}
								</a>
							</TableBodyCell>
							<TableBodyCell>
								<a href="/details/{quote.raw.symbol}">
									{formatPercent(quote.today_change)}
								</a>
							</TableBodyCell>
							<TableBodyCell>
								<Button
									pill={true}
									class="p-2!"
									color="green"
									on:click={() => {
										const updated = new Set(comparedTickers);
										updated.add(quote);
										comparedTickers = updated;
									}}><CirclePlusSolid class="h-6 w-6" /></Button
								>
							</TableBodyCell>
						</TableBodyRow>
					{/if}
				{/each}
				<TableBodyRow color="custom">
					<TableBodyCell></TableBodyCell>
					<TableBodyCell></TableBodyCell>
					<TableBodyCell></TableBodyCell>
					<TableBodyCell></TableBodyCell>
					<TableBodyCell></TableBodyCell>
				</TableBodyRow>
				{#each comparedTickers.values() as quote (quote.raw.symbol)}
					<TableBodyRow>
						<TableBodyCell>
							<a href="/details/{quote.raw.symbol}">
								{quote.raw.longname}
							</a>
						</TableBodyCell>
						<TableBodyCell>
							<a href="/details/{quote.raw.symbol}">
								<Avatar src={quote.icon_url!} rounded />
							</a>
						</TableBodyCell>
						<TableBodyCell>
							<a href="/details/{quote.raw.symbol}">
								{formatCurrency(quote.info.currentPrice)}
							</a>
						</TableBodyCell>
						<TableBodyCell>
							<a href="/details/{quote.raw.symbol}">
								{formatPercent(quote.today_change)}
							</a>
						</TableBodyCell>
						<TableBodyCell>
							<Checkbox
								checked
								on:change={() => {
									const updated = new Set(comparedTickers);
									updated.delete(quote);
									comparedTickers = updated;
								}}
							/>
						</TableBodyCell>
					</TableBodyRow>
				{/each}
			</TableBody>
		</Table>
	{/if}
</div>
