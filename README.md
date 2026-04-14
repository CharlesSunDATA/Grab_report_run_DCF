# NVIDIA (NVDA) DCF Valuation Model

## Overview

This repository contains a comprehensive **Discounted Cash Flow (DCF)** valuation model for NVIDIA (NVDA) stock. The model projects NVIDIA's future cash flows, calculates enterprise and equity value, and provides sensitivity analysis to understand how changes in key assumptions affect the valuation.

## Project Structure

```
Grab_report_run_DCF/
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── NVDA_DCF_Model.ipynb          # Main DCF model (Jupyter Notebook)
```

## Model Overview

The DCF model does the following:

1. **Fetches Historical Data** - Uses Yahoo Finance to retrieve NVIDIA's financial statements
2. **Calculates Historical Metrics** - Analyzes revenue growth, operating margins, and free cash flow
3. **Projects Future Cash Flows** - Forecasts 5 years of revenue, operating income, and free cash flow
4. **Calculates Terminal Value** - Estimates value beyond the projection period using perpetuity growth
5. **Discounts to Present Value** - Uses WACC to discount all cash flows
6. **Calculates Equity Value** - Derives stock valuation from enterprise value
7. **Sensitivity Analysis** - Shows how valuation changes with different WACC and growth rate assumptions
8. **Visualizations** - Charts for revenues, cash flows, and sensitivity heatmaps

## Key Assumptions (Base Case)

### Valuation Parameters
- **WACC (Discount Rate):** 10.05%
  - Cost of Equity: 14.59% (using CAPM with Beta=1.85)
  - Risk-Free Rate: 4.0%
  - Market Risk Premium: 5.5%
- **Tax Rate:** 15%
- **Terminal Growth Rate:** 3.0%

### Projection Parameters (5-Year)
- **Revenue Growth Rates:** 25%, 22%, 18%, 15%, 12% (declining trajectory)
- **Operating Margins:** 42-44% (stable, high-margin business)
- **CapEx as % of Revenue:** 2%
- **Working Capital Change:** 1% of revenue growth

## Getting Started

### Prerequisites
- Python 3.8+
- Jupyter Notebook
- Required packages (see requirements.txt)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Grab_report_run_DCF
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Model

1. Start Jupyter:
```bash
jupyter notebook
```

2. Open `NVDA_DCF_Model.ipynb` and run all cells sequentially

3. The notebook will output:
   - Fair value per share (DCF valuation)
   - Upside/Downside vs. current market price
   - Sensitivity analysis table and heatmap
   - Projections and visualizations

## Model Components

### 1. Historical Analysis
- Retrieves 5 years of income statements, balance sheets, and cash flow statements
- Calculates revenue growth rates, operating margins, and free cash flow
- Provides baseline for projections

### 2. Cash Flow Projections
- Projects revenue based on declining growth assumptions (capturing market maturity)
- Applies operating margin assumptions to calculate operating income
- Calculates NOPAT (Net Operating Profit After Tax)
- Deducts CapEx and working capital changes to derive Free Cash Flow

### 3. WACC Calculation
Uses Capital Asset Pricing Model (CAPM) for cost of equity:
- **Cost of Equity = Risk-Free Rate + Beta × Market Risk Premium**
- WACC = (% Equity × Cost of Equity) + (% Debt × Cost of Debt × (1 - Tax Rate))

### 4. Terminal Value
Uses perpetuity growth method:
- **Terminal Value = Terminal Year FCF × (1 + g) / (WACC - g)**
- Where g = long-term growth rate (typically GDP growth)

### 5. Enterprise & Equity Value
- **Enterprise Value** = PV of projected FCF + PV of Terminal Value
- **Equity Value** = Enterprise Value - Net Debt
- **Fair Value Per Share** = Equity Value / Shares Outstanding

### 6. Sensitivity Analysis
- Creates a 2D sensitivity table showing fair value per share across:
  - WACC range: ±2% from base case
  - Terminal Growth Rate range: ±1.5% from base case
- Visualized as a heatmap for easy interpretation

## Interpreting Results

### Fair Value vs. Market Price
- **Fair Value > Market Price:** Stock appears undervalued (potential upside)
- **Fair Value < Market Price:** Stock appears overvalued (potential downside)
- **Upside/Downside %:** Indicates potential return if model assumptions are correct

### Sensitivity Analysis
- **Bull Case:** Lower WACC (more confidence in cash flows) or higher terminal growth
- **Base Case:** Mid-range assumptions based on historical performance
- **Bear Case:** Higher WACC (more risk) or lower terminal growth

## Key Insights from This Model

The DCF model reveals:
- NVIDIA as a **high-margin, high-growth business** with 42-44% operating margins
- **Significant reliance on terminal value** (~70% of enterprise value)
- **High sensitivity to cost of capital** (WACC) given the long projection period
- **Revenue growth slowdown expected** as NVIDIA's markets mature (25% → 12%)

## Customization

To modify assumptions, edit these cells:

1. **Section 4 (Projections)**: Adjust revenue growth rates and operating margins
2. **Section 5 (Terminal Value)**: Change terminal growth rate and WACC components
3. **Section 8 (Sensitivity)**: Modify WACC and TGR ranges for sensitivity analysis

## Model Limitations

⚠️ **Important Considerations:**

- **Historical dependency:** Model assumes past growth patterns continue
- **Assumption sensitivity:** Small changes in WACC or growth rates significantly impact valuation
- **Terminal value risk:** ~70% of value comes from terminal value (uncertain long-term assumptions)
- **Market conditions:** Doesn't account for competitive threats or market changes
- **Data quality:** Relies on Yahoo Finance data availability and accuracy
- **Not accounting for:** Special items, one-time costs, major M&A activity

## Further Enhancements

Potential improvements to the model:
- Scenario analysis (bull/base/bear cases)
- Two-stage DCF with different growth rates pre/post maturity
- Peer comparison (P/E, EV/Revenue multiples)
- Monte Carlo simulation for probability distributions
- Market sentiment and option-implied valuation
- Detailed industry analysis and competitive positioning

## Disclaimer

This DCF model is for educational and analytical purposes only. It should not be considered as financial advice. Investment decisions should be based on thorough research, understanding of your risk tolerance, and consultation with financial professionals.

The accuracy of DCF valuations depends heavily on the quality of assumptions. Small changes in discount rates or growth assumptions can significantly impact results.

## References

- [NVIDIA Investor Relations](https://investor.nvidia.com/)
- [Yahoo Finance](https://finance.yahoo.com/)
- Damodaran, A. (2012). *Damodaran on Valuation*
- Roic & Co. DCF Methodology

## License

This project is provided as-is for educational purposes.

---

**Last Updated:** April 2025  
**Model Version:** 1.0  
**Data Source:** Yahoo Finance via yfinance