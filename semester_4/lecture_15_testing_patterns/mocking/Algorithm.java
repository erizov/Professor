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
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("MOCKING PATTERN DEMONSTRATION");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Example 1: Manual Mock
        System.out.println("Example 1: Manual Mock Object");
        System.out.println("-".repeat(70));
        
        MockPaymentGateway mockGateway = new MockPaymentGateway();
        OrderService orderService = new OrderService(mockGateway);
        
        boolean result = orderService.placeOrder(100.0, "1234-5678-9012-3456");
        
        System.out.printf("Order placed: %s%n", result);
        System.out.printf("Payment gateway called: %d times%n", mockGateway.callCount);
        System.out.printf("Last amount: $%.2f%n", mockGateway.lastAmount);
        System.out.println();
        
        // Example 2: Mock Email Service
        System.out.println("Example 2: Mock Email Service");
        System.out.println("-".repeat(70));
        
        MockEmailService mockEmail = new MockEmailService();
        NotificationService notificationService = new NotificationService(mockEmail);
        
        result = notificationService.notifyUser("user@example.com", "Test message");
        
        System.out.printf("Notification sent: %s%n", result);
        System.out.printf("Email service called: %s%n", mockEmail.callCount > 0);
        System.out.printf("Email sent to: %s%n", mockEmail.lastTo);
        System.out.println();
        
        // Example 3: Stub Implementation
        System.out.println("Example 3: Stub Implementation");
        System.out.println("-".repeat(70));
        
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
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nPattern Summary:");
        System.out.println("\nIntent:");
        System.out.println("  Creates mock objects that simulate the behavior of real");
        System.out.println("  objects for testing. Allows testing in isolation.");
        System.out.println("\nKey Advantages:");
        System.out.println("  - Fast test execution");
        System.out.println("  - Isolated testing");
        System.out.println("  - No external dependencies");
        System.out.println("  - Predictable behavior");
        System.out.println("\nWhen to Use:");
        System.out.println("  - External service dependencies");
        System.out.println("  - Slow operations");
        System.out.println("  - Unpredictable behavior");
        System.out.println("  - Isolated unit testing");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
