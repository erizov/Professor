package semester_01.lecture_11_dynamic_programming.edit_distance;

/**
 * Edit Distance (Levenshtein Distance) - Dynamic Programming.
 *
 * Minimum number of single-character edits (insertions, deletions,
 * substitutions) required to change one word into another.
 */
import java.util.*;

import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    /**
     * Calculate edit distance (Levenshtein distance).
     * 
     * Time Complexity: O(m * n)
     * Space Complexity: O(m * n)
     */
    static int editDistance(String s1, String s2) {
        int m = s1.length();
        int n = s2.length();
        int[][] dp = new int[m + 1][n + 1];
        
        // Base cases
        for (int i = 0; i <= m; i++) {
            dp[i][0] = i;  // Delete all characters from s1
        }
        for (int j = 0; j <= n; j++) {
            dp[0][j] = j;  // Insert all characters from s2
        }
        
        // Fill DP table
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (s1.charAt(i - 1) == s2.charAt(j - 1)) {
                    // Characters match, no operation needed
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    // Take minimum of three operations
                    dp[i][j] = 1 + Math.min(
                        Math.min(dp[i - 1][j],      // Delete
                                 dp[i][j - 1]),     // Insert
                        dp[i - 1][j - 1]            // Replace
                    );
                }
            }
        }
        
        return dp[m][n];
    }
    
    /**
     * Space-optimized edit distance.
     * Space Complexity: O(min(m, n))
     */
    static int editDistanceOptimized(String s1, String s2) {
        if (s1.length() < s2.length()) {
            String temp = s1;
            s1 = s2;
            s2 = temp;
        }
        
        int m = s1.length();
        int n = s2.length();
        int[] prev = new int[n + 1];
        int[] curr = new int[n + 1];
        
        // Initialize prev
        for (int j = 0; j <= n; j++) {
            prev[j] = j;
        }
        
        for (int i = 1; i <= m; i++) {
            curr[0] = i;
            for (int j = 1; j <= n; j++) {
                if (s1.charAt(i - 1) == s2.charAt(j - 1)) {
                    curr[j] = prev[j - 1];
                } else {
                    curr[j] = 1 + Math.min(
                        Math.min(prev[j], curr[j - 1]),
                        prev[j - 1]
                    );
                }
            }
            // Swap arrays
            int[] temp = prev;
            prev = curr;
            curr = temp;
        }
        
        return prev[n];
    }
    
    /**
     * Calculate similarity percentage.
     */
    static double similarity(String s1, String s2) {
        if (s1.isEmpty() && s2.isEmpty()) {
            return 1.0;
        }
        
        int maxLen = Math.max(s1.length(), s2.length());
        if (maxLen == 0) {
            return 1.0;
        }
        
        int distance = editDistance(s1, s2);
        return 1.0 - ((double) distance / maxLen);
    }
    
    public static void main(String[] args) {
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        long startTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("EDIT DISTANCE (LEVENSHTEIN DISTANCE) DEMONSTRATION");
        logger.info(separator);
        logger.info("");
        
        // Example 1: Basic edit distance
        logger.info("Example 1: Basic Edit Distance");
        logger.info(dash);
        
        String[][] testCases = {
            {"kitten", "sitting"},
            {"saturday", "sunday"},
            {"horse", "ros"},
            {"intention", "execution"}
        };
        
        for (String[] test : testCases) {
            int distance = editDistance(test[0], test[1]);
            System.out.printf("'%s' -> '%s': %d operations%n",
                            test[0], test[1], distance);
        }
        logger.info("");
        
        // Example 2: Similarity
        logger.info("Example 2: String Similarity");
        logger.info(dash);
        
        String[][] pairs = {
            {"hello", "hello"},
            {"hello", "hallo"},
            {"hello", "world"},
            {"algorithm", "alogrithm"}
        };
        
        for (String[] pair : pairs) {
            double sim = similarity(pair[0], pair[1]);
            int dist = editDistance(pair[0], pair[1]);
            System.out.printf("'%s' vs '%s':%n", pair[0], pair[1]);
            System.out.printf("  Distance: %d, Similarity: %.2f%%%n", 
                            dist, sim * 100);
        }
        logger.info("");
        
        // Example 3: Space-optimized version
        logger.info("Example 3: Space-Optimized Version");
        logger.info(dash);
        
        String s1 = "saturday";
        String s2 = "sunday";
        int distStandard = editDistance(s1, s2);
        int distOptimized = editDistanceOptimized(s1, s2);
        
        System.out.printf("'%s' -> '%s':%n", s1, s2);
        System.out.printf("  Standard: %d%n", distStandard);
        System.out.printf("  Optimized: %d%n", distOptimized);
        logger.info("Note: Optimized uses O(min(m,n)) space instead of O(m*n)");
        logger.info("");
        
        long endTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("\nComplexity Summary:");
        logger.info("  Time:  O(m * n) - m and n are string lengths");
        logger.info("  Space: O(m * n) - standard");
        logger.info("        O(min(m, n)) - optimized");
        logger.info("\nKey Advantages:");
        logger.info("  - Optimal solution");
        logger.info("  - Can be space-optimized");
        logger.info("  - Useful for many applications");
        logger.info("\nWhen to Use:");
        logger.info("  - Spell checking");
        logger.info("  - DNA sequence alignment");
        logger.info("  - Fuzzy string matching");
        logger.info("  - Autocorrect systems");
        logger.info(separator);
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
