#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Blue-Green Deployment Pattern.

Maintains two identical production environments (blue and green).
Only one environment is live at a time, allowing instant rollback.
"""

import sys
from pathlib import Path
from enum import Enum
from typing import Optional
from dataclasses import dataclass
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


class Environment(Enum):
    """Deployment environment."""
    BLUE = "blue"
    GREEN = "green"


@dataclass
class Deployment:
    """Deployment information."""
    environment: Environment
    version: str
    deployed_at: datetime
    is_live: bool = False


class BlueGreenDeployment:
    """Blue-Green deployment manager."""
    
    def __init__(self):
        self.blue: Optional[Deployment] = None
        self.green: Optional[Deployment] = None
        self.current_live: Optional[Environment] = None
    
    def deploy_to_blue(self, version: str) -> Deployment:
        """Deploy to blue environment."""
        self.blue = Deployment(
            environment=Environment.BLUE,
            version=version,
            deployed_at=datetime.now(),
            is_live=False
        )
        logger.info(f"Deployed version {version} to BLUE environment")
        return self.blue
    
    def deploy_to_green(self, version: str) -> Deployment:
        """Deploy to green environment."""
        self.green = Deployment(
            environment=Environment.GREEN,
            version=version,
            deployed_at=datetime.now(),
            is_live=False
        )
        logger.info(f"Deployed version {version} to GREEN environment")
        return self.green
    
    def switch_to_blue(self) -> bool:
        """Switch traffic to blue environment."""
        if not self.blue:
            logger.info("Error: Blue environment not deployed")
            return False
        
        # Deactivate current live environment
        if self.current_live == Environment.GREEN and self.green:
            self.green.is_live = False
            logger.info("Deactivated GREEN environment")
        
        # Activate blue
        self.blue.is_live = True
        self.current_live = Environment.BLUE
        logger.info(f"Switched traffic to BLUE environment (version {self.blue.version})")
        return True
    
    def switch_to_green(self) -> bool:
        """Switch traffic to green environment."""
        if not self.green:
            logger.info("Error: Green environment not deployed")
            return False
        
        # Deactivate current live environment
        if self.current_live == Environment.BLUE and self.blue:
            self.blue.is_live = False
            logger.info("Deactivated BLUE environment")
        
        # Activate green
        self.green.is_live = True
        self.current_live = Environment.GREEN
        logger.info(f"Switched traffic to GREEN environment (version {self.green.version})")
        return True
    
    def rollback(self) -> bool:
        """Rollback to previous environment."""
        if self.current_live == Environment.BLUE:
            return self.switch_to_green()
        elif self.current_live == Environment.GREEN:
            return self.switch_to_blue()
        else:
            logger.info("Error: No live environment to rollback from")
            return False
    
    def get_live_environment(self) -> Optional[Deployment]:
        """Get current live environment."""
        if self.current_live == Environment.BLUE:
            return self.blue
        elif self.current_live == Environment.GREEN:
            return self.green
        return None
    
    def get_status(self) -> dict:
        """Get deployment status."""
        return {
            "blue": {
                "version": self.blue.version if self.blue else None,
                "is_live": self.blue.is_live if self.blue else False,
                "deployed_at": self.blue.deployed_at.isoformat() if self.blue else None
            },
            "green": {
                "version": self.green.version if self.green else None,
                "is_live": self.green.is_live if self.green else False,
                "deployed_at": self.green.deployed_at.isoformat() if self.green else None
            },
            "current_live": self.current_live.value if self.current_live else None
        }


def main() -> None:
    """Demonstration of Blue-Green Deployment Pattern."""
    logger.info("=" * 70)
    logger.info("BLUE-GREEN DEPLOYMENT PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Initial Deployment
    logger.info("Example 1: Initial Deployment to Blue")
    logger.info("-" * 70)
    
    deployment = BlueGreenDeployment()
    deployment.deploy_to_blue("v1.0.0")
    deployment.switch_to_blue()
    logger.info()
    
    # Example 2: Deploy New Version to Green
    logger.info("Example 2: Deploy New Version to Green")
    logger.info("-" * 70)
    
    deployment.deploy_to_green("v1.1.0")
    logger.info(f"Status: {deployment.get_status()}")
    logger.info()
    
    # Example 3: Switch to Green
    logger.info("Example 3: Switch Traffic to Green (New Version)")
    logger.info("-" * 70)
    
    deployment.switch_to_green()
    live = deployment.get_live_environment()
    logger.info(f"Live environment: {live.environment.value} (version {live.version})")
    logger.info()
    
    # Example 4: Rollback
    logger.info("Example 4: Rollback to Blue")
    logger.info("-" * 70)
    
    deployment.rollback()
    live = deployment.get_live_environment()
    logger.info(f"After rollback: {live.environment.value} (version {live.version})")
    logger.info()
    
    # Example 5: Deploy Another Version
    logger.info("Example 5: Deploy Another Version to Blue")
    logger.info("-" * 70)
    
    deployment.deploy_to_blue("v1.2.0")
    deployment.switch_to_blue()
    logger.info(f"Status: {deployment.get_status()}")
    logger.info()
    
    # Example 6: Performance measurement
    logger.info("Example 6: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Blue-Green Deployment")
    
    def deployment_operations():
        dep = BlueGreenDeployment()
        dep.deploy_to_blue("v1.0.0")
        dep.switch_to_blue()
        dep.deploy_to_green("v1.1.0")
        dep.switch_to_green()
        dep.rollback()
        return dep.get_live_environment().version
    
    result, metrics = timer.measure(deployment_operations)
    logger.info(f"Time for full blue-green cycle: {metrics['execution_time_ms']:.3f} ms")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Maintains two identical production environments (blue and green).")
    logger.info("  Only one environment is live at a time, allowing instant rollback.")
    logger.info("\nKey Advantages:")
    logger.info("  - Zero-downtime deployments")
    logger.info("  - Instant rollback")
    logger.info("  - Easy testing of new version")
    logger.info("  - Reduced deployment risk")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Requires double infrastructure")
    logger.info("  - Higher resource costs")
    logger.info("  - Database migration complexity")
    logger.info("  - State synchronization challenges")
    logger.info("\nWhen to Use:")
    logger.info("  - Zero-downtime requirements")
    logger.info("  - Critical production systems")
    logger.info("  - When rollback speed is important")
    logger.info("  - Stateless applications")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Web application deployments")
    logger.info("  - API service deployments")
    logger.info("  - Microservices deployments")
    logger.info("  - Cloud-native applications")
    logger.info("\nDeployment Flow:")
    logger.info("  1. Deploy new version to inactive environment")
    logger.info("  2. Run smoke tests")
    logger.info("  3. Switch traffic to new environment")
    logger.info("  4. Monitor for issues")
    logger.info("  5. Rollback if needed (instant)")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()