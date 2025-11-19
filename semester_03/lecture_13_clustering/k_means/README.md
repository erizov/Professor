# K-Means Clustering

1. **Name of Algorithm**  
   K-Means Clustering

2. **What problem does it solve? (1 sentence)**  
   Partitions data into k clusters by iteratively assigning points to nearest cluster centers and updating centers, finding groups of similar data points.

3. **Intuition (plain-language explanation)**  
   Like organizing items into groups: K-Means is like organizing a messy room into k boxes - you start by placing k boxes (cluster centers) randomly, then you put each item (data point) in the nearest box, then you move each box to the center of its items, and repeat until the boxes stop moving - the result is k organized groups (clusters) where items in each group are similar to each other.

4. **Inputs & Outputs**  
   - Input: Data points, number of clusters k, distance metric, initialization method, convergence criteria.  
   - Output: K clusters, cluster centers (centroids), cluster assignments, within-cluster sum of squares.

5. **Step-by-step description (5–10 lines max)**  
1. Initialize: randomly select k initial cluster centers (centroids).
2. Assign: assign each data point to nearest centroid.
3. Update: update each centroid to mean of points in its cluster.
4. Check: check if centroids changed significantly (convergence).
5. Repeat: if not converged, repeat assignment and update steps.
6. Converge: stop when centroids stabilize or max iterations reached.
7. Compute: compute within-cluster sum of squares (WCSS).
8. Validate: validate clustering quality (silhouette score, elbow method).
9. Refine: optionally refine with different initializations.
10. Return: return final clusters and centroids.

6. **Tiny example (hand-simulated)**  
   K-Means: data: 1000 customer purchase records → k: 5 clusters → initialize: 5 random centroids → assign: each customer to nearest centroid → update: move centroids to cluster means → repeat: 10 iterations → converge: clusters stable → result: 5 customer segments (budget, premium, etc.) → K-Means successful.

7. **Time & Space Complexity**  
   - Time: O(n·k·d·i) where n is points, k is clusters, d is dimensions, i is iterations (typically O(n·k·d) for few iterations).  
   - Space: O(n·d + k·d) where n·d is data points, k·d is centroids.

8. **Strengths**  
- Simplicity: simple and easy to implement.
- Efficiency: fast and scalable for large datasets.
- Versatility: works well for spherical, well-separated clusters.

9. **Weaknesses / limitations**  
- K selection: requires specifying number of clusters k in advance.
- Initialization: sensitive to initial centroid placement.
- Shape: assumes spherical clusters, struggles with non-spherical shapes.

10. **Compare with alternatives**  
    Alternatives: Hierarchical Clustering, DBSCAN, Gaussian Mixture Models, K-Medoids

11. **30-second explanation (your own words)**  
    Partitions data into k clusters by iteratively assigning points to nearest cluster centers and updating centers, finding groups of similar data points.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
