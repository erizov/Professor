/**
 * Integration Testing Pattern.
 * 
 * Tests the integration between different components, modules, or systems
 * to ensure they work together correctly.
 */
import java.util.*;

class TestResult {
    String testName;
    boolean passed;
    String message;
    double executionTime;
    
    TestResult(String testName, boolean passed, String message, double executionTime) {
        this.testName = testName;
        this.passed = passed;
        this.message = message;
        this.executionTime = executionTime;
    }
}

abstract class IntegrationTest {
    protected String name;
    protected boolean setupCalled = false;
    protected boolean teardownCalled = false;
    
    IntegrationTest(String name) {
        this.name = name;
    }
    
    void setup() {
        setupCalled = true;
    }
    
    void teardown() {
        teardownCalled = true;
    }
    
    TestResult run() {
        long start = System.nanoTime();
        
        try {
            setup();
            boolean result = execute();
            teardown();
            
            double elapsed = (System.nanoTime() - start) / 1_000_000.0;
            return new TestResult(name, result,
                                result ? "Test passed" : "Test failed",
                                elapsed);
        } catch (Exception e) {
            teardown();
            double elapsed = (System.nanoTime() - start) / 1_000_000.0;
            return new TestResult(name, false,
                                "Test error: " + e.getMessage(),
                                elapsed);
        }
    }
    
    abstract boolean execute();
}

class DatabaseService {
    private final Map<String, Object> data = new HashMap<>();
    
    void save(String key, Object value) {
        data.put(key, value);
    }
    
    Object get(String key) {
        return data.get(key);
    }
    
    void delete(String key) {
        data.remove(key);
    }
}

class UserService {
    private final DatabaseService db;
    
    UserService(DatabaseService db) {
        this.db = db;
    }
    
    void createUser(String userId, String name) {
        Map<String, Object> user = new HashMap<>();
        user.put("id", userId);
        user.put("name", name);
        db.save("user:" + userId, user);
    }
    
    @SuppressWarnings("unchecked")
    Map<String, Object> getUser(String userId) {
        return (Map<String, Object>) db.get("user:" + userId);
    }
}

class DatabaseIntegrationTest extends IntegrationTest {
    private DatabaseService db;
    private UserService userService;
    
    DatabaseIntegrationTest() {
        super("Database Integration Test");
    }
    
    @Override
    void setup() {
        super.setup();
        db = new DatabaseService();
        userService = new UserService(db);
    }
    
    @Override
    boolean execute() {
        userService.createUser("123", "Alice");
        Map<String, Object> user = userService.getUser("123");
        
        if (user == null || !"Alice".equals(user.get("name"))) {
            return false;
        }
        
        return true;
    }
}

class APIClient {
    private final String baseUrl;
    private final Map<String, Object> responses = new HashMap<>();
    
    APIClient(String baseUrl) {
        this.baseUrl = baseUrl;
    }
    
    @SuppressWarnings("unchecked")
    Map<String, Object> get(String endpoint) {
        return (Map<String, Object>) responses.getOrDefault(endpoint, new HashMap<>());
    }
    
    Map<String, Object> post(String endpoint, Map<String, Object> data) {
        responses.put(endpoint, data);
        Map<String, Object> result = new HashMap<>();
        result.put("status", "success");
        result.put("data", data);
        return result;
    }
}

class APIIntegrationTest extends IntegrationTest {
    private APIClient apiClient;
    
    APIIntegrationTest() {
        super("API Integration Test");
    }
    
    @Override
    void setup() {
        super.setup();
        apiClient = new APIClient("http://api.example.com");
    }
    
    @Override
    boolean execute() {
        Map<String, Object> data = new HashMap<>();
        data.put("name", "Bob");
        Map<String, Object> response = apiClient.post("/users", data);
        
        if (!"success".equals(response.get("status"))) {
            return false;
        }
        
        Map<String, Object> getData = apiClient.get("/users");
        return getData != null;
    }
}

class TestRunner {
    private final List<IntegrationTest> tests = new ArrayList<>();
    private final List<TestResult> results = new ArrayList<>();
    
    void addTest(IntegrationTest test) {
        tests.add(test);
    }
    
    List<TestResult> runAll() {
        results.clear();
        
        for (IntegrationTest test : tests) {
            TestResult result = test.run();
            results.add(result);
        }
        
        return results;
    }
    
    void printResults() {
        System.out.println("Integration Test Results:");
        System.out.println("-".repeat(70));
        
        long passed = results.stream().filter(r -> r.passed).count();
        long total = results.size();
        
        for (TestResult result : results) {
            String status = result.passed ? "✓ PASS" : "✗ FAIL";
            System.out.printf("%s: %s%n", status, result.testName);
            if (!result.passed) {
                System.out.printf("  Error: %s%n", result.message);
            }
            System.out.printf("  Time: %.2f ms%n", result.executionTime);
        }
        
        System.out.println("-".repeat(70));
        System.out.printf("Total: %d/%d passed%n", passed, total);
        System.out.println();
    }
}

public class Algorithm {
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("INTEGRATION TESTING PATTERN DEMONSTRATION");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Example 1: Database Integration Test
        System.out.println("Example 1: Database Integration Test");
        System.out.println("-".repeat(70));
        
        DatabaseIntegrationTest dbTest = new DatabaseIntegrationTest();
        TestResult result = dbTest.run();
        
        System.out.printf("Test: %s%n", result.testName);
        System.out.printf("Result: %s%n", result.passed ? "PASSED" : "FAILED");
        System.out.printf("Message: %s%n", result.message);
        System.out.println();
        
        // Example 2: API Integration Test
        System.out.println("Example 2: API Integration Test");
        System.out.println("-".repeat(70));
        
        APIIntegrationTest apiTest = new APIIntegrationTest();
        result = apiTest.run();
        
        System.out.printf("Test: %s%n", result.testName);
        System.out.printf("Result: %s%n", result.passed ? "PASSED" : "FAILED");
        System.out.println();
        
        // Example 3: Test Suite
        System.out.println("Example 3: Integration Test Suite");
        System.out.println("-".repeat(70));
        
        TestRunner runner = new TestRunner();
        runner.addTest(new DatabaseIntegrationTest());
        runner.addTest(new APIIntegrationTest());
        
        runner.runAll();
        runner.printResults();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nPattern Summary:");
        System.out.println("\nIntent:");
        System.out.println("  Tests the integration between different components,");
        System.out.println("  modules, or systems to ensure they work together correctly.");
        System.out.println("\nKey Advantages:");
        System.out.println("  - Catches integration issues early");
        System.out.println("  - Tests real interactions");
        System.out.println("  - Validates system behavior");
        System.out.println("  - Confidence in deployments");
        System.out.println("\nWhen to Use:");
        System.out.println("  - Testing component interactions");
        System.out.println("  - API integration");
        System.out.println("  - Database integration");
        System.out.println("  - End-to-end workflows");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
