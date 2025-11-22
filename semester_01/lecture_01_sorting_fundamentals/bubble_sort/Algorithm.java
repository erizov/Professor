package semester_01.lecture_01_sorting_fundamentals.bubble_sort;

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
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());
    private static final String dash = "-".repeat(70);

    
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
        logger.info("Initial array: " + Arrays.toString(arr));
        logger.info("");
        
        for (int i = 0; i < n; i++) {
            boolean swapped = false;
            logger.info("Pass " + (i + 1) + ":");
            
            for (int j = 0; j < n - i - 1; j++) {
                System.out.print("  Comparing " + arr[j] + 
                               " and " + arr[j + 1]);
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                    swapped = true;
                    logger.info(" → Swapped: " + 
                                     Arrays.toString(arr));
                } else {
                    logger.info(" → No swap");
                }
            }
            
            if (!swapped) {
                logger.info("  No swaps in this pass. Array is sorted!");
                break;
            }
            logger.info("");
        }
        
        logger.info("Final sorted array: " + Arrays.toString(arr));
        return arr;
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        String separator = "=".repeat(70);
        logger.info(separator);
        logger.info("BUBBLE SORT DEMONSTRATION");
        logger.info(separator);
        logger.info("");
        
        // Example 1: Basic sorting
        logger.info("Example 1: Basic Integer Sorting");
        logger.info(dash);
        int[] data1 = {64, 34, 25, 12, 22, 11, 90};
        logger.info("Original: " + Arrays.toString(data1));
        int[] result1 = bubbleSort(data1.clone());
        logger.info("Sorted:   " + Arrays.toString(result1));
        logger.info("");
        
        // Example 2: Already sorted
        logger.info("Example 2: Already Sorted Array");
        logger.info(dash);
        int[] data2 = {1, 2, 3, 4, 5, 6, 7};
        logger.info("Original: " + Arrays.toString(data2));
        int[] result2 = bubbleSort(data2.clone());
        logger.info("Sorted:   " + Arrays.toString(result2));
        logger.info("Note: O(n) with early termination!");
        logger.info("");
        
        // Example 3: Visualization
        logger.info("Example 3: Visualized Bubble Sort Process");
        logger.info(dash);
        int[] data3 = {5, 2, 8, 1, 9};
        bubbleSortVisualized(data3.clone());
        logger.info("");
        
        // Example 4: Performance
        logger.info("Example 4: Performance Measurement");
        logger.info(dash);
        
        Random rand = new Random(42);
        
        // Small
        int[] small = new int[100];
        for (int i = 0; i < small.length; i++) {
            small[i] = rand.nextInt(100);
        }
        long t1 = System.nanoTime();
        bubbleSort(small);
        long t2 = System.nanoTime();
        logger.info("Small (100 elements):");
        logger.info(String.format("  Time: %.3f ms%n", (t2-t1)/1_000_000.0));
        
        long endTime = System.nanoTime();
        
        logger.info("");
        logger.info(separator);
        logger.info("\nComplexity Summary:");
        logger.info("  Time:  O(n²) - average and worst");
        logger.info("         O(n) - best case (optimized)");
        logger.info("  Space: O(1)");
        logger.info("  Stable: Yes");
        logger.info("\nKey Advantages:");
        logger.info("  - Simple to understand");
        logger.info("  - Adaptive");
        logger.info("  - In-place");
        logger.info(separator);
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
