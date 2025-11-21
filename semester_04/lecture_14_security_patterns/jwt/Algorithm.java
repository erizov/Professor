package semester_04.lecture_14_security_patterns.jwt;

import java.nio.charset.StandardCharsets;
import java.util.Base64;
import java.util.HashMap;
import java.util.Map;
import java.util.logging.Logger;

/**
 * Jwt implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Encode JWT.
     */
    public String encode(Map<String, Object> payload, long expiresInSeconds) {
        logger.info("Executing encode");
        long exp = (System.currentTimeMillis() / 1000) + expiresInSeconds;
        Map<String, Object> fullPayload = new HashMap<>(payload);
        fullPayload.put("exp", exp);

        String headerJson = "{\"alg\":\"HS256\",\"typ\":\"JWT\"}";
        String payloadJson = JsonUtil.toJson(fullPayload);

        String headerB64 = Base64.getUrlEncoder().withoutPadding()
            .encodeToString(headerJson.getBytes(StandardCharsets.UTF_8));
        String payloadB64 = Base64.getUrlEncoder().withoutPadding()
            .encodeToString(payloadJson.getBytes(StandardCharsets.UTF_8));

        // Dummy signature for illustration purposes
        String signature = Base64.getUrlEncoder().withoutPadding()
            .encodeToString("signature".getBytes(StandardCharsets.UTF_8));

        return headerB64 + "." + payloadB64 + "." + signature;
    }

    /**
     * Decode JWT.
     */
    public Map<String, Object> decode(String token) {
        logger.info("Executing decode");
        String[] parts = token.split("\\.");
        if (parts.length != 3) {
            throw new IllegalArgumentException("Invalid token format");
        }
        String payloadJson = new String(Base64.getUrlDecoder().decode(parts[1]), StandardCharsets.UTF_8);
        return JsonUtil.fromJson(payloadJson);
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Jwt");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        Map<String, Object> payload = new HashMap<>();
        payload.put("sub", "user-123");
        payload.put("role", "admin");
        String token = algo.encode(payload, 3600);
        System.out.println("Token: " + token);
        System.out.println("Decoded: " + algo.decode(token));
        System.out.println("=".repeat(70));
    }
}

final class JsonUtil {
    private JsonUtil() {
    }

    static String toJson(Map<String, Object> map) {
        StringBuilder builder = new StringBuilder("{");
        boolean first = true;
        for (Map.Entry<String, Object> entry : map.entrySet()) {
            if (!first) {
                builder.append(",");
            }
            builder.append("\"").append(entry.getKey()).append("\":");
            Object value = entry.getValue();
            if (value instanceof Number) {
                builder.append(value);
            } else {
                builder.append("\"").append(value).append("\"");
            }
            first = false;
        }
        builder.append("}");
        return builder.toString();
    }

    static Map<String, Object> fromJson(String json) {
        Map<String, Object> map = new HashMap<>();
        String content = json.trim();
        if (content.length() <= 2) {
            return map;
        }
        content = content.substring(1, content.length() - 1); // remove braces
        for (String pair : content.split(",")) {
            String[] parts = pair.split(":", 2);
            if (parts.length != 2) {
                continue;
            }
            String key = parts[0].trim().replace("\"", "");
            String rawValue = parts[1].trim();
            if (rawValue.matches("\\d+")) {
                map.put(key, Long.parseLong(rawValue));
            } else {
                map.put(key, rawValue.replace("\"", ""));
            }
        }
        return map;
    }
}
