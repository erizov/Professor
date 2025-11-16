/**
 * Proxy Design Pattern.
 * 
 * Provides surrogate for another object.
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
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
            logger.info("Loading " + filename + " from disk...");
        }
        
        public void display() {
            logger.info("Displaying " + filename);
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
        logger.info("=".repeat(70));
        logger.info("PROXY DESIGN PATTERN");
        logger.info("=".repeat(70));
        logger.info();
        
        Image image = new ProxyImage("photo.jpg");
        logger.info("Image proxy created (not loaded yet)");
        image.display();
        logger.info();
        
        logger.info("=".repeat(70));
        logger.info("\nPattern: Provides surrogate for object");
        logger.info("=".repeat(70));
    }
}