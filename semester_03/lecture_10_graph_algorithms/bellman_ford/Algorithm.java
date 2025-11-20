import java.util.*;

/**
package semester_03.lecture_10_graph_algorithms.bellman_ford;
 * Bellman-Ford Algorithm implementation.
 * 
 * Finds shortest paths with negative weights and detects negative cycles.
 * 
 * Time Complexity: O(V * E)
 * Space Complexity: O(V)
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    static class Edge {
        int u, v;
        double weight;
        
        Edge(int u, int v, double weight) {
            this.u = u;
            this.v = v;
            this.weight = weight;
        }
    }
    
    static class Graph {
        private int numVertices;
        private List<Edge> edges;
        private boolean directed;
        
        Graph(int numVertices, boolean directed) {
            this.numVertices = numVertices;
            this.edges = new ArrayList<>();
            this.directed = directed;
        }
        
        void addEdge(int u, int v, double weight) {
            edges.add(new Edge(u, v, weight));
            if (!directed) {
                edges.add(new Edge(v, u, weight));
            }
        }
        
        BellmanFordResult bellmanFord(int start) {
            Map<Integer, Double> distances = new HashMap<>();
            Map<Integer, Integer> previous = new HashMap<>();
            
            // Initialize distances
            distances.put(start, 0.0);
            previous.put(start, null);
            
            for (int i = 0; i < numVertices; i++) {
                if (i != start) {
                    distances.put(i, Double.POSITIVE_INFINITY);
                }
            }
            
            // Relax edges (V-1) times
            for (int i = 0; i < numVertices - 1; i++) {
                for (Edge edge : edges) {
                    double uDist = distances.get(edge.u);
                    if (uDist != Double.POSITIVE_INFINITY) {
                        double newDist = uDist + edge.weight;
                        double vDist = distances.get(edge.v);
                        
                        if (newDist < vDist) {
                            distances.put(edge.v, newDist);
                            previous.put(edge.v, edge.u);
                        }
                    }
                }
            }
            
            // Check for negative cycles
            boolean hasNegativeCycle = false;
            for (Edge edge : edges) {
                double uDist = distances.get(edge.u);
                if (uDist != Double.POSITIVE_INFINITY) {
                    double newDist = uDist + edge.weight;
                    double vDist = distances.get(edge.v);
                    
                    if (newDist < vDist) {
                        hasNegativeCycle = true;
                        break;
                    }
                }
            }
            
            return new BellmanFordResult(distances, previous, hasNegativeCycle);
        }
        
        List<Integer> shortestPath(int start, int end) {
            BellmanFordResult result = bellmanFord(start);
            
            if (result.hasNegativeCycle) {
                logger.info("Warning: Negative cycle detected!");
                return null;
            }
            
            Double dist = result.distances.get(end);
            if (dist == null || dist == Double.POSITIVE_INFINITY) {
                return null;
            }
            
            // Reconstruct path
            List<Integer> path = new ArrayList<>();
            Integer current = end;
            
            while (current != null) {
                path.add(current);
                current = result.previous.get(current);
            }
            
            Collections.reverse(path);
            return path;
        }
    }
    
    static class BellmanFordResult {
        Map<Integer, Double> distances;
        Map<Integer, Integer> previous;
        boolean hasNegativeCycle;
        
        BellmanFordResult(Map<Integer, Double> distances,
                         Map<Integer, Integer> previous,
                         boolean hasNegativeCycle) {
            this.distances = distances;
            this.previous = previous;
            this.hasNegativeCycle = hasNegativeCycle;
        }
    }
    
    public static void main(String[] args) {
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        long startTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("BELLMAN-FORD ALGORITHM DEMONSTRATION");
        logger.info(separator);
        logger.info("");
        
        // Example 1: Basic shortest path
        logger.info("Example 1: Basic Shortest Path");
        logger.info(dash);
        
        Graph g1 = new Graph(5, true);
        g1.addEdge(0, 1, -1.0);
        g1.addEdge(0, 2, 4.0);
        g1.addEdge(1, 2, 3.0);
        g1.addEdge(1, 3, 2.0);
        g1.addEdge(1, 4, 2.0);
        g1.addEdge(3, 2, 5.0);
        g1.addEdge(3, 1, 1.0);
        g1.addEdge(4, 3, -3.0);
        
        BellmanFordResult result = g1.bellmanFord(0);
        
        logger.info("Shortest distances from vertex 0:");
        result.distances.entrySet().stream()
                       .sorted(Map.Entry.comparingByKey())
                       .forEach(entry -> {
                           double dist = entry.getValue();
                           if (dist == Double.POSITIVE_INFINITY) {
                               System.out.printf("  To vertex %d: ∞%n", 
                                               entry.getKey());
                           } else {
                               System.out.printf("  To vertex %d: %.1f%n",
                                               entry.getKey(), dist);
                           }
                       });
        
        logger.info("\nNegative cycle detected: " + 
                         result.hasNegativeCycle);
        logger.info("");
        
        // Example 2: Path reconstruction
        logger.info("Example 2: Path Reconstruction");
        logger.info(dash);
        
        List<Integer> path = g1.shortestPath(0, 3);
        if (path != null) {
            System.out.print("Shortest path from 0 to 3: ");
            logger.info(path.stream()
                                  .map(String::valueOf)
                                  .reduce((a, b) -> a + " → " + b)
                                  .orElse(""));
        }
        logger.info("");
        
        // Example 3: Negative cycle detection
        logger.info("Example 3: Negative Cycle Detection");
        logger.info(dash);
        
        Graph g2 = new Graph(4, true);
        g2.addEdge(0, 1, 1.0);
        g2.addEdge(1, 2, -2.0);
        g2.addEdge(2, 3, -1.0);
        g2.addEdge(3, 1, 1.0);  // Creates negative cycle
        
        BellmanFordResult result2 = g2.bellmanFord(0);
        
        logger.info("Negative cycle detected: " + 
                         result2.hasNegativeCycle);
        if (result2.hasNegativeCycle) {
            logger.info("Warning:  Warning: Graph contains negative cycle!");
        }
        logger.info("");
        
        long endTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("\nComplexity Summary:");
        logger.info("  Time:  O(V * E)");
        logger.info("  Space: O(V)");
        logger.info("\nKey Advantages:");
        logger.info("  - Works with negative weights");
        logger.info("  - Detects negative cycles");
        logger.info(separator);
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
