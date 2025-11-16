import java.util.*;

/**
 * Caching Pattern.
 * 
 * Stores frequently accessed data.
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    static class LRUCache {
        private final int capacity;
        private LinkedHashMap<String, String> cache;
        
        LRUCache(int capacity) {
            this.capacity = capacity;
            this.cache = new LinkedHashMap<String, String>(capacity, 0.75f, true) {
                protected boolean removeEldestEntry(Map.Entry<String, String> eldest) {
                    return size() > capacity;
                }
            };
        }
        
        String get(String key) {
            return cache.get(key);
        }
        
        void put(String key, String value) {
            cache.put(key, value);
        }
        
        int size() {
            return cache.size();
        }
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        logger.info("=".repeat(70));
        logger.info("CACHING PATTERN");
        logger.info("=".repeat(70));
        logger.info();
        
        LRUCache cache = new LRUCache(3);
        
        cache.put("key1", "value1");
        cache.put("key2", "value2");
        cache.put("key3", "value3");
        
        logger.info("Cache size: " + cache.size());
        logger.info("key1: " + cache.get("key1"));
        logger.info();
        
        long endTime = System.nanoTime();
        
        logger.info("=".repeat(70));
        logger.info("\nPattern: Stores frequently accessed data");
        logger.info("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}