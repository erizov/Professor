/**
 * Logistic Regression implementation.
 * 
 * Binary classification using sigmoid function.
 * 
 * Time Complexity: O(n*d*iter)
 * Space Complexity: O(d)
 */
public class Algorithm {
    
    static class LogisticRegression {
        private double[] weights;
        private double bias;
        private double learningRate;
        private int nIterations;
        
        LogisticRegression(double learningRate, int nIterations) {
            this.learningRate = learningRate;
            this.nIterations = nIterations;
        }
        
        private double sigmoid(double z) {
            return 1.0 / (1.0 + Math.exp(-Math.max(-500, Math.min(500, z))));
        }
        
        void fit(double[][] X, int[] y) {
            int nSamples = X.length;
            int nFeatures = X[0].length;
            
            // Initialize
            weights = new double[nFeatures];
            bias = 0;
            
            // Gradient descent
            for (int iter = 0; iter < nIterations; iter++) {
                // Predictions
                double[] yPred = new double[nSamples];
                for (int i = 0; i < nSamples; i++) {
                    double z = bias;
                    for (int j = 0; j < nFeatures; j++) {
                        z += weights[j] * X[i][j];
                    }
                    yPred[i] = sigmoid(z);
                }
                
                // Calculate gradients
                double[] dw = new double[nFeatures];
                double db = 0;
                
                for (int i = 0; i < nSamples; i++) {
                    double error = yPred[i] - y[i];
                    for (int j = 0; j < nFeatures; j++) {
                        dw[j] += error * X[i][j];
                    }
                    db += error;
                }
                
                // Update parameters
                for (int j = 0; j < nFeatures; j++) {
                    weights[j] -= learningRate * dw[j] / nSamples;
                }
                bias -= learningRate * db / nSamples;
            }
        }
        
        double[] predictProba(double[][] X) {
            int nSamples = X.length;
            int nFeatures = X[0].length;
            double[] probas = new double[nSamples];
            
            for (int i = 0; i < nSamples; i++) {
                double z = bias;
                for (int j = 0; j < nFeatures; j++) {
                    z += weights[j] * X[i][j];
                }
                probas[i] = sigmoid(z);
            }
            
            return probas;
        }
        
        int[] predict(double[][] X) {
            double[] probas = predictProba(X);
            int[] predictions = new int[probas.length];
            
            for (int i = 0; i < probas.length; i++) {
                predictions[i] = probas[i] >= 0.5 ? 1 : 0;
            }
            
            return predictions;
        }
        
        double score(double[][] X, int[] y) {
            int[] yPred = predict(X);
            int correct = 0;
            
            for (int i = 0; i < y.length; i++) {
                if (yPred[i] == y[i]) {
                    correct++;
                }
            }
            
            return (double) correct / y.length;
        }
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("LOGISTIC REGRESSION DEMONSTRATION");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Example 1: Binary classification
        System.out.println("Example 1: Binary Classification");
        System.out.println("-".repeat(70));
        
        int n = 100;
        double[][] X = new double[n][2];
        int[] y = new int[n];
        
        // Generate data
        for (int i = 0; i < n / 2; i++) {
            X[i][0] = 2 + Math.random();
            X[i][1] = 2 + Math.random();
            y[i] = 0;
        }
        for (int i = n / 2; i < n; i++) {
            X[i][0] = -2 + Math.random();
            X[i][1] = -2 + Math.random();
            y[i] = 1;
        }
        
        LogisticRegression model = new LogisticRegression(0.1, 1000);
        model.fit(X, y);
        
        System.out.printf("Accuracy: %.4f%n", model.score(X, y));
        System.out.print("Weights: [");
        for (int i = 0; i < model.weights.length; i++) {
            System.out.printf("%.4f", model.weights[i]);
            if (i < model.weights.length - 1) System.out.print(", ");
        }
        System.out.println("]");
        System.out.printf("Bias: %.4f%n", model.bias);
        System.out.println();
        
        // Example 2: Probability predictions
        System.out.println("Example 2: Probability Predictions");
        System.out.println("-".repeat(70));
        
        double[][] testSamples = {
            {3, 3},
            {-3, -3},
            {0, 0}
        };
        
        double[] probas = model.predictProba(testSamples);
        int[] predictions = model.predict(testSamples);
        
        for (int i = 0; i < testSamples.length; i++) {
            System.out.printf("Sample [%.1f, %.1f]:%n", 
                            testSamples[i][0], testSamples[i][1]);
            System.out.printf("  P(class=1) = %.4f%n", probas[i]);
            System.out.printf("  Predicted class: %d%n", predictions[i]);
        }
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nComplexity Summary:");
        System.out.println("  Time:  O(n*d*iter)");
        System.out.println("  Space: O(d)");
        System.out.println("\nKey Advantages:");
        System.out.println("  - Probabilistic predictions");
        System.out.println("  - Interpretable");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
