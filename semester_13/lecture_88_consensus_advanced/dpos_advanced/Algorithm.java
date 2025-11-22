// package semester_13.lecture_88_consensus_advanced.dpos_advanced;
import java.util.*;
import java.util.logging.Logger;

/**
 * Dpos Advanced implementation.
 */
    public static int dposadvanced(int n) {
    if (n <= 1) {
        return n;
    }
    
    int[] dp = new int[n + 1];
    dp[1] = 1;
    
    for (int i = 2; i <= n; i++) {
        dp[i] = dp[i - 1] + dp[i - 2];
    }
    
    return dp[n];
}

public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Dpos Advanced");
        System.out.println("=".repeat(70));
        
        Object result = dpos_advanced();
        System.out.println("Result: " + result);
        System.out.println("\nSee README.md for implementation details");
    }
}
