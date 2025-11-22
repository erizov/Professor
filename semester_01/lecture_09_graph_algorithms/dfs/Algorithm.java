package semester_01.lecture_09_graph_algorithms.dfs;

import java.util.*;
import java.util.logging.Logger;

/**
 * Dfs implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());
    
public static List<Integer> dfs(Map<Integer, List<Integer>> graph, int start) {
    List<Integer> visited = new ArrayList<>();
    Stack<Integer> stack = new Stack<>();
    Set<Integer> seen = new HashSet<>();
    
    stack.push(start);
    seen.add(start);
    
    while (!stack.isEmpty()) {
        int vertex = stack.pop();
        visited.add(vertex);
        
        List<Integer> neighbors = graph.getOrDefault(vertex, new ArrayList<>());
        for (int neighbor : neighbors) {
            if (!seen.contains(neighbor)) {
                seen.add(neighbor);
                stack.push(neighbor);
            }
        }
    }
    
    return visited;
}
    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("DFS");
        System.out.println("=".repeat(70));
        
        // Example usage
        // Add example calls based on function signature
        System.out.println("See function implementation for usage examples");
    }

}
