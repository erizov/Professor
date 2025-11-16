#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Leader Election Pattern.

Algorithm for selecting a leader among distributed nodes in a system.
Ensures only one leader exists at a time for coordination and decision-making.
"""

import sys
from pathlib import Path
from enum import Enum
from typing import List, Optional, Dict
from dataclasses import dataclass
from datetime import datetime
import threading
import time
import random

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


class NodeState(Enum):
    """Node state."""
    FOLLOWER = "follower"
    CANDIDATE = "candidate"
    LEADER = "leader"


@dataclass
class Node:
    """Distributed node."""
    node_id: str
    state: NodeState = NodeState.FOLLOWER
    term: int = 0
    votes_received: int = 0
    last_heartbeat: Optional[datetime] = None


class LeaderElection:
    """Leader election implementation using Raft-like algorithm."""
    
    def __init__(self, node_ids: List[str]):
        """
        Initialize leader election.
        
        Args:
            node_ids: List of node identifiers
        """
        self.nodes: Dict[str, Node] = {
            node_id: Node(node_id=node_id) for node_id in node_ids
        }
        self.current_leader: Optional[str] = None
        self.election_timeout = 5.0  # seconds
        self.heartbeat_interval = 1.0  # seconds
        self.running = False
        self.lock = threading.Lock()
    
    def start_election(self, candidate_id: str) -> bool:
        """
        Start election process.
        
        Args:
            candidate_id: Node starting election
            
        Returns:
            True if elected as leader
        """
        with self.lock:
            if candidate_id not in self.nodes:
                return False
            
            candidate = self.nodes[candidate_id]
            candidate.state = NodeState.CANDIDATE
            candidate.term += 1
            candidate.votes_received = 1  # Vote for self
            
            logger.info(f"Node {candidate_id} starting election (term {candidate.term})")
            
            # Request votes from other nodes
            votes_needed = (len(self.nodes) // 2) + 1
            
            for node_id, node in self.nodes.items():
                if node_id == candidate_id:
                    continue
                
                # Simulate vote (in real system, would send network request)
                if self._request_vote(node_id, candidate.term):
                    candidate.votes_received += 1
                    logger.info(f"  Node {node_id} voted for {candidate_id}")
            
            # Check if majority
            if candidate.votes_received >= votes_needed:
                self._become_leader(candidate_id)
                return True
            else:
                candidate.state = NodeState.FOLLOWER
                logger.info(f"  Election failed: {candidate.votes_received}/{votes_needed} votes")
                return False
    
    def _request_vote(self, node_id: str, term: int) -> bool:
        """
        Request vote from node.
        
        Args:
            node_id: Node to request vote from
            term: Election term
            
        Returns:
            True if vote granted
        """
        node = self.nodes[node_id]
        
        # Grant vote if term is higher and node is not already leader
        if term > node.term and node.state != NodeState.LEADER:
            node.term = term
            node.state = NodeState.FOLLOWER
            return True
        
        return False
    
    def _become_leader(self, node_id: str) -> None:
        """
        Node becomes leader.
        
        Args:
            node_id: Node becoming leader
        """
        with self.lock:
            # Demote current leader if exists
            if self.current_leader and self.current_leader != node_id:
                old_leader = self.nodes[self.current_leader]
                old_leader.state = NodeState.FOLLOWER
                logger.info(f"  Node {self.current_leader} demoted from leader")
            
            # Promote new leader
            leader = self.nodes[node_id]
            leader.state = NodeState.LEADER
            self.current_leader = node_id
            
            logger.info(f"  Node {node_id} elected as leader (term {leader.term})")
    
    def send_heartbeat(self, leader_id: str) -> None:
        """
        Send heartbeat from leader to followers.
        
        Args:
            leader_id: Leader node ID
        """
        with self.lock:
            if leader_id not in self.nodes:
                return
            
            leader = self.nodes[leader_id]
            if leader.state != NodeState.LEADER:
                return
            
            current_time = datetime.now()
            
            for node_id, node in self.nodes.items():
                if node_id != leader_id:
                    node.last_heartbeat = current_time
                    node.term = leader.term
                    if node.state != NodeState.FOLLOWER:
                        node.state = NodeState.FOLLOWER
    
    def check_leader_timeout(self, node_id: str) -> bool:
        """
        Check if leader heartbeat timeout occurred.
        
        Args:
            node_id: Node to check
            
        Returns:
            True if timeout occurred
        """
        with self.lock:
            if node_id not in self.nodes:
                return False
            
            node = self.nodes[node_id]
            
            if node.state == NodeState.LEADER:
                return False
            
            if node.last_heartbeat is None:
                return True
            
            elapsed = (datetime.now() - node.last_heartbeat).total_seconds()
            return elapsed > self.election_timeout
    
    def get_leader(self) -> Optional[str]:
        """Get current leader."""
        with self.lock:
            return self.current_leader
    
    def get_status(self) -> Dict:
        """Get election status."""
        with self.lock:
            return {
                "current_leader": self.current_leader,
                "nodes": {
                    node_id: {
                        "state": node.state.value,
                        "term": node.term,
                        "votes": node.votes_received
                    }
                    for node_id, node in self.nodes.items()
                }
            }


def main() -> None:
    """Demonstration of Leader Election Pattern."""
    logger.info("=" * 70)
    logger.info("LEADER ELECTION PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Initial Election
    logger.info("Example 1: Initial Leader Election")
    logger.info("-" * 70)
    
    nodes = ["node1", "node2", "node3", "node4", "node5"]
    election = LeaderElection(nodes)
    
    # Node 1 starts election
    elected = election.start_election("node1")
    logger.info(f"Election result: {'Success' if elected else 'Failed'}")
    logger.info(f"Current leader: {election.get_leader()}")
    logger.info()
    
    # Example 2: Leader Heartbeat
    logger.info("Example 2: Leader Sending Heartbeat")
    logger.info("-" * 70)
    
    if election.get_leader():
        election.send_heartbeat(election.get_leader())
        logger.info("Heartbeat sent to all followers")
        logger.info(f"Status: {election.get_status()}")
    logger.info()
    
    # Example 3: Leader Failure and Re-election
    logger.info("Example 3: Leader Failure and Re-election")
    logger.info("-" * 70)
    
    # Simulate leader failure (remove heartbeat)
    leader_id = election.get_leader()
    if leader_id:
        # Manually set last_heartbeat to None to simulate failure
        with election.lock:
            for node in election.nodes.values():
                node.last_heartbeat = None
        
        # Node 2 detects timeout and starts election
        if election.check_leader_timeout("node2"):
            logger.info(f"Node 2 detected leader timeout, starting election...")
            elected = election.start_election("node2")
            logger.info(f"New leader: {election.get_leader()}")
    logger.info()
    
    # Example 4: Multiple Concurrent Elections
    logger.info("Example 4: Multiple Concurrent Elections (Split Vote)")
    logger.info("-" * 70)
    
    election2 = LeaderElection(["node1", "node2", "node3"])
    
    # Two nodes start election simultaneously
    result1 = election2.start_election("node1")
    result2 = election2.start_election("node2")
    
    logger.info(f"Node 1 election: {'Success' if result1 else 'Failed'}")
    logger.info(f"Node 2 election: {'Success' if result2 else 'Failed'}")
    logger.info(f"Final leader: {election2.get_leader()}")
    logger.info()
    
    # Example 5: Performance measurement
    logger.info("Example 5: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Leader Election")
    
    def election_operations():
        nodes = [f"node{i}" for i in range(1, 6)]
        election = LeaderElection(nodes)
        election.start_election("node1")
        election.send_heartbeat("node1")
        return election.get_leader()
    
    result, metrics = timer.measure(election_operations)
    logger.info(f"Time for leader election: {metrics['execution_time_ms']:.3f} ms")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Algorithm for selecting a leader among distributed nodes.")
    logger.info("  Ensures only one leader exists at a time for coordination.")
    logger.info("\nKey Advantages:")
    logger.info("  - Single point of coordination")
    logger.info("  - Prevents split-brain scenarios")
    logger.info("  - Automatic failover")
    logger.info("  - Consensus-based selection")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Single point of failure (mitigated by re-election)")
    logger.info("  - Network overhead for heartbeats")
    logger.info("  - Election can cause temporary unavailability")
    logger.info("  - Complexity in implementation")
    logger.info("\nWhen to Use:")
    logger.info("  - Distributed systems requiring coordination")
    logger.info("  - Master-slave architectures")
    logger.info("  - Consensus algorithms (Raft, Paxos)")
    logger.info("  - Cluster management")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Database replication (primary/secondary)")
    logger.info("  - Distributed locks")
    logger.info("  - Service discovery")
    logger.info("  - Configuration management")
    logger.info("  - Load balancer coordination")
    logger.info("\nLeader Election Algorithms:")
    logger.info("  - Raft: Leader election with log replication")
    logger.info("  - Paxos: Consensus algorithm")
    logger.info("  - Bully: Highest ID wins")
    logger.info("  - Ring: Token passing")
    logger.info("\nImplementation Considerations:")
    logger.info("  - Use majority voting to prevent split-brain")
    logger.info("  - Implement heartbeat mechanism")
    logger.info("  - Handle network partitions")
    logger.info("  - Use timeouts for failure detection")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()