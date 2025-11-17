import java.util.Arrays;
import java.util.Random;

import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger
    /**
     * Semantic Search.
     * 
     * @param arr Array to search
     * @param target Target value
     * @return Index if found, -1 otherwise
     */
    public static int semanticsearch(int[] arr, int target) {
        if (arr == null || arr.length == 0) {
            return -1;
        }
        
        // TODO: Implement semantic_search
        logger.info("Executing semantic_search");
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) {
                return i;
            }
        }
        return -1;
    }
    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Semantic Search");
        System.out.println("=".repeat(70));
        
        Object result = semanticsearch();
        System.out.println("Result: " + result);
        System.out.println("\nSee README.md for implementation details");
    }
}