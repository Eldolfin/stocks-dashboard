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
		defaultShown?: string[];
	}
	const {
		title,
		dataset,
		dates,
		color,
		showTickerSelector = false,
		defaultShown
	}: Props = $props();
	let chartElt;
	let chartInstance: Chart | undefined | null;

	// Ticker selection state - only used when showTickerSelector is true
	let selectedTickers = $state(new SvelteSet<string>());
	let selectedTickersArray = $derived(Array.from(selectedTickers));
	let availableTickers: string[] = $derived(showTickerSelector ?
		Object.keys(dataset).filter(ticker =>
			ticker !== 'total' &&
			ticker !== 'Closed Positions' &&
			ticker !== 'price'
		) : []);

	// Computed dataset based on selected tickers
	let filteredDataset = $derived(() => {
		console.log('filteredDataset recalculating, selectedTickers size:', selectedTickers.size);
		console.log('selectedTickersArray:', selectedTickersArray);

		if (!showTickerSelector) {
			return dataset;
		}

		const result: { [key: string]: number[] } = {};

		if (defaultShown) {
			for (const ticker of defaultShown) {
				result[ticker] = dataset[ticker];
			}
		}

		// Add selected individual tickers
		// Use the derived array to ensure proper reactivity tracking
		for (const ticker of selectedTickersArray) {
			if (dataset[ticker]) {
				console.log('Adding ticker to chart:', ticker);
				result[ticker] = dataset[ticker];
			}
		}

		console.log('filteredDataset result keys:', Object.keys(result));
		return result;
	});

	const createChart = () => {
		const data = {
			labels: dates,
			datasets: Object.entries(filteredDataset()).map(([label, data], index) => {
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
						enabled: true,
						itemSort: function (a, b) {
							// Sort tooltip items by y-axis value (descending - highest first)
							const aValue = a?.parsed?.y ?? 0;
							const bValue = b?.parsed?.y ?? 0;
							return bValue - aValue;
						}
					},
					legend: {
						display: true
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
		console.log('Chart effect triggered, filteredDataset keys:', Object.keys(filteredDataset()));
		if (chartInstance) {
			chartInstance.data.labels = dates;
			chartInstance.data.datasets = Object.entries(filteredDataset()).map(
				([label, data], index) => {
					console.log('Creating dataset for:', label, 'with', data.length, 'data points');
					const isMainLine = label === 'price';
					const lineColor = isMainLine ? color : SMA_COLORS[index % SMA_COLORS.length];
					return {
						label,
						data: [...data],
						borderColor: lineColor,
						backgroundColor: transparentize(lineColor, 0.5),
						yAxisID: 'y'
					};
				}
			);
			console.log('Updating chart with', chartInstance.data.datasets.length, 'datasets');
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
				bind:selectedTickers
			/>
		</div>
	{/if}
</div>
