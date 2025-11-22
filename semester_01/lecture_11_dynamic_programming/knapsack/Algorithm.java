// package semester_01.lecture_11_dynamic_programming.knapsack;

import java.util.*;

/**
 * 0/1 Knapsack Problem - Dynamic Programming.
 * 
 * Time Complexity: O(n * capacity)
 * Space Complexity: O(n * capacity) or O(capacity) optimized
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    static class KnapsackResult {
        int maxValue;
        List<Integer> selectedItems;
        
        KnapsackResult(int maxValue, List<Integer> selectedItems) {
            this.maxValue = maxValue;
            this.selectedItems = selectedItems;
        }
    }
    
    static KnapsackResult knapsack01(int[] weights, int[] values, 
                                     int capacity) {
        int n = weights.length;
        int[][] dp = new int[n + 1][capacity + 1];
        
        // Build DP table
        for (int i = 1; i <= n; i++) {
            for (int w = 0; w <= capacity; w++) {
                dp[i][w] = dp[i - 1][w]; // Don't take item i
                
                if (weights[i - 1] <= w) {
                    dp[i][w] = Math.max(dp[i][w],
                                       dp[i - 1][w - weights[i - 1]] + 
                                       values[i - 1]);
                }
            }
        }
        
        // Reconstruct solution
        List<Integer> selected = new ArrayList<>();
        int w = capacity;
        
        for (int i = n; i > 0; i--) {
            if (dp[i][w] != dp[i - 1][w]) {
                selected.add(i - 1);
                w -= weights[i - 1];
            }
        }
        
        Collections.reverse(selected);
        return new KnapsackResult(dp[n][capacity], selected);
    }
    
    static int knapsack01Optimized(int[] weights, int[] values, 
                                   int capacity) {
        int n = weights.length;
        int[] dp = new int[capacity + 1];
        
        for (int i = 0; i < n; i++) {
            for (int w = capacity; w >= weights[i]; w--) {
                dp[w] = Math.max(dp[w], dp[w - weights[i]] + values[i]);
            }
        }
        
        return dp[capacity];
    }
    
    public static void main(String[] args) {
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        long startTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("0/1 KNAPSACK PROBLEM DEMONSTRATION");
        logger.info(separator);
        logger.info("");
        
        // Example 1
        logger.info("Example 1: Basic 0/1 Knapsack");
        logger.info(dash);
        
        int[] weights1 = {10, 20, 30};
        int[] values1 = {60, 100, 120};
        int capacity1 = 50;
        
        KnapsackResult result = knapsack01(weights1, values1, capacity1);
        
        logger.info("Weights: " + Arrays.toString(weights1));
        logger.info("Values: " + Arrays.toString(values1));
        logger.info("Capacity: " + capacity1);
        logger.info("Maximum value: " + result.maxValue);
        logger.info("Selected items: " + result.selectedItems);
        logger.info("");
        
        // Example 2
        logger.info("Example 2: Space-Optimized Version");
        logger.info(dash);
        
        int[] weights2 = {1, 3, 4, 5};
        int[] values2 = {1, 4, 5, 7};
        int capacity2 = 7;
        
        int valueStandard = knapsack01(weights2, values2, capacity2).maxValue;
        int valueOptimized = knapsack01Optimized(weights2, values2, capacity2);
        
        logger.info("Weights: " + Arrays.toString(weights2));
        logger.info("Values: " + Arrays.toString(values2));
        logger.info("Capacity: " + capacity2);
        logger.info("Max value (standard): " + valueStandard);
        logger.info("Max value (optimized): " + valueOptimized);
        logger.info("");
        
        long endTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("\nComplexity Summary:");
        logger.info("  Time:  O(n * capacity)");
        logger.info("  Space: O(n * capacity) or O(capacity)");
        logger.info(separator);
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
