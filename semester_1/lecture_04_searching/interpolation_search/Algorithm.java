import java.util.Random;

/**
 * Interpolation Search implementation.
 * 
 * Search algorithm for uniformly distributed sorted arrays.
 * 
 * Time Complexity: O(log log n) average, O(n) worst case
 * Space Complexity: O(1)
 */
public class Algorithm {
    
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
        System.out.println("Target: " + target);
        System.out.println();
        
        int left = 0;
        int right = arr.length - 1;
        int iteration = 0;
        
        while (left <= right && target >= arr[left] && target <= arr[right]) {
            iteration++;
            System.out.println("Iteration " + iteration + ":");
            System.out.printf("  Range: [%d, %d]%n", left, right);
            System.out.printf("  arr[%d] = %d, arr[%d] = %d%n",
                            left, arr[left], right, arr[right]);
            
            if (left == right) {
                if (arr[left] == target) {
                    System.out.println("  Found at index " + left + "!");
                    return left;
                }
                System.out.println("  Not found.");
                return -1;
            }
            
            // Calculate interpolated position
            int pos = left + (int)((double)(target - arr[left]) / 
                                   (arr[right] - arr[left]) * 
                                   (right - left));
            
            System.out.printf("  Interpolated position: %d%n", pos);
            System.out.printf("  arr[%d] = %d%n", pos, arr[pos]);
            
            if (arr[pos] == target) {
                System.out.println("  Found at index " + pos + "!");
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
            System.out.println();
        }
        
        System.out.println("Target out of range or not found.");
        return -1;
    }
    
    /**
     * Main method for demonstration.
     */
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("INTERPOLATION SEARCH DEMONSTRATION");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Example 1: Uniformly distributed
        System.out.println("Example 1: Uniformly Distributed (Best Case)");
        System.out.println("-".repeat(70));
        int[] data1 = {10, 20, 30, 40, 50, 60, 70, 80, 90, 100};
        int target1 = 70;
        int result1 = interpolationSearch(data1, target1);
        System.out.println("Target: " + target1);
        System.out.println("Result: Index " + result1);
        if (result1 != -1) {
            System.out.printf("Verification: arr[%d] = %d%n",
                            result1, data1[result1]);
        }
        System.out.println();
        
        // Example 2: Element not found
        System.out.println("Example 2: Element Not Found");
        System.out.println("-".repeat(70));
        int[] data2 = {10, 20, 30, 40, 50, 60, 70, 80, 90, 100};
        int target2 = 35;
        int result2 = interpolationSearch(data2, target2);
        System.out.println("Target: " + target2);
        System.out.println("Result: " + 
                          (result2 == -1 ? "Not found" : "Index " + result2));
        System.out.println();
        
        // Example 3: Visualization
        System.out.println("Example 3: Visualized Interpolation Search");
        System.out.println("-".repeat(70));
        int[] data3 = {10, 20, 30, 40, 50, 60, 70, 80, 90, 100};
        int target3 = 55;
        interpolationSearchVisualized(data3, target3);
        System.out.println();
        
        // Example 4: Performance measurement
        System.out.println("Example 4: Performance Measurement");
        System.out.println("-".repeat(70));
        System.out.println("With uniformly distributed data:");
        
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
        
        System.out.println();
        System.out.println("=".repeat(70));
        System.out.println("\nComplexity Summary:");
        System.out.println("  Time:  O(log log n) - uniform distribution");
        System.out.println("         O(n) - non-uniform distribution");
        System.out.println("  Space: O(1)");
        System.out.println("\nKey Points:");
        System.out.println("  + Faster than binary for uniform data");
        System.out.println("  + O(log log n) average");
        System.out.println("  + Works on sorted arrays");
        System.out.println("  - Requires uniform distribution");
        System.out.println("  - Worst case O(n)");
        System.out.println("\nComparison:");
        System.out.println("  Linear:        O(n)");
        System.out.println("  Jump:          O(√n)");
        System.out.println("  Binary:        O(log n)");
        System.out.println("  Interpolation: O(log log n) avg");
        System.out.println("\nWhen to use:");
        System.out.println("  • Sorted array");
        System.out.println("  • Uniform distribution");
        System.out.println("  • Large datasets");
        System.out.println("\nWhen NOT to use:");
        System.out.println("  • Non-uniform distribution");
        System.out.println("  • Small datasets");
        System.out.println("=".repeat(70));
        
        long endTime = System.nanoTime();
        double totalMs = (endTime - startTime) / 1_000_000.0;
        System.out.printf("\nTotal execution time: %.3f ms%n", totalMs);
    }
}
