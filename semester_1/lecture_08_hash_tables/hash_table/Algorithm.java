import java.util.*;

/**
 * Hash Table implementation with chaining.
 * 
 * Average O(1) operations for insert, lookup, delete.
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    static class HashTable<K, V> {
        private static class Entry<K, V> {
            K key;
            V value;
            
            Entry(K key, V value) {
                this.key = key;
                this.value = value;
            }
        }
        
        private List<List<Entry<K, V>>> buckets;
        private int capacity;
        private int size;
        private double loadFactor;
        
        HashTable(int initialCapacity, double loadFactor) {
            this.capacity = initialCapacity;
            this.loadFactor = loadFactor;
            this.size = 0;
            this.buckets = new ArrayList<>();
            for (int i = 0; i < capacity; i++) {
                buckets.add(new ArrayList<>());
            }
        }
        
        HashTable() {
            this(16, 0.75);
        }
        
        private int hash(K key) {
            return Math.abs(key.hashCode() % capacity);
        }
        
        private void resize() {
            List<List<Entry<K, V>>> oldBuckets = buckets;
            capacity *= 2;
            size = 0;
            buckets = new ArrayList<>();
            for (int i = 0; i < capacity; i++) {
                buckets.add(new ArrayList<>());
            }
            
            // Rehash all entries
            for (List<Entry<K, V>> bucket : oldBuckets) {
                for (Entry<K, V> entry : bucket) {
                    put(entry.key, entry.value);
                }
            }
        }
        
        void put(K key, V value) {
            int index = hash(key);
            List<Entry<K, V>> bucket = buckets.get(index);
            
            // Check if key exists
            for (Entry<K, V> entry : bucket) {
                if (entry.key.equals(key)) {
                    entry.value = value; // Update
                    return;
                }
            }
            
            // Add new entry
            bucket.add(new Entry<>(key, value));
            size++;
            
            // Check if resize needed
            if (size > capacity * loadFactor) {
                resize();
            }
        }
        
        V get(K key) {
            int index = hash(key);
            List<Entry<K, V>> bucket = buckets.get(index);
            
            for (Entry<K, V> entry : bucket) {
                if (entry.key.equals(key)) {
                    return entry.value;
                }
            }
            
            return null;
        }
        
        boolean remove(K key) {
            int index = hash(key);
            List<Entry<K, V>> bucket = buckets.get(index);
            
            for (int i = 0; i < bucket.size(); i++) {
                if (bucket.get(i).key.equals(key)) {
                    bucket.remove(i);
                    size--;
                    return true;
                }
            }
            
            return false;
        }
        
        boolean containsKey(K key) {
            return get(key) != null;
        }
        
        int size() {
            return size;
        }
        
        boolean isEmpty() {
            return size == 0;
        }
        
        public String toString() {
            StringBuilder sb = new StringBuilder("{");
            boolean first = true;
            for (List<Entry<K, V>> bucket : buckets) {
                for (Entry<K, V> entry : bucket) {
                    if (!first) sb.append(", ");
                    sb.append(entry.key).append("=").append(entry.value);
                    first = false;
                }
            }
            sb.append("}");
            return sb.toString();
        }
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        logger.info("=".repeat(70));
        logger.info("HASH TABLE DEMONSTRATION");
        logger.info("=".repeat(70));
        logger.info();
        
        // Example 1: Basic operations
        logger.info("Example 1: Basic Operations");
        logger.info("-".repeat(70));
        
        HashTable<String, Integer> ht = new HashTable<>();
        
        ht.put("apple", 5);
        ht.put("banana", 3);
        ht.put("cherry", 8);
        ht.put("date", 2);
        
        logger.info("Hash table: " + ht);
        logger.info("Size: " + ht.size());
        logger.info("Get 'apple': " + ht.get("apple"));
        logger.info("Contains 'cherry': " + ht.containsKey("cherry"));
        logger.info();
        
        // Example 2: Update and remove
        logger.info("Example 2: Update and Remove");
        logger.info("-".repeat(70));
        
        ht.put("apple", 10);
        logger.info("After updating 'apple' to 10: " + ht);
        
        ht.remove("banana");
        logger.info("After removing 'banana': " + ht);
        logger.info("Size: " + ht.size());
        logger.info();
        
        // Example 3: Integer keys
        logger.info("Example 3: Integer Keys");
        logger.info("-".repeat(70));
        
        HashTable<Integer, String> ht2 = new HashTable<>();
        ht2.put(1, "one");
        ht2.put(2, "two");
        ht2.put(3, "three");
        ht2.put(100, "hundred");
        
        logger.info("Hash table with integers: " + ht2);
        logger.info("Get key 100: " + ht2.get(100));
        logger.info();
        
        long endTime = System.nanoTime();
        
        logger.info("=".repeat(70));
        logger.info("\nComplexity Summary:");
        logger.info("  Average: O(1) for all operations");
        logger.info("  Worst: O(n) with collisions");
        logger.info("  Space: O(n)");
        logger.info("\nKey Advantages:");
        logger.info("  - Fast average-case operations");
        logger.info("  - Flexible key types");
        logger.info("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}