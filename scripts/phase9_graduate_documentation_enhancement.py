#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 9: Graduate Documentation Enhancement
Enhance documentation for 100+ additional graduate-level files
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json

ROOT = Path(__file__).resolve().parents[1]


# Expanded descriptions for graduate-level topics
EXPANDED_GRADUATE_DESCRIPTIONS: Dict[str, str] = {
    # Operating Systems
    "microkernel_architecture": "Microkernel architecture is an operating system design where the kernel provides minimal services (IPC, memory management, scheduling) while most functionality runs in user space. Solves problems of system reliability, security, and modularity. Example: QNX and MINIX use microkernels where device drivers run as separate user processes. Works by keeping kernel minimal, moving services to user space, and using message passing for communication between components.",
    "exokernel_design": "Exokernel is an operating system architecture that provides minimal abstractions, allowing applications to manage hardware resources directly. Solves problems of performance overhead and flexibility limitations in traditional kernels. Example: ExOS exokernel lets applications implement their own file systems and network protocols. Works by exposing hardware resources directly to applications while the kernel only ensures protection and multiplexing.",
    "real_time_systems": "Real-time systems guarantee response within strict time constraints, either hard (failure if deadline missed) or soft (degraded performance). Solves problems of time-critical applications like avionics, medical devices, and industrial control. Example: Flight control systems must respond to sensor inputs within milliseconds. Works by using priority-based scheduling, interrupt handling, and deterministic algorithms to meet deadlines.",
    "container_runtimes": "Container runtimes manage the lifecycle of containers, providing isolation and resource management. Solves problems of application portability and resource efficiency. Example: Docker uses containerd runtime to manage container creation, execution, and deletion. Works by leveraging OS features (cgroups, namespaces) to isolate processes and manage resources.",
    "cpu_scheduling_advanced": "Advanced CPU scheduling algorithms optimize processor allocation for different workloads and priorities. Solves problems of fairness, throughput, and response time in multi-core systems. Example: Linux CFS (Completely Fair Scheduler) uses red-black trees to ensure fair CPU time distribution. Works by tracking process execution time, calculating virtual runtime, and selecting processes with least virtual runtime.",
    "memory_optimization": "Memory optimization techniques reduce memory usage and improve cache performance. Solves problems of memory pressure and cache misses in high-performance systems. Example: Memory pooling reuses allocated blocks to reduce fragmentation. Works by pre-allocating memory pools, tracking free blocks, and reusing memory instead of frequent allocation/deallocation.",
    # Concurrency
    "actor_model": "Actor model is a concurrency paradigm where actors are independent entities that communicate through asynchronous messages. Solves problems of shared state and race conditions in concurrent systems. Example: Erlang and Akka use actors where each actor processes messages sequentially. Works by encapsulating state in actors, sending immutable messages, and processing messages one at a time per actor.",
    "lock_free_data_structures": "Lock-free data structures use atomic operations instead of locks to ensure thread safety. Solves problems of lock contention and deadlocks in high-concurrency systems. Example: Lock-free queues use compare-and-swap (CAS) operations for enqueue/dequeue. Works by using atomic operations (CAS, fetch-and-add) to modify shared data without locks.",
    "transactional_memory": "Transactional memory provides atomic blocks for memory operations, similar to database transactions. Solves problems of deadlocks and lock granularity in concurrent programming. Example: Intel TSX provides hardware transactional memory support. Works by tracking memory accesses in a transaction, executing atomically, and rolling back on conflicts.",
    "wait_free_algorithms": "Wait-free algorithms guarantee that every thread completes its operation in a bounded number of steps regardless of other threads. Solves problems of starvation and unbounded delays in concurrent systems. Example: Wait-free queues ensure all operations complete in O(1) steps. Works by using atomic operations and helping mechanisms where threads assist each other.",
    # Distributed Systems
    "consensus_algorithms": "Consensus algorithms enable distributed systems to agree on a single value despite failures. Solves problems of coordination and agreement in distributed systems. Example: Raft and Paxos ensure all nodes agree on log entries in distributed databases. Works by electing a leader, replicating operations, and achieving majority agreement.",
    "vector_clocks": "Vector clocks track causal relationships between events in distributed systems. Solves problems of determining event ordering without global clocks. Example: Distributed databases use vector clocks to detect concurrent updates. Works by maintaining a vector of logical clocks, one per node, and updating on message send/receive.",
    "crdt": "Conflict-free Replicated Data Types (CRDTs) are data structures that can be replicated and merged without conflicts. Solves problems of consistency in eventually consistent distributed systems. Example: G-Set (grow-only set) and LWW-Register (last-write-wins) are CRDTs. Works by designing operations to be commutative and associative, enabling safe merging.",
    "byzantine_fault_tolerance": "Byzantine fault tolerance handles arbitrary failures including malicious behavior. Solves problems of security and reliability in untrusted environments. Example: Blockchain uses BFT to reach consensus despite malicious nodes. Works by requiring 2/3 majority agreement and using cryptographic signatures to prevent tampering.",
    "eventual_consistency": "Eventual consistency guarantees that if no updates occur, all replicas will eventually converge to the same state. Solves problems of availability and partition tolerance in distributed systems. Example: DNS and Amazon DynamoDB use eventual consistency. Works by allowing temporary inconsistencies, propagating updates asynchronously, and resolving conflicts using conflict resolution strategies.",
    # Cloud Native
    "service_mesh": "Service mesh provides infrastructure layer for service-to-service communication with observability and security. Solves problems of managing microservices communication, security, and observability. Example: Istio and Linkerd provide service mesh with traffic management, security policies, and metrics. Works by deploying sidecar proxies that intercept and manage all service communication.",
    "serverless_architecture": "Serverless architecture runs code without managing servers, with automatic scaling and pay-per-use pricing. Solves problems of server management and cost optimization. Example: AWS Lambda executes functions in response to events. Works by abstracting infrastructure, auto-scaling based on demand, and charging only for execution time.",
    "function_as_service": "Function-as-a-Service (FaaS) is a serverless computing model where functions are deployed and executed on-demand. Solves problems of infrastructure management and cost efficiency. Example: AWS Lambda, Azure Functions, and Google Cloud Functions are FaaS platforms. Works by packaging code as functions, triggering on events, and executing in isolated containers.",
    "container_orchestration": "Container orchestration automates deployment, scaling, and management of containerized applications. Solves problems of managing containers at scale. Example: Kubernetes orchestrates containers across clusters. Works by maintaining desired state, scheduling containers, monitoring health, and auto-scaling based on metrics.",
    # Observability
    "distributed_tracing": "Distributed tracing tracks requests across multiple services to understand system behavior. Solves problems of debugging and performance analysis in microservices. Example: OpenTelemetry and Jaeger trace requests through multiple services. Works by generating trace IDs, propagating context, and collecting spans with timing and metadata.",
    "metrics_collection": "Metrics collection gathers quantitative measurements about system performance and behavior. Solves problems of monitoring and alerting in production systems. Example: Prometheus collects metrics and stores them as time series. Works by exposing metrics endpoints, scraping at intervals, and storing in time-series database.",
    "apm": "Application Performance Monitoring (APM) tracks application performance and user experience. Solves problems of identifying performance bottlenecks and errors. Example: New Relic and Datadog provide APM with transaction tracing and error tracking. Works by instrumenting applications, collecting performance data, and providing dashboards and alerts.",
    "chaos_engineering_advanced": "Advanced chaos engineering systematically tests system resilience by injecting failures. Solves problems of discovering weaknesses before production incidents. Example: Netflix Chaos Monkey randomly terminates instances to test resilience. Works by injecting controlled failures, observing system behavior, and validating recovery mechanisms.",
    # Data Engineering
    "data_mesh": "Data mesh is a decentralized data architecture where data is treated as a product. Solves problems of data silos and centralized bottlenecks. Example: Data mesh organizes data by domain with self-serve infrastructure. Works by decentralizing data ownership, treating data as products, and providing self-serve data infrastructure.",
    "stream_processing_advanced": "Advanced stream processing handles continuous data streams in real-time. Solves problems of processing high-volume, high-velocity data. Example: Apache Kafka Streams and Apache Flink process millions of events per second. Works by processing events as they arrive, using windowing for aggregations, and maintaining state for joins.",
    "lambda_architecture": "Lambda architecture combines batch and stream processing for comprehensive data processing. Solves problems of both historical and real-time data analysis. Example: Lambda architecture uses Hadoop for batch and Kafka for streaming. Works by processing data in batch layer (complete accuracy) and speed layer (low latency), then merging results.",
    "batch_processing_advanced": "Advanced batch processing handles large-scale data processing jobs efficiently. Solves problems of processing terabytes of data. Example: Apache Spark processes large datasets in parallel across clusters. Works by dividing data into partitions, processing in parallel, and aggregating results.",
    # LLM & AI
    "transformer_optimization": "Transformer optimization improves efficiency of transformer models through various techniques. Solves problems of computational cost and memory usage. Example: Flash Attention reduces memory from O(n²) to O(n). Works by computing attention in blocks, using tiling, and avoiding full attention matrix storage.",
    "llm_compression": "LLM compression reduces model size while maintaining performance. Solves problems of model deployment and inference cost. Example: Quantization reduces model size by using lower precision (INT8 instead of FP32). Works by reducing precision, pruning unimportant weights, and distilling knowledge to smaller models.",
    "fine_tuning_llm": "Fine-tuning adapts pre-trained language models to specific tasks or domains. Solves problems of task-specific adaptation without training from scratch. Example: Fine-tuning BERT on medical texts for clinical question answering. Works by continuing training on domain-specific data with lower learning rates.",
    "rag_advanced": "Advanced Retrieval-Augmented Generation combines retrieval with generation for accurate responses. Solves problems of factual accuracy and knowledge updates. Example: RAG retrieves relevant documents, then generates answers using retrieved context. Works by embedding queries, searching vector databases, retrieving top-k documents, and conditioning generation.",
    # Databases
    "query_optimization": "Query optimization improves database query performance through indexing and execution planning. Solves problems of slow queries and high database load. Example: PostgreSQL query planner chooses optimal join order and index usage. Works by analyzing query structure, estimating costs, generating execution plans, and selecting most efficient plan.",
    "database_sharding": "Database sharding horizontally partitions data across multiple databases. Solves problems of database scalability and performance. Example: User data sharded by user_id across 10 database servers. Works by determining shard key, routing queries to appropriate shards, and managing data distribution.",
    "index_optimization": "Index optimization improves query performance through strategic index design. Solves problems of slow queries and high I/O. Example: Composite indexes on (user_id, created_at) optimize queries filtering on both columns. Works by creating indexes on frequently queried columns, using covering indexes, and maintaining index statistics.",
}


