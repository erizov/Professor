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
            System.out.println("Error: Blue environment not deployed");
            return false;
        }
        
        if (currentLive == Environment.GREEN && green != null) {
            green.isLive = false;
            System.out.println("Deactivated GREEN environment");
        }
        
        blue.isLive = true;
        currentLive = Environment.BLUE;
        System.out.printf("Switched traffic to BLUE environment (version %s)%n", blue.version);
        return true;
    }
    
    boolean switchToGreen() {
        if (green == null) {
            System.out.println("Error: Green environment not deployed");
            return false;
        }
        
        if (currentLive == Environment.BLUE && blue != null) {
            blue.isLive = false;
            System.out.println("Deactivated BLUE environment");
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
            System.out.println("Error: No live environment to rollback from");
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
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("BLUE-GREEN DEPLOYMENT PATTERN DEMONSTRATION");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Example 1: Initial Deployment
        System.out.println("Example 1: Initial Deployment to Blue");
        System.out.println("-".repeat(70));
        
        BlueGreenDeployment deployment = new BlueGreenDeployment();
        deployment.deployToBlue("v1.0.0");
        deployment.switchToBlue();
        System.out.println();
        
        // Example 2: Deploy New Version to Green
        System.out.println("Example 2: Deploy New Version to Green");
        System.out.println("-".repeat(70));
        
        deployment.deployToGreen("v1.1.0");
        System.out.printf("Status: %s%n", deployment.getStatus());
        System.out.println();
        
        // Example 3: Switch to Green
        System.out.println("Example 3: Switch Traffic to Green (New Version)");
        System.out.println("-".repeat(70));
        
        deployment.switchToGreen();
        Deployment live = deployment.getLiveEnvironment();
        System.out.printf("Live environment: %s (version %s)%n",
                        live.environment.name(), live.version);
        System.out.println();
        
        // Example 4: Rollback
        System.out.println("Example 4: Rollback to Blue");
        System.out.println("-".repeat(70));
        
        deployment.rollback();
        live = deployment.getLiveEnvironment();
        System.out.printf("After rollback: %s (version %s)%n",
                        live.environment.name(), live.version);
        System.out.println();
        
        // Example 5: Deploy Another Version
        System.out.println("Example 5: Deploy Another Version to Blue");
        System.out.println("-".repeat(70));
        
        deployment.deployToBlue("v1.2.0");
        deployment.switchToBlue();
        System.out.printf("Status: %s%n", deployment.getStatus());
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nPattern Summary:");
        System.out.println("\nIntent:");
        System.out.println("  Maintains two identical production environments (blue and green).");
        System.out.println("  Only one environment is live at a time, allowing instant rollback.");
        System.out.println("\nKey Advantages:");
        System.out.println("  - Zero-downtime deployments");
        System.out.println("  - Instant rollback");
        System.out.println("  - Easy testing of new version");
        System.out.println("  - Reduced deployment risk");
        System.out.println("\nWhen to Use:");
        System.out.println("  - Zero-downtime requirements");
        System.out.println("  - Critical production systems");
        System.out.println("  - When rollback speed is important");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
