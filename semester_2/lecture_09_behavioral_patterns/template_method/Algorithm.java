/**
 * Template Method Design Pattern.
 * 
 * Defines algorithm skeleton in method.
 */
public class Algorithm {
    
    abstract static class DataProcessor {
        void process() {
            readData();
            processData();
            saveData();
        }
        
        abstract void readData();
        abstract void processData();
        
        void saveData() {
            System.out.println("Saving processed data...");
        }
    }
    
    static class CSVProcessor extends DataProcessor {
        void readData() {
            System.out.println("Reading CSV file...");
        }
        
        void processData() {
            System.out.println("Processing CSV data...");
        }
    }
    
    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("TEMPLATE METHOD DESIGN PATTERN");
        System.out.println("=".repeat(70));
        System.out.println();
        
        DataProcessor processor = new CSVProcessor();
        processor.process();
        System.out.println();
        
        System.out.println("=".repeat(70));
        System.out.println("\nPattern: Defines algorithm skeleton");
        System.out.println("=".repeat(70));
    }
}
