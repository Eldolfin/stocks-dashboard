import { client } from '$lib/typed-fetch-client';
import { error } from '@sveltejs/kit';

export async function load({
	params,
	url
}: {
	params: {
		ticker: string;
	};
	url: URL;
}) {
	const period = url.searchParams.get('period') || 'ytd';
	const kpis_res = await client.GET('/api/kpis/', {
		params: {
			query: {
				ticker_name: params.ticker
			}
		}
	});
	if (!kpis_res.response.ok) {
		error(kpis_res.response.status, kpis_res.response.statusText);
	}

	const history_res = await client.GET('/api/ticker/', {
		params: {
			query: {
				period,
				ticker_name: params.ticker
			}
		}
	});
	if (!history_res.response.ok) {
		error(history_res.response.status, history_res.response.statusText);
	}

	let historical_kpis_res;
	try {
		historical_kpis_res = await client.GET('/api/historical-kpis/', {
			params: {
				query: {
					ticker_name: params.ticker
				}
			}
		});
		if (!historical_kpis_res.response.ok) {
			if (historical_kpis_res.response.status === 404) {
				historical_kpis_res = null; // No historical data found
			} else {
				error(historical_kpis_res.response.status, historical_kpis_res.response.statusText);
			}
		}
	} catch {
		historical_kpis_res = null; // Handle network errors or other exceptions
	}

	return {
		ticker: params.ticker,
		summary: kpis_res.data,
		history: history_res.data,
		historical_kpis: historical_kpis_res ? historical_kpis_res.data : null
	};
}
