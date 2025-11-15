import java.util.*;

/**
 * Bellman-Ford Algorithm implementation.
 * 
 * Finds shortest paths with negative weights and detects negative cycles.
 * 
 * Time Complexity: O(V * E)
 * Space Complexity: O(V)
 */
public class Algorithm {
    
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
                System.out.println("Warning: Negative cycle detected!");
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
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("BELLMAN-FORD ALGORITHM DEMONSTRATION");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Example 1: Basic shortest path
        System.out.println("Example 1: Basic Shortest Path");
        System.out.println("-".repeat(70));
        
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
        
        System.out.println("Shortest distances from vertex 0:");
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
        
        System.out.println("\nNegative cycle detected: " + 
                         result.hasNegativeCycle);
        System.out.println();
        
        // Example 2: Path reconstruction
        System.out.println("Example 2: Path Reconstruction");
        System.out.println("-".repeat(70));
        
        List<Integer> path = g1.shortestPath(0, 3);
        if (path != null) {
            System.out.print("Shortest path from 0 to 3: ");
            System.out.println(path.stream()
                                  .map(String::valueOf)
                                  .reduce((a, b) -> a + " → " + b)
                                  .orElse(""));
        }
        System.out.println();
        
        // Example 3: Negative cycle detection
        System.out.println("Example 3: Negative Cycle Detection");
        System.out.println("-".repeat(70));
        
        Graph g2 = new Graph(4, true);
        g2.addEdge(0, 1, 1.0);
        g2.addEdge(1, 2, -2.0);
        g2.addEdge(2, 3, -1.0);
        g2.addEdge(3, 1, 1.0);  // Creates negative cycle
        
        BellmanFordResult result2 = g2.bellmanFord(0);
        
        System.out.println("Negative cycle detected: " + 
                         result2.hasNegativeCycle);
        if (result2.hasNegativeCycle) {
            System.out.println("⚠️  Warning: Graph contains negative cycle!");
        }
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nComplexity Summary:");
        System.out.println("  Time:  O(V * E)");
        System.out.println("  Space: O(V)");
        System.out.println("\nKey Advantages:");
        System.out.println("  - Works with negative weights");
        System.out.println("  - Detects negative cycles");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}

