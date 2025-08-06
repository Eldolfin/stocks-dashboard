use chrono::Utc;
use serde::Serialize;
use std::error::Error;
use std::fs::{self, OpenOptions};
use std::path::Path;
use yahoo_finance_api::{self as yahoo, YSummaryData};

#[derive(Debug, Serialize)]
struct Snapshot {
    timestamp: String,
    ticker: String,
    price: f64,
    market_cap: u64,
    shares_outstanding: u64,
    float_shares: u64,
    trailing_pe: f64,
    forward_pe: f64,
    trailing_eps: f64,
    forward_eps: f64,
    dividend_yield: f64,
    ex_dividend_date: i64,
    target_mean_price: f64,
    recommendation_mean: f64,
    beta: f64,
    held_percent_insiders: f64,
    held_percent_institutions: f64,
}

fn collect_snapshot(ticker: &str) -> Result<Snapshot, Box<dyn Error>> {
    let mut provider = yahoo::YahooConnector::new()?;
    let quote = provider.get_ticker_info(ticker)?;
    let summary = &quote.quote_summary.unwrap().result.unwrap()[0];
    let YSummaryData {
        asset_profile: Some(_asset_profile),
        summary_detail: Some(summary_detail),
        default_key_statistics: Some(default_key_statistics),
        quote_type: Some(_quote_type),
        financial_data: Some(financial_data),
    } = summary
    else {
        panic!("There should always be the same amount of data here");
    };

    Ok(Snapshot {
        timestamp: Utc::now().to_rfc3339(),
        ticker: ticker.to_string(),
        price: financial_data.current_price.unwrap(),
        market_cap: summary_detail.market_cap.unwrap(),
        forward_pe: default_key_statistics.forward_pe.unwrap(),
        trailing_eps: default_key_statistics.trailing_eps.unwrap(),
        forward_eps: default_key_statistics.forward_eps.unwrap(),
        beta: default_key_statistics.beta.unwrap(),
        held_percent_insiders: default_key_statistics.held_percent_insiders.unwrap(),
        held_percent_institutions: default_key_statistics.held_percent_institutions.unwrap(),
        shares_outstanding: default_key_statistics.shares_outstanding.unwrap(),
        float_shares: default_key_statistics.float_shares.unwrap(),
        ex_dividend_date: summary_detail.ex_dividend_date.unwrap(),
        trailing_pe: summary_detail.trailing_pe.unwrap(),
        dividend_yield: summary_detail.dividend_yield.unwrap(),
        target_mean_price: financial_data.target_mean_price.unwrap(),
        recommendation_mean: financial_data.recommendation_mean.unwrap(),
    })
}

fn append_snapshots_to_csv(snapshots: &[Snapshot], file_path: &str) -> Result<(), Box<dyn Error>> {
    let file_exists = Path::new(file_path).exists();
    let file_is_empty = !file_exists || fs::metadata(file_path)?.len() == 0;

    let file = OpenOptions::new()
        .create(true)
        .append(true)
        .open(file_path)?;

    let mut writer = csv::WriterBuilder::new()
        .has_headers(file_is_empty)
        .from_writer(file);

    for snapshot in snapshots {
        writer.serialize(snapshot)?;
    }
    Ok(())
}

fn main() -> Result<(), Box<dyn Error>> {
    let tickers = vec!["AAPL", "MSFT", "GOOGL"];
    let file_path = "snapshots.csv";

    let snapshots: Vec<Snapshot> = tickers
        .iter()
        .filter_map(|&ticker| match collect_snapshot(ticker) {
            Ok(snapshot) => {
                println!("✅ Collected snapshot for {}", ticker);
                Some(snapshot)
            }
            Err(e) => {
                eprintln!("❌ Failed to collect {}: {}", ticker, e);
                None
            }
        })
        .collect();

    if !snapshots.is_empty() {
        append_snapshots_to_csv(&snapshots, file_path)?;
    }

    Ok(())
}
