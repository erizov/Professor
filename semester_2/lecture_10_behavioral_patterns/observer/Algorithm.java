import java.util.*;

/**
 * Observer Design Pattern.
 * 
 * One-to-many dependency: when subject changes, observers are notified.
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    // Observer interface
    interface Observer {
        void update(Object data);
    }
    
    // Subject interface
    interface Subject {
        void attach(Observer observer);
        void detach(Observer observer);
        void notifyObservers();
    }
    
    // Concrete Subject: News Agency
    static class NewsAgency implements Subject {
        private List<Observer> observers = new ArrayList<>();
        private String news = "";
        
        public void attach(Observer observer) {
            if (!observers.contains(observer)) {
                observers.add(observer);
                logger.info("Observer attached: " + observer);
            }
        }
        
        public void detach(Observer observer) {
            observers.remove(observer);
            logger.info("Observer detached: " + observer);
        }
        
        public void notifyObservers() {
            for (Observer observer : observers) {
                observer.update(news);
            }
        }
        
        public void setNews(String news) {
            this.news = news;
            logger.info("\nNews Agency: Publishing news - '" + news + "'");
            notifyObservers();
        }
    }
    
    // Concrete Observer: News Channel
    static class NewsChannel implements Observer {
        private String name;
        private String news = "";
        
        NewsChannel(String name) {
            this.name = name;
        }
        
        public void update(Object data) {
            if (data instanceof String) {
                this.news = (String) data;
                logger.info("  " + name + ": Received news - '" + news + "'");
            }
        }
        
        public String toString() {
            return "NewsChannel(" + name + ")";
        }
    }
    
    // Concrete Observer: Email Subscriber
    static class EmailSubscriber implements Observer {
        private String email;
        private String news = "";
        
        EmailSubscriber(String email) {
            this.email = email;
        }
        
        public void update(Object data) {
            if (data instanceof String) {
                this.news = (String) data;
                logger.info("  Email to " + email + ": '" + news + "'");
            }
        }
        
        public String toString() {
            return "EmailSubscriber(" + email + ")";
        }
    }
    
    // Weather Station Example
    static class WeatherData implements Subject {
        private List<Observer> observers = new ArrayList<>();
        private double temperature;
        private double humidity;
        private double pressure;
        
        public void attach(Observer observer) {
            if (!observers.contains(observer)) {
                observers.add(observer);
            }
        }
        
        public void detach(Observer observer) {
            observers.remove(observer);
        }
        
        public void notifyObservers() {
            for (Observer observer : observers) {
                observer.update(this);
            }
        }
        
        public void setMeasurements(double temperature, 
                                   double humidity, 
                                   double pressure) {
            this.temperature = temperature;
            this.humidity = humidity;
            this.pressure = pressure;
            notifyObservers();
        }
        
        public double getTemperature() { return temperature; }
        public double getHumidity() { return humidity; }
        public double getPressure() { return pressure; }
    }
    
    static class CurrentConditionsDisplay implements Observer {
        private String name;
        private double temperature;
        private double humidity;
        
        CurrentConditionsDisplay(String name) {
            this.name = name;
        }
        
        public void update(Object data) {
            if (data instanceof WeatherData) {
                WeatherData weather = (WeatherData) data;
                this.temperature = weather.getTemperature();
                this.humidity = weather.getHumidity();
                logger.info("  " + name + " Display:");
                System.out.printf("    Temperature: %.1f°F%n", temperature);
                System.out.printf("    Humidity: %.1f%%%n", humidity);
            }
        }
    }
    
    // Stock Market Example
    static class Stock implements Subject {
        private List<Observer> observers = new ArrayList<>();
        private String symbol;
        private double price;
        
        Stock(String symbol, double price) {
            this.symbol = symbol;
            this.price = price;
        }
        
        public void attach(Observer observer) {
            if (!observers.contains(observer)) {
                observers.add(observer);
            }
        }
        
        public void detach(Observer observer) {
            observers.remove(observer);
        }
        
        public void notifyObservers() {
            for (Observer observer : observers) {
                observer.update(this);
            }
        }
        
        public void setPrice(double price) {
            double oldPrice = this.price;
            this.price = price;
            double change = price - oldPrice;
            double changePct = oldPrice > 0 ? (change / oldPrice * 100) : 0;
            
            System.out.printf("%n%s: $%.2f → $%.2f (%.2f, %.2f%%)%n",
                            symbol, oldPrice, price, change, changePct);
            notifyObservers();
        }
        
        public double getPrice() { return price; }
        public String getSymbol() { return symbol; }
    }
    
    static class StockTrader implements Observer {
        private String name;
        private Double buyThreshold;
        private Double sellThreshold;
        private double lastPrice = 0.0;
        
        StockTrader(String name) {
            this.name = name;
        }
        
        StockTrader(String name, Double buyThreshold, Double sellThreshold) {
            this.name = name;
            this.buyThreshold = buyThreshold;
            this.sellThreshold = sellThreshold;
        }
        
        public void update(Object data) {
            if (data instanceof Stock) {
                Stock stock = (Stock) data;
                double price = stock.getPrice();
                System.out.printf("  %s: %s = $%.2f", name, stock.getSymbol(), price);
                
                if (buyThreshold != null && price <= buyThreshold) {
                    logger.info(" → BUY SIGNAL!");
                } else if (sellThreshold != null && price >= sellThreshold) {
                    logger.info(" → SELL SIGNAL!");
                } else {
                    logger.info();
                }
                
                lastPrice = price;
            }
        }
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        logger.info("=".repeat(70));
        logger.info("OBSERVER DESIGN PATTERN DEMONSTRATION");
        logger.info("=".repeat(70));
        logger.info();
        
        // Example 1: News Agency
        logger.info("Example 1: News Agency");
        logger.info("-".repeat(70));
        
        NewsAgency agency = new NewsAgency();
        NewsChannel channel1 = new NewsChannel("CNN");
        NewsChannel channel2 = new NewsChannel("BBC");
        EmailSubscriber email1 = new EmailSubscriber("user@example.com");
        
        agency.attach(channel1);
        agency.attach(channel2);
        agency.attach(email1);
        
        agency.setNews("Breaking: New algorithm discovered!");
        logger.info();
        
        agency.detach(channel2);
        agency.setNews("Update: Algorithm implementation complete!");
        logger.info();
        
        // Example 2: Weather Station
        logger.info("Example 2: Weather Station");
        logger.info("-".repeat(70));
        
        WeatherData weather = new WeatherData();
        CurrentConditionsDisplay display1 = 
            new CurrentConditionsDisplay("Mobile App");
        CurrentConditionsDisplay display2 = 
            new CurrentConditionsDisplay("Website");
        
        weather.attach(display1);
        weather.attach(display2);
        
        weather.setMeasurements(75.0, 65.0, 30.4);
        logger.info();
        
        weather.setMeasurements(80.0, 70.0, 30.2);
        logger.info();
        
        // Example 3: Stock Market
        logger.info("Example 3: Stock Market Trading");
        logger.info("-".repeat(70));
        
        Stock apple = new Stock("AAPL", 150.00);
        StockTrader trader1 = new StockTrader("Alice", 145.0, 160.0);
        StockTrader trader2 = new StockTrader("Bob", 140.0, null);
        
        apple.attach(trader1);
        apple.attach(trader2);
        
        apple.setPrice(148.50);
        apple.setPrice(142.00);
        apple.setPrice(155.00);
        apple.setPrice(162.00);
        logger.info();
        
        long endTime = System.nanoTime();
        
        logger.info("=".repeat(70));
        logger.info("\nPattern Summary:");
        logger.info("\nKey Advantages:");
        logger.info("  - Loose coupling");
        logger.info("  - Dynamic subscription");
        logger.info("  - Broadcast communication");
        logger.info("\nWhen to Use:");
        logger.info("  - Event-driven systems");
        logger.info("  - MVC architecture");
        logger.info("  - Publish-Subscribe");
        logger.info("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
