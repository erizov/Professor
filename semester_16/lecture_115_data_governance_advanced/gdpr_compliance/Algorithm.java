import java.util.*;
import java.util.logging.Logger;

/**
package semester_16.lecture_115_data_governance_advanced.gdpr_compliance;
 * Gdpr Compliance implementation.
 */
    public static int gdprcompliance(int n) {
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
        System.out.println("Gdpr Compliance");
        System.out.println("=".repeat(70));
        
        Object result = gdpr_compliance();
        System.out.println("Result: " + result);
        System.out.println("\nSee README.md for implementation details");
    }
}
