package semester_01.lecture_02_efficient_sorting.quick_sort;

/**
 * Quick Sort implementation.
 *
 * Efficient divide-and-conquer sorting algorithm that picks a pivot
 * element and partitions the array around it.
 */
import java.util.Arrays;
import java.util.Random;

import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    /**
     * Sort array using quick sort algorithm.
     * 
     * Time Complexity:
     *   Best: O(n log n)
     *   Average: O(n log n)
     *   Worst: O(n²) - when pivot is always min/max
     * 
     * Space Complexity: O(log n) for recursion stack
     */
    public static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            // Partition and get pivot index
            int pivotIdx = partition(arr, low, high);
            
            // Recursively sort left and right subarrays
            quickSort(arr, low, pivotIdx - 1);
            quickSort(arr, pivotIdx + 1, high);
        }
    }
    
    /**
     * Partition array around pivot element.
     */
    private static int partition(int[] arr, int low, int high) {
        // Use last element as pivot
        int pivot = arr[high];
        int i = low - 1; // Index of smaller element
        
        for (int j = low; j < high; j++) {
            // If current element is smaller than or equal to pivot
            if (arr[j] <= pivot) {
                i++;
                swap(arr, i, j);
            }
        }
        
        // Place pivot in correct position
        swap(arr, i + 1, high);
        return i + 1;
    }
    
    /**
     * Swap two elements in array.
     */
    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
    
    /**
     * Quick sort with random pivot selection.
     */
    public static void quickSortRandom(int[] arr, int low, int high) {
        if (low < high) {
            // Random pivot selection
            Random random = new Random();
            int randomIdx = low + random.nextInt(high - low + 1);
            swap(arr, randomIdx, high);
            
            int pivotIdx = partition(arr, low, high);
            quickSortRandom(arr, low, pivotIdx - 1);
            quickSortRandom(arr, pivotIdx + 1, high);
        }
    }
    
    public static void main(String[] args) {
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        logger.info(separator);
        logger.info("QUICK SORT ALGORITHM DEMONSTRATION");
        logger.info(separator);
        logger.info("");
        
        // Example 1: Basic Quick Sort
        logger.info("Example 1: Basic Quick Sort");
        logger.info(dash);
        
        int[] arr1 = {64, 34, 25, 12, 22, 11, 90};
        logger.info("Original array: " + Arrays.toString(arr1));
        
        quickSort(arr1, 0, arr1.length - 1);
        logger.info("Sorted array: " + Arrays.toString(arr1));
        logger.info("");
        
        // Example 2: Quick Sort with Random Pivot
        logger.info("Example 2: Quick Sort with Random Pivot");
        logger.info(dash);
        
        int[] arr2 = {5, 2, 8, 1, 9, 3, 7, 4, 6};
        logger.info("Original array: " + Arrays.toString(arr2));
        
        quickSortRandom(arr2, 0, arr2.length - 1);
        logger.info("Sorted array: " + Arrays.toString(arr2));
        logger.info("");
        
        // Example 3: Already Sorted Array
        logger.info("Example 3: Already Sorted Array");
        logger.info(dash);
        
        int[] arr3 = {1, 2, 3, 4, 5};
        logger.info("Original array: " + Arrays.toString(arr3));
        
        quickSort(arr3, 0, arr3.length - 1);
        logger.info("Sorted array: " + Arrays.toString(arr3));
        logger.info("");
        
        // Example 4: Reverse Sorted Array
        logger.info("Example 4: Reverse Sorted Array");
        logger.info(dash);
        
        int[] arr4 = {5, 4, 3, 2, 1};
        logger.info("Original array: " + Arrays.toString(arr4));
        
        quickSort(arr4, 0, arr4.length - 1);
        logger.info("Sorted array: " + Arrays.toString(arr4));
        logger.info("");
        
        // Example 5: Performance measurement
        logger.info("Example 5: Performance Measurement");
        logger.info(dash);
        
        int[] largeArr = new int[1000];
        Random random = new Random();
        for (int i = 0; i < largeArr.length; i++) {
            largeArr[i] = random.nextInt(10000);
        }
        
        long startTime = System.nanoTime();
        quickSortRandom(largeArr, 0, largeArr.length - 1);
        long endTime = System.nanoTime();
        
        double executionTimeMs = (endTime - startTime) / 1_000_000.0;
        logger.info(String.format("Time to sort 1000 elements: %.3f ms%n", executionTimeMs));
        logger.info("");
        
        logger.info(separator);
        logger.info("\nAlgorithm Summary:");
        logger.info("\nIntent:");
        logger.info("  Efficient divide-and-conquer sorting algorithm that picks");
        logger.info("  a pivot element and partitions the array around it.");
        logger.info("\nTime Complexity:");
        logger.info("  Best: O(n log n)");
        logger.info("  Average: O(n log n)");
        logger.info("  Worst: O(n²) - when pivot is always min/max");
        logger.info("\nSpace Complexity: O(log n) for recursion stack");
        logger.info("\nKey Advantages:");
        logger.info("  - Fast average case performance");
        logger.info("  - In-place sorting");
        logger.info("  - Cache-friendly");
        logger.info("  - Widely used");
        logger.info("\nKey Disadvantages:");
        logger.info("  - Worst case O(n²)");
        logger.info("  - Not stable");
        logger.info("  - Recursive (stack space)");
        logger.info("\nWhen to Use:");
        logger.info("  - General-purpose sorting");
        logger.info("  - When average performance matters");
        logger.info("  - Large datasets");
        logger.info("  - When stability not required");
        logger.info(separator);
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(50));
        System.out.println("Quick Sort Algorithm Test");
        System.out.println("=".repeat(50));

        try {
            // Validate input
            if (args.length > 0) {
                System.out.println("Note: Command line arguments ignored. Using sample data.");
            }

            // Test with sample data
            int[] testArray = {64, 34, 25, 12, 22, 11, 90};
            System.out.println("Original array: " + java.util.Arrays.toString(testArray));

            // Validate array
            if (testArray == null || testArray.length == 0) {
                throw new IllegalArgumentException("Array cannot be null or empty");
            }

            Algorithm algo = new Algorithm();
            long startTime = System.nanoTime();
            algo.quickSort(testArray, 0, testArray.length - 1);
            long endTime = System.nanoTime();

            System.out.println("Sorted array:   " + java.util.Arrays.toString(testArray));
            System.out.printf("Execution time: %.3f ms%n", (endTime - startTime) / 1_000_000.0);
            System.out.println("Status: SUCCESS");

        } catch (IllegalArgumentException e) {
            System.err.println("Input validation error: " + e.getMessage());
            System.exit(1);
        } catch (Exception e) {
            System.err.println("Error running algorithm: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }

        System.out.println("=".repeat(50));
    }
}
