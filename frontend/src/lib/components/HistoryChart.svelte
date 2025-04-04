<script lang="ts">
	import Chart, { type ChartConfiguration } from 'chart.js/auto';
	import { CHART_COLORS, months, transparentize } from '$lib/chart-utils';
	import { onDestroy, onMount } from 'svelte';
	const { title, dataset, yValuesIndex, color } = $props();
	const data = {
		labels: [],
		datasets: [
			{
				label: 'Price',
				data: dataset,
				borderColor: CHART_COLORS[color],
				backgroundColor: transparentize(CHART_COLORS[color], 0.5),
				yAxisID: 'y',
				parsing: {
					yAxisKey: yValuesIndex,
					xAxisKey: 'Date'
				}
			}
		]
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

	let chartElt;
	let chartInstance;

	const createChart = () => {
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
