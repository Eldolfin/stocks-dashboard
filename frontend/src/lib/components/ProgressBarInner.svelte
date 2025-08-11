<script lang="ts">
	import type { components } from '../../generated/api';
	import Self from './ProgressBarInner.svelte';

	type TaskProgressResponse = components['schemas']['TaskProgressResponse'];
	interface Props {
		progress: TaskProgressResponse;
	}

	let { progress }: Props = $props();

	let progressPercentage = $derived(
		progress ? (progress.step_number / progress.step_count) * 100 : 0
	);
</script>

<div class="flex justify-between text-sm text-gray-600 dark:text-gray-300">
	<span>{progress.step_name}</span>
	<span>{progress.step_number} / {progress.step_count}</span>
</div>
<div class="h-2.5 w-full rounded-full bg-gray-200 dark:bg-gray-700">
	<div
		class="h-2.5 rounded-full bg-blue-600 transition-all duration-300 ease-out"
		style="width: {progressPercentage}%"
	></div>
</div>

{#if progress.sub_task !== null}
	<Self progress={progress.sub_task} />
{/if}
