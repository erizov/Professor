import java.util.*;

/**
 * Iterator Design Pattern.
 * 
 * Provides way to access elements sequentially.
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
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
        logger.info("=".repeat(70));
        logger.info("ITERATOR DESIGN PATTERN");
        logger.info("=".repeat(70));
        logger.info();
        
        BookCollection collection = new BookCollection();
        collection.addBook("Design Patterns");
        collection.addBook("Clean Code");
        collection.addBook("Refactoring");
        
        Iterator<String> iterator = collection.createIterator();
        logger.info("Books:");
        while (iterator.hasNext()) {
            logger.info("  - " + iterator.next());
        }
        logger.info();
        
        logger.info("=".repeat(70));
        logger.info("\nPattern: Sequential access to elements");
        logger.info("=".repeat(70));
    }
}