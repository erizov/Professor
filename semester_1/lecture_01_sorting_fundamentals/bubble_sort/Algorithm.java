import java.util.Arrays;
import java.util.Random;

/**
 * Bubble Sort implementation.
 * 
 * Simple comparison-based sorting algorithm.
 * 
 * Time Complexity: O(n²) - average and worst case
 * Space Complexity: O(1)
 * Stable: Yes
 * Adaptive: Yes
 */
public class Algorithm {
    
    /**
     * Sort array using bubble sort.
     * 
     * @param arr Array to be sorted
     * @return Sorted array
     */
    public static int[] bubbleSort(int[] arr) {
        int n = arr.length;
        
        for (int i = 0; i < n; i++) {
            boolean swapped = false;
            
            // Last i elements are already in place
            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    // Swap
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                    swapped = true;
                }
            }
            
            // If no swapping occurred, array is sorted
            if (!swapped) {
                break;
            }
        }
        
        return arr;
    }
    
    /**
     * Bubble sort with visualization.
     */
    public static int[] bubbleSortVisualized(int[] arr) {
        int n = arr.length;
        System.out.println("Initial array: " + Arrays.toString(arr));
        System.out.println();
        
        for (int i = 0; i < n; i++) {
            boolean swapped = false;
            System.out.println("Pass " + (i + 1) + ":");
            
            for (int j = 0; j < n - i - 1; j++) {
                System.out.print("  Comparing " + arr[j] + 
                               " and " + arr[j + 1]);
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                    swapped = true;
                    System.out.println(" → Swapped: " + 
                                     Arrays.toString(arr));
                } else {
                    System.out.println(" → No swap");
                }
            }
            
            if (!swapped) {
                System.out.println("  No swaps in this pass. Array is sorted!");
                break;
            }
            System.out.println();
        }
        
        System.out.println("Final sorted array: " + Arrays.toString(arr));
        return arr;
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("BUBBLE SORT DEMONSTRATION");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Example 1: Basic sorting
        System.out.println("Example 1: Basic Integer Sorting");
        System.out.println("-".repeat(70));
        int[] data1 = {64, 34, 25, 12, 22, 11, 90};
        System.out.println("Original: " + Arrays.toString(data1));
        int[] result1 = bubbleSort(data1.clone());
        System.out.println("Sorted:   " + Arrays.toString(result1));
        System.out.println();
        
        // Example 2: Already sorted
        System.out.println("Example 2: Already Sorted Array");
        System.out.println("-".repeat(70));
        int[] data2 = {1, 2, 3, 4, 5, 6, 7};
        System.out.println("Original: " + Arrays.toString(data2));
        int[] result2 = bubbleSort(data2.clone());
        System.out.println("Sorted:   " + Arrays.toString(result2));
        System.out.println("Note: O(n) with early termination!");
        System.out.println();
        
        // Example 3: Visualization
        System.out.println("Example 3: Visualized Bubble Sort Process");
        System.out.println("-".repeat(70));
        int[] data3 = {5, 2, 8, 1, 9};
        bubbleSortVisualized(data3.clone());
        System.out.println();
        
        // Example 4: Performance
        System.out.println("Example 4: Performance Measurement");
        System.out.println("-".repeat(70));
        
        Random rand = new Random(42);
        
        // Small
        int[] small = new int[100];
        for (int i = 0; i < small.length; i++) {
            small[i] = rand.nextInt(100);
        }
        long t1 = System.nanoTime();
        bubbleSort(small);
        long t2 = System.nanoTime();
        System.out.println("Small (100 elements):");
        System.out.printf("  Time: %.3f ms%n", (t2-t1)/1_000_000.0);
        
        long endTime = System.nanoTime();
        
        System.out.println();
        System.out.println("=".repeat(70));
        System.out.println("\nComplexity Summary:");
        System.out.println("  Time:  O(n²) - average and worst");
        System.out.println("         O(n) - best case (optimized)");
        System.out.println("  Space: O(1)");
        System.out.println("  Stable: Yes");
        System.out.println("\nKey Advantages:");
        System.out.println("  - Simple to understand");
        System.out.println("  - Adaptive");
        System.out.println("  - In-place");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
