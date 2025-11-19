# K-Means Clustering

1. **Name of Algorithm**  
   K-Means Clustering

2. **What problem does it solve? (1 sentence)**  
   Partitions n data points into k clusters by minimizing within-cluster variance and maximizing between-cluster separation.

3. **Intuition (plain-language explanation)**  
   Place k centroids randomly, assign each point to the nearest centroid, move centroids to cluster centers, repeat until stable.

4. **Inputs & Outputs**  
   - Input: Dataset of n points with d features and desired number of clusters k.  
   - Output: k cluster centroids and assignment of each point to a cluster.

5. **Step-by-step description (5–10 lines max)**  
1. Initialize k centroids randomly or using k-means++.
2. Assign each point to the nearest centroid (Euclidean distance).
3. Update each centroid to the mean of points in its cluster.
4. Repeat assignment and update steps until centroids converge or max iterations.
5. Return final centroids and cluster assignments.

6. **Tiny example (hand-simulated)**  
   Points: [(1,1), (1,2), (5,4), (6,5)], k=2 → clusters: {[(1,1),(1,2)], [(5,4),(6,5)]} with centroids (1,1.5) and (5.5,4.5).

7. **Time & Space Complexity**  
   - Time: O(n·k·d·i) where i is iterations, typically converges quickly.  
   - Space: O(n·d + k·d) for points and centroids.

8. **Strengths**  
- Simple and fast for large datasets.
- Works well with spherical, well-separated clusters.

9. **Weaknesses / limitations**  
- Requires specifying k in advance.
- Sensitive to initialization and may converge to local optima.

10. **Compare with alternatives**  
    Alternatives: Hierarchical Clustering, DBSCAN, Gaussian Mixture Models

11. **30-second explanation (your own words)**  
    Iteratively refine cluster centers by assigning points to nearest centroids and updating centroids to cluster means.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
