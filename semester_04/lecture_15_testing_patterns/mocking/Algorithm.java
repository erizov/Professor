// package semester_04.lecture_15_testing_patterns.mocking;

import java.util.HashMap;
import java.util.Map;
import java.util.logging.Logger;

public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Mocking");
        System.out.println("=".repeat(70));

        MockPaymentGateway mockGateway = new MockPaymentGateway();
        OrderService orderService = new OrderService(mockGateway);
        boolean placed = orderService.placeOrder(42.5, "1234-5678-9012-3456");
        System.out.printf("Order placed: %s%n", placed);
        System.out.printf("Gateway call count: %d%n", mockGateway.getCallCount());

        MockEmailService mockEmail = new MockEmailService();
        NotificationService notificationService = new NotificationService(mockEmail);
        notificationService.notifyUser("user@example.com", "Test message");
        System.out.printf("Email sent to: %s%n", mockEmail.getLastTo());

        DatabaseStub stub = new DatabaseStub();
        stub.save("user:1", Map.of("name", "Alice"));
        System.out.println("User in stub: " + stub.get("user:1"));

        System.out.println("=".repeat(70));
    }
}

interface PaymentGateway {
    boolean processPayment(double amount, String cardNumber);
}

class MockPaymentGateway implements PaymentGateway {
    private int callCount = 0;
    private double lastAmount = 0;

    @Override
    public boolean processPayment(double amount, String cardNumber) {
        callCount++;
        lastAmount = amount;
        return amount > 0;
    }

    int getCallCount() {
        return callCount;
    }

    double getLastAmount() {
        return lastAmount;
    }
}

class OrderService {
    private final PaymentGateway paymentGateway;

    OrderService(PaymentGateway paymentGateway) {
        this.paymentGateway = paymentGateway;
    }

    boolean placeOrder(double amount, String cardNumber) {
        return paymentGateway.processPayment(amount, cardNumber);
    }
}

interface EmailService {
    boolean sendEmail(String to, String subject, String body);
}

class MockEmailService implements EmailService {
    private String lastTo;
    private String lastSubject;
    private String lastBody;

    @Override
    public boolean sendEmail(String to, String subject, String body) {
        lastTo = to;
        lastSubject = subject;
        lastBody = body;
        return true;
    }

    String getLastTo() {
        return lastTo;
    }
}

class NotificationService {
    private final EmailService emailService;

    NotificationService(EmailService emailService) {
        this.emailService = emailService;
    }

    boolean notifyUser(String email, String message) {
        return emailService.sendEmail(email, "Notification", message);
    }
}

class DatabaseStub {
    private final Map<String, Object> store = new HashMap<>();

    void save(String key, Object value) {
        store.put(key, value);
    }

    Object get(String key) {
        return store.get(key);
    }

    boolean delete(String key) {
        return store.remove(key) != null;
    }
}

