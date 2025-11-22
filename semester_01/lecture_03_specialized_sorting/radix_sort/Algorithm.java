package semester_01.lecture_03_specialized_sorting.radix_sort;

import java.util.Arrays;
import java.util.Random;

/**
 * Radix Sort implementation (LSD - Least Significant Digit).
 * 
 * Non-comparative integer sorting algorithm.
 * 
 * Time Complexity: O(d * (n + k)) where d=digits, k=radix
 * Space Complexity: O(n + k)
 * Stable: Yes
 * Adaptive: No
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    /**
     * Sort array using radix sort (LSD).
     * 
     * @param arr Array of non-negative integers
     * @return Sorted array
     */
    public static int[] radixSort(int[] arr) {
        if (arr.length <= 1) {
            return arr;
        }
        
        // Find maximum number to know number of digits
        int maxNum = arr[0];
        for (int num : arr) {
            if (num > maxNum) {
                maxNum = num;
            }
        }
        
        // Do counting sort for every digit
        int exp = 1;
        while (maxNum / exp > 0) {
            countingSortByDigit(arr, exp);
            exp *= 10;
        }
        
        return arr;
    }
    
    /**
     * Counting sort based on digit represented by exp.
     * 
     * @param arr Array to sort (modified in-place)
     * @param exp Current digit position (1, 10, 100, etc.)
     */
    private static void countingSortByDigit(int[] arr, int exp) {
        int n = arr.length;
        int[] output = new int[n];
        int[] count = new int[10]; // For digits 0-9
        
        // Count occurrences of digits
        for (int i = 0; i < n; i++) {
            int digit = (arr[i] / exp) % 10;
            count[digit]++;
        }
        
        // Change count[i] to actual position
        for (int i = 1; i < 10; i++) {
            count[i] += count[i - 1];
        }
        
        // Build output array
        for (int i = n - 1; i >= 0; i--) {
            int digit = (arr[i] / exp) % 10;
            output[count[digit] - 1] = arr[i];
            count[digit]--;
        }
        
        // Copy output array to arr
        System.arraycopy(output, 0, arr, 0, n);
    }
    
    /**
     * Get number of digits in a number.
     */
    private static int getNumDigits(int num) {
        if (num == 0) return 1;
        int digits = 0;
        while (num > 0) {
            digits++;
            num /= 10;
        }
        return digits;
    }
    
    /**
     * Main method for demonstration.
     */
    public static void main(String[] args) {
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        long startTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("RADIX SORT DEMONSTRATION");
        logger.info(separator);
        logger.info("");
        
        // Example 1: Basic sorting
        logger.info("Example 1: Basic Integer Sorting");
        logger.info(dash);
        int[] data1 = {170, 45, 75, 90, 802, 24, 2, 66};
        logger.info("Original: " + Arrays.toString(data1));
        int[] result1 = radixSort(data1.clone());
        logger.info("Sorted:   " + Arrays.toString(result1));
        logger.info("");
        
        // Example 2: Small numbers
        logger.info("Example 2: Small Numbers");
        logger.info(dash);
        int[] data2 = {9, 8, 7, 6, 5, 4, 3, 2, 1, 0};
        logger.info("Original: " + Arrays.toString(data2));
        int[] result2 = radixSort(data2.clone());
        logger.info("Sorted:   " + Arrays.toString(result2));
        logger.info("");
        
        // Example 3: Large numbers
        logger.info("Example 3: Large Numbers");
        logger.info(dash);
        int[] data3 = {1234, 5678, 9012, 3456, 7890};
        logger.info("Original: " + Arrays.toString(data3));
        int[] result3 = radixSort(data3.clone());
        logger.info("Sorted:   " + Arrays.toString(result3));
        logger.info("");
        
        // Example 4: Duplicates
        logger.info("Example 4: With Duplicates");
        logger.info(dash);
        int[] data4 = {321, 123, 321, 456, 123, 789};
        logger.info("Original: " + Arrays.toString(data4));
        int[] result4 = radixSort(data4.clone());
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
                data[i] = rand.nextInt(10000);
            }
            
            long start = System.nanoTime();
            radixSort(data.clone());
            long end = System.nanoTime();
            
            double ms = (end - start) / 1_000_000.0;
            System.out.printf("n=%5d: %8.3f ms%n", size, ms);
        }
        
        logger.info("");
        logger.info(separator);
        logger.info("\nComplexity Summary:");
        logger.info("  Time:  O(d * (n + k))");
        logger.info("         d = digits, k = radix (10)");
        logger.info("  Space: O(n + k)");
        logger.info("  Stable: Yes");
        logger.info("  Adaptive: No");
        logger.info("\nKey Points:");
        logger.info("  + Linear time when d is constant");
        logger.info("  + Stable sorting");
        logger.info("  + No comparisons");
        logger.info("  + Good for fixed-length integers");
        logger.info("  - Only for integers");
        logger.info("  - Not in-place");
        logger.info("\nWhen to use:");
        logger.info("  • Sorting integers with limited digits");
        logger.info("  • n is large, d is small");
        logger.info("  • Need stable sort");
        logger.info("\nWhen NOT to use:");
        logger.info("  • Variable-length keys");
        logger.info("  • Small datasets");
        logger.info(separator);
        
        long endTime = System.nanoTime();
        double totalMs = (endTime - startTime) / 1_000_000.0;
        System.out.printf("\nTotal execution time: %.3f ms%n", totalMs);
    }
}
