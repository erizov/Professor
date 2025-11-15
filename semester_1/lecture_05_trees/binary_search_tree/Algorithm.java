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
public class Algorithm {
    
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
        
        System.out.println("=".repeat(70));
        System.out.println("BINARY SEARCH TREE DEMONSTRATION");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Example 1
        System.out.println("Example 1: Building a BST");
        System.out.println("-".repeat(70));
        
        BST bst = new BST();
        int[] values = {50, 30, 70, 20, 40, 60, 80};
        
        System.out.println("Inserting: " + Arrays.toString(values));
        for (int val : values) {
            bst.insert(val);
        }
        
        System.out.println("Size: " + bst.size());
        System.out.println("Height: " + bst.height());
        System.out.println("Inorder (sorted): " + bst.inorder());
        System.out.println();
        
        // Example 2: Search
        System.out.println("Example 2: Searching");
        System.out.println("-".repeat(70));
        
        int[] searchVals = {40, 25, 70, 100};
        for (int val : searchVals) {
            System.out.printf("Search %d: %s%n", val,
                            bst.search(val) ? "Found" : "Not found");
        }
        System.out.println();
        
        // Example 3: Deletion
        System.out.println("Example 3: Deletion");
        System.out.println("-".repeat(70));
        
        System.out.println("Before: " + bst.inorder());
        bst.delete(20);
        System.out.println("After deleting 20: " + bst.inorder());
        bst.delete(30);
        System.out.println("After deleting 30: " + bst.inorder());
        bst.delete(50);
        System.out.println("After deleting 50: " + bst.inorder());
        System.out.println();
        
        // Example 4: Performance
        System.out.println("Example 4: Performance (Random Insertion)");
        System.out.println("-".repeat(70));
        
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
        
        System.out.println();
        System.out.println("=".repeat(70));
        System.out.println("\nComplexity Summary:");
        System.out.println("  Search/Insert/Delete: O(h)");
        System.out.println("  Balanced: O(log n)");
        System.out.println("  Unbalanced: O(n)");
        System.out.println("\nKey Points:");
        System.out.println("  + Fast operations if balanced");
        System.out.println("  + Inorder = sorted");
        System.out.println("  + Simple implementation");
        System.out.println("  - Can become unbalanced");
        System.out.println("  - Worst case O(n)");
        System.out.println("=".repeat(70));
        
        long endTime = System.nanoTime();
        double totalMs = (endTime - startTime) / 1_000_000.0;
        System.out.printf("\nTotal execution time: %.3f ms%n", totalMs);
    }
}