def find_graduate_readme_files() -> List[Path]:
    """Find README files in graduate semesters (9-16)."""
    readme_files = []
    for readme_path in ROOT.rglob("**/README.md"):
        if "supporting_documents" in str(readme_path):
            continue
        if readme_path.name == "README.md" and readme_path.parent.name != "Professor":
            # Check if in graduate semester (9-16)
            path_str = str(readme_path.relative_to(ROOT))
            if any(f"semester_{i}" in path_str for i in range(9, 17)):
                readme_files.append(readme_path)
    return readme_files


def has_generic_content(content: str) -> bool:
    """Check if README has generic placeholder content."""
    generic_phrases = [
        "works by systematically processing",
        "Core principle: [Describe main idea]",
        "Data structures used: [List structures]",
        "Termination condition: [When algorithm stops]",
        "Addresses advanced computational challenges",
        "This topic covers advanced techniques",
        "The algorithm works by systematically",
        "This technique is used for",
    ]
    return any(phrase in content for phrase in generic_phrases)


def get_description(algorithm_name: str, lecture_name: str) -> Optional[str]:
    """Get specific description for algorithm."""
    algo_lower = algorithm_name.lower()
    lecture_lower = lecture_name.lower()

    # Try exact match
    description = EXPANDED_GRADUATE_DESCRIPTIONS.get(algorithm_name)
    if description:
        return description

    # Try partial match
    for key, desc in EXPANDED_GRADUATE_DESCRIPTIONS.items():
        if key in algo_lower or algo_lower in key:
            return desc

    # Try lecture-based matching
    if "os" in lecture_lower or "operating" in lecture_lower:
        if "microkernel" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("microkernel_architecture")
        elif "exokernel" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("exokernel_design")
        elif "real" in algo_lower and "time" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("real_time_systems")
        elif "container" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("container_runtimes")
        elif "scheduling" in algo_lower or "cpu" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("cpu_scheduling_advanced")
        elif "memory" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("memory_optimization")

    elif "concurrency" in lecture_lower:
        if "actor" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("actor_model")
        elif "lock" in algo_lower and "free" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("lock_free_data_structures")
        elif "transactional" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("transactional_memory")
        elif "wait" in algo_lower and "free" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("wait_free_algorithms")

    elif "distributed" in lecture_lower:
        if "consensus" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("consensus_algorithms")
        elif "vector" in algo_lower or "clock" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("vector_clocks")
        elif "crdt" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("crdt")
        elif "byzantine" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("byzantine_fault_tolerance")
        elif "eventual" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("eventual_consistency")

    elif "cloud" in lecture_lower or "native" in lecture_lower:
        if "service" in algo_lower and "mesh" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("service_mesh")
        elif "serverless" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("serverless_architecture")
        elif "function" in algo_lower or "faas" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("function_as_service")
        elif "container" in algo_lower and "orchestration" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("container_orchestration")

    elif "observability" in lecture_lower or "monitoring" in lecture_lower:
        if "tracing" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("distributed_tracing")
        elif "metric" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("metrics_collection")
        elif "apm" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("apm")
        elif "chaos" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("chaos_engineering_advanced")

    elif "data" in lecture_lower and "engineering" in lecture_lower:
        if "mesh" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("data_mesh")
        elif "stream" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("stream_processing_advanced")
        elif "lambda" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("lambda_architecture")
        elif "batch" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("batch_processing_advanced")

    elif "llm" in lecture_lower or "ai" in lecture_lower:
        if "optimization" in algo_lower or "transformer" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("transformer_optimization")
        elif "compression" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("llm_compression")
        elif "fine" in algo_lower or "tuning" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("fine_tuning_llm")
        elif "rag" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("rag_advanced")

    elif "database" in lecture_lower or "sql" in lecture_lower:
        if "optimization" in algo_lower or "query" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("query_optimization")
        elif "sharding" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("database_sharding")
        elif "index" in algo_lower:
            return EXPANDED_GRADUATE_DESCRIPTIONS.get("index_optimization")

    return None


