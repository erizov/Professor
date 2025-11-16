/**
 * Chain of Responsibility Design Pattern.
 * 
 * Passes request along chain of handlers.
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
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
        logger.info("=".repeat(70));
        logger.info("CHAIN OF RESPONSIBILITY PATTERN");
        logger.info("=".repeat(70));
        logger.info();
        
        Handler monkey = new MonkeyHandler();
        Handler dog = new DogHandler();
        monkey.setNext(dog);
        
        logger.info(monkey.handle("Banana"));
        logger.info(monkey.handle("MeatBall"));
        logger.info();
        
        logger.info("=".repeat(70));
        logger.info("\nPattern: Passes request along chain");
        logger.info("=".repeat(70));
    }
}