import java.util.*;

/**
 * Observer Design Pattern.
 * 
 * One-to-many dependency between objects.
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    interface Observer {
        void update(String data);
    }
    
    interface Subject {
        void attach(Observer observer);
        void detach(Observer observer);
        void notifyObservers();
    }
    
    static class NewsAgency implements Subject {
        private List<Observer> observers;
        private String news;
        
        NewsAgency() {
            observers = new ArrayList<>();
        }
        
        public void attach(Observer observer) {
            observers.add(observer);
        }
        
        public void detach(Observer observer) {
            observers.remove(observer);
        }
        
        public void notifyObservers() {
            for (Observer observer : observers) {
                observer.update(news);
            }
        }
        
        void setNews(String news) {
            this.news = news;
            notifyObservers();
        }
    }
    
    static class NewsChannel implements Observer {
        private String name;
        
        NewsChannel(String name) {
            this.name = name;
        }
        
        public void update(String data) {
            logger.info(name + " received: " + data);
        }
    }
    
    public static void main(String[] args) {
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        long startTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("OBSERVER DESIGN PATTERN");
        logger.info(separator);
        logger.info("");
        
        NewsAgency agency = new NewsAgency();
        agency.attach(new NewsChannel("CNN"));
        agency.attach(new NewsChannel("BBC"));
        
        agency.setNews("Breaking: New technology breakthrough!");
        logger.info("");
        
        long endTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("\nPattern: One-to-many dependency");
        logger.info(separator);
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
