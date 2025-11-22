// package semester_09.lecture_59_distributed_systems_advanced.eventual_consistency;

import java.util.logging.Logger;

/**
 * Eventual Consistency implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());
    
    public static int compareVectorClocks(int[] vc1, int[] vc2) {
        if (vc1.length != vc2.length) {
            return -1;
        }
        
        for (int i = 0; i < vc1.length; i++) {
            if (vc1[i] < vc2[i]) return -1;
            if (vc1[i] > vc2[i]) return 1;
        }
        return 0;
    }
    
    public static void main(String[] args) {
        logger.info("Eventual Consistency");
        logger.info("==================================================");
        
        int[] vc1 = {1, 2, 3};
        int[] vc2 = {1, 2, 4};
        
        int result = compareVectorClocks(vc1, vc2);
        logger.info("Comparison result: " + result);
    }
}