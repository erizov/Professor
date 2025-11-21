package semester_08.lecture_48_documentation.code_documentation;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.logging.Logger;

/**
 * Code Documentation implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Document function.
     */
    public Map<String, Object> document_function(String funcName, String docstring, List<String> params, String returns) {
        logger.info("Executing document_function");
        Map<String, Object> result = new HashMap<>();
        result.put("type", "function");
        result.put("name", funcName);
        result.put("doc", docstring);
        result.put("params", params);
        result.put("returns", returns);
        return result;
    }

    /**
     * Document class.
     */
    public Map<String, Object> document_class(String className, String docstring, List<String> methods) {
        logger.info("Executing document_class");
        Map<String, Object> result = new HashMap<>();
        result.put("type", "class");
        result.put("name", className);
        result.put("doc", docstring);
        result.put("methods", methods);
        return result;
    }

    /**
     * Generate documentation.
     */
    public String generate_docs() {
        logger.info("Executing generate_docs");
        Map<String, Object> cls = document_class(
            "SampleClass",
            "Holds the primary orchestration logic.",
            Arrays.asList("start", "stop", "report")
        );

        Map<String, Object> func = document_function(
            "processData",
            "Processes the provided dataset and stores the result.",
            Arrays.asList("data", "options"),
            "ProcessingSummary"
        );

        StringBuilder builder = new StringBuilder();
        builder.append("# Documentation Draft\n\n");
        builder.append("## Class\n");
        builder.append("- ").append(cls.get("name")).append(": ").append(cls.get("doc")).append("\n");
        builder.append("  Methods: ").append(cls.get("methods")).append("\n\n");
        builder.append("## Function\n");
        builder.append("- ").append(func.get("name")).append(": ").append(func.get("doc")).append("\n");
        builder.append("  Params: ").append(func.get("params")).append("\n");
        builder.append("  Returns: ").append(func.get("returns")).append("\n");

        return builder.toString();
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Code Documentation");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        Map<String, Object> functionDoc = algo.document_function(
            "generateSummary",
            "Generates a plain text summary.",
            Arrays.asList("content", "formatter"),
            "String"
        );
        System.out.println("Function doc: " + functionDoc);
        System.out.println();
        System.out.println(algo.generate_docs());
        System.out.println("=".repeat(70));
    }
}
