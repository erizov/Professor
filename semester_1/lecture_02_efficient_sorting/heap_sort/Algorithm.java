import java.util.Arrays;
import java.util.Random;

/**
 * Heap Sort implementation.
 * 
 * Sorting algorithm based on binary heap data structure.
 * 
 * Time Complexity: O(n log n) - all cases
 * Space Complexity: O(1) - in-place
 * Stable: No
 * Adaptive: No
 */
public class Algorithm {
    
    /**
     * Heapify subtree rooted at index i.
     * 
     * @param arr Array to heapify
     * @param n Size of heap
     * @param i Root index of subtree
     */
    private static void heapify(int[] arr, int n, int i) {
        int largest = i;
        int left = 2 * i + 1;
        int right = 2 * i + 2;
        
        // Check left child
        if (left < n && arr[left] > arr[largest]) {
            largest = left;
        }
        
        // Check right child
        if (right < n && arr[right] > arr[largest]) {
            largest = right;
        }
        
        // If largest is not root
        if (largest != i) {
            int temp = arr[i];
            arr[i] = arr[largest];
            arr[largest] = temp;
            
            // Recursively heapify
            heapify(arr, n, largest);
        }
    }
    
    /**
     * Sort array using heap sort.
     * 
     * @param arr Array to be sorted
     * @return Sorted array
     */
    public static int[] heapSort(int[] arr) {
        int n = arr.length;
        
        // Build max heap
        for (int i = n / 2 - 1; i >= 0; i--) {
            heapify(arr, n, i);
        }
        
        // Extract elements from heap
        for (int i = n - 1; i > 0; i--) {
            // Move current root to end
            int temp = arr[0];
            arr[0] = arr[i];
            arr[i] = temp;
            
            // Heapify reduced heap
            heapify(arr, i, 0);
        }
        
        return arr;
    }
    
    /**
     * Heap sort with visualization.
     */
    public static int[] heapSortVisualized(int[] arr) {
        int n = arr.length;
        System.out.println("Initial array: " + Arrays.toString(arr));
        System.out.println();
        
        // Build max heap
        System.out.println("Building max heap:");
        for (int i = n / 2 - 1; i >= 0; i--) {
            heapify(arr, n, i);
            System.out.println("  After heapifying at index " + i + 
                             ": " + Arrays.toString(arr));
        }
        System.out.println("Max heap built: " + Arrays.toString(arr));
        System.out.println();
        
        // Extract elements
        System.out.println("Extracting elements:");
        for (int i = n - 1; i > 0; i--) {
            int temp = arr[0];
            arr[0] = arr[i];
            arr[i] = temp;
            
            System.out.print("  Moved " + arr[i] + 
                           " to position " + i + ": ");
            System.out.print(Arrays.toString(
                Arrays.copyOfRange(arr, 0, i)));
            System.out.println(" | [" + Arrays.toString(
                Arrays.copyOfRange(arr, i, n)) + "]");
            
            heapify(arr, i, 0);
            System.out.print("  After heapify: ");
            System.out.print(Arrays.toString(
                Arrays.copyOfRange(arr, 0, i)));
            System.out.println(" | [" + Arrays.toString(
                Arrays.copyOfRange(arr, i, n)) + "]");
        }
        
        System.out.println("\nFinal sorted array: " + 
                         Arrays.toString(arr));
        return arr;
    }
    
    /**
     * Sort in descending order using min heap.
     */
    public static int[] heapSortDescending(int[] arr) {
        int n = arr.length;
        
        // Build min heap
        for (int i = n / 2 - 1; i >= 0; i--) {
            minHeapify(arr, n, i);
        }
        
        // Extract elements
        for (int i = n - 1; i > 0; i--) {
            int temp = arr[0];
            arr[0] = arr[i];
            arr[i] = temp;
            
            minHeapify(arr, i, 0);
        }
        
        return arr;
    }
    
    /**
     * Min heapify for descending sort.
     */
    private static void minHeapify(int[] arr, int n, int i) {
        int smallest = i;
        int left = 2 * i + 1;
        int right = 2 * i + 2;
        
        if (left < n && arr[left] < arr[smallest]) {
            smallest = left;
        }
        if (right < n && arr[right] < arr[smallest]) {
            smallest = right;
        }
        
        if (smallest != i) {
            int temp = arr[i];
            arr[i] = arr[smallest];
            arr[smallest] = temp;
            minHeapify(arr, n, smallest);
        }
    }
    
    /**
     * Main method for demonstration.
     */
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("HEAP SORT DEMONSTRATION");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Example 1: Basic sorting
        System.out.println("Example 1: Basic Integer Sorting");
        System.out.println("-".repeat(70));
        int[] data1 = {64, 34, 25, 12, 22, 11, 90};
        System.out.println("Original: " + Arrays.toString(data1));
        int[] result1 = heapSort(data1.clone());
        System.out.println("Sorted:   " + Arrays.toString(result1));
        System.out.println();
        
        // Example 2: Already sorted
        System.out.println("Example 2: Already Sorted Array");
        System.out.println("-".repeat(70));
        int[] data2 = {1, 2, 3, 4, 5, 6, 7};
        System.out.println("Original: " + Arrays.toString(data2));
        int[] result2 = heapSort(data2.clone());
        System.out.println("Sorted:   " + Arrays.toString(result2));
        System.out.println("Note: Still O(n log n) - not adaptive");
        System.out.println();
        
        // Example 3: Descending
        System.out.println("Example 3: Descending Order");
        System.out.println("-".repeat(70));
        int[] data3 = {64, 34, 25, 12, 22, 11, 90};
        System.out.println("Original: " + Arrays.toString(data3));
        int[] result3 = heapSortDescending(data3.clone());
        System.out.println("Sorted (desc): " + Arrays.toString(result3));
        System.out.println();
        
        // Example 4: Visualization
        System.out.println("Example 4: Visualized Heap Sort Process");
        System.out.println("-".repeat(70));
        int[] data4 = {12, 11, 13, 5, 6, 7};
        heapSortVisualized(data4);
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
        heapSort(small);
        long t2 = System.nanoTime();
        System.out.println("Small (100 elements):");
        System.out.printf("  Time: %.3f ms%n", (t2-t1)/1_000_000.0);
        
        // Medium
        int[] medium = new int[1000];
        for (int i = 0; i < medium.length; i++) {
            medium[i] = rand.nextInt(1000);
        }
        t1 = System.nanoTime();
        heapSort(medium);
        t2 = System.nanoTime();
        System.out.println("\nMedium (1,000 elements):");
        System.out.printf("  Time: %.3f ms%n", (t2-t1)/1_000_000.0);
        
        long endTime = System.nanoTime();
        double duration = (endTime - startTime) / 1_000_000.0;
        
        System.out.println();
        System.out.println("=".repeat(70));
        System.out.println("\nComplexity Summary:");
        System.out.println("  Time:  O(n log n) - all cases");
        System.out.println("  Space: O(1) - in-place");
        System.out.println("  Stable: No");
        System.out.println("\nKey Advantages:");
        System.out.println("  - Guaranteed O(n log n)");
        System.out.println("  - In-place sorting");
        System.out.println("  - No worst-case quadratic time");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal execution time: %.3f ms%n", duration);
    }
}
