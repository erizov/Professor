/**
 * Abstract Factory Design Pattern.
 * 
 * Provides interface for creating families of related objects.
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    // Abstract Products
    interface Button {
        String render();
    }
    
    interface Dialog {
        String render();
    }
    
    // Concrete Products - Windows
    static class WindowsButton implements Button {
        public String render() {
            return "Windows Button rendered";
        }
    }
    
    static class WindowsDialog implements Dialog {
        public String render() {
            return "Windows Dialog rendered";
        }
    }
    
    // Concrete Products - Mac
    static class MacButton implements Button {
        public String render() {
            return "Mac Button rendered";
        }
    }
    
    static class MacDialog implements Dialog {
        public String render() {
            return "Mac Dialog rendered";
        }
    }
    
    // Abstract Factory
    interface GUIFactory {
        Button createButton();
        Dialog createDialog();
    }
    
    // Concrete Factories
    static class WindowsFactory implements GUIFactory {
        public Button createButton() {
            return new WindowsButton();
        }
        
        public Dialog createDialog() {
            return new WindowsDialog();
        }
    }
    
    static class MacFactory implements GUIFactory {
        public Button createButton() {
            return new MacButton();
        }
        
        public Dialog createDialog() {
            return new MacDialog();
        }
    }
    
    // Client
    static class Application {
        private GUIFactory factory;
        private Button button;
        private Dialog dialog;
        
        Application(GUIFactory factory) {
            this.factory = factory;
        }
        
        void createUI() {
            button = factory.createButton();
            dialog = factory.createDialog();
        }
        
        void renderUI() {
            if (button != null && dialog != null) {
                logger.info(button.render());
                logger.info(dialog.render());
            }
        }
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        logger.info("=".repeat(70));
        logger.info("ABSTRACT FACTORY DESIGN PATTERN");
        logger.info("=".repeat(70));
        logger.info();
        
        // Windows application
        GUIFactory windowsFactory = new WindowsFactory();
        Application windowsApp = new Application(windowsFactory);
        windowsApp.createUI();
        logger.info("Windows UI:");
        windowsApp.renderUI();
        logger.info();
        
        // Mac application
        GUIFactory macFactory = new MacFactory();
        Application macApp = new Application(macFactory);
        macApp.createUI();
        logger.info("Mac UI:");
        macApp.renderUI();
        logger.info();
        
        long endTime = System.nanoTime();
        
        logger.info("=".repeat(70));
        logger.info("\nPattern: Creates families of related objects");
        logger.info("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}