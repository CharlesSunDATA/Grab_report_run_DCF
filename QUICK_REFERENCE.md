# NVDA DCF Model - Quick Reference Guide

## Files in This Repository

### 📓 **NVDA_DCF_Model.ipynb** (Recommended - Interactive Jupyter Notebook)
- Full DCF model with visualizations
- Step-by-step analysis with outputs
- Charts and sensitivity heatmaps
- Perfect for learning and deep analysis

### 🐍 **nvda_dcf_cli.py** (Command-line Script)
- Standalone Python script (no Jupyter required)
- Quick valuations and sensitivity analysis
- Useful for automation and batch runs
- Usage: `python nvda_dcf_cli.py`

### 📋 **README.md** (Full Documentation)
- Comprehensive model documentation
- Installation instructions
- Detailed explanation of each component
- Interpretation guide

---

## Key Files at a Glance

| File | Purpose | Use When |
|------|---------|----------|
| `NVDA_DCF_Model.ipynb` | Interactive DCF analysis | Want visualizations & detailed outputs |
| `nvda_dcf_cli.py` | Command-line valuation | Need quick results, no Jupyter |
| `requirements.txt` | Python dependencies | Setting up environment |
| `README.md` | Complete documentation | Need detailed explanation |

---

## Quick Start (5 Minutes)

### Using Jupyter Notebook (Recommended)
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start Jupyter
jupyter notebook

# 3. Open NVDA_DCF_Model.ipynb and run all cells (Shift+Enter)
```

### Using Command-Line Script
```bash
# 1. Install dependencies  
pip install -r requirements.txt

# 2. Run the model
python nvda_dcf_cli.py
```

---

## What the Model Does

```
┌─────────────────────────────────────────────────┐
│ STEP 1: Fetch Historical Data                   │
│ (5 years of financials from Yahoo Finance)      │
└────────────┬────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────┐
│ STEP 2: Calculate Historical Metrics            │
│ (Revenue growth, margins, FCF trends)           │
└────────────┬────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────┐
│ STEP 3: Make Projections (5 Years)              │
│ (Revenue, Op Income, FCF)                       │
└────────────┬────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────┐
│ STEP 4: Calculate Terminal Value                │
│ (Perpetuity growth method)                      │
└────────────┬────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────┐
│ STEP 5: Discount to Present Value               │
│ (Using WACC = 10.05%)                           │
└────────────┬────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────┐
│ STEP 6: Calculate Equity Value                  │
│ (Enterprise Value - Net Debt)                   │
└────────────┬────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────┐
│ RESULT: Fair Value Per Share                    │
│ Compare with current market price                │
└─────────────────────────────────────────────────┘
```

---

## Model Summary (Base Case)

| Metric | Value |
|--------|-------|
| **Fair Value Per Share** | Model calculates this |
| **Current Price** | Fetched from market |
| **Upside/Downside** | Fair Value vs Market |
| **WACC** | 10.05% |
| **Terminal Growth** | 3.0% |
| **Projection Period** | 5 Years |
| **Tax Rate** | 15% |

---

## Key Insights

✅ **Strengths of NVIDIA (from model)**
- Very high operating margins (42-44%)
- Strong historical revenue growth (25%+ CAGR)
- Positive and growing free cash flow
- Minimal debt

⚠️ **Model Sensitivities**
- **Most Sensitive To:** WACC (discount rate)
- **Terminal Value:** ~70% of total enterprise value
- **Growth Assumptions:** Large impact on valuation

---

## Customizing the Model

To adjust assumptions, open the Jupyter notebook and modify these cells:

1. **Projection Parameters** (Cell with revenue growth rates)
   - `revenue_growth_rates = [0.25, 0.22, 0.18, 0.15, 0.12]`
   - `operating_margin_forecast = [0.42, 0.43, 0.44, 0.44, 0.43]`

2. **Terminal Value** (Cell with terminal assumptions)
   - `terminal_growth_rate = 0.03`

3. **WACC Components** (Cell with cost of capital)
   - `risk_free_rate = 0.04`
   - `beta = 1.85`

---

## Sensitivity Analysis Grid

The model shows how valuation changes across:

| | WACC | Terminal Growth |
|---|------|-----------------|
| **Range** | ±2.0% | ±1.5% |
| **Base Case** | 10.05% | 3.0% |
| **Bull Case** | 8.05% | 4.5% |
| **Bear Case** | 12.05% | 1.5% |

---

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'yfinance'`
**Solution:** Run `pip install -r requirements.txt`

### Issue: Yahoo Finance returns no data
**Solution:** Check internet connection; Yahoo Finance API may be temporarily unavailable

### Issue: Historical data incomplete
**Solution:** This is normal if NVDA's older financial data is limited; model uses available data

### Issue: Valuation seems too high/low
**Solution:** Adjust WACC or terminal growth rate in sensitivity analysis to see impact

---

## Using Results for Investment Decisions

### Fair Value $X, Market Price $Y

**If Fair Value > Market Price (Upside)**
- Stock appears undervalued
- Potential buying opportunity
- But verify: Do you agree with assumptions?

**If Fair Value < Market Price (Downside)**
- Stock appears overvalued
- Potential risk
- But verify: Has market priced in information model doesn't have?

**Remember:**
- ⚠️ This is ONE valuation method
- ⚠️ Use alongside other methods (multiples, peer comp, etc.)
- ⚠️ Valuation depends heavily on assumptions
- ⚠️ NOT financial advice - consult professionals

---

## Performance Interpretation

### Value Composition
- **PV of 5-Year FCF:** ~30% of enterprise value
- **PV of Terminal Value:** ~70% of enterprise value
  - (Higher terminal value % = more risk from long-term assumptions)

### Historical vs Projections
- Model assumes growth rates decline from 25% to 12%
- Operating margins remain stable at 42-44%
- This reflects market maturation

---

## Next Steps

1. **Run the model** with base assumptions
2. **Review sensitivity analysis** and understand key drivers
3. **Research assumptions**:
   - Are revenue growth rates realistic?
   - Do margins seem achievable?
   - Is WACC appropriate for NVIDIA's risk profile?
4. **Compare results** with:
   - Sell-side analyst estimates
   - Peer company valuations
   - Market multiples (P/E, EV/Revenue)
5. **Make informed decisions** - Don't use DCF in isolation

---

## Additional Resources

- [NVIDIA Investor Relations](https://investor.nvidia.com/)
- [Damodaran DCF Methodology](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/valuations.html)
- [Yahoo Finance NVDA](https://finance.yahoo.com/quote/NVDA)

---

**Happy Analyzing! 📊**

For questions or suggestions, refer to README.md
