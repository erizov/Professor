/**
 * OAuth 2.0 Pattern.
 * 
 * Authorization framework that enables applications to obtain limited access
 * to user accounts. Uses authorization codes, access tokens, and refresh tokens.
 */
import java.util.*;
import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;

import java.util.logging.Logger;
class Client {
    String clientId;
    String clientSecret;
    String redirectUri;
    List<String> scopes;
    
    Client(String clientId, String clientSecret, String redirectUri, List<String> scopes) {
        this.clientId = clientId;
        this.clientSecret = clientSecret;
        this.redirectUri = redirectUri;
        this.scopes = scopes;
    }
}

class AuthorizationCode {
    String code;
    String clientId;
    String userId;
    String redirectUri;
    List<String> scopes;
    LocalDateTime expiresAt;
    
    AuthorizationCode(String code, String clientId, String userId, 
                     String redirectUri, List<String> scopes) {
        this.code = code;
        this.clientId = clientId;
        this.userId = userId;
        this.redirectUri = redirectUri;
        this.scopes = scopes;
        this.expiresAt = LocalDateTime.now().plusMinutes(10);
    }
}

class AccessToken {
    String token;
    String clientId;
    String userId;
    List<String> scopes;
    LocalDateTime expiresAt;
    String refreshToken;
    
    AccessToken(String token, String clientId, String userId, 
               List<String> scopes, String refreshToken) {
        this.token = token;
        this.clientId = clientId;
        this.userId = userId;
        this.scopes = scopes;
        this.refreshToken = refreshToken;
        this.expiresAt = LocalDateTime.now().plusHours(1);
    }
}

class AuthorizationServer {
    private final Map<String, Client> clients = new HashMap<>();
    private final Map<String, AuthorizationCode> authorizationCodes = new HashMap<>();
    private final Map<String, AccessToken> accessTokens = new HashMap<>();
    private final Map<String, AccessToken> refreshTokens = new HashMap<>();
    
    void registerClient(Client client) {
        clients.put(client.clientId, client);
    }
    
    String generateAuthorizationCode(String clientId, String userId, 
                                    String redirectUri, List<String> scopes) {
        String code = UUID.randomUUID().toString();
        AuthorizationCode authCode = new AuthorizationCode(
            code, clientId, userId, redirectUri, scopes
        );
        authorizationCodes.put(code, authCode);
        return code;
    }
    
    AccessToken exchangeCodeForToken(String code, String clientId, String clientSecret) {
        AuthorizationCode authCode = authorizationCodes.get(code);
        if (authCode == null) {
            return null;
        }
        
        if (!authCode.clientId.equals(clientId)) {
            return null;
        }
        
        Client client = clients.get(clientId);
        if (client == null || !client.clientSecret.equals(clientSecret)) {
            return null;
        }
        
        if (LocalDateTime.now().isAfter(authCode.expiresAt)) {
            authorizationCodes.remove(code);
            return null;
        }
        
        String accessTokenStr = UUID.randomUUID().toString();
        String refreshTokenStr = UUID.randomUUID().toString();
        AccessToken accessToken = new AccessToken(
            accessTokenStr, clientId, authCode.userId, authCode.scopes, refreshTokenStr
        );
        
        accessTokens.put(accessTokenStr, accessToken);
        refreshTokens.put(refreshTokenStr, accessToken);
        authorizationCodes.remove(code);
        
        return accessToken;
    }
    
    AccessToken refreshAccessToken(String refreshToken) {
        AccessToken oldToken = refreshTokens.get(refreshToken);
        if (oldToken == null) {
            return null;
        }
        
        String newAccessTokenStr = UUID.randomUUID().toString();
        String newRefreshTokenStr = UUID.randomUUID().toString();
        AccessToken newToken = new AccessToken(
            newAccessTokenStr, oldToken.clientId, oldToken.userId, 
            oldToken.scopes, newRefreshTokenStr
        );
        
        accessTokens.remove(oldToken.token);
        refreshTokens.remove(refreshToken);
        accessTokens.put(newAccessTokenStr, newToken);
        refreshTokens.put(newRefreshTokenStr, newToken);
        
        return newToken;
    }
    
    AccessToken validateToken(String token) {
        AccessToken accessToken = accessTokens.get(token);
        if (accessToken == null) {
            return null;
        }
        
        if (LocalDateTime.now().isAfter(accessToken.expiresAt)) {
            accessTokens.remove(token);
            return null;
        }
        
        return accessToken;
    }
}

