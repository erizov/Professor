#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Canary Deployment Pattern.

Gradually roll out new version to a small subset of users before
full deployment. Monitor metrics and rollback if issues detected.
"""

import sys
from pathlib import Path
from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import random

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


class DeploymentStatus(Enum):
    """Deployment status."""
    PENDING = "pending"
    CANARY = "canary"
    ROLLING_OUT = "rolling_out"
    COMPLETE = "complete"
    ROLLED_BACK = "rolled_back"


@dataclass
class CanaryDeployment:
    """Canary deployment information."""
    version: str
    status: DeploymentStatus
    traffic_percentage: float
    deployed_at: datetime
    metrics: Dict[str, float] = None
    
    def __post_init__(self):
        if self.metrics is None:
            self.metrics = {}


class CanaryDeploymentManager:
    """Canary deployment manager."""
    
    def __init__(self, baseline_version: str = "v1.0.0"):
        self.baseline_version = baseline_version
        self.canary: Optional[CanaryDeployment] = None
        self.traffic_split: float = 0.0  # Percentage to canary
    
    def deploy_canary(self, version: str, initial_traffic: float = 5.0) -> CanaryDeployment:
        """
        Deploy canary version.
        
        Args:
            version: New version to deploy
            initial_traffic: Initial traffic percentage (default 5%)
        """
        if initial_traffic < 0 or initial_traffic > 100:
            raise ValueError("Traffic percentage must be between 0 and 100")
        
        self.canary = CanaryDeployment(
            version=version,
            status=DeploymentStatus.CANARY,
            traffic_percentage=initial_traffic,
            deployed_at=datetime.now()
        )
        
        self.traffic_split = initial_traffic
        logger.info(f"Deployed canary version {version} with {initial_traffic}% traffic")
        return self.canary
    
    def increase_traffic(self, increment: float = 10.0) -> bool:
        """
        Increase canary traffic.
        
        Args:
            increment: Percentage to increase (default 10%)
        """
        if not self.canary:
            logger.info("Error: No canary deployment")
            return False
        
        new_percentage = min(100.0, self.traffic_split + increment)
        self.traffic_split = new_percentage
        self.canary.traffic_percentage = new_percentage
        
        if new_percentage >= 100.0:
            self.canary.status = DeploymentStatus.COMPLETE
            logger.info(f"Canary deployment complete: {self.canary.version}")
        else:
            self.canary.status = DeploymentStatus.ROLLING_OUT
            logger.info(f"Increased canary traffic to {new_percentage}%")
        
        return True
    
    def update_metrics(self, error_rate: float, latency_ms: float, 
                      throughput: float) -> None:
        """Update canary metrics."""
        if not self.canary:
            return
        
        self.canary.metrics = {
            "error_rate": error_rate,
            "latency_ms": latency_ms,
            "throughput": throughput
        }
    
    def should_rollback(self, baseline_metrics: Dict[str, float], 
                       threshold: float = 0.1) -> bool:
        """
        Determine if canary should be rolled back.
        
        Args:
            baseline_metrics: Baseline version metrics
            threshold: Error rate threshold (default 10%)
        """
        if not self.canary or not self.canary.metrics:
            return False
        
        canary_error_rate = self.canary.metrics.get("error_rate", 0.0)
        baseline_error_rate = baseline_metrics.get("error_rate", 0.0)
        
        # Rollback if canary error rate is significantly higher
        if canary_error_rate > baseline_error_rate + threshold:
            return True
        
        # Rollback if canary latency is significantly higher
        canary_latency = self.canary.metrics.get("latency_ms", 0.0)
        baseline_latency = baseline_metrics.get("latency_ms", 0.0)
        
        if canary_latency > baseline_latency * 1.5:  # 50% increase
            return True
        
        return False
    
    def rollback(self) -> bool:
        """Rollback canary deployment."""
        if not self.canary:
            logger.info("Error: No canary deployment to rollback")
            return False
        
        self.canary.status = DeploymentStatus.ROLLED_BACK
        self.traffic_split = 0.0
        logger.info(f"Rolled back canary version {self.canary.version}")
        return True
    
    def route_request(self, user_id: str) -> str:
        """
        Route request to baseline or canary based on traffic split.
        
        Args:
            user_id: User identifier
            
        Returns:
            Version to route to
        """
        if not self.canary or self.canary.status == DeploymentStatus.ROLLED_BACK:
            return self.baseline_version
        
        # Deterministic routing based on user_id hash
        user_hash = hash(user_id) % 100
        if user_hash < self.traffic_split:
            return self.canary.version
        else:
            return self.baseline_version
    
    def get_status(self) -> dict:
        """Get deployment status."""
        return {
            "baseline_version": self.baseline_version,
            "canary": {
                "version": self.canary.version if self.canary else None,
                "status": self.canary.status.value if self.canary else None,
                "traffic_percentage": self.traffic_split,
                "metrics": self.canary.metrics if self.canary else None
            }
        }


def main() -> None:
    """Demonstration of Canary Deployment Pattern."""
    logger.info("=" * 70)
    logger.info("CANARY DEPLOYMENT PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Initial Canary Deployment
    logger.info("Example 1: Deploy Canary with 5% Traffic")
    logger.info("-" * 70)
    
    manager = CanaryDeploymentManager(baseline_version="v1.0.0")
    manager.deploy_canary("v1.1.0", initial_traffic=5.0)
    logger.info(f"Status: {manager.get_status()}")
    logger.info()
    
    # Example 2: Request Routing
    logger.info("Example 2: Request Routing Based on Traffic Split")
    logger.info("-" * 70)
    
    users = ["user1", "user2", "user3", "user4", "user5"]
    for user in users:
        version = manager.route_request(user)
        logger.info(f"User {user} -> {version}")
    logger.info()
    
    # Example 3: Monitor Metrics
    logger.info("Example 3: Monitor Canary Metrics")
    logger.info("-" * 70)
    
    baseline_metrics = {"error_rate": 0.01, "latency_ms": 100.0, "throughput": 1000.0}
    canary_metrics = {"error_rate": 0.005, "latency_ms": 95.0, "throughput": 1050.0}
    
    manager.update_metrics(
        error_rate=canary_metrics["error_rate"],
        latency_ms=canary_metrics["latency_ms"],
        throughput=canary_metrics["throughput"]
    )
    
    should_rollback = manager.should_rollback(baseline_metrics)
    logger.info(f"Canary metrics: {canary_metrics}")
    logger.info(f"Should rollback: {should_rollback} (canary is performing well)")
    logger.info()
    
    # Example 4: Increase Traffic
    logger.info("Example 4: Gradually Increase Traffic")
    logger.info("-" * 70)
    
    manager.increase_traffic(10.0)  # 15%
    manager.increase_traffic(15.0)  # 30%
    manager.increase_traffic(20.0)  # 50%
    manager.increase_traffic(50.0)  # 100%
    logger.info()
    
    # Example 5: Rollback on Issues
    logger.info("Example 5: Rollback on High Error Rate")
    logger.info("-" * 70)
    
    manager2 = CanaryDeploymentManager(baseline_version="v1.0.0")
    manager2.deploy_canary("v1.2.0", initial_traffic=10.0)
    
    # Simulate high error rate
    manager2.update_metrics(error_rate=0.15, latency_ms=200.0, throughput=800.0)
    should_rollback = manager2.should_rollback(baseline_metrics, threshold=0.1)
    
    logger.info(f"Canary error rate: 15% (baseline: 1%)")
    logger.info(f"Should rollback: {should_rollback}")
    
    if should_rollback:
        manager2.rollback()
    logger.info()
    
    # Example 6: Performance measurement
    logger.info("Example 6: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Canary Deployment")
    
    def canary_operations():
        mgr = CanaryDeploymentManager("v1.0.0")
        mgr.deploy_canary("v1.1.0", 5.0)
        
        for _ in range(100):
            mgr.route_request(f"user{random.randint(1, 1000)}")
        
        mgr.increase_traffic(95.0)
        return mgr.get_status()
    
    result, metrics = timer.measure(canary_operations)
    logger.info(f"Time for canary operations: {metrics['execution_time_ms']:.3f} ms")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Gradually roll out new version to a small subset of users")
    logger.info("  before full deployment. Monitor metrics and rollback if needed.")
    logger.info("\nKey Advantages:")
    logger.info("  - Reduced risk of bad deployments")
    logger.info("  - Real-world testing with production traffic")
    logger.info("  - Gradual rollout")
    logger.info("  - Automatic rollback capability")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Requires monitoring infrastructure")
    logger.info("  - More complex than blue-green")
    logger.info("  - Slower deployment process")
    logger.info("  - Traffic routing complexity")
    logger.info("\nWhen to Use:")
    logger.info("  - High-traffic applications")
    logger.info("  - When gradual rollout is preferred")
    logger.info("  - When monitoring is available")
    logger.info("  - Risk-averse deployments")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Large-scale web applications")
    logger.info("  - API service deployments")
    logger.info("  - Feature flag rollouts")
    logger.info("  - A/B testing")
    logger.info("\nDeployment Flow:")
    logger.info("  1. Deploy canary with small traffic (5-10%)")
    logger.info("  2. Monitor metrics (error rate, latency, throughput)")
    logger.info("  3. Gradually increase traffic (10% -> 25% -> 50% -> 100%)")
    logger.info("  4. Rollback if metrics degrade")
    logger.info("  5. Complete deployment if metrics are good")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()