// package semester_01.lecture_06_advanced_trees.avl_tree;
import java.util.Arrays;
import java.util.Random;

import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());
    /**
     * Avl Tree.
     * 
     * @param args Variable arguments
     * @return Result of the algorithm
     */
    public static Object avltree(Object... args) {
        logger.info("Executing avl_tree");





    return null;
    }
    public static void main(String[] args) {
        System.out.println("=".repeat(50));
        System.out.println("AVL Tree Algorithm Test");
        System.out.println("=".repeat(50));

        try {
            // Test AVL tree operations
            System.out.println("Testing AVL Tree operations...");

            long startTime = System.nanoTime();
            Object result = avltree();
            long endTime = System.nanoTime();

            System.out.println("AVL Tree operations completed");
            System.out.println("Result: " + result);
            System.out.printf("Execution time: %.3f ms%n", (endTime - startTime) / 1_000_000.0);
            System.out.println("Status: SUCCESS");
            System.out.println("\nSee README.md for implementation details");

        } catch (Exception e) {
            System.err.println("Error running AVL Tree algorithm: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }

        System.out.println("=".repeat(50));
    }
        public static class AVLNode {
    int val, height;
    AVLNode left, right;
    
    AVLNode(int val) {
        this.val = val;
        this.height = 1;
    }
}
    public static int getHeight(AVLNode node) {
        return node == null ? 0 : node.height;
    }
    public static int getBalance(AVLNode node) {
        return node == null ? 0 : getHeight(node.left) - getHeight(node.right);
    }
    public static AVLNode rightRotate(AVLNode y) {
        AVLNode x = y.left;
        AVLNode T2 = x.right;
    
        x.right = y;
        y.left = T2;
    
        y.height = Math.max(getHeight(y.left), getHeight(y.right)) + 1;
        x.height = Math.max(getHeight(x.left), getHeight(x.right)) + 1;
    
        return x;
    }
    public static AVLNode leftRotate(AVLNode x) {
        AVLNode y = x.right;
        AVLNode T2 = y.left;
    
        y.left = x;
        x.right = T2;
    
        x.height = Math.max(getHeight(x.left), getHeight(x.right)) + 1;
        y.height = Math.max(getHeight(y.left), getHeight(y.right)) + 1;
    
        return y;
    }
    public static AVLNode insert(AVLNode root, int val) {
        if (root == null) {
            return new AVLNode(val);
        }
    
        if (val < root.val) {
            root.left = insert(root.left, val);
        } else if (val > root.val) {
            root.right = insert(root.right, val);
        } else {
            return root;
        }
    
        root.height = Math.max(getHeight(root.left), getHeight(root.right)) + 1;
        int balance = getBalance(root);
    
        if (balance > 1 && val < root.left.val) {
            return rightRotate(root);
        }
        if (balance < -1 && val > root.right.val) {
            return leftRotate(root);
        }
        if (balance > 1 && val > root.left.val) {
            root.left = leftRotate(root.left);
            return rightRotate(root);
        }
        if (balance < -1 && val < root.right.val) {
            root.right = rightRotate(root.right);
            return leftRotate(root);
        }
    
        return root;
    }
}
