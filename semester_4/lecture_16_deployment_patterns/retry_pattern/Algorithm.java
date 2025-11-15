import java.util.function.Supplier;

/**
 * Retry Pattern.
 * 
 * Automatically retries failed operations.
 */
public class Algorithm {
    
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
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("RETRY PATTERN");
        System.out.println("=".repeat(70));
        System.out.println();
        
        RetryHandler retry = new RetryHandler(3, 100);
        
        try {
            String result = retry.execute(() -> "Success");
            System.out.println("Result: " + result);
        } catch (Exception e) {
            System.out.println("Failed: " + e.getMessage());
        }
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nPattern: Retries failed operations");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
