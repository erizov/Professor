/**
package semester_03.lecture_12_ml_algorithms.linear_regression;
 * Linear Regression implementation.
 * 
 * Models linear relationship between variables.
 * 
 * Time Complexity: O(n*d*iter) for gradient descent
 * Space Complexity: O(d) where d is number of features
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    static class LinearRegression {
        private double[] weights;
        private double bias;
        private double learningRate;
        private int nIterations;
        
        LinearRegression(double learningRate, int nIterations) {
            this.learningRate = learningRate;
            this.nIterations = nIterations;
        }
        
        void fit(double[][] X, double[] y) {
            int nSamples = X.length;
            int nFeatures = X[0].length;
            
            // Initialize parameters
            weights = new double[nFeatures];
            bias = 0;
            
            // Gradient descent
            for (int iter = 0; iter < nIterations; iter++) {
                // Predictions
                double[] yPred = new double[nSamples];
                for (int i = 0; i < nSamples; i++) {
                    yPred[i] = bias;
                    for (int j = 0; j < nFeatures; j++) {
                        yPred[i] += weights[j] * X[i][j];
                    }
                }
                
                // Calculate gradients
                double[] dw = new double[nFeatures];
                double db = 0;
                
                for (int i = 0; i < nSamples; i++) {
                    double error = y[i] - yPred[i];
                    for (int j = 0; j < nFeatures; j++) {
                        dw[j] += error * X[i][j];
                    }
                    db += error;
                }
                
                // Update parameters
                for (int j = 0; j < nFeatures; j++) {
                    weights[j] += learningRate * (2.0 / nSamples) * dw[j];
                }
                bias += learningRate * (2.0 / nSamples) * db;
            }
        }
        
        double[] predict(double[][] X) {
            int nSamples = X.length;
            int nFeatures = X[0].length;
            double[] predictions = new double[nSamples];
            
            for (int i = 0; i < nSamples; i++) {
                predictions[i] = bias;
                for (int j = 0; j < nFeatures; j++) {
                    predictions[i] += weights[j] * X[i][j];
                }
            }
            
            return predictions;
        }
        
        double score(double[][] X, double[] y) {
            double[] yPred = predict(X);
            
            double ssRes = 0;
            double ssTot = 0;
            double yMean = 0;
            
            // Calculate mean
            for (double val : y) {
                yMean += val;
            }
            yMean /= y.length;
            
            // Calculate SS
            for (int i = 0; i < y.length; i++) {
                ssRes += Math.pow(y[i] - yPred[i], 2);
                ssTot += Math.pow(y[i] - yMean, 2);
            }
            
            return 1 - (ssRes / ssTot);
        }
    }
    
    public static void main(String[] args) {
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        long startTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("LINEAR REGRESSION DEMONSTRATION");
        logger.info(separator);
        logger.info("");
        
        // Example 1: Simple regression
        logger.info("Example 1: Simple Linear Regression");
        logger.info(dash);
        
        // Generate data: y = 3x + 5
        int n = 100;
        double[][] X = new double[n][1];
        double[] y = new double[n];
        
        for (int i = 0; i < n; i++) {
            X[i][0] = Math.random() * 10;
            y[i] = 3 * X[i][0] + 5 + (Math.random() - 0.5) * 2;
        }
        
        LinearRegression model = new LinearRegression(0.01, 1000);
        model.fit(X, y);
        
        logger.info("True equation: y = 3x + 5");
        System.out.printf("Learned: y = %.2fx + %.2f%n", 
                        model.weights[0], model.bias);
        System.out.printf("R² score: %.4f%n", model.score(X, y));
        logger.info("");
        
        // Example 2: Multiple regression
        logger.info("Example 2: Multiple Linear Regression");
        logger.info(dash);
        
        double[][] X2 = new double[n][3];
        double[] y2 = new double[n];
        
        for (int i = 0; i < n; i++) {
            X2[i][0] = Math.random() * 10;
            X2[i][1] = Math.random() * 10;
            X2[i][2] = Math.random() * 10;
            y2[i] = 2 * X2[i][0] + 3 * X2[i][1] - 
                    X2[i][2] + 10;
        }
        
        LinearRegression model2 = new LinearRegression(0.01, 1000);
        model2.fit(X2, y2);
        
        logger.info("True: y = 2x + 3x - 1x + 10");
        System.out.printf("Learned: y = %.2fx + %.2fx + %.2fx + %.2f%n",
                        model2.weights[0], model2.weights[1],
                        model2.weights[2], model2.bias);
        System.out.printf("R² score: %.4f%n", model2.score(X2, y2));
        logger.info("");
        
        long endTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("\nComplexity Summary:");
        logger.info("  Time:  O(n*d*iter)");
        logger.info("  Space: O(d)");
        logger.info("\nKey Advantages:");
        logger.info("  - Simple and interpretable");
        logger.info("  - Fast training");
        logger.info(separator);
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}