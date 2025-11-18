/**
 * Liskov Substitution Principle (LSP) implementation.
 * 
 * Objects of a superclass should be replaceable with objects of its
 * subclasses without breaking the application.
 */
abstract class Shape {
    abstract double getArea();
}

import java.util.logging.Logger;
class Rectangle extends Shape {
    private double width;
    private double height;
    
    public Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }
    
    public double getArea() {
        return width * height;
    }
}

class Square extends Shape {
    private double side;
    
    public Square(double side) {
        this.side = side;
    }
    
    public double getArea() {
        return side * side;
    }
}

public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public static void printArea(Shape shape) {
        logger.info("Area: " + shape.getArea());
    }
    
    public static void main(String[] args) {
        logger.info("=".repeat(70));
        logger.info("LISKOV SUBSTITUTION PRINCIPLE DEMONSTRATION");
        logger.info("=".repeat(70));
        logger.info();
        
        // Example 1: Rectangle
        logger.info("Example 1: Rectangle");
        logger.info("-".repeat(70));
        Shape rectangle = new Rectangle(5, 4);
        printArea(rectangle);
        logger.info();
        
        // Example 2: Square (substitutable for Shape)
        logger.info("Example 2: Square");
        logger.info("-".repeat(70));
        Shape square = new Square(5);
        printArea(square);
        logger.info();
        
        // Example 3: Substitution
        logger.info("Example 3: Substitution in Array");
        logger.info("-".repeat(70));
        Shape[] shapes = {
            new Rectangle(3, 4),
            new Square(5),
            new Rectangle(2, 6)
        };
        
        for (Shape shape : shapes) {
            printArea(shape);
        }
        logger.info();
        
        logger.info("=".repeat(70));
        logger.info("\nPrinciple Summary:");
        logger.info("\nIntent:");
        logger.info("  Objects of a superclass should be replaceable");
        logger.info("  with objects of its subclasses.");
        logger.info("\nKey Benefits:");
        logger.info("  - Polymorphism works correctly");
        logger.info("  - Subtypes are truly substitutable");
        logger.info("  - No unexpected behavior");
        logger.info("  - Better code reuse");
        logger.info("=".repeat(70));
    }
}