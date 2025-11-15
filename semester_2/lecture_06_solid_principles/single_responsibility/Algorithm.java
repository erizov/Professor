/**
 * Single Responsibility Principle (SRP).
 * 
 * A class should have only one reason to change.
 */
public class Algorithm {
    
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
            System.out.println("Saving " + name + " to database...");
        }
        
        void sendEmail(String message) {
            System.out.println("Sending email to " + name + ": " + message);
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
            System.out.println("Sending email to " + emp.getName() + 
                             ": " + message);
        }
    }
    
    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("SINGLE RESPONSIBILITY PRINCIPLE");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Good example
        Employee emp = new Employee("John", 50000);
        double pay = PayCalculator.calculatePay(emp);
        System.out.println("Pay: $" + pay);
        EmailService.sendEmail(emp, "Welcome!");
        System.out.println();
        
        System.out.println("=".repeat(70));
        System.out.println("\nPrinciple: A class should have only one reason to change");
        System.out.println("=".repeat(70));
    }
}
