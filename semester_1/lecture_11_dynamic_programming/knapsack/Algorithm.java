import java.util.*;

/**
 * 0/1 Knapsack Problem - Dynamic Programming.
 * 
 * Time Complexity: O(n * capacity)
 * Space Complexity: O(n * capacity) or O(capacity) optimized
 */
public class Algorithm {
    
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
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("0/1 KNAPSACK PROBLEM DEMONSTRATION");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Example 1
        System.out.println("Example 1: Basic 0/1 Knapsack");
        System.out.println("-".repeat(70));
        
        int[] weights1 = {10, 20, 30};
        int[] values1 = {60, 100, 120};
        int capacity1 = 50;
        
        KnapsackResult result = knapsack01(weights1, values1, capacity1);
        
        System.out.println("Weights: " + Arrays.toString(weights1));
        System.out.println("Values: " + Arrays.toString(values1));
        System.out.println("Capacity: " + capacity1);
        System.out.println("Maximum value: " + result.maxValue);
        System.out.println("Selected items: " + result.selectedItems);
        System.out.println();
        
        // Example 2
        System.out.println("Example 2: Space-Optimized Version");
        System.out.println("-".repeat(70));
        
        int[] weights2 = {1, 3, 4, 5};
        int[] values2 = {1, 4, 5, 7};
        int capacity2 = 7;
        
        int valueStandard = knapsack01(weights2, values2, capacity2).maxValue;
        int valueOptimized = knapsack01Optimized(weights2, values2, capacity2);
        
        System.out.println("Weights: " + Arrays.toString(weights2));
        System.out.println("Values: " + Arrays.toString(values2));
        System.out.println("Capacity: " + capacity2);
        System.out.println("Max value (standard): " + valueStandard);
        System.out.println("Max value (optimized): " + valueOptimized);
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nComplexity Summary:");
        System.out.println("  Time:  O(n * capacity)");
        System.out.println("  Space: O(n * capacity) or O(capacity)");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}

