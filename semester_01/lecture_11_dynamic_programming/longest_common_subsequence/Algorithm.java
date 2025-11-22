// package semester_01.lecture_11_dynamic_programming.longest_common_subsequence;

import java.util.*;

/**
 * Longest Common Subsequence (LCS) - Dynamic Programming.
 * 
 * Time Complexity: O(m * n)
 * Space Complexity: O(m * n)
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    static int lcsLength(String s1, String s2) {
        int m = s1.length();
        int n = s2.length();
        int[][] dp = new int[m + 1][n + 1];
        
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (s1.charAt(i - 1) == s2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }
        
        return dp[m][n];
    }
    
    static String lcsSequence(String s1, String s2) {
        int m = s1.length();
        int n = s2.length();
        int[][] dp = new int[m + 1][n + 1];
        
        // Build DP table
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (s1.charAt(i - 1) == s2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }
        
        // Reconstruct LCS
        StringBuilder lcs = new StringBuilder();
        int i = m, j = n;
        
        while (i > 0 && j > 0) {
            if (s1.charAt(i - 1) == s2.charAt(j - 1)) {
                lcs.append(s1.charAt(i - 1));
                i--;
                j--;
            } else if (dp[i - 1][j] > dp[i][j - 1]) {
                i--;
            } else {
                j--;
            }
        }
        
        return lcs.reverse().toString();
    }
    
    public static void main(String[] args) {
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        long startTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("LONGEST COMMON SUBSEQUENCE (LCS) DEMONSTRATION");
        logger.info(separator);
        logger.info("");
        
        // Example 1
        logger.info("Example 1: Basic LCS");
        logger.info(dash);
        
        String s1 = "ABCDGH";
        String s2 = "AEDFHR";
        
        int length = lcsLength(s1, s2);
        String sequence = lcsSequence(s1, s2);
        
        logger.info("String 1: " + s1);
        logger.info("String 2: " + s2);
        logger.info("LCS Length: " + length);
        logger.info("LCS Sequence: " + sequence);
        logger.info("");
        
        // Example 2
        logger.info("Example 2: Another Example");
        logger.info(dash);
        
        String s3 = "AGGTAB";
        String s4 = "GXTXAYB";
        
        int length2 = lcsLength(s3, s4);
        String sequence2 = lcsSequence(s3, s4);
        
        logger.info("String 1: " + s3);
        logger.info("String 2: " + s4);
        logger.info("LCS Length: " + length2);
        logger.info("LCS Sequence: " + sequence2);
        logger.info("");
        
        long endTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("\nComplexity Summary:");
        logger.info("  Time:  O(m * n)");
        logger.info("  Space: O(m * n)");
        logger.info(separator);
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
