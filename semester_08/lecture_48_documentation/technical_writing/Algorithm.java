package semester_08.lecture_48_documentation.technical_writing;

import java.util.Arrays;
import java.util.List;
import java.util.logging.Logger;

/**
 * Technical Writing implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Create technical document.
     */
    public String create_doc(String docId, String title, String content) {
        logger.info("Executing create_doc");
        StringBuilder builder = new StringBuilder();
        builder.append("# ").append(title).append("\n\n");
        builder.append("Document ID: ").append(docId).append("\n\n");
        builder.append(content).append("\n");
        return builder.toString();
    }

    /**
     * Generate API documentation.
     */
    public String generate_api_doc(String functionName, String description, List<String> params) {
        logger.info("Executing generate_api_doc");
        StringBuilder builder = new StringBuilder();
        builder.append("## ").append(functionName).append("\n\n");
        builder.append(description).append("\n\n");
        builder.append("### Parameters\n");
        for (String param : params) {
            builder.append("- ").append(param).append("\n");
        }
        return builder.toString();
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Technical Writing");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        String document = algo.create_doc("DOC-100", "Integration Guide", "Step-by-step instructions.");
        System.out.println(document);
        System.out.println();
        String apiDoc = algo.generate_api_doc(
            "publishArticle",
            "Publishes the supplied article content.",
            Arrays.asList("title", "body", "tags")
        );
        System.out.println(apiDoc);
        System.out.println("=".repeat(70));
    }
}
