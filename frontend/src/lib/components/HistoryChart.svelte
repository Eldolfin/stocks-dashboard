<script lang="ts">
	import Chart, { type ChartConfiguration } from 'chart.js/auto';
	import { transparentize, SMA_COLORS } from '$lib/chart-utils';
	import { onDestroy, onMount } from 'svelte';
	import TickerSelector from './TickerSelector.svelte';
	import { SvelteSet } from 'svelte/reactivity';

	interface Props {
		title: string;
		dataset: { [key: string]: number[] };
		dates: string[];
		color: string;
		showTickerSelector?: boolean;
		fullDataset?: { [key: string]: number[] };
	}
	const { title, dataset, dates, color, showTickerSelector = false, fullDataset }: Props = $props();
	let chartElt;
	let chartInstance: Chart | undefined | null;

	// Ticker selection state - only used when showTickerSelector is true
	let selectedTickers = new SvelteSet<string>();
	let availableTickers: string[] = $derived(
		showTickerSelector && fullDataset
			? Object.keys(fullDataset).filter((key) => key !== 'total' && key !== 'Closed Positions')
			: []
	);

	// Computed dataset based on selected tickers
	let filteredDataset = $derived(() => {
		if (!showTickerSelector) {
			return dataset;
		}

		const result: { [key: string]: number[] } = {};

		// Always show total and closed positions if they exist
		if (dataset['total']) {
			result['total'] = dataset['total'];
		}
		if (dataset['Closed Positions']) {
			result['Closed Positions'] = dataset['Closed Positions'];
		}

		// Add selected individual tickers
		for (const ticker of selectedTickers) {
			if (fullDataset?.[ticker]) {
				result[ticker] = fullDataset[ticker];
			}
		}

		return result;
	});

	const createChart = () => {
		const data = {
			labels: dates,
			datasets: Object.entries(filteredDataset).map(([label, data], index) => {
				const isMainLine = label === 'price';
				const lineColor = isMainLine ? color : SMA_COLORS[index % SMA_COLORS.length];
				return {
					label,
					data: [...data],
					borderColor: lineColor,
					backgroundColor: transparentize(lineColor, 0.5),
					yAxisID: 'y'
				};
			})
		};
		const config = {
			type: 'line',
			data: data,
			options: {
				responsive: true,
				interaction: {
					mode: 'index',
					intersect: false
				},
				plugins: {
					title: {
						display: true,
						text: title
					},
					tooltip: {
						enabled: true
					},
					legend: {
						display: false
					},
					zoom: {
						pan: {
							enabled: true,
							mode: 'x'
						},
						zoom: {
							wheel: {
								enabled: true
							},
							pinch: {
								enabled: true
							},
							mode: 'x'
						}
					}
				},
				scales: {
					y: {
						type: 'linear',
						display: true,
						position: 'left'
					},
					x: {
						type: 'timeseries'
					}
				},
				elements: {
					point: {
						radius: 0
					},
					line: {
						borderWidth: 1
					}
				}
			}
		} satisfies ChartConfiguration;

		if (chartInstance) {
			chartInstance.destroy();
			chartInstance = null; // Explicitly set to null after destroying
		}
		chartInstance = new Chart(chartElt! as HTMLCanvasElement, config);
	};

	onMount(async () => {
		const zoomPlugin = await import('chartjs-plugin-zoom');
		Chart.register(zoomPlugin.default);
		createChart();
	});

	$effect(() => {
		if (chartInstance) {
			chartInstance.data.labels = dates;
			chartInstance.data.datasets = Object.entries(filteredDataset).map(([label, data], index) => {
				const isMainLine = label === 'price';
				const lineColor = isMainLine ? color : SMA_COLORS[index % SMA_COLORS.length];
				return {
					label,
					data: [...data],
					borderColor: lineColor,
					backgroundColor: transparentize(lineColor, 0.5),
					yAxisID: 'y'
				};
			});
			chartInstance.update();
		}
	});

	onDestroy(() => {
		if (chartInstance) {
			chartInstance.destroy();
			chartInstance = null; // Explicitly set to null after destroying
		}
	});
</script>

<div class="flex h-full w-full flex-col items-center justify-center">
	<canvas bind:this={chartElt} id="history-chart"></canvas>
	<button
		class="mt-4 rounded-full bg-gray-800 px-4 py-1 text-white shadow transition hover:scale-105"
		onclick={() => chartInstance?.resetZoom()}>Reset zoom</button
	>

	{#if showTickerSelector}
		<div class="mt-4 w-full max-w-md">
			<TickerSelector
				{availableTickers}
				{selectedTickers}
				onTickerToggle={() => {
					// Trigger reactivity - the chart will update via the $effect
				}}
			/>
		</div>
	{/if}
</div>
