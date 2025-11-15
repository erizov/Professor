import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

/**
 * K-Means Clustering implementation.
 * 
 * Time Complexity: O(n*k*d*i) where i is iterations
 * Space Complexity: O(n + k*d)
 */
public class Algorithm {
    
    /**
     * Calculate Euclidean distance.
     */
    private static double euclideanDistance(double[] p1, double[] p2) {
        double sum = 0.0;
        for (int i = 0; i < p1.length; i++) {
            sum += Math.pow(p1[i] - p2[i], 2);
        }
        return Math.sqrt(sum);
    }
    
    /**
     * K-Means Clustering Algorithm.
     */
    public static class KMeans {
        private int k;
        private int maxIters;
        private long randomState;
        private double[][] centroids;
        private int[] labels;
        private double inertia;
        private List<double[]> history;
        
        /**
         * Initialize K-Means.
         */
        public KMeans(int k, int maxIters, long randomState) {
            this.k = k;
            this.maxIters = maxIters;
            this.randomState = randomState;
            this.history = new ArrayList<>();
        }
        
        /**
         * Fit K-Means to data.
         */
        public void fit(double[][] X) {
            Random rand = new Random(randomState);
            int nSamples = X.length;
            int nFeatures = X[0].length;
            
            // Initialize centroids randomly
            centroids = new double[k][nFeatures];
            List<Integer> indices = new ArrayList<>();
            for (int i = 0; i < nSamples; i++) {
                indices.add(i);
            }
            
            for (int i = 0; i < k; i++) {
                int idx = rand.nextInt(indices.size());
                int sampleIdx = indices.remove(idx);
                System.arraycopy(X[sampleIdx], 0, centroids[i], 0, 
                               nFeatures);
            }
            
            labels = new int[nSamples];
            
            for (int iteration = 0; iteration < maxIters; iteration++) {
                // Assign points to nearest centroid
                int[] newLabels = new int[nSamples];
                for (int i = 0; i < nSamples; i++) {
                    double minDist = Double.MAX_VALUE;
                    int minIdx = 0;
                    
                    for (int j = 0; j < k; j++) {
                        double dist = euclideanDistance(X[i], centroids[j]);
                        if (dist < minDist) {
                            minDist = dist;
                            minIdx = j;
                        }
                    }
                    newLabels[i] = minIdx;
                }
                
                // Check convergence
                if (Arrays.equals(newLabels, labels)) {
                    break;
                }
                
                labels = newLabels;
                
                // Update centroids
                double[][] newCentroids = new double[k][nFeatures];
                int[] counts = new int[k];
                
                for (int i = 0; i < nSamples; i++) {
                    int cluster = labels[i];
                    for (int j = 0; j < nFeatures; j++) {
                        newCentroids[cluster][j] += X[i][j];
                    }
                    counts[cluster]++;
                }
                
                for (int i = 0; i < k; i++) {
                    if (counts[i] > 0) {
                        for (int j = 0; j < nFeatures; j++) {
                            newCentroids[i][j] /= counts[i];
                        }
                        centroids[i] = newCentroids[i];
                    }
                }
                
                // Calculate inertia
                double inertiaVal = 0.0;
                for (int i = 0; i < nSamples; i++) {
                    double dist = euclideanDistance(X[i], 
                                                   centroids[labels[i]]);
                    inertiaVal += dist * dist;
                }
                
                history.add(new double[]{iteration, inertiaVal});
            }
            
            // Final inertia
            inertia = 0.0;
            for (int i = 0; i < nSamples; i++) {
                double dist = euclideanDistance(X[i], centroids[labels[i]]);
                inertia += dist * dist;
            }
        }
        
        /**
         * Predict cluster labels.
         */
        public int[] predict(double[][] X) {
            int[] predictions = new int[X.length];
            
            for (int i = 0; i < X.length; i++) {
                double minDist = Double.MAX_VALUE;
                int minIdx = 0;
                
                for (int j = 0; j < k; j++) {
                    double dist = euclideanDistance(X[i], centroids[j]);
                    if (dist < minDist) {
                        minDist = dist;
                        minIdx = j;
                    }
                }
                predictions[i] = minIdx;
            }
            
            return predictions;
        }
        
        public double[][] getCentroids() { return centroids; }
        public int[] getLabels() { return labels; }
        public double getInertia() { return inertia; }
        public List<double[]> getHistory() { return history; }
    }
    
