/**
 * Support Vector Machine (SVM) implementation.
 * 
 * Binary classifier with maximum margin.
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    static class SVM {
        private double[] weights;
        private double bias;
        private double learningRate;
        private double lambdaParam;
        private int nIterations;
        
        SVM(double learningRate, double lambdaParam, int nIterations) {
            this.learningRate = learningRate;
            this.lambdaParam = lambdaParam;
            this.nIterations = nIterations;
        }
        
        void fit(double[][] X, int[] y) {
            int nSamples = X.length;
            int nFeatures = X[0].length;
            
            // Convert labels to -1 and 1
            int[] y_ = new int[nSamples];
            for (int i = 0; i < nSamples; i++) {
                y_[i] = y[i] <= 0 ? -1 : 1;
            }
            
            // Initialize
            weights = new double[nFeatures];
            bias = 0;
            
            // Gradient descent
            for (int iter = 0; iter < nIterations; iter++) {
                for (int idx = 0; idx < nSamples; idx++) {
                    double dotProduct = 0;
                    for (int j = 0; j < nFeatures; j++) {
                        dotProduct += X[idx][j] * weights[j];
                    }
                    
                    double condition = y_[idx] * (dotProduct - bias);
                    
                    if (condition >= 1) {
                        // Update with regularization
                        for (int j = 0; j < nFeatures; j++) {
                            weights[j] -= learningRate * 
                                         (2 * lambdaParam * weights[j]);
                        }
                    } else {
                        // Update with loss
                        for (int j = 0; j < nFeatures; j++) {
                            weights[j] -= learningRate * (
                                2 * lambdaParam * weights[j] - 
                                X[idx][j] * y_[idx]
                            );
                        }
                        bias -= learningRate * y_[idx];
                    }
                }
            }
        }
        
        int[] predict(double[][] X) {
            int nSamples = X.length;
            int nFeatures = X[0].length;
            int[] predictions = new int[nSamples];
            
            for (int i = 0; i < nSamples; i++) {
                double dotProduct = 0;
                for (int j = 0; j < nFeatures; j++) {
                    dotProduct += X[i][j] * weights[j];
                }
                predictions[i] = (dotProduct - bias) >= 0 ? 1 : -1;
            }
            
            return predictions;
        }
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        logger.info("=".repeat(70));
        logger.info("SUPPORT VECTOR MACHINE (SVM) DEMONSTRATION");
        logger.info("=".repeat(70));
        logger.info();
        
        // Example
        logger.info("Example: Basic SVM");
        logger.info("-".repeat(70));
        
        double[][] X = {
            {1, 1}, {2, 2}, {3, 3},
            {-1, -1}, {-2, -2}, {-3, -3}
        };
        int[] y = {1, 1, 1, -1, -1, -1};
        
        SVM svm = new SVM(0.01, 0.01, 1000);
        svm.fit(X, y);
        
        int[] predictions = svm.predict(X);
        int correct = 0;
        for (int i = 0; i < y.length; i++) {
            if (predictions[i] == y[i]) correct++;
        }
        
        logger.info("Accuracy: " + (double)correct / y.length);
        logger.info();
        
        long endTime = System.nanoTime();
        
        logger.info("=".repeat(70));
        logger.info("\nComplexity Summary:");
        logger.info("  Training: O(n*d*iter)");
        logger.info("  Prediction: O(d)");
        logger.info("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
