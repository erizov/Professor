/**
 * Blue-Green Deployment Pattern.
 * 
 * Maintains two identical production environments (blue and green).
 * Only one environment is live at a time, allowing instant rollback.
 */
import java.time.LocalDateTime;
import java.util.*;

enum Environment {
    BLUE, GREEN
}

import java.util.logging.Logger;
class Deployment {
    Environment environment;
    String version;
    LocalDateTime deployedAt;
    boolean isLive;
    
    Deployment(Environment environment, String version, LocalDateTime deployedAt, boolean isLive) {
        this.environment = environment;
        this.version = version;
        this.deployedAt = deployedAt;
        this.isLive = isLive;
    }
}

class BlueGreenDeployment {
    private Deployment blue;
    private Deployment green;
    private Environment currentLive;
    
    Deployment deployToBlue(String version) {
        blue = new Deployment(Environment.BLUE, version, LocalDateTime.now(), false);
        System.out.printf("Deployed version %s to BLUE environment%n", version);
        return blue;
    }
    
    Deployment deployToGreen(String version) {
        green = new Deployment(Environment.GREEN, version, LocalDateTime.now(), false);
        System.out.printf("Deployed version %s to GREEN environment%n", version);
        return green;
    }
    
    boolean switchToBlue() {
        if (blue == null) {
            logger.info("Error: Blue environment not deployed");
            return false;
        }
        
        if (currentLive == Environment.GREEN && green != null) {
            green.isLive = false;
            logger.info("Deactivated GREEN environment");
        }
        
        blue.isLive = true;
        currentLive = Environment.BLUE;
        System.out.printf("Switched traffic to BLUE environment (version %s)%n", blue.version);
        return true;
    }
    
    boolean switchToGreen() {
        if (green == null) {
            logger.info("Error: Green environment not deployed");
            return false;
        }
        
        if (currentLive == Environment.BLUE && blue != null) {
            blue.isLive = false;
            logger.info("Deactivated BLUE environment");
        }
        
        green.isLive = true;
        currentLive = Environment.GREEN;
        System.out.printf("Switched traffic to GREEN environment (version %s)%n", green.version);
        return true;
    }
    
    boolean rollback() {
        if (currentLive == Environment.BLUE) {
            return switchToGreen();
        } else if (currentLive == Environment.GREEN) {
            return switchToBlue();
        } else {
            logger.info("Error: No live environment to rollback from");
            return false;
        }
    }
    
    Deployment getLiveEnvironment() {
        if (currentLive == Environment.BLUE) {
            return blue;
        } else if (currentLive == Environment.GREEN) {
            return green;
        }
        return null;
    }
    
    Map<String, Object> getStatus() {
        Map<String, Object> status = new HashMap<>();
        
        Map<String, Object> blueStatus = new HashMap<>();
        blueStatus.put("version", blue != null ? blue.version : null);
        blueStatus.put("is_live", blue != null && blue.isLive);
        blueStatus.put("deployed_at", blue != null ? blue.deployedAt.toString() : null);
        
        Map<String, Object> greenStatus = new HashMap<>();
        greenStatus.put("version", green != null ? green.version : null);
        greenStatus.put("is_live", green != null && green.isLive);
        greenStatus.put("deployed_at", green != null ? green.deployedAt.toString() : null);
        
        status.put("blue", blueStatus);
        status.put("green", greenStatus);
        status.put("current_live", currentLive != null ? currentLive.name() : null);
        
        return status;
    }
}

public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        logger.info("=".repeat(70));
        logger.info("BLUE-GREEN DEPLOYMENT PATTERN DEMONSTRATION");
        logger.info("=".repeat(70));
        logger.info();
        
        // Example 1: Initial Deployment
        logger.info("Example 1: Initial Deployment to Blue");
        logger.info("-".repeat(70));
        
        BlueGreenDeployment deployment = new BlueGreenDeployment();
        deployment.deployToBlue("v1.0.0");
        deployment.switchToBlue();
        logger.info();
        
        // Example 2: Deploy New Version to Green
        logger.info("Example 2: Deploy New Version to Green");
        logger.info("-".repeat(70));
        
        deployment.deployToGreen("v1.1.0");
        System.out.printf("Status: %s%n", deployment.getStatus());
        logger.info();
        
        // Example 3: Switch to Green
        logger.info("Example 3: Switch Traffic to Green (New Version)");
        logger.info("-".repeat(70));
        
        deployment.switchToGreen();
        Deployment live = deployment.getLiveEnvironment();
        System.out.printf("Live environment: %s (version %s)%n",
                        live.environment.name(), live.version);
        logger.info();
        
        // Example 4: Rollback
        logger.info("Example 4: Rollback to Blue");
        logger.info("-".repeat(70));
        
        deployment.rollback();
        live = deployment.getLiveEnvironment();
        System.out.printf("After rollback: %s (version %s)%n",
                        live.environment.name(), live.version);
        logger.info();
        
        // Example 5: Deploy Another Version
        logger.info("Example 5: Deploy Another Version to Blue");
        logger.info("-".repeat(70));
        
        deployment.deployToBlue("v1.2.0");
        deployment.switchToBlue();
        System.out.printf("Status: %s%n", deployment.getStatus());
        logger.info();
        
        long endTime = System.nanoTime();
        
        logger.info("=".repeat(70));
        logger.info("\nPattern Summary:");
        logger.info("\nIntent:");
        logger.info("  Maintains two identical production environments (blue and green).");
        logger.info("  Only one environment is live at a time, allowing instant rollback.");
        logger.info("\nKey Advantages:");
        logger.info("  - Zero-downtime deployments");
        logger.info("  - Instant rollback");
        logger.info("  - Easy testing of new version");
        logger.info("  - Reduced deployment risk");
        logger.info("\nWhen to Use:");
        logger.info("  - Zero-downtime requirements");
        logger.info("  - Critical production systems");
        logger.info("  - When rollback speed is important");
        logger.info("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}