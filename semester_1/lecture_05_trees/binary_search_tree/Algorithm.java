import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;

/**
 * Binary Search Tree implementation.
 * 
 * Time Complexity: O(h) where h is height
 *   Balanced: O(log n)
 *   Unbalanced: O(n)
 * Space Complexity: O(n)
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    static class TreeNode {
        int val;
        TreeNode left;
        TreeNode right;
        
        TreeNode(int val) {
            this.val = val;
        }
    }
    
    static class BST {
        TreeNode root;
        
        void insert(int val) {
            root = insertRec(root, val);
        }
        
        private TreeNode insertRec(TreeNode node, int val) {
            if (node == null) {
                return new TreeNode(val);
            }
            
            if (val < node.val) {
                node.left = insertRec(node.left, val);
            } else {
                node.right = insertRec(node.right, val);
            }
            
            return node;
        }
        
        boolean search(int val) {
            return searchRec(root, val);
        }
        
        private boolean searchRec(TreeNode node, int val) {
            if (node == null) return false;
            if (node.val == val) return true;
            
            if (val < node.val) {
                return searchRec(node.left, val);
            } else {
                return searchRec(node.right, val);
            }
        }
        
        void delete(int val) {
            root = deleteRec(root, val);
        }
        
        private TreeNode deleteRec(TreeNode node, int val) {
            if (node == null) return null;
            
            if (val < node.val) {
                node.left = deleteRec(node.left, val);
            } else if (val > node.val) {
                node.right = deleteRec(node.right, val);
            } else {
                // Node found
                if (node.left == null) return node.right;
                if (node.right == null) return node.left;
                
                // Two children: get inorder successor
                TreeNode min = findMin(node.right);
                node.val = min.val;
                node.right = deleteRec(node.right, min.val);
            }
            
            return node;
        }
        
        private TreeNode findMin(TreeNode node) {
            while (node.left != null) {
                node = node.left;
            }
            return node;
        }
        
        List<Integer> inorder() {
            List<Integer> result = new ArrayList<>();
            inorderRec(root, result);
            return result;
        }
        
        private void inorderRec(TreeNode node, List<Integer> result) {
            if (node != null) {
                inorderRec(node.left, result);
                result.add(node.val);
                inorderRec(node.right, result);
            }
        }
        
        int height() {
            return heightRec(root);
        }
        
        private int heightRec(TreeNode node) {
            if (node == null) return 0;
            return Math.max(heightRec(node.left), 
                          heightRec(node.right)) + 1;
        }
        
        int size() {
            return sizeRec(root);
        }
        
        private int sizeRec(TreeNode node) {
            if (node == null) return 0;
            return 1 + sizeRec(node.left) + sizeRec(node.right);
        }
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        logger.info("=".repeat(70));
        logger.info("BINARY SEARCH TREE DEMONSTRATION");
        logger.info("=".repeat(70));
        logger.info();
        
        // Example 1
        logger.info("Example 1: Building a BST");
        logger.info("-".repeat(70));
        
        BST bst = new BST();
        int[] values = {50, 30, 70, 20, 40, 60, 80};
        
        logger.info("Inserting: " + Arrays.toString(values));
        for (int val : values) {
            bst.insert(val);
        }
        
        logger.info("Size: " + bst.size());
        logger.info("Height: " + bst.height());
        logger.info("Inorder (sorted): " + bst.inorder());
        logger.info();
        
        // Example 2: Search
        logger.info("Example 2: Searching");
        logger.info("-".repeat(70));
        
        int[] searchVals = {40, 25, 70, 100};
        for (int val : searchVals) {
            System.out.printf("Search %d: %s%n", val,
                            bst.search(val) ? "Found" : "Not found");
        }
        logger.info();
        
        // Example 3: Deletion
        logger.info("Example 3: Deletion");
        logger.info("-".repeat(70));
        
        logger.info("Before: " + bst.inorder());
        bst.delete(20);
        logger.info("After deleting 20: " + bst.inorder());
        bst.delete(30);
        logger.info("After deleting 30: " + bst.inorder());
        bst.delete(50);
        logger.info("After deleting 50: " + bst.inorder());
        logger.info();
        
        // Example 4: Performance
        logger.info("Example 4: Performance (Random Insertion)");
        logger.info("-".repeat(70));
        
        int[] sizes = {100, 500, 1000};
        Random rand = new Random(42);
        
        for (int size : sizes) {
            List<Integer> vals = new ArrayList<>();
            for (int i = 0; i < size; i++) {
                vals.add(i);
            }
            Collections.shuffle(vals, rand);
            
            BST perfBst = new BST();
            long start = System.nanoTime();
            for (int val : vals) {
                perfBst.insert(val);
            }
            long end = System.nanoTime();
            
            double ms = (end - start) / 1_000_000.0;
            System.out.printf("n=%4d: %8.3f ms, height=%d%n",
                            size, ms, perfBst.height());
        }
        
        logger.info();
        logger.info("=".repeat(70));
        logger.info("\nComplexity Summary:");
        logger.info("  Search/Insert/Delete: O(h)");
        logger.info("  Balanced: O(log n)");
        logger.info("  Unbalanced: O(n)");
        logger.info("\nKey Points:");
        logger.info("  + Fast operations if balanced");
        logger.info("  + Inorder = sorted");
        logger.info("  + Simple implementation");
        logger.info("  - Can become unbalanced");
        logger.info("  - Worst case O(n)");
        logger.info("=".repeat(70));
        
        long endTime = System.nanoTime();
        double totalMs = (endTime - startTime) / 1_000_000.0;
        System.out.printf("\nTotal execution time: %.3f ms%n", totalMs);
    }
}