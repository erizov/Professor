# Model Caching

1. **Name of Algorithm**  
   Model Caching

2. **What problem does it solve? (1 sentence)**  
   Caches loaded models and frequently used predictions in memory or fast storage to avoid repeated model loading and redundant computations, reducing latency and improving inference throughput.

3. **Intuition (plain-language explanation)**  
   Like keeping frequently used tools on your desk: instead of loading the model from disk every time (slow), keep it in memory (fast) - and if you've seen the same input before, reuse the prediction instead of recomputing it.

4. **Inputs & Outputs**  
   - Input: Model files, inference requests, cache storage (memory, Redis, etc.), cache eviction policy.  
   - Output: Cached models ready for inference, cached predictions for repeated queries.

5. **Step-by-step description (5–10 lines max)**  
1. Model caching: load model into memory on startup or first request, keep in memory for subsequent requests.
2. Prediction caching: hash input data to create cache key, check if prediction exists in cache.
3. Cache hit: return cached prediction immediately (no model inference needed).
4. Cache miss: run model inference, store result in cache with input hash as key.
5. Cache eviction: remove old or least-recently-used entries when cache is full (LRU, LFU, or TTL-based).
6. Cache invalidation: invalidate cache when model is updated or data changes significantly.
7. Distributed caching: use shared cache (Redis, Memcached) for multi-instance deployments.
8. Monitor cache: track hit rate, cache size, and performance metrics.

6. **Tiny example (hand-simulated)**  
   Image classification API: first request for image X → load ResNet-50 (2s) → inference (50ms) → cache prediction → subsequent requests for image X → cache hit (1ms) → return cached result. Model caching: load model once → serve 1000 requests → no reload needed.

7. **Time & Space Complexity**  
   - Time: O(1) for cache lookup, O(M) for model loading (one-time), O(I) for inference on cache miss where I is inference time.  
   - Space: O(M) for model in memory, O(C·(S+P)) for prediction cache where C is cache size, S is input size, P is prediction size.

8. **Strengths**  
- Reduces latency: cache hits are orders of magnitude faster than inference.
- Improves throughput: model loading overhead eliminated for cached models.
- Cost effective: reduces compute costs for repeated queries.

9. **Weaknesses / limitations**  
- Memory intensive: requires storing models and predictions in memory.
- Cache invalidation: must handle model updates and data changes carefully.

10. **Compare with alternatives**  
    Alternatives: No Caching, Model Warm-up, Prediction Precomputation, CDN Caching

11. **30-second explanation (your own words)**  
    Caches loaded models and predictions in memory to avoid repeated loading and redundant computations, significantly reducing latency and improving inference throughput for repeated queries.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