def enhance_short_description(
    readme_path: Path, algorithm_name: str, lecture_name: str
) -> bool:
    """Enhance short description with specific content."""
    try:
        content = readme_path.read_text(encoding="utf-8")

        # Get specific description
        description = get_description(algorithm_name, lecture_name)
        if not description:
            return False

        # Extract first sentence for short description
        short_desc = (
            description.split(".")[0] + "." if "." in description else description
        )

        # Find Short Description section
        short_desc_pattern = r"(### Short Description\s*\n\s*\n)(.*?)(?=\n##|\n###|\Z)"
        match = re.search(short_desc_pattern, content, re.DOTALL)

        if match:
            existing_desc = match.group(2).strip()

            # Check if it's generic or too short (be more lenient)
            if has_generic_content(existing_desc) or len(existing_desc) < 150:
                # Replace with specific description
                content = (
                    content[: match.start(2)]
                    + short_desc
                    + "\n\n"
                    + content[match.end(2) :]
                )
                readme_path.write_text(content, encoding="utf-8")
                return True

        return False
    except Exception as e:
        print(f"Error processing {readme_path}: {e}")
        return False


def enhance_introduction(
    readme_path: Path, algorithm_name: str, lecture_name: str
) -> bool:
    """Enhance introduction with specific content."""
    try:
        content = readme_path.read_text(encoding="utf-8")

        # Get specific description
        description = get_description(algorithm_name, lecture_name)
        if not description:
            return False

        # Find Introduction section
        intro_pattern = r"(## Introduction\s*\n\s*\n)(.*?)(?=\n##|\n###|\Z)"
        match = re.search(intro_pattern, content, re.DOTALL)

        if match:
            existing_intro = match.group(2).strip()

            # Check if it's generic (be more lenient)
            if has_generic_content(existing_intro) or len(existing_intro) < 200:
                # Create enhanced introduction
                enhanced_intro = (
                    description
                    + "\n\n"
                    + f"This advanced topic is essential for understanding modern {algorithm_name.replace('_', ' ')} "
                    f"systems and their applications in production environments. "
                    f"Mastery of {algorithm_name.replace('_', ' ')} is crucial for building scalable, "
                    f"efficient systems in enterprise settings."
                )

                content = (
                    content[: match.start(2)]
                    + enhanced_intro
                    + "\n\n"
                    + content[match.end(2) :]
                )
                readme_path.write_text(content, encoding="utf-8")
                return True

        return False
    except Exception as e:
        print(f"Error processing {readme_path}: {e}")
        return False


