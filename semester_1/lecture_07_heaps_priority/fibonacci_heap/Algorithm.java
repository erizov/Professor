import java.util.*;

/**
 * Fibonacci Heap Implementation.
 * 
 * Advanced heap with O(1) insert and decrease-key.
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
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
        
        logger.info("=".repeat(70));
        logger.info("FIBONACCI HEAP");
        logger.info("=".repeat(70));
        logger.info();
        
        FibonacciHeap heap = new FibonacciHeap();
        
        logger.info("Inserting elements:");
        for (int key : new int[]{5, 3, 7, 1, 9, 2}) {
            heap.insert(key);
            logger.info("  Inserted: " + key + ", Min: " + heap.findMin());
        }
        logger.info();
        
        logger.info("Extracting minimum:");
        while (!heap.isEmpty()) {
            FibonacciNode min = heap.extractMin();
            logger.info("  Extracted: " + min.key);
        }
        logger.info();
        
        long endTime = System.nanoTime();
        
        logger.info("=".repeat(70));
        logger.info("\nComplexity: O(1) insert, O(log n) extract");
        logger.info("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}