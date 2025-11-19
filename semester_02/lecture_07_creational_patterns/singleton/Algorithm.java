/**
 * Singleton Design Pattern.
 * 
 * Ensures class has only one instance.
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    // Eager initialization (thread-safe)
    static class EagerSingleton {
        private static final EagerSingleton INSTANCE = new EagerSingleton();
        
        private EagerSingleton() {}
        
        public static EagerSingleton getInstance() {
            return INSTANCE;
        }
    }
    
    // Lazy initialization with double-checked locking
    static class LazySingleton {
        private static volatile LazySingleton instance;
        
        private LazySingleton() {}
        
        public static LazySingleton getInstance() {
            if (instance == null) {
                synchronized (LazySingleton.class) {
                    if (instance == null) {
                        instance = new LazySingleton();
                    }
                }
            }
            return instance;
        }
    }
    
    // Bill Pugh Singleton (best approach)
    static class BillPughSingleton {
        private BillPughSingleton() {}
        
        private static class SingletonHelper {
            private static final BillPughSingleton INSTANCE = 
                new BillPughSingleton();
        }
        
        public static BillPughSingleton getInstance() {
            return SingletonHelper.INSTANCE;
        }
    }
    
    // Example: Configuration Manager
    static class ConfigurationManager {
        private static volatile ConfigurationManager instance;
        private java.util.Map<String, String> config;
        
        private ConfigurationManager() {
            config = new java.util.HashMap<>();
        }
        
        public static ConfigurationManager getInstance() {
            if (instance == null) {
                synchronized (ConfigurationManager.class) {
                    if (instance == null) {
                        instance = new ConfigurationManager();
                    }
                }
            }
            return instance;
        }
        
        public void set(String key, String value) {
            config.put(key, value);
        }
        
        public String get(String key) {
            return config.get(key);
        }
    }
    
    // Example: Database Connection
    static class DatabaseConnection {
        private static DatabaseConnection instance;
        private String connectionString;
        private boolean connected;
        
        private DatabaseConnection() {
            connected = false;
        }
        
        public static synchronized DatabaseConnection getInstance() {
            if (instance == null) {
                instance = new DatabaseConnection();
            }
            return instance;
        }
        
        public void connect(String connectionString) {
            if (!connected) {
                this.connectionString = connectionString;
                this.connected = true;
                logger.info("Connected to: " + connectionString);
            }
        }
        
        public void disconnect() {
            if (connected) {
                connected = false;
                logger.info("Disconnected from database");
            }
        }
        
        public String executeQuery(String query) {
            if (!connected) {
                return "Error: Not connected";
            }
            return "Executed: " + query;
        }
    }
    
    public static void main(String[] args) {
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        long startTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("SINGLETON DESIGN PATTERN DEMONSTRATION");
        logger.info(separator);
        logger.info("");
        
        // Example 1: Configuration Manager
        logger.info("Example 1: Configuration Manager");
        logger.info(dash);
        
        ConfigurationManager config1 = ConfigurationManager.getInstance();
        config1.set("database_url", "localhost:5432");
        config1.set("debug", "true");
        
        ConfigurationManager config2 = ConfigurationManager.getInstance();
        logger.info("config1 == config2: " + (config1 == config2));
        logger.info("config2.get('database_url'): " + 
                         config2.get("database_url"));
        logger.info("");
        
        // Example 2: Database Connection
        logger.info("Example 2: Database Connection");
        logger.info(dash);
        
        DatabaseConnection db1 = DatabaseConnection.getInstance();
        db1.connect("postgresql://localhost:5432/mydb");
        
        DatabaseConnection db2 = DatabaseConnection.getInstance();
        logger.info("db1 == db2: " + (db1 == db2));
        logger.info(db2.executeQuery("SELECT * FROM users"));
        db1.disconnect();
        logger.info("");
        
        // Example 3: Different implementations
        logger.info("Example 3: Different Implementations");
        logger.info(dash);
        
        EagerSingleton eager1 = EagerSingleton.getInstance();
        EagerSingleton eager2 = EagerSingleton.getInstance();
        logger.info("Eager: " + (eager1 == eager2));
        
        LazySingleton lazy1 = LazySingleton.getInstance();
        LazySingleton lazy2 = LazySingleton.getInstance();
        logger.info("Lazy: " + (lazy1 == lazy2));
        
        BillPughSingleton bp1 = BillPughSingleton.getInstance();
        BillPughSingleton bp2 = BillPughSingleton.getInstance();
        logger.info("Bill Pugh: " + (bp1 == bp2));
        logger.info("");
        
        // Example 4: Thread Safety
        logger.info("Example 4: Thread Safety Test");
        logger.info(dash);
        
        final java.util.Set<ConfigurationManager> instances = 
            new java.util.HashSet<>();
        
        Thread[] threads = new Thread[10];
        for (int i = 0; i < threads.length; i++) {
            threads[i] = new Thread(() -> {
                instances.add(ConfigurationManager.getInstance());
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        
        logger.info("Created 10 threads");
        logger.info("Unique instances: " + instances.size());
        logger.info("All same: " + (instances.size() == 1));
        logger.info("");
        
        long endTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("\nPattern Summary:");
        logger.info("\nKey Advantages:");
        logger.info("  - Single instance guaranteed");
        logger.info("  - Global access point");
        logger.info("  - Lazy initialization");
        logger.info("\nWhen to Use:");
        logger.info("  - Configuration management");
        logger.info("  - Connection pools");
        logger.info("  - Logging");
        logger.info(separator);
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}