export function roundPrecision(value: number, precision: number) {
	let factor = Math.pow(10, precision);
	return Math.round(value * factor) / factor;
}
export function formatPercent(ratio: number | null) {
	if (!ratio) return '';
	return `${roundPrecision(ratio * 100, 2)}%`;
}
export function formatCurrency(dollars: number | null) {
	if (!dollars) return undefined;
	return `${dollars}$`;
}

export function formatLargeNumber(num: number | null) {
	if (num === null) return '';
	if (num >= 1_000_000_000_000) {
		return `${roundPrecision(num / 1_000_000_000_000, 2)}T`;
	} else if (num >= 1_000_000_000) {
		return `${roundPrecision(num / 1_000_000_000, 2)}B`;
	} else if (num >= 1_000_000) {
		return `${roundPrecision(num / 1_000_000, 2)}M`;
	} else if (num >= 1_000) {
		return `${roundPrecision(num / 1_000, 2)}K`;
	} else {
		return num.toString();
	}
}

export const ratioColor = (ratio: number | null | undefined) => {
	if (!ratio) {
		return 'gray';
	}
	if (ratio > 0) {
		return 'green';
	} else if (ratio < 0) {
		return 'red';
	} else {
		return 'gray';
	}
};