class ResourceServer {
    private final AuthorizationServer authServer;
    
    ResourceServer(AuthorizationServer authServer) {
        this.authServer = authServer;
    }
    
    Map<String, Object> getResource(String token, String resourcePath) {
        AccessToken accessToken = authServer.validateToken(token);
        if (accessToken == null) {
            return null;
        }
        
        if (!accessToken.scopes.contains("read")) {
            return null;
        }
        
        Map<String, Object> resource = new HashMap<>();
        resource.put("user_id", accessToken.userId);
        resource.put("resource", resourcePath);
        resource.put("data", "Protected data for " + resourcePath);
        return resource;
    }
}

public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        logger.info("=".repeat(70));
        logger.info("OAUTH 2.0 PATTERN DEMONSTRATION");
        logger.info("=".repeat(70));
        logger.info();
        
        // Example 1: OAuth 2.0 Flow
        logger.info("Example 1: OAuth 2.0 Authorization Code Flow");
        logger.info("-".repeat(70));
        
        AuthorizationServer authServer = new AuthorizationServer();
        
        Client client = new Client(
            "my-app", "my-secret", "https://my-app.com/callback",
            Arrays.asList("read", "write")
        );
        authServer.registerClient(client);
        
        logger.info("Step 1: User authorizes application");
        String authCode = authServer.generateAuthorizationCode(
            "my-app", "user123", "https://my-app.com/callback",
            Arrays.asList("read", "write")
        );
        System.out.printf("Authorization code generated: %s...%n", 
                        authCode.substring(0, Math.min(20, authCode.length())));
        logger.info();
        
        logger.info("Step 2: Exchange authorization code for access token");
        AccessToken accessToken = authServer.exchangeCodeForToken(
            authCode, "my-app", "my-secret"
        );
        
        if (accessToken != null) {
            System.out.printf("Access token: %s...%n", 
                            accessToken.token.substring(0, Math.min(30, accessToken.token.length())));
            System.out.printf("Refresh token: %s...%n",
                            accessToken.refreshToken.substring(0, Math.min(30, accessToken.refreshToken.length())));
            System.out.printf("Expires at: %s%n", accessToken.expiresAt);
            System.out.printf("Scopes: %s%n", accessToken.scopes);
        }
        logger.info();
        
        logger.info("Step 3: Use access token to access protected resource");
        ResourceServer resourceServer = new ResourceServer(authServer);
        
        if (accessToken != null) {
            Map<String, Object> resource = resourceServer.getResource(
                accessToken.token, "/api/user/profile"
            );
            
            if (resource != null) {
                System.out.printf("Resource accessed: %s%n", resource);
            } else {
                logger.info("Access denied");
            }
        }
        logger.info();
        
        // Example 2: Token Refresh
        logger.info("Example 2: Refresh Access Token");
        logger.info("-".repeat(70));
        
        if (accessToken != null && accessToken.refreshToken != null) {
            AccessToken newToken = authServer.refreshAccessToken(accessToken.refreshToken);
            if (newToken != null) {
                System.out.printf("New access token: %s...%n",
                                newToken.token.substring(0, Math.min(30, newToken.token.length())));
                System.out.printf("New refresh token: %s...%n",
                                newToken.refreshToken.substring(0, Math.min(30, newToken.refreshToken.length())));
            }
        }
        logger.info();
        
        long endTime = System.nanoTime();
        
        logger.info("=".repeat(70));
        logger.info("\nPattern Summary:");
        logger.info("\nIntent:");
        logger.info("  Authorization framework that enables applications to obtain");
        logger.info("  limited access to user accounts.");
        logger.info("\nOAuth 2.0 Flow:");
        logger.info("  1. Client requests authorization");
        logger.info("  2. User authorizes");
        logger.info("  3. Authorization code returned");
        logger.info("  4. Code exchanged for access token");
        logger.info("  5. Access token used for API calls");
        logger.info("  6. Refresh token used to get new access token");
        logger.info("\nKey Advantages:");
        logger.info("  - Delegated authorization");
        logger.info("  - Limited scope access");
        logger.info("  - No password sharing");
        logger.info("  - Revocable access");
        logger.info("\nWhen to Use:");
        logger.info("  - Third-party application access");
        logger.info("  - API authorization");
        logger.info("  - Single Sign-On (SSO)");
        logger.info("  - Mobile app authentication");
        logger.info("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}