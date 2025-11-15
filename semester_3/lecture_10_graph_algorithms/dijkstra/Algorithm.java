import java.util.*;

/**
 * Dijkstra's Algorithm implementation.
 * 
 * Finds shortest paths in weighted graphs with non-negative weights.
 * 
 * Time Complexity: O((V + E) log V) with priority queue
 * Space Complexity: O(V)
 */
public class Algorithm {
    
    static class Edge {
        int to;
        double weight;
        
        Edge(int to, double weight) {
            this.to = to;
            this.weight = weight;
        }
    }
    
    static class Graph {
        private Map<Integer, List<Edge>> graph;
        private boolean directed;
        
        Graph(boolean directed) {
            this.graph = new HashMap<>();
            this.directed = directed;
        }
        
        void addEdge(int u, int v, double weight) {
            graph.computeIfAbsent(u, k -> new ArrayList<>())
                 .add(new Edge(v, weight));
            if (!directed) {
                graph.computeIfAbsent(v, k -> new ArrayList<>())
                     .add(new Edge(u, weight));
            }
        }
        
        Map<Integer, Double> dijkstra(int start) {
            Map<Integer, Double> distances = new HashMap<>();
            distances.put(start, 0.0);
            
            PriorityQueue<Map.Entry<Double, Integer>> pq = 
                new PriorityQueue<>(Map.Entry.comparingByKey());
            pq.offer(new AbstractMap.SimpleEntry<>(0.0, start));
            
            Set<Integer> visited = new HashSet<>();
            
            while (!pq.isEmpty()) {
                Map.Entry<Double, Integer> entry = pq.poll();
                double currentDist = entry.getKey();
                int current = entry.getValue();
                
                if (visited.contains(current)) {
                    continue;
                }
                
                visited.add(current);
                
                List<Edge> neighbors = graph.getOrDefault(current, 
                                                          new ArrayList<>());
                for (Edge edge : neighbors) {
                    if (visited.contains(edge.to)) {
                        continue;
                    }
                    
                    double newDist = currentDist + edge.weight;
                    
                    if (!distances.containsKey(edge.to) || 
                        newDist < distances.get(edge.to)) {
                        distances.put(edge.to, newDist);
                        pq.offer(new AbstractMap.SimpleEntry<>(newDist, 
                                                              edge.to));
                    }
                }
            }
            
            return distances;
        }
        
        List<Integer> shortestPath(int start, int end) {
            Map<Integer, Double> distances = new HashMap<>();
            Map<Integer, Integer> previous = new HashMap<>();
            distances.put(start, 0.0);
            previous.put(start, null);
            
            PriorityQueue<Map.Entry<Double, Integer>> pq = 
                new PriorityQueue<>(Map.Entry.comparingByKey());
            pq.offer(new AbstractMap.SimpleEntry<>(0.0, start));
            
            Set<Integer> visited = new HashSet<>();
            
            while (!pq.isEmpty()) {
                Map.Entry<Double, Integer> entry = pq.poll();
                double currentDist = entry.getKey();
                int current = entry.getValue();
                
                if (visited.contains(current)) {
                    continue;
                }
                
                visited.add(current);
                
                if (current == end) {
                    break;
                }
                
                List<Edge> neighbors = graph.getOrDefault(current, 
                                                          new ArrayList<>());
                for (Edge edge : neighbors) {
                    if (visited.contains(edge.to)) {
                        continue;
                    }
                    
                    double newDist = currentDist + edge.weight;
                    
                    if (!distances.containsKey(edge.to) || 
                        newDist < distances.get(edge.to)) {
                        distances.put(edge.to, newDist);
                        previous.put(edge.to, current);
                        pq.offer(new AbstractMap.SimpleEntry<>(newDist, 
                                                              edge.to));
                    }
                }
            }
            
            // Reconstruct path
            if (!previous.containsKey(end)) {
                return null;
            }
            
            List<Integer> path = new ArrayList<>();
            Integer current = end;
            while (current != null) {
                path.add(current);
                current = previous.get(current);
            }
            Collections.reverse(path);
            return path;
        }
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("DIJKSTRA'S ALGORITHM DEMONSTRATION");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Example 1: Basic shortest path
        System.out.println("Example 1: Basic Shortest Path Finding");
        System.out.println("-".repeat(70));
        
        Graph g1 = new Graph(false);
        g1.addEdge(0, 1, 4.0);
        g1.addEdge(1, 2, 2.0);
        g1.addEdge(2, 3, 1.0);
        g1.addEdge(0, 2, 5.0);
        
        Map<Integer, Double> distances = g1.dijkstra(0);
        
        System.out.println("Shortest distances from vertex 0:");
        distances.entrySet().stream()
                 .sorted(Map.Entry.comparingByKey())
                 .forEach(entry -> 
                     System.out.printf("  To vertex %d: %.1f%n", 
                                     entry.getKey(), entry.getValue()));
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
            System.out.printf("Total distance: %.1f%n", 
                            distances.get(3));
        }
        System.out.println();
        
        // Example 3: Complex graph
        System.out.println("Example 3: Complex Weighted Graph");
        System.out.println("-".repeat(70));
        
        Graph g2 = new Graph(true);
        g2.addEdge(0, 1, 1.0);
        g2.addEdge(0, 2, 4.0);
        g2.addEdge(1, 2, 2.0);
        g2.addEdge(1, 3, 5.0);
        g2.addEdge(2, 3, 1.0);
        g2.addEdge(3, 4, 3.0);
        g2.addEdge(2, 4, 6.0);
        
        Map<Integer, Double> distances2 = g2.dijkstra(0);
        
        System.out.println("Shortest distances from vertex 0:");
        distances2.entrySet().stream()
                  .sorted(Map.Entry.comparingByKey())
                  .forEach(entry -> 
                      System.out.printf("  To vertex %d: %.1f%n", 
                                      entry.getKey(), entry.getValue()));
        
        System.out.println("\nShortest paths:");
        for (int target = 1; target <= 4; target++) {
            List<Integer> p = g2.shortestPath(0, target);
            if (p != null) {
                System.out.print("  0 → " + target + ": ");
                System.out.print(p.stream()
                                  .map(String::valueOf)
                                  .reduce((a, b) -> a + " → " + b)
                                  .orElse(""));
                System.out.printf(" (distance: %.1f)%n", 
                                distances2.get(target));
            }
        }
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nComplexity Summary:");
        System.out.println("  Time:  O((V + E) log V)");
        System.out.println("  Space: O(V)");
        System.out.println("\nKey Advantages:");
        System.out.println("  - Finds shortest path in weighted graphs");
        System.out.println("  - Efficient with priority queue");
        System.out.println("\nLimitations:");
        System.out.println("  - Does NOT work with negative weights");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}

