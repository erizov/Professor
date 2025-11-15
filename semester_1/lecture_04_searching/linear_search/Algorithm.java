public class Algorithm {
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
        System.out.println("Linear Search - O(n)");
        System.out.println("Found at index: " + result);
    }
}
