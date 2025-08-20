#!/usr/bin/env python3
"""
Test script to demonstrate and validate the SMA calculation fix.
This test can be run independently to verify the SMA calculation behavior.
"""

import sys
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

# Add the backend src to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def mock_ticker_history(ticker_name: str, period: str, interval: str) -> pd.DataFrame:
    """Mock function to simulate ticker history data for testing."""
    
    # Generate test data for different periods
    if period == "max":
        # Generate 2 years of data for max period
        start_date = datetime.now() - timedelta(days=730)
        dates = pd.date_range(start_date, periods=730, freq='D')
    elif period == "1y":
        start_date = datetime.now() - timedelta(days=365)
        dates = pd.date_range(start_date, periods=365, freq='D')
    elif period == "3mo":
        start_date = datetime.now() - timedelta(days=90)
        dates = pd.date_range(start_date, periods=90, freq='D')
    elif period == "1mo":
        start_date = datetime.now() - timedelta(days=30)
        dates = pd.date_range(start_date, periods=30, freq='D')
    else:
        # Default to 100 days
        start_date = datetime.now() - timedelta(days=100)
        dates = pd.date_range(start_date, periods=100, freq='D')
    
    # Generate mock price data (simple upward trend with some volatility)
    base_price = 100
    price_data = [base_price + i * 0.1 + (i % 10) * 0.5 for i in range(len(dates))]
    
    return pd.DataFrame({
        'Date': dates,
        'Open': [p * 0.99 for p in price_data],
        'Close': price_data,
        'High': [p * 1.02 for p in price_data],
        'Low': [p * 0.98 for p in price_data],
        'Volume': [1000000] * len(dates)
    })

def mock_ticker_history_from_start(ticker_name: str, start: str, interval: str) -> pd.DataFrame:
    """Mock function to simulate ticker history from start date."""
    start_date = datetime.strptime(start, "%Y-%m-%d")
    days_since_start = (datetime.now() - start_date).days
    dates = pd.date_range(start_date, periods=days_since_start, freq='D')
    
    base_price = 100
    price_data = [base_price + i * 0.1 + (i % 10) * 0.5 for i in range(len(dates))]
    
    return pd.DataFrame({
        'Date': dates,
        'Open': [p * 0.99 for p in price_data],
        'Close': price_data,
        'High': [p * 1.02 for p in price_data],
        'Low': [p * 0.98 for p in price_data],
        'Volume': [1000000] * len(dates)
    })

def test_sma_calculation_issue():
    """Test to demonstrate the current SMA calculation issue."""
    
    with patch('src.database.stocks_repository.get_ticker_history', side_effect=mock_ticker_history), \
         patch('src.database.stocks_repository.get_ticker_history_from_start', side_effect=mock_ticker_history_from_start):
        
        from src.services import stocks_service
        from src import models
        
        # Test case 1: Request 1 month of data
        query_1mo = models.TickerQuery(ticker_name="AAPL", period="1mo", interval="1d")
        result_1mo = stocks_service.get_ticker(query_1mo)
        
        # Test case 2: Request 3 months of data  
        query_3mo = models.TickerQuery(ticker_name="AAPL", period="3mo", interval="1d")
        result_3mo = stocks_service.get_ticker(query_3mo)
        
        # Test case 3: Request max data
        query_max = models.TickerQuery(ticker_name="AAPL", period="max", interval="3mo")
        result_max = stocks_service.get_ticker(query_max)
        
        if result_1mo and result_3mo and result_max:
            print("=== SMA Calculation Test Results ===")
            print(f"1 month request - Data points: {len(result_1mo.candles)}, SMA30 points: {len(result_1mo.smas[30])}")
            print(f"3 month request - Data points: {len(result_3mo.candles)}, SMA30 points: {len(result_3mo.smas[30])}")
            print(f"Max request - Data points: {len(result_max.candles)}, SMA30 points: {len(result_max.smas[30])}")
            
            # Check if SMA values are different for different periods (they should be!)
            sma30_1mo_last = result_1mo.smas[30][-1] if result_1mo.smas[30] else None
            sma30_3mo_last = result_3mo.smas[30][-1] if result_3mo.smas[30] else None
            
            print(f"1 month SMA30 last value: {sma30_1mo_last}")
            print(f"3 month SMA30 last value: {sma30_3mo_last}")
            
            # The issue: these values might be the same because both are using "max" period for calculation
            if sma30_1mo_last and sma30_3mo_last and abs(sma30_1mo_last - sma30_3mo_last) < 0.01:
                print("❌ ISSUE CONFIRMED: SMA values are the same for different periods!")
                print("This indicates SMA is being calculated over the same dataset regardless of requested period.")
            else:
                print("✅ SMA values are different for different periods - this is expected behavior.")
                
            return True
        else:
            print("❌ Failed to get ticker data for testing")
            return False

if __name__ == "__main__":
    print("Testing SMA calculation behavior...")
    test_sma_calculation_issue()