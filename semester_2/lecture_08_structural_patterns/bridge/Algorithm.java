/**
 * Bridge Design Pattern.
 * 
 * Decouples abstraction from implementation.
 */
public class Algorithm {
    
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
        System.out.println("=".repeat(70));
        System.out.println("BRIDGE DESIGN PATTERN");
        System.out.println("=".repeat(70));
        System.out.println();
        
        Shape circle1 = new CircleShape(1, 2, 3, new DrawingAPI1());
        Shape circle2 = new CircleShape(5, 7, 11, new DrawingAPI2());
        
        circle1.draw();
        circle2.draw();
        System.out.println();
        
        System.out.println("=".repeat(70));
        System.out.println("\nPrinciple: Decouples abstraction from implementation");
        System.out.println("=".repeat(70));
    }
}
