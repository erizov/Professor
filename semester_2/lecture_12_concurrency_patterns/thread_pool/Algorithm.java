import java.util.concurrent.*;

/**
 * Thread Pool Design Pattern.
 * 
 * Maintains pool of worker threads.
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
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
                logger.info("Task " + taskId + " completed");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        logger.info("=".repeat(70));
        logger.info("THREAD POOL DESIGN PATTERN");
        logger.info("=".repeat(70));
        logger.info();
        
        // Using ExecutorService (Java's thread pool)
        ExecutorService executor = Executors.newFixedThreadPool(4);
        
        logger.info("Submitting tasks to thread pool:");
        for (int i = 1; i <= 5; i++) {
            executor.submit(new Task(i, 100));
            logger.info("  Submitted task " + i);
        }
        
        executor.shutdown();
        try {
            executor.awaitTermination(5, TimeUnit.SECONDS);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        logger.info("All tasks completed!");
        logger.info();
        
        long endTime = System.nanoTime();
        
        logger.info("=".repeat(70));
        logger.info("\nPattern: Reuses threads for tasks");
        logger.info("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}