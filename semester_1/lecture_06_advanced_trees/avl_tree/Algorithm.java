import java.util.*;
import java.util.logging.Logger;

/**
 * Avl Tree implementation.
 */
    public static class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    TreeNode(int val) { this.val = val; }
}

public static List<Integer> avltree(TreeNode root) {
    List<Integer> result = new ArrayList<>();
    if (root == null) {
        return result;
    }
    
    // TODO: Implement avltree traversal
    inOrder(root, result);
    return result;
}

private static void inOrder(TreeNode node, List<Integer> result) {
    if (node != null) {
        inOrder(node.left, result);
        result.add(node.val);
        inOrder(node.right, result);
    }
}

public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Avl Tree");
        System.out.println("=".repeat(70));
        
        Object result = avl_tree();
        System.out.println("Result: " + result);
        System.out.println("\nSee README.md for implementation details");
    }
}
