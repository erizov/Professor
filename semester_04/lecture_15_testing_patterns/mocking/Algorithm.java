/**
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
    }
}

class MockPaymentGateway implements PaymentGateway {
    int callCount = 0;
    Double lastAmount = null;
    boolean shouldSucceed = true;
    
    @Override
    public boolean processPayment(double amount, String cardNumber) {
        callCount++;
        lastAmount = amount;
        return shouldSucceed;
    }
}

class OrderService {
    private final PaymentGateway paymentGateway;
    
    OrderService(PaymentGateway paymentGateway) {
        this.paymentGateway = paymentGateway;
    }
    
    boolean placeOrder(double amount, String cardNumber) {
        if (amount <= 0) {
            return false;
        }
        return paymentGateway.processPayment(amount, cardNumber);
    }
}

interface EmailService {
    boolean sendEmail(String to, String subject, String body);
}

class RealEmailService implements EmailService {
    @Override
    public boolean sendEmail(String to, String subject, String body) {
        // Would send real email
        return true;
    }
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
    
    void save(String key, Object value) {
        data.put(key, value);
    }
    
    Object get(String key) {
        return data.get(key);
    }
    
    boolean delete(String key) {
        if (data.containsKey(key)) {
            data.remove(key);
            return true;
        }
        return false;
    }
}

public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    public static void main(String[] args) {
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        long startTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("MOCKING PATTERN DEMONSTRATION");
        logger.info(separator);
        logger.info("");
        
        // Example 1: Manual Mock
        logger.info("Example 1: Manual Mock Object");
        logger.info(dash);
        
        MockPaymentGateway mockGateway = new MockPaymentGateway();
        OrderService orderService = new OrderService(mockGateway);
        
        boolean result = orderService.placeOrder(100.0, "1234-5678-9012-3456");
        
        System.out.printf("Order placed: %s%n", result);
        System.out.printf("Payment gateway called: %d times%n", mockGateway.callCount);
        System.out.printf("Last amount: $%.2f%n", mockGateway.lastAmount);
        logger.info("");
        
        // Example 2: Mock Email Service
        logger.info("Example 2: Mock Email Service");
        logger.info(dash);
        
        MockEmailService mockEmail = new MockEmailService();
        NotificationService notificationService = new NotificationService(mockEmail);
        
        result = notificationService.notifyUser("user@example.com", "Test message");
        
        System.out.printf("Notification sent: %s%n", result);
        System.out.printf("Email service called: %s%n", mockEmail.callCount > 0);
        System.out.printf("Email sent to: %s%n", mockEmail.lastTo);
        logger.info("");
        
        // Example 3: Stub Implementation
        logger.info("Example 3: Stub Implementation");
        logger.info(dash);
        
        DatabaseStub dbStub = new DatabaseStub();
        Map<String, Object> user = new HashMap<>();
        user.put("name", "Alice");
        user.put("email", "alice@example.com");
        dbStub.save("user:123", user);
        
        @SuppressWarnings("unchecked")
        Map<String, Object> retrieved = (Map<String, Object>) dbStub.get("user:123");
        System.out.printf("Retrieved user: %s%n", retrieved);
        
        boolean deleted = dbStub.delete("user:123");
        System.out.printf("User deleted: %s%n", deleted);
        System.out.printf("User still exists: %s%n", dbStub.get("user:123") != null);
        logger.info("");
        
        long endTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("\nPattern Summary:");
        logger.info("\nIntent:");
        logger.info("  Creates mock objects that simulate the behavior of real");
        logger.info("  objects for testing. Allows testing in isolation.");
        logger.info("\nKey Advantages:");
        logger.info("  - Fast test execution");
        logger.info("  - Isolated testing");
        logger.info("  - No external dependencies");
        logger.info("  - Predictable behavior");
        logger.info("\nWhen to Use:");
        logger.info("  - External service dependencies");
        logger.info("  - Slow operations");
        logger.info("  - Unpredictable behavior");
        logger.info("  - Isolated unit testing");
        logger.info(separator);
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}