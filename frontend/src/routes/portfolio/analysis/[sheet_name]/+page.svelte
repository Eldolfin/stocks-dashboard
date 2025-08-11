<script lang="ts">
	import { client } from '../../../../lib/typed-fetch-client';
	import type { components } from '../../../../generated/api.js';
	import BarChart from '$lib/components/BarChart.svelte';
	import HistoryChart from '$lib/components/HistoryChart.svelte';
	import ProgressBar from '$lib/components/ProgressBar.svelte';
	import { page } from '$app/stores'; // Import page store

	interface EtoroData {
		close_date: string[];
		closed_trades: number[];
		profit_usd: number[];
	}

	interface EtoroEvolutionData {
		evolution: {
			parts: { [key: string]: number[] };
			dates: string[];
		};
	}

	type Precision = components['schemas']['PrecisionEnum'];
	type TaskProgressResponse = components['schemas']['TaskProgressResponse'];

	const precision_values: Array<[string, Precision]> = [
		['Year', 'Y'],
		['Month', 'M'],
		['Day', 'D']
	];

	let trades_data: EtoroData | undefined = $state(undefined);
	let evolution_data: EtoroEvolutionData | undefined = $state(undefined);
	let precision_index: number = $state(1); // 'M'
	let error: string | undefined = $state(undefined);

	// Task tracking state
	let tradesTaskId: string | undefined = $state(undefined);
	let evolutionTaskId: string | undefined = $state(undefined);
	let tradesProgress: TaskProgressResponse | null = $state(null);
	let evolutionProgress: TaskProgressResponse | null = $state(null);
	let tradesComplete = $state(false);
	let evolutionComplete = $state(false);
	let tradesError: string | null = $state(null);
	let evolutionError: string | null = $state(null);

	// Function to poll task status until completion
	async function pollTaskStatus(
		taskId: string,
		onProgress: (progress: TaskProgressResponse | null) => void,
		onComplete: (result: EtoroData | EtoroEvolutionData) => void,
		onError: (error: string) => void
	) {
		const poll = async () => {
			try {
				const statusRes = await client.GET('/api/task_status/{task_id}', {
					params: { path: { task_id: taskId } }
				});

				if (statusRes.error) {
					onError('Failed to get task status');
					return;
				}

				const status = statusRes.data!;
				onProgress(status.progress || null);

				if (status.status === 'completed') {
					// Get the result
					const resultRes = await client.GET('/api/task_result/{task_id}', {
						params: { path: { task_id: taskId } }
					});

					if (resultRes.error) {
						onError('Failed to get task result');
						return;
					}

					onComplete(resultRes.data!.result as unknown as EtoroData | EtoroEvolutionData);
				} else if (status.status === 'failed') {
					onError(status.error || 'Task failed');
				} else {
					// Continue polling
					setTimeout(poll, 1000);
				}
			} catch (err) {
				onError(`Polling error: ${err}`);
			}
		};

		poll();
	}

	// Function to start async analysis
	async function startAnalyses(reportName: string, precision: Precision) {
		// Reset state
		trades_data = undefined;
		evolution_data = undefined;
		tradesTaskId = undefined;
		evolutionTaskId = undefined;
		tradesProgress = null;
		evolutionProgress = null;
		tradesComplete = false;
		evolutionComplete = false;
		tradesError = null;
		evolutionError = null;
		error = undefined;

		try {
			// Start both tasks concurrently
			const [tradesTaskRes, evolutionTaskRes] = await Promise.all([
				client.GET('/api/etoro_analysis_by_name', {
					params: {
						query: {
							filename: reportName,
							precision: precision
						}
					}
				}),
				client.GET('/api/etoro_evolution_by_name', {
					params: {
						query: {
							filename: reportName,
							precision: precision
						}
					}
				})
			]);

			// Handle trades analysis task
			if (tradesTaskRes.error) {
				tradesError = (tradesTaskRes.error as components['schemas']['NotFoundResponse']).message;
			} else {
				tradesTaskId = tradesTaskRes.data!.task_id;
				pollTaskStatus(
					tradesTaskId,
					(progress) => {
						tradesProgress = progress;
					},
					(result) => {
						trades_data = result as EtoroData;
						tradesComplete = true;
					},
					(error) => {
						tradesError = error;
					}
				);
			}

			// Handle evolution analysis task
			if (evolutionTaskRes.error) {
				evolutionError = (evolutionTaskRes.error as components['schemas']['NotFoundResponse'])
					.message;
			} else {
				evolutionTaskId = evolutionTaskRes.data!.task_id;
				pollTaskStatus(
					evolutionTaskId,
					(progress) => {
						evolutionProgress = progress;
					},
					(result) => {
						evolution_data = result as EtoroEvolutionData;
						evolutionComplete = true;
					},
					(error) => {
						evolutionError = error;
					}
				);
			}
		} catch (err) {
			error = `Failed to start analysis: ${err}`;
		}
	}

	// React to changes in sheet_name or precision_index
	$effect(() => {
		const sheetName = $page.params.sheet_name;
		const currentPrecision = precision_values[precision_index][1];
		if (sheetName) {
			startAnalyses(sheetName, currentPrecision);
		}
	});
</script>

<div class="space-y-8 p-8">
	{#if error}
		<div class="text-center text-red-500">{error}</div>
	{/if}

	<!-- Analysis Progress and Results Grid -->
	<div class="grid grid-cols-1 gap-8 lg:grid-cols-2">
		<!-- Trades Analysis Box -->
		<div class="space-y-4">
			<ProgressBar
				title="Trades Analysis"
				progress={tradesProgress}
				isComplete={tradesComplete}
				error={tradesError}
			/>

			{#if trades_data}
				<div
					class="rounded-lg border border-gray-300 bg-white p-6 shadow-md dark:border-gray-600 dark:bg-gray-800"
				>
					<BarChart
						dataset={new Map([
							['profit (USD)', new Array(...trades_data.profit_usd)],
							['closed trades', new Array(...trades_data.closed_trades)]
						])}
						dates={trades_data.close_date}
					/>
				<div class="flex flex-col items-center">
					<label for="precision-range" class="mb-2 block text-white"
						>{precision_values[precision_index][0]}</label
					>
					<input
						type="range"
						id="precision-range"
						min="0"
						max={precision_values.length - 1}
						step="1"
						bind:value={precision_index}
						class="h-2 w-64 cursor-pointer appearance-none rounded-lg bg-gray-700 dark:bg-gray-700"
					/>
				</div>
				</div>
			{/if}
		</div>

		<!-- Evolution Analysis Box -->
		<div class="space-y-4">
			<ProgressBar
				title="Evolution Analysis"
				progress={evolutionProgress}
				isComplete={evolutionComplete}
				error={evolutionError}
			/>

			{#if evolution_data}
				<div
					class="rounded-lg border border-gray-300 bg-white p-6 shadow-md dark:border-gray-600 dark:bg-gray-800"
				>
					<HistoryChart
						color="green"
						title="Total profits evolution overtime"
						showTickerSelector={true}
						defaultShown={['total', 'Closed Positions']}
						dataset={evolution_data['evolution']['parts']}
						dates={evolution_data['evolution']['dates']}
					/>
				</div>
			{/if}
		</div>
	</div>
</div>
