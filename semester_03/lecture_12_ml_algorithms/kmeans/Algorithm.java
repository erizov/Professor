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
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
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
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        long startTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("K-MEANS CLUSTERING DEMONSTRATION");
        logger.info(separator);
        logger.info("");
        
        DataGenerator gen = new DataGenerator(42);
        
        // Example 1: Basic clustering
        logger.info("Example 1: Basic Clustering");
        logger.info(dash);
        
        double[][] X = gen.generate(30, 3);
        
        System.out.printf("Generated %d samples in 3 clusters%n", X.length);
        logger.info("");
        
        KMeans kmeans = new KMeans(3, 100, 42);
        kmeans.fit(X);
        
        System.out.printf("Converged in %d iterations%n", 
                         kmeans.getHistory().size());
        System.out.printf("Final inertia: %.2f%n", kmeans.getInertia());
        logger.info("");
        
        logger.info("Cluster centroids:");
        double[][] centroids = kmeans.getCentroids();
        for (int i = 0; i < centroids.length; i++) {
            System.out.printf("  Cluster %d: [%.2f, %.2f]%n",
                            i, centroids[i][0], centroids[i][1]);
        }
        logger.info("");
        
        // Example 2: Cluster sizes
        logger.info("Example 2: Cluster Sizes");
        logger.info(dash);
        
        int[] clusterCounts = new int[3];
        for (int label : kmeans.getLabels()) {
            clusterCounts[label]++;
        }
        
        for (int i = 0; i < clusterCounts.length; i++) {
            System.out.printf("  Cluster %d: %d samples%n", 
                            i, clusterCounts[i]);
        }
        logger.info("");
        
        // Example 3: Predict new points
        logger.info("Example 3: Predicting New Points");
        logger.info(dash);
        
        double[][] X_test = {
            {0.0, 0.0},
            {5.0, 5.0},
            {10.0, 10.0}
        };
        
        int[] predictions = kmeans.predict(X_test);
        
        logger.info("Predictions:");
        for (int i = 0; i < X_test.length; i++) {
            System.out.printf("  Point [%.1f, %.1f] → Cluster %d%n",
                            X_test[i][0], X_test[i][1], predictions[i]);
        }
        logger.info("");
        
        // Example 4: Performance measurement
        logger.info("Example 4: Performance Measurement");
        logger.info(dash);
        
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
        
        logger.info("");
        logger.info(separator);
        logger.info("\nComplexity Summary:");
        logger.info("  Time:  O(n*k*d*i)");
        logger.info("  Space: O(n + k*d)");
        logger.info("\nKey Points:");
        logger.info("  + Simple and fast");
        logger.info("  + Works well for spherical clusters");
        logger.info("  + Scalable");
        logger.info("  - Requires knowing K");
        logger.info("  - Sensitive to initialization");
        logger.info("\nWhen to use:");
        logger.info("  • Know number of clusters");
        logger.info("  • Spherical clusters");
        logger.info("  • Large datasets");
        logger.info(separator);
        
        long endTime = System.nanoTime();
        double totalMs = (endTime - startTime) / 1_000_000.0;
        System.out.printf("\nTotal execution time: %.3f ms%n", totalMs);
    }
}