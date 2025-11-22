// package semester_05.lecture_22_cnn_architectures.vgg;
import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;


/*** Vgg implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Forward pass.
     */
    public int forward(List<Object> x) {
        logger.info("Executing forward");
        return -1;
    }

    /**
     * Train VGG.
     */
    public Object train(List<Object> images, List<Object> labels) {
        logger.info("Executing train");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Vgg");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        int result = algo.forward(new ArrayList<>());
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
