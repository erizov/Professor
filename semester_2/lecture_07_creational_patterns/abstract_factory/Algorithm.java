/**
 * Abstract Factory Design Pattern.
 * 
 * Provides interface for creating families of related objects.
 */
public class Algorithm {
    
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
                System.out.println(button.render());
                System.out.println(dialog.render());
            }
        }
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("ABSTRACT FACTORY DESIGN PATTERN");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Windows application
        GUIFactory windowsFactory = new WindowsFactory();
        Application windowsApp = new Application(windowsFactory);
        windowsApp.createUI();
        System.out.println("Windows UI:");
        windowsApp.renderUI();
        System.out.println();
        
        // Mac application
        GUIFactory macFactory = new MacFactory();
        Application macApp = new Application(macFactory);
        macApp.createUI();
        System.out.println("Mac UI:");
        macApp.renderUI();
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nPattern: Creates families of related objects");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
