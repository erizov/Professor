import java.util.*;

/**
 * Iterator Design Pattern.
 * 
 * Provides way to access elements sequentially.
 */
public class Algorithm {
    
    interface Iterator<T> {
        boolean hasNext();
        T next();
    }
    
    interface Aggregate<T> {
        Iterator<T> createIterator();
    }
    
    static class BookCollection implements Aggregate<String> {
        private List<String> books;
        
        BookCollection() {
            books = new ArrayList<>();
        }
        
        void addBook(String book) {
            books.add(book);
        }
        
        public Iterator<String> createIterator() {
            return new BookIterator(books);
        }
    }
    
    static class BookIterator implements Iterator<String> {
        private List<String> books;
        private int index;
        
        BookIterator(List<String> books) {
            this.books = books;
            this.index = 0;
        }
        
        public boolean hasNext() {
            return index < books.size();
        }
        
        public String next() {
            return hasNext() ? books.get(index++) : null;
        }
    }
    
    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("ITERATOR DESIGN PATTERN");
        System.out.println("=".repeat(70));
        System.out.println();
        
        BookCollection collection = new BookCollection();
        collection.addBook("Design Patterns");
        collection.addBook("Clean Code");
        collection.addBook("Refactoring");
        
        Iterator<String> iterator = collection.createIterator();
        System.out.println("Books:");
        while (iterator.hasNext()) {
            System.out.println("  - " + iterator.next());
        }
        System.out.println();
        
        System.out.println("=".repeat(70));
        System.out.println("\nPattern: Sequential access to elements");
        System.out.println("=".repeat(70));
    }
}
