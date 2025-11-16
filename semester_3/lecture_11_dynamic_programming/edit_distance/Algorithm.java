/**
 * Edit Distance (Levenshtein Distance) - Dynamic Programming.
 * 
 * Minimum number of single-character edits (insertions, deletions,
 * substitutions) required to change one word into another.
 */
import java.util.*;

public class Algorithm {
    
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
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("EDIT DISTANCE (LEVENSHTEIN DISTANCE) DEMONSTRATION");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Example 1: Basic edit distance
        System.out.println("Example 1: Basic Edit Distance");
        System.out.println("-".repeat(70));
        
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
        System.out.println();
        
        // Example 2: Similarity
        System.out.println("Example 2: String Similarity");
        System.out.println("-".repeat(70));
        
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
        System.out.println();
        
        // Example 3: Space-optimized version
        System.out.println("Example 3: Space-Optimized Version");
        System.out.println("-".repeat(70));
        
        String s1 = "saturday";
        String s2 = "sunday";
        int distStandard = editDistance(s1, s2);
        int distOptimized = editDistanceOptimized(s1, s2);
        
        System.out.printf("'%s' -> '%s':%n", s1, s2);
        System.out.printf("  Standard: %d%n", distStandard);
        System.out.printf("  Optimized: %d%n", distOptimized);
        System.out.println("Note: Optimized uses O(min(m,n)) space instead of O(m*n)");
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nComplexity Summary:");
        System.out.println("  Time:  O(m * n) - m and n are string lengths");
        System.out.println("  Space: O(m * n) - standard");
        System.out.println("        O(min(m, n)) - optimized");
        System.out.println("\nKey Advantages:");
        System.out.println("  - Optimal solution");
        System.out.println("  - Can be space-optimized");
        System.out.println("  - Useful for many applications");
        System.out.println("\nWhen to Use:");
        System.out.println("  - Spell checking");
        System.out.println("  - DNA sequence alignment");
        System.out.println("  - Fuzzy string matching");
        System.out.println("  - Autocorrect systems");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
