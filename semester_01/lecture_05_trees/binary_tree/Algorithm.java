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
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
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
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        long startTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("BINARY TREE DEMONSTRATION");
        logger.info(separator);
        logger.info("");
        
        // Example 1: Basic operations
        logger.info("Example 1: Building a Binary Tree");
        logger.info(dash);
        
        BinaryTree tree = new BinaryTree();
        int[] values = {1, 2, 3, 4, 5, 6, 7};
        
        logger.info("Inserting values: " + 
                          java.util.Arrays.toString(values));
        for (int val : values) {
            tree.insert(val);
        }
        
        logger.info("Tree size: " + tree.size());
        logger.info("Tree height: " + tree.height());
        logger.info("");
        
        // Example 2: Traversals
        logger.info("Example 2: Tree Traversals");
        logger.info(dash);
        
        logger.info("Inorder:     " + tree.inorder());
        logger.info("Preorder:    " + tree.preorder());
        logger.info("Postorder:   " + tree.postorder());
        logger.info("Level-order: " + tree.levelOrder());
        logger.info("");
        
        // Example 3: Search
        logger.info("Example 3: Searching");
        logger.info(dash);
        
        int[] searchVals = {5, 10, 1, 8};
        for (int val : searchVals) {
            boolean found = tree.search(val);
            System.out.printf("Search %d: %s%n", val, 
                            found ? "Found" : "Not found");
        }
        logger.info("");
        
        // Example 4: Performance
        logger.info("Example 4: Performance Measurement");
        logger.info(dash);
        
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
        
        logger.info("");
        logger.info(separator);
        logger.info("\nComplexity Summary:");
        logger.info("  Insertion: O(n)");
        logger.info("  Search: O(n)");
        logger.info("  Traversal: O(n)");
        logger.info("  Space: O(n)");
        logger.info("\nKey Points:");
        logger.info("  + Simple hierarchical structure");
        logger.info("  + Foundation for other trees");
        logger.info("  + Natural recursive operations");
        logger.info("  - No ordering guarantee");
        logger.info("  - Search is O(n)");
        logger.info(separator);
        
        long endTime = System.nanoTime();
        double totalMs = (endTime - startTime) / 1_000_000.0;
        System.out.printf("\nTotal execution time: %.3f ms%n", totalMs);
    }
}