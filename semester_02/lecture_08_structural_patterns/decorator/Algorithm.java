/**
 * Decorator Design Pattern.
 * 
 * Adds behavior to objects dynamically.
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    // Component interface
    interface Coffee {
        String getDescription();
        double getCost();
    }
    
    // Concrete component
    static class SimpleCoffee implements Coffee {
        public String getDescription() {
            return "Simple Coffee";
        }
        
        public double getCost() {
            return 2.0;
        }
    }
    
    // Base decorator
    static abstract class CoffeeDecorator implements Coffee {
        protected Coffee coffee;
        
        CoffeeDecorator(Coffee coffee) {
            this.coffee = coffee;
        }
        
        public String getDescription() {
            return coffee.getDescription();
        }
        
        public double getCost() {
            return coffee.getCost();
        }
    }
    
    // Concrete decorators
    static class MilkDecorator extends CoffeeDecorator {
        MilkDecorator(Coffee coffee) {
            super(coffee);
        }
        
        public String getDescription() {
            return coffee.getDescription() + ", Milk";
        }
        
        public double getCost() {
            return coffee.getCost() + 0.5;
        }
    }
    
    static class SugarDecorator extends CoffeeDecorator {
        SugarDecorator(Coffee coffee) {
            super(coffee);
        }
        
        public String getDescription() {
            return coffee.getDescription() + ", Sugar";
        }
        
        public double getCost() {
            return coffee.getCost() + 0.2;
        }
    }
    
    static class WhippedCreamDecorator extends CoffeeDecorator {
        WhippedCreamDecorator(Coffee coffee) {
            super(coffee);
        }
        
        public String getDescription() {
            return coffee.getDescription() + ", Whipped Cream";
        }
        
        public double getCost() {
            return coffee.getCost() + 0.7;
        }
    }
    
    static class CaramelDecorator extends CoffeeDecorator {
        CaramelDecorator(Coffee coffee) {
            super(coffee);
        }
        
        public String getDescription() {
            return coffee.getDescription() + ", Caramel";
        }
        
        public double getCost() {
            return coffee.getCost() + 0.6;
        }
    }
    
    // Text processing example
    interface TextProcessor {
        String process(String text);
    }
    
    static class PlainText implements TextProcessor {
        public String process(String text) {
            return text;
        }
    }
    
    static abstract class TextDecorator implements TextProcessor {
        protected TextProcessor processor;
        
        TextDecorator(TextProcessor processor) {
            this.processor = processor;
        }
        
        public String process(String text) {
            return processor.process(text);
        }
    }
    
    static class BoldDecorator extends TextDecorator {
        BoldDecorator(TextProcessor processor) {
            super(processor);
        }
        
        public String process(String text) {
            return "<b>" + processor.process(text) + "</b>";
        }
    }
    
    static class ItalicDecorator extends TextDecorator {
        ItalicDecorator(TextProcessor processor) {
            super(processor);
        }
        
        public String process(String text) {
            return "<i>" + processor.process(text) + "</i>";
        }
    }
    
    static class UnderlineDecorator extends TextDecorator {
        UnderlineDecorator(TextProcessor processor) {
            super(processor);
        }
        
        public String process(String text) {
            return "<u>" + processor.process(text) + "</u>";
        }
    }
    
    public static void main(String[] args) {
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        long startTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("DECORATOR DESIGN PATTERN DEMONSTRATION");
        logger.info(separator);
        logger.info("");
        
        // Example 1: Coffee
        logger.info("Example 1: Coffee Ordering System");
        logger.info(dash);
        
        Coffee coffee = new SimpleCoffee();
        System.out.printf("%s: $%.2f%n", 
                        coffee.getDescription(), coffee.getCost());
        
        Coffee coffeeWithMilk = new MilkDecorator(new SimpleCoffee());
        System.out.printf("%s: $%.2f%n",
                        coffeeWithMilk.getDescription(), 
                        coffeeWithMilk.getCost());
        
        Coffee fancyCoffee = new WhippedCreamDecorator(
            new CaramelDecorator(
                new SugarDecorator(
                    new MilkDecorator(new SimpleCoffee())
                )
            )
        );
        System.out.printf("%s: $%.2f%n",
                        fancyCoffee.getDescription(),
                        fancyCoffee.getCost());
        logger.info("");
        
        // Example 2: Text formatting
        logger.info("Example 2: Text Formatting");
        logger.info(dash);
        
        String text = "Hello, World!";
        
        TextProcessor plain = new PlainText();
        logger.info("Plain: " + plain.process(text));
        
        TextProcessor bold = new BoldDecorator(new PlainText());
        logger.info("Bold: " + bold.process(text));
        
        TextProcessor boldItalic = new ItalicDecorator(
            new BoldDecorator(new PlainText())
        );
        logger.info("Bold + Italic: " + boldItalic.process(text));
        
        TextProcessor formatted = new UnderlineDecorator(
            new BoldDecorator(new PlainText())
        );
        logger.info("Underline + Bold: " + formatted.process(text));
        logger.info("");
        
        long endTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("\nPattern Summary:");
        logger.info("\nKey Advantages:");
        logger.info("  - Add behavior dynamically");
        logger.info("  - Compose behaviors");
        logger.info("  - Flexible alternative to inheritance");
        logger.info("\nWhen to Use:");
        logger.info("  - Add responsibilities dynamically");
        logger.info("  - Avoid feature explosion");
        logger.info(separator);
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
