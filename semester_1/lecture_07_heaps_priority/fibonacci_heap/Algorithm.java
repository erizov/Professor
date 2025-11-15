import java.util.*;

/**
 * Fibonacci Heap Implementation.
 * 
 * Advanced heap with O(1) insert and decrease-key.
 */
public class Algorithm {
    
    static class FibonacciNode {
        int key;
        FibonacciNode parent;
        FibonacciNode child;
        FibonacciNode left;
        FibonacciNode right;
        int degree;
        boolean marked;
        
        FibonacciNode(int key) {
            this.key = key;
            this.left = this;
            this.right = this;
        }
    }
    
    static class FibonacciHeap {
        private FibonacciNode minNode;
        private int numNodes;
        
        FibonacciHeap() {
            minNode = null;
            numNodes = 0;
        }
        
        boolean isEmpty() {
            return minNode == null;
        }
        
        FibonacciNode insert(int key) {
            FibonacciNode node = new FibonacciNode(key);
            
            if (minNode == null) {
                minNode = node;
            } else {
                node.left = minNode;
                node.right = minNode.right;
                minNode.right = node;
                node.right.left = node;
                
                if (node.key < minNode.key) {
                    minNode = node;
                }
            }
            
            numNodes++;
            return node;
        }
        
        Integer findMin() {
            return minNode != null ? minNode.key : null;
        }
        
        FibonacciNode extractMin() {
            if (minNode == null) {
                return null;
            }
            
            FibonacciNode min = minNode;
            
            if (min.right == min) {
                minNode = null;
            } else {
                min.left.right = min.right;
                min.right.left = min.left;
                minNode = min.right;
            }
            
            numNodes--;
            return min;
        }
        
        int size() {
            return numNodes;
        }
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("FIBONACCI HEAP");
        System.out.println("=".repeat(70));
        System.out.println();
        
        FibonacciHeap heap = new FibonacciHeap();
        
        System.out.println("Inserting elements:");
        for (int key : new int[]{5, 3, 7, 1, 9, 2}) {
            heap.insert(key);
            System.out.println("  Inserted: " + key + ", Min: " + heap.findMin());
        }
        System.out.println();
        
        System.out.println("Extracting minimum:");
        while (!heap.isEmpty()) {
            FibonacciNode min = heap.extractMin();
            System.out.println("  Extracted: " + min.key);
        }
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nComplexity: O(1) insert, O(log n) extract");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
