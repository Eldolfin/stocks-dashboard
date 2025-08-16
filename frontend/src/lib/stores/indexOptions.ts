import { writable } from 'svelte/store';

export interface IndexOption {
	label: string;
	value: string;
}

export const indexOptions = writable<IndexOption[]>([]);

export async function loadIndexOptions() {
	const res = await fetch('/api/static/top_indexes.csv');
	if (!res.ok) return;
	const text = await res.text();
	const lines = text.split('\n').filter(Boolean);
	const options = lines.slice(1).map((line) => {
		const [symbol, name] = line.split(',');
		return { label: `${name} (${symbol})`, value: symbol };
	});
	indexOptions.set(options);
}