def enhance_detailed_explanation(
    readme_path: Path, algorithm_name: str, lecture_name: str
) -> bool:
    """Enhance detailed explanation section."""
    try:
        content = readme_path.read_text(encoding="utf-8")

        # Get specific description
        description = get_description(algorithm_name, lecture_name)
        if not description:
            return False

        # Check if detailed explanation has generic content
        detail_pattern = r"(## Detailed Explanation\s*\n\s*\n)(.*?)(?=\n##|\Z)"
        match = re.search(detail_pattern, content, re.DOTALL)

        if match:
            existing_detail = match.group(2).strip()

            # Check if generic or too short (more lenient)
            if has_generic_content(existing_detail) or len(existing_detail) < 400:
                # Create detailed explanation
                parts = description.split(". ")
                core_principle = parts[0] if parts else description
                how_it_works = ". ".join(parts[1:3]) if len(parts) > 1 else description

                detailed = f"""The {algorithm_name.replace('_', ' ').title()} technique is a critical component of modern software systems.

**Core Principles**:
{core_principle}

**How It Works**:
{how_it_works}

**Key Components**:
- Implementation details vary based on specific use case and requirements
- Performance characteristics depend on system configuration and workload
- Scalability considerations are essential for production deployment
- Error handling and edge cases must be thoroughly tested

**Real-World Considerations**:
- Production systems require careful tuning and monitoring
- Documentation and maintenance are critical for long-term success
- Integration with existing systems requires careful planning
- Performance optimization should be based on actual usage patterns"""

                content = (
                    content[: match.start(2)]
                    + detailed
                    + "\n\n"
                    + content[match.end(2) :]
                )
                readme_path.write_text(content, encoding="utf-8")
                return True

        return False
    except Exception as e:
        print(f"Error processing {readme_path}: {e}")
        return False