    /**
     * Generate synthetic clustered data.
     */
    private static class DataGenerator {
        private Random rand;
        
        public DataGenerator(long seed) {
            this.rand = new Random(seed);
        }
        
        public double[][] generate(int nSamples, int nClusters) {
            double[][] X = new double[nSamples * nClusters][2];
            
            for (int cluster = 0; cluster < nClusters; cluster++) {
                double[] center = {cluster * 5.0, cluster * 5.0};
                
                for (int i = 0; i < nSamples; i++) {
                    int idx = cluster * nSamples + i;
                    X[idx][0] = center[0] + rand.nextGaussian();
                    X[idx][1] = center[1] + rand.nextGaussian();
                }
            }
            
            return X;
        }
    }
    
    /**
     * Main method for demonstration.
     */
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("K-MEANS CLUSTERING DEMONSTRATION");
        System.out.println("=".repeat(70));
        System.out.println();
        
        DataGenerator gen = new DataGenerator(42);
        
        // Example 1: Basic clustering
        System.out.println("Example 1: Basic Clustering");
        System.out.println("-".repeat(70));
        
        double[][] X = gen.generate(30, 3);
        
        System.out.printf("Generated %d samples in 3 clusters%n", X.length);
        System.out.println();
        
        KMeans kmeans = new KMeans(3, 100, 42);
        kmeans.fit(X);
        
        System.out.printf("Converged in %d iterations%n", 
                         kmeans.getHistory().size());
        System.out.printf("Final inertia: %.2f%n", kmeans.getInertia());
        System.out.println();
        
        System.out.println("Cluster centroids:");
        double[][] centroids = kmeans.getCentroids();
        for (int i = 0; i < centroids.length; i++) {
            System.out.printf("  Cluster %d: [%.2f, %.2f]%n",
                            i, centroids[i][0], centroids[i][1]);
        }
        System.out.println();
        
        // Example 2: Cluster sizes
        System.out.println("Example 2: Cluster Sizes");
        System.out.println("-".repeat(70));
        
        int[] clusterCounts = new int[3];
        for (int label : kmeans.getLabels()) {
            clusterCounts[label]++;
        }
        
        for (int i = 0; i < clusterCounts.length; i++) {
            System.out.printf("  Cluster %d: %d samples%n", 
                            i, clusterCounts[i]);
        }
        System.out.println();
        
        // Example 3: Predict new points
        System.out.println("Example 3: Predicting New Points");
        System.out.println("-".repeat(70));
        
        double[][] X_test = {
            {0.0, 0.0},
            {5.0, 5.0},
            {10.0, 10.0}
        };
        
        int[] predictions = kmeans.predict(X_test);
        
        System.out.println("Predictions:");
        for (int i = 0; i < X_test.length; i++) {
            System.out.printf("  Point [%.1f, %.1f] → Cluster %d%n",
                            X_test[i][0], X_test[i][1], predictions[i]);
        }
        System.out.println();
        
        // Example 4: Performance measurement
        System.out.println("Example 4: Performance Measurement");
        System.out.println("-".repeat(70));
        
        int[] sizes = {100, 500, 1000};
        
        for (int size : sizes) {
            double[][] X_perf = gen.generate(size / 3, 3);
            KMeans model = new KMeans(3, 50, 42);
            
            long start = System.nanoTime();
            model.fit(X_perf);
            long end = System.nanoTime();
            
            double ms = (end - start) / 1_000_000.0;
            System.out.printf("n=%4d: %8.3f ms%n", size, ms);
        }
        
        System.out.println();
        System.out.println("=".repeat(70));
        System.out.println("\nComplexity Summary:");
        System.out.println("  Time:  O(n*k*d*i)");
        System.out.println("  Space: O(n + k*d)");
        System.out.println("\nKey Points:");
        System.out.println("  + Simple and fast");
        System.out.println("  + Works well for spherical clusters");
        System.out.println("  + Scalable");
        System.out.println("  - Requires knowing K");
        System.out.println("  - Sensitive to initialization");
        System.out.println("\nWhen to use:");
        System.out.println("  • Know number of clusters");
        System.out.println("  • Spherical clusters");
        System.out.println("  • Large datasets");
        System.out.println("=".repeat(70));
        
        long endTime = System.nanoTime();
        double totalMs = (endTime - startTime) / 1_000_000.0;
        System.out.printf("\nTotal execution time: %.3f ms%n", totalMs);
    }
}
