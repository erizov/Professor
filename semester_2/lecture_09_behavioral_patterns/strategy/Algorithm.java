import java.util.*;

/**
 * Strategy Design Pattern.
 * 
 * Encapsulates algorithms and makes them interchangeable.
 */
public class Algorithm {
    
    interface PaymentStrategy {
        boolean pay(double amount);
        String getName();
    }
    
    static class CreditCardStrategy implements PaymentStrategy {
        private String cardNumber;
        
        CreditCardStrategy(String cardNumber) {
            this.cardNumber = cardNumber;
        }
        
        public boolean pay(double amount) {
            System.out.printf("Processing $%.2f using Credit Card%n", amount);
            System.out.println("Card: ****" + cardNumber.substring(cardNumber.length() - 4));
            return true;
        }
        
        public String getName() {
            return "Credit Card";
        }
    }
    
    static class PayPalStrategy implements PaymentStrategy {
        private String email;
        
        PayPalStrategy(String email) {
            this.email = email;
        }
        
        public boolean pay(double amount) {
            System.out.printf("Processing $%.2f using PayPal%n", amount);
            System.out.println("Email: " + email);
            return true;
        }
        
        public String getName() {
            return "PayPal";
        }
    }
    
    static class PaymentProcessor {
        private PaymentStrategy strategy;
        
        void setStrategy(PaymentStrategy strategy) {
            this.strategy = strategy;
        }
        
        boolean processPayment(double amount) {
            if (strategy == null) {
                throw new IllegalArgumentException("No strategy set");
            }
            return strategy.pay(amount);
        }
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("STRATEGY DESIGN PATTERN");
        System.out.println("=".repeat(70));
        System.out.println();
        
        PaymentProcessor processor = new PaymentProcessor();
        
        processor.setStrategy(new CreditCardStrategy("1234567890123456"));
        processor.processPayment(100.0);
        System.out.println();
        
        processor.setStrategy(new PayPalStrategy("user@paypal.com"));
        processor.processPayment(50.0);
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nPattern: Encapsulates algorithms");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