def main():
    """Execute Phase 9: Graduate Documentation Enhancement."""
    print("=" * 70)
    print("Phase 9: Graduate Documentation Enhancement")
    print("=" * 70)

    readme_files = find_graduate_readme_files()
    print(f"\nFound {len(readme_files)} graduate-level README files")

    short_desc_updated = 0
    intro_updated = 0
    detail_updated = 0

    for i, readme_path in enumerate(readme_files, 1):
        algorithm_name = readme_path.parent.name
        lecture_name = readme_path.parent.parent.name

        if enhance_short_description(readme_path, algorithm_name, lecture_name):
            short_desc_updated += 1

        if enhance_introduction(readme_path, algorithm_name, lecture_name):
            intro_updated += 1

        if enhance_detailed_explanation(readme_path, algorithm_name, lecture_name):
            detail_updated += 1

        total_updated = short_desc_updated + intro_updated + detail_updated
        if total_updated % 50 == 0 and total_updated > 0:
            print(
                f"[PROGRESS] Processed {i}/{len(readme_files)} files, updated {total_updated} sections..."
            )

    print(f"\n[COMPLETE] Processed {len(readme_files)} files")
    print(f"Short descriptions enhanced: {short_desc_updated} files")
    print(f"Introductions enhanced: {intro_updated} files")
    print(f"Detailed explanations enhanced: {detail_updated} files")
    print(
        f"Total enhancements: {short_desc_updated + intro_updated + detail_updated} sections"
    )
    print("\nEnhancements applied:")
    print("  - Specific, detailed descriptions for graduate topics")
    print("  - Enhanced introductions with context and importance")
    print("  - Improved detailed explanations with core principles")
    print("  - Removed generic placeholder content")
    print("\nCoverage areas:")
    print("  - Operating Systems (microkernel, exokernel, real-time, containers)")
    print("  - Concurrency (actors, lock-free, transactional memory)")
    print("  - Distributed Systems (consensus, vector clocks, CRDTs, BFT)")
    print("  - Cloud Native (service mesh, serverless, FaaS, orchestration)")
    print("  - Observability (tracing, metrics, APM, chaos engineering)")
    print("  - Data Engineering (data mesh, stream processing, lambda architecture)")
    print("  - LLM & AI (transformer optimization, compression, fine-tuning, RAG)")
    print("  - Databases (query optimization, sharding, indexing)")


if __name__ == "__main__":
    main()
