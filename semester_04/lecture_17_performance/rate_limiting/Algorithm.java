package semester_04.lecture_17_performance.rate_limiting;

/*** Rate Limiting Pattern.
 * 
 * Controls the rate of requests sent or received to prevent abuse,
 * ensure fair usage, and protect system resources.
 */
import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

import java.util.logging.Logger;
class RateLimitConfig {
    int maxRequests;
    double windowSeconds;
    
    RateLimitConfig(int maxRequests, double windowSeconds) {
        this.maxRequests = maxRequests;
        this.windowSeconds = windowSeconds;
    }
}

interface RateLimiter {
    boolean isAllowed(String identifier);
    int getRemaining(String identifier);
}

class TokenBucketRateLimiter implements RateLimiter {
    private final RateLimitConfig config;
    private final Map<String, TokenBucket> buckets = new ConcurrentHashMap<>();
    
    TokenBucketRateLimiter(RateLimitConfig config) {
        this.config = config;
    }
    
    @Override
    public boolean isAllowed(String identifier) {
        LocalDateTime now = LocalDateTime.now();
        
        TokenBucket bucket = buckets.computeIfAbsent(identifier,
            k -> new TokenBucket(config.maxRequests, now));
        
        long elapsedSeconds = ChronoUnit.SECONDS.between(bucket.lastRefill, now);
        int tokensToAdd = (int) ((elapsedSeconds / config.windowSeconds) * config.maxRequests);
        
        if (tokensToAdd > 0) {
            bucket.tokens = Math.min(config.maxRequests, bucket.tokens + tokensToAdd);
            bucket.lastRefill = now;
        }
        
        if (bucket.tokens > 0) {
            bucket.tokens--;
            return true;
        }
        
        return false;
    }
    
    @Override
    public int getRemaining(String identifier) {
        if (!buckets.containsKey(identifier)) {
            return config.maxRequests;
        }
        
        TokenBucket bucket = buckets.get(identifier);
        LocalDateTime now = LocalDateTime.now();
        long elapsedSeconds = ChronoUnit.SECONDS.between(bucket.lastRefill, now);
        int tokensToAdd = (int) ((elapsedSeconds / config.windowSeconds) * config.maxRequests);
        
        int currentTokens = Math.min(config.maxRequests, bucket.tokens + tokensToAdd);
        return Math.max(0, currentTokens);
    }
    
    private static class TokenBucket {
        int tokens;
        LocalDateTime lastRefill;
        
        TokenBucket(int tokens, LocalDateTime lastRefill) {
            this.tokens = tokens;
            this.lastRefill = lastRefill;
        }
    }
}

class SlidingWindowRateLimiter implements RateLimiter {
    private final RateLimitConfig config;
    private final Map<String, Deque<LocalDateTime>> windows = new ConcurrentHashMap<>();
    
    SlidingWindowRateLimiter(RateLimitConfig config) {
        this.config = config;
    }
    
    @Override
    public boolean isAllowed(String identifier) {
        LocalDateTime now = LocalDateTime.now();
        LocalDateTime cutoff = now.minusSeconds((long) config.windowSeconds);
        
        Deque<LocalDateTime> window = windows.computeIfAbsent(identifier,
            k -> new ArrayDeque<>());
        
        while (!window.isEmpty() && window.peekFirst().isBefore(cutoff)) {
            window.pollFirst();
        }
        
        if (window.size() < config.maxRequests) {
            window.addLast(now);
            return true;
        }
        
        return false;
    }
    
    @Override
    public int getRemaining(String identifier) {
        if (!windows.containsKey(identifier)) {
            return config.maxRequests;
        }
        
        LocalDateTime now = LocalDateTime.now();
        LocalDateTime cutoff = now.minusSeconds((long) config.windowSeconds);
        Deque<LocalDateTime> window = windows.get(identifier);
        
        while (!window.isEmpty() && window.peekFirst().isBefore(cutoff)) {
            window.pollFirst();
        }
        
        return Math.max(0, config.maxRequests - window.size());
    }
}

class FixedWindowRateLimiter implements RateLimiter {
    private final RateLimitConfig config;
    private final Map<String, FixedWindow> windows = new ConcurrentHashMap<>();
    
    FixedWindowRateLimiter(RateLimitConfig config) {
        this.config = config;
    }
    
