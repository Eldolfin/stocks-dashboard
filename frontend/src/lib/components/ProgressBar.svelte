<script lang="ts">
	import type { components } from '../../generated/api';
	import ProgressBarInner from './ProgressBarInner.svelte';

	type TaskProgressResponse = components['schemas']['TaskProgressResponse'];
	interface Props {
		title: string;
		progress: TaskProgressResponse | null;
		isComplete: boolean;
		error?: string | null;
	}

	let { title, progress, isComplete, error = null }: Props = $props();
</script>

{#if !isComplete}
	<div
		class="rounded-lg border border-gray-300 bg-white p-6 shadow-md border-gray-600 bg-gray-800"
	>
		<h3 class="mb-4 text-lg font-semibold text-gray-900 text-white">{title}</h3>

		{#if error}
			<div class="rounded-md bg-red-50 p-4 bg-red-900/20">
				<div class="flex">
					<div class="ml-3">
						<h3 class="text-sm font-medium text-red-800 text-red-200">Error</h3>
						<div class="mt-2 text-sm text-red-700 text-red-300">
							<p>{error}</p>
						</div>
					</div>
				</div>
			</div>
		{:else if progress}
			<div class="space-y-3">
				<ProgressBarInner {progress} />
			</div>
		{:else}
			<div class="space-y-3">
				<div class="text-sm text-gray-600 text-gray-300">
					<span>Starting analysis...</span>
				</div>
				<div class="h-2.5 w-full rounded-full bg-gray-200 bg-gray-700">
					<div class="h-2.5 animate-pulse rounded-full bg-blue-600" style="width: 10%"></div>
				</div>
			</div>
		{/if}
	</div>
{/if}
