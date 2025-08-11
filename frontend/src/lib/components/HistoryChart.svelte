<script lang="ts">
	import Chart, { type ChartConfiguration } from 'chart.js/auto';
	import { transparentize } from '$lib/chart-utils';
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
		showLegend?: boolean;
		zoomable?: boolean;
	}
	const {
		title,
		dataset,
		dates,
		color,
		showTickerSelector = false,
		defaultShown,
		showLegend = true,
		zoomable = true
	}: Props = $props();
	let chartElt;
	let chartInstance: Chart | undefined | null;

	// Ticker selection state - only used when showTickerSelector is true
	let selectedTickers = $state(new SvelteSet<string>());
	let selectedTickersArray = $derived(Array.from(selectedTickers));
	let availableTickers: string[] = $derived(
		showTickerSelector
			? Object.keys(dataset).filter(
					(ticker) => [undefined, -1].indexOf(defaultShown?.indexOf(ticker)) !== -1
				)
			: []
	);

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
		const mainColumns = ['Total', 'price'];
		const entries = Object.entries(filteredDataset()).sort(([labelA], [labelB]) => {
			const isMainA = mainColumns.includes(labelA);
			const isMainB = mainColumns.includes(labelB);
			return isMainA === isMainB ? 0 : isMainA ? -1 : 1;
		});
		const totalLines = entries.length;
		// Move mainData ("Total" or "price") to the front
		const data = {
			labels: dates,
			datasets: entries.map(([label, data], index) => {
				const isMainData = ['Total', 'price'].indexOf(label) !== -1;
				const mainHue = 170;
				// Generate hue separated colors (0 to 360 degrees)
				// We skip the main line since you want a special color for it
				// But if you want main line also colored by hue, just remove that condition
				const hue = isMainData ? mainHue : (360 * index) / totalLines + mainHue;
				const lineColor = `hsl(${hue}, 100%, 70%)`;
				return {
					label,
					data: [...data],
					borderColor: lineColor,
					borderWidth: isMainData ? 2 : undefined,
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
						display: showLegend
					},
					zoom: {
						pan: {
							enabled: zoomable,
							mode: 'x'
						},
						zoom: {
							wheel: {
								enabled: zoomable
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
						position: 'left',
						grid: {
							color: (ctx) => (ctx.tick.value === 0 ? 'white' : 'gray'),
							lineWidth: (ctx) => (ctx.tick.value === 0 ? 1 : 0.5)
						}
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
		// if (chartInstance) {
		// 	chartInstance.data.labels = dates;
		// 	chartInstance.data.datasets = Object.entries(filteredDataset()).map(
		// 		([label, data], index) => {
		// 			console.log('Creating dataset for:', label, 'with', data.length, 'data points');
		// 			const isMainLine = label === 'price';
		// 			const lineColor = isMainLine ? color : SMA_COLORS[index % SMA_COLORS.length];
		// 			return {
		// 				label,
		// 				data: [...data],
		// 				borderColor: lineColor,
		// 				backgroundColor: transparentize(lineColor, 0.5),
		// 				yAxisID: 'y'
		// 			};
		// 		}
		// 	);
		// 	console.log('Updating chart with', chartInstance.data.datasets.length, 'datasets');
		// 	chartInstance.update();
		// }
		// FIXME: this is suboptimal + annoying to the user
		// but for now I'm not re-assigning colors on dataset change so this is needed
		createChart();
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
	{#if zoomable}
		<button
			class="mt-4 rounded-full bg-gray-800 px-4 py-1 text-white shadow transition hover:scale-105"
			onclick={() => chartInstance?.resetZoom()}>Reset zoom</button
		>
	{/if}

	{#if showTickerSelector}
		<div class="mt-4 w-full max-w-md">
			<TickerSelector {availableTickers} bind:selectedTickers />
		</div>
	{/if}
</div>
