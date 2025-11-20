/**
package semester_04.lecture_15_testing_patterns.unit_testing;
 * Unit Testing Pattern.
 * 
 * Tests individual units of code (functions, methods, classes) in isolation.
 * Ensures each unit works correctly before integration.
 */
import java.util.*;

import java.util.logging.Logger;
class Calculator {
    double add(double a, double b) {
        return a + b;
    }
    
    double subtract(double a, double b) {
        return a - b;
    }
    
    double multiply(double a, double b) {
        return a * b;
    }
    
    double divide(double a, double b) {
        if (b == 0) {
            throw new IllegalArgumentException("Cannot divide by zero");
        }
        return a / b;
    }
}

class TestCalculator {
    private final Calculator calculator = new Calculator();
    private int testsPassed = 0;
    private int testsFailed = 0;
    
    void assertEqual(Object actual, Object expected, String testName) {
        if (Objects.equals(actual, expected)) {
            System.out.printf("✓ %s: PASSED%n", testName);
            testsPassed++;
        } else {
            System.out.printf("✗ %s: FAILED (expected %s, got %s)%n",
                            testName, expected, actual);
            testsFailed++;
        }
    }
    
    void assertRaises(Runnable func, Class<? extends Exception> exceptionType,
                     String testName) {
        try {
            func.run();
            System.out.printf("✗ %s: FAILED (expected %s)%n",
                            testName, exceptionType.getSimpleName());
            testsFailed++;
        } catch (Exception e) {
            if (exceptionType.isInstance(e)) {
                System.out.printf("✓ %s: PASSED%n", testName);
                testsPassed++;
            } else {
                System.out.printf("✗ %s: FAILED (got %s)%n",
                                testName, e.getClass().getSimpleName());
                testsFailed++;
            }
        }
    }
    
    void testAdd() {
        assertEqual(calculator.add(2, 3), 5.0, "test_add");
        assertEqual(calculator.add(-1, 1), 0.0, "test_add_negative");
        assertEqual(calculator.add(0, 0), 0.0, "test_add_zero");
    }
    
    void testSubtract() {
        assertEqual(calculator.subtract(5, 3), 2.0, "test_subtract");
        assertEqual(calculator.subtract(0, 5), -5.0, "test_subtract_negative");
    }
    
    void testMultiply() {
        assertEqual(calculator.multiply(3, 4), 12.0, "test_multiply");
        assertEqual(calculator.multiply(0, 5), 0.0, "test_multiply_zero");
    }
    
    void testDivide() {
        assertEqual(calculator.divide(10, 2), 5.0, "test_divide");
        assertRaises(() -> calculator.divide(10, 0), IllegalArgumentException.class,
                    "test_divide_by_zero");
    }
    
    void runAllTests() {
        logger.info("Running unit tests...");
        logger.info("");
        testAdd();
        testSubtract();
        testMultiply();
        testDivide();
        logger.info("");
        System.out.printf("Tests passed: %d%n", testsPassed);
        System.out.printf("Tests failed: %d%n", testsFailed);
        System.out.printf("Total: %d%n", testsPassed + testsFailed);
    }
}

class UserService {
    private final List<Map<String, Object>> users = new ArrayList<>();
    
    Map<String, Object> createUser(String username, String email) {
        if (username == null || username.isEmpty() || email == null || email.isEmpty()) {
            throw new IllegalArgumentException("Username and email required");
        }
        Map<String, Object> user = new HashMap<>();
        user.put("id", users.size() + 1);
        user.put("username", username);
        user.put("email", email);
        users.add(user);
        return user;
    }
    
    Map<String, Object> getUser(int userId) {
        for (Map<String, Object> user : users) {
            if (user.get("id").equals(userId)) {
                return user;
            }
        }
        throw new IllegalArgumentException("User not found");
    }
}

class UserServiceTest {
    private final UserService service = new UserService();
    private int testsPassed = 0;
    private int testsFailed = 0;
    
    void assertEqual(Object actual, Object expected, String testName) {
        if (Objects.equals(actual, expected)) {
            System.out.printf("✓ %s: PASSED%n", testName);
            testsPassed++;
        } else {
            System.out.printf("✗ %s: FAILED (expected %s, got %s)%n",
                            testName, expected, actual);
            testsFailed++;
        }
    }
    
    void assertRaises(Runnable func, Class<? extends Exception> exceptionType,
                     String testName) {
        try {
            func.run();
            System.out.printf("✗ %s: FAILED (expected %s)%n",
                            testName, exceptionType.getSimpleName());
            testsFailed++;
        } catch (Exception e) {
            if (exceptionType.isInstance(e)) {
                System.out.printf("✓ %s: PASSED%n", testName);
                testsPassed++;
            } else {
                System.out.printf("✗ %s: FAILED (got %s)%n",
                                testName, e.getClass().getSimpleName());
                testsFailed++;
            }
        }
    }
    
    void testCreateUser() {
        Map<String, Object> user = service.createUser("alice", "alice@example.com");
        assertEqual(user.get("username"), "alice", "test_create_user");
        assertEqual(user.get("email"), "alice@example.com", "test_create_user_email");
    }
    
    void testCreateUserInvalid() {
        assertRaises(() -> service.createUser("", "email@example.com"),
                    IllegalArgumentException.class, "test_create_user_invalid");
    }
    
    void testGetUser() {
        Map<String, Object> user = service.createUser("bob", "bob@example.com");
        @SuppressWarnings("unchecked")
        Map<String, Object> found = service.getUser((Integer) user.get("id"));
        assertEqual(found.get("username"), "bob", "test_get_user");
    }
    
    void testGetUserNotFound() {
        assertRaises(() -> service.getUser(999), IllegalArgumentException.class,
                    "test_get_user_not_found");
    }
    
    void runAllTests() {
        logger.info("Running UserService unit tests...");
        logger.info("");
        testCreateUser();
        testCreateUserInvalid();
        testGetUser();
        testGetUserNotFound();
        logger.info("");
        System.out.printf("Tests passed: %d%n", testsPassed);
        System.out.printf("Tests failed: %d%n", testsFailed);
    }
}

public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    public static void main(String[] args) {
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        long startTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("UNIT TESTING PATTERN DEMONSTRATION");
        logger.info(separator);
        logger.info("");
        
        // Example 1: Manual Unit Tests
        logger.info("Example 1: Manual Unit Tests");
        logger.info(dash);
        
        TestCalculator testSuite = new TestCalculator();
        testSuite.runAllTests();
        logger.info("");
        
        // Example 2: User Service Tests
        logger.info("Example 2: User Service Unit Tests");
        logger.info(dash);
        
        UserServiceTest userTest = new UserServiceTest();
        userTest.runAllTests();
        logger.info("");
        
        long endTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("\nPattern Summary:");
        logger.info("\nIntent:");
        logger.info("  Test individual units of code (functions, methods, classes)");
        logger.info("  in isolation. Ensures each unit works correctly.");
        logger.info("\nKey Advantages:");
        logger.info("  - Early bug detection");
        logger.info("  - Confidence in code");
        logger.info("  - Documentation through tests");
        logger.info("  - Regression prevention");
        logger.info("\nWhen to Use:");
        logger.info("  - All production code");
        logger.info("  - Critical business logic");
        logger.info("  - Complex algorithms");
        logger.info("  - API endpoints");
        logger.info(separator);
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}