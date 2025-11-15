import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

/**
 * Binary Tree implementation.
 * 
 * Time Complexity: 
 *   Insert: O(n)
 *   Search: O(n)
 *   Traversal: O(n)
 * Space Complexity: O(n)
 */
public class Algorithm {
    
    /**
     * Node in a binary tree.
     */
    static class TreeNode {
        int val;
        TreeNode left;
        TreeNode right;
        
        TreeNode(int val) {
            this.val = val;
            this.left = null;
            this.right = null;
        }
    }
    
    /**
     * Binary Tree class.
     */
    static class BinaryTree {
        TreeNode root;
        
        BinaryTree() {
            this.root = null;
        }
        
        /**
         * Insert value (level-order).
         */
        void insert(int val) {
            if (root == null) {
                root = new TreeNode(val);
                return;
            }
            
            Queue<TreeNode> queue = new LinkedList<>();
            queue.add(root);
            
            while (!queue.isEmpty()) {
                TreeNode node = queue.poll();
                
                if (node.left == null) {
                    node.left = new TreeNode(val);
                    return;
                } else {
                    queue.add(node.left);
                }
                
                if (node.right == null) {
                    node.right = new TreeNode(val);
                    return;
                } else {
                    queue.add(node.right);
                }
            }
        }
        
        /**
         * Inorder traversal.
         */
        List<Integer> inorder() {
            List<Integer> result = new ArrayList<>();
            inorderHelper(root, result);
            return result;
        }
        
        private void inorderHelper(TreeNode node, List<Integer> result) {
            if (node != null) {
                inorderHelper(node.left, result);
                result.add(node.val);
                inorderHelper(node.right, result);
            }
        }
        
        /**
         * Preorder traversal.
         */
        List<Integer> preorder() {
            List<Integer> result = new ArrayList<>();
            preorderHelper(root, result);
            return result;
        }
        
        private void preorderHelper(TreeNode node, List<Integer> result) {
            if (node != null) {
                result.add(node.val);
                preorderHelper(node.left, result);
                preorderHelper(node.right, result);
            }
        }
        
        /**
         * Postorder traversal.
         */
        List<Integer> postorder() {
            List<Integer> result = new ArrayList<>();
            postorderHelper(root, result);
            return result;
        }
        
        private void postorderHelper(TreeNode node, List<Integer> result) {
            if (node != null) {
                postorderHelper(node.left, result);
                postorderHelper(node.right, result);
                result.add(node.val);
            }
        }
        
        /**
         * Level-order traversal.
         */
        List<Integer> levelOrder() {
            List<Integer> result = new ArrayList<>();
            if (root == null) return result;
            
            Queue<TreeNode> queue = new LinkedList<>();
            queue.add(root);
            
            while (!queue.isEmpty()) {
                TreeNode node = queue.poll();
                result.add(node.val);
                
                if (node.left != null) queue.add(node.left);
                if (node.right != null) queue.add(node.right);
            }
            
            return result;
        }
        
        /**
         * Calculate height.
         */
        int height() {
            return heightHelper(root);
        }
        
        private int heightHelper(TreeNode node) {
            if (node == null) return 0;
            return Math.max(heightHelper(node.left), 
                          heightHelper(node.right)) + 1;
        }
        
        /**
         * Count nodes.
         */
        int size() {
            return sizeHelper(root);
        }
        
        private int sizeHelper(TreeNode node) {
            if (node == null) return 0;
            return 1 + sizeHelper(node.left) + sizeHelper(node.right);
        }
        
        /**
         * Search for value.
         */
        boolean search(int val) {
            return searchHelper(root, val);
        }
        
        private boolean searchHelper(TreeNode node, int val) {
            if (node == null) return false;
            if (node.val == val) return true;
            return searchHelper(node.left, val) || 
                   searchHelper(node.right, val);
        }
    }
    
    /**
     * Main demonstration.
     */
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("BINARY TREE DEMONSTRATION");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Example 1: Basic operations
        System.out.println("Example 1: Building a Binary Tree");
        System.out.println("-".repeat(70));
        
        BinaryTree tree = new BinaryTree();
        int[] values = {1, 2, 3, 4, 5, 6, 7};
        
        System.out.println("Inserting values: " + 
                          java.util.Arrays.toString(values));
        for (int val : values) {
            tree.insert(val);
        }
        
        System.out.println("Tree size: " + tree.size());
        System.out.println("Tree height: " + tree.height());
        System.out.println();
        
        // Example 2: Traversals
        System.out.println("Example 2: Tree Traversals");
        System.out.println("-".repeat(70));
        
        System.out.println("Inorder:     " + tree.inorder());
        System.out.println("Preorder:    " + tree.preorder());
        System.out.println("Postorder:   " + tree.postorder());
        System.out.println("Level-order: " + tree.levelOrder());
        System.out.println();
        
        // Example 3: Search
        System.out.println("Example 3: Searching");
        System.out.println("-".repeat(70));
        
        int[] searchVals = {5, 10, 1, 8};
        for (int val : searchVals) {
            boolean found = tree.search(val);
            System.out.printf("Search %d: %s%n", val, 
                            found ? "Found" : "Not found");
        }
        System.out.println();
        
        // Example 4: Performance
        System.out.println("Example 4: Performance Measurement");
        System.out.println("-".repeat(70));
        
        int[] sizes = {100, 500, 1000};
        
        for (int size : sizes) {
            BinaryTree perfTree = new BinaryTree();
            
            long start = System.nanoTime();
            for (int i = 0; i < size; i++) {
                perfTree.insert(i);
            }
            long end = System.nanoTime();
            
            double ms = (end - start) / 1_000_000.0;
            System.out.printf("n=%4d: %8.3f ms, height=%d%n",
                            size, ms, perfTree.height());
        }
        
        System.out.println();
        System.out.println("=".repeat(70));
        System.out.println("\nComplexity Summary:");
        System.out.println("  Insertion: O(n)");
        System.out.println("  Search: O(n)");
        System.out.println("  Traversal: O(n)");
        System.out.println("  Space: O(n)");
        System.out.println("\nKey Points:");
        System.out.println("  + Simple hierarchical structure");
        System.out.println("  + Foundation for other trees");
        System.out.println("  + Natural recursive operations");
        System.out.println("  - No ordering guarantee");
        System.out.println("  - Search is O(n)");
        System.out.println("=".repeat(70));
        
        long endTime = System.nanoTime();
        double totalMs = (endTime - startTime) / 1_000_000.0;
        System.out.printf("\nTotal execution time: %.3f ms%n", totalMs);
    }
}
