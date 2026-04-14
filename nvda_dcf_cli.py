#!/usr/bin/env python3
"""
NVIDIA (NVDA) DCF Valuation Model - Standalone Script
Calculates fair value per share using Discounted Cash Flow analysis
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime

class NVDADCFModel:
    def __init__(self):
        self.ticker = "NVDA"
        self.projection_years = 5
        
        # DCF Assumptions
        self.revenue_growth_rates = [0.25, 0.22, 0.18, 0.15, 0.12]
        self.operating_margin_forecast = [0.42, 0.43, 0.44, 0.44, 0.43]
        self.tax_rate = 0.15
        self.capex_pct_revenue = 0.02
        self.nwc_change_pct = 0.01
        
        # WACC Components
        self.risk_free_rate = 0.04
        self.market_risk_premium = 0.055
        self.beta = 1.85
        self.cost_of_debt = 0.035
        self.terminal_growth_rate = 0.03
        
    def fetch_data(self):
        """Fetch NVDA financial data from Yahoo Finance"""
        print(f"Fetching {self.ticker} financial data...")
        self.nvda = yf.Ticker(self.ticker)
        
        self.income_stmt = self.nvda.income_stmt
        self.balance_sheet = self.nvda.balance_sheet
        self.cash_flow = self.nvda.cash_flow
        
        self.current_price = self.nvda.info.get('currentPrice', 0)
        self.shares_outstanding = self.nvda.info.get('sharesOutstanding', 0)
        
        print(f"✓ Data fetched successfully")
        print(f"  Current Price: ${self.current_price:.2f}")
        print(f"  Shares Outstanding: {self.shares_outstanding/1e9:.2f}B\n")
    
    def calculate_historical_metrics(self):
        """Calculate key historical metrics"""
        years = 5
        
        # Extract data
        revenue = self.income_stmt.loc['Total Revenue'].iloc[:years].sort_index(ascending=False).values
        operating_income = self.income_stmt.loc['Operating Income'].iloc[:years].sort_index(ascending=False).values
        operating_cash_flow = self.cash_flow.loc['Operating Cash Flow'].iloc[:years].sort_index(ascending=False).values
        capex = abs(self.cash_flow.loc['Capital Expenditures'].iloc[:years].sort_index(ascending=False).values)
        
        self.base_year_revenue = revenue[0]
        self.historical_revenue = revenue
        
        # Operating margins
        self.operating_margins = operating_income / revenue
        self.avg_operating_margin = np.mean(self.operating_margins)
        
        print("Historical Metrics (Last 5 Years):")
        print(f"  Average Revenue: ${revenue.mean()/1e9:.2f}B")
        print(f"  Average Operating Margin: {self.avg_operating_margin*100:.1f}%")
        print(f"  Base Year Revenue (FY2025): ${self.base_year_revenue/1e9:.2f}B\n")
    
    def project_cash_flows(self):
        """Project future free cash flows"""
        projection_df = pd.DataFrame(index=range(1, self.projection_years + 1))
        
        # Project revenue
        projected_revenue = [self.base_year_revenue]
        for i in range(self.projection_years):
            projected_revenue.append(projected_revenue[-1] * (1 + self.revenue_growth_rates[i]))
        
        projection_df['Revenue'] = projected_revenue[1:]
        projection_df['Operating Margin'] = self.operating_margin_forecast
        projection_df['Operating Income'] = projection_df['Revenue'] * projection_df['Operating Margin']
        projection_df['NOPAT'] = projection_df['Operating Income'] * (1 - self.tax_rate)
        
        # Calculate Free Cash Flow
        projection_df['CapEx'] = projection_df['Revenue'] * self.capex_pct_revenue
        projection_df['Change in Revenue'] = projection_df['Revenue'].diff().fillna(0)
        projection_df['Change in NWC'] = projection_df['Change in Revenue'] * self.nwc_change_pct
        projection_df['Free Cash Flow'] = projection_df['NOPAT'] - projection_df['CapEx'] - projection_df['Change in NWC']
        
        self.projection_df = projection_df
        self.projected_fcf = projection_df['Free Cash Flow'].values
        
        print("Projected Free Cash Flows (5 Years):")
        print(projection_df[['Revenue', 'Operating Income', 'Free Cash Flow']].to_string())
        print()
    
    def calculate_wacc(self):
        """Calculate Weighted Average Cost of Capital"""
        # Cost of Equity
        self.cost_of_equity = self.risk_free_rate + self.beta * self.market_risk_premium
        
        # Simple WACC (assuming minimal debt for NVDA)
        equity_weight = 0.95
        debt_weight = 0.05
        
        self.wacc = (equity_weight * self.cost_of_equity) + (debt_weight * self.cost_of_debt * (1 - self.tax_rate))
        
        print(f"WACC Calculation:")
        print(f"  Cost of Equity: {self.cost_of_equity*100:.2f}%")
        print(f"  WACC: {self.wacc*100:.2f}%\n")
    
    def calculate_terminal_value(self):
        """Calculate terminal value using perpetuity growth"""
        terminal_fcf = self.projected_fcf[-1] * (1 + self.terminal_growth_rate)
        self.terminal_value = terminal_fcf / (self.wacc - self.terminal_growth_rate)
        
        print(f"Terminal Value:")
        print(f"  Terminal FCF: ${terminal_fcf/1e9:.2f}B")
        print(f"  Terminal Value: ${self.terminal_value/1e9:.2f}B\n")
    
    def calculate_valuation(self):
        """Calculate enterprise value and fair value per share"""
        # Discount projected FCF
        pv_fcf = sum([fcf / (1 + self.wacc) ** (i+1) for i, fcf in enumerate(self.projected_fcf)])
        
        # Discount terminal value
        terminal_discount_factor = 1 / (1 + self.wacc) ** self.projection_years
        terminal_pv = self.terminal_value * terminal_discount_factor
        
        # Enterprise Value
        self.enterprise_value = pv_fcf + terminal_pv
        
        # Get net debt (assume minimal for NVDA)
        cash = self.balance_sheet.loc['Cash And Cash Equivalents'].iloc[0] if 'Cash And Cash Equivalents' in self.balance_sheet.index else 0
        self.net_debt = -cash  # Positive net cash for NVDA
        
        # Equity Value
        self.equity_value = self.enterprise_value - self.net_debt
        
        # Fair value per share
        self.fair_value_per_share = self.equity_value * 1e9 / self.shares_outstanding
        
        self.upside_downside = ((self.fair_value_per_share / self.current_price) - 1) * 100
        
        print("DCF Valuation Summary:")
        print(f"  PV of Projected FCF: ${pv_fcf/1e9:.2f}B")
        print(f"  PV of Terminal Value: ${terminal_pv/1e9:.2f}B ({terminal_pv/self.enterprise_value*100:.0f}% of EV)")
        print(f"  Enterprise Value: ${self.enterprise_value/1e9:.2f}B")
        print(f"  Less: Net Debt: ${self.net_debt/1e9:.2f}B")
        print(f"  Equity Value: ${self.equity_value/1e9:.2f}B")
        print(f"\n  Fair Value Per Share: ${self.fair_value_per_share:.2f}")
        print(f"  Current Market Price: ${self.current_price:.2f}")
        print(f"  Upside/(Downside): {self.upside_downside:.1f}%\n")
    
    def sensitivity_analysis(self):
        """Perform sensitivity analysis on WACC and terminal growth rate"""
        print("Sensitivity Analysis: Fair Value Per Share")
        print("(Terminal Growth Rate vs WACC)\n")
        
        wacc_range = np.arange(self.wacc - 0.02, self.wacc + 0.025, 0.01)
        tgr_range = np.arange(self.terminal_growth_rate - 0.015, self.terminal_growth_rate + 0.02, 0.01)
        
        sensitivity_table = pd.DataFrame(index=tgr_range, columns=wacc_range)
        
        for wacc_var in wacc_range:
            for tgr_var in tgr_range:
                if wacc_var > tgr_var:  # WACC must be greater than growth rate
                    # Calculate EV with different assumptions
                    pv_fcf_var = sum([fcf / (1 + wacc_var) ** (i+1) for i, fcf in enumerate(self.projected_fcf)])
                    terminal_fcf_var = self.projected_fcf[-1] * (1 + tgr_var)
                    terminal_value_var = terminal_fcf_var / (wacc_var - tgr_var)
                    terminal_pv_var = terminal_value_var / (1 + wacc_var) ** self.projection_years
                    ev_var = pv_fcf_var + terminal_pv_var
                    
                    eq_val = ev_var - self.net_debt
                    fv_share = eq_val * 1e9 / self.shares_outstanding
                    sensitivity_table.loc[tgr_var, wacc_var] = fv_share
        
        # Display table
        sensitivity_display = sensitivity_table.astype(float).round(2)
        print(sensitivity_display.to_string())
        
        print(f"\nBase Case (WACC={self.wacc*100:.2f}%, TGR={self.terminal_growth_rate*100:.2f}%): ${self.fair_value_per_share:.2f}")
        print(f"Best Case: ${sensitivity_display.max().max():.2f}")
        print(f"Worst Case: ${sensitivity_display.min().min():.2f}\n")
    
    def print_summary(self):
        """Print executive summary"""
        print("\n" + "="*70)
        print("NVIDIA (NVDA) DCF VALUATION MODEL - EXECUTIVE SUMMARY")
        print("="*70)
        print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print(f"\n📊 BASE CASE VALUATION")
        print(f"  Fair Value Per Share:        ${self.fair_value_per_share:>10.2f}")
        print(f"  Current Market Price:        ${self.current_price:>10.2f}")
        print(f"  Upside/(Downside):           {self.upside_downside:>10.1f}%")
        
        print(f"\n💰 VALUE COMPOSITION")
        print(f"  Enterprise Value:            ${self.enterprise_value/1e9:>10.2f}B")
        pv_fcf = sum([fcf / (1 + self.wacc) ** (i+1) for i, fcf in enumerate(self.projected_fcf)])
        terminal_pv = (self.terminal_value / (1 + self.wacc) ** self.projection_years)
        print(f"  PV of 5-Year FCF:            ${pv_fcf/1e9:>10.2f}B ({pv_fcf/self.enterprise_value*100:.0f}%)")
        print(f"  PV of Terminal Value:        ${terminal_pv/1e9:>10.2f}B ({terminal_pv/self.enterprise_value*100:.0f}%)")
        
        print(f"\n📈 KEY ASSUMPTIONS")
        print(f"  WACC:                        {self.wacc*100:>10.2f}%")
        print(f"  Cost of Equity:              {self.cost_of_equity*100:>10.2f}%")
        print(f"  Beta:                        {self.beta:>10.2f}")
        print(f"  Terminal Growth Rate:        {self.terminal_growth_rate*100:>10.2f}%")
        print(f"  Tax Rate:                    {self.tax_rate*100:>10.2f}%")
        
        print("\n" + "="*70 + "\n")
    
    def run(self):
        """Run the complete DCF model"""
        print("\n" + "="*70)
        print("NVIDIA DCF VALUATION MODEL")
        print("="*70 + "\n")
        
        self.fetch_data()
        self.calculate_historical_metrics()
        self.project_cash_flows()
        self.calculate_wacc()
        self.calculate_terminal_value()
        self.calculate_valuation()
        self.sensitivity_analysis()
        self.print_summary()
        
        return {
            'fair_value': self.fair_value_per_share,
            'market_price': self.current_price,
            'upside_downside': self.upside_downside,
            'enterprise_value': self.enterprise_value,
            'wacc': self.wacc
        }


if __name__ == "__main__":
    model = NVDADCFModel()
    result = model.run()
