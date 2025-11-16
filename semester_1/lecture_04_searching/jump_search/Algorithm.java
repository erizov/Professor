import java.util.Random;

/**
 * Jump Search implementation.
 * 
 * Search algorithm for sorted arrays using jumping.
 * 
 * Time Complexity: O(√n)
 * Space Complexity: O(1)
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    /**
     * Search for target using jump search.
     * 
     * @param arr Sorted array to search
     * @param target Element to find
     * @return Index of target if found, -1 otherwise
     */
    public static int jumpSearch(int[] arr, int target) {
        int n = arr.length;
        if (n == 0) {
            return -1;
        }
        
        // Calculate optimal jump size (√n)
        int step = (int)Math.sqrt(n);
        
        // Jump to find block
        int prev = 0;
        while (arr[Math.min(step, n) - 1] < target) {
            prev = step;
            step += (int)Math.sqrt(n);
            
            // If beyond array
            if (prev >= n) {
                return -1;
            }
        }
        
        // Linear search in block
        while (arr[prev] < target) {
            prev++;
            
            // If reached next block or end
            if (prev == Math.min(step, n)) {
                return -1;
            }
        }
        
        // If element found
        if (arr[prev] == target) {
            return prev;
        }
        
        return -1;
    }
    
    /**
     * Jump search with visualization.
     */
    public static int jumpSearchVisualized(int[] arr, int target) {
        int n = arr.length;
        int step = (int)Math.sqrt(n);
        
        logger.info("Array length: " + n);
        logger.info("Target: " + target);
        logger.info("Jump size: " + step + " (√" + n + ")");
        logger.info();
        
        logger.info("Jumping phase:");
        int prev = 0;
        int jumpCount = 0;
        
        while (arr[Math.min(step, n) - 1] < target) {
            System.out.printf("  Jump %d: Check arr[%d] = %d < %d%n",
                            jumpCount + 1, Math.min(step, n) - 1,
                            arr[Math.min(step, n) - 1], target);
            prev = step;
            step += (int)Math.sqrt(n);
            jumpCount++;
            
            if (prev >= n) {
                logger.info("  Went beyond array. Not found.");
                return -1;
            }
        }
        
        System.out.printf("  Found block: indices [%d:%d]%n", 
                         prev, Math.min(step, n));
        logger.info();
        
        logger.info("Linear search phase:");
        while (arr[prev] < target) {
            System.out.printf("  Check arr[%d] = %d < %d%n",
                            prev, arr[prev], target);
            prev++;
            
            if (prev == Math.min(step, n)) {
                logger.info("  Reached end of block. Not found.");
                return -1;
            }
        }
        
        if (arr[prev] == target) {
            System.out.printf("  Found! arr[%d] = %d%n", prev, target);
            return prev;
        } else {
            System.out.printf("  arr[%d] = %d > %d. Not found.%n",
                            prev, arr[prev], target);
            return -1;
        }
    }
    
    /**
     * Main method for demonstration.
     */
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        logger.info("=".repeat(70));
        logger.info("JUMP SEARCH DEMONSTRATION");
        logger.info("=".repeat(70));
        logger.info();
        
        // Example 1: Element found
        logger.info("Example 1: Element Found");
        logger.info("-".repeat(70));
        int[] data1 = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19};
        int target1 = 13;
        int result1 = jumpSearch(data1, target1);
        logger.info("Target: " + target1);
        logger.info("Result: Index " + result1);
        if (result1 != -1) {
            System.out.printf("Verification: arr[%d] = %d%n",
                            result1, data1[result1]);
        }
        logger.info();
        
        // Example 2: Element not found
        logger.info("Example 2: Element Not Found");
        logger.info("-".repeat(70));
        int[] data2 = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19};
        int target2 = 10;
        int result2 = jumpSearch(data2, target2);
        logger.info("Target: " + target2);
        logger.info("Result: " + 
                          (result2 == -1 ? "Not found" : "Index " + result2));
        logger.info();
        
        // Example 3: Visualization
        logger.info("Example 3: Visualized Jump Search");
        logger.info("-".repeat(70));
        int[] data3 = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15};
        int target3 = 11;
        jumpSearchVisualized(data3, target3);
        logger.info();
        
        // Example 4: Performance measurement
        logger.info("Example 4: Performance Measurement");
        logger.info("-".repeat(70));
        
        Random rand = new Random(42);
        int[] sizes = {1000, 10000, 100000};
        
        for (int size : sizes) {
            int[] data = new int[size];
            for (int i = 0; i < size; i++) {
                data[i] = i * 2; // Even numbers
            }
            
            int target = data[rand.nextInt(size)];
            
            long start = System.nanoTime();
            jumpSearch(data, target);
            long end = System.nanoTime();
            
            double ms = (end - start) / 1_000_000.0;
            System.out.printf("n=%6d: %8.3f ms%n", size, ms);
        }
        
        logger.info();
        logger.info("=".repeat(70));
        logger.info("\nComplexity Summary:");
        logger.info("  Time:  O(√n)");
        logger.info("  Space: O(1)");
        logger.info("\nKey Points:");
        logger.info("  + Better than linear O(n)");
        logger.info("  + Simpler than binary");
        logger.info("  + Works on sorted arrays");
        logger.info("  - Requires sorted array");
        logger.info("  - Slower than binary O(log n)");
        logger.info("\nComparison:");
        logger.info("  Linear:  O(n)");
        logger.info("  Jump:    O(√n)");
        logger.info("  Binary:  O(log n)");
        logger.info("\nWhen to use:");
        logger.info("  • Sorted array");
        logger.info("  • Middle ground search");
        logger.info("  • Backward jumping not possible");
        logger.info("=".repeat(70));
        
        long endTime = System.nanoTime();
        double totalMs = (endTime - startTime) / 1_000_000.0;
        System.out.printf("\nTotal execution time: %.3f ms%n", totalMs);
    }
}