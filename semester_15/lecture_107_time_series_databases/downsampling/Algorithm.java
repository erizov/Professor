package semester_15.lecture_107_time_series_databases.downsampling;
import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;


/*** Downsampling implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Downsample with aggregation.
     */
    public int downsample(List<Object> data, Object window, String method) {
        logger.info("Executing downsample");
        return -1;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Downsampling");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        int result = algo.downsample(new ArrayList<>(), null, "");
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
