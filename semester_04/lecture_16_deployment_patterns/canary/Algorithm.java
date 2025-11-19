/**
 * Canary Deployment Pattern.
 * 
 * Gradually roll out new version to a small subset of users before
 * full deployment. Monitor metrics and rollback if issues detected.
 */
import java.time.LocalDateTime;
import java.util.*;

enum DeploymentStatus {
    PENDING, CANARY, ROLLING_OUT, COMPLETE, ROLLED_BACK
}

import java.util.logging.Logger;
class CanaryDeployment {
    String version;
    DeploymentStatus status;
    double trafficPercentage;
    LocalDateTime deployedAt;
    Map<String, Double> metrics;
    
    CanaryDeployment(String version, DeploymentStatus status, double trafficPercentage,
                    LocalDateTime deployedAt) {
        this.version = version;
        this.status = status;
        this.trafficPercentage = trafficPercentage;
        this.deployedAt = deployedAt;
        this.metrics = new HashMap<>();
    }
}

class CanaryDeploymentManager {
    private final String baselineVersion;
    private CanaryDeployment canary;
    private double trafficSplit = 0.0;
    
    CanaryDeploymentManager(String baselineVersion) {
        this.baselineVersion = baselineVersion;
    }
    
    CanaryDeployment deployCanary(String version, double initialTraffic) {
        if (initialTraffic < 0 || initialTraffic > 100) {
            throw new IllegalArgumentException("Traffic percentage must be between 0 and 100");
        }
        
        canary = new CanaryDeployment(version, DeploymentStatus.CANARY,
                                     initialTraffic, LocalDateTime.now());
        trafficSplit = initialTraffic;
        System.out.printf("Deployed canary version %s with %.1f%% traffic%n",
                         version, initialTraffic);
        return canary;
    }
    
    boolean increaseTraffic(double increment) {
        if (canary == null) {
            logger.info("Error: No canary deployment");
            return false;
        }
        
        double newPercentage = Math.min(100.0, trafficSplit + increment);
        trafficSplit = newPercentage;
        canary.trafficPercentage = newPercentage;
        
        if (newPercentage >= 100.0) {
            canary.status = DeploymentStatus.COMPLETE;
            System.out.printf("Canary deployment complete: %s%n", canary.version);
        } else {
            canary.status = DeploymentStatus.ROLLING_OUT;
            System.out.printf("Increased canary traffic to %.1f%%%n", newPercentage);
        }
        
        return true;
    }
    
    void updateMetrics(double errorRate, double latencyMs, double throughput) {
        if (canary == null) {
            return;
        }
        
        canary.metrics.put("error_rate", errorRate);
        canary.metrics.put("latency_ms", latencyMs);
        canary.metrics.put("throughput", throughput);
    }
    
    boolean shouldRollback(Map<String, Double> baselineMetrics, double threshold) {
        if (canary == null || canary.metrics.isEmpty()) {
            return false;
        }
        
        double canaryErrorRate = canary.metrics.getOrDefault("error_rate", 0.0);
        double baselineErrorRate = baselineMetrics.getOrDefault("error_rate", 0.0);
        
        if (canaryErrorRate > baselineErrorRate + threshold) {
            return true;
        }
        
        double canaryLatency = canary.metrics.getOrDefault("latency_ms", 0.0);
        double baselineLatency = baselineMetrics.getOrDefault("latency_ms", 0.0);
        
        if (canaryLatency > baselineLatency * 1.5) {
            return true;
        }
        
        return false;
    }
    
    boolean rollback() {
        if (canary == null) {
            logger.info("Error: No canary deployment to rollback");
            return false;
        }
        
        canary.status = DeploymentStatus.ROLLED_BACK;
        trafficSplit = 0.0;
        System.out.printf("Rolled back canary version %s%n", canary.version);
        return true;
    }
    
    String routeRequest(String userId) {
        if (canary == null || canary.status == DeploymentStatus.ROLLED_BACK) {
            return baselineVersion;
        }
        
        int userHash = Math.abs(userId.hashCode()) % 100;
        if (userHash < trafficSplit) {
            return canary.version;
        } else {
            return baselineVersion;
        }
    }
    
