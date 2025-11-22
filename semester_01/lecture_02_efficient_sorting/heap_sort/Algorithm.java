// package semester_01.lecture_02_efficient_sorting.heap_sort;

import java.util.Arrays;
import java.util.logging.Logger;

/**
 * Heap Sort implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());
    
    private static void heapify(int[] arr, int n, int i) {
        int largest = i;
        int left = 2 * i + 1;
        int right = 2 * i + 2;
        
        if (left < n && arr[left] > arr[largest]) {
            largest = left;
        }
        
        if (right < n && arr[right] > arr[largest]) {
            largest = right;
        }
        
        if (largest != i) {
            int temp = arr[i];
            arr[i] = arr[largest];
            arr[largest] = temp;
            heapify(arr, n, largest);
        }
    }
    
    public static void heapSort(int[] arr) {
        int n = arr.length;
        
        for (int i = n / 2 - 1; i >= 0; i--) {
            heapify(arr, n, i);
        }
        
        for (int i = n - 1; i > 0; i--) {
            int temp = arr[0];
            arr[0] = arr[i];
            arr[i] = temp;
            heapify(arr, i, 0);
        }
    }
    
    public static void main(String[] args) {
        logger.info("Heap Sort Demonstration");
        logger.info("==================================================");
        
        int[] arr1 = {64, 34, 25, 12, 22, 11, 90};
        logger.info("Original: " + Arrays.toString(arr1));
        heapSort(arr1);
        logger.info("Sorted: " + Arrays.toString(arr1));
        
        int[] arr2 = {5, 2, 8, 1, 9};
        logger.info("Original: " + Arrays.toString(arr2));
        heapSort(arr2);
        logger.info("Sorted: " + Arrays.toString(arr2));
    }
}