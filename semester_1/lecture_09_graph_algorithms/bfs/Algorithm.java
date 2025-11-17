import java.util.*;
import java.util.logging.Logger;

/**
 * Bfs implementation.
 */
    public static List<Integer> bfs(Map<Integer, List<Integer>> graph, int start) {
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
        System.out.println("Bfs");
        System.out.println("=".repeat(70));
        
        Object result = bfs();
        System.out.println("Result: " + result);
        System.out.println("\nSee README.md for implementation details");
    }
}
