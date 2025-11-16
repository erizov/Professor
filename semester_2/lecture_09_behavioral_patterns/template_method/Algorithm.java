/**
 * Template Method Design Pattern.
 * 
 * Defines algorithm skeleton in method.
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    abstract static class DataProcessor {
        void process() {
            readData();
            processData();
            saveData();
        }
        
        abstract void readData();
        abstract void processData();
        
        void saveData() {
            logger.info("Saving processed data...");
        }
    }
    
    static class CSVProcessor extends DataProcessor {
        void readData() {
            logger.info("Reading CSV file...");
        }
        
        void processData() {
            logger.info("Processing CSV data...");
        }
    }
    
    public static void main(String[] args) {
        logger.info("=".repeat(70));
        logger.info("TEMPLATE METHOD DESIGN PATTERN");
        logger.info("=".repeat(70));
        logger.info();
        
        DataProcessor processor = new CSVProcessor();
        processor.process();
        logger.info();
        
        logger.info("=".repeat(70));
        logger.info("\nPattern: Defines algorithm skeleton");
        logger.info("=".repeat(70));
    }
}