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
public class Algorithm {
    
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
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("BUCKET SORT DEMONSTRATION");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Example 1: Floating point numbers
        System.out.println("Example 1: Sorting Floating Point Numbers");
        System.out.println("-".repeat(70));
        double[] data1 = {0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 
                         0.21, 0.12, 0.23, 0.68};
        System.out.println("Original: " + Arrays.toString(data1));
        double[] result1 = bucketSort(data1.clone(), 5);
        System.out.println("Sorted:   " + Arrays.toString(result1));
        System.out.println();
        
        // Example 2: Integers
        System.out.println("Example 2: Sorting Integers");
        System.out.println("-".repeat(70));
        int[] data2 = {42, 32, 33, 52, 37, 47, 51};
        System.out.println("Original: " + Arrays.toString(data2));
        int[] result2 = bucketSortIntegers(data2.clone());
        System.out.println("Sorted:   " + Arrays.toString(result2));
        System.out.println();
        
        // Example 3: Large range
        System.out.println("Example 3: Large Range");
        System.out.println("-".repeat(70));
        double[] data3 = {1.5, 8.9, 3.2, 7.4, 2.1, 9.8, 4.6};
        System.out.println("Original: " + Arrays.toString(data3));
        double[] result3 = bucketSort(data3.clone(), 5);
        System.out.println("Sorted:   " + Arrays.toString(result3));
        System.out.println();
        
        // Example 4: Performance measurement
        System.out.println("Example 4: Performance Measurement");
        System.out.println("-".repeat(70));
        
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
        
        System.out.println();
        System.out.println("=".repeat(70));
        System.out.println("\nComplexity Summary:");
        System.out.println("  Time:  O(n + k) average");
        System.out.println("         O(n²) worst case");
        System.out.println("  Space: O(n + k)");
        System.out.println("  Stable: Yes");
        System.out.println("  Adaptive: No");
        System.out.println("\nKey Points:");
        System.out.println("  + Linear average time");
        System.out.println("  + Good for floating points");
        System.out.println("  + Can be stable");
        System.out.println("  + Parallelizable");
        System.out.println("  - Depends on distribution");
        System.out.println("  - Requires knowledge of range");
        System.out.println("\nWhen to use:");
        System.out.println("  • Uniform distribution");
        System.out.println("  • Know input range");
        System.out.println("  • Sorting floats");
        System.out.println("\nWhen NOT to use:");
        System.out.println("  • Non-uniform distribution");
        System.out.println("  • Unknown range");
        System.out.println("=".repeat(70));
        
        long endTime = System.nanoTime();
        double totalMs = (endTime - startTime) / 1_000_000.0;
        System.out.printf("\nTotal execution time: %.3f ms%n", totalMs);
    }
}
