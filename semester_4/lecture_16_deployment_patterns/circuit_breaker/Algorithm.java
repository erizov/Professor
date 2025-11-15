import java.util.concurrent.atomic.AtomicInteger;
import java.time.LocalDateTime;

/**
 * Circuit Breaker Design Pattern.
 * 
 * Prevents cascading failures.
 */
public class Algorithm {
    
    enum CircuitState {
        CLOSED, OPEN, HALF_OPEN
    }
    
    static class CircuitBreaker {
        private CircuitState state = CircuitState.CLOSED;
        private AtomicInteger failureCount = new AtomicInteger(0);
        private AtomicInteger successCount = new AtomicInteger(0);
        private LocalDateTime lastFailureTime;
        private int failureThreshold = 5;
        private int successThreshold = 2;
        private long timeoutSeconds = 60;
        
        public <T> T call(java.util.function.Supplier<T> func) throws Exception {
            if (state == CircuitState.OPEN) {
                if (shouldAttemptReset()) {
                    state = CircuitState.HALF_OPEN;
                    successCount.set(0);
                } else {
                    throw new RuntimeException("Circuit breaker is OPEN");
                }
            }
            
            try {
                T result = func.get();
                onSuccess();
                return result;
            } catch (Exception e) {
                onFailure();
                throw e;
            }
        }
        
        private boolean shouldAttemptReset() {
            if (lastFailureTime == null) return true;
            return java.time.Duration.between(lastFailureTime, 
                LocalDateTime.now()).getSeconds() >= timeoutSeconds;
        }
        
        private void onSuccess() {
            failureCount.set(0);
            if (state == CircuitState.HALF_OPEN) {
                if (successCount.incrementAndGet() >= successThreshold) {
                    state = CircuitState.CLOSED;
                    successCount.set(0);
                }
            }
        }
        
        private void onFailure() {
            lastFailureTime = LocalDateTime.now();
            if (state == CircuitState.HALF_OPEN) {
                state = CircuitState.OPEN;
            } else if (failureCount.incrementAndGet() >= failureThreshold) {
                state = CircuitState.OPEN;
            }
        }
        
        public CircuitState getState() {
            return state;
        }
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("CIRCUIT BREAKER PATTERN");
        System.out.println("=".repeat(70));
        System.out.println();
        
        CircuitBreaker breaker = new CircuitBreaker();
        
        try {
            String result = breaker.call(() -> "Service response");
            System.out.println("Result: " + result);
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
        
        System.out.println("State: " + breaker.getState());
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nPattern: Prevents cascading failures");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
