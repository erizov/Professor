import java.util.concurrent.*;

/**
 * Thread Pool Design Pattern.
 * 
 * Maintains pool of worker threads.
 */
public class Algorithm {
    
    static class Task implements Runnable {
        private int taskId;
        private int duration;
        
        Task(int taskId, int duration) {
            this.taskId = taskId;
            this.duration = duration;
        }
        
        public void run() {
            try {
                Thread.sleep(duration);
                System.out.println("Task " + taskId + " completed");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("THREAD POOL DESIGN PATTERN");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Using ExecutorService (Java's thread pool)
        ExecutorService executor = Executors.newFixedThreadPool(4);
        
        System.out.println("Submitting tasks to thread pool:");
        for (int i = 1; i <= 5; i++) {
            executor.submit(new Task(i, 100));
            System.out.println("  Submitted task " + i);
        }
        
        executor.shutdown();
        try {
            executor.awaitTermination(5, TimeUnit.SECONDS);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        System.out.println("All tasks completed!");
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nPattern: Reuses threads for tasks");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
