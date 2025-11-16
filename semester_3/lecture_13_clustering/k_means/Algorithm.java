import java.util.Arrays;
import java.util.Random;

/**
 * K-Means Clustering implementation.
 * 
 * Unsupervised learning for partitioning data into K clusters.
 * 
 * Time Complexity: O(n*k*d*iter)
 * Space Complexity: O(n + k*d)
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    static class KMeans {
        private int nClusters;
        private int maxIterations;
        private double[][] centroids;
        private int[] labels;
        private double inertia;
        private int nIter;
        private Random random;
        
        KMeans(int nClusters, int maxIterations, int randomState) {
            this.nClusters = nClusters;
            this.maxIterations = maxIterations;
            this.random = new Random(randomState);
        }
        
        void fit(double[][] X) {
            int nSamples = X.length;
            int nFeatures = X[0].length;
            
            // Initialize centroids randomly
            initializeCentroids(X);
            labels = new int[nSamples];
            
            // Iterate
            for (int iter = 0; iter < maxIterations; iter++) {
                int[] oldLabels = labels.clone();
                
                // Assign clusters
                assignClusters(X);
                
                // Update centroids
                updateCentroids(X);
                
                // Check convergence
                if (Arrays.equals(labels, oldLabels)) {
                    nIter = iter + 1;
                    break;
                }
                nIter = iter + 1;
            }
            
            // Calculate inertia
            calculateInertia(X);
        }
        
        private void initializeCentroids(double[][] X) {
            int nSamples = X.length;
            int nFeatures = X[0].length;
            centroids = new double[nClusters][nFeatures];
            
            // Random initialization
            boolean[] selected = new boolean[nSamples];
            for (int i = 0; i < nClusters; i++) {
                int idx;
                do {
                    idx = random.nextInt(nSamples);
                } while (selected[idx]);
                selected[idx] = true;
                centroids[i] = X[idx].clone();
            }
        }
        
        private void assignClusters(double[][] X) {
            for (int i = 0; i < X.length; i++) {
                double minDist = Double.MAX_VALUE;
                int closestCluster = 0;
                
                for (int j = 0; j < nClusters; j++) {
                    double dist = euclideanDistance(X[i], centroids[j]);
                    if (dist < minDist) {
                        minDist = dist;
                        closestCluster = j;
                    }
                }
                
                labels[i] = closestCluster;
            }
        }
        
        private void updateCentroids(double[][] X) {
            int nFeatures = X[0].length;
            double[][] newCentroids = new double[nClusters][nFeatures];
            int[] counts = new int[nClusters];
            
            // Sum points in each cluster
            for (int i = 0; i < X.length; i++) {
                int cluster = labels[i];
                counts[cluster]++;
                for (int j = 0; j < nFeatures; j++) {
                    newCentroids[cluster][j] += X[i][j];
                }
            }
            
            // Calculate means
            for (int i = 0; i < nClusters; i++) {
                if (counts[i] > 0) {
                    for (int j = 0; j < nFeatures; j++) {
                        centroids[i][j] = newCentroids[i][j] / counts[i];
                    }
                }
            }
        }
        
        private void calculateInertia(double[][] X) {
            inertia = 0;
            for (int i = 0; i < X.length; i++) {
                double dist = euclideanDistance(X[i], 
                                               centroids[labels[i]]);
                inertia += dist * dist;
            }
        }
        
        private double euclideanDistance(double[] a, double[] b) {
            double sum = 0;
            for (int i = 0; i < a.length; i++) {
                sum += Math.pow(a[i] - b[i], 2);
            }
            return Math.sqrt(sum);
        }
        
        int[] predict(double[][] X) {
            int[] predictions = new int[X.length];
            
            for (int i = 0; i < X.length; i++) {
                double minDist = Double.MAX_VALUE;
                int closestCluster = 0;
                
                for (int j = 0; j < nClusters; j++) {
                    double dist = euclideanDistance(X[i], centroids[j]);
                    if (dist < minDist) {
                        minDist = dist;
                        closestCluster = j;
                    }
                }
                
                predictions[i] = closestCluster;
            }
            
            return predictions;
        }
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        logger.info("=".repeat(70));
        logger.info("K-MEANS CLUSTERING DEMONSTRATION");
        logger.info("=".repeat(70));
        logger.info();
        
        // Example 1: Simple clustering
        logger.info("Example 1: Simple 2D Clustering");
        logger.info("-".repeat(70));
        
        Random rand = new Random(42);
        int n = 90;
        double[][] X = new double[n][2];
        
        // Generate 3 clusters
        for (int i = 0; i < 30; i++) {
            X[i][0] = 5 + rand.nextGaussian();
            X[i][1] = 5 + rand.nextGaussian();
        }
        for (int i = 30; i < 60; i++) {
            X[i][0] = rand.nextGaussian();
            X[i][1] = rand.nextGaussian();
        }
        for (int i = 60; i < 90; i++) {
            X[i][0] = 5 + rand.nextGaussian();
            X[i][1] = rand.nextGaussian();
        }
        
        KMeans kmeans = new KMeans(3, 300, 42);
        kmeans.fit(X);
        
        System.out.printf("Converged in %d iterations%n", kmeans.nIter);
        System.out.printf("Inertia: %.2f%n", kmeans.inertia);
        
        logger.info("\nCentroids:");
        for (int i = 0; i < kmeans.centroids.length; i++) {
            System.out.printf("  Cluster %d: [%.2f, %.2f]%n",
                            i, kmeans.centroids[i][0], 
                            kmeans.centroids[i][1]);
        }
        
        logger.info("\nCluster sizes:");
        int[] counts = new int[3];
        for (int label : kmeans.labels) {
            counts[label]++;
        }
        for (int i = 0; i < 3; i++) {
            System.out.printf("  Cluster %d: %d points%n", i, counts[i]);
        }
        logger.info();
        
        // Example 2: Prediction
        logger.info("Example 2: Predicting New Points");
        logger.info("-".repeat(70));
        
        double[][] newPoints = {
            {5.5, 5.5},
            {0.5, 0.5},
            {5.5, 0.5}
        };
        
        int[] predictions = kmeans.predict(newPoints);
        
        for (int i = 0; i < newPoints.length; i++) {
            System.out.printf("Point [%.1f, %.1f] → Cluster %d%n",
                            newPoints[i][0], newPoints[i][1], 
                            predictions[i]);
        }
        logger.info();
        
        long endTime = System.nanoTime();
        
        logger.info("=".repeat(70));
        logger.info("\nComplexity Summary:");
        logger.info("  Time:  O(n*k*d*iter)");
        logger.info("  Space: O(n + k*d)");
        logger.info("\nKey Advantages:");
        logger.info("  - Simple and fast");
        logger.info("  - Scales well");
        logger.info("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
