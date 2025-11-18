import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Jwt implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Encode JWT.
     */
    public String encode(Object payload, Object expires_in) {
        logger.info("Executing encode");
        long currentTime = System.currentTimeMillis();
        String result = "" + header_b64 + ".";
        String result = "" + message + ".";
        return "";
    }

    /**
     * Decode JWT.
     */
    public Map<String, Object> decode(String token) {
        logger.info("Executing decode");
        long currentTime = System.currentTimeMillis();
        String result = "" + header_b64 + ".";
        return "";
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Jwt");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        str result = algo.encode(null, null);
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
