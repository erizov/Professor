import java.util.*;

/**
package semester_02.lecture_08_structural_patterns.composite;
 * Composite Design Pattern.
 * 
 * Composes objects into tree structures.
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    interface FileSystemComponent {
        int getSize();
        void display(String indent);
    }
    
    static class File implements FileSystemComponent {
        private String name;
        private int size;
        
        File(String name, int size) {
            this.name = name;
            this.size = size;
        }
        
        public int getSize() {
            return size;
        }
        
        public void display(String indent) {
            logger.info(indent + "📄 " + name + " (" + size + " bytes)");
        }
    }
    
    static class Directory implements FileSystemComponent {
        private String name;
        private List<FileSystemComponent> children;
        
        Directory(String name) {
            this.name = name;
            this.children = new ArrayList<>();
        }
        
        void add(FileSystemComponent component) {
            children.add(component);
        }
        
        public int getSize() {
            return children.stream()
                          .mapToInt(FileSystemComponent::getSize)
                          .sum();
        }
        
        public void display(String indent) {
            logger.info(indent + " " + name + "/ (" + getSize() + " bytes)");
            for (FileSystemComponent child : children) {
                child.display(indent + "  ");
            }
        }
    }
    
    public static void main(String[] args) {
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        logger.info(separator);
        logger.info("COMPOSITE DESIGN PATTERN");
        logger.info(separator);
        logger.info("");
        
        Directory root = new Directory("root");
        Directory home = new Directory("home");
        home.add(new File("document.txt", 1024));
        home.add(new File("image.jpg", 2048));
        root.add(home);
        root.add(new File("readme.txt", 512));
        
        root.display("");
        logger.info("");
        
        logger.info(separator);
        logger.info("\nPattern: Composes objects into tree structures");
        logger.info(separator);
    }
}
