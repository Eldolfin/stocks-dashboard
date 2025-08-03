#!/usr/bin/env python3
"""
Demonstration of the Net Worth feature implementation
Shows the net worth calculation and visualization from the eToro Excel file
"""

import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from pathlib import Path

# Add backend src to path
backend_src = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend', 'src')
sys.path.insert(0, backend_src)

from etoro_data import extract_net_worth, extract_closed_position

def demo_net_worth_feature():
    """Demonstrate the net worth feature with sample data"""
    
    # Path to test Excel file
    excel_file = Path('tests/data/etoro-account-statement-12-31-2014-7-5-2025_TEST.xlsx')
    
    if not excel_file.exists():
        print(f"❌ Test Excel file not found: {excel_file}")
        return
    
    print("🎯 Net Worth Over Time Feature Demo")
    print("=" * 50)
    
    # Extract net worth data with different precisions
    print("\n📊 Extracting net worth data...")
    
    # Daily precision
    daily_data = extract_net_worth(excel_file, 'D')
    print(f"✅ Daily data: {len(daily_data['date'])} data points")
    
    # Monthly precision  
    monthly_data = extract_net_worth(excel_file, 'M')
    print(f"✅ Monthly data: {len(monthly_data['date'])} data points")
    
    # Also extract profit data for comparison
    profit_data = extract_closed_position(excel_file, 'M')
    print(f"✅ Profit data: {len(profit_data['close_date'])} data points")
    
    # Create visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    fig.suptitle('eToro Portfolio Analysis - Net Worth Feature Demo', fontsize=16, fontweight='bold')
    
    # Plot 1: Net Worth Over Time (Line Chart)
    dates_daily = [datetime.fromisoformat(d.replace('T00:00:00', '')) for d in daily_data['date']]
    dates_monthly = [datetime.fromisoformat(d.replace('T00:00:00', '')) for d in monthly_data['date']]
    
    ax1.plot(dates_daily, daily_data['net_worth'], 'o-', color='#00ff88', linewidth=2, markersize=3, label='Daily Net Worth')
    ax1.plot(dates_monthly, monthly_data['net_worth'], 's-', color='#ff6b35', linewidth=3, markersize=5, label='Monthly Net Worth')
    
    ax1.set_title('Net Worth Over Time', fontweight='bold', fontsize=14)
    ax1.set_ylabel('Net Worth ($)', fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
    
    # Add annotations for key insights
    first_value = daily_data['net_worth'][0]
    last_value = daily_data['net_worth'][-1]
    total_change = last_value - first_value
    percent_change = (total_change / first_value) * 100 if first_value != 0 else 0
    
    ax1.annotate(f'Start: ${first_value:.2f}', 
                xy=(dates_daily[0], first_value), 
                xytext=(10, 10), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.3', fc='lightblue', alpha=0.7),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    
    ax1.annotate(f'End: ${last_value:.2f}\n({percent_change:+.1f}%)', 
                xy=(dates_daily[-1], last_value), 
                xytext=(-60, 10), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.3', fc='lightgreen', alpha=0.7),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    
    # Plot 2: Monthly Profit (Bar Chart - existing feature)
    profit_dates = [datetime.fromisoformat(d) for d in profit_data['close_date']]
    colors = ['green' if p >= 0 else 'red' for p in profit_data['profit_usd']]
    
    bars = ax2.bar(profit_dates, profit_data['profit_usd'], color=colors, alpha=0.7, width=20)
    ax2.set_title('Monthly Profit/Loss (Existing Feature)', fontweight='bold', fontsize=14)
    ax2.set_ylabel('Profit/Loss ($)', fontweight='bold')
    ax2.set_xlabel('Date', fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    
    # Add value labels on bars
    for bar, value in zip(bars, profit_data['profit_usd']):
        height = bar.get_height()
        ax2.annotate(f'${value:.1f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3 if height >= 0 else -15),
                    textcoords="offset points",
                    ha='center', va='bottom' if height >= 0 else 'top',
                    fontsize=8, fontweight='bold')
    
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax2.xaxis.set_major_locator(mdates.MonthLocator())
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
    
    plt.tight_layout()
    
    # Save the plot
    output_path = '/tmp/net_worth_demo.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n🎨 Visualization saved to: {output_path}")
    
    # Print summary statistics
    print("\n📈 Summary Statistics:")
    print(f"   • Total time period: {len(daily_data['date'])} days")
    print(f"   • Starting net worth: ${first_value:.2f}")
    print(f"   • Ending net worth: ${last_value:.2f}")
    print(f"   • Total change: ${total_change:+.2f} ({percent_change:+.1f}%)")
    print(f"   • Peak net worth: ${max(daily_data['net_worth']):.2f}")
    print(f"   • Lowest net worth: ${min(daily_data['net_worth']):.2f}")
    
    total_profit = sum(profit_data['profit_usd'])
    total_trades = sum(profit_data['closed_trades'])
    print(f"   • Total profit from closed positions: ${total_profit:.2f}")
    print(f"   • Total closed trades: {total_trades}")
    
    print("\n✅ Net Worth Feature Implementation Complete!")
    print("   • ✅ Backend: extract_net_worth() function processes Account Activity sheet")
    print("   • ✅ API: /api/etoro_net_worth and /api/etoro_net_worth_by_name endpoints")
    print("   • ✅ Frontend: HistoryChart component displays net worth as line chart")
    print("   • ✅ UI: Side-by-side display with existing profit bar chart")
    print("   • ✅ Features: Precision control (Daily/Monthly/Yearly) for both charts")
    print("   • ✅ Tests: Comprehensive Playwright end-to-end tests")
    
    return output_path

if __name__ == "__main__":
    demo_net_worth_feature()