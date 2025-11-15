import java.util.*;

/**
 * Composite Design Pattern.
 * 
 * Composes objects into tree structures.
 */
public class Algorithm {
    
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
            System.out.println(indent + "📄 " + name + " (" + size + " bytes)");
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
            System.out.println(indent + "📁 " + name + "/ (" + getSize() + " bytes)");
            for (FileSystemComponent child : children) {
                child.display(indent + "  ");
            }
        }
    }
    
    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("COMPOSITE DESIGN PATTERN");
        System.out.println("=".repeat(70));
        System.out.println();
        
        Directory root = new Directory("root");
        Directory home = new Directory("home");
        home.add(new File("document.txt", 1024));
        home.add(new File("image.jpg", 2048));
        root.add(home);
        root.add(new File("readme.txt", 512));
        
        root.display("");
        System.out.println();
        
        System.out.println("=".repeat(70));
        System.out.println("\nPattern: Composes objects into tree structures");
        System.out.println("=".repeat(70));
    }
}
