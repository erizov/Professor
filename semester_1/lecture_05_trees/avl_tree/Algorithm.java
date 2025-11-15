/**
 * AVL Tree implementation.
 * 
 * Self-balancing binary search tree.
 * 
 * Time Complexity: O(log n) - insert, delete, search
 * Space Complexity: O(n)
 */
public class Algorithm {
    
    static class AVLNode {
        int key;
        AVLNode left, right;
        int height;
        
        AVLNode(int key) {
            this.key = key;
            this.height = 1;
        }
    }
    
    static class AVLTree {
        AVLNode root;
        
        int getHeight(AVLNode node) {
            return node == null ? 0 : node.height;
        }
        
        int getBalance(AVLNode node) {
            return node == null ? 0 : 
                getHeight(node.left) - getHeight(node.right);
        }
        
        void updateHeight(AVLNode node) {
            node.height = 1 + Math.max(getHeight(node.left),
                                       getHeight(node.right));
        }
        
        AVLNode rotateRight(AVLNode z) {
            AVLNode y = z.left;
            AVLNode B = y.right;
            
            // Rotation
            y.right = z;
            z.left = B;
            
            // Update heights
            updateHeight(z);
            updateHeight(y);
            
            return y;
        }
        
        AVLNode rotateLeft(AVLNode z) {
            AVLNode y = z.right;
            AVLNode B = y.left;
            
            // Rotation
            y.left = z;
            z.right = B;
            
            // Update heights
            updateHeight(z);
            updateHeight(y);
            
            return y;
        }
        
        void insert(int key) {
            root = insertHelper(root, key);
        }
        
        AVLNode insertHelper(AVLNode node, int key) {
            // Standard BST insertion
            if (node == null) {
                return new AVLNode(key);
            }
            
            if (key < node.key) {
                node.left = insertHelper(node.left, key);
            } else if (key > node.key) {
                node.right = insertHelper(node.right, key);
            } else {
                return node; // Duplicates not allowed
            }
            
            // Update height
            updateHeight(node);
            
            // Get balance
            int balance = getBalance(node);
            
            // Left-Left case
            if (balance > 1 && key < node.left.key) {
                return rotateRight(node);
            }
            
            // Right-Right case
            if (balance < -1 && key > node.right.key) {
                return rotateLeft(node);
            }
            
            // Left-Right case
            if (balance > 1 && key > node.left.key) {
                node.left = rotateLeft(node.left);
                return rotateRight(node);
            }
            
            // Right-Left case
            if (balance < -1 && key < node.right.key) {
                node.right = rotateRight(node.right);
                return rotateLeft(node);
            }
            
            return node;
        }
        
        void delete(int key) {
            root = deleteHelper(root, key);
        }
        
        AVLNode deleteHelper(AVLNode node, int key) {
            if (node == null) return node;
            
            // Standard BST deletion
            if (key < node.key) {
                node.left = deleteHelper(node.left, key);
            } else if (key > node.key) {
                node.right = deleteHelper(node.right, key);
            } else {
                // Node with one or no child
                if (node.left == null) {
                    return node.right;
                } else if (node.right == null) {
                    return node.left;
                }
                
                // Node with two children
                AVLNode temp = getMinNode(node.right);
                node.key = temp.key;
                node.right = deleteHelper(node.right, temp.key);
            }
            
            // Update height
            updateHeight(node);
            
            // Get balance
            int balance = getBalance(node);
            
            // Left-Left case
            if (balance > 1 && getBalance(node.left) >= 0) {
                return rotateRight(node);
            }
            
            // Left-Right case
            if (balance > 1 && getBalance(node.left) < 0) {
                node.left = rotateLeft(node.left);
                return rotateRight(node);
            }
            
            // Right-Right case
            if (balance < -1 && getBalance(node.right) <= 0) {
                return rotateLeft(node);
            }
            
            // Right-Left case
            if (balance < -1 && getBalance(node.right) > 0) {
                node.right = rotateRight(node.right);
                return rotateLeft(node);
            }
            
            return node;
        }
        
        AVLNode getMinNode(AVLNode node) {
            while (node.left != null) {
                node = node.left;
            }
            return node;
        }
        
        boolean search(int key) {
            return searchHelper(root, key);
        }
        
        boolean searchHelper(AVLNode node, int key) {
            if (node == null) return false;
            if (key == node.key) return true;
            return key < node.key ? 
                searchHelper(node.left, key) : 
                searchHelper(node.right, key);
        }
        
        void printInorder() {
            printInorderHelper(root);
            System.out.println();
        }
        
        void printInorderHelper(AVLNode node) {
            if (node != null) {
                printInorderHelper(node.left);
                System.out.print(node.key + " ");
                printInorderHelper(node.right);
            }
        }
        
        void printTree() {
            printTreeHelper(root, 0);
        }
        
        void printTreeHelper(AVLNode node, int level) {
            if (node != null) {
                printTreeHelper(node.right, level + 1);
                System.out.println(" ".repeat(4 * level) + "→ " + 
                                 node.key + " (h=" + node.height + ")");
                printTreeHelper(node.left, level + 1);
            }
        }
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("AVL TREE DEMONSTRATION");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Example 1: Basic operations
        System.out.println("Example 1: Basic Insert and Search");
        System.out.println("-".repeat(70));
        AVLTree avl = new AVLTree();
        int[] keys = {10, 20, 30, 40, 50, 25};
        
        System.out.print("Inserting: ");
        for (int key : keys) {
            System.out.print(key + " ");
            avl.insert(key);
        }
        System.out.println("\n\nTree structure:");
        avl.printTree();
        
        System.out.print("\nInorder traversal: ");
        avl.printInorder();
        
        System.out.println("Search for 30: " + avl.search(30));
        System.out.println("Search for 35: " + avl.search(35));
        System.out.println();
        
        // Example 2: Deletion
        System.out.println("Example 2: Deletion");
        System.out.println("-".repeat(70));
        System.out.println("Deleting 10, 30...");
        avl.delete(10);
        avl.delete(30);
        
        System.out.println("\nTree structure after deletion:");
        avl.printTree();
        System.out.print("Inorder traversal: ");
        avl.printInorder();
        System.out.println();
        
        // Example 3: Left-Left rotation
        System.out.println("Example 3: Left-Left Rotation");
        System.out.println("-".repeat(70));
        AVLTree avl2 = new AVLTree();
        System.out.println("Inserting 30, 20, 10 (triggers LL rotation)");
        avl2.insert(30);
        avl2.insert(20);
        avl2.insert(10);
        
        System.out.println("\nBalanced tree:");
        avl2.printTree();
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nComplexity Summary:");
        System.out.println("  Time:  O(log n) - all operations");
        System.out.println("  Space: O(n)");
        System.out.println("\nKey Advantages:");
        System.out.println("  - Guaranteed O(log n) operations");
        System.out.println("  - Self-balancing");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n", 
                        (endTime - startTime) / 1_000_000.0);
    }
}
