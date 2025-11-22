package semester_02.lecture_07_creational_patterns.factory;

/*** Factory Design Pattern.
 * 
 * Creates objects without specifying exact class.
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    // Product interface
    interface Shape {
        String draw();
        double area();
    }
    
    // Concrete products
    static class Circle implements Shape {
        private double radius;
        
        Circle(double radius) {
            this.radius = radius;
        }
        
        public String draw() {
            return "Drawing Circle with radius " + radius;
        }
        
        public double area() {
            return Math.PI * radius * radius;
        }
    }
    
    static class Rectangle implements Shape {
        private double width, height;
        
        Rectangle(double width, double height) {
            this.width = width;
            this.height = height;
        }
        
        public String draw() {
            return "Drawing Rectangle " + width + "x" + height;
        }
        
        public double area() {
            return width * height;
        }
    }
    
    static class Triangle implements Shape {
        private double base, height;
        
        Triangle(double base, double height) {
            this.base = base;
            this.height = height;
        }
        
        public String draw() {
            return "Drawing Triangle base=" + base + ", height=" + height;
        }
        
        public double area() {
            return 0.5 * base * height;
        }
    }
    
    // Simple Factory
    static class ShapeFactory {
        public static Shape createShape(String type, double... args) {
            switch (type.toLowerCase()) {
                case "circle":
                    return new Circle(args[0]);
                case "rectangle":
                    return new Rectangle(args[0], args[1]);
                case "triangle":
                    return new Triangle(args[0], args[1]);
                default:
                    throw new IllegalArgumentException("Unknown shape: " + type);
            }
        }
    }
    
    // Factory Method Pattern
    interface Document {
        Page createPage();
        
        default void printDocument() {
            logger.info("Creating " + this.getClass().getSimpleName());
            for (int i = 0; i < 3; i++) {
                Page page = createPage();
                logger.info("  Page " + (i + 1) + ": " + page.render());
            }
        }
    }
    
    interface Page {
        String render();
    }
    
    static class PDFDocument implements Document {
        public Page createPage() {
            return new PDFPage();
        }
    }
    
    static class PDFPage implements Page {
        public String render() {
            return "Rendering PDF page with vector graphics";
        }
    }
    
    static class WordDocument implements Document {
        public Page createPage() {
            return new WordPage();
        }
    }
    
    static class WordPage implements Page {
        public String render() {
            return "Rendering Word page with formatted text";
        }
    }
    
    public static void main(String[] args) {
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        long startTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("FACTORY DESIGN PATTERN DEMONSTRATION");
        logger.info(separator);
        logger.info("");
        
        // Example 1: Simple Factory
        logger.info("Example 1: Simple Factory Pattern");
        logger.info(dash);
        
        Shape circle = ShapeFactory.createShape("circle", 5.0);
        logger.info(circle.draw());
        System.out.printf("Area: %.2f%n", circle.area());
        
        Shape rectangle = ShapeFactory.createShape("rectangle", 4.0, 6.0);
        logger.info(rectangle.draw());
        System.out.printf("Area: %.2f%n", rectangle.area());
        
        Shape triangle = ShapeFactory.createShape("triangle", 3.0, 4.0);
        logger.info(triangle.draw());
        System.out.printf("Area: %.2f%n", triangle.area());
        logger.info("");
        
        // Example 2: Factory Method
        logger.info("Example 2: Factory Method Pattern");
        logger.info(dash);
        
        Document pdfDoc = new PDFDocument();
        pdfDoc.printDocument();
        
        logger.info("");
        
        Document wordDoc = new WordDocument();
        wordDoc.printDocument();
        logger.info("");
        
        // Example 3: Multiple shapes
        logger.info("Example 3: Creating Multiple Objects");
        logger.info(dash);
        
        Object[][] specs = {
            {"circle", new double[]{3.0}},
            {"rectangle", new double[]{5.0, 2.0}},
            {"triangle", new double[]{4.0, 3.0}}
        };
        
        double totalArea = 0;
        for (Object[] spec : specs) {
            String type = (String) spec[0];
            double[] shapeArgs = (double[]) spec[1];
            Shape shape = ShapeFactory.createShape(type, shapeArgs);
            logger.info(shape.draw());
            double area = shape.area();
            System.out.printf("  Area: %.2f%n", area);
            totalArea += area;
        }
        
        System.out.printf("%nTotal area: %.2f%n", totalArea);
        logger.info("");
        
        // Example 4: Error handling
        logger.info("Example 4: Error Handling");
        logger.info(dash);
        
        try {
            Shape invalid = ShapeFactory.createShape("hexagon", 5.0);
        } catch (IllegalArgumentException e) {
            logger.info("Error: " + e.getMessage());
        }
        logger.info("");
        
        long endTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("\nPattern Summary:");
        logger.info("\nKey Advantages:");
        logger.info("  - Loose coupling");
        logger.info("  - Easy to extend");
        logger.info("  - Centralized creation");
        logger.info("\nWhen to Use:");
        logger.info("  - Multiple related types");
        logger.info("  - Runtime type determination");
        logger.info("  - Delegation to subclasses");
        logger.info(separator);
        System.out.printf("%nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
