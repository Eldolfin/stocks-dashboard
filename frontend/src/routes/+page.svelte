<script lang="ts">
	import {
		Avatar,
		Progressbar,
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell
	} from 'flowbite-svelte';
	import { Label, Input, Spinner } from 'flowbite-svelte';
	import { SearchOutline } from 'flowbite-svelte-icons';
	import type { components } from '../generated/api';
	import { client } from '$lib/typed-fetch-client';
	import { goto } from '$app/navigation';
	import { formatCurrency, formatPercent } from '$lib/format-utils';
	import { debounce } from 'chart.js/helpers';

	let searchResult = $state<components['schemas']['Quote'][] | undefined>(undefined);
	let searchText = $state('');
	let pendingRequest = $state(0);
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
	onSearch();
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
			</TableHead>
			<TableBody tableBodyClass="divide-y">
				{#each searchResult as quote}
					<TableBodyRow
						on:click={() => {
							goto(`/details/${quote.raw.symbol}`);
						}}
					>
						<TableBodyCell>{quote.raw.longname}</TableBodyCell>
						<TableBodyCell>
							<Avatar src={quote.icon_url!} rounded />
						</TableBodyCell>
						<TableBodyCell>
							{formatCurrency(quote.info.currentPrice)}
						</TableBodyCell>
						<TableBodyCell>
							{formatPercent(quote.today_change)}
						</TableBodyCell>
					</TableBodyRow>
				{/each}
			</TableBody>
		</Table>
	{/if}
</div>
