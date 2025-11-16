/**
 * Breadth-First Search (BFS) implementation.
 * 
 * Graph traversal algorithm that explores all neighbors at current depth
 * before moving to next depth level.
 */
import java.util.*;

import java.util.logging.Logger;
class Graph {
    private Map<Integer, List<Integer>> graph;
    private boolean directed;
    
    public Graph(boolean directed) {
        this.graph = new HashMap<>();
        this.directed = directed;
    }
    
    public void addEdge(int u, int v) {
        graph.putIfAbsent(u, new ArrayList<>());
        graph.putIfAbsent(v, new ArrayList<>());
        graph.get(u).add(v);
        if (!directed) {
            graph.get(v).add(u);
        }
    }
    
    public List<Integer> bfs(int start) {
        List<Integer> result = new ArrayList<>();
        Set<Integer> visited = new HashSet<>();
        Queue<Integer> queue = new LinkedList<>();
        
        queue.offer(start);
        visited.add(start);
        
        while (!queue.isEmpty()) {
            int node = queue.poll();
            result.add(node);
            
            List<Integer> neighbors = graph.getOrDefault(node, new ArrayList<>());
            for (int neighbor : neighbors) {
                if (!visited.contains(neighbor)) {
                    visited.add(neighbor);
                    queue.offer(neighbor);
                }
            }
        }
        
        return result;
    }
    
    public List<Integer> shortestPath(int start, int end) {
        if (start == end) {
            return Arrays.asList(start);
        }
        
        Map<Integer, Integer> parent = new HashMap<>();
        Queue<Integer> queue = new LinkedList<>();
        Set<Integer> visited = new HashSet<>();
        
        queue.offer(start);
        visited.add(start);
        parent.put(start, -1);
        
        while (!queue.isEmpty()) {
            int node = queue.poll();
            
            List<Integer> neighbors = graph.getOrDefault(node, new ArrayList<>());
            for (int neighbor : neighbors) {
                if (neighbor == end) {
                    List<Integer> path = new ArrayList<>();
                    path.add(end);
                    int current = node;
                    while (current != -1) {
                        path.add(0, current);
                        current = parent.get(current);
                    }
                    return path;
                }
                
                if (!visited.contains(neighbor)) {
                    visited.add(neighbor);
                    parent.put(neighbor, node);
                    queue.offer(neighbor);
                }
            }
        }
        
        return null; // No path found
    }
}

public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public static void main(String[] args) {
        logger.info("=".repeat(70));
        logger.info("BREADTH-FIRST SEARCH (BFS) DEMONSTRATION");
        logger.info("=".repeat(70));
        logger.info();
        
        // Example 1: Basic BFS
        logger.info("Example 1: Basic BFS Traversal");
        logger.info("-".repeat(70));
        Graph g1 = new Graph(false);
        g1.addEdge(0, 1);
        g1.addEdge(0, 2);
        g1.addEdge(1, 3);
        g1.addEdge(2, 4);
        g1.addEdge(3, 4);
        
        List<Integer> bfsResult = g1.bfs(0);
        logger.info("BFS from node 0: " + bfsResult);
        logger.info();
        
        // Example 2: Shortest Path
        logger.info("Example 2: Shortest Path");
        logger.info("-".repeat(70));
        List<Integer> path = g1.shortestPath(0, 4);
        logger.info("Shortest path from 0 to 4: " + path);
        logger.info();
        
        logger.info("=".repeat(70));
        logger.info("\nAlgorithm Summary:");
        logger.info("\nTime Complexity: O(V + E)");
        logger.info("Space Complexity: O(V)");
        logger.info("\nKey Advantages:");
        logger.info("  - Finds shortest path in unweighted graphs");
        logger.info("  - Level-order traversal");
        logger.info("  - Guaranteed to find solution if exists");
        logger.info("=".repeat(70));
    }
}