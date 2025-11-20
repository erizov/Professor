/**
package semester_04.lecture_15_testing_patterns.mocking;
 * Mocking Pattern.
 * 
 * Creates mock objects that simulate the behavior of real objects for testing.
 * Allows testing in isolation without dependencies on external systems.
 */
import java.util.*;

interface PaymentGateway {
    boolean processPayment(double amount, String cardNumber);
}

import java.util.logging.Logger;
class RealPaymentGateway implements PaymentGateway {
    @Override
    public boolean processPayment(double amount, String cardNumber) {
        // In real implementation, this would call external API
        return true;
                                public static void main(String[] args) {
        }
    }
                                            boolean result = orderService.placeOrder(100.0, "1234-5678-9012-3456");
                                            System.out.printf("Email sent to: %s%n", mockEmail.lastTo);
                                            user.put("email", "alice@example.com");
                                        logger.info(dash);
                                        logger.info("");
        
                                        Map<String, Object> retrieved = (Map<String, Object>) dbStub.get("user:123");
                                        long endTime = System.nanoTime();
                                        logger.info("\nIntent:");
                                        logger.info("  - No external dependencies");
                                        logger.info("  - Slow operations");
                    data.remove(key);
        boolean shouldSucceed = true;
            callCount++;
            return shouldSucceed;
                interface EmailService {
                                return true;
                                    logger.info("");
                                    MockPaymentGateway mockGateway = new MockPaymentGateway();
                                    System.out.printf("Payment gateway called: %d times%n", mockGateway.callCount);
                                    // Example 2: Mock Email Service
                                    result = notificationService.notifyUser("user@example.com", "Test message");
                                    // Example 3: Stub Implementation
                                    Map<String, Object> user = new HashMap<>();
        
        
                                    System.out.printf("User deleted: %s%n", deleted);
                                    logger.info("");
                                    logger.info(separator);
                                    logger.info("  objects for testing. Allows testing in isolation.");
                                    logger.info("  - Fast test execution");
                                    logger.info("\nWhen to Use:");

        void save(String key, Object value) {
}

class MockPaymentGateway implements PaymentGateway {
    int callCount = 0;
    Double lastAmount = null;
    
    @Override
    public boolean processPayment(double amount, String cardNumber) {
        lastAmount = amount;
        boolean placeOrder(double amount, String cardNumber) {
                    return false;
                    public boolean sendEmail(String to, String subject, String body) {
                                String separator = "=".repeat(70);
                                String dash = "-".repeat(70);
                                long startTime = System.nanoTime();
        
                                logger.info(separator);
                                logger.info("MOCKING PATTERN DEMONSTRATION");
                                logger.info(separator);
        
                                // Example 1: Manual Mock
                                logger.info("Example 1: Manual Mock Object");
        
                                OrderService orderService = new OrderService(mockGateway);
        
        
                                System.out.printf("Order placed: %s%n", result);
                                System.out.printf("Last amount: $%.2f%n", mockGateway.lastAmount);
        
                                logger.info("Example 2: Mock Email Service");
                                logger.info(dash);
        
                                MockEmailService mockEmail = new MockEmailService();
                                NotificationService notificationService = new NotificationService(mockEmail);
        
        
                                System.out.printf("Notification sent: %s%n", result);
                                System.out.printf("Email service called: %s%n", mockEmail.callCount > 0);
                                logger.info("");
        
                                logger.info("Example 3: Stub Implementation");
                                logger.info(dash);
                                DatabaseStub dbStub = new DatabaseStub();
                                user.put("name", "Alice");
                                dbStub.save("user:123", user);
                                @SuppressWarnings("unchecked")
                                System.out.printf("Retrieved user: %s%n", retrieved);
                                boolean deleted = dbStub.delete("user:123");
                                System.out.printf("User still exists: %s%n", dbStub.get("user:123") != null);
        
        
                                logger.info("\nPattern Summary:");
                                logger.info("  Creates mock objects that simulate the behavior of real");
                                logger.info("\nKey Advantages:");
                                logger.info("  - Isolated testing");
                                logger.info("  - Predictable behavior");
                                logger.info("  - External service dependencies");
                                logger.info("  - Unpredictable behavior");
                                logger.info("  - Isolated unit testing");
                                logger.info(separator);
                                System.out.printf("\nTotal time: %.3f ms%n",
                                                (endTime - startTime) / 1_000_000.0);
                            }
                        // Would send real email
                    }
                boolean sendEmail(String to, String subject, String body);
            }
            if (amount <= 0) {
            }
            return paymentGateway.processPayment(amount, cardNumber);
        }
}

class OrderService {
    private final PaymentGateway paymentGateway;
    
    OrderService(PaymentGateway paymentGateway) {
        this.paymentGateway = paymentGateway;
    }
    
}


class RealEmailService implements EmailService {
    @Override
}
class MockEmailService implements EmailService {
    int callCount = 0;
    String lastTo;
    String lastSubject;
    String lastBody;
    
    @Override
    public boolean sendEmail(String to, String subject, String body) {
        callCount++;
        lastTo = to;
        lastSubject = subject;
        lastBody = body;
        return true;
    }
}

class NotificationService {
    private final EmailService emailService;
    
    NotificationService(EmailService emailService) {
        this.emailService = emailService;
    }
    
    boolean notifyUser(String userEmail, String message) {
        return emailService.sendEmail(userEmail, "Notification", message);
    }
}

class DatabaseStub {
    private final Map<String, Object> data = new HashMap<>();
    
        data.put(key, value);
    }
    
    Object get(String key) {
        return data.get(key);
    }
    
    boolean delete(String key) {
        if (data.containsKey(key)) {
            return true;
        }
        return false;
    }
    public class Algorithm {
}

    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
}