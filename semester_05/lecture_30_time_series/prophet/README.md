# Prophet

1. **Name of Algorithm**  
   Prophet

2. **What problem does it solve? (1 sentence)**  
   Forecasts time series with automatic handling of trends, seasonality, and holidays using additive decomposition, designed for business time series with strong seasonal patterns.

3. **Intuition (plain-language explanation)**  
   Like a smart calendar that understands patterns: automatically detects if data grows linearly or saturates (trend), finds weekly/monthly/yearly patterns (seasonality), and accounts for special events (holidays) to forecast future values.

4. **Inputs & Outputs**  
   - Input: Time series data (ds: dates, y: values), optional holiday calendar, growth model (linear or logistic).  
   - Output: Forecasted values with uncertainty intervals and decomposed components (trend, seasonality, holidays).

5. **Step-by-step description (5–10 lines max)**  
1. Model time series as: y(t) = g(t) + s(t) + h(t) + ε, where g=trend, s=seasonality, h=holidays, ε=noise.
2. Fit trend component: linear or logistic growth with changepoints.
3. Fit seasonality: Fourier series for weekly, monthly, yearly patterns.
4. Fit holiday effects: indicator variables for known holidays.
5. Estimate parameters using Bayesian inference or maximum likelihood.
6. Generate forecasts with uncertainty intervals using posterior predictive distribution.

6. **Tiny example (hand-simulated)**  
   E-commerce sales: daily data → Prophet detects: upward trend (business growing), weekly seasonality (higher on weekends), yearly seasonality (holiday spikes), Black Friday effect → forecast: next 30 days with confidence bands.

7. **Time & Space Complexity**  
   - Time: O(n) for fitting where n is number of observations (efficient optimization).  
   - Space: O(n) for storing time series and model components.

8. **Strengths**  
- Automatic handling of seasonality and holidays.
- Robust to missing data and outliers.
- Interpretable components (trend, seasonality).

9. **Weaknesses / limitations**  
- Designed for daily/weekly data with strong seasonality.
- May not capture complex non-linear patterns as well as neural networks.

10. **Compare with alternatives**  
    Alternatives: ARIMA, LSTM, Exponential Smoothing, NeuralProphet

11. **30-second explanation (your own words)**  
    Decomposes time series into trend, seasonality, and holiday components using additive model, automatically handling common patterns in business time series for robust forecasting.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
