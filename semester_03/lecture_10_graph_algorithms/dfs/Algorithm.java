/**
 * Depth-First Search (DFS) implementation.
 * 
 * Graph traversal algorithm that explores as far as possible along each
 * branch before backtracking.
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
    
    public List<Integer> dfs(int start) {
        List<Integer> result = new ArrayList<>();
        Set<Integer> visited = new HashSet<>();
        dfsRecursive(start, visited, result);
        return result;
    }
    
    private void dfsRecursive(int node, Set<Integer> visited, List<Integer> result) {
        visited.add(node);
        result.add(node);
        
        List<Integer> neighbors = graph.getOrDefault(node, new ArrayList<>());
        for (int neighbor : neighbors) {
            if (!visited.contains(neighbor)) {
                dfsRecursive(neighbor, visited, result);
            }
        }
    }
    
    public List<Integer> dfsIterative(int start) {
        List<Integer> result = new ArrayList<>();
        Set<Integer> visited = new HashSet<>();
        Stack<Integer> stack = new Stack<>();
        
        stack.push(start);
        
        while (!stack.isEmpty()) {
            int node = stack.pop();
            
            if (!visited.contains(node)) {
                visited.add(node);
                result.add(node);
                
                List<Integer> neighbors = graph.getOrDefault(node, new ArrayList<>());
                Collections.reverse(neighbors);
                for (int neighbor : neighbors) {
                    if (!visited.contains(neighbor)) {
                        stack.push(neighbor);
                    }
                }
            }
        }
        
        return result;
    }
}

public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public static void main(String[] args) {
        logger.info("=".repeat(70));
        logger.info("DEPTH-FIRST SEARCH (DFS) DEMONSTRATION");
        logger.info("=".repeat(70));
        logger.info();
        
        // Example 1: Recursive DFS
        logger.info("Example 1: Recursive DFS");
        logger.info("-".repeat(70));
        Graph g1 = new Graph(false);
        g1.addEdge(0, 1);
        g1.addEdge(0, 2);
        g1.addEdge(1, 3);
        g1.addEdge(2, 4);
        g1.addEdge(3, 4);
        
        List<Integer> dfsResult = g1.dfs(0);
        logger.info("DFS from node 0: " + dfsResult);
        logger.info();
        
        // Example 2: Iterative DFS
        logger.info("Example 2: Iterative DFS");
        logger.info("-".repeat(70));
        List<Integer> dfsIter = g1.dfsIterative(0);
        logger.info("Iterative DFS from node 0: " + dfsIter);
        logger.info();
        
        logger.info("=".repeat(70));
        logger.info("\nAlgorithm Summary:");
        logger.info("\nTime Complexity: O(V + E)");
        logger.info("Space Complexity: O(V)");
        logger.info("\nKey Advantages:");
        logger.info("  - Memory efficient");
        logger.info("  - Detects cycles");
        logger.info("  - Topological sorting");
        logger.info("=".repeat(70));
    }
}