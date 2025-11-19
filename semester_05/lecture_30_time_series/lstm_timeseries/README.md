# LSTM for Time Series

1. **Name of Algorithm**  
   LSTM for Time Series

2. **What problem does it solve? (1 sentence)**  
   Uses Long Short-Term Memory networks to model temporal dependencies in time series data, capturing long-range patterns and non-linear relationships for forecasting.

3. **Intuition (plain-language explanation)**  
   Like a memory system that remembers important patterns from the past: LSTM selectively remembers and forgets information, allowing it to capture both short-term fluctuations and long-term trends in time series.

4. **Inputs & Outputs**  
   - Input: Time series data, sequence length (lookback window), LSTM architecture, number of layers.  
   - Output: Forecasted future values with ability to capture complex temporal patterns.

5. **Step-by-step description (5–10 lines max)**  
1. Prepare sequences: create sliding windows of fixed length (e.g., 60 days) as input, next value as target.
2. Build LSTM network: input layer, one or more LSTM layers, dense output layer.
3. LSTM processes sequences: forget gate, input gate, output gate control information flow.
4. Train on historical sequences using backpropagation through time.
5. Validate on hold-out period to prevent overfitting.
6. Forecast: use last N values to predict next value, iteratively for multi-step ahead.

6. **Tiny example (hand-simulated)**  
   Stock prices: input sequence [price_day1, ..., price_day60] → LSTM processes → hidden states capture patterns → output: predicted price_day61. For 7-day forecast: predict day 61, use it to predict day 62, etc.

7. **Time & Space Complexity**  
   - Time: O(n·l·d²) where n is sequence length, l is number of layers, d is hidden dimension (sequential processing).  
   - Space: O(l·d²) for LSTM parameters plus O(n·d) for hidden states.

8. **Strengths**  
- Captures long-range dependencies and non-linear patterns.
- Flexible architecture adaptable to various time series characteristics.

9. **Weaknesses / limitations**  
- Requires large amounts of data for training.
- Less interpretable than statistical models like ARIMA.

10. **Compare with alternatives**  
    Alternatives: ARIMA, Prophet, GRU, Transformer for Time Series

11. **30-second explanation (your own words)**  
    Uses LSTM networks to model temporal dependencies in time series, leveraging memory cells to capture both short-term and long-term patterns for accurate forecasting.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
