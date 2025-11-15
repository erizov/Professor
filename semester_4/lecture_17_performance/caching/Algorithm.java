import java.util.*;

/**
 * Caching Pattern.
 * 
 * Stores frequently accessed data.
 */
public class Algorithm {
    
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
        
        System.out.println("=".repeat(70));
        System.out.println("CACHING PATTERN");
        System.out.println("=".repeat(70));
        System.out.println();
        
        LRUCache cache = new LRUCache(3);
        
        cache.put("key1", "value1");
        cache.put("key2", "value2");
        cache.put("key3", "value3");
        
        System.out.println("Cache size: " + cache.size());
        System.out.println("key1: " + cache.get("key1"));
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nPattern: Stores frequently accessed data");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
