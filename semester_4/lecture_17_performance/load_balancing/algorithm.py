#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Load Balancing Pattern.

Distributes incoming requests across multiple servers to optimize
resource utilization, maximize throughput, and minimize response time.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass
from enum import Enum
import random
import time

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


class LoadBalancingStrategy(Enum):
    """Load balancing strategies."""
    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    RANDOM = "random"
    IP_HASH = "ip_hash"


@dataclass
class Server:
    """Server representation."""
    id: str
    address: str
    weight: int = 1
    active_connections: int = 0
    is_healthy: bool = True
    
    def __str__(self) -> str:
        return f"Server({self.id}, connections={self.active_connections}, healthy={self.is_healthy})"


class LoadBalancer(ABC):
    """Abstract load balancer."""
    
    def __init__(self, servers: List[Server]):
        """
        Initialize load balancer.
        
        Args:
            servers: List of servers
        """
        self.servers = servers
        self.current_index = 0
    
    @abstractmethod
    def select_server(self, client_ip: str = None) -> Optional[Server]:
        """
        Select server for request.
        
        Args:
            client_ip: Client IP address (for IP hash strategy)
            
        Returns:
            Selected server or None if no healthy servers
        """
        pass
    
    def get_healthy_servers(self) -> List[Server]:
        """Get list of healthy servers."""
        return [s for s in self.servers if s.is_healthy]
    
    def mark_server_unhealthy(self, server_id: str) -> None:
        """Mark server as unhealthy."""
        for server in self.servers:
            if server.id == server_id:
                server.is_healthy = False
    
    def mark_server_healthy(self, server_id: str) -> None:
        """Mark server as healthy."""
        for server in self.servers:
            if server.id == server_id:
                server.is_healthy = True


class RoundRobinLoadBalancer(LoadBalancer):
    """Round-robin load balancer."""
    
    def select_server(self, client_ip: str = None) -> Optional[Server]:
        """Select server using round-robin."""
        healthy = self.get_healthy_servers()
        if not healthy:
            return None
        
        server = healthy[self.current_index % len(healthy)]
        self.current_index += 1
        return server


class LeastConnectionsLoadBalancer(LoadBalancer):
    """Least connections load balancer."""
    
    def select_server(self, client_ip: str = None) -> Optional[Server]:
        """Select server with least connections."""
        healthy = self.get_healthy_servers()
        if not healthy:
            return None
        
        return min(healthy, key=lambda s: s.active_connections)


class WeightedRoundRobinLoadBalancer(LoadBalancer):
    """Weighted round-robin load balancer."""
    
    def __init__(self, servers: List[Server]):
        super().__init__(servers)
        self.current_weight = 0
        self.gcd = self._calculate_gcd([s.weight for s in servers])
        self.max_weight = max(s.weight for s in servers) if servers else 0
    
    def _calculate_gcd(self, weights: List[int]) -> int:
        """Calculate greatest common divisor."""
        def gcd(a: int, b: int) -> int:
            while b:
                a, b = b, a % b
            return a
        
        result = weights[0] if weights else 1
        for w in weights[1:]:
            result = gcd(result, w)
        return result
    
    def select_server(self, client_ip: str = None) -> Optional[Server]:
        """Select server using weighted round-robin."""
        healthy = self.get_healthy_servers()
        if not healthy:
            return None
        
        while True:
            self.current_index = (self.current_index + 1) % len(healthy)
            if self.current_index == 0:
                self.current_weight -= self.gcd
                if self.current_weight <= 0:
                    self.current_weight = self.max_weight
            
            if healthy[self.current_index].weight >= self.current_weight:
                return healthy[self.current_index]


class RandomLoadBalancer(LoadBalancer):
    """Random load balancer."""
    
    def select_server(self, client_ip: str = None) -> Optional[Server]:
        """Select random server."""
        healthy = self.get_healthy_servers()
        if not healthy:
            return None
        
        return random.choice(healthy)


class IPHashLoadBalancer(LoadBalancer):
    """IP hash load balancer."""
    
    def select_server(self, client_ip: str = None) -> Optional[Server]:
        """Select server based on IP hash."""
        healthy = self.get_healthy_servers()
        if not healthy:
            return None
        
        if client_ip is None:
            client_ip = "0.0.0.0"
        
        # Simple hash function
        hash_value = hash(client_ip)
        index = abs(hash_value) % len(healthy)
        return healthy[index]


class LoadBalancerFactory:
    """Factory for creating load balancers."""
    
    @staticmethod
    def create(strategy: LoadBalancingStrategy, servers: List[Server]) -> LoadBalancer:
        """Create load balancer with specified strategy."""
        if strategy == LoadBalancingStrategy.ROUND_ROBIN:
            return RoundRobinLoadBalancer(servers)
        elif strategy == LoadBalancingStrategy.LEAST_CONNECTIONS:
            return LeastConnectionsLoadBalancer(servers)
        elif strategy == LoadBalancingStrategy.WEIGHTED_ROUND_ROBIN:
            return WeightedRoundRobinLoadBalancer(servers)
        elif strategy == LoadBalancingStrategy.RANDOM:
            return RandomLoadBalancer(servers)
        elif strategy == LoadBalancingStrategy.IP_HASH:
            return IPHashLoadBalancer(servers)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")


