import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;

/**
 * Bucket Sort implementation.
 * 
 * Distribution sort using buckets.
 * 
 * Time Complexity: O(n + k) average, O(n²) worst case
 * Space Complexity: O(n + k)
 * Stable: Yes (with stable sub-sort)
 * Adaptive: No
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    /**
     * Sort array using bucket sort.
     * 
     * @param arr Array of numbers to sort
     * @param numBuckets Number of buckets
     * @return Sorted array
     */
    public static double[] bucketSort(double[] arr, int numBuckets) {
        if (arr.length <= 1) {
            return arr;
        }
        
        // Find min and max
        double minVal = arr[0];
        double maxVal = arr[0];
        for (double num : arr) {
            if (num < minVal) minVal = num;
            if (num > maxVal) maxVal = num;
        }
        
        // Create buckets
        List<List<Double>> buckets = new ArrayList<>();
        for (int i = 0; i < numBuckets; i++) {
            buckets.add(new ArrayList<>());
        }
        
        // Distribute elements
        double rangeVal = maxVal - minVal;
        if (rangeVal == 0) {
            return arr; // All elements same
        }
        
        for (double num : arr) {
            int index = (int)((num - minVal) / rangeVal * (numBuckets - 1));
            buckets.get(index).add(num);
        }
        
        // Sort buckets and concatenate
        double[] result = new double[arr.length];
        int idx = 0;
        for (List<Double> bucket : buckets) {
            if (!bucket.isEmpty()) {
                Collections.sort(bucket);
                for (double num : bucket) {
                    result[idx++] = num;
                }
            }
        }
        
        return result;
    }
    
    /**
     * Sort array using bucket sort (auto bucket count).
     * 
     * @param arr Array to sort
     * @return Sorted array
     */
    public static double[] bucketSort(double[] arr) {
        return bucketSort(arr, arr.length);
    }
    
    /**
     * Bucket sort for integers.
     * 
     * @param arr Array of integers
     * @return Sorted array
     */
    public static int[] bucketSortIntegers(int[] arr) {
        if (arr.length <= 1) {
            return arr;
        }
        
        int minVal = arr[0];
        int maxVal = arr[0];
        for (int num : arr) {
            if (num < minVal) minVal = num;
            if (num > maxVal) maxVal = num;
        }
        
        // Create buckets for each value
        int bucketCount = maxVal - minVal + 1;
        List<List<Integer>> buckets = new ArrayList<>();
        for (int i = 0; i < bucketCount; i++) {
            buckets.add(new ArrayList<>());
        }
        
        // Distribute elements
        for (int num : arr) {
            buckets.get(num - minVal).add(num);
        }
        
        // Concatenate buckets
        int[] result = new int[arr.length];
        int idx = 0;
        for (List<Integer> bucket : buckets) {
            for (int num : bucket) {
                result[idx++] = num;
            }
        }
        
        return result;
    }
    
    /**
     * Main method for demonstration.
     */
    public static void main(String[] args) {
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        long startTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("BUCKET SORT DEMONSTRATION");
        logger.info(separator);
        logger.info("");
        
        // Example 1: Floating point numbers
        logger.info("Example 1: Sorting Floating Point Numbers");
        logger.info(dash);
        double[] data1 = {0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 
                         0.21, 0.12, 0.23, 0.68};
        logger.info("Original: " + Arrays.toString(data1));
        double[] result1 = bucketSort(data1.clone(), 5);
        logger.info("Sorted:   " + Arrays.toString(result1));
        logger.info("");
        
        // Example 2: Integers
        logger.info("Example 2: Sorting Integers");
        logger.info(dash);
        int[] data2 = {42, 32, 33, 52, 37, 47, 51};
        logger.info("Original: " + Arrays.toString(data2));
        int[] result2 = bucketSortIntegers(data2.clone());
        logger.info("Sorted:   " + Arrays.toString(result2));
        logger.info("");
        
        // Example 3: Large range
        logger.info("Example 3: Large Range");
        logger.info(dash);
        double[] data3 = {1.5, 8.9, 3.2, 7.4, 2.1, 9.8, 4.6};
        logger.info("Original: " + Arrays.toString(data3));
        double[] result3 = bucketSort(data3.clone(), 5);
        logger.info("Sorted:   " + Arrays.toString(result3));
        logger.info("");
        
        // Example 4: Performance measurement
        logger.info("Example 4: Performance Measurement");
        logger.info(dash);
        
        Random rand = new Random(42);
        int[] sizes = {100, 1000, 10000};
        
        for (int size : sizes) {
            double[] data = new double[size];
            for (int i = 0; i < size; i++) {
                data[i] = rand.nextDouble();
            }
            
            long start = System.nanoTime();
            bucketSort(data.clone());
            long end = System.nanoTime();
            
            double ms = (end - start) / 1_000_000.0;
            System.out.printf("n=%5d: %8.3f ms%n", size, ms);
        }
        
        logger.info("");
        logger.info(separator);
        logger.info("\nComplexity Summary:");
        logger.info("  Time:  O(n + k) average");
        logger.info("         O(n²) worst case");
        logger.info("  Space: O(n + k)");
        logger.info("  Stable: Yes");
        logger.info("  Adaptive: No");
        logger.info("\nKey Points:");
        logger.info("  + Linear average time");
        logger.info("  + Good for floating points");
        logger.info("  + Can be stable");
        logger.info("  + Parallelizable");
        logger.info("  - Depends on distribution");
        logger.info("  - Requires knowledge of range");
        logger.info("\nWhen to use:");
        logger.info("  • Uniform distribution");
        logger.info("  • Know input range");
        logger.info("  • Sorting floats");
        logger.info("\nWhen NOT to use:");
        logger.info("  • Non-uniform distribution");
        logger.info("  • Unknown range");
        logger.info(separator);
        
        long endTime = System.nanoTime();
        double totalMs = (endTime - startTime) / 1_000_000.0;
        System.out.printf("\nTotal execution time: %.3f ms%n", totalMs);
    }
}