import java.util.*;

/**
 * Prototype Design Pattern.
 * 
 * Creates objects by cloning prototypes.
 */
public class Algorithm {
    
    interface Prototype {
        Prototype clone();
    }
    
    static class Document implements Prototype {
        private String title;
        private String content;
        private String author;
        private List<String> pages;
        
        Document(String title, String content, String author) {
            this.title = title;
            this.content = content;
            this.author = author;
            this.pages = new ArrayList<>();
        }
        
        private Document(Document other) {
            this.title = other.title;
            this.content = other.content;
            this.author = other.author;
            this.pages = new ArrayList<>(other.pages);
        }
        
        void addPage(String page) {
            pages.add(page);
        }
        
        public Document clone() {
            return new Document(this);
        }
        
        void setTitle(String title) {
            this.title = title;
        }
        
        public String toString() {
            return String.format("Document(title='%s', author='%s', pages=%d)",
                               title, author, pages.size());
        }
    }
    
    static class Shape implements Prototype {
        protected int x, y;
        protected String color;
        
        Shape(int x, int y, String color) {
            this.x = x;
            this.y = y;
            this.color = color;
        }
        
        protected Shape(Shape other) {
            this.x = other.x;
            this.y = other.y;
            this.color = other.color;
        }
        
        public Shape clone() {
            return new Shape(this);
        }
        
        public String toString() {
            return String.format("Shape(x=%d, y=%d, color='%s')",
                               x, y, color);
        }
    }
    
    static class Circle extends Shape {
        private int radius;
        
        Circle(int x, int y, String color, int radius) {
            super(x, y, color);
            this.radius = radius;
        }
        
        private Circle(Circle other) {
            super(other);
            this.radius = other.radius;
        }
        
        public Circle clone() {
            return new Circle(this);
        }
        
        public String toString() {
            return String.format("Circle(x=%d, y=%d, color='%s', radius=%d)",
                               x, y, color, radius);
        }
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("PROTOTYPE DESIGN PATTERN");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Document prototype
        Document original = new Document("Design Patterns", 
                                        "Content...", 
                                        "John Doe");
        original.addPage("Page 1");
        original.addPage("Page 2");
        
        System.out.println("Original: " + original);
        
        Document cloned = original.clone();
        cloned.setTitle("Advanced Patterns");
        cloned.addPage("Page 3");
        
        System.out.println("Original: " + original);
        System.out.println("Clone: " + cloned);
        System.out.println();
        
        // Shape prototype
        Circle circle = new Circle(10, 20, "red", 5);
        Circle circle2 = circle.clone();
        circle2.x = 50;
        
        System.out.println("Original: " + circle);
        System.out.println("Clone: " + circle2);
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nPattern: Creates objects by cloning");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
