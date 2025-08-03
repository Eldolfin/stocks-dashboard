import colorLib, { Color, type RGBA } from '@kurkle/color';
import 'chartjs-adapter-luxon';

// Adapted from http://indiegamr.com/generate-repeatable-random-numbers-in-js/
var _seed = Date.now();

function valueOrDefault(value: any, def: any) {
	return value || def;
}

export function srand(seed: number) {
	_seed = seed;
}

export function rand(min: number = 0, max: number = 0) {
	_seed = (_seed * 9301 + 49297) % 233280;
	return min! + (_seed / 233280) * (max! - min!);
}

export function numbers(config: {
	min: number | undefined;
	max: number | undefined;
	from: number | undefined;
	count: number | undefined;
	decimals: number | undefined;
	continuity: number | undefined;
}) {
	var cfg = config || {};
	var min = valueOrDefault(cfg.min, 0);
	var max = valueOrDefault(cfg.max, 100);
	var from = valueOrDefault(cfg.from, []);
	var count = valueOrDefault(cfg.count, 8);
	var decimals = valueOrDefault(cfg.decimals, 8);
	var continuity = valueOrDefault(cfg.continuity, 1);
	var dfactor = Math.pow(10, decimals) || 0;
	var data = [];
	var i, value;

	for (i = 0; i < count; ++i) {
		value = (from[i] || 0) + rand(min, max);
		if (rand() <= continuity) {
			data.push(Math.round(dfactor * value) / dfactor);
		} else {
			data.push(null);
		}
	}

	return data;
}

export const MONTHS = [
	'January',
	'February',
	'March',
	'April',
	'May',
	'June',
	'July',
	'August',
	'September',
	'October',
	'November',
	'December'
];

export function transparentize(
	value: string | number[] | Color | RGBA,
	opacity: number | undefined
) {
	var alpha = opacity === undefined ? 0.5 : 1 - opacity;
	return colorLib(value).alpha(alpha).rgbString();
}

export const CHART_COLORS = {
	red: 'rgb(255, 99, 132)',
	orange: 'rgb(255, 159, 64)',
	yellow: 'rgb(255, 205, 86)',
	green: 'rgb(75, 192, 192)',
	blue: 'rgb(54, 162, 235)',
	purple: 'rgb(153, 102, 255)',
	grey: 'rgb(201, 203, 207)'
};

const NAMED_COLORS = [
	CHART_COLORS.red,
	CHART_COLORS.orange,
	CHART_COLORS.yellow,
	CHART_COLORS.green,
	CHART_COLORS.blue,
	CHART_COLORS.purple,
	CHART_COLORS.grey
];

export function namedColor(index: number) {
	return NAMED_COLORS[index % NAMED_COLORS.length];
}

export const SMA_COLORS = [
	CHART_COLORS.blue,
	CHART_COLORS.purple,
	CHART_COLORS.orange,
	CHART_COLORS.grey,
	CHART_COLORS.yellow
];
