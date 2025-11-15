/**
 * Decorator Design Pattern.
 * 
 * Adds behavior to objects dynamically.
 */
public class Algorithm {
    
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
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("DECORATOR DESIGN PATTERN DEMONSTRATION");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Example 1: Coffee
        System.out.println("Example 1: Coffee Ordering System");
        System.out.println("-".repeat(70));
        
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
        System.out.println();
        
        // Example 2: Text formatting
        System.out.println("Example 2: Text Formatting");
        System.out.println("-".repeat(70));
        
        String text = "Hello, World!";
        
        TextProcessor plain = new PlainText();
        System.out.println("Plain: " + plain.process(text));
        
        TextProcessor bold = new BoldDecorator(new PlainText());
        System.out.println("Bold: " + bold.process(text));
        
        TextProcessor boldItalic = new ItalicDecorator(
            new BoldDecorator(new PlainText())
        );
        System.out.println("Bold + Italic: " + boldItalic.process(text));
        
        TextProcessor formatted = new UnderlineDecorator(
            new BoldDecorator(new PlainText())
        );
        System.out.println("Underline + Bold: " + formatted.process(text));
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nPattern Summary:");
        System.out.println("\nKey Advantages:");
        System.out.println("  - Add behavior dynamically");
        System.out.println("  - Compose behaviors");
        System.out.println("  - Flexible alternative to inheritance");
        System.out.println("\nWhen to Use:");
        System.out.println("  - Add responsibilities dynamically");
        System.out.println("  - Avoid feature explosion");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
