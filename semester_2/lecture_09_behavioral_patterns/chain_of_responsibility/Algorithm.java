/**
 * Chain of Responsibility Design Pattern.
 * 
 * Passes request along chain of handlers.
 */
public class Algorithm {
    
    abstract static class Handler {
        protected Handler nextHandler;
        
        Handler setNext(Handler handler) {
            nextHandler = handler;
            return handler;
        }
        
        abstract String handle(String request);
    }
    
    static class MonkeyHandler extends Handler {
        public String handle(String request) {
            if ("Banana".equals(request)) {
                return "Monkey: I'll eat the " + request;
            } else if (nextHandler != null) {
                return nextHandler.handle(request);
            }
            return null;
        }
    }
    
    static class DogHandler extends Handler {
        public String handle(String request) {
            if ("MeatBall".equals(request)) {
                return "Dog: I'll eat the " + request;
            } else if (nextHandler != null) {
                return nextHandler.handle(request);
            }
            return null;
        }
    }
    
    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("CHAIN OF RESPONSIBILITY PATTERN");
        System.out.println("=".repeat(70));
        System.out.println();
        
        Handler monkey = new MonkeyHandler();
        Handler dog = new DogHandler();
        monkey.setNext(dog);
        
        System.out.println(monkey.handle("Banana"));
        System.out.println(monkey.handle("MeatBall"));
        System.out.println();
        
        System.out.println("=".repeat(70));
        System.out.println("\nPattern: Passes request along chain");
        System.out.println("=".repeat(70));
    }
}
