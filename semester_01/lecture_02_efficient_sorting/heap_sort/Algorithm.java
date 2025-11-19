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
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
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
        logger.info("Initial array: " + Arrays.toString(arr));
        logger.info("");
        
        // Build max heap
        logger.info("Building max heap:");
        for (int i = n / 2 - 1; i >= 0; i--) {
            heapify(arr, n, i);
            logger.info("  After heapifying at index " + i + 
                             ": " + Arrays.toString(arr));
        }
        logger.info("Max heap built: " + Arrays.toString(arr));
        logger.info("");
        
        // Extract elements
        logger.info("Extracting elements:");
        for (int i = n - 1; i > 0; i--) {
            int temp = arr[0];
            arr[0] = arr[i];
            arr[i] = temp;
            
            System.out.print("  Moved " + arr[i] + 
                           " to position " + i + ": ");
            System.out.print(Arrays.toString(
                Arrays.copyOfRange(arr, 0, i)));
            logger.info(" | [" + Arrays.toString(
                Arrays.copyOfRange(arr, i, n)) + "]");
            
            heapify(arr, i, 0);
            System.out.print("  After heapify: ");
            System.out.print(Arrays.toString(
                Arrays.copyOfRange(arr, 0, i)));
            logger.info(" | [" + Arrays.toString(
                Arrays.copyOfRange(arr, i, n)) + "]");
        }
        
        logger.info("\nFinal sorted array: " + 
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
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        long startTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("HEAP SORT DEMONSTRATION");
        logger.info(separator);
        logger.info("");
        
        // Example 1: Basic sorting
        logger.info("Example 1: Basic Integer Sorting");
        logger.info(dash);
        int[] data1 = {64, 34, 25, 12, 22, 11, 90};
        logger.info("Original: " + Arrays.toString(data1));
        int[] result1 = heapSort(data1.clone());
        logger.info("Sorted:   " + Arrays.toString(result1));
        logger.info("");
        
        // Example 2: Already sorted
        logger.info("Example 2: Already Sorted Array");
        logger.info(dash);
        int[] data2 = {1, 2, 3, 4, 5, 6, 7};
        logger.info("Original: " + Arrays.toString(data2));
        int[] result2 = heapSort(data2.clone());
        logger.info("Sorted:   " + Arrays.toString(result2));
        logger.info("Note: Still O(n log n) - not adaptive");
        logger.info("");
        
        // Example 3: Descending
        logger.info("Example 3: Descending Order");
        logger.info(dash);
        int[] data3 = {64, 34, 25, 12, 22, 11, 90};
        logger.info("Original: " + Arrays.toString(data3));
        int[] result3 = heapSortDescending(data3.clone());
        logger.info("Sorted (desc): " + Arrays.toString(result3));
        logger.info("");
        
        // Example 4: Visualization
        logger.info("Example 4: Visualized Heap Sort Process");
        logger.info(dash);
        int[] data4 = {12, 11, 13, 5, 6, 7};
        heapSortVisualized(data4);
        logger.info("");
        
        // Example 5: Performance
        logger.info("Example 5: Performance Measurement");
        logger.info(dash);
        
        Random rand = new Random(42);
        
        // Small
        int[] small = new int[100];
        for (int i = 0; i < small.length; i++) {
            small[i] = rand.nextInt(100);
        }
        long t1 = System.nanoTime();
        heapSort(small);
        long t2 = System.nanoTime();
        logger.info("Small (100 elements):");
        System.out.printf("  Time: %.3f ms%n", (t2-t1)/1_000_000.0);
        
        // Medium
        int[] medium = new int[1000];
        for (int i = 0; i < medium.length; i++) {
            medium[i] = rand.nextInt(1000);
        }
        t1 = System.nanoTime();
        heapSort(medium);
        t2 = System.nanoTime();
        logger.info("\nMedium (1,000 elements):");
        System.out.printf("  Time: %.3f ms%n", (t2-t1)/1_000_000.0);
        
        long endTime = System.nanoTime();
        double duration = (endTime - startTime) / 1_000_000.0;
        
        logger.info("");
        logger.info(separator);
        logger.info("\nComplexity Summary:");
        logger.info("  Time:  O(n log n) - all cases");
        logger.info("  Space: O(1) - in-place");
        logger.info("  Stable: No");
        logger.info("\nKey Advantages:");
        logger.info("  - Guaranteed O(n log n)");
        logger.info("  - In-place sorting");
        logger.info("  - No worst-case quadratic time");
        logger.info(separator);
        System.out.printf("\nTotal execution time: %.3f ms%n", duration);
    }
}