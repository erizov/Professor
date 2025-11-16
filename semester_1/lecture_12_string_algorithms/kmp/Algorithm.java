import java.util.*;

/**
 * Knuth-Morris-Pratt (KMP) Algorithm.
 * 
 * Efficient string pattern matching.
 * 
 * Time Complexity: O(n + m)
 * Space Complexity: O(m)
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    static int[] computeLPS(String pattern) {
        int m = pattern.length();
        int[] lps = new int[m];
        int length = 0;
        int i = 1;
        
        while (i < m) {
            if (pattern.charAt(i) == pattern.charAt(length)) {
                length++;
                lps[i] = length;
                i++;
            } else {
                if (length != 0) {
                    length = lps[length - 1];
                } else {
                    lps[i] = 0;
                    i++;
                }
            }
        }
        
        return lps;
    }
    
    static List<Integer> kmpSearch(String text, String pattern) {
        int n = text.length();
        int m = pattern.length();
        
        if (m == 0 || m > n) {
            return new ArrayList<>();
        }
        
        int[] lps = computeLPS(pattern);
        List<Integer> result = new ArrayList<>();
        
        int i = 0; // Index for text
        int j = 0; // Index for pattern
        
        while (i < n) {
            if (pattern.charAt(j) == text.charAt(i)) {
                i++;
                j++;
            }
            
            if (j == m) {
                result.add(i - j);
                j = lps[j - 1];
            } else if (i < n && pattern.charAt(j) != text.charAt(i)) {
                if (j != 0) {
                    j = lps[j - 1];
                } else {
                    i++;
                }
            }
        }
        
        return result;
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        logger.info("=".repeat(70));
        logger.info("KNUTH-MORRIS-PRATT (KMP) ALGORITHM");
        logger.info("=".repeat(70));
        logger.info();
        
        // Example 1
        logger.info("Example 1: Basic Pattern Matching");
        logger.info("-".repeat(70));
        
        String text1 = "ABABDABACDABABCABCABAB";
        String pattern1 = "ABABCABAB";
        
        List<Integer> matches = kmpSearch(text1, pattern1);
        logger.info("Text: " + text1);
        logger.info("Pattern: " + pattern1);
        logger.info("Matches found at indices: " + matches);
        logger.info();
        
        // Example 2
        logger.info("Example 2: Multiple Occurrences");
        logger.info("-".repeat(70));
        
        String text2 = "AABAACAADAABAABA";
        String pattern2 = "AABA";
        
        List<Integer> matches2 = kmpSearch(text2, pattern2);
        logger.info("Text: " + text2);
        logger.info("Pattern: " + pattern2);
        logger.info("Matches: " + matches2);
        logger.info();
        
        long endTime = System.nanoTime();
        
        logger.info("=".repeat(70));
        logger.info("\nComplexity Summary:");
        logger.info("  Time:  O(n + m)");
        logger.info("  Space: O(m)");
        logger.info("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
