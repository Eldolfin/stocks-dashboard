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
			// datasets: dataset.map((data) => {
			// 	return {
			// 		label: 'Price',
			// 		data: data,
			// 		// FIXME: default css colors are ugly
			// 		borderColor: color,
			// 		backgroundColor: transparentize(color, 0.5),
			// 		yAxisID: 'y'
			// 	};
			// })
			datasets: Object.entries(dataset).map(([label, data]) => {
				return {
					label,
					data
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
				// stacked: false,
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
	onMount(() => {
		createChart();
	});

	$effect(() => {
		createChart();
	});

	onDestroy(() => {
		if (chartInstance) chartInstance.destroy();
	});
</script>

<div style="width: 800px;"><canvas bind:this={chartElt}></canvas></div>
