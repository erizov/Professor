/**
 * Open/Closed Principle (OCP).
 * 
 * Open for extension, closed for modification.
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    // GOOD: Open for extension
    interface Shape {
        double area();
    }
    
    static class Rectangle implements Shape {
        private double width, height;
        
        Rectangle(double width, double height) {
            this.width = width;
            this.height = height;
        }
        
        public double area() {
            return width * height;
        }
    }
    
    static class Circle implements Shape {
        private double radius;
        
        Circle(double radius) {
            this.radius = radius;
        }
        
        public double area() {
            return Math.PI * radius * radius;
        }
    }
    
    // Can add new shapes without modifying AreaCalculator
    static class Square implements Shape {
        private double side;
        
        Square(double side) {
            this.side = side;
        }
        
        public double area() {
            return side * side;
        }
    }
    
    static class AreaCalculator {
        double calculateTotalArea(java.util.List<Shape> shapes) {
            return shapes.stream()
                        .mapToDouble(Shape::area)
                        .sum();
        }
    }
    
    public static void main(String[] args) {
        logger.info("=".repeat(70));
        logger.info("OPEN/CLOSED PRINCIPLE");
        logger.info("=".repeat(70));
        logger.info();
        
        java.util.List<Shape> shapes = new java.util.ArrayList<>();
        shapes.add(new Rectangle(5, 3));
        shapes.add(new Circle(2));
        shapes.add(new Square(4));
        
        AreaCalculator calc = new AreaCalculator();
        double total = calc.calculateTotalArea(shapes);
        logger.info("Total area: " + total);
        logger.info();
        
        logger.info("=".repeat(70));
        logger.info("\nPrinciple: Open for extension, closed for modification");
        logger.info("=".repeat(70));
    }
}