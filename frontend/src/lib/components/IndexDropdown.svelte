<script lang="ts">
	import { onMount } from 'svelte';
	import { indexOptions, loadIndexOptions, type IndexOption } from '$lib/stores/indexOptions';

	let { selected = $bindable(null), onSelect }: { selected?: string | null; onSelect: (option: IndexOption) => void } = $props();

	let search = '';

	onMount(() => {
		loadIndexOptions();
	});

	const filtered = $derived(
		$indexOptions.filter((opt) =>
			opt.label.toLowerCase().includes(search.toLowerCase())
		)
	);
</script>

<div class="mx-auto w-full max-w-md">
	<input
		type="text"
		placeholder="Search index..."
		bind:value={search}
		class="mb-2 w-full rounded border border-gray-300 bg-white p-2 text-gray-900 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400"
	/>
	<ul class="max-h-48 overflow-auto rounded border border-gray-300 bg-white shadow dark:border-gray-600 dark:bg-gray-800">
		{#each filtered as opt}
			<button
				type="button"
				class="w-full cursor-pointer p-2 text-left text-gray-900 hover:bg-gray-200 dark:text-white dark:hover:bg-gray-700 {selected === opt.value ? 'bg-blue-100 dark:bg-blue-900' : ''}"
				on:click={() => {
					selected = opt.value;
					onSelect(opt);
				}}
			>
				{opt.label}
			</button>
		{/each}
	</ul>
</div>
