// package semester_01.lecture_02_efficient_sorting.quick_sort;

import java.util.Arrays;
import java.util.logging.Logger;

/**
 * Quick Sort implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());
    private static final String DASH = "--------------------------------------------------";
    
    public static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pivotIdx = partition(arr, low, high);
            quickSort(arr, low, pivotIdx - 1);
            quickSort(arr, pivotIdx + 1, high);
        }
    }
    
    private static int partition(int[] arr, int low, int high) {
        int pivot = arr[high];
        int i = low - 1;
        
        for (int j = low; j < high; j++) {
            if (arr[j] <= pivot) {
                i++;
                int temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }
        
        int temp = arr[i + 1];
        arr[i + 1] = arr[high];
        arr[high] = temp;
        
        return i + 1;
    }
    
    public static void main(String[] args) {
        logger.info("Quick Sort Demonstration");
        logger.info(DASH);
        
        int[] arr1 = {64, 34, 25, 12, 22, 11, 90};
        logger.info("Original: " + Arrays.toString(arr1));
        quickSort(arr1, 0, arr1.length - 1);
        logger.info("Sorted: " + Arrays.toString(arr1));
        
        logger.info(DASH);
        
        int[] arr2 = {5, 2, 8, 1, 9};
        logger.info("Original: " + Arrays.toString(arr2));
        quickSort(arr2, 0, arr2.length - 1);
        logger.info("Sorted: " + Arrays.toString(arr2));
    }
}