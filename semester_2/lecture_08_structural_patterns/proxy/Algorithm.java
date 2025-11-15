/**
 * Proxy Design Pattern.
 * 
 * Provides surrogate for another object.
 */
public class Algorithm {
    
    interface Image {
        void display();
    }
    
    static class RealImage implements Image {
        private String filename;
        
        RealImage(String filename) {
            this.filename = filename;
            loadFromDisk();
        }
        
        private void loadFromDisk() {
            System.out.println("Loading " + filename + " from disk...");
        }
        
        public void display() {
            System.out.println("Displaying " + filename);
        }
    }
    
    static class ProxyImage implements Image {
        private String filename;
        private RealImage realImage;
        
        ProxyImage(String filename) {
            this.filename = filename;
        }
        
        public void display() {
            if (realImage == null) {
                realImage = new RealImage(filename);
            }
            realImage.display();
        }
    }
    
    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("PROXY DESIGN PATTERN");
        System.out.println("=".repeat(70));
        System.out.println();
        
        Image image = new ProxyImage("photo.jpg");
        System.out.println("Image proxy created (not loaded yet)");
        image.display();
        System.out.println();
        
        System.out.println("=".repeat(70));
        System.out.println("\nPattern: Provides surrogate for object");
        System.out.println("=".repeat(70));
    }
}
