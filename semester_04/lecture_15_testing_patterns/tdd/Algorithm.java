/**
package semester_04.lecture_15_testing_patterns.tdd;
 * Test-Driven Development (TDD) Pattern.
 * 
 * Development approach where tests are written before implementation.
 * Follows Red-Green-Refactor cycle: Write test (Red), Implement (Green), Refactor.
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
            throw new IllegalArgumentException("Division by zero");
        }
        return a / b;
    }
}

class Stack<T> {
    private final List<T> items = new ArrayList<>();
    
    void push(T item) {
        items.add(item);
    }
    
    T pop() {
        if (isEmpty()) {
            throw new IndexOutOfBoundsException("Stack is empty");
        }
        return items.remove(items.size() - 1);
    }
    
    T peek() {
        if (isEmpty()) {
            throw new IndexOutOfBoundsException("Stack is empty");
        }
        return items.get(items.size() - 1);
    }
    
    boolean isEmpty() {
        return items.isEmpty();
    }
    
    int size() {
        return items.size();
    }
}

class TDDTestRunner {
    private int passed = 0;
    private int failed = 0;
    
    boolean assertEqual(Object actual, Object expected, String message) {
        if (Objects.equals(actual, expected)) {
            passed++;
            return true;
        } else {
            failed++;
            System.out.printf("  ✗ FAIL: %s%n", message);
            System.out.printf("    Expected: %s, Got: %s%n", expected, actual);
            return false;
        }
    }
    
    boolean assertRaises(Runnable func, Class<? extends Exception> exceptionType, String message) {
        try {
            func.run();
            failed++;
            System.out.printf("  ✗ FAIL: %s - Expected %s%n", message, exceptionType.getSimpleName());
            return false;
        } catch (Exception e) {
            if (exceptionType.isInstance(e)) {
                passed++;
                return true;
            } else {
                failed++;
                System.out.printf("  ✗ FAIL: %s - Got %s instead of %s%n",
                                message, e.getClass().getSimpleName(), exceptionType.getSimpleName());
                return false;
            }
        }
    }
    
    void runTests() {
        logger.info("Running TDD Tests:");
        logger.info(dash);
        
        // Calculator tests
        Calculator calc = new Calculator();
        
        assertEqual(calc.add(2, 3), 5.0, "Add 2 + 3 = 5");
        assertEqual(calc.subtract(5, 3), 2.0, "Subtract 5 - 3 = 2");
        assertEqual(calc.multiply(4, 3), 12.0, "Multiply 4 * 3 = 12");
        assertEqual(calc.divide(10, 2), 5.0, "Divide 10 / 2 = 5");
        
        assertRaises(() -> calc.divide(10, 0), IllegalArgumentException.class,
                    "Division by zero raises IllegalArgumentException");
        
        // Stack tests
        Stack<Integer> stack = new Stack<>();
        
        assertEqual(stack.isEmpty(), true, "New stack is empty");
        assertEqual(stack.size(), 0, "New stack size is 0");
        
        stack.push(1);
        assertEqual(stack.isEmpty(), false, "Stack not empty after push");
        assertEqual(stack.size(), 1, "Stack size is 1 after one push");
        assertEqual(stack.peek(), 1, "Peek returns top item");
        
        stack.push(2);
        assertEqual(stack.peek(), 2, "Peek returns new top item");
        
        int popped = stack.pop();
        assertEqual(popped, 2, "Pop returns top item");
        assertEqual(stack.size(), 1, "Stack size after pop");
        
        assertRaises(() -> new Stack<Integer>().pop(), IndexOutOfBoundsException.class,
                    "Pop from empty stack raises IndexOutOfBoundsException");
        
        logger.info(dash);
        System.out.printf("Tests: %d passed, %d failed%n", passed, failed);
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
        logger.info("TEST-DRIVEN DEVELOPMENT (TDD) PATTERN DEMONSTRATION");
        logger.info(separator);
        logger.info("");
        
        // Example 1: TDD Cycle Demonstration
        logger.info("Example 1: TDD Red-Green-Refactor Cycle");
        logger.info(dash);
        
        logger.info("TDD Cycle:");
        logger.info("  1. RED: Write failing test");
        logger.info("  2. GREEN: Write minimal code to pass");
        logger.info("  3. REFACTOR: Improve code while keeping tests green");
        logger.info("");
        
        // Example 2: Running TDD Tests
        logger.info("Example 2: Running TDD Tests");
        logger.info(dash);
        
        TDDTestRunner runner = new TDDTestRunner();
        runner.runTests();
        
        // Example 3: TDD Benefits
        logger.info("Example 3: TDD Benefits Demonstration");
        logger.info(dash);
        
        Calculator calc = new Calculator();
        
        logger.info("Testing calculator with multiple scenarios:");
        System.out.printf("  ✓ add(1, 2) = %.0f (expected 3)%n", calc.add(1, 2));
        System.out.printf("  ✓ multiply(4, 5) = %.0f (expected 20)%n", calc.multiply(4, 5));
        System.out.printf("  ✓ divide(15, 3) = %.0f (expected 5)%n", calc.divide(15, 3));
        logger.info("");
        
        long endTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("\nPattern Summary:");
        logger.info("\nIntent:");
        logger.info("  Development approach where tests are written before");
        logger.info("  implementation. Follows Red-Green-Refactor cycle.");
        logger.info("\nTDD Cycle:");
        logger.info("  1. RED: Write failing test");
        logger.info("  2. GREEN: Write minimal code to make test pass");
        logger.info("  3. REFACTOR: Improve code while keeping tests green");
        logger.info("  4. Repeat");
        logger.info("\nKey Advantages:");
        logger.info("  - Better code design");
        logger.info("  - Comprehensive test coverage");
        logger.info("  - Confidence in refactoring");
        logger.info("  - Documentation through tests");
        logger.info("\nWhen to Use:");
        logger.info("  - Complex logic");
        logger.info("  - Critical functionality");
        logger.info("  - API development");
        logger.info(separator);
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}