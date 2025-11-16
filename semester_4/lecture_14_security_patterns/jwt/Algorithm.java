/**
 * JSON Web Token (JWT) Pattern.
 * 
 * Compact, URL-safe token format for securely transmitting information
 * between parties. Consists of header, payload, and signature.
 */
import java.util.*;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.time.Instant;
import java.util.Base64;

import java.util.logging.Logger;
class JWT {
    private final String secret;
    
    JWT(String secret) {
        this.secret = secret;
    }
    
    String encode(Map<String, Object> payload, int expiresInSeconds) {
        // Header
        Map<String, String> header = new HashMap<>();
        header.put("alg", "HS256");
        header.put("typ", "JWT");
        
        // Add expiration
        Map<String, Object> payloadCopy = new HashMap<>(payload);
        long now = Instant.now().getEpochSecond();
        payloadCopy.put("exp", now + expiresInSeconds);
        payloadCopy.put("iat", now);
        
        // Encode header and payload
        String headerEncoded = base64UrlEncode(mapToJson(header).getBytes(StandardCharsets.UTF_8));
        String payloadEncoded = base64UrlEncode(mapToJson(payloadCopy).getBytes(StandardCharsets.UTF_8));
        
        // Create signature
        String message = headerEncoded + "." + payloadEncoded;
        String signature = sign(message);
        String signatureEncoded = base64UrlEncode(signature.getBytes(StandardCharsets.UTF_8));
        
        return message + "." + signatureEncoded;
    }
    
    Map<String, Object> decode(String token) {
        try {
            String[] parts = token.split("\\.");
            if (parts.length != 3) {
                return null;
            }
            
            String headerEncoded = parts[0];
            String payloadEncoded = parts[1];
            String signatureEncoded = parts[2];
            
            // Verify signature
            String message = headerEncoded + "." + payloadEncoded;
            String expectedSignature = base64UrlEncode(sign(message).getBytes(StandardCharsets.UTF_8));
            
            if (!signatureEncoded.equals(expectedSignature)) {
                return null;
            }
            
            // Decode payload
            String payloadJson = new String(base64UrlDecode(payloadEncoded), StandardCharsets.UTF_8);
            Map<String, Object> payload = jsonToMap(payloadJson);
            
            // Check expiration
            if (payload.containsKey("exp")) {
                long expTimestamp = ((Number) payload.get("exp")).longValue();
                if (Instant.now().getEpochSecond() > expTimestamp) {
                    return null;
                }
            }
            
            return payload;
        } catch (Exception e) {
            return null;
        }
    }
    
    private String sign(String message) {
        try {
            Mac mac = Mac.getInstance("HmacSHA256");
            SecretKeySpec secretKeySpec = new SecretKeySpec(secret.getBytes(StandardCharsets.UTF_8), "HmacSHA256");
            mac.init(secretKeySpec);
            byte[] signature = mac.doFinal(message.getBytes(StandardCharsets.UTF_8));
            return Base64.getEncoder().encodeToString(signature);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
    
    private String base64UrlEncode(byte[] data) {
        return Base64.getUrlEncoder().withoutPadding().encodeToString(data);
    }
    
    private byte[] base64UrlDecode(String data) {
        return Base64.getUrlDecoder().decode(data);
    }
    
    private String mapToJson(Map<String, ?> map) {
        StringBuilder sb = new StringBuilder("{");
        boolean first = true;
        for (Map.Entry<String, ?> entry : map.entrySet()) {
            if (!first) sb.append(",");
            sb.append("\"").append(entry.getKey()).append("\":");
            Object value = entry.getValue();
            if (value instanceof String) {
                sb.append("\"").append(value).append("\"");
            } else {
                sb.append(value);
            }
            first = false;
        }
        sb.append("}");
        return sb.toString();
    }
    
    private Map<String, Object> jsonToMap(String json) {
        Map<String, Object> map = new HashMap<>();
        json = json.trim().replace("{", "").replace("}", "");
        String[] pairs = json.split(",");
        for (String pair : pairs) {
            String[] kv = pair.split(":");
            if (kv.length == 2) {
                String key = kv[0].trim().replace("\"", "");
                String value = kv[1].trim().replace("\"", "");
                try {
                    map.put(key, Long.parseLong(value));
                } catch (NumberFormatException e) {
                    map.put(key, value);
                }
            }
        }
        return map;
    }
}

public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        logger.info("=".repeat(70));
        logger.info("JSON WEB TOKEN (JWT) PATTERN DEMONSTRATION");
        logger.info("=".repeat(70));
        logger.info();
        
        // Example 1: Create and verify JWT
        logger.info("Example 1: Create and Verify JWT");
        logger.info("-".repeat(70));
        
        JWT jwt = new JWT("my-secret-key");
        
        Map<String, Object> payload = new HashMap<>();
        payload.put("user_id", 12345);
        payload.put("username", "alice");
        payload.put("role", "admin");
        
        String token = jwt.encode(payload, 3600);
        System.out.printf("Token: %s...%n", token.substring(0, Math.min(50, token.length())));
        logger.info();
        
        Map<String, Object> decoded = jwt.decode(token);
        if (decoded != null) {
            logger.info("Decoded payload:");
            for (Map.Entry<String, Object> entry : decoded.entrySet()) {
                if (!entry.getKey().equals("exp") && !entry.getKey().equals("iat")) {
                    System.out.printf("  %s: %s%n", entry.getKey(), entry.getValue());
                }
            }
        } else {
            logger.info("Token invalid or expired");
        }
        logger.info();
        
        // Example 2: Invalid token
        logger.info("Example 2: Invalid Token Detection");
        logger.info("-".repeat(70));
        
        String invalidToken = "invalid.token.here";
        Map<String, Object> invalidDecoded = jwt.decode(invalidToken);
        System.out.printf("Invalid token decode: %s%n",
                        invalidDecoded != null ? "Valid" : "Invalid (as expected)");
        logger.info();
        
        long endTime = System.nanoTime();
        
        logger.info("=".repeat(70));
        logger.info("\nPattern Summary:");
        logger.info("\nIntent:");
        logger.info("  Compact, URL-safe token format for securely transmitting");
        logger.info("  information between parties.");
        logger.info("\nToken Structure:");
        logger.info("  - Header: Algorithm and token type");
        logger.info("  - Payload: Claims (data)");
        logger.info("  - Signature: Verification signature");
        logger.info("\nKey Advantages:");
        logger.info("  - Stateless authentication");
        logger.info("  - Compact format");
        logger.info("  - Self-contained");
        logger.info("  - Widely supported");
        logger.info("\nWhen to Use:");
        logger.info("  - Stateless authentication");
        logger.info("  - API authentication");
        logger.info("  - Microservices communication");
        logger.info("  - Single Sign-On (SSO)");
        logger.info("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}