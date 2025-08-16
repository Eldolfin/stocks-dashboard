from collections.abc import Callable
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf
import yfinance_cache as yfc

from src import models
from src.services.task_manager import TaskProgress


def column_date_to_timestamp(column: pd.Series) -> pd.Series:
    return pd.to_datetime(column, format="%d/%m/%Y %H:%M:%S")


def _map_etoro_ticker_to_yahoo(details: str, is_crypto: bool = False) -> tuple[str | None, float]:
    """Map eToro ticker details to Yahoo Finance ticker symbol.

    Returns:
        tuple: (yahoo_ticker, scale_factor) or (None, 1) if unsupported
    """
    [ticker, market] = details.split("/")
    ticker = ticker.removesuffix(".US").removesuffix(".EXT")
    scale = 1

    if is_crypto:
        return f"{ticker}-{market}", scale
    if ticker == "BRK.B":
        return (
            "BRK-B",
            scale,
        )
    if ticker == "NSDQ100":
        return (
            "^NDX",
            scale,
        )
    if ticker == "SPX500":
        return (
            "^SPX",
            scale,
        )
    # MHFI (McGraw Hill Financial) changed its ticker to SPGI (S&P Global Inc.) after a corporate rebranding.
    if ticker == "MHFI":
        return (
            "SPGI",
            scale,
        )
    if market != "USD":
        if market == "GBX":
            scale = yfc.Ticker("GBPUSD=X").fast_info["lastPrice"] / 100
            match ticker:
                case "BT.l":
                    ticker = "BT-A.L"
        elif market == "EUR":
            scale = yfc.Ticker("EURUSD=X").fast_info["lastPrice"]
            match ticker:
                case "ACA" | "BNP" | "ENGI":
                    ticker += ".PA"
                case "NN.NV" | "ASRNL.NV":
                    ticker = ticker[:-3] + ".AS"
                case "STLAM.MI":
                    ticker = "STLAM.MI"
                case "BKT":
                    ticker = "BKT.MC"
                case "SAN.MC":
                    ticker = "SAN.MC"
                case "PAH3.DE":
                    ticker = "PAH3.DE"
                case "REP.MC":
                    ticker = "REP.MC"
                case "DG":
                    ticker = "DG.PA"  # Vinci SA
                case "AIR":
                    ticker = "AIR.PA"  # Airbus
                case "AMUN.PA":
                    ticker = "AMUN.PA"
                case "AZM":
                    ticker = "AZM.MI"  # Azimut
                case "EDP.LSB":
                    ticker = "EDP.LS"
                case "DTE.de":
                    ticker = "DTE.DE"
                case "RWE.de":
                    ticker = "RWE.DE"
                case "AC":
                    ticker = "AC.PA"  # Accor
                case "SIE.de":
                    ticker = "SIE.DE"
                case "AKZA.NV":
                    ticker = "AKZA.AS"
                case "ABI.BR":
                    ticker = "ABI.BR"
                case "VNA.DE":
                    ticker = "VNA.DE"
                case "CLNX.MC":
                    ticker = "CLNX.MC"
                case "CA":
                    ticker = "CA.PA"  # Carrefour
                case "GFC.PA":
                    ticker = "GFC.PA"
                case "ENEL":
                    ticker = "ENEL.MI"
                case "SU":
                    ticker = "SU.PA"  # Schneider Electric
                case "ORA":
                    ticker = "ORA.PA"
                case "WCH.DE":
                    ticker = "WCH.DE"
                case "AKE.PA":
                    ticker = "AKE.PA"
                case "MRL.MC":
                    ticker = "MRL.MC"
                case "TEP.PA":
                    ticker = "TEP.PA"
                case "FGR.PA":
                    ticker = "FGR.PA"
                case "SAN.PA":
                    ticker = "SAN.PA"
                case "ES.PA":
                    ticker = "ES.PA"
                case "INGA.NV":
                    ticker = "INGA.AS"
                case "DAN.MI":
                    ticker = "DAN.MI"
                case "AALB.NV":
                    ticker = "AALB.AS"
                case "ELIS.PA":
                    ticker = "ELIS.PA"
                case "RF.PA":
                    ticker = "RF.PA"
                case "NEXI.MI":
                    ticker = "NEXI.MI"
                case "SW.PA":
                    ticker = "SW.PA"
                case "ISP":
                    ticker = "ISP.MI"
                case _:
                    return (
                        None,
                        scale,
                    )
        elif market == "HKD":
            scale = yfc.Ticker("HKDUSD=X").fast_info["lastPrice"]
            ticker = ticker[-7:]  # remove eToro's prefix
        elif market == "SEK":
            scale = yfc.Ticker("SEKUSD=X").fast_info["lastPrice"]
            match ticker:
                case "NDA_SE.ST":
                    ticker = "0N4T.IL"  # Nordea Bank via LSE
                case "EVO.ST":
                    ticker = "EVO.ST"
                case _:
                    return (
                        None,
                        scale,
                    )
        elif market == "CHF":
            scale = yfc.Ticker("CHFUSD=X").fast_info["lastPrice"]
            match ticker:
                case "BAER":
                    ticker = "BAER.SW"
                case "CLN.ZU":
                    ticker = "CLN.SW"
                case "USD":
                    ticker = "CHFUSD=X"
                    scale = 1
                case _:
                    return (
                        None,
                        scale,
                    )
        elif market == "AUD":
            scale = yfc.Ticker("AUDUSD=X").fast_info["lastPrice"]
            match ticker:
                case "CLW.ASX":
                    ticker = "CLW.AX"
                case "PLS.ASX":
                    ticker = "PLS.AX"
                case _:
                    return (
                        None,
                        scale,
                    )
        elif market == "NOK":
            scale = yfc.Ticker("NOKUSD=X").fast_info["lastPrice"]
            match ticker:
                case "NAS":
                    ticker = "NAS.OL"
                case "HAUTO.OL":
                    ticker = "HAUTO.OL"
                case "WAWI.OL":
                    ticker = "WAWI.OL"
                case _:
                    return (
                        None,
                        scale,
                    )
        elif market == "DKK":
            scale = yfc.Ticker("DKKUSD=X").fast_info["lastPrice"]
            match ticker:
                case "ISS":
                    ticker = "ISS.CO"
                case "DANSKE":
                    ticker = "DANSKE.CO"
                case _:
                    return (
                        None,
                        scale,
                    )
        elif market == "JPY":
            scale = yfc.Ticker("JPYUSD=X").fast_info["lastPrice"]
            # No JPY tickers in your list except CAD/USD placeholders
        elif market == "SGD":
            scale = yfc.Ticker("SGDUSD=X").fast_info["lastPrice"]
            if ticker == "USD":
                ticker = "SGDUSD=X"
        else:
            return (
                None,
                scale,
            )

    return (
        ticker,
        scale,
    )


