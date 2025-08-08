<script lang="ts">
	import Chart, { type ChartConfiguration } from 'chart.js/auto';
	import { transparentize, SMA_COLORS } from '$lib/chart-utils';
	import { onDestroy, onMount } from 'svelte';

	interface Props {
		title: string;
		dataset: { [key: string]: number[] };
		dates: string[];
		color: string;
	}
	const { title, dataset, dates, color }: Props = $props();
	let chartElt;
	let chartInstance: Chart | undefined | null;

	const createChart = () => {
		const data = {
			labels: dates,
			datasets: Object.entries(dataset).map(([label, data], index) => {
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
			chartInstance.data.datasets = Object.entries(dataset).map(([label, data], index) => {
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

<div class="flex h-full w-full items-center justify-center">
	<canvas bind:this={chartElt} id="history-chart"></canvas>
</div>
