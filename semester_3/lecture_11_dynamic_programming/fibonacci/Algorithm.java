import java.util.*;

/**
 * Fibonacci Sequence - Dynamic Programming.
 * 
 * Multiple approaches: naive, memoized, bottom-up, optimized.
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
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
        
        logger.info("=".repeat(70));
        logger.info("FIBONACCI SEQUENCE - DYNAMIC PROGRAMMING");
        logger.info("=".repeat(70));
        logger.info();
        
        // Example 1: Compare approaches
        logger.info("Example 1: Comparing Different Approaches");
        logger.info("-".repeat(70));
        
        int n = 10;
        logger.info("Computing Fibonacci(" + n + "):");
        logger.info("  Naive recursive: " + fibonacciNaive(n));
        logger.info("  Memoized: " + 
                         fibonacciMemoized(n, new HashMap<>()));
        logger.info("  Bottom-up DP: " + fibonacciBottomUp(n));
        logger.info("  Optimized: " + fibonacciOptimized(n));
        logger.info();
        
        // Example 2: Performance
        logger.info("Example 2: Performance Comparison");
        logger.info("-".repeat(70));
        
        int[] testValues = {20, 30, 35};
        
        for (int nVal : testValues) {
            logger.info("\nComputing Fibonacci(" + nVal + "):");
            
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
        logger.info();
        
        // Example 3: Generate sequence
        logger.info("Example 3: Generating Fibonacci Sequence");
        logger.info("-".repeat(70));
        
        List<Long> sequence = fibonacciSequence(15, "optimized");
        logger.info("First 15 Fibonacci numbers:");
        logger.info("  " + sequence);
        logger.info();
        
        // Example 4: Large values
        logger.info("Example 4: Large Fibonacci Numbers");
        logger.info("-".repeat(70));
        
        int[] largeN = {50, 100};
        for (int nVal : largeN) {
            long result = fibonacciOptimized(nVal);
            logger.info("Fibonacci(" + nVal + ") = " + result);
            logger.info("  (digits: " + String.valueOf(result).length() + ")");
        }
        logger.info();
        
        long endTime = System.nanoTime();
        
        logger.info("=".repeat(70));
        logger.info("\nComplexity Summary:");
        logger.info("  Naive: O(2^n) time, O(n) space");
        logger.info("  Memoized: O(n) time, O(n) space");
        logger.info("  Bottom-up: O(n) time, O(n) space");
        logger.info("  Optimized: O(n) time, O(1) space");
        logger.info("\nKey Advantages:");
        logger.info("  - Demonstrates DP concepts");
        logger.info("  - Multiple optimization strategies");
        logger.info("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
