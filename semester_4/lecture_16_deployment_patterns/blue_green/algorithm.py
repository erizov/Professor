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
        print(f"Deployed version {version} to BLUE environment")
        return self.blue
    
    def deploy_to_green(self, version: str) -> Deployment:
        """Deploy to green environment."""
        self.green = Deployment(
            environment=Environment.GREEN,
            version=version,
            deployed_at=datetime.now(),
            is_live=False
        )
        print(f"Deployed version {version} to GREEN environment")
        return self.green
    
    def switch_to_blue(self) -> bool:
        """Switch traffic to blue environment."""
        if not self.blue:
            print("Error: Blue environment not deployed")
            return False
        
        # Deactivate current live environment
        if self.current_live == Environment.GREEN and self.green:
            self.green.is_live = False
            print("Deactivated GREEN environment")
        
        # Activate blue
        self.blue.is_live = True
        self.current_live = Environment.BLUE
        print(f"Switched traffic to BLUE environment (version {self.blue.version})")
        return True
    
    def switch_to_green(self) -> bool:
        """Switch traffic to green environment."""
        if not self.green:
            print("Error: Green environment not deployed")
            return False
        
        # Deactivate current live environment
        if self.current_live == Environment.BLUE and self.blue:
            self.blue.is_live = False
            print("Deactivated BLUE environment")
        
        # Activate green
        self.green.is_live = True
        self.current_live = Environment.GREEN
        print(f"Switched traffic to GREEN environment (version {self.green.version})")
        return True
    
    def rollback(self) -> bool:
        """Rollback to previous environment."""
        if self.current_live == Environment.BLUE:
            return self.switch_to_green()
        elif self.current_live == Environment.GREEN:
            return self.switch_to_blue()
        else:
            print("Error: No live environment to rollback from")
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
    print("=" * 70)
    print("BLUE-GREEN DEPLOYMENT PATTERN DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Initial Deployment
    print("Example 1: Initial Deployment to Blue")
    print("-" * 70)
    
    deployment = BlueGreenDeployment()
    deployment.deploy_to_blue("v1.0.0")
    deployment.switch_to_blue()
    print()
    
    # Example 2: Deploy New Version to Green
    print("Example 2: Deploy New Version to Green")
    print("-" * 70)
    
    deployment.deploy_to_green("v1.1.0")
    print(f"Status: {deployment.get_status()}")
    print()
    
    # Example 3: Switch to Green
    print("Example 3: Switch Traffic to Green (New Version)")
    print("-" * 70)
    
    deployment.switch_to_green()
    live = deployment.get_live_environment()
    print(f"Live environment: {live.environment.value} (version {live.version})")
    print()
    
    # Example 4: Rollback
    print("Example 4: Rollback to Blue")
    print("-" * 70)
    
    deployment.rollback()
    live = deployment.get_live_environment()
    print(f"After rollback: {live.environment.value} (version {live.version})")
    print()
    
    # Example 5: Deploy Another Version
    print("Example 5: Deploy Another Version to Blue")
    print("-" * 70)
    
    deployment.deploy_to_blue("v1.2.0")
    deployment.switch_to_blue()
    print(f"Status: {deployment.get_status()}")
    print()
    
    # Example 6: Performance measurement
    print("Example 6: Performance Measurement")
    print("-" * 70)
    
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
    print(f"Time for full blue-green cycle: {metrics['execution_time_ms']:.3f} ms")
    print()
    
    print("=" * 70)
    print("\nPattern Summary:")
    print("\nIntent:")
    print("  Maintains two identical production environments (blue and green).")
    print("  Only one environment is live at a time, allowing instant rollback.")
    print("\nKey Advantages:")
    print("  - Zero-downtime deployments")
    print("  - Instant rollback")
    print("  - Easy testing of new version")
    print("  - Reduced deployment risk")
    print("\nKey Disadvantages:")
    print("  - Requires double infrastructure")
    print("  - Higher resource costs")
    print("  - Database migration complexity")
    print("  - State synchronization challenges")
    print("\nWhen to Use:")
    print("  - Zero-downtime requirements")
    print("  - Critical production systems")
    print("  - When rollback speed is important")
    print("  - Stateless applications")
    print("\nCommon Use Cases:")
    print("  - Web application deployments")
    print("  - API service deployments")
    print("  - Microservices deployments")
    print("  - Cloud-native applications")
    print("\nDeployment Flow:")
    print("  1. Deploy new version to inactive environment")
    print("  2. Run smoke tests")
    print("  3. Switch traffic to new environment")
    print("  4. Monitor for issues")
    print("  5. Rollback if needed (instant)")
    print("=" * 70)


if __name__ == "__main__":
    main()
