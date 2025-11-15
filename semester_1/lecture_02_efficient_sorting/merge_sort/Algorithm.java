import java.util.Arrays;
import java.util.Random;

/**
 * Merge Sort implementation.
 * 
 * Efficient divide-and-conquer sorting algorithm.
 * 
 * Time Complexity: O(n log n) - all cases
 * Space Complexity: O(n)
 * Stable: Yes
 * Adaptive: No
 */
public class Algorithm {
    
    /**
     * Sort array using merge sort.
     * 
     * @param arr Array to be sorted
     * @return Sorted array
     */
    public static int[] mergeSort(int[] arr) {
        if (arr.length <= 1) {
            return arr;
        }
        
        // Divide
        int mid = arr.length / 2;
        int[] left = Arrays.copyOfRange(arr, 0, mid);
        int[] right = Arrays.copyOfRange(arr, mid, arr.length);
        
        // Conquer
        left = mergeSort(left);
        right = mergeSort(right);
        
        // Merge
        return merge(left, right);
    }
    
    /**
     * Merge two sorted arrays.
     * 
     * @param left First sorted array
     * @param right Second sorted array
     * @return Merged sorted array
     */
    private static int[] merge(int[] left, int[] right) {
        int[] result = new int[left.length + right.length];
        int i = 0, j = 0, k = 0;
        
        // Compare and merge
        while (i < left.length && j < right.length) {
            if (left[i] <= right[j]) {
                result[k++] = left[i++];
            } else {
                result[k++] = right[j++];
            }
        }
        
        // Copy remaining elements
        while (i < left.length) {
            result[k++] = left[i++];
        }
        while (j < right.length) {
            result[k++] = right[j++];
        }
        
        return result;
    }
    
    /**
     * In-place merge sort.
     * 
     * @param arr Array to be sorted
     */
    public static void mergeSortInPlace(int[] arr) {
        if (arr.length <= 1) return;
        mergeSortHelper(arr, 0, arr.length);
    }
    
    /**
     * Helper method for in-place merge sort.
     */
    private static void mergeSortHelper(int[] arr, int start, int end) {
        if (end - start <= 1) return;
        
        int mid = (start + end) / 2;
        mergeSortHelper(arr, start, mid);
        mergeSortHelper(arr, mid, end);
        mergeInPlace(arr, start, mid, end);
    }
    
    /**
     * Merge subarrays in place.
     */
    private static void mergeInPlace(int[] arr, int start, 
                                     int mid, int end) {
        int[] temp = new int[end - start];
        int i = start, j = mid, k = 0;
        
        while (i < mid && j < end) {
            if (arr[i] <= arr[j]) {
                temp[k++] = arr[i++];
            } else {
                temp[k++] = arr[j++];
            }
        }
        
        while (i < mid) temp[k++] = arr[i++];
        while (j < end) temp[k++] = arr[j++];
        
        // Copy back
        System.arraycopy(temp, 0, arr, start, temp.length);
    }
    
    /**
     * Merge sort with visualization.
     */
    public static int[] visualizeMergeSort(int[] arr, int depth) {
        String indent = "  ".repeat(depth);
        System.out.println(indent + "Sorting: " + 
                         Arrays.toString(arr));
        
        if (arr.length <= 1) {
            System.out.println(indent + "Base case: " + 
                             Arrays.toString(arr));
            return arr;
        }
        
        int mid = arr.length / 2;
        System.out.println(indent + "Dividing at index " + mid);
        
        int[] left = Arrays.copyOfRange(arr, 0, mid);
        int[] right = Arrays.copyOfRange(arr, mid, arr.length);
        
        left = visualizeMergeSort(left, depth + 1);
        right = visualizeMergeSort(right, depth + 1);
        
        int[] result = merge(left, right);
        System.out.println(indent + "Merged: " + 
                         Arrays.toString(result));
        
        return result;
    }
    
