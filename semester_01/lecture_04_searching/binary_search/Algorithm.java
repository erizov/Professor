package semester_01.lecture_04_searching.binary_search;

/**
 * Binary Search implementation.
 *
 * Efficient search algorithm for sorted arrays using divide-and-conquer.
 */
import java.util.Arrays;

import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    /**
     * Search for target in sorted array using binary search (iterative).
     * 
     * Time Complexity: O(log n)
     * Space Complexity: O(1)
     */
    public static int binarySearch(int[] arr, int target) {
        int left = 0;
        int right = arr.length - 1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (arr[mid] == target) {
                return mid;
            } else if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return -1; // Not found
    }
    
    /**
     * Search for target in sorted array using binary search (recursive).
     * 
     * Time Complexity: O(log n)
     * Space Complexity: O(log n) for recursion stack
     */
    public static int binarySearchRecursive(int[] arr, int target, int left, int right) {
        if (left > right) {
            return -1; // Not found
        }
        
        int mid = left + (right - left) / 2;
        
        if (arr[mid] == target) {
            return mid;
        } else if (arr[mid] < target) {
            return binarySearchRecursive(arr, target, mid + 1, right);
        } else {
            return binarySearchRecursive(arr, target, left, mid - 1);
        }
    }
    
    /**
     * Find first occurrence of target (lower bound).
     */
    public static int binarySearchFirst(int[] arr, int target) {
        int left = 0;
        int right = arr.length - 1;
        int result = -1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (arr[mid] == target) {
                result = mid;
                right = mid - 1; // Continue searching left
            } else if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return result;
    }
    
    /**
     * Find last occurrence of target (upper bound).
     */
    public static int binarySearchLast(int[] arr, int target) {
        int left = 0;
        int right = arr.length - 1;
        int result = -1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (arr[mid] == target) {
                result = mid;
                left = mid + 1; // Continue searching right
            } else if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return result;
    }
    
    public static void main(String[] args) {
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        logger.info(separator);
        logger.info("BINARY SEARCH ALGORITHM DEMONSTRATION");
        logger.info(separator);
        logger.info("");
        
        // Example 1: Basic Binary Search
        logger.info("Example 1: Basic Binary Search");
        logger.info(dash);
        
        int[] arr1 = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19};
        int target1 = 7;
        
        logger.info("Array: " + Arrays.toString(arr1));
        logger.info("Target: " + target1);
        
        int index1 = binarySearch(arr1, target1);
        logger.info("Found at index: " + index1);
        logger.info("");
        
        // Example 2: Element Not Found
        logger.info("Example 2: Element Not Found");
        logger.info(dash);
        
        int target2 = 8;
        logger.info("Target: " + target2);
        
        int index2 = binarySearch(arr1, target2);
        logger.info("Found at index: " + index2 + " (not found)");
        logger.info("");
        
        // Example 3: Recursive Binary Search
        logger.info("Example 3: Recursive Binary Search");
        logger.info(dash);
        
        int target3 = 13;
        logger.info("Target: " + target3);
        
        int index3 = binarySearchRecursive(arr1, target3, 0, arr1.length - 1);
        logger.info("Found at index: " + index3);
        logger.info("");
        
        // Example 4: First Occurrence
        logger.info("Example 4: Find First Occurrence");
        logger.info(dash);
        
        int[] arr4 = {1, 2, 2, 2, 3, 4, 5};
        int target4 = 2;
        
        logger.info("Array: " + Arrays.toString(arr4));
        logger.info("Target: " + target4);
        
        int firstIdx = binarySearchFirst(arr4, target4);
        logger.info("First occurrence at index: " + firstIdx);
        logger.info("");
        
        // Example 5: Last Occurrence
        logger.info("Example 5: Find Last Occurrence");
        logger.info(dash);
        
        int lastIdx = binarySearchLast(arr4, target4);
        logger.info("Last occurrence at index: " + lastIdx);
        logger.info("");
        
        // Example 6: Performance measurement
        logger.info("Example 6: Performance Measurement");
        logger.info(dash);
        
        int[] largeArr = new int[1000000];
        for (int i = 0; i < largeArr.length; i++) {
            largeArr[i] = i * 2;
        }
        
        int target6 = 500000;
        long startTime = System.nanoTime();
        int index6 = binarySearch(largeArr, target6);
        long endTime = System.nanoTime();
        
        double executionTimeMs = (endTime - startTime) / 1_000_000.0;
        System.out.printf("Time to search in 1M elements: %.3f ms%n", executionTimeMs);
        logger.info("Found at index: " + index6);
        logger.info("");
        
        logger.info(separator);
        logger.info("\nAlgorithm Summary:");
        logger.info("\nIntent:");
        logger.info("  Efficient search algorithm for sorted arrays using");
        logger.info("  divide-and-conquer approach.");
        logger.info("\nTime Complexity: O(log n)");
        logger.info("Space Complexity: O(1) iterative, O(log n) recursive");
        logger.info("\nKey Advantages:");
        logger.info("  - Very fast for large sorted arrays");
        logger.info("  - Simple to implement");
        logger.info("  - Optimal for sorted data");
        logger.info("  - Can find first/last occurrence");
        logger.info("\nKey Disadvantages:");
        logger.info("  - Requires sorted array");
        logger.info("  - Not suitable for unsorted data");
        logger.info("  - Random access required");
        logger.info("\nWhen to Use:");
        logger.info("  - Searching in sorted arrays");
        logger.info("  - Finding insertion point");
        logger.info("  - Range queries");
        logger.info("  - When data is already sorted");
        logger.info("\nCommon Use Cases:");
        logger.info("  - Database indexes");
        logger.info("  - Search in sorted lists");
        logger.info("  - Finding boundaries");
        logger.info("  - Binary search trees");
        logger.info(separator);
    }
}