    @Override
    public boolean isAllowed(String identifier) {
        LocalDateTime now = LocalDateTime.now();
        LocalDateTime windowStart = now.withSecond(0).withNano(0);
        
        FixedWindow window = windows.computeIfAbsent(identifier,
            k -> new FixedWindow(windowStart, 0));
        
        if (window.windowStart.isBefore(windowStart)) {
            window.windowStart = windowStart;
            window.count = 0;
        }
        
        if (window.count < config.maxRequests) {
            window.count++;
            return true;
        }
        
        return false;
    }
    
    @Override
    public int getRemaining(String identifier) {
        if (!windows.containsKey(identifier)) {
            return config.maxRequests;
        }
        
        FixedWindow window = windows.get(identifier);
        LocalDateTime now = LocalDateTime.now();
        LocalDateTime windowStart = now.withSecond(0).withNano(0);
        
        if (window.windowStart.isBefore(windowStart)) {
            return config.maxRequests;
        }
        
        return Math.max(0, config.maxRequests - window.count);
    }
    
    private static class FixedWindow {
        LocalDateTime windowStart;
        int count;
        
        FixedWindow(LocalDateTime windowStart, int count) {
            this.windowStart = windowStart;
            this.count = count;
        }
    }
}

public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());
    private static final String dash = "-".repeat(70);
    private static final String separator = "=".repeat(70);

    
    public static void main(String[] args) throws InterruptedException {
        long startTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("RATE LIMITING PATTERN DEMONSTRATION");
        logger.info(separator);
        logger.info("");
        
        // Example 1: Token Bucket
        logger.info("Example 1: Token Bucket Rate Limiter");
        logger.info(dash);
        
        RateLimitConfig config = new RateLimitConfig(5, 10.0);
        RateLimiter limiter = new TokenBucketRateLimiter(config);
        
        String clientId = "client1";
        System.out.printf("Rate limit: %d requests per %.0fs%n",
                         config.maxRequests, config.windowSeconds);
        logger.info(String.format("%nMaking requests as %s:%n", clientId));
        
        for (int i = 0; i < 8; i++) {
            boolean allowed = limiter.isAllowed(clientId);
            int remaining = limiter.getRemaining(clientId);
            String status = allowed ? "ALLOWED" : "DENIED";
            System.out.printf("  Request %d: %s (remaining: %d)%n",
                            i + 1, status, remaining);
            Thread.sleep(100);
        }
        logger.info("");
        
        // Example 2: Sliding Window
        logger.info("Example 2: Sliding Window Rate Limiter");
        logger.info(dash);
        
        config = new RateLimitConfig(3, 5.0);
        limiter = new SlidingWindowRateLimiter(config);
        
        clientId = "client2";
        System.out.printf("Rate limit: %d requests per %.0fs%n",
                         config.maxRequests, config.windowSeconds);
        logger.info(String.format("%nMaking requests as %s:%n", clientId));
        
        for (int i = 0; i < 5; i++) {
            boolean allowed = limiter.isAllowed(clientId);
            int remaining = limiter.getRemaining(clientId);
            String status = allowed ? "ALLOWED" : "DENIED";
            System.out.printf("  Request %d: %s (remaining: %d)%n",
                            i + 1, status, remaining);
            Thread.sleep(500);
        }
        logger.info("");
        
        // Example 3: Multiple Clients
        logger.info("Example 3: Rate Limiting Multiple Clients");
        logger.info(dash);
        
        limiter = new TokenBucketRateLimiter(new RateLimitConfig(3, 5.0));
        
        String[] clients = {"client_a", "client_b", "client_c"};
        logger.info("Distributing requests across clients:");
        
        for (int i = 0; i < 12; i++) {
            String client = clients[i % clients.length];
            boolean allowed = limiter.isAllowed(client);
            int remaining = limiter.getRemaining(client);
            String status = allowed ? "✓" : "✗";
            System.out.printf("  Request %d (%s): %s (remaining: %d)%n",
                            i + 1, client, status, remaining);
        }
        logger.info("");
        
        long endTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("\nPattern Summary:");
        logger.info("\nIntent:");
        logger.info("  Controls the rate of requests sent or received to prevent");
        logger.info("  abuse, ensure fair usage, and protect system resources.");
        logger.info("\nKey Advantages:");
        logger.info("  - Prevents abuse");
        logger.info("  - Protects system resources");
        logger.info("  - Ensures fair usage");
        logger.info("  - DDoS protection");
        logger.info("\nWhen to Use:");
        logger.info("  - API rate limiting");
        logger.info("  - DDoS protection");
        logger.info("  - Fair resource allocation");
        logger.info("  - Cost control");
        logger.info(separator);
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