    /**
     * Main method for demonstration.
     */
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("MERGE SORT DEMONSTRATION");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Example 1: Basic sorting
        System.out.println("Example 1: Basic Integer Sorting");
        System.out.println("-".repeat(70));
        int[] data1 = {64, 34, 25, 12, 22, 11, 90, 88};
        System.out.println("Original: " + Arrays.toString(data1));
        int[] result1 = mergeSort(data1.clone());
        System.out.println("Sorted:   " + Arrays.toString(result1));
        System.out.println();
        
        // Example 2: Already sorted
        System.out.println("Example 2: Already Sorted Array");
        System.out.println("-".repeat(70));
        int[] data2 = {1, 2, 3, 4, 5, 6, 7, 8};
        System.out.println("Original: " + Arrays.toString(data2));
        int[] result2 = mergeSort(data2.clone());
        System.out.println("Sorted:   " + Arrays.toString(result2));
        System.out.println("Note: Still O(n log n) even when sorted!");
        System.out.println();
        
        // Example 3: Reverse sorted
        System.out.println("Example 3: Reverse Sorted Array");
        System.out.println("-".repeat(70));
        int[] data3 = {8, 7, 6, 5, 4, 3, 2, 1};
        System.out.println("Original: " + Arrays.toString(data3));
        int[] result3 = mergeSort(data3.clone());
        System.out.println("Sorted:   " + Arrays.toString(result3));
        System.out.println();
        
        // Example 4: Visualization
        System.out.println("Example 4: Visualized Merge Sort Process");
        System.out.println("-".repeat(70));
        System.out.println("Watch the divide-and-conquer process:\n");
        int[] data4 = {5, 2, 8, 1, 9, 3};
        visualizeMergeSort(data4, 0);
        System.out.println();
        
        // Example 5: Performance
        System.out.println("Example 5: Performance Measurement");
        System.out.println("-".repeat(70));
        
        Random rand = new Random(42);
        
        // Small
        int[] small = new int[100];
        for (int i = 0; i < small.length; i++) {
            small[i] = rand.nextInt(100);
        }
        long t1 = System.nanoTime();
        mergeSort(small);
        long t2 = System.nanoTime();
        System.out.println("Small (100 elements):");
        System.out.printf("  Time: %.3f ms%n", (t2-t1)/1_000_000.0);
        
        // Medium
        int[] medium = new int[1000];
        for (int i = 0; i < medium.length; i++) {
            medium[i] = rand.nextInt(1000);
        }
        t1 = System.nanoTime();
        mergeSort(medium);
        t2 = System.nanoTime();
        System.out.println("\nMedium (1,000 elements):");
        System.out.printf("  Time: %.3f ms%n", (t2-t1)/1_000_000.0);
        
        // Large
        int[] large = new int[10000];
        for (int i = 0; i < large.length; i++) {
            large[i] = rand.nextInt(10000);
        }
        t1 = System.nanoTime();
        mergeSort(large);
        t2 = System.nanoTime();
        System.out.println("\nLarge (10,000 elements):");
        System.out.printf("  Time: %.3f ms%n", (t2-t1)/1_000_000.0);
        System.out.println();
        
        // Example 6: In-place
        System.out.println("Example 6: In-place Merge Sort");
        System.out.println("-".repeat(70));
        int[] data6 = {64, 34, 25, 12, 22, 11, 90};
        System.out.println("Original: " + Arrays.toString(data6));
        mergeSortInPlace(data6);
        System.out.println("Sorted:   " + Arrays.toString(data6));
        System.out.println();
        
        long endTime = System.nanoTime();
        double duration = (endTime - startTime) / 1_000_000.0;
        
        System.out.println("=".repeat(70));
        System.out.println("\nComplexity Summary:");
        System.out.println("  Time:  O(n log n) - all cases");
        System.out.println("  Space: O(n) - auxiliary array");
        System.out.println("  Stable: Yes");
        System.out.println("\nKey Advantages:");
        System.out.println("  - Guaranteed O(n log n)");
        System.out.println("  - Stable sorting");
        System.out.println("  - Good for linked lists");
        System.out.println("  - Parallelizable");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal execution time: %.3f ms%n", duration);
    }
}
