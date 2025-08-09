import { client } from '$lib/typed-fetch-client';
import { error } from '@sveltejs/kit';

export async function load({
	params,
	url
}: {
	params: {
		tickers: string;
	};
	url: URL;
}) {
	const period = url.searchParams.get('period') || 'ytd';
	const tickerArray = params.tickers.split(',').map((t) => t.trim());
	const history_data = await client.GET('/api/compare_growth/', {
		params: {
			query: {
				ticker_names: tickerArray,
				period
			}
		}
	});
	if (!history_data.response.ok) {
		error(history_data.response.status, history_data.response.statusText);
	}

	return {
		tickers: params.tickers,
		history_data: history_data.data!
	};
}