    Map<String, Object> getStatus() {
        Map<String, Object> status = new HashMap<>();
        status.put("baseline_version", baselineVersion);
        
        Map<String, Object> canaryStatus = new HashMap<>();
        if (canary != null) {
            canaryStatus.put("version", canary.version);
            canaryStatus.put("status", canary.status.name());
            canaryStatus.put("traffic_percentage", trafficSplit);
            canaryStatus.put("metrics", canary.metrics);
        } else {
            canaryStatus.put("version", null);
            canaryStatus.put("status", null);
            canaryStatus.put("traffic_percentage", 0.0);
            canaryStatus.put("metrics", null);
        }
        
        status.put("canary", canaryStatus);
        return status;
    }
}

public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    public static void main(String[] args) {
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        long startTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("CANARY DEPLOYMENT PATTERN DEMONSTRATION");
        logger.info(separator);
        logger.info("");
        
        // Example 1: Initial Canary Deployment
        logger.info("Example 1: Deploy Canary with 5% Traffic");
        logger.info(dash);
        
        CanaryDeploymentManager manager = new CanaryDeploymentManager("v1.0.0");
        manager.deployCanary("v1.1.0", 5.0);
        System.out.printf("Status: %s%n", manager.getStatus());
        logger.info("");
        
        // Example 2: Request Routing
        logger.info("Example 2: Request Routing Based on Traffic Split");
        logger.info(dash);
        
        String[] users = {"user1", "user2", "user3", "user4", "user5"};
        for (String user : users) {
            String version = manager.routeRequest(user);
            System.out.printf("User %s -> %s%n", user, version);
        }
        logger.info("");
        
        // Example 3: Monitor Metrics
        logger.info("Example 3: Monitor Canary Metrics");
        logger.info(dash);
        
        Map<String, Double> baselineMetrics = new HashMap<>();
        baselineMetrics.put("error_rate", 0.01);
        baselineMetrics.put("latency_ms", 100.0);
        baselineMetrics.put("throughput", 1000.0);
        
        manager.updateMetrics(0.005, 95.0, 1050.0);
        boolean shouldRollback = manager.shouldRollback(baselineMetrics, 0.1);
        
        logger.info("Canary metrics: error_rate=0.005, latency_ms=95.0, throughput=1050.0");
        System.out.printf("Should rollback: %s (canary is performing well)%n", shouldRollback);
        logger.info("");
        
        // Example 4: Increase Traffic
        logger.info("Example 4: Gradually Increase Traffic");
        logger.info(dash);
        
        manager.increaseTraffic(10.0);  // 15%
        manager.increaseTraffic(15.0);  // 30%
        manager.increaseTraffic(20.0);  // 50%
        manager.increaseTraffic(50.0);  // 100%
        logger.info("");
        
        // Example 5: Rollback on Issues
        logger.info("Example 5: Rollback on High Error Rate");
        logger.info(dash);
        
        CanaryDeploymentManager manager2 = new CanaryDeploymentManager("v1.0.0");
        manager2.deployCanary("v1.2.0", 10.0);
        
        manager2.updateMetrics(0.15, 200.0, 800.0);
        shouldRollback = manager2.shouldRollback(baselineMetrics, 0.1);
        
        logger.info("Canary error rate: 15% (baseline: 1%)");
        System.out.printf("Should rollback: %s%n", shouldRollback);
        
        if (shouldRollback) {
            manager2.rollback();
        }
        logger.info("");
        
        long endTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("\nPattern Summary:");
        logger.info("\nIntent:");
        logger.info("  Gradually roll out new version to a small subset of users");
        logger.info("  before full deployment. Monitor metrics and rollback if needed.");
        logger.info("\nKey Advantages:");
        logger.info("  - Reduced risk of bad deployments");
        logger.info("  - Real-world testing with production traffic");
        logger.info("  - Gradual rollout");
        logger.info("  - Automatic rollback capability");
        logger.info("\nWhen to Use:");
        logger.info("  - High-traffic applications");
        logger.info("  - When gradual rollout is preferred");
        logger.info("  - When monitoring is available");
        logger.info(separator);
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}