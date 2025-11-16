import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;
import java.util.stream.Collectors;

/**
 * Decision Tree Classifier implementation.
 * 
 * Time Complexity: O(n*d*log(n)) training
 * Space Complexity: O(n) for tree
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    static class Node {
        Integer feature;
        Double threshold;
        Node left;
        Node right;
        Integer value;
        
        Node(Integer value) {
            this.value = value;
        }
        
        Node(int feature, double threshold, Node left, Node right) {
            this.feature = feature;
            this.threshold = threshold;
            this.left = left;
            this.right = right;
        }
    }
    
    static class DecisionTreeClassifier {
        int maxDepth;
        int minSamplesSplit;
        Node root;
        
        DecisionTreeClassifier(int maxDepth, int minSamplesSplit) {
            this.maxDepth = maxDepth;
            this.minSamplesSplit = minSamplesSplit;
        }
        
        void fit(double[][] X, int[] y) {
            root = growTree(X, y, 0);
        }
        
        private Node growTree(double[][] X, int[] y, int depth) {
            int nSamples = y.length;
            
            // Stopping criteria
            if (depth >= maxDepth || nSamples < minSamplesSplit || 
                isHomogeneous(y)) {
                return new Node(majorityClass(y));
            }
            
            // Find best split
            int[] bestSplit = bestSplit(X, y);
            if (bestSplit == null) {
                return new Node(majorityClass(y));
            }
            
            int bestFeature = bestSplit[0];
            double bestThreshold = Double.longBitsToDouble(
                ((long)bestSplit[1] << 32) | (bestSplit[2] & 0xFFFFFFFFL));
            
            // Split data
            List<Integer> leftIndices = new ArrayList<>();
            List<Integer> rightIndices = new ArrayList<>();
            
            for (int i = 0; i < nSamples; i++) {
                if (X[i][bestFeature] < bestThreshold) {
                    leftIndices.add(i);
                } else {
                    rightIndices.add(i);
                }
            }
            
            // Build subtrees
            double[][] leftX = new double[leftIndices.size()][];
            int[] leftY = new int[leftIndices.size()];
            for (int i = 0; i < leftIndices.size(); i++) {
                leftX[i] = X[leftIndices.get(i)];
                leftY[i] = y[leftIndices.get(i)];
            }
            
            double[][] rightX = new double[rightIndices.size()][];
            int[] rightY = new int[rightIndices.size()];
            for (int i = 0; i < rightIndices.size(); i++) {
                rightX[i] = X[rightIndices.get(i)];
                rightY[i] = y[rightIndices.get(i)];
            }
            
            Node left = growTree(leftX, leftY, depth + 1);
            Node right = growTree(rightX, rightY, depth + 1);
            
            return new Node(bestFeature, bestThreshold, left, right);
        }
        
        private boolean isHomogeneous(int[] y) {
            if (y.length == 0) return true;
            int first = y[0];
            for (int val : y) {
                if (val != first) return false;
            }
            return true;
        }
        
        private int majorityClass(int[] y) {
            if (y.length == 0) return 0;
            Map<Integer, Integer> counts = new HashMap<>();
            for (int val : y) {
                counts.put(val, counts.getOrDefault(val, 0) + 1);
            }
            return counts.entrySet().stream()
                    .max(Map.Entry.comparingByValue())
                    .get().getKey();
        }
        
        private int[] bestSplit(double[][] X, int[] y) {
            if (X.length == 0) return null;
            
            double bestGini = Double.MAX_VALUE;
            int bestFeature = -1;
            double bestThreshold = 0;
            
            int nFeatures = X[0].length;
            
            for (int feature = 0; feature < nFeatures; feature++) {
                Set<Double> uniqueVals = new HashSet<>();
                for (double[] row : X) {
                    uniqueVals.add(row[feature]);
                }
                List<Double> sorted = new ArrayList<>(uniqueVals);
                java.util.Collections.sort(sorted);
                
                for (int i = 0; i < sorted.size() - 1; i++) {
                    double threshold = (sorted.get(i) + sorted.get(i + 1)) / 2;
                    
                    List<Integer> leftY = new ArrayList<>();
                    List<Integer> rightY = new ArrayList<>();
                    
                    for (int j = 0; j < X.length; j++) {
                        if (X[j][feature] < threshold) {
                            leftY.add(y[j]);
                        } else {
                            rightY.add(y[j]);
                        }
                    }
                    
                    if (leftY.isEmpty() || rightY.isEmpty()) continue;
                    
                    double gini = (double)leftY.size() / y.length * 
                                 giniImpurity(leftY) +
                                 (double)rightY.size() / y.length *
                                 giniImpurity(rightY);
                    
                    if (gini < bestGini) {
                        bestGini = gini;
                        bestFeature = feature;
                        bestThreshold = threshold;
                    }
                }
            }
            
            if (bestFeature == -1) return null;
            
            long bits = Double.doubleToLongBits(bestThreshold);
            return new int[]{bestFeature, (int)(bits >> 32), (int)bits};
        }
        
        private double giniImpurity(List<Integer> y) {
            if (y.isEmpty()) return 0;
            
            Map<Integer, Long> counts = y.stream()
                    .collect(Collectors.groupingBy(e -> e, Collectors.counting()));
            
            double impurity = 1.0;
            for (long count : counts.values()) {
                double prob = (double)count / y.size();
                impurity -= prob * prob;
            }
            
            return impurity;
        }
        
        int[] predict(double[][] X) {
            int[] predictions = new int[X.length];
            for (int i = 0; i < X.length; i++) {
                predictions[i] = traverse(X[i], root);
            }
            return predictions;
        }
        
        private int traverse(double[] x, Node node) {
            if (node.value != null) {
                return node.value;
            }
            
            if (x[node.feature] < node.threshold) {
                return traverse(x, node.left);
            } else {
                return traverse(x, node.right);
            }
        }
        
        double score(double[][] X, int[] y) {
            int[] predictions = predict(X);
            int correct = 0;
            for (int i = 0; i < y.length; i++) {
                if (predictions[i] == y[i]) correct++;
            }
            return (double)correct / y.length;
        }
    }
    
    public static void main(String[] args) {
        logger.info("=".repeat(70));
        logger.info("DECISION TREE CLASSIFIER DEMONSTRATION");
        logger.info("=".repeat(70));
        logger.info();
        
        // Generate data
        Random rand = new Random(42);
        int n = 80;
        double[][] X = new double[n][2];
        int[] y = new int[n];
        
        for (int i = 0; i < n/2; i++) {
            X[i][0] = rand.nextDouble() * 3;
            X[i][1] = rand.nextDouble() * 3;
            y[i] = 0;
        }
        
        for (int i = n/2; i < n; i++) {
            X[i][0] = 4 + rand.nextDouble() * 3;
            X[i][1] = 4 + rand.nextDouble() * 3;
            y[i] = 1;
        }
        
        logger.info("Generated " + n + " training samples");
        logger.info();
        
        // Train
        DecisionTreeClassifier tree = 
            new DecisionTreeClassifier(5, 2);
        tree.fit(X, y);
        
        double accuracy = tree.score(X, y);
        System.out.printf("Training Accuracy: %.4f%n", accuracy);
        logger.info();
        
        // Predictions
        double[][] X_test = {{1.0, 1.0}, {6.0, 6.0}, {3.5, 3.5}};
        int[] predictions = tree.predict(X_test);
        
        logger.info("Predictions:");
        for (int i = 0; i < X_test.length; i++) {
            System.out.printf("  [%.1f, %.1f] → Class %d%n",
                            X_test[i][0], X_test[i][1], predictions[i]);
        }
        
        logger.info();
        logger.info("=".repeat(70));
        logger.info("\nComplexity: O(n*d*log(n)) training");
        logger.info("Space: O(n)");
        logger.info("\nKey Points:");
        logger.info("  + Interpretable");
        logger.info("  + No scaling needed");
        logger.info("  + Handles non-linear");
        logger.info("  - Can overfit");
        logger.info("=".repeat(70));
    }
}