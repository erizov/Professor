/**
 * Factory Design Pattern.
 * 
 * Creates objects without specifying exact class.
 */
public class Algorithm {
    
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
            System.out.println("Creating " + this.getClass().getSimpleName());
            for (int i = 0; i < 3; i++) {
                Page page = createPage();
                System.out.println("  Page " + (i + 1) + ": " + page.render());
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
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("FACTORY DESIGN PATTERN DEMONSTRATION");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Example 1: Simple Factory
        System.out.println("Example 1: Simple Factory Pattern");
        System.out.println("-".repeat(70));
        
        Shape circle = ShapeFactory.createShape("circle", 5.0);
        System.out.println(circle.draw());
        System.out.printf("Area: %.2f%n", circle.area());
        
        Shape rectangle = ShapeFactory.createShape("rectangle", 4.0, 6.0);
        System.out.println(rectangle.draw());
        System.out.printf("Area: %.2f%n", rectangle.area());
        
        Shape triangle = ShapeFactory.createShape("triangle", 3.0, 4.0);
        System.out.println(triangle.draw());
        System.out.printf("Area: %.2f%n", triangle.area());
        System.out.println();
        
        // Example 2: Factory Method
        System.out.println("Example 2: Factory Method Pattern");
        System.out.println("-".repeat(70));
        
        Document pdfDoc = new PDFDocument();
        pdfDoc.printDocument();
        
        System.out.println();
        
        Document wordDoc = new WordDocument();
        wordDoc.printDocument();
        System.out.println();
        
        // Example 3: Multiple shapes
        System.out.println("Example 3: Creating Multiple Objects");
        System.out.println("-".repeat(70));
        
        Object[][] specs = {
            {"circle", new double[]{3.0}},
            {"rectangle", new double[]{5.0, 2.0}},
            {"triangle", new double[]{4.0, 3.0}}
        };
        
        double totalArea = 0;
        for (Object[] spec : specs) {
            String type = (String) spec[0];
            double[] args = (double[]) spec[1];
            Shape shape = ShapeFactory.createShape(type, args);
            System.out.println(shape.draw());
            double area = shape.area();
            System.out.printf("  Area: %.2f%n", area);
            totalArea += area;
        }
        
        System.out.printf("%nTotal area: %.2f%n", totalArea);
        System.out.println();
        
        // Example 4: Error handling
        System.out.println("Example 4: Error Handling");
        System.out.println("-".repeat(70));
        
        try {
            Shape invalid = ShapeFactory.createShape("hexagon", 5.0);
        } catch (IllegalArgumentException e) {
            System.out.println("Error: " + e.getMessage());
        }
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nPattern Summary:");
        System.out.println("\nKey Advantages:");
        System.out.println("  - Loose coupling");
        System.out.println("  - Easy to extend");
        System.out.println("  - Centralized creation");
        System.out.println("\nWhen to Use:");
        System.out.println("  - Multiple related types");
        System.out.println("  - Runtime type determination");
        System.out.println("  - Delegation to subclasses");
        System.out.println("=".repeat(70));
        System.out.printf("%nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
