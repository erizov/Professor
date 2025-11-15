import java.util.*;

/**
 * Priority Queue implementation using binary heap.
 * 
 * O(log n) insert and delete, O(1) peek.
 */
public class Algorithm {
    
    static class PriorityQueue<T> {
        private List<Entry<T>> heap;
        private boolean maxPriority;
        private int counter;
        
        private static class Entry<T> {
            int priority;
            int insertionOrder;
            T item;
            
            Entry(int priority, int insertionOrder, T item) {
                this.priority = priority;
                this.insertionOrder = insertionOrder;
                this.item = item;
            }
        }
        
        PriorityQueue(boolean maxPriority) {
            this.heap = new ArrayList<>();
            this.maxPriority = maxPriority;
            this.counter = 0;
        }
        
        PriorityQueue() {
            this(false);
        }
        
        void push(T item, int priority) {
            if (maxPriority) {
                priority = -priority; // Negate for max-heap
            }
            heap.add(new Entry<>(priority, counter++, item));
            heapifyUp(heap.size() - 1);
        }
        
        T pop() {
            if (heap.isEmpty()) {
                return null;
            }
            
            T top = heap.get(0).item;
            heap.set(0, heap.get(heap.size() - 1));
            heap.remove(heap.size() - 1);
            
            if (!heap.isEmpty()) {
                heapifyDown(0);
            }
            
            return top;
        }
        
        T peek() {
            return heap.isEmpty() ? null : heap.get(0).item;
        }
        
        boolean isEmpty() {
            return heap.isEmpty();
        }
        
        int size() {
            return heap.size();
        }
        
        private void heapifyUp(int index) {
            while (index > 0) {
                int parent = (index - 1) / 2;
                if (compare(heap.get(index), heap.get(parent)) >= 0) {
                    break;
                }
                Collections.swap(heap, index, parent);
                index = parent;
            }
        }
        
        private void heapifyDown(int index) {
            while (true) {
                int left = 2 * index + 1;
                int right = 2 * index + 2;
                int smallest = index;
                
                if (left < heap.size() && 
                    compare(heap.get(left), heap.get(smallest)) < 0) {
                    smallest = left;
                }
                
                if (right < heap.size() && 
                    compare(heap.get(right), heap.get(smallest)) < 0) {
                    smallest = right;
                }
                
                if (smallest == index) {
                    break;
                }
                
                Collections.swap(heap, index, smallest);
                index = smallest;
            }
        }
        
        private int compare(Entry<T> a, Entry<T> b) {
            if (a.priority != b.priority) {
                return Integer.compare(a.priority, b.priority);
            }
            return Integer.compare(a.insertionOrder, b.insertionOrder);
        }
    }
    
    static class Task {
        String name;
        int priority;
        
        Task(String name, int priority) {
            this.name = name;
            this.priority = priority;
        }
        
        public String toString() {
            return "Task(" + name + ", priority=" + priority + ")";
        }
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("PRIORITY QUEUE DEMONSTRATION");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Example 1: Min priority queue
        System.out.println("Example 1: Min Priority Queue");
        System.out.println("-".repeat(70));
        
        PriorityQueue<String> pq = new PriorityQueue<>(false);
        
        pq.push("Task A", 5);
        pq.push("Task B", 1);
        pq.push("Task C", 3);
        pq.push("Task D", 2);
        
        System.out.println("Processing tasks in priority order:");
        while (!pq.isEmpty()) {
            System.out.println("  Processing: " + pq.pop());
        }
        System.out.println();
        
        // Example 2: Task scheduling
        System.out.println("Example 2: Task Scheduling");
        System.out.println("-".repeat(70));
        
        PriorityQueue<Task> taskQueue = new PriorityQueue<>(false);
        taskQueue.push(new Task("Email", 3), 3);
        taskQueue.push(new Task("Urgent Bug Fix", 1), 1);
        taskQueue.push(new Task("Code Review", 4), 4);
        taskQueue.push(new Task("Critical Issue", 0), 0);
        
        System.out.println("Task execution order:");
        int order = 1;
        while (!taskQueue.isEmpty()) {
            System.out.println("  " + order + ". " + taskQueue.pop());
            order++;
        }
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nComplexity Summary:");
        System.out.println("  Push: O(log n)");
        System.out.println("  Pop: O(log n)");
        System.out.println("  Peek: O(1)");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
