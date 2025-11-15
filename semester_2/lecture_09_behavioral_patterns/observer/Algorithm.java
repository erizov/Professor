import java.util.*;

/**
 * Observer Design Pattern.
 * 
 * One-to-many dependency between objects.
 */
public class Algorithm {
    
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
            System.out.println(name + " received: " + data);
        }
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("OBSERVER DESIGN PATTERN");
        System.out.println("=".repeat(70));
        System.out.println();
        
        NewsAgency agency = new NewsAgency();
        agency.attach(new NewsChannel("CNN"));
        agency.attach(new NewsChannel("BBC"));
        
        agency.setNews("Breaking: New technology breakthrough!");
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nPattern: One-to-many dependency");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
