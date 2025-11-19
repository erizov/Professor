# ARIMA (AutoRegressive Integrated Moving Average)

1. **Name of Algorithm**  
   ARIMA (AutoRegressive Integrated Moving Average)

2. **What problem does it solve? (1 sentence)**  
   Models time series data by combining autoregressive (AR), differencing (I), and moving average (MA) components to capture trends, seasonality, and noise for forecasting.

3. **Intuition (plain-language explanation)**  
   Like predicting tomorrow's weather: use past values (AR), account for trends by looking at changes (I), and smooth out noise using averages (MA) to forecast future values.

4. **Inputs & Outputs**  
   - Input: Time series data, AR order (p), differencing order (d), MA order (q), seasonal parameters (optional).  
   - Output: Fitted ARIMA model and forecasts for future time points with confidence intervals.

5. **Step-by-step description (5–10 lines max)**  
1. Check stationarity: if non-stationary, apply differencing (d times) to make it stationary.
2. Identify AR order (p): how many past values to use for prediction.
3. Identify MA order (q): how many past forecast errors to use.
4. Estimate model parameters using maximum likelihood estimation.
5. Validate model: check residuals for white noise (no patterns).
6. Forecast future values using fitted model with prediction intervals.

6. **Tiny example (hand-simulated)**  
   Stock prices: non-stationary → difference once (d=1) → ARIMA(1,1,1): uses yesterday's price change (AR) and yesterday's forecast error (MA) → forecast: price tomorrow = today's price + predicted change ± confidence interval.

7. **Time & Space Complexity**  
   - Time: O(n²) for parameter estimation where n is time series length.  
   - Space: O(n) for storing time series data and model parameters.

8. **Strengths**  
- Interpretable model with clear statistical foundation.
- Handles trends and seasonality effectively.

9. **Weaknesses / limitations**  
- Requires manual parameter selection (p, d, q).
- Assumes linear relationships and may miss complex patterns.

10. **Compare with alternatives**  
    Alternatives: LSTM/GRU, Prophet, Exponential Smoothing, SARIMA (seasonal ARIMA)

11. **30-second explanation (your own words)**  
    Models time series by combining autoregressive terms, differencing for stationarity, and moving average terms, providing interpretable forecasts with statistical guarantees.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
