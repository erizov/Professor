import java.util.function.Supplier;

/**
 * Retry Pattern.
 * 
 * Automatically retries failed operations.
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    static class RetryHandler {
        private int maxAttempts;
        private long initialDelayMs;
        
        RetryHandler(int maxAttempts, long initialDelayMs) {
            this.maxAttempts = maxAttempts;
            this.initialDelayMs = initialDelayMs;
        }
        
        <T> T execute(Supplier<T> func) throws Exception {
            Exception lastException = null;
            
            for (int attempt = 1; attempt <= maxAttempts; attempt++) {
                try {
                    return func.get();
                } catch (Exception e) {
                    lastException = e;
                    if (attempt < maxAttempts) {
                        long delay = initialDelayMs * (long)Math.pow(2, attempt - 1);
                        Thread.sleep(delay);
                    }
                }
            }
            
            throw lastException;
        }
    }
    
    public static void main(String[] args) {
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        long startTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("RETRY PATTERN");
        logger.info(separator);
        logger.info("");
        
        RetryHandler retry = new RetryHandler(3, 100);
        
        try {
            String result = retry.execute(() -> "Success");
            logger.info("Result: " + result);
        } catch (Exception e) {
            logger.info("Failed: " + e.getMessage());
        }
        logger.info("");
        
        long endTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("\nPattern: Retries failed operations");
        logger.info(separator);
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
