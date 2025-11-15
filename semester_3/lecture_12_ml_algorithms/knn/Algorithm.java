import java.util.*;

/**
 * K-Nearest Neighbors (KNN) implementation.
 * 
 * A simple, instance-based learning algorithm for classification.
 * 
 * Time Complexity:
 *   Training: O(1) - just stores data
 *   Prediction: O(n*d) per sample - n training samples, d dimensions
 * Space Complexity: O(n*d) - stores all training data
 */
public class Algorithm {
    
    /**
     * KNN Classifier class.
     */
    static class KNNClassifier {
        private int k;
        private List<double[]> xTrain;
        private List<Integer> yTrain;
        
        public KNNClassifier(int k) {
            this.k = k;
        }
        
        /**
         * Train the model (store training data).
         */
        public void fit(List<double[]> X, List<Integer> y) {
            this.xTrain = new ArrayList<>(X);
            this.yTrain = new ArrayList<>(y);
        }
        
        /**
         * Calculate Euclidean distance between two points.
         */
        private double euclideanDistance(double[] p1, double[] p2) {
            double sum = 0.0;
            for (int i = 0; i < p1.length; i++) {
                double diff = p1[i] - p2[i];
                sum += diff * diff;
            }
            return Math.sqrt(sum);
        }
        
        /**
         * Predict class for a single sample.
         */
        public int predictSingle(double[] x) {
            // Calculate distances to all training points
            List<DistanceLabel> distances = new ArrayList<>();
            for (int i = 0; i < xTrain.size(); i++) {
                double dist = euclideanDistance(x, xTrain.get(i));
                distances.add(new DistanceLabel(dist, yTrain.get(i)));
            }
            
            // Sort by distance
            Collections.sort(distances);
            
            // Get k nearest labels
            Map<Integer, Integer> votes = new HashMap<>();
            for (int i = 0; i < k && i < distances.size(); i++) {
                int label = distances.get(i).label;
                votes.put(label, votes.getOrDefault(label, 0) + 1);
            }
            
            // Find most common label
            int maxVotes = 0;
            int prediction = 0;
            for (Map.Entry<Integer, Integer> entry : votes.entrySet()) {
                if (entry.getValue() > maxVotes) {
                    maxVotes = entry.getValue();
                    prediction = entry.getKey();
                }
            }
            
            return prediction;
        }
        
        /**
         * Predict classes for multiple samples.
         */
        public List<Integer> predict(List<double[]> X) {
            List<Integer> predictions = new ArrayList<>();
            for (double[] x : X) {
                predictions.add(predictSingle(x));
            }
            return predictions;
        }
        
        /**
         * Calculate accuracy.
         */
        public double score(List<double[]> X, List<Integer> y) {
            List<Integer> predictions = predict(X);
            int correct = 0;
            for (int i = 0; i < predictions.size(); i++) {
                if (predictions.get(i).equals(y.get(i))) {
                    correct++;
                }
            }
            return (double) correct / y.size();
        }
    }
    
    /**
     * Helper class to store distance and label pairs.
     */
    static class DistanceLabel implements Comparable<DistanceLabel> {
        double distance;
        int label;
        
        DistanceLabel(double distance, int label) {
            this.distance = distance;
            this.label = label;
        }
        
        @Override
        public int compareTo(DistanceLabel other) {
            return Double.compare(this.distance, other.distance);
        }
    }
    
    /**
     * Main method for demonstration.
     */
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("K-NEAREST NEIGHBORS (KNN) DEMONSTRATION");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Example 1: Simple 2D classification
        System.out.println("Example 1: 2D Classification");
        System.out.println("-".repeat(70));
        
        // Training data
        List<double[]> xTrain = new ArrayList<>();
        List<Integer> yTrain = new ArrayList<>();
        
        // Class 0
        xTrain.add(new double[]{1.0, 1.0}); yTrain.add(0);
        xTrain.add(new double[]{1.5, 1.5}); yTrain.add(0);
        xTrain.add(new double[]{2.0, 2.0}); yTrain.add(0);
        xTrain.add(new double[]{1.2, 1.8}); yTrain.add(0);
        xTrain.add(new double[]{2.1, 1.9}); yTrain.add(0);
        
        // Class 1
        xTrain.add(new double[]{5.0, 5.0}); yTrain.add(1);
        xTrain.add(new double[]{5.5, 5.5}); yTrain.add(1);
        xTrain.add(new double[]{6.0, 6.0}); yTrain.add(1);
        xTrain.add(new double[]{5.2, 5.8}); yTrain.add(1);
        xTrain.add(new double[]{6.1, 5.9}); yTrain.add(1);
        
        // Test data
        List<double[]> xTest = new ArrayList<>();
        List<Integer> yTest = new ArrayList<>();
        xTest.add(new double[]{1.1, 1.2}); yTest.add(0);
        xTest.add(new double[]{5.8, 5.9}); yTest.add(1);
        xTest.add(new double[]{2.5, 2.5}); yTest.add(0);
        xTest.add(new double[]{5.0, 4.8}); yTest.add(1);
        
        // Train and predict
        KNNClassifier knn = new KNNClassifier(3);
        knn.fit(xTrain, yTrain);
        
        List<Integer> predictions = knn.predict(xTest);
        double accuracy = knn.score(xTest, yTest);
        
        System.out.println("Training samples: " + xTrain.size());
        System.out.println("Test samples: " + xTest.size());
        System.out.println("k = " + knn.k);
        System.out.println();
        System.out.println("Predictions:");
        for (int i = 0; i < xTest.size(); i++) {
            double[] x = xTest.get(i);
            int pred = predictions.get(i);
            int truth = yTest.get(i);
            String match = pred == truth ? "✓" : "✗";
            System.out.printf("  %d. [%.1f, %.1f] → Predicted: %d, " +
                            "True: %d %s%n", 
                            i + 1, x[0], x[1], pred, truth, match);
        }
        System.out.printf("%nAccuracy: %.0f%%%n%n", accuracy * 100);
        
        // Example 2: Effect of k
        System.out.println("Example 2: Effect of Different k Values");
        System.out.println("-".repeat(70));
        
        for (int k : new int[]{1, 3, 5, 7}) {
            KNNClassifier knnK = new KNNClassifier(k);
            knnK.fit(xTrain, yTrain);
            double acc = knnK.score(xTest, yTest);
            System.out.printf("k=%d: Accuracy = %.0f%%%n", k, acc * 100);
        }
        System.out.println();
        
        long endTime = System.nanoTime();
        double durationMs = (endTime - startTime) / 1_000_000.0;
        
        System.out.println("=".repeat(70));
        System.out.println("\nComplexity Summary:");
        System.out.println("  Training Time:  O(1) - just stores data");
        System.out.println("  Prediction Time: O(n*d) per sample");
        System.out.println("  Space: O(n*d) - stores all training data");
        System.out.println("\nKey Points:");
        System.out.println("  - No training phase (lazy learning)");
        System.out.println("  - Slow prediction for large datasets");
        System.out.println("  - Sensitive to feature scaling");
        System.out.println("  - Works well for small datasets");
        System.out.println("=".repeat(70));
        System.out.printf("%nTotal execution time: %.3f ms%n", durationMs);
    }
}
