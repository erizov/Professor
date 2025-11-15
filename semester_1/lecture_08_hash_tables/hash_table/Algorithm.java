import java.util.*;

/**
 * Hash Table implementation with chaining.
 * 
 * Average O(1) operations for insert, lookup, delete.
 */
public class Algorithm {
    
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
        
        System.out.println("=".repeat(70));
        System.out.println("HASH TABLE DEMONSTRATION");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Example 1: Basic operations
        System.out.println("Example 1: Basic Operations");
        System.out.println("-".repeat(70));
        
        HashTable<String, Integer> ht = new HashTable<>();
        
        ht.put("apple", 5);
        ht.put("banana", 3);
        ht.put("cherry", 8);
        ht.put("date", 2);
        
        System.out.println("Hash table: " + ht);
        System.out.println("Size: " + ht.size());
        System.out.println("Get 'apple': " + ht.get("apple"));
        System.out.println("Contains 'cherry': " + ht.containsKey("cherry"));
        System.out.println();
        
        // Example 2: Update and remove
        System.out.println("Example 2: Update and Remove");
        System.out.println("-".repeat(70));
        
        ht.put("apple", 10);
        System.out.println("After updating 'apple' to 10: " + ht);
        
        ht.remove("banana");
        System.out.println("After removing 'banana': " + ht);
        System.out.println("Size: " + ht.size());
        System.out.println();
        
        // Example 3: Integer keys
        System.out.println("Example 3: Integer Keys");
        System.out.println("-".repeat(70));
        
        HashTable<Integer, String> ht2 = new HashTable<>();
        ht2.put(1, "one");
        ht2.put(2, "two");
        ht2.put(3, "three");
        ht2.put(100, "hundred");
        
        System.out.println("Hash table with integers: " + ht2);
        System.out.println("Get key 100: " + ht2.get(100));
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nComplexity Summary:");
        System.out.println("  Average: O(1) for all operations");
        System.out.println("  Worst: O(n) with collisions");
        System.out.println("  Space: O(n)");
        System.out.println("\nKey Advantages:");
        System.out.println("  - Fast average-case operations");
        System.out.println("  - Flexible key types");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
