#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Log Aggregation Pattern.

Collects, centralizes, and stores logs from multiple sources for analysis,
monitoring, and troubleshooting. Essential for distributed systems observability.
"""

import sys
from pathlib import Path
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import json
import threading
from collections import deque

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


class LogLevel(Enum):
    """Log level."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class LogEntry:
    """Log entry."""
    timestamp: datetime
    level: LogLevel
    service: str
    message: str
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "level": self.level.value,
            "service": self.service,
            "message": self.message,
            "metadata": self.metadata
        }
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict())


class LogAggregator:
    """Log aggregation service."""
    
    def __init__(self, max_entries: int = 10000):
        """
        Initialize log aggregator.
        
        Args:
            max_entries: Maximum number of log entries to store
        """
        self.logs: deque = deque(maxlen=max_entries)
        self.lock = threading.Lock()
        self.filters: List[Callable] = []
    
    def add_log(self, entry: LogEntry) -> None:
        """
        Add log entry.
        
        Args:
            entry: Log entry to add
        """
        with self.lock:
            # Apply filters
            if all(filter_func(entry) for filter_func in self.filters):
                self.logs.append(entry)
    
    def add_log_entry(self, level: LogLevel, service: str, message: str, 
                     metadata: Dict = None) -> None:
        """
        Add log entry with parameters.
        
        Args:
            level: Log level
            service: Service name
            message: Log message
            metadata: Additional metadata
        """
        entry = LogEntry(
            timestamp=datetime.now(),
            level=level,
            service=service,
            message=message,
            metadata=metadata or {}
        )
        self.add_log(entry)
    
    def query_logs(self, service: Optional[str] = None,
                   level: Optional[LogLevel] = None,
                   start_time: Optional[datetime] = None,
                   end_time: Optional[datetime] = None) -> List[LogEntry]:
        """
        Query logs with filters.
        
        Args:
            service: Filter by service name
            level: Filter by log level
            start_time: Filter by start time
            end_time: Filter by end time
            
        Returns:
            List of matching log entries
        """
        with self.lock:
            results = []
            
            for entry in self.logs:
                # Service filter
                if service and entry.service != service:
                    continue
                
                # Level filter
                if level and entry.level != level:
                    continue
                
                # Time range filter
                if start_time and entry.timestamp < start_time:
                    continue
                
                if end_time and entry.timestamp > end_time:
                    continue
                
                results.append(entry)
            
            return results
    
    def get_logs_by_level(self, level: LogLevel) -> List[LogEntry]:
        """
        Get all logs of specific level.
        
        Args:
            level: Log level
            
        Returns:
            List of log entries
        """
        return self.query_logs(level=level)
    
    def get_logs_by_service(self, service: str) -> List[LogEntry]:
        """
        Get all logs from specific service.
        
        Args:
            service: Service name
            
        Returns:
            List of log entries
        """
        return self.query_logs(service=service)
    
    def get_error_logs(self) -> List[LogEntry]:
        """Get all error and critical logs."""
        with self.lock:
            return [
                entry for entry in self.logs
                if entry.level in [LogLevel.ERROR, LogLevel.CRITICAL]
            ]
    
    def add_filter(self, filter_func: Callable) -> None:
        """
        Add filter function.
        
        Args:
            filter_func: Function that takes LogEntry and returns bool
        """
        self.filters.append(filter_func)
    
    def get_statistics(self) -> Dict:
        """Get log statistics."""
        with self.lock:
            stats = {
                "total_logs": len(self.logs),
                "by_level": {},
                "by_service": {}
            }
            
            for entry in self.logs:
                # Count by level
                level = entry.level.value
                stats["by_level"][level] = stats["by_level"].get(level, 0) + 1
                
                # Count by service
                service = entry.service
                stats["by_service"][service] = stats["by_service"].get(service, 0) + 1
            
            return stats
    
    def export_logs(self, format: str = "json") -> str:
        """
        Export logs in specified format.
        
        Args:
            format: Export format (json, text)
            
        Returns:
            Exported logs as string
        """
        with self.lock:
            if format == "json":
                return json.dumps([entry.to_dict() for entry in self.logs], indent=2)
            elif format == "text":
                lines = []
                for entry in self.logs:
                    lines.append(
                        f"[{entry.timestamp.isoformat()}] "
                        f"{entry.level.value} "
                        f"[{entry.service}] "
                        f"{entry.message}"
                    )
                return "\n".join(lines)
            else:
                raise ValueError(f"Unsupported format: {format}")


class LogProducer:
    """Log producer (simulates service generating logs)."""
    
    def __init__(self, service_name: str, aggregator: LogAggregator):
        """
        Initialize log producer.
        
        Args:
            service_name: Name of the service
            aggregator: Log aggregator to send logs to
        """
        self.service_name = service_name
        self.aggregator = aggregator
    
    def log(self, level: LogLevel, message: str, metadata: Dict = None) -> None:
        """
        Generate log entry.
        
        Args:
            level: Log level
            message: Log message
            metadata: Additional metadata
        """
        self.aggregator.add_log_entry(level, self.service_name, message, metadata)
    
    def debug(self, message: str, metadata: Dict = None) -> None:
        """Log debug message."""
        self.log(LogLevel.DEBUG, message, metadata)
    
    def info(self, message: str, metadata: Dict = None) -> None:
        """Log info message."""
        self.log(LogLevel.INFO, message, metadata)
    
    def warning(self, message: str, metadata: Dict = None) -> None:
        """Log warning message."""
        self.log(LogLevel.WARNING, message, metadata)
    
    def error(self, message: str, metadata: Dict = None) -> None:
        """Log error message."""
        self.log(LogLevel.ERROR, message, metadata)
    
    def critical(self, message: str, metadata: Dict = None) -> None:
        """Log critical message."""
        self.log(LogLevel.CRITICAL, message, metadata)


