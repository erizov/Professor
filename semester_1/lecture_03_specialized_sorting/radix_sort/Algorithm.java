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
public class Algorithm {
    
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
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("RADIX SORT DEMONSTRATION");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Example 1: Basic sorting
        System.out.println("Example 1: Basic Integer Sorting");
        System.out.println("-".repeat(70));
        int[] data1 = {170, 45, 75, 90, 802, 24, 2, 66};
        System.out.println("Original: " + Arrays.toString(data1));
        int[] result1 = radixSort(data1.clone());
        System.out.println("Sorted:   " + Arrays.toString(result1));
        System.out.println();
        
        // Example 2: Small numbers
        System.out.println("Example 2: Small Numbers");
        System.out.println("-".repeat(70));
        int[] data2 = {9, 8, 7, 6, 5, 4, 3, 2, 1, 0};
        System.out.println("Original: " + Arrays.toString(data2));
        int[] result2 = radixSort(data2.clone());
        System.out.println("Sorted:   " + Arrays.toString(result2));
        System.out.println();
        
        // Example 3: Large numbers
        System.out.println("Example 3: Large Numbers");
        System.out.println("-".repeat(70));
        int[] data3 = {1234, 5678, 9012, 3456, 7890};
        System.out.println("Original: " + Arrays.toString(data3));
        int[] result3 = radixSort(data3.clone());
        System.out.println("Sorted:   " + Arrays.toString(result3));
        System.out.println();
        
        // Example 4: Duplicates
        System.out.println("Example 4: With Duplicates");
        System.out.println("-".repeat(70));
        int[] data4 = {321, 123, 321, 456, 123, 789};
        System.out.println("Original: " + Arrays.toString(data4));
        int[] result4 = radixSort(data4.clone());
        System.out.println("Sorted:   " + Arrays.toString(result4));
        System.out.println();
        
        // Example 5: Performance measurement
        System.out.println("Example 5: Performance Measurement");
        System.out.println("-".repeat(70));
        
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
        
        System.out.println();
        System.out.println("=".repeat(70));
        System.out.println("\nComplexity Summary:");
        System.out.println("  Time:  O(d * (n + k))");
        System.out.println("         d = digits, k = radix (10)");
        System.out.println("  Space: O(n + k)");
        System.out.println("  Stable: Yes");
        System.out.println("  Adaptive: No");
        System.out.println("\nKey Points:");
        System.out.println("  + Linear time when d is constant");
        System.out.println("  + Stable sorting");
        System.out.println("  + No comparisons");
        System.out.println("  + Good for fixed-length integers");
        System.out.println("  - Only for integers");
        System.out.println("  - Not in-place");
        System.out.println("\nWhen to use:");
        System.out.println("  • Sorting integers with limited digits");
        System.out.println("  • n is large, d is small");
        System.out.println("  • Need stable sort");
        System.out.println("\nWhen NOT to use:");
        System.out.println("  • Variable-length keys");
        System.out.println("  • Small datasets");
        System.out.println("=".repeat(70));
        
        long endTime = System.nanoTime();
        double totalMs = (endTime - startTime) / 1_000_000.0;
        System.out.printf("\nTotal execution time: %.3f ms%n", totalMs);
    }
}
