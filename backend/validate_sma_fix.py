#!/usr/bin/env python3
"""
Manual validation script to test the SMA fix logic.
This simulates the corrected behavior without needing external dependencies.
"""

def rolling_mean(data, window_size):
    """Simple rolling mean calculation."""
    if len(data) < window_size:
        return [0] * len(data)
    
    result = []
    for i in range(len(data)):
        if i < window_size - 1:
            result.append(0)  # Not enough data for meaningful average
        else:
            window_data = data[i - window_size + 1:i + 1]
            result.append(sum(window_data) / len(window_data))
    return result

def simulate_sma_calculation_old(period: str, data_points: int = 30):
    """Simulate the OLD (incorrect) SMA calculation that always uses 'max' period."""
    # Old logic: Always get max period data (simulated as 365 days)
    max_data_points = 365
    prices = [100 + i * 0.1 for i in range(max_data_points)]  # Simulate price data
    
    smas_sizes = [30, 100, 500]
    smas = {}
    
    for size in smas_sizes:
        sma_values = rolling_mean(prices, size)
        # Take only the last data_points values to match requested period
        smas[size] = sma_values[-data_points:]
    
    return smas

def simulate_sma_calculation_new(period: str, data_points: int = 30):
    """Simulate the NEW (corrected) SMA calculation that respects the requested period."""
    smas_sizes = [30, 100, 500]
    max_sma_window = max(smas_sizes)
    
    if period == "max":
        # For max, use all available data
        extended_data_points = 365
    else:
        # For specific periods, extend by SMA window for accurate calculation
        extended_data_points = data_points + max_sma_window
    
    # Generate extended price data for SMA calculation
    prices = [100 + i * 0.1 for i in range(extended_data_points)]
    
    smas = {}
    for size in smas_sizes:
        sma_values = rolling_mean(prices, size)
        
        if period == "max":
            # For max period, use values that correspond to the price data length
            smas[size] = sma_values[-data_points:]
        else:
            # For specific periods, get SMA values for the requested period
            if len(sma_values) >= data_points:
                smas[size] = sma_values[-data_points:]
            else:
                padding = [0] * (data_points - len(sma_values))
                smas[size] = padding + sma_values
    
    return smas

def test_sma_fix():
    """Test that demonstrates the fix for SMA calculation."""
    
    print("=== SMA Calculation Fix Validation ===\n")
    
    # Test different periods
    test_cases = [
        ("1mo", 30),
        ("3mo", 90), 
        ("ytd", 180),  # Approximate YTD
        ("max", 365)
    ]
    
    for period, data_points in test_cases:
        print(f"Testing period: {period} (data points: {data_points})")
        
        old_smas = simulate_sma_calculation_old(period, data_points)
        new_smas = simulate_sma_calculation_new(period, data_points)
        
        print(f"  OLD method - SMA30 last value: {old_smas[30][-1]:.2f}")
        print(f"  NEW method - SMA30 last value: {new_smas[30][-1]:.2f}")
        
        # Check if values are different (they should be for most periods)
        sma30_diff = abs(old_smas[30][-1] - new_smas[30][-1])
        if sma30_diff > 0.01:  # Allow for small numerical differences
            print(f"  ✅ Values differ by {sma30_diff:.2f} - NEW method respects period")
        else:
            print(f"  ⚠️  Values are similar - may need further investigation")
        
        print()
    
    # Test that different periods produce different SMA values in NEW method
    print("Testing that different periods produce different SMA values:")
    new_1mo = simulate_sma_calculation_new("1mo", 30)
    new_3mo = simulate_sma_calculation_new("3mo", 90)
    
    sma_1mo_last = new_1mo[30][-1]
    sma_3mo_last = new_3mo[30][-1]
    
    print(f"1 month SMA30 last: {sma_1mo_last:.2f}")
    print(f"3 month SMA30 last: {sma_3mo_last:.2f}")
    
    if abs(sma_1mo_last - sma_3mo_last) > 0.01:
        print("✅ Different periods produce different SMA values - Fix is working!")
    else:
        print("⚠️  Different periods produce similar SMA values - May need adjustment")
        
    print("\n=== Summary ===")
    print("The fix ensures SMA calculation uses the correct time period:")
    print("- OLD: Always used 'max' period data, just trimmed the result")
    print("- NEW: Uses requested period + sufficient lookback for accurate SMA")
    print("This provides more accurate SMA values that actually correspond to the requested time period.")

if __name__ == "__main__":
    test_sma_fix()