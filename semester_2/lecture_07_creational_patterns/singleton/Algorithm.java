/**
 * Singleton Design Pattern.
 * 
 * Ensures class has only one instance.
 */
public class Algorithm {
    
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
                System.out.println("Connected to: " + connectionString);
            }
        }
        
        public void disconnect() {
            if (connected) {
                connected = false;
                System.out.println("Disconnected from database");
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
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("SINGLETON DESIGN PATTERN DEMONSTRATION");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Example 1: Configuration Manager
        System.out.println("Example 1: Configuration Manager");
        System.out.println("-".repeat(70));
        
        ConfigurationManager config1 = ConfigurationManager.getInstance();
        config1.set("database_url", "localhost:5432");
        config1.set("debug", "true");
        
        ConfigurationManager config2 = ConfigurationManager.getInstance();
        System.out.println("config1 == config2: " + (config1 == config2));
        System.out.println("config2.get('database_url'): " + 
                         config2.get("database_url"));
        System.out.println();
        
        // Example 2: Database Connection
        System.out.println("Example 2: Database Connection");
        System.out.println("-".repeat(70));
        
        DatabaseConnection db1 = DatabaseConnection.getInstance();
        db1.connect("postgresql://localhost:5432/mydb");
        
        DatabaseConnection db2 = DatabaseConnection.getInstance();
        System.out.println("db1 == db2: " + (db1 == db2));
        System.out.println(db2.executeQuery("SELECT * FROM users"));
        db1.disconnect();
        System.out.println();
        
        // Example 3: Different implementations
        System.out.println("Example 3: Different Implementations");
        System.out.println("-".repeat(70));
        
        EagerSingleton eager1 = EagerSingleton.getInstance();
        EagerSingleton eager2 = EagerSingleton.getInstance();
        System.out.println("Eager: " + (eager1 == eager2));
        
        LazySingleton lazy1 = LazySingleton.getInstance();
        LazySingleton lazy2 = LazySingleton.getInstance();
        System.out.println("Lazy: " + (lazy1 == lazy2));
        
        BillPughSingleton bp1 = BillPughSingleton.getInstance();
        BillPughSingleton bp2 = BillPughSingleton.getInstance();
        System.out.println("Bill Pugh: " + (bp1 == bp2));
        System.out.println();
        
        // Example 4: Thread Safety
        System.out.println("Example 4: Thread Safety Test");
        System.out.println("-".repeat(70));
        
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
        
        System.out.println("Created 10 threads");
        System.out.println("Unique instances: " + instances.size());
        System.out.println("All same: " + (instances.size() == 1));
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nPattern Summary:");
        System.out.println("\nKey Advantages:");
        System.out.println("  - Single instance guaranteed");
        System.out.println("  - Global access point");
        System.out.println("  - Lazy initialization");
        System.out.println("\nWhen to Use:");
        System.out.println("  - Configuration management");
        System.out.println("  - Connection pools");
        System.out.println("  - Logging");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
