import java.util.*;

/**
 * Fibonacci Sequence - Dynamic Programming.
 * 
 * Multiple approaches: naive, memoized, bottom-up, optimized.
 */
public class Algorithm {
    
    // Naive recursive (exponential time)
    static int fibonacciNaive(int n) {
        if (n <= 1) return n;
        return fibonacciNaive(n - 1) + fibonacciNaive(n - 2);
    }
    
    // Memoized (top-down DP)
    static int fibonacciMemoized(int n, Map<Integer, Integer> memo) {
        if (memo == null) {
            memo = new HashMap<>();
        }
        
        if (memo.containsKey(n)) {
            return memo.get(n);
        }
        
        if (n <= 1) {
            return n;
        }
        
        int result = fibonacciMemoized(n - 1, memo) + 
                     fibonacciMemoized(n - 2, memo);
        memo.put(n, result);
        return result;
    }
    
    // Bottom-up DP
    static int fibonacciBottomUp(int n) {
        if (n <= 1) return n;
        
        int[] dp = new int[n + 1];
        dp[0] = 0;
        dp[1] = 1;
        
        for (int i = 2; i <= n; i++) {
            dp[i] = dp[i - 1] + dp[i - 2];
        }
        
        return dp[n];
    }
    
    // Space-optimized (O(1) space)
    static int fibonacciOptimized(int n) {
        if (n <= 1) return n;
        
        int prev2 = 0;  // F(0)
        int prev1 = 1;  // F(1)
        
        for (int i = 2; i <= n; i++) {
            int current = prev1 + prev2;
            prev2 = prev1;
            prev1 = current;
        }
        
        return prev1;
    }
    
    // Generate sequence
    static List<Long> fibonacciSequence(int n, String method) {
        List<Long> sequence = new ArrayList<>();
        
        for (int i = 0; i < n; i++) {
            long value;
            switch (method) {
                case "optimized":
                    value = fibonacciOptimized(i);
                    break;
                case "bottom_up":
                    value = fibonacciBottomUp(i);
                    break;
                case "memoized":
                    value = fibonacciMemoized(i, new HashMap<>());
                    break;
                default:
                    value = fibonacciOptimized(i);
            }
            sequence.add(value);
        }
        
        return sequence;
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("FIBONACCI SEQUENCE - DYNAMIC PROGRAMMING");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Example 1: Compare approaches
        System.out.println("Example 1: Comparing Different Approaches");
        System.out.println("-".repeat(70));
        
        int n = 10;
        System.out.println("Computing Fibonacci(" + n + "):");
        System.out.println("  Naive recursive: " + fibonacciNaive(n));
        System.out.println("  Memoized: " + 
                         fibonacciMemoized(n, new HashMap<>()));
        System.out.println("  Bottom-up DP: " + fibonacciBottomUp(n));
        System.out.println("  Optimized: " + fibonacciOptimized(n));
        System.out.println();
        
        // Example 2: Performance
        System.out.println("Example 2: Performance Comparison");
        System.out.println("-".repeat(70));
        
        int[] testValues = {20, 30, 35};
        
        for (int nVal : testValues) {
            System.out.println("\nComputing Fibonacci(" + nVal + "):");
            
            // Naive (only for small n)
            if (nVal <= 30) {
                long t1 = System.nanoTime();
                fibonacciNaive(nVal);
                long t2 = System.nanoTime();
                System.out.printf("  Naive: %.3f ms%n", 
                                (t2 - t1) / 1_000_000.0);
            }
            
            // Memoized
            long t1 = System.nanoTime();
            fibonacciMemoized(nVal, new HashMap<>());
            long t2 = System.nanoTime();
            System.out.printf("  Memoized: %.3f ms%n", 
                            (t2 - t1) / 1_000_000.0);
            
            // Bottom-up
            t1 = System.nanoTime();
            fibonacciBottomUp(nVal);
            t2 = System.nanoTime();
            System.out.printf("  Bottom-up: %.3f ms%n", 
                            (t2 - t1) / 1_000_000.0);
            
            // Optimized
            t1 = System.nanoTime();
            fibonacciOptimized(nVal);
            t2 = System.nanoTime();
            System.out.printf("  Optimized: %.3f ms%n", 
                            (t2 - t1) / 1_000_000.0);
        }
        System.out.println();
        
        // Example 3: Generate sequence
        System.out.println("Example 3: Generating Fibonacci Sequence");
        System.out.println("-".repeat(70));
        
        List<Long> sequence = fibonacciSequence(15, "optimized");
        System.out.println("First 15 Fibonacci numbers:");
        System.out.println("  " + sequence);
        System.out.println();
        
        // Example 4: Large values
        System.out.println("Example 4: Large Fibonacci Numbers");
        System.out.println("-".repeat(70));
        
        int[] largeN = {50, 100};
        for (int nVal : largeN) {
            long result = fibonacciOptimized(nVal);
            System.out.println("Fibonacci(" + nVal + ") = " + result);
            System.out.println("  (digits: " + String.valueOf(result).length() + ")");
        }
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nComplexity Summary:");
        System.out.println("  Naive: O(2^n) time, O(n) space");
        System.out.println("  Memoized: O(n) time, O(n) space");
        System.out.println("  Bottom-up: O(n) time, O(n) space");
        System.out.println("  Optimized: O(n) time, O(1) space");
        System.out.println("\nKey Advantages:");
        System.out.println("  - Demonstrates DP concepts");
        System.out.println("  - Multiple optimization strategies");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}