def main() -> None:
    """Demonstration of Load Balancing Pattern."""
    logger.info("=" * 70)
    logger.info("LOAD BALANCING PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Round-Robin Load Balancing
    logger.info("Example 1: Round-Robin Load Balancing")
    logger.info("-" * 70)
    
    servers = [
        Server("server1", "192.168.1.1"),
        Server("server2", "192.168.1.2"),
        Server("server3", "192.168.1.3"),
    ]
    
    lb = RoundRobinLoadBalancer(servers)
    
    logger.info("Distributing 10 requests:")
    for i in range(10):
        server = lb.select_server()
        server.active_connections += 1
        logger.info(f"  Request {i+1} -> {server.id} (connections: {server.active_connections})")
    logger.info()
    
    # Example 2: Least Connections
    logger.info("Example 2: Least Connections Load Balancing")
    logger.info("-" * 70)
    
    servers = [
        Server("server1", "192.168.1.1", active_connections=5),
        Server("server2", "192.168.1.2", active_connections=2),
        Server("server3", "192.168.1.3", active_connections=8),
    ]
    
    lb = LeastConnectionsLoadBalancer(servers)
    
    logger.info("Distributing 5 requests:")
    for i in range(5):
        server = lb.select_server()
        server.active_connections += 1
        logger.info(f"  Request {i+1} -> {server.id} (connections: {server.active_connections})")
    logger.info()
    
    # Example 3: Weighted Round-Robin
    logger.info("Example 3: Weighted Round-Robin Load Balancing")
    logger.info("-" * 70)
    
    servers = [
        Server("server1", "192.168.1.1", weight=3),
        Server("server2", "192.168.1.2", weight=2),
        Server("server3", "192.168.1.3", weight=1),
    ]
    
    lb = WeightedRoundRobinLoadBalancer(servers)
    
    logger.info("Distributing 12 requests (weights: 3, 2, 1):")
    distribution = {}
    for i in range(12):
        server = lb.select_server()
        distribution[server.id] = distribution.get(server.id, 0) + 1
        logger.info(f"  Request {i+1} -> {server.id}")
    
    logger.info("\nDistribution summary:")
    for server_id, count in distribution.items():
        logger.info(f"  {server_id}: {count} requests")
    logger.info()
    
    # Example 4: Health Checks
    logger.info("Example 4: Health Checks and Failover")
    logger.info("-" * 70)
    
    servers = [
        Server("server1", "192.168.1.1"),
        Server("server2", "192.168.1.2"),
        Server("server3", "192.168.1.3"),
    ]
    
    lb = RoundRobinLoadBalancer(servers)
    
    logger.info("Marking server2 as unhealthy:")
    lb.mark_server_unhealthy("server2")
    
    logger.info("Distributing 6 requests:")
    for i in range(6):
        server = lb.select_server()
        if server:
            logger.info(f"  Request {i+1} -> {server.id}")
        else:
            logger.info(f"  Request {i+1} -> No healthy servers")
    logger.info()
    
    # Example 5: Performance measurement
    logger.info("Example 5: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Load Balancing")
    
    def load_balancing_operations():
        servers = [Server(f"server{i}", f"192.168.1.{i}") for i in range(1, 11)]
        lb = RoundRobinLoadBalancer(servers)
        
        for _ in range(1000):
            server = lb.select_server()
            if server:
                server.active_connections += 1
        
        return sum(s.active_connections for s in servers)
    
    result, metrics = timer.measure(load_balancing_operations)
    logger.info(f"Time to distribute 1000 requests: {metrics['execution_time_ms']:.3f} ms")
    logger.info(f"Total connections: {result}")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Distributes incoming requests across multiple servers to")
    logger.info("  optimize resource utilization, maximize throughput, and")
    logger.info("  minimize response time.")
    logger.info("\nKey Advantages:")
    logger.info("  - Improved performance")
    logger.info("  - High availability")
    logger.info("  - Scalability")
    logger.info("  - Fault tolerance")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Additional infrastructure")
    logger.info("  - Session affinity challenges")
    logger.info("  - Configuration complexity")
    logger.info("  - Single point of failure (if not redundant)")
    logger.info("\nWhen to Use:")
    logger.info("  - Multiple server instances")
    logger.info("  - High traffic applications")
    logger.info("  - Need for high availability")
    logger.info("  - Horizontal scaling")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Web servers")
    logger.info("  - Application servers")
    logger.info("  - Database servers")
    logger.info("  - API gateways")
    logger.info("\nLoad Balancing Strategies:")
    logger.info("  - Round-Robin: Distribute sequentially")
    logger.info("  - Least Connections: Choose server with fewest connections")
    logger.info("  - Weighted Round-Robin: Distribute based on server capacity")
    logger.info("  - Random: Random selection")
    logger.info("  - IP Hash: Consistent hashing based on client IP")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()