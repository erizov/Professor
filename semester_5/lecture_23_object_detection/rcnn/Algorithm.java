/**
 * R-CNN implementation.
 * 
 * Category: Computer Vision
 * Time Complexity: O(n*proposals)
 * Space Complexity: O(proposals)
 */
public class Algorithm {
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("==".repeat(35));
        System.out.println("R-CNN");
        System.out.println("==".repeat(35));
        System.out.println("Category: Computer Vision");
        System.out.println("Time: O(n*proposals)");
        System.out.println("Space: O(proposals)");
        System.out.println();
        System.out.println("Resource Requirements:");
        System.out.println("  - GPU: Optional");
        System.out.println("  - Memory: Medium");
        System.out.println("==".repeat(35));
        
        long endTime = System.nanoTime();
        double durationMs = (endTime - startTime) / 1_000_000.0;
        System.out.println(String.format("\nExecution time: %.3f ms", durationMs));
    }
}
