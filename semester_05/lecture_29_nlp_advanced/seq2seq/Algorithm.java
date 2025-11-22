package semester_05.lecture_29_nlp_advanced.seq2seq;
import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;


/*** Seq2Seq implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Encode sequence.
     */
    public int encode(List<Object> sequence) {
        logger.info("Executing encode");
        return -1;
    }

    /**
     * Decode sequence.
     */
    public int decode(List<Object> hidden_state, Object max_length) {
        logger.info("Executing decode");
        return -1;
    }

    /**
     * Train seq2seq model.
     */
    public Object train(List<Object> source_seqs, List<Object> target_seqs) {
        logger.info("Executing train");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Seq2Seq");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        int result = algo.encode(new ArrayList<>());
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
