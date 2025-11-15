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
public class Algorithm {
    
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
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("COUNTING SORT DEMONSTRATION");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Example 1: Basic sorting
        System.out.println("Example 1: Basic Integer Sorting");
        System.out.println("-".repeat(70));
        int[] data1 = {4, 2, 2, 8, 3, 3, 1};
        System.out.println("Original: " + Arrays.toString(data1));
        int[] result1 = countingSort(data1.clone());
        System.out.println("Sorted:   " + Arrays.toString(result1));
        System.out.println();
        
        // Example 2: Larger range
        System.out.println("Example 2: Larger Range");
        System.out.println("-".repeat(70));
        int[] data2 = {64, 34, 25, 12, 22, 11, 90, 88};
        System.out.println("Original: " + Arrays.toString(data2));
        int[] result2 = countingSort(data2.clone());
        System.out.println("Sorted:   " + Arrays.toString(result2));
        System.out.println();
        
        // Example 3: Negative numbers
        System.out.println("Example 3: With Negative Numbers");
        System.out.println("-".repeat(70));
        int[] data3 = {3, -1, 2, -5, 0, 4, -3};
        System.out.println("Original: " + Arrays.toString(data3));
        int[] result3 = countingSort(data3.clone());
        System.out.println("Sorted:   " + Arrays.toString(result3));
        System.out.println();
        
        // Example 4: Duplicates
        System.out.println("Example 4: Many Duplicates");
        System.out.println("-".repeat(70));
        int[] data4 = {5, 2, 2, 2, 9, 1, 5, 5, 5};
        System.out.println("Original: " + Arrays.toString(data4));
        int[] result4 = countingSort(data4.clone());
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
                data[i] = rand.nextInt(101); // 0-100
            }
            
            long start = System.nanoTime();
            countingSort(data.clone());
            long end = System.nanoTime();
            
            double ms = (end - start) / 1_000_000.0;
            System.out.printf("n=%5d, k=100: %8.3f ms%n", size, ms);
        }
        
        System.out.println();
        System.out.println("=".repeat(70));
        System.out.println("\nComplexity Summary:");
        System.out.println("  Time:  O(n + k) where k is the range");
        System.out.println("  Space: O(n + k)");
        System.out.println("  Stable: Yes");
        System.out.println("  Adaptive: No");
        System.out.println("\nKey Points:");
        System.out.println("  + Linear time O(n+k)");
        System.out.println("  + Stable sorting");
        System.out.println("  + Good for small range");
        System.out.println("  + No comparisons");
        System.out.println("  - Only works with integers");
        System.out.println("  - Inefficient for large ranges");
        System.out.println("\nWhen to use:");
        System.out.println("  • Sorting integers");
        System.out.println("  • Range k ≤ n");
        System.out.println("  • Need linear time");
        System.out.println("\nWhen NOT to use:");
        System.out.println("  • Range is very large (k >> n)");
        System.out.println("  • Sorting floats or strings");
        System.out.println("=".repeat(70));
        
        long endTime = System.nanoTime();
        double totalMs = (endTime - startTime) / 1_000_000.0;
        System.out.printf("\nTotal execution time: %.3f ms%n", totalMs);
    }
}
