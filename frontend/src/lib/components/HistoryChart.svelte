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
	let chartInstance: Chart | undefined;

	const createChart = () => {
		const data = {
			labels: dates,
			datasets: Object.entries(dataset).map(([label, data], index) => {
				const isMainLine = label === 'price';
				const lineColor = isMainLine ? color : SMA_COLORS[index % SMA_COLORS.length];
				return {
					label,
					data,
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
			chartInstance.destroy(); // Destroy old chart before creating a new one
		}
		chartInstance = new Chart(chartElt! as HTMLCanvasElement, config);
	};

	onMount(async () => {
		const zoomPlugin = await import('chartjs-plugin-zoom');
		Chart.register(zoomPlugin.default);
		createChart();
	});

	$effect(() => {
		createChart();
	});

	onDestroy(() => {
		if (chartInstance) chartInstance.destroy();
	});
</script>

<div class="flex h-full w-full items-center justify-center">
	<canvas bind:this={chartElt}></canvas>
</div>
