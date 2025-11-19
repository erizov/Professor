import java.util.ArrayList;
import java.util.List;

/**
 * B-Tree implementation.
 * 
 * Self-balancing tree optimized for disk I/O.
 * 
 * Time Complexity: O(log_t n) where t is minimum degree
 * Space Complexity: O(n)
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    static class BTreeNode {
        List<Integer> keys;
        List<BTreeNode> children;
        boolean leaf;
        
        BTreeNode(boolean leaf) {
            this.keys = new ArrayList<>();
            this.children = new ArrayList<>();
            this.leaf = leaf;
        }
    }
    
    static class BTree {
        BTreeNode root;
        int t; // Minimum degree
        
        BTree(int t) {
            this.root = new BTreeNode(true);
            this.t = t;
        }
        
        boolean search(int key) {
            return searchHelper(root, key);
        }
        
        private boolean searchHelper(BTreeNode node, int key) {
            int i = 0;
            while (i < node.keys.size() && key > node.keys.get(i)) {
                i++;
            }
            
            if (i < node.keys.size() && key == node.keys.get(i)) {
                return true;
            }
            
            if (node.leaf) {
                return false;
            }
            
            return searchHelper(node.children.get(i), key);
        }
        
        void insert(int key) {
            BTreeNode root = this.root;
            
            if (root.keys.size() >= 2 * t - 1) {
                BTreeNode newRoot = new BTreeNode(false);
                newRoot.children.add(this.root);
                this.root = newRoot;
                split(newRoot, 0);
                insertNonFull(newRoot, key);
            } else {
                insertNonFull(root, key);
            }
        }
        
        private void insertNonFull(BTreeNode node, int key) {
            int i = node.keys.size() - 1;
            
            if (node.leaf) {
                node.keys.add(0); // Placeholder
                while (i >= 0 && key < node.keys.get(i)) {
                    node.keys.set(i + 1, node.keys.get(i));
                    i--;
                }
                node.keys.set(i + 1, key);
            } else {
                while (i >= 0 && key < node.keys.get(i)) {
                    i--;
                }
                i++;
                
                if (node.children.get(i).keys.size() >= 2 * t - 1) {
                    split(node, i);
                    if (key > node.keys.get(i)) {
                        i++;
                    }
                }
                insertNonFull(node.children.get(i), key);
            }
        }
        
        private void split(BTreeNode parent, int index) {
            BTreeNode child = parent.children.get(index);
            BTreeNode newChild = new BTreeNode(child.leaf);
            
            int mid = t - 1;
            
            // Copy second half of keys
            for (int j = 0; j < t - 1; j++) {
                newChild.keys.add(child.keys.get(mid + 1 + j));
            }
            
            // Copy children if not leaf
            if (!child.leaf) {
                for (int j = 0; j < t; j++) {
                    newChild.children.add(child.children.get(mid + 1 + j));
                }
            }
            
            // Remove moved keys and children from child
            int midKey = child.keys.get(mid);
            child.keys.subList(mid, child.keys.size()).clear();
            if (!child.leaf) {
                child.children.subList(mid + 1, 
                                      child.children.size()).clear();
            }
            
            // Insert middle key and new child into parent
            parent.keys.add(index, midKey);
            parent.children.add(index + 1, newChild);
        }
        
        void printTree() {
            printTreeHelper(root, 0);
        }
        
        private void printTreeHelper(BTreeNode node, int level) {
            logger.info(" ".repeat(4 * level) + "→ " + 
                             node.keys);
            
            if (!node.leaf) {
                for (BTreeNode child : node.children) {
                    printTreeHelper(child, level + 1);
                }
            }
        }
        
        List<Integer> inorder() {
            List<Integer> result = new ArrayList<>();
            inorderHelper(root, result);
            return result;
        }
        
        private void inorderHelper(BTreeNode node, 
                                   List<Integer> result) {
            for (int i = 0; i < node.keys.size(); i++) {
                if (!node.leaf) {
                    inorderHelper(node.children.get(i), result);
                }
                result.add(node.keys.get(i));
            }
            
            if (!node.leaf) {
                inorderHelper(node.children.get(
                    node.children.size() - 1), result);
            }
        }
    }
    
    public static void main(String[] args) {
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        long startTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("B-TREE DEMONSTRATION");
        logger.info(separator);
        logger.info("");
        
        // Example 1
        logger.info("Example 1: Basic Insert and Search (t=3)");
        logger.info(dash);
        BTree btree = new BTree(3);
        int[] keys = {10, 20, 5, 6, 12, 30, 7, 17};
        
        System.out.print("Inserting: ");
        for (int key : keys) {
            System.out.print(key + " ");
            btree.insert(key);
        }
        
        logger.info("\n\nTree structure:");
        btree.printTree();
        
        logger.info("\nInorder: " + btree.inorder());
        logger.info("Search for 12: " + btree.search(12));
        logger.info("Search for 15: " + btree.search(15));
        logger.info("");
        
        // Example 2
        logger.info("Example 2: Larger Tree (t=2)");
        logger.info(dash);
        BTree btree2 = new BTree(2);
        
        System.out.print("Inserting 1-10: ");
        for (int i = 1; i <= 10; i++) {
            btree2.insert(i);
        }
        
        logger.info("\n\nTree structure:");
        btree2.printTree();
        logger.info("\nInorder: " + btree2.inorder());
        logger.info("");
        
        long endTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("\nComplexity Summary:");
        logger.info("  Time:  O(log_t n)");
        logger.info("  Space: O(n)");
        logger.info("\nKey Advantages:");
        logger.info("  - Optimized for disk I/O");
        logger.info("  - Used in databases");
        logger.info(separator);
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}