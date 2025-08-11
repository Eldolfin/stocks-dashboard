<script lang="ts">
	interface Props {
		title: string;
		progress?: {
			step_name: string;
			step_number: number;
			step_count: number;
		} | null;
		isComplete?: boolean;
		error?: string | null;
	}

	let { title, progress, isComplete = false, error = null }: Props = $props();

	let progressPercentage = $derived(
		progress ? (progress.step_number / progress.step_count) * 100 : 0
	);
</script>

{#if !isComplete}

<div
	class="rounded-lg border border-gray-300 bg-white p-6 shadow-md dark:border-gray-600 dark:bg-gray-800"
>
	<h3 class="mb-4 text-lg font-semibold text-gray-900 dark:text-white">{title}</h3>

	{#if error}
		<div class="rounded-md bg-red-50 p-4 dark:bg-red-900/20">
			<div class="flex">
				<div class="ml-3">
					<h3 class="text-sm font-medium text-red-800 dark:text-red-200">Error</h3>
					<div class="mt-2 text-sm text-red-700 dark:text-red-300">
						<p>{error}</p>
					</div>
				</div>
			</div>
		</div>
	{:else if progress}
		<div class="space-y-3">
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
		</div>
	{:else}
		<div class="space-y-3">
			<div class="text-sm text-gray-600 dark:text-gray-300">
				<span>Starting analysis...</span>
			</div>
			<div class="h-2.5 w-full rounded-full bg-gray-200 dark:bg-gray-700">
				<div class="h-2.5 animate-pulse rounded-full bg-blue-600" style="width: 10%"></div>
			</div>
		</div>
	{/if}
</div>
{/if}