def extract_closed_position(
    etoro_statement_file: Path, time_unit: str, progress_callback: Callable[[str, int, int], None]
) -> dict[str, list[str]]:
    """Extract closed positions with optional progress reporting."""
    total_steps = 4

    progress_callback("Reading Excel file", 1, total_steps)

    excel = pd.read_excel(etoro_statement_file, sheet_name=None)
    closed_positions_df = excel["Closed Positions"]

    progress_callback("Processing dates", 2, total_steps)

    closed_positions_df["Close Date"] = column_date_to_timestamp(
        closed_positions_df["Close Date"],
    )
    closed_positions_df["Open Date"] = column_date_to_timestamp(
        closed_positions_df["Open Date"],
    )

    progress_callback("Calculating gains", 3, total_steps)

    gains_graphs_columns = {
        "Close Date": "close_date",
        "Profit(USD)": "profit_usd",
    }
    gains = closed_positions_df[gains_graphs_columns.keys()].reset_index()
    gains = gains.rename(columns=gains_graphs_columns)
    gains = (
        gains.groupby(gains["close_date"].dt.to_period(time_unit))
        .agg(
            profit_usd=("profit_usd", "sum"),
            closed_trades=("profit_usd", "count"),
        )
        .reset_index()
    )
    gains["close_date"] = gains["close_date"].dt.to_timestamp()
    gains["close_date"] = gains["close_date"].dt.strftime("%Y-%m-%dT%H:%M:%S")

    progress_callback("Finalizing results", 4, total_steps)

    return {column: gains[column].tolist() for column in gains.columns}


