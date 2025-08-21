<script lang="ts">
	import { onMount } from 'svelte';
	import { indexOptions, loadIndexOptions, type IndexOption } from '$lib/stores/indexOptions';
	import { writable, derived } from 'svelte/store';

	let {
		selected = $bindable(null),
		onSelect
	}: { selected?: string | null; onSelect: (option: IndexOption) => void } = $props();

	const search = writable('');

	onMount(() => {
		loadIndexOptions();
	});

	const filtered = derived([indexOptions, search], ([$indexOptions, $search]) =>
		$indexOptions.filter((opt) => opt.label.toLowerCase().includes($search.toLowerCase()))
	);
</script>

<div class="mx-auto w-full max-w-md">
	<input
		type="text"
		placeholder="Search index..."
		bind:value={$search}
		class="mb-2 w-full rounded border border-gray-300 border-gray-600 bg-gray-700 bg-white p-2  text-white placeholder-gray-400"
	/>
	<ul
		class="max-h-48 overflow-auto rounded border border-gray-300 border-gray-600 bg-gray-800 bg-white shadow"
	>
		{#each $filtered as opt (opt.value)}
			<button
				type="button"
				class="w-full cursor-pointer p-2 text-left  text-white hover:bg-gray-200 hover:bg-gray-700 {selected ===
				opt.value
					? 'bg-blue-100 bg-blue-900'
					: ''}"
				onclick={() => {
					selected = opt.value;
					onSelect(opt);
				}}
			>
				{opt.label}
			</button>
		{/each}
	</ul>
</div>
