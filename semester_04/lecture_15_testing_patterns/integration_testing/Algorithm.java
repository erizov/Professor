package semester_04.lecture_15_testing_patterns.integration_testing;

import java.util.*;

import java.util.logging.Logger;
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
    private static final Logger logger = Logger.getLogger(TestRunner.class.getName());
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
        logger.info("Integration Test Results:");
        String dash = "-".repeat(70);
        logger.info(dash);
        
        long passed = results.stream().filter(r -> r.passed).count();
        long total = results.size();
        
        for (TestResult result : results) {
            String status = result.passed ? "✓ PASS" : "✗ FAIL";
            logger.info(String.format("{}: {}\n", status, result.testName));
            if (!result.passed) {
                logger.info(String.format("  Error: {}\n", result.message));
            }
            logger.info(String.format("  Time: {} ms\n", result.executionTime));
        }
        
        logger.info(dash);
        logger.info(String.format("Total: {}/{} passed\n", passed, total));
        logger.info("");
    }
}

public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());
    
    public static void main(String[] args) {
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        long startTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("INTEGRATION TESTING PATTERN DEMONSTRATION");
        logger.info(separator);
        logger.info("");
        
        // Example 1: Database Integration Test
        logger.info("Example 1: Database Integration Test");
        logger.info(dash);
        
        DatabaseIntegrationTest dbTest = new DatabaseIntegrationTest();
        TestResult result = dbTest.run();
        
        logger.info(String.format("Test: {}\n", result.testName));
        logger.info(String.format("Result: {}\n", result.passed ? "PASSED" : "FAILED"));
        logger.info(String.format("Message: {}\n", result.message));
        logger.info("");
        
        // Example 2: API Integration Test
        logger.info("Example 2: API Integration Test");
        logger.info(dash);
        
        APIIntegrationTest apiTest = new APIIntegrationTest();
        result = apiTest.run();
        
        logger.info(String.format("Test: {}\n", result.testName));
        logger.info(String.format("Result: {}\n", result.passed ? "PASSED" : "FAILED"));
        logger.info("");
        
        // Example 3: Test Suite
        logger.info("Example 3: Integration Test Suite");
        logger.info(dash);
        
        TestRunner runner = new TestRunner();
        runner.addTest(new DatabaseIntegrationTest());
        runner.addTest(new APIIntegrationTest());
        
        runner.runAll();
        runner.printResults();
        
        long endTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("\nPattern Summary:");
        logger.info("\nIntent:");
        logger.info("  Tests the integration between different components,");
        logger.info("  modules, or systems to ensure they work together correctly.");
        logger.info("\nKey Advantages:");
        logger.info("  - Catches integration issues early");
        logger.info("  - Tests real interactions");
        logger.info("  - Validates system behavior");
        logger.info("  - Confidence in deployments");
        logger.info("\nWhen to Use:");
        logger.info("  - Testing component interactions");
        logger.info("  - API integration");
        logger.info("  - Database integration");
        logger.info("  - End-to-end workflows");
        logger.info(separator);
        logger.info(String.format("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0));
    }
}