def extract_portfolio_evolution(
    etoro_statement_file: Path, progress_callback: Callable[[TaskProgress], None]
) -> models.EtoroEvolutionInner:
    """Extract portfolio evolution with optional progress reporting."""
    total_steps = 6

    progress_callback(TaskProgress("Reading Excel file", 1, total_steps))

    excel = pd.read_excel(etoro_statement_file, sheet_name=None)

    progress_callback(TaskProgress("Processing closed positions", 2, total_steps))

    closed = excel["Closed Positions"]
    closed["Close Date"] = column_date_to_timestamp(closed["Close Date"])
    closed = closed.sort_values(by="Close Date")
    closed = closed.set_index(closed["Close Date"])
    closed["Profit(USD)"] = closed["Profit(USD)"].astype(np.float32)
    closed = closed.resample("D").agg({"Profit(USD)": "sum"}).fillna(0)
    closed["Cumulative Profit"] = closed["Profit(USD)"].cumsum()

    progress_callback(TaskProgress("Processing open positions", 3, total_steps))

    activity = excel["Account Activity"]
    activity["Date"] = column_date_to_timestamp(activity["Date"])
    activity = activity.set_index("Date")

    # Extract and process stock splits
    splits = activity[activity["Type"] == "corp action: Split"].copy()
    if not splits.empty:
        splits = splits.groupby(["Date", "Details"]).last()
        # Extract split factor from Details column (format like "Split 10:1" or "NVDA/USD Split 10:1")
        details_series = splits.index.get_level_values("Details")
        split_factors = []
        for detail in details_series:
            parts = detail.split(" ")
            if "Split" in parts:
                split_idx = parts.index("Split")
                if split_idx + 1 < len(parts):
                    split_ratio = parts[split_idx + 1]  # '10:1'
                    split_factor = float(split_ratio.split(":")[0])
                    split_factors.append(split_factor)
                else:
                    split_factors.append(1.0)
            else:
                # Fallback: try original parsing for "Split 10:1" format
                try:
                    split_factor = float(parts[1].split(":")[0]) if len(parts) > 1 else 1.0
                    split_factors.append(split_factor)
                except (ValueError, IndexError):
                    split_factors.append(1.0)

        splits["Factor"] = split_factors
        splits = splits.reset_index().set_index("Date")
    else:
        splits = pd.DataFrame(columns=["Details", "Factor"]).set_index(pd.DatetimeIndex([], name="Date"))

    activity[activity["Type"] == "Open Position"]
    closed_positions = activity[activity["Type"] == "Position closed"]
    closed_positions["Position ID"].dropna().astype(str)
    still_open = activity[activity["Type"].isin(["Open Position", "Position closed"])].copy()
    still_open["Units / Contracts"] = still_open["Units / Contracts"].astype(np.float32)
    still_open.loc[still_open["Type"] == "Position closed", "Units / Contracts"] = (
        still_open.loc[still_open["Type"] == "Position closed", "Units / Contracts"] * -1
    )

    shares_per_ticker = {}
    for tick in still_open["Details"].unique():
        _ticker_positions = still_open[still_open["Details"] == tick].copy()
        _ticker_positions = _ticker_positions.sort_values(by="Date")
        _ticker_positions["Units / Contracts"] = _ticker_positions["Units / Contracts"].astype(np.float32)
        _ticker_positions = _ticker_positions.resample("D").agg({"Units / Contracts": "sum"}).fillna(0)

        # Create date range for the ticker
        date_range = pd.date_range(_ticker_positions.index.min(), pd.Timestamp.today())
        _ticker_positions = _ticker_positions.reindex(date_range, fill_value=0)

        # Apply split adjustments for this ticker
        if not splits.empty:
            ticker_splits = splits[splits["Details"].str.startswith(tick)].copy()
            if not ticker_splits.empty:
                # Create daily split factor series, starting with 1.0
                split_factors_df = pd.Series(1.0, index=date_range, name="split_factor")

                # Process splits in reverse chronological order to build cumulative factors
                ticker_splits = ticker_splits.sort_index(ascending=False)

                for split_date, split_row in ticker_splits.iterrows():
                    split_factor = split_row["Factor"]
                    # For dates before this split, multiply by the split factor to get equivalent post-split shares
                    mask = split_factors_df.index < split_date
                    split_factors_df.loc[mask] = split_factors_df.loc[mask] * split_factor

                # Apply split adjustments to shares
                _ticker_positions["split_factor"] = split_factors_df
                _ticker_positions["Units / Contracts"] = (
                    _ticker_positions["Units / Contracts"] * _ticker_positions["split_factor"]
                )

        # Calculate cumulative shares
        _ticker_positions["shares_sum"] = _ticker_positions["Units / Contracts"].cumsum()

        shares_per_ticker[tick] = _ticker_positions

    progress_callback(TaskProgress("Fetching market data", 4, total_steps))

    # Pre-process all tickers to get Yahoo Finance symbols and metadata
    tickers_to_fetch = still_open["Details"].unique()
    ticker_metadata = {}
    yahoo_symbols = []
    crypto_symbols = []

    for _details in tickers_to_fetch:
        first_open_date = still_open[still_open["Details"] == _details].index.min()
        is_crypto = still_open.loc[still_open["Details"] == _details, "Asset type"].iloc[0] == "Crypto"

        yahoo_ticker, scale = _map_etoro_ticker_to_yahoo(_details, is_crypto=is_crypto)

        if yahoo_ticker is not None:
            ticker_metadata[_details] = {
                "yahoo_symbol": yahoo_ticker,
                "scale": scale,
                "is_crypto": is_crypto,
                "first_open_date": first_open_date,
            }
            if is_crypto:
                crypto_symbols.append(yahoo_ticker)
            else:
                yahoo_symbols.append(yahoo_ticker)

    # Find the earliest start date across all tickers
    if ticker_metadata:
        earliest_date = min(meta["first_open_date"] for meta in ticker_metadata.values())
        years_to_fetch = pd.Timestamp.now().year - earliest_date.year + 1
        period = f"{years_to_fetch}y"

        # Bulk fetch all non-crypto tickers at once using yf.Tickers()
        bulk_histories = {}
        if yahoo_symbols:
            try:
                # Use bulk fetch for non-crypto symbols with yfinance_cache
                bulk_data = yf.Tickers(yahoo_symbols).history(period=period)
                for symbol in yahoo_symbols:
                    try:
                        symbol = symbol.upper()
                        symbol_data = bulk_data.xs(symbol, level=1, axis=1)
                        bulk_histories[symbol] = symbol_data[["Close"]]
                    except KeyError:
                        # Symbol not found in bulk data
                        print(f"Could not find {symbol} in bulk_data. Skipping.")
                        continue
            except Exception as e:
                print(f"Bulk fetch failed, falling back to individual fetches: {e}")

        # Fetch crypto symbols individually (they need different handling)
        for symbol in crypto_symbols:
            try:
                ticker_data = yf.Ticker(symbol)
                history = ticker_data.history(period=period)
                if not history.empty:
                    bulk_histories[symbol] = history[["Close"]]
            except Exception as e:
                print(f"Could not fetch crypto data for {symbol}: {e}")

        # Process the bulk data to create yahoo_data with original eToro details as keys
        yahoo_data = {}
        for _details, metadata in ticker_metadata.items():
            yahoo_symbol = metadata["yahoo_symbol"].upper()
            scale = metadata["scale"]
            first_open_date = metadata["first_open_date"]

            if yahoo_symbol in bulk_histories:
                history = bulk_histories[yahoo_symbol].copy()
                # Filter to only include data from the ticker's first open date
                # Ensure both dates are timezone-naive for proper comparison
                history_index_naive = pd.to_datetime(history.index).tz_localize(None)
                first_open_date_naive = (
                    pd.to_datetime(first_open_date).tz_localize(None) if first_open_date.tz else first_open_date
                )
                history = history[history_index_naive >= first_open_date_naive]
                if not history.empty:
                    # Apply scaling
                    history.loc[:, "Close"] = history.loc[:, "Close"] * scale
                    yahoo_data[_details] = history
                else:
                    print(f"No data found for {yahoo_symbol} after filtering")
            else:
                print(f"No data found for {yahoo_symbol}")
    else:
        yahoo_data = {}

    progress_callback(TaskProgress("Combining portfolio data", 5, total_steps))

    all_combined_data = {}
    for _ticker_name, _ticker in shares_per_ticker.items():
        if _ticker_name in yahoo_data:
            _yahoo_data = yahoo_data[_ticker_name]
            _ticker.index = pd.to_datetime(_ticker.index).tz_localize(None)
            _yahoo_data.index = pd.to_datetime(_yahoo_data.index).tz_localize(None)
            combined = _ticker.join(_yahoo_data, how="left")
            combined["net_value"] = combined["Close"] * combined["shares_sum"]
            all_combined_data[_ticker_name] = combined

    all_combined_data_filled = {}
    for _stock, _df in all_combined_data.items():
        all_combined_data_filled[_stock] = _df.ffill()

    progress_callback(TaskProgress("Finalizing evolution", 6, total_steps))

    _all_data = pd.DataFrame()
    all_profits = dict(all_combined_data_filled)
    all_profits["Closed Positions"] = closed.rename(columns={"Cumulative Profit": "net_value"})
    for _stock, _df in all_profits.items():
        _all_data = _all_data.join(
            _df[["net_value"]].rename(columns={"net_value": _stock}),
            how="outer",
        )
    daily_deposits = activity[activity["Type"] == "Deposit"]["Amount"].astype(np.float32).resample("D").sum().fillna(0)
    cumulative_deposits = daily_deposits.cumsum()
    start_date = daily_deposits.index.min()
    end_date = pd.Timestamp.today()
    date_range = pd.date_range(start=start_date, end=end_date, freq="D")
    cumulative_deposits = cumulative_deposits.reindex(date_range).ffill()

    _all_data = _all_data.ffill().fillna(0)
    _all_data["total"] = _all_data.loc[:, ~_all_data.columns.str.contains("Closed Positions")].sum(axis=1)
    _all_data = _all_data.join(cumulative_deposits, how="outer")
    _all_data.index = pd.to_datetime(_all_data.index).strftime("%Y-%m-%d")
    _all_data = _all_data.rename(columns={"Amount": "Deposits", "total": "Total"})

    _all_data["P&L"] = _all_data["Total"] - _all_data["Deposits"]
    _all_data = _all_data.fillna(0)

    parts = {
        str(k): [float(x) for x in v]
        for k, v in _all_data.reset_index().drop(columns=["index"]).to_dict("list").items()
    }
    return models.EtoroEvolutionInner(
        dates=_all_data.index.astype(str).to_list(),
        parts=parts,
    )
