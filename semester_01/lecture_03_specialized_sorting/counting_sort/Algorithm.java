import java.util.Arrays;
import java.util.Random;

/**
 * Counting Sort implementation.
 * 
 * Integer sorting algorithm that counts occurrences.
 * 
 * Time Complexity: O(n + k) where k is the range
 * Space Complexity: O(n + k)
 * Stable: Yes
 * Adaptive: No
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    /**
     * Sort array using counting sort.
     * 
     * @param arr Array of integers to sort
     * @return Sorted array
     */
    public static int[] countingSort(int[] arr) {
        if (arr.length == 0) {
            return arr;
        }
        
        // Find range
        int maxVal = arr[0];
        int minVal = arr[0];
        for (int num : arr) {
            if (num > maxVal) maxVal = num;
            if (num < minVal) minVal = num;
        }
        
        int rangeSize = maxVal - minVal + 1;
        
        // Create count array
        int[] count = new int[rangeSize];
        
        // Count occurrences
        for (int num : arr) {
            count[num - minVal]++;
        }
        
        // Cumulative count
        for (int i = 1; i < count.length; i++) {
            count[i] += count[i - 1];
        }
        
        // Build output array
        int[] output = new int[arr.length];
        for (int i = arr.length - 1; i >= 0; i--) {
            int num = arr[i];
            int index = count[num - minVal] - 1;
            output[index] = num;
            count[num - minVal]--;
        }
        
        return output;
    }
    
    /**
     * Simple counting sort (non-stable).
     * 
     * @param arr Array to sort
     * @return Sorted array
     */
    public static int[] countingSortSimple(int[] arr) {
        if (arr.length == 0) {
            return arr;
        }
        
        int maxVal = arr[0];
        int minVal = arr[0];
        for (int num : arr) {
            if (num > maxVal) maxVal = num;
            if (num < minVal) minVal = num;
        }
        
        int rangeSize = maxVal - minVal + 1;
        
        // Count occurrences
        int[] count = new int[rangeSize];
        for (int num : arr) {
            count[num - minVal]++;
        }
        
        // Rebuild array
        int[] result = new int[arr.length];
        int index = 0;
        for (int i = 0; i < rangeSize; i++) {
            for (int j = 0; j < count[i]; j++) {
                result[index++] = i + minVal;
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
        logger.info("COUNTING SORT DEMONSTRATION");
        logger.info(separator);
        logger.info("");
        
        // Example 1: Basic sorting
        logger.info("Example 1: Basic Integer Sorting");
        logger.info(dash);
        int[] data1 = {4, 2, 2, 8, 3, 3, 1};
        logger.info("Original: " + Arrays.toString(data1));
        int[] result1 = countingSort(data1.clone());
        logger.info("Sorted:   " + Arrays.toString(result1));
        logger.info("");
        
        // Example 2: Larger range
        logger.info("Example 2: Larger Range");
        logger.info(dash);
        int[] data2 = {64, 34, 25, 12, 22, 11, 90, 88};
        logger.info("Original: " + Arrays.toString(data2));
        int[] result2 = countingSort(data2.clone());
        logger.info("Sorted:   " + Arrays.toString(result2));
        logger.info("");
        
        // Example 3: Negative numbers
        logger.info("Example 3: With Negative Numbers");
        logger.info(dash);
        int[] data3 = {3, -1, 2, -5, 0, 4, -3};
        logger.info("Original: " + Arrays.toString(data3));
        int[] result3 = countingSort(data3.clone());
        logger.info("Sorted:   " + Arrays.toString(result3));
        logger.info("");
        
        // Example 4: Duplicates
        logger.info("Example 4: Many Duplicates");
        logger.info(dash);
        int[] data4 = {5, 2, 2, 2, 9, 1, 5, 5, 5};
        logger.info("Original: " + Arrays.toString(data4));
        int[] result4 = countingSort(data4.clone());
        logger.info("Sorted:   " + Arrays.toString(result4));
        logger.info("");
        
        // Example 5: Performance measurement
        logger.info("Example 5: Performance Measurement");
        logger.info(dash);
        
        Random rand = new Random(42);
        int[] sizes = {100, 1000, 10000};
        
        for (int size : sizes) {
            int[] data = new int[size];
            for (int i = 0; i < size; i++) {
                data[i] = rand.nextInt(101); // 0-100
            }
            
            long start = System.nanoTime();
            countingSort(data.clone());
            long end = System.nanoTime();
            
            double ms = (end - start) / 1_000_000.0;
            System.out.printf("n=%5d, k=100: %8.3f ms%n", size, ms);
        }
        
        logger.info("");
        logger.info(separator);
        logger.info("\nComplexity Summary:");
        logger.info("  Time:  O(n + k) where k is the range");
        logger.info("  Space: O(n + k)");
        logger.info("  Stable: Yes");
        logger.info("  Adaptive: No");
        logger.info("\nKey Points:");
        logger.info("  + Linear time O(n+k)");
        logger.info("  + Stable sorting");
        logger.info("  + Good for small range");
        logger.info("  + No comparisons");
        logger.info("  - Only works with integers");
        logger.info("  - Inefficient for large ranges");
        logger.info("\nWhen to use:");
        logger.info("  • Sorting integers");
        logger.info("  • Range k ≤ n");
        logger.info("  • Need linear time");
        logger.info("\nWhen NOT to use:");
        logger.info("  • Range is very large (k >> n)");
        logger.info("  • Sorting floats or strings");
        logger.info(separator);
        
        long endTime = System.nanoTime();
        double totalMs = (endTime - startTime) / 1_000_000.0;
        System.out.printf("\nTotal execution time: %.3f ms%n", totalMs);
    }
}