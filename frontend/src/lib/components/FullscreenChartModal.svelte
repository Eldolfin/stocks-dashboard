<script lang="ts">
	import HistoryChart from './HistoryChart.svelte';
	import { fly, fade } from 'svelte/transition';

	interface Props {
		show: boolean;
		title: string;
		dataset: { [key: string]: number[] };
		dates: string[];
		color: string;
		onClose: () => void;
	}

	const { show, title, dataset, dates, color, onClose }: Props = $props();

	// Handle escape key to close modal
	const handleKeydown = (e: KeyboardEvent) => {
		if (e.key === 'Escape') {
			onClose();
		}
	};
</script>

<svelte:window on:keydown={handleKeydown} />

{#if show}
	<!-- Modal backdrop -->
	<div
		class="bg-opacity-75 fixed inset-0 z-50 flex items-center justify-center bg-black"
		transition:fade={{ duration: 300 }}
		onclick={(e) => e.target === e.currentTarget && onClose()}
		onkeydown={(e) => e.key === 'Enter' && e.target === e.currentTarget && onClose()}
		role="dialog"
		aria-modal="true"
		aria-labelledby="modal-title"
		tabindex="-1"
	>
		<!-- Modal content -->
		<div
			class="relative h-screen w-screen bg-gradient-to-br from-[#0a1629] to-[#1a2332] p-6"
			transition:fly={{ y: 50, duration: 400 }}
			role="main"
		>
			<!-- Header with back button -->
			<div class="mb-6 flex items-center justify-between">
				<button
					class="flex items-center gap-2 rounded-lg bg-gray-800 px-4 py-2 text-white transition hover:bg-gray-700"
					onclick={onClose}
					aria-label="Close fullscreen view"
				>
					<!-- Back arrow icon -->
					<svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M10 19l-7-7m0 0l7-7m-7 7h18"
						/>
					</svg>
					Back
				</button>
				<h1 id="modal-title" class="text-2xl font-bold text-white">
					{title}
				</h1>
				<div class="w-20"></div>
				<!-- Spacer for centering -->
			</div>

			<!-- Chart container -->
			<div class="h-[calc(100vh-8rem)] w-full">
				<HistoryChart {title} {dataset} {dates} {color} />
			</div>
		</div>
	</div>
{/if}