def main() -> None:
    """Demonstration of Log Aggregation Pattern."""
    logger.info("=" * 70)
    logger.info("LOG AGGREGATION PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Basic Log Aggregation
    logger.info("Example 1: Basic Log Aggregation")
    logger.info("-" * 70)
    
    aggregator = LogAggregator()
    
    # Create log producers for different services
    api_service = LogProducer("api-service", aggregator)
    db_service = LogProducer("database-service", aggregator)
    cache_service = LogProducer("cache-service", aggregator)
    
    # Generate logs
    api_service.info("API server started", {"port": 8080})
    api_service.info("Handling request", {"method": "GET", "path": "/users"})
    db_service.info("Database connection established")
    db_service.warning("Slow query detected", {"query_time_ms": 1500})
    cache_service.error("Cache miss", {"key": "user:123"})
    api_service.error("Request failed", {"status_code": 500, "error": "Internal error"})
    
    logger.info(f"Total logs collected: {len(aggregator.logs)}")
    logger.info()
    
    # Example 2: Query Logs
    logger.info("Example 2: Query Logs by Service")
    logger.info("-" * 70)
    
    api_logs = aggregator.get_logs_by_service("api-service")
    logger.info(f"API service logs: {len(api_logs)}")
    for log in api_logs:
        logger.info(f"  [{log.level.value}] {log.message}")
    logger.info()
    
    # Example 3: Query by Level
    logger.info("Example 3: Query Error Logs")
    logger.info("-" * 70)
    
    error_logs = aggregator.get_error_logs()
    logger.info(f"Error/Critical logs: {len(error_logs)}")
    for log in error_logs:
        logger.info(f"  [{log.service}] {log.message}")
    logger.info()
    
    # Example 4: Statistics
    logger.info("Example 4: Log Statistics")
    logger.info("-" * 70)
    
    stats = aggregator.get_statistics()
    logger.info(f"Total logs: {stats['total_logs']}")
    logger.info("By level:")
    for level, count in stats['by_level'].items():
        logger.info(f"  {level}: {count}")
    logger.info("By service:")
    for service, count in stats['by_service'].items():
        logger.info(f"  {service}: {count}")
    logger.info()
    
    # Example 5: Time-based Query
    logger.info("Example 5: Time-based Query")
    logger.info("-" * 70)
    
    # Add more logs with time gap
    import time
    time.sleep(0.1)
    start_time = datetime.now()
    
    api_service.info("New request received")
    db_service.info("Query executed")
    
    time.sleep(0.1)
    end_time = datetime.now()
    
    recent_logs = aggregator.query_logs(start_time=start_time, end_time=end_time)
    logger.info(f"Logs between {start_time.isoformat()} and {end_time.isoformat()}: {len(recent_logs)}")
    logger.info()
    
    # Example 6: Export Logs
    logger.info("Example 6: Export Logs")
    logger.info("-" * 70)
    
    json_export = aggregator.export_logs("json")
    logger.info(f"JSON export length: {len(json_export)} characters")
    logger.info(f"First 200 chars: {json_export[:200]}...")
    logger.info()
    
    # Example 7: Performance measurement
    logger.info("Example 7: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Log Aggregation")
    
    def log_operations():
        agg = LogAggregator()
        producer = LogProducer("test-service", agg)
        
        for i in range(1000):
            producer.info(f"Log message {i}")
        
        return len(agg.logs)
    
    result, metrics = timer.measure(log_operations)
    logger.info(f"Time to process 1000 logs: {metrics['execution_time_ms']:.3f} ms")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Collects, centralizes, and stores logs from multiple sources")
    logger.info("  for analysis, monitoring, and troubleshooting.")
    logger.info("\nKey Advantages:")
    logger.info("  - Centralized log storage")
    logger.info("  - Easy search and analysis")
    logger.info("  - Correlation across services")
    logger.info("  - Historical data retention")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Storage requirements")
    logger.info("  - Network overhead")
    logger.info("  - Potential single point of failure")
    logger.info("  - Performance impact on services")
    logger.info("\nWhen to Use:")
    logger.info("  - Distributed systems")
    logger.info("  - Microservices architecture")
    logger.info("  - Multi-server deployments")
    logger.info("  - When debugging across services")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Application logging")
    logger.info("  - System monitoring")
    logger.info("  - Security auditing")
    logger.info("  - Performance analysis")
    logger.info("  - Troubleshooting")
    logger.info("\nPopular Tools:")
    logger.info("  - ELK Stack (Elasticsearch, Logstash, Kibana)")
    logger.info("  - Splunk")
    logger.info("  - Fluentd")
    logger.info("  - Loki (Grafana)")
    logger.info("  - CloudWatch Logs")
    logger.info("\nBest Practices:")
    logger.info("  - Use structured logging (JSON)")
    logger.info("  - Include correlation IDs")
    logger.info("  - Set appropriate log levels")
    logger.info("  - Implement log rotation")
    logger.info("  - Monitor log volume")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()