import java.util.*;

/**
 * Floyd-Warshall Algorithm implementation.
 * 
 * Finds shortest paths between all pairs of vertices.
 * 
 * Time Complexity: O(V³)
 * Space Complexity: O(V²)
 */
public class Algorithm {
    
    static class Graph {
        private int numVertices;
        private double[][] distances;
        private Integer[][] nextVertex;
        private boolean directed;
        
        Graph(int numVertices, boolean directed) {
            this.numVertices = numVertices;
            this.directed = directed;
            this.distances = new double[numVertices][numVertices];
            this.nextVertex = new Integer[numVertices][numVertices];
            
            // Initialize with infinity
            for (int i = 0; i < numVertices; i++) {
                for (int j = 0; j < numVertices; j++) {
                    distances[i][j] = Double.POSITIVE_INFINITY;
                    if (i == j) {
                        distances[i][j] = 0.0;
                    }
                }
            }
        }
        
        void addEdge(int u, int v, double weight) {
            distances[u][v] = weight;
            nextVertex[u][v] = v;
            if (!directed) {
                distances[v][u] = weight;
                nextVertex[v][u] = u;
            }
        }
        
        FloydWarshallResult floydWarshall() {
            double[][] dist = new double[numVertices][numVertices];
            for (int i = 0; i < numVertices; i++) {
                dist[i] = distances[i].clone();
            }
            
            // Floyd-Warshall algorithm
            for (int k = 0; k < numVertices; k++) {
                for (int i = 0; i < numVertices; i++) {
                    for (int j = 0; j < numVertices; j++) {
                        if (dist[i][k] != Double.POSITIVE_INFINITY &&
                            dist[k][j] != Double.POSITIVE_INFINITY) {
                            if (dist[i][j] > dist[i][k] + dist[k][j]) {
                                dist[i][j] = dist[i][k] + dist[k][j];
                                nextVertex[i][j] = nextVertex[i][k];
                            }
                        }
                    }
                }
            }
            
            // Check for negative cycles
            boolean hasNegativeCycle = false;
            for (int i = 0; i < numVertices; i++) {
                if (dist[i][i] < 0) {
                    hasNegativeCycle = true;
                    break;
                }
            }
            
            return new FloydWarshallResult(dist, hasNegativeCycle);
        }
        
        List<Integer> shortestPath(int start, int end) {
            FloydWarshallResult result = floydWarshall();
            
            if (result.hasNegativeCycle) {
                System.out.println("Warning: Negative cycle detected!");
                return null;
            }
            
            if (result.distances[start][end] == Double.POSITIVE_INFINITY) {
                return null;
            }
            
            if (nextVertex[start][end] == null) {
                return start == end ? 
                    Collections.singletonList(start) : null;
            }
            
            List<Integer> path = new ArrayList<>();
            int current = start;
            
            while (current != end) {
                path.add(current);
                current = nextVertex[current][end];
            }
            path.add(end);
            
            return path;
        }
        
        Double shortestDistance(int start, int end) {
            FloydWarshallResult result = floydWarshall();
            
            if (result.hasNegativeCycle) {
                return null;
            }
            
            double dist = result.distances[start][end];
            return dist == Double.POSITIVE_INFINITY ? null : dist;
        }
    }
    
    static class FloydWarshallResult {
        double[][] distances;
        boolean hasNegativeCycle;
        
        FloydWarshallResult(double[][] distances, boolean hasNegativeCycle) {
            this.distances = distances;
            this.hasNegativeCycle = hasNegativeCycle;
        }
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("FLOYD-WARSHALL ALGORITHM DEMONSTRATION");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Example 1: All-pairs shortest paths
        System.out.println("Example 1: All-Pairs Shortest Paths");
        System.out.println("-".repeat(70));
        
        Graph g1 = new Graph(4, true);
        g1.addEdge(0, 1, 3.0);
        g1.addEdge(0, 3, 7.0);
        g1.addEdge(1, 0, 8.0);
        g1.addEdge(1, 2, 2.0);
        g1.addEdge(2, 0, 5.0);
        g1.addEdge(2, 3, 1.0);
        g1.addEdge(3, 0, 2.0);
        
        FloydWarshallResult result = g1.floydWarshall();
        
        System.out.println("Shortest distances between all pairs:");
        System.out.print("    ");
        for (int j = 0; j < 4; j++) {
            System.out.printf("  %d", j);
        }
        System.out.println();
        
        for (int i = 0; i < 4; i++) {
            System.out.printf("  %d:", i);
            for (int j = 0; j < 4; j++) {
                double dist = result.distances[i][j];
                if (dist == Double.POSITIVE_INFINITY) {
                    System.out.print("  ∞");
                } else {
                    System.out.printf(" %3.0f", dist);
                }
            }
            System.out.println();
        }
        System.out.println();
        
        // Example 2: Path reconstruction
        System.out.println("Example 2: Path Reconstruction");
        System.out.println("-".repeat(70));
        
        int[][] paths = {{0, 3}, {1, 0}, {2, 3}};
        for (int[] p : paths) {
            List<Integer> path = g1.shortestPath(p[0], p[1]);
            Double distance = g1.shortestDistance(p[0], p[1]);
            if (path != null && distance != null) {
                System.out.print("Path from " + p[0] + " to " + p[1] + ": ");
                System.out.print(path.stream()
                                    .map(String::valueOf)
                                    .reduce((a, b) -> a + " → " + b)
                                    .orElse(""));
                System.out.printf(" (distance: %.0f)%n", distance);
            }
        }
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nComplexity Summary:");
        System.out.println("  Time:  O(V³)");
        System.out.println("  Space: O(V²)");
        System.out.println("\nKey Advantages:");
        System.out.println("  - All-pairs shortest paths");
        System.out.println("  - Works with negative weights");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
