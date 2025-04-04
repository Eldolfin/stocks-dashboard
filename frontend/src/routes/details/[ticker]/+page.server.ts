import { client } from "$lib/typed-fetch-client";
import { error } from "@sveltejs/kit";

export async function load(
  { params, url }: {
    params: {
      ticker: string;
    };
    url: URL;
  },
) {
  const period = url.searchParams.get("period") || "ytd";
  const kpis_res = await client.GET("/api/kpis/", {
    params: {
      query: {
        ticker_name: params.ticker,
      },
    },
  });
  if (!kpis_res.response.ok) {
    error(kpis_res.response.status, kpis_res.response.statusText);
  }

  const history_res = await client.GET("/api/ticker/", {
    params: {
      query: {
        period,
        ticker_name: params.ticker,
      },
    },
  });
  if (!history_res.response.ok) {
    error(history_res.response.status, history_res.response.statusText);
  }

  return {
    ticker: params.ticker,
    summary: kpis_res.data,
    history: history_res.data,
  };
}
