/**
 * Red-Black Tree implementation.
 * 
 * Self-balancing BST with color property.
 * 
 * Time Complexity: O(log n) - all operations
 * Space Complexity: O(n)
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    enum Color {
        RED, BLACK
    }
    
    static class RBNode {
        int key;
        Color color;
        RBNode left, right, parent;
        
        RBNode(int key) {
            this.key = key;
            this.color = Color.RED;
        }
    }
    
    static class RedBlackTree {
        private final RBNode NIL;
        private RBNode root;
        
        RedBlackTree() {
            NIL = new RBNode(0);
            NIL.color = Color.BLACK;
            root = NIL;
        }
        
        void insert(int key) {
            RBNode node = new RBNode(key);
            node.left = NIL;
            node.right = NIL;
            
            RBNode parent = null;
            RBNode current = root;
            
            // Find position
            while (current != NIL) {
                parent = current;
                if (node.key < current.key) {
                    current = current.left;
                } else {
                    current = current.right;
                }
            }
            
            node.parent = parent;
            
            if (parent == null) {
                root = node;
            } else if (node.key < parent.key) {
                parent.left = node;
            } else {
                parent.right = node;
            }
            
            insertFixup(node);
        }
        
        private void insertFixup(RBNode node) {
            while (node.parent != null && 
                   node.parent.color == Color.RED) {
                if (node.parent == node.parent.parent.left) {
                    RBNode uncle = node.parent.parent.right;
                    
                    if (uncle.color == Color.RED) {
                        // Case 1
                        node.parent.color = Color.BLACK;
                        uncle.color = Color.BLACK;
                        node.parent.parent.color = Color.RED;
                        node = node.parent.parent;
                    } else {
                        if (node == node.parent.right) {
                            // Case 2
                            node = node.parent;
                            rotateLeft(node);
                        }
                        // Case 3
                        node.parent.color = Color.BLACK;
                        node.parent.parent.color = Color.RED;
                        rotateRight(node.parent.parent);
                    }
                } else {
                    RBNode uncle = node.parent.parent.left;
                    
                    if (uncle.color == Color.RED) {
                        node.parent.color = Color.BLACK;
                        uncle.color = Color.BLACK;
                        node.parent.parent.color = Color.RED;
                        node = node.parent.parent;
                    } else {
                        if (node == node.parent.left) {
                            node = node.parent;
                            rotateRight(node);
                        }
                        node.parent.color = Color.BLACK;
                        node.parent.parent.color = Color.RED;
                        rotateLeft(node.parent.parent);
                    }
                }
            }
            root.color = Color.BLACK;
        }
        
        private void rotateLeft(RBNode x) {
            RBNode y = x.right;
            x.right = y.left;
            
            if (y.left != NIL) {
                y.left.parent = x;
            }
            
            y.parent = x.parent;
            
            if (x.parent == null) {
                root = y;
            } else if (x == x.parent.left) {
                x.parent.left = y;
            } else {
                x.parent.right = y;
            }
            
            y.left = x;
            x.parent = y;
        }
        
        private void rotateRight(RBNode x) {
            RBNode y = x.left;
            x.left = y.right;
            
            if (y.right != NIL) {
                y.right.parent = x;
            }
            
            y.parent = x.parent;
            
            if (x.parent == null) {
                root = y;
            } else if (x == x.parent.right) {
                x.parent.right = y;
            } else {
                x.parent.left = y;
            }
            
            y.right = x;
            x.parent = y;
        }
        
        boolean search(int key) {
            return searchHelper(root, key) != NIL;
        }
        
        private RBNode searchHelper(RBNode node, int key) {
            if (node == NIL || key == node.key) {
                return node;
            }
            
            if (key < node.key) {
                return searchHelper(node.left, key);
            }
            return searchHelper(node.right, key);
        }
        
        void printInorder() {
            printInorderHelper(root);
            logger.info("");
        }
        
        private void printInorderHelper(RBNode node) {
            if (node != NIL) {
                printInorderHelper(node.left);
                System.out.print(node.key + " ");
                printInorderHelper(node.right);
            }
        }
        
        void printTree() {
            printTreeHelper(root, 0);
        }
        
        private void printTreeHelper(RBNode node, int level) {
            if (node != NIL) {
                printTreeHelper(node.right, level + 1);
                String color = node.color == Color.RED ? "R" : "B";
                logger.info(" ".repeat(4 * level) + 
                                 "→ " + node.key + "(" + color + ")");
                printTreeHelper(node.left, level + 1);
            }
        }
    }
    
    public static void main(String[] args) {
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        long startTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("RED-BLACK TREE DEMONSTRATION");
        logger.info(separator);
        logger.info("");
        
        // Example 1
        logger.info("Example 1: Basic Insert and Search");
        logger.info(dash);
        RedBlackTree tree = new RedBlackTree();
        int[] keys = {7, 3, 18, 10, 22, 8, 11, 26};
        
        System.out.print("Inserting: ");
        for (int key : keys) {
            System.out.print(key + " ");
            tree.insert(key);
        }
        
        logger.info("\n\nTree structure (R=Red, B=Black):");
        tree.printTree();
        
        System.out.print("\nInorder traversal: ");
        tree.printInorder();
        
        logger.info("Search for 10: " + tree.search(10));
        logger.info("Search for 15: " + tree.search(15));
        logger.info("");
        
        // Example 2
        logger.info("Example 2: Sequential Insertion");
        logger.info(dash);
        RedBlackTree tree2 = new RedBlackTree();
        logger.info("Inserting 1 through 10...");
        for (int i = 1; i <= 10; i++) {
            tree2.insert(i);
        }
        
        logger.info("\nBalanced tree:");
        tree2.printTree();
        System.out.print("Inorder: ");
        tree2.printInorder();
        logger.info("");
        
        long endTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("\nComplexity Summary:");
        logger.info("  Time:  O(log n)");
        logger.info("  Space: O(n)");
        logger.info("\nKey Advantages:");
        logger.info("  - Guaranteed O(log n)");
        logger.info("  - Fewer rotations than AVL");
        logger.info(separator);
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}