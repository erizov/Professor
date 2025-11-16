import java.util.*;

/**
 * Strategy Design Pattern.
 * 
 * Encapsulates algorithms and makes them interchangeable.
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    // Strategy interface
    interface SortingStrategy {
        List<Integer> sort(List<Integer> data);
        String getName();
    }
    
    // Concrete strategies
    static class BubbleSortStrategy implements SortingStrategy {
        public List<Integer> sort(List<Integer> data) {
            List<Integer> arr = new ArrayList<>(data);
            int n = arr.size();
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n - i - 1; j++) {
                    if (arr.get(j) > arr.get(j + 1)) {
                        Collections.swap(arr, j, j + 1);
                    }
                }
            }
            return arr;
        }
        
        public String getName() {
            return "Bubble Sort";
        }
    }
    
    static class QuickSortStrategy implements SortingStrategy {
        public List<Integer> sort(List<Integer> data) {
            if (data.size() <= 1) {
                return new ArrayList<>(data);
            }
            
            int pivot = data.get(data.size() / 2);
            List<Integer> left = new ArrayList<>();
            List<Integer> middle = new ArrayList<>();
            List<Integer> right = new ArrayList<>();
            
            for (int x : data) {
                if (x < pivot) left.add(x);
                else if (x == pivot) middle.add(x);
                else right.add(x);
            }
            
            List<Integer> result = new ArrayList<>();
            result.addAll(sort(left));
            result.addAll(middle);
            result.addAll(sort(right));
            return result;
        }
        
        public String getName() {
            return "Quick Sort";
        }
    }
    
    static class MergeSortStrategy implements SortingStrategy {
        public List<Integer> sort(List<Integer> data) {
            if (data.size() <= 1) {
                return new ArrayList<>(data);
            }
            
            int mid = data.size() / 2;
            List<Integer> left = sort(data.subList(0, mid));
            List<Integer> right = sort(data.subList(mid, data.size()));
            
            return merge(left, right);
        }
        
        private List<Integer> merge(List<Integer> left, 
                                    List<Integer> right) {
            List<Integer> result = new ArrayList<>();
            int i = 0, j = 0;
            
            while (i < left.size() && j < right.size()) {
                if (left.get(i) <= right.get(j)) {
                    result.add(left.get(i++));
                } else {
                    result.add(right.get(j++));
                }
            }
            
            while (i < left.size()) result.add(left.get(i++));
            while (j < right.size()) result.add(right.get(j++));
            
            return result;
        }
        
        public String getName() {
            return "Merge Sort";
        }
    }
    
    // Context
    static class Sorter {
        private SortingStrategy strategy;
        
        void setStrategy(SortingStrategy strategy) {
            this.strategy = strategy;
        }
        
        List<Integer> sort(List<Integer> data) {
            if (strategy == null) {
                throw new IllegalStateException("No strategy set");
            }
            return strategy.sort(data);
        }
    }
    
    // Payment Strategy Example
    interface PaymentStrategy {
        boolean pay(double amount);
        String getName();
    }
    
    static class CreditCardPayment implements PaymentStrategy {
        private String cardNumber;
        private String cvv;
        
        CreditCardPayment(String cardNumber, String cvv) {
            this.cardNumber = cardNumber;
            this.cvv = cvv;
        }
        
        public boolean pay(double amount) {
            System.out.printf("Processing $%.2f payment via Credit Card%n", 
                            amount);
            logger.info("Card: ****" + 
                            cardNumber.substring(cardNumber.length() - 4));
            return true;
        }
        
        public String getName() {
            return "Credit Card";
        }
    }
    
    static class PayPalPayment implements PaymentStrategy {
        private String email;
        
        PayPalPayment(String email) {
            this.email = email;
        }
        
        public boolean pay(double amount) {
            System.out.printf("Processing $%.2f payment via PayPal%n", amount);
            logger.info("Email: " + email);
            return true;
        }
        
        public String getName() {
            return "PayPal";
        }
    }
    
    static class ShoppingCart {
        private List<Item> items = new ArrayList<>();
        private PaymentStrategy paymentStrategy;
        
        void addItem(String name, double price) {
            items.add(new Item(name, price));
        }
        
        void setPaymentStrategy(PaymentStrategy strategy) {
            this.paymentStrategy = strategy;
        }
        
        boolean checkout() {
            if (items.isEmpty()) {
                logger.info("Cart is empty!");
                return false;
            }
            
            if (paymentStrategy == null) {
                logger.info("No payment method selected!");
                return false;
            }
            
            double total = items.stream()
                               .mapToDouble(item -> item.price)
                               .sum();
            
            System.out.printf("%nTotal: $%.2f%n", total);
            logger.info("Payment method: " + 
                             paymentStrategy.getName());
            
            return paymentStrategy.pay(total);
        }
    }
    
    static class Item {
        String name;
        double price;
        
        Item(String name, double price) {
            this.name = name;
            this.price = price;
        }
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        logger.info("=".repeat(70));
        logger.info("STRATEGY DESIGN PATTERN DEMONSTRATION");
        logger.info("=".repeat(70));
        logger.info();
        
        // Example 1: Sorting Strategies
        logger.info("Example 1: Sorting Strategies");
        logger.info("-".repeat(70));
        
        List<Integer> data = Arrays.asList(64, 34, 25, 12, 22, 11, 90);
        logger.info("Original data: " + data);
        
        Sorter sorter = new Sorter();
        
        SortingStrategy[] strategies = {
            new BubbleSortStrategy(),
            new QuickSortStrategy(),
            new MergeSortStrategy()
        };
        
        for (SortingStrategy strategy : strategies) {
            sorter.setStrategy(strategy);
            List<Integer> sorted = sorter.sort(data);
            logger.info(strategy.getName() + ": " + sorted);
        }
        logger.info();
        
        // Example 2: Payment Strategies
        logger.info("Example 2: Payment Strategies");
        logger.info("-".repeat(70));
        
        ShoppingCart cart = new ShoppingCart();
        cart.addItem("Laptop", 999.99);
        cart.addItem("Mouse", 29.99);
        cart.addItem("Keyboard", 79.99);
        
        PaymentStrategy[] payments = {
            new CreditCardPayment("1234567890123456", "123"),
            new PayPalPayment("user@example.com")
        };
        
        for (PaymentStrategy payment : payments) {
            cart.setPaymentStrategy(payment);
            cart.checkout();
            logger.info();
        }
        
        long endTime = System.nanoTime();
        
        logger.info("=".repeat(70));
        logger.info("\nPattern Summary:");
        logger.info("\nKey Advantages:");
        logger.info("  - Algorithms interchangeable at runtime");
        logger.info("  - Eliminates conditional statements");
        logger.info("  - Easy to add new strategies");
        logger.info("\nWhen to Use:");
        logger.info("  - Multiple ways to perform task");
        logger.info("  - Want to avoid conditionals");
        logger.info("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
