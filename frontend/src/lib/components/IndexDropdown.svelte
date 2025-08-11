<script lang="ts">
	import { onMount } from 'svelte';
	import { indexOptions, loadIndexOptions, type IndexOption } from '$lib/stores/indexOptions';
	import { get } from 'svelte/store';

	export let selected: string | null = null;
	export let onSelect: (option: IndexOption) => void;

	let search = '';
	let filtered = [];

	onMount(() => {
		loadIndexOptions();
	});

	$: filtered = get(indexOptions).filter((opt) =>
		opt.label.toLowerCase().includes(search.toLowerCase())
	);
</script>

<div class="mx-auto w-full max-w-md">
	<input
		type="text"
		placeholder="Search index..."
		bind:value={search}
		class="mb-2 w-full rounded border p-2"
	/>
	<ul class="max-h-48 overflow-auto rounded border bg-white shadow">
		{#each filtered as opt}
			<li
				class="cursor-pointer p-2 hover:bg-gray-200 {selected === opt.value ? 'bg-blue-100' : ''}"
				on:click={() => {
					selected = opt.value;
					onSelect(opt);
				}}
			>
				{opt.label}
			</li>
		{/each}
	</ul>
</div>
