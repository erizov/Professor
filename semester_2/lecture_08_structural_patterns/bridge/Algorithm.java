/**
 * Bridge Design Pattern.
 * 
 * Decouples abstraction from implementation.
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    interface DrawingAPI {
        void drawCircle(double x, double y, double radius);
    }
    
    static class DrawingAPI1 implements DrawingAPI {
        public void drawCircle(double x, double y, double radius) {
            System.out.printf("API1.circle at (%.2f, %.2f) radius %.2f%n",
                            x, y, radius);
        }
    }
    
    static class DrawingAPI2 implements DrawingAPI {
        public void drawCircle(double x, double y, double radius) {
            System.out.printf("API2.circle at (%.2f, %.2f) radius %.2f%n",
                            x, y, radius);
        }
    }
    
    abstract static class Shape {
        protected DrawingAPI drawingAPI;
        
        Shape(DrawingAPI api) {
            this.drawingAPI = api;
        }
        
        abstract void draw();
    }
    
    static class CircleShape extends Shape {
        private double x, y, radius;
        
        CircleShape(double x, double y, double radius, DrawingAPI api) {
            super(api);
            this.x = x;
            this.y = y;
            this.radius = radius;
        }
        
        void draw() {
            drawingAPI.drawCircle(x, y, radius);
        }
    }
    
    public static void main(String[] args) {
        logger.info("=".repeat(70));
        logger.info("BRIDGE DESIGN PATTERN");
        logger.info("=".repeat(70));
        logger.info();
        
        Shape circle1 = new CircleShape(1, 2, 3, new DrawingAPI1());
        Shape circle2 = new CircleShape(5, 7, 11, new DrawingAPI2());
        
        circle1.draw();
        circle2.draw();
        logger.info();
        
        logger.info("=".repeat(70));
        logger.info("\nPrinciple: Decouples abstraction from implementation");
        logger.info("=".repeat(70));
    }
}