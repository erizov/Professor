/**
 * Edit Distance (Levenshtein Distance) - Dynamic Programming.
 * 
 * Minimum operations to transform one string into another.
 */
public class Algorithm {
    
    static int editDistance(String s1, String s2) {
        int m = s1.length();
        int n = s2.length();
        int[][] dp = new int[m + 1][n + 1];
        
        // Base cases
        for (int i = 0; i <= m; i++) {
            dp[i][0] = i;
        }
        for (int j = 0; j <= n; j++) {
            dp[0][j] = j;
        }
        
        // Fill DP table
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (s1.charAt(i - 1) == s2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    dp[i][j] = 1 + Math.min(
                        Math.min(dp[i - 1][j], dp[i][j - 1]),
                        dp[i - 1][j - 1]
                    );
                }
            }
        }
        
        return dp[m][n];
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("EDIT DISTANCE (LEVENSHTEIN DISTANCE)");
        System.out.println("=".repeat(70));
        System.out.println();
        
        String[][] testCases = {
            {"kitten", "sitting"},
            {"saturday", "sunday"},
            {"horse", "ros"}
        };
        
        for (String[] test : testCases) {
            int distance = editDistance(test[0], test[1]);
            System.out.printf("'%s' -> '%s': %d operations%n",
                            test[0], test[1], distance);
        }
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nComplexity Summary:");
        System.out.println("  Time:  O(m * n)");
        System.out.println("  Space: O(m * n)");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}

