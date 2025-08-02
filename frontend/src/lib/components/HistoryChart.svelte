<script lang="ts">
	import Chart, { type ChartConfiguration } from 'chart.js/auto';
	import { transparentize } from '$lib/chart-utils';
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
			datasets: Object.entries(dataset).map(([label, data]) => {
				return {
					label,
					data,
					borderColor: color,
					backgroundColor: transparentize(color, 0.5),
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

<div class="w-full h-full"><canvas bind:this={chartElt}></canvas></div>