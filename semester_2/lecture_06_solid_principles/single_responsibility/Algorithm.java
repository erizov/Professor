/**
 * Single Responsibility Principle (SRP).
 * 
 * A class should have only one reason to change.
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    // BAD: Multiple responsibilities
    static class BadEmployee {
        private String name;
        private double salary;
        
        BadEmployee(String name, double salary) {
            this.name = name;
            this.salary = salary;
        }
        
        double calculatePay() {
            return salary * 0.8;
        }
        
        void saveToDatabase() {
            logger.info("Saving " + name + " to database...");
        }
        
        void sendEmail(String message) {
            logger.info("Sending email to " + name + ": " + message);
        }
    }
    
    // GOOD: Single responsibility
    static class Employee {
        private String name;
        private double salary;
        
        Employee(String name, double salary) {
            this.name = name;
            this.salary = salary;
        }
        
        String getName() { return name; }
        double getSalary() { return salary; }
    }
    
    static class PayCalculator {
        static double calculatePay(Employee emp) {
            return emp.getSalary() * 0.8;
        }
    }
    
    static class EmailService {
        static void sendEmail(Employee emp, String message) {
            logger.info("Sending email to " + emp.getName() + 
                             ": " + message);
        }
    }
    
    public static void main(String[] args) {
        logger.info("=".repeat(70));
        logger.info("SINGLE RESPONSIBILITY PRINCIPLE");
        logger.info("=".repeat(70));
        logger.info();
        
        // Good example
        Employee emp = new Employee("John", 50000);
        double pay = PayCalculator.calculatePay(emp);
        logger.info("Pay: $" + pay);
        EmailService.sendEmail(emp, "Welcome!");
        logger.info();
        
        logger.info("=".repeat(70));
        logger.info("\nPrinciple: A class should have only one reason to change");
        logger.info("=".repeat(70));
    }
}