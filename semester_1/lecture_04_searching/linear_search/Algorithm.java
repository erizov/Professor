import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public static int linearSearch(int[] arr, int target) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) {
                return i;
            }
        }
        return -1;
    }
    
    public static void main(String[] args) {
        int[] data = {64, 34, 25, 12, 22, 11, 90};
        int target = 22;
        
        int result = linearSearch(data, target);
        logger.info("Linear Search - O(n)");
        logger.info("Found at index: " + result);
    }
}