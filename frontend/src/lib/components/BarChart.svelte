<script lang="ts">
	import 'chartjs-adapter-moment';
	import Chart from 'chart.js/auto';

	type Dataset = Map<String, number[]>;
	interface Props {
		title: string;
		dataset: Dataset;
		dates: number[];
		color: string;
	}
	const { title, dataset, dates, color }: Props = $props();
	let chartInstance: Chart | undefined = $state();

	function chart(node: HTMLCanvasElement, dataset: Dataset) {
		function setupChart(dataset: Dataset) {
			chartInstance = new Chart(node, {
				type: 'bar',
				data: {
					labels: dates
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
						}
					}
				}
			});
		}
		console.log(dataset);
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
</script>

<div style="width: 800px;">
	<canvas class="chart" use:chart={$state.snapshot(dataset)}></canvas>
</div>
