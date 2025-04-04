<script lang="ts">
	import {
		Avatar,
		Button,
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell
	} from 'flowbite-svelte';
	import { Label, Input } from 'flowbite-svelte';
	import { SearchOutline } from 'flowbite-svelte-icons';
	import type { components } from '../generated/api';
	import { client } from '$lib/typed-fetch-client';
	import { goto } from '$app/navigation';

	let searchResult = $state<components['schemas']['Quote'][] | undefined>(undefined);
	let searchText = $state('apple');
	const onSearch = async () => {
		const res = await client.GET('/api/search/', {
			params: {
				query: {
					query: searchText
				}
			}
		});
		searchResult = res.data?.quotes;
	};
	onSearch();
</script>

<div class="p-8">
	<Label for="input-group-1" class="mb-2 block">Search a ticker</Label>

	<form onsubmit={onSearch}>
		<Input bind:value={searchText} id="search" type="text" placeholder="Apple, Microsoft, ...">
			<SearchOutline slot="left" class="h-5 w-5 text-gray-500 dark:text-gray-400" />
		</Input>
	</form>

	{#if searchResult !== undefined}
		<Table class="mt-10" hoverable={true}>
			<TableHead>
				<TableHeadCell>Stock name</TableHeadCell>
				<TableHeadCell>Logo</TableHeadCell>
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
							<Avatar src={quote.icon_url} rounded/>
						</TableBodyCell>
					</TableBodyRow>
				{/each}
			</TableBody>
		</Table>
	{/if}
</div>
