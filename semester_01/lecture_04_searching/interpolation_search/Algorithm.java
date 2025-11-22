// package semester_01.lecture_04_searching.interpolation_search;

import java.util.Random;

/**
 * Interpolation Search implementation.
 * 
 * Search algorithm for uniformly distributed sorted arrays.
 * 
 * Time Complexity: O(log log n) average, O(n) worst case
 * Space Complexity: O(1)
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    /**
     * Search for target using interpolation search.
     * 
     * @param arr Sorted array of integers
     * @param target Element to find
     * @return Index of target if found, -1 otherwise
     */
    public static int interpolationSearch(int[] arr, int target) {
        int left = 0;
        int right = arr.length - 1;
        
        while (left <= right && target >= arr[left] && target <= arr[right]) {
            // If only one element left
            if (left == right) {
                if (arr[left] == target) {
                    return left;
                }
                return -1;
            }
            
            // Estimate position using interpolation
            int pos = left + (int)((double)(target - arr[left]) / 
                                   (arr[right] - arr[left]) * 
                                   (right - left));
            
            // Target found
            if (arr[pos] == target) {
                return pos;
            }
            
            // Target in right subarray
            if (arr[pos] < target) {
                left = pos + 1;
            }
            // Target in left subarray
            else {
                right = pos - 1;
            }
        }
        
        return -1;
    }
    
    /**
     * Interpolation search with visualization.
     */
    public static int interpolationSearchVisualized(int[] arr, int target) {
        logger.info("Target: " + target);
        logger.info("");
        
        int left = 0;
        int right = arr.length - 1;
        int iteration = 0;
        
        while (left <= right && target >= arr[left] && target <= arr[right]) {
            iteration++;
            logger.info("Iteration " + iteration + ":");
            System.out.printf("  Range: [%d, %d]%n", left, right);
            System.out.printf("  arr[%d] = %d, arr[%d] = %d%n",
                            left, arr[left], right, arr[right]);
            
            if (left == right) {
                if (arr[left] == target) {
                    logger.info("  Found at index " + left + "!");
                    return left;
                }
                logger.info("  Not found.");
                return -1;
            }
            
            // Calculate interpolated position
            int pos = left + (int)((double)(target - arr[left]) / 
                                   (arr[right] - arr[left]) * 
                                   (right - left));
            
            System.out.printf("  Interpolated position: %d%n", pos);
            System.out.printf("  arr[%d] = %d%n", pos, arr[pos]);
            
            if (arr[pos] == target) {
                logger.info("  Found at index " + pos + "!");
                return pos;
            }
            
            if (arr[pos] < target) {
                System.out.printf("  %d < %d, search right half%n",
                                arr[pos], target);
                left = pos + 1;
            } else {
                System.out.printf("  %d > %d, search left half%n",
                                arr[pos], target);
                right = pos - 1;
            }
            logger.info("");
        }
        
        logger.info("Target out of range or not found.");
        return -1;
    }
    
    /**
     * Main method for demonstration.
     */
    public static void main(String[] args) {
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        long startTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("INTERPOLATION SEARCH DEMONSTRATION");
        logger.info(separator);
        logger.info("");
        
        // Example 1: Uniformly distributed
        logger.info("Example 1: Uniformly Distributed (Best Case)");
        logger.info(dash);
        int[] data1 = {10, 20, 30, 40, 50, 60, 70, 80, 90, 100};
        int target1 = 70;
        int result1 = interpolationSearch(data1, target1);
        logger.info("Target: " + target1);
        logger.info("Result: Index " + result1);
        if (result1 != -1) {
            System.out.printf("Verification: arr[%d] = %d%n",
                            result1, data1[result1]);
        }
        logger.info("");
        
        // Example 2: Element not found
        logger.info("Example 2: Element Not Found");
        logger.info(dash);
        int[] data2 = {10, 20, 30, 40, 50, 60, 70, 80, 90, 100};
        int target2 = 35;
        int result2 = interpolationSearch(data2, target2);
        logger.info("Target: " + target2);
        logger.info("Result: " + 
                          (result2 == -1 ? "Not found" : "Index " + result2));
        logger.info("");
        
        // Example 3: Visualization
        logger.info("Example 3: Visualized Interpolation Search");
        logger.info(dash);
        int[] data3 = {10, 20, 30, 40, 50, 60, 70, 80, 90, 100};
        int target3 = 55;
        interpolationSearchVisualized(data3, target3);
        logger.info("");
        
        // Example 4: Performance measurement
        logger.info("Example 4: Performance Measurement");
        logger.info(dash);
        logger.info("With uniformly distributed data:");
        
        Random rand = new Random(42);
        int[] sizes = {1000, 10000, 100000};
        
        for (int size : sizes) {
            int[] data = new int[size];
            for (int i = 0; i < size; i++) {
                data[i] = i * 10; // Uniformly distributed
            }
            
            int target = data[rand.nextInt(size)];
            
            long start = System.nanoTime();
            interpolationSearch(data, target);
            long end = System.nanoTime();
            
            double ms = (end - start) / 1_000_000.0;
            System.out.printf("n=%6d: %8.3f ms%n", size, ms);
        }
        
        logger.info("");
        logger.info(separator);
        logger.info("\nComplexity Summary:");
        logger.info("  Time:  O(log log n) - uniform distribution");
        logger.info("         O(n) - non-uniform distribution");
        logger.info("  Space: O(1)");
        logger.info("\nKey Points:");
        logger.info("  + Faster than binary for uniform data");
        logger.info("  + O(log log n) average");
        logger.info("  + Works on sorted arrays");
        logger.info("  - Requires uniform distribution");
        logger.info("  - Worst case O(n)");
        logger.info("\nComparison:");
        logger.info("  Linear:        O(n)");
        logger.info("  Jump:          O(√n)");
        logger.info("  Binary:        O(log n)");
        logger.info("  Interpolation: O(log log n) avg");
        logger.info("\nWhen to use:");
        logger.info("  • Sorted array");
        logger.info("  • Uniform distribution");
        logger.info("  • Large datasets");
        logger.info("\nWhen NOT to use:");
        logger.info("  • Non-uniform distribution");
        logger.info("  • Small datasets");
        logger.info(separator);
        
        long endTime = System.nanoTime();
        double totalMs = (endTime - startTime) / 1_000_000.0;
        System.out.printf("\nTotal execution time: %.3f ms%n", totalMs);
    }
}
