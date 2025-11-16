import java.util.*;

/**
 * Load Balancing Pattern.
 * 
 * Distributes requests across servers.
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    static class Server {
        String id;
        int connections;
        
        Server(String id) {
            this.id = id;
            this.connections = 0;
        }
    }
    
    static class RoundRobinLoadBalancer {
        private List<Server> servers;
        private int currentIndex;
        
        RoundRobinLoadBalancer(List<Server> servers) {
            this.servers = servers;
            this.currentIndex = 0;
        }
        
        Server selectServer() {
            if (servers.isEmpty()) return null;
            Server server = servers.get(currentIndex % servers.size());
            currentIndex++;
            return server;
        }
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        logger.info("=".repeat(70));
        logger.info("LOAD BALANCING PATTERN");
        logger.info("=".repeat(70));
        logger.info();
        
        List<Server> servers = Arrays.asList(
            new Server("server1"),
            new Server("server2"),
            new Server("server3")
        );
        
        RoundRobinLoadBalancer lb = new RoundRobinLoadBalancer(servers);
        
        for (int i = 0; i < 5; i++) {
            Server server = lb.selectServer();
            server.connections++;
            logger.info("Request " + (i+1) + " -> " + server.id);
        }
        logger.info();
        
        long endTime = System.nanoTime();
        
        logger.info("=".repeat(70));
        logger.info("\nPattern: Distributes requests");
        logger.info("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}