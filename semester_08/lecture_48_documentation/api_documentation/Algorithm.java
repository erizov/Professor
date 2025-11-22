// package semester_08.lecture_48_documentation.api_documentation;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.logging.Logger;

/**
 * Api Documentation implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());
    private final List<Map<String, Object>> endpoints = new ArrayList<>();

    public Algorithm() {
        // Initialize
    }

    /**
     * Add API endpoint.
     */
    public Map<String, Object> add_endpoint(String method, String path, String description, List<String> params, String response) {
        logger.info("Executing add_endpoint");
        Map<String, Object> endpoint = new HashMap<>();
        endpoint.put("method", method);
        endpoint.put("path", path);
        endpoint.put("description", description);
        endpoint.put("params", params);
        endpoint.put("response", response);
        endpoints.add(endpoint);
        return endpoint;
    }

    /**
     * Generate markdown documentation.
     */
    public String generate_markdown() {
        logger.info("Executing generate_markdown");
        StringBuilder builder = new StringBuilder();
        builder.append("# API Documentation\n\n");
        for (Map<String, Object> endpoint : endpoints) {
            builder.append("## ").append(endpoint.get("method")).append(" ").append(endpoint.get("path")).append("\n");
            builder.append(endpoint.get("description")).append("\n\n");
            builder.append("### Parameters\n");
            @SuppressWarnings("unchecked")
            List<String> params = (List<String>) endpoint.get("params");
            for (String param : params) {
                builder.append("- ").append(param).append("\n");
            }
            builder.append("\n**Response:** ").append(endpoint.get("response")).append("\n\n");
        }
        return builder.toString();
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Api Documentation");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        algo.add_endpoint("GET", "/status", "Returns the service status.", List.of("verbose"), "{ \"status\": \"ok\" }");
        algo.add_endpoint("POST", "/users", "Creates a new user.", List.of("name", "email"), "{ \"id\": 1 }");
        System.out.println(algo.generate_markdown());
        System.out.println("=".repeat(70));
    }
}
