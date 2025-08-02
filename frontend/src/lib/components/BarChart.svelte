<script lang="ts">
	import 'chartjs-adapter-moment';
	import Chart from 'chart.js/auto';
	import { browser } from '$app/environment';
	import { mount, onMount } from 'svelte';

	type Dataset = Map<String, number[]>;
	interface Props {
		title: string;
		dataset: Dataset;
		dates: string[];
		color: string;
	}
	const { title, dataset, dates, color }: Props = $props();
	let chartInstance: Chart | undefined = $state();

	function chart(node: HTMLCanvasElement, dataset: Dataset) {
		function setupChart(dataset: Dataset) {
			chartInstance = new Chart(node, {
				type: 'bar',
				data: {
					labels: dates,
					datasets: Array.from(
						dataset.keys().map((label) => {
							return {
								label: label.toString(),
								data: dataset.get(label)!
							};
						})
					)
				},
				options: {
					scales: {
						y: {
							beginAtZero: true
						},
						x: {
							type: 'timeseries'
						}
					},
					plugins: {
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
					}
				}
			});
		}
		setupChart(dataset);
		return {
			update(dataset: Dataset) {
				chartInstance?.destroy();
				setupChart(dataset);
			},
			destroy() {
				chartInstance?.destroy();
			}
		};
	}
	onMount(async () => {
		if (browser) {
			const zoomPlugin = await import('chartjs-plugin-zoom');
			Chart.register(zoomPlugin.default);
		}
	});
</script>

<div class="w-full">
	<canvas class="chart" use:chart={$state.snapshot(dataset)}></canvas>
	<button class="px-4 py-1 rounded-full bg-gray-800 text-white shadow hover:scale-105 transition mt-4" onclick={() => chartInstance?.resetZoom()}>Reset zoom</button>
</div>