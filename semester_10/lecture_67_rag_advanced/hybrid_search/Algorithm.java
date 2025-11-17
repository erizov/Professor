import java.util.*;
import java.util.logging.Logger;

/**
 * Hybrid Search implementation.
 */
    public static int hybridsearch(int[] arr, int target) {
    if (arr.length == 0) {
        return -1;
    }
    
    // TODO: Implement hybridsearch algorithm
    for (int i = 0; i < arr.length; i++) {
        if (arr[i] == target) {
            return i;
        }
    }
    return -1;
}

public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Hybrid Search");
        System.out.println("=".repeat(70));
        
        Object result = hybrid_search();
        System.out.println("Result: " + result);
        System.out.println("\nSee README.md for implementation details");
    }
}
