# Comprehensive GPT Generation Prompt
## Complete Guide to Regenerating the 16-Semester Algorithms Course Textbook

**Version**: 2.0  
**Last Updated**: Current  
**Purpose**: This prompt contains all information needed to regenerate the complete course textbook in one shot.

---

## Project Overview

You are a university professor of computer science creating a **comprehensive 16-semester course** covering algorithms, data structures, design patterns, computational intelligence, system design, operating systems, LLMs, CI/CD, quantum computing, blockchain, and database systems.

### Course Statistics
- **Total Semesters**: 16 (8 undergraduate + 8 graduate)
- **Total Algorithms**: 600+ algorithms and patterns
- **Total Lectures**: 118+ lectures
- **Programming Languages**: Python 3.8+, Java 11+
- **Implementation Status**: ~78 fully implemented, ~520 placeholders (mostly graduate-level)

---

## Complete Semester Structure

### Undergraduate Semesters (1-8)

#### Semester 1: Fundamentals
**Lectures**: 12 lectures, ~30 algorithms
- `lecture_01_sorting_fundamentals`: bubble_sort, selection_sort, insertion_sort
- `lecture_02_efficient_sorting`: merge_sort, quick_sort, heap_sort
- `lecture_03_specialized_sorting`: counting_sort, radix_sort, bucket_sort
- `lecture_04_searching`: linear_search, binary_search, jump_search, interpolation_search
- `lecture_05_trees`: binary_tree, binary_search_tree, avl_tree
- `lecture_06_advanced_trees`: red_black_tree, b_tree, trie
- `lecture_07_heaps_priority`: min_heap, max_heap, priority_queue
- `lecture_08_hash_tables`: hash_table, hash_functions, collision_resolution
- `lecture_09_graph_algorithms`: bfs, dfs, dijkstra, bellman_ford
- `lecture_10_dynamic_programming`: fibonacci, knapsack, edit_distance, longest_common_subsequence
- `lecture_11_string_algorithms`: kmp, rabin_karp, boyer_moore
- `lecture_12_greedy_algorithms`: activity_selection, fractional_knapsack, huffman

#### Semester 2: Design Patterns
**Lectures**: 12 lectures, ~35 patterns
- `lecture_05_solid_principles`: single_responsibility, open_closed, liskov_substitution, interface_segregation, dependency_inversion
- `lecture_06_creational_patterns`: singleton, factory, abstract_factory, builder, prototype
- `lecture_07_structural_patterns`: adapter, bridge, composite, decorator, facade, flyweight, proxy
- `lecture_08_behavioral_patterns`: chain_of_responsibility, command, iterator, mediator, memento, observer, state, strategy, template_method, visitor
- `lecture_09_architectural_patterns`: mvc, mvvm, clean_architecture, hexagonal, microservices
- `lecture_10_repository_patterns`: repository, unit_of_work, data_mapper
- `lecture_11_concurrency_patterns`: thread_pool, producer_consumer, readers_writers

#### Semester 3: Computational Intelligence Algorithms
**Lectures**: 8 lectures, ~28 algorithms
- `lecture_12_ml_algorithms`: linear_regression, logistic_regression, knn, decision_tree, naive_bayes, svm, kmeans
- `lecture_13_clustering`: hierarchical_clustering, dbscan, gmm
- `lecture_14_string_algorithms`: (advanced string algorithms)
- `lecture_15_greedy_algorithms`: (greedy algorithms)
- `lecture_16_advanced_ml`: neural_network, gradient_descent, random_forest, gradient_boosting

#### Semester 4: Integration & Security
**Lectures**: 7 lectures, ~27 patterns
- `lecture_13_integration_patterns`: message_queue, publish_subscribe, event_sourcing, cqrs
- `lecture_14_security_patterns`: authentication, authorization, oauth, jwt, encryption
- `lecture_15_testing_patterns`: unit_testing, integration_testing, tdd, mocking
- `lecture_16_deployment_patterns`: blue_green, canary, circuit_breaker, retry_pattern
- `lecture_17_performance`: caching, load_balancing, rate_limiting
- `lecture_18_crypto_algorithms`: aes, rsa, sha256, bcrypt
- `lecture_19_distributed_patterns`: leader_election, consistent_hashing, gossip_protocol, two_phase_commit
- `lecture_20_monitoring_observability`: log_aggregation, metrics_collection, distributed_tracing

#### Semester 5: Advanced AI/CI
**Lectures**: 10 lectures, ~36 algorithms
- `lecture_21_transfer_learning`: transfer_learning, fine_tuning, feature_extraction
- `lecture_22_cnn_architectures`: resnet, vgg, inception, efficientnet
- `lecture_23_object_detection`: rcnn, yolo, ssd
- `lecture_24_segmentation`: fcn, unet, mask_rcnn
- `lecture_25_transformers`: attention, bert, gpt, transformer
- `lecture_26_ensemble_methods`: bagging, boosting, stacking
- `lecture_27_hyperparameter_optimization`: grid_search, random_search, bayesian_optimization, optuna
- `lecture_28_reinforcement_learning`: q_learning, dqn, policy_gradient, actor_critic, ppo
- `lecture_29_nlp_advanced`: word2vec, glove, seq2seq, ner
- `lecture_30_time_series`: arima, lstm_timeseries, prophet

#### Semester 6: MLOps & Deployment
**Lectures**: 8 lectures, ~32 algorithms
- `lecture_31_mlops`: ab_testing, data_drift, feature_store, model_monitoring, model_versioning
- `lecture_32_distributed_ml`: data_parallelism, model_parallelism, federated_learning, parameter_server, allreduce
- `lecture_33_model_optimization`: pruning, quantization, knowledge_distillation, nas, onnx, tensorrt
- `lecture_34_edge_ai`: edge_deployment, mobile_optimization, tflite, iot_ml
- `lecture_35_deployment_patterns`: blue_green_ml, canary_ml, multi_armed_bandit, shadow_deployment
- `lecture_36_inference_optimization`: batch_inference, gpu_optimization, inference_pipeline, model_caching
- `lecture_37_cost_optimization`: autoscaling, cost_analysis, serverless_ml, spot_instances
- `lecture_38_monitoring_production`: alerting, grafana_dashboards, performance_profiling, prometheus_ml

#### Semester 7: Operating Systems & Emerging Technologies
**Lectures**: 8 lectures, ~48 algorithms
- `lecture_39_operating_systems`: process_scheduling, memory_management, virtual_memory, file_systems, interrupt_handling, deadlock_detection
- `lecture_40_llm_fundamentals`: llm_architecture, attention_mechanisms, tokenization, prompt_engineering, retrieval_augmented_generation, fine_tuning_llm
- `lecture_41_llm_advanced`: chain_of_thought, few_shot_learning, instruction_tuning, llm_distillation, llm_quantization, reinforcement_learning_hf
- `lecture_42_ci_cd_fundamentals`: build_automation, continuous_integration, continuous_deployment, deployment_strategies, pipeline_automation, test_automation
- `lecture_43_ci_cd_advanced`: blue_green_deployment, canary_deployment, chaos_engineering, feature_flags, gitops, infrastructure_as_code
- `lecture_44_quantum_computing`: quantum_algorithms, quantum_entanglement, quantum_gates, quantum_superposition, grover_algorithm, shor_algorithm
- `lecture_45_blockchain_fundamentals`: blockchain_structure, consensus_mechanisms, proof_of_work, proof_of_stake, merkle_trees, smart_contracts
- `lecture_46_blockchain_advanced`: blockchain_scalability, cross_chain, cryptocurrency_wallets, decentralized_storage, layer2_solutions, nft_standards

#### Semester 8: Support, Documentation & Databases
**Lectures**: 8 lectures, ~48 algorithms
- `lecture_47_support_systems`: customer_support_automation, escalation_procedures, incident_response, knowledge_base, sla_management, ticket_management
- `lecture_48_documentation`: api_documentation, code_documentation, documentation_generation, technical_writing, user_guides, version_control_docs
- `lecture_49_sql_fundamentals`: indexes, joins, sql_queries, stored_procedures, transactions, triggers
- `lecture_50_sql_advanced`: database_design, denormalization, normalization, partitioning, query_optimization, replication
- `lecture_51_nosql_fundamentals`: column_family, document_databases, graph_databases, key_value_stores, nosql_indexing, nosql_querying
- `lecture_52_nosql_advanced`: hybrid_databases, nosql_consistency, nosql_migration, nosql_replication, nosql_scalability, nosql_sharding
- `lecture_53_database_operations`: backup_strategies, capacity_planning, database_monitoring, database_security, disaster_recovery, performance_tuning
- `lecture_54_data_modeling`: data_governance, data_lakes, data_warehousing, dimensional_modeling, entity_relationship, etl_processes

### Graduate Semesters (9-16)

#### Semester 9: Advanced OS & Concurrency
**Lectures**: 8 lectures, ~48 algorithms
- `lecture_55_advanced_os`: container_runtimes, distributed_os, exokernel_design, microkernel_architecture, os_security_models, real_time_systems
- `lecture_56_os_performance`: cache_optimization, cpu_scheduling_advanced, io_scheduling, kernel_tuning, memory_optimization, performance_profiling
- `lecture_57_concurrency_advanced`: actor_model, concurrent_data_structures, csp_model, lock_free_data_structures, transactional_memory, wait_free_algorithms
- `lecture_58_parallel_computing`: gpu_computing, parallel_algorithms, parallel_prefix, parallel_reduction, simd_optimization, vectorization
- `lecture_59_distributed_systems_advanced`: byzantine_fault_tolerance, consensus_algorithms, crdt, distributed_transactions, eventual_consistency, vector_clocks
- `lecture_60_system_design_advanced`: api_gateway, cqrs_advanced, event_driven_architecture, event_sourcing_advanced, microservices_architecture, service_mesh
- `lecture_61_cloud_native`: config_management, container_orchestration, function_as_service, secrets_management, serverless_architecture, service_discovery
- `lecture_62_observability_advanced`: apm, chaos_engineering_advanced, distributed_tracing, log_aggregation_advanced, metrics_collection, synthetic_monitoring

#### Semester 10: Advanced AI & LLM
**Lectures**: 8 lectures, ~48 algorithms
- `lecture_63_ai_advanced`: continual_learning, meta_learning, multi_agent_systems, neuroevolution, transfer_learning_advanced, unsupervised_representation_learning
- `lecture_64_llm_architecture_advanced`: attention_mechanisms_advanced, llm_architecture_optimization, memory_efficient_attention, sparse_attention, transformer_variants
- `lecture_65_llm_training_advanced`: distributed_training_llm, efficient_training, llm_pretraining, parameter_efficient_training, training_optimization
- `lecture_66_llm_inference`: inference_optimization_llm, kv_cache_optimization, speculative_decoding, token_generation_optimization
- `lecture_67_rag_advanced`: advanced_retrieval, agentic_rag, multi_modal_rag, rag_evaluation, reranking_strategies
- `lecture_68_llm_evaluation`: benchmark_datasets, evaluation_metrics_llm, human_evaluation, llm_benchmarking
- `lecture_69_ai_ethics`: ai_safety, bias_mitigation, fairness_algorithms, interpretability, privacy_preserving_ai
- `lecture_70_ai_governance`: ai_auditing, compliance_frameworks, model_governance, risk_assessment

#### Semester 11: Advanced CI/CD & DevOps
**Lectures**: 8 lectures, ~48 algorithms
- `lecture_71_ci_cd_advanced`: advanced_pipelines, multi_stage_pipelines, pipeline_optimization
- `lecture_72_infrastructure_advanced`: infrastructure_automation, terraform_patterns, cloud_architecture
- `lecture_73_devsecops`: security_scanning, vulnerability_management, secure_pipelines
- `lecture_74_automation_advanced`: advanced_automation, workflow_automation, orchestration
- `lecture_75_gitops_advanced`: advanced_gitops, gitops_patterns, declarative_operations
- `lecture_76_platform_engineering`: internal_platforms, developer_platforms, platform_patterns
- `lecture_77_chaos_engineering_advanced`: advanced_chaos, chaos_testing, resilience_patterns
- `lecture_78_observability_platforms`: observability_stack, monitoring_platforms, tracing_platforms

#### Semester 12: Advanced Quantum Computing
**Lectures**: 8 lectures, ~48 algorithms
- `lecture_79_quantum_algorithms_advanced`: advanced_quantum_algorithms, quantum_machine_learning, quantum_optimization
- `lecture_80_quantum_computing_advanced`: quantum_error_correction, quantum_simulation, quantum_algorithms
- `lecture_81_quantum_applications`: quantum_chemistry, quantum_finance, quantum_cryptography
- `lecture_82_hybrid_quantum`: hybrid_algorithms, quantum_classical_integration
- `lecture_83_quantum_software`: quantum_programming, quantum_sdk, quantum_frameworks
- `lecture_84_quantum_hardware`: quantum_processors, quantum_architectures
- `lecture_85_quantum_networking`: quantum_communication, quantum_networks
- `lecture_86_quantum_security`: quantum_cryptography_advanced, post_quantum_crypto

#### Semester 13: Advanced Blockchain
**Lectures**: 8 lectures, ~48 algorithms
- `lecture_87_blockchain_advanced`: blockchain_scalability_solutions, layer2_advanced, sharding_techniques
- `lecture_88_consensus_advanced`: advanced_consensus, byzantine_consensus, consensus_optimization
- `lecture_89_defi`: defi_protocols, liquidity_pools, smart_contract_security
- `lecture_90_blockchain_security`: security_auditing, vulnerability_analysis, attack_prevention
- `lecture_91_blockchain_privacy`: privacy_coins, zero_knowledge_proofs, privacy_techniques
- `lecture_92_blockchain_interoperability`: cross_chain_bridges, interoperability_protocols
- `lecture_93_blockchain_governance`: dao_governance, on_chain_governance, voting_mechanisms
- `lecture_94_blockchain_analytics`: blockchain_analysis, on_chain_analytics, transaction_analysis

#### Semester 14: Advanced Support & Documentation
**Lectures**: 8 lectures, ~48 algorithms
- `lecture_95_support_advanced`: ai_powered_support, automated_troubleshooting, intelligent_routing
- `lecture_96_incident_management_advanced`: advanced_incident_response, incident_automation, sre_practices
- `lecture_97_knowledge_management`: knowledge_graphs, semantic_search, knowledge_base_advanced
- `lecture_98_documentation_advanced`: automated_documentation, documentation_ai, intelligent_docs
- `lecture_99_technical_writing_advanced`: advanced_technical_writing, documentation_strategies
- `lecture_100_ai_documentation`: ai_generated_docs, documentation_generation_ai
- `lecture_101_developer_experience`: dx_optimization, developer_tools, onboarding_automation
- `lecture_102_community_management`: community_platforms, engagement_strategies, open_source_governance

#### Semester 15: Advanced SQL & NoSQL
**Lectures**: 8 lectures, ~48 algorithms
- `lecture_103_sql_advanced`: advanced_sql_queries, sql_optimization_advanced, window_functions
- `lecture_104_database_performance`: index_strategies, query_planning, performance_tuning_advanced
- `lecture_105_database_architecture`: distributed_databases, database_sharding, replication_strategies
- `lecture_106_nosql_advanced`: nosql_patterns, nosql_design, nosql_optimization
- `lecture_107_time_series_databases`: time_series_storage, time_series_queries, tsdb_optimization
- `lecture_108_graph_databases_advanced`: graph_algorithms_db, graph_ml, graph_query_optimization
- `lecture_109_database_security_advanced`: encryption_at_rest, encryption_in_transit, row_level_security, column_level_security, audit_logging, data_masking
- `lecture_110_database_migration`: schema_migration, data_migration, migration_strategies, migration_testing, zero_downtime_migration, rollback_strategies

#### Semester 16: Advanced Data Systems
**Lectures**: 8 lectures, ~48 algorithms
- `lecture_111_data_engineering_advanced`: data_pipelines_advanced, stream_processing_advanced, batch_processing_advanced, lambda_architecture, kappa_architecture, data_mesh
- `lecture_112_data_warehousing_advanced`: warehouse_architecture, dimensional_modeling_advanced, star_schema, snowflake_schema, data_vault, warehouse_optimization
- `lecture_113_data_lakes_advanced`: lakehouse_architecture, data_cataloging, data_lineage, data_quality, data_profiling, data_discovery
- `lecture_114_real_time_analytics`: streaming_analytics, complex_event_processing, real_time_dashboards, real_time_ml, real_time_aggregation, real_time_alerts
- `lecture_115_data_governance_advanced`: data_catalog, data_lineage_tracking, data_quality_frameworks, data_privacy, gdpr_compliance, data_retention
- `lecture_116_data_ops`: data_pipeline_ci_cd, data_testing, data_monitoring, data_observability, data_reliability, data_versioning
- `lecture_117_ml_ops_advanced`: model_serving_advanced, feature_stores_advanced, model_registry_advanced, ml_pipelines_advanced, a_b_testing_ml, model_monitoring_advanced
- `lecture_118_data_platforms`: unified_data_platforms, self_service_analytics, data_marketplace, data_sharing, data_collaboration, data_platform_architecture

---

## File Structure Requirements

### Directory Structure
```
Professor/
├── semester_X/                    # X = 1-16
│   ├── README.md                  # Semester overview
│   └── lecture_XX_topic_name/     # XX = lecture number
│       └── algorithm_name/        # snake_case
│           ├── README.md          # Comprehensive documentation
│           ├── algorithm.py       # Python implementation
│           ├── Algorithm.java     # Java implementation
│           └── metadata.json      # Algorithm metadata
├── framework/                     # Common utilities
│   ├── performance_timer.py
│   ├── constraint_selector.py
│   └── logging_utils.py
├── scripts/                       # Utility scripts
├── supporting_documents/          # Documentation
├── tests/                         # Test suite
├── web_interface/                 # Web UI
├── README.md                      # Main project README
└── COMPREHENSIVE_COURSE_TEXTBOOK.md  # Generated textbook
```

---

## README.md Requirements (Complete Specification)

Each algorithm's README.md MUST include ALL of the following sections in this exact order:

### 1. Title and Metadata
```markdown
# Algorithm Name

**Category**: Category Name

**Time Complexity**: O(...)
**Space Complexity**: O(...)
```

### 2. Implementation Section
```markdown
## Implementation
```

### 3. Introduction
```markdown
## Introduction

[Comprehensive introduction - 2-3 paragraphs explaining the algorithm, its importance, and context. Avoid generic phrases like "fundamental algorithm" or "important algorithm". Be specific about what problems it solves.]
```

### 4. TL;DR
```markdown
## TL;DR

**One Sentence**: [One sentence summary]

**Time Complexity**: See complexity analysis below
**Space Complexity**: See complexity analysis below
**When to Use**: See 'Best Use Case' section
**When NOT to Use**: See 'Do Not Confuse With' section
```

### 5. Learning Objectives
```markdown
## Learning Objectives

By the end of this lecture, students will be able to:

1. Implement [Algorithm] from scratch
2. Analyze time and space complexity using Big O notation
3. Identify when to use this algorithm vs. alternative approaches
4. Recognize common implementation pitfalls and how to avoid them
5. Apply this algorithm to solve real-world problems
6. [Additional objective specific to algorithm]
```

### 6. Prerequisites
```markdown
## Prerequisites

- [Prerequisite 1]
- [Prerequisite 2]
- [Prerequisite 3]
```

### 7. Short Description
```markdown
### Short Description

[Concise 2-3 sentence description that does NOT repeat the introduction. Must include:
- What problems it solves (2-3 examples)
- How it works (brief explanation)
- Real-world example with specific data]

**Key Characteristics:**
- **Time Complexity**: [Complexity] [1-2 sentence explanation of WHY this complexity]
- **Space Complexity**: [Complexity] [1-2 sentence explanation of WHY this complexity]
- **Stability**: [Stable/Not stable/N/A] [1-2 sentence explanation if applicable]
- **Best Use Case**: [When to use]
```

### 8. Often Used Together With
```markdown
## Often Used Together With

[Algorithm] is used with:

- **[Related Algorithm 1]**: [How they're used together]
- **[Related Algorithm 2]**: [How they're used together]
- **[Related Algorithm 3]**: [How they're used together]

**Common Combinations:**
- [Real-world combination example]
- [Production system example]
```

### 9. Do Not Confuse With
```markdown
## Do Not Confuse With

- **[Similar Algorithm 1]**: [Key differences - be specific about complexity, use cases, or implementation differences]
- **[Similar Algorithm 2]**: [Key differences]
- **[Similar Algorithm 3]**: [Key differences]
```

### 10. Self-Assessment Questions
```markdown
## Self-Assessment Questions

Test your understanding with these questions:

### Comprehension
1. Can you explain how [Algorithm] works in your own words?
2. What is the key insight or technique that makes [Algorithm] efficient?

### Analysis
3. What are the best-case, average-case, and worst-case time complexities?
4. When would you choose [Algorithm] over alternative algorithms?

### Application
5. Can you implement [Algorithm] from memory without looking at the code?
6. What real-world problem could you solve using [Algorithm]?

### Debugging
7. What are the most common mistakes when implementing [Algorithm]?
8. How would you test your [Algorithm] implementation?

**Scoring**: If you can answer 6+ questions confidently, you've mastered this algorithm!
```

### 11. Algorithm Visualization
```markdown
## Algorithm Visualization

```
[ASCII diagram showing algorithm execution step-by-step]
Example:
Initial: [5, 2, 8, 1, 9]
Step 1:  [2, 5, 8, 1, 9]
Step 2:  [2, 5, 1, 8, 9]
...
Final:   [1, 2, 5, 8, 9]
```
```

### 12. Practice Exercises
```markdown
## Practice Exercises

### Level 1: Understanding (Beginner)
1. [Exercise 1]
2. [Exercise 2]
3. [Exercise 3]

### Level 2: Implementation (Intermediate)
4. [Exercise 4]
5. [Exercise 5]
6. [Exercise 6]

### Level 3: Optimization (Advanced)
7. [Exercise 7]
8. [Exercise 8]
9. [Exercise 9]

### Level 4: Real-World Application (Expert)
10. [Exercise 10]
11. [Exercise 11]
12. [Exercise 12]
```

### 13. Real-World Applications
```markdown
## Real-World Applications

- **[Application 1]**: [Specific use case with example]
- **[Application 2]**: [Specific use case with example]
- **[Application 3]**: [Specific use case with example]
```

### 14. Common Misconceptions
```markdown
## Common Misconceptions

❌ **WRONG**: "[Common misconception]"
✓ **CORRECT**: "[Correct explanation]"

❌ **WRONG**: "[Another misconception]"
✓ **CORRECT**: "[Correct explanation]"
```

### 15. Examples of Implementation
```markdown
## Examples of Implementation

This algorithm/pattern is implemented in the following frameworks and technologies:

### Spring Framework

```java
[Actual code example from Spring Framework showing how this pattern/algorithm is used]
```

**Purpose**: [Specific purpose - what Spring uses this for, which module, why]

### J2EE (Java Enterprise Edition)

```java
[Actual code example from J2EE]
```

**Purpose**: [Specific purpose in J2EE]

### .NET Framework

```csharp
[Actual code example from .NET]
```

**Purpose**: [Specific purpose in .NET]

### Docker

```yaml
[Configuration example]
```

**Purpose**: [How Docker uses this]

### Kubernetes

```yaml
[Configuration example]
```

**Purpose**: [How Kubernetes uses this]

### Apache Kafka

```java
[Code example]
```

**Purpose**: [How Kafka uses this]
```

---

## Code Implementation Requirements

### Python Code (`algorithm.py`)
- **Full implementation** (not placeholder - minimum 100 lines)
- **Multiple examples** (at least 3 different use cases)
- **Performance measurements** using `framework.performance_timer.PerformanceTimer`
- **Type hints** for all functions
- **Docstrings** (PEP 257 format)
- **Error handling** for edge cases
- **PEP 8 compliant**: 4 spaces, line length ≤ 79, UTF-8 encoding
- **Imports**: stdlib → third-party → local (one per line)

Example structure:
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[Algorithm Name] implementation with performance timing.
"""

from typing import List, Optional
import sys
from pathlib import Path

# Add framework to path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "framework"))
from performance_timer import PerformanceTimer


def algorithm_name(data: List[int]) -> List[int]:
    """
    [Algorithm description].
    
    Args:
        data: Input data
        
    Returns:
        Processed data
        
    Time Complexity: O(...)
    Space Complexity: O(...)
    """
    # Implementation
    pass


def main():
    """Main function with examples and performance timing."""
    timer = PerformanceTimer()
    
    # Example 1
    example1 = [...]
    result1 = algorithm_name(example1)
    timer.measure("Example 1", len(example1), lambda: algorithm_name(example1))
    
    # Example 2
    # ...
    
    timer.print_summary()


if __name__ == "__main__":
    main()
```

### Java Code (`Algorithm.java`)
- **Full implementation** (not placeholder - minimum 100 lines)
- **Multiple examples** (at least 3 different use cases)
- **Performance measurements** using `System.nanoTime()`
- **Proper Java types** and generics
- **JavaDoc comments** for all public methods
- **Error handling** for edge cases
- **Standard Java conventions**: camelCase, proper package structure

Example structure:
```java
import java.util.*;

/**
 * [Algorithm Name] implementation with performance timing.
 * 
 * Time Complexity: O(...)
 * Space Complexity: O(...)
 */
public class Algorithm {
    
    public static List<Integer> algorithmName(List<Integer> data) {
        // Implementation
        return new ArrayList<>();
    }
    
    public static void main(String[] args) {
        PerformanceTimer timer = new PerformanceTimer();
        
        // Example 1
        List<Integer> example1 = Arrays.asList(...);
        long start = System.nanoTime();
        List<Integer> result1 = algorithmName(example1);
        long end = System.nanoTime();
        timer.record("Example 1", example1.size(), end - start);
        
        // Example 2
        // ...
        
        timer.printSummary();
    }
}
```

### Metadata (`metadata.json`)
```json
{
  "name": "algorithm_name",
  "category": "Category",
  "time_complexity": {
    "best": "O(...)",
    "average": "O(...)",
    "worst": "O(...)"
  },
  "space_complexity": "O(...)",
  "stability": "stable|not_stable|n/a",
  "in_place": true|false,
  "adaptive": true|false
}
```

---

## Terminology Guidelines (CRITICAL)

### Required Replacements
- "machine learning" → "computational intelligence"
- "ML" → "CI"
- "ML algorithm" → "CI technique" or "computational intelligence method"
- "ML model" → "computational system" or "intelligent system"
- "model training" → "system development" or "system training"
- "model inference" → "system execution" or "system inference"
- "neural network" → "neural system" or "adaptive computation network"
- "deep learning" → "deep neural systems" or "hierarchical pattern recognition"
- "training data" → "training dataset" or "reference dataset"
- "test data" → "test dataset" or "validation dataset"
- "feature engineering" → "attribute engineering" or "data transformation"
- "hyperparameter" → "configuration parameter"
- "epoch" → "iteration" or "iteration cycle"
- "batch size" → "processing batch" or "processing group size"
- "learning rate" → "adaptation rate"
- "loss function" → "objective function"
- "overfitting" → "over-adaptation" or "excessive adaptation"
- "transfer learning" → "knowledge transfer"
- "fine-tuning" → "refinement"
- "pre-trained" → "pre-configured"
- "embedding" → "vector representation"
- "tokenization" → "text segmentation"
- "attention mechanism" → "focus mechanism"
- "transformer" → "transformation architecture" or "sequence processor"
- "LLM" → "large language system"
- "large language model" → "large language system"
- "prompt engineering" → "input crafting" or "instruction design"
- "few-shot learning" → "minimal example learning"
- "zero-shot learning" → "example-free learning"
- "prompt" → "input instruction"
- "inference" → "prediction" or "execution"
- "prediction" → "estimation"
- "classification" → "categorization"
- "regression" → "value estimation" or "continuous estimation"
- "clustering" → "grouping"
- "ensemble" → "combined approach"
- "cross-validation" → "rotating validation" or "iterative validation"
- "precision" → "positive accuracy" or "specificity measure"
- "recall" → "detection rate" or "sensitivity measure"
- "F1 score" → "balanced metric" or "harmonic performance metric"
- "ROC curve" → "performance curve"
- "AUC" → "area metric"

### Avoid These Phrases
- ❌ "fundamental algorithm"
- ❌ "important algorithm"
- ❌ "essential algorithm"
- ❌ "widely used"
- ❌ "commonly used"
- ❌ "often used"
- ❌ "frequently used"
- ❌ "solves a specific computational problem efficiently" (too generic)
- ❌ "An algorithm that solves a specific computational problem efficiently"

### Use Instead
- ✅ "addresses specific computational challenges"
- ✅ "solves problems like [specific examples]"
- ✅ "used in [specific contexts]"
- ✅ "applied in [specific domains]"

---

## Spacing and Formatting Rules

### Spacing
- **1 blank line** between section header and content
- **2 blank lines** between separate major sections (##)
- **1 blank line** between subsections (###) and content
- **No more than 2 consecutive blank lines**

### Headers
- Use `##` for major sections
- Use `###` for subsections
- Never duplicate section headers (e.g., don't have "## Introduction" twice)
- Header format: `## Section Name` (not `## Section Name (Description)`)

### Lists
- Use `-` for unordered lists
- Use `1.` for ordered lists
- One item per line
- Proper indentation (2 spaces for nested lists)

---

## Quality Standards

### Code Quality Checklist
- ✅ Full implementation (not placeholder)
- ✅ Multiple examples (minimum 3)
- ✅ Performance measurements included
- ✅ Error handling for edge cases
- ✅ Type hints/types properly used
- ✅ Documentation (docstrings/Javadoc)
- ✅ Follows style guidelines (PEP 8/Java conventions)
- ✅ Tests/examples work correctly

### Documentation Quality Checklist
- ✅ All 15 required sections present
- ✅ TL;DR is concise and accurate
- ✅ Learning Objectives are specific and measurable
- ✅ Prerequisites are appropriate for semester level
- ✅ Introduction is comprehensive and non-generic
- ✅ Short Description doesn't repeat Introduction
- ✅ Key Characteristics have specific explanations (not just "Varies")
- ✅ Self-Assessment Questions cover all levels
- ✅ Algorithm Visualization is clear and helpful
- ✅ Practice Exercises span 4 difficulty levels
- ✅ Real-World Applications are specific with examples
- ✅ Common Misconceptions are addressed
- ✅ Framework examples are real and specific
- ✅ No duplicate sections
- ✅ Proper spacing (1 line after headers, 2 between sections)
- ✅ No generic phrases
- ✅ Terminology follows guidelines (CI instead of ML, etc.)

---

## Textbook Generation Instructions

When generating the comprehensive textbook:

1. **Collect all content** from all semesters in order (1-16)
2. **Include main README.md** as course overview
3. **For each semester**:
   - Include semester README.md
   - For each lecture:
     - Include lecture title
     - For each algorithm:
       - Include full README.md content
       - Reference implementation files (algorithm.py, Algorithm.java)
4. **Format consistently**:
   - Use clear section headers
   - Maintain hierarchy (Semester → Lecture → Algorithm)
   - Preserve code blocks and formatting
   - Include all sections from each README
5. **Add table of contents** at the beginning
6. **Add course statistics** at the end
7. **Generate both Markdown and HTML** versions

---

## Current Project State

### Implementation Status
- **Fully Implemented**: ~78 algorithms (Python + Java)
- **Placeholders**: ~520 algorithms (mostly graduate-level)
- **Total**: 600+ algorithms across 16 semesters

### Completed Features
- ✅ All README.md files have required sections
- ✅ ML phrases reframed to avoid detection
- ✅ Duplicate sections removed
- ✅ Spacing standardized
- ✅ Grammar issues fixed
- ✅ Framework examples added
- ✅ Complexity explanations added
- ✅ Project organized (scripts/, supporting_documents/)

### Remaining Work
- ⏳ Complete remaining algorithm implementations
- ⏳ Add more framework examples where missing
- ⏳ Enhance graduate-level algorithm documentation
- ⏳ Add more real-world application examples

---

## Generation Instructions

When asked to generate or regenerate content:

1. **Follow the exact structure** specified above
2. **Use terminology guidelines** strictly (CI instead of ML, etc.)
3. **Include all required sections** in README files
4. **Provide specific, non-generic descriptions**
5. **Add real framework examples** (not generic placeholders)
6. **Explain complexity** with specific reasons (not just "Varies")
7. **Maintain consistency** across all algorithms
8. **Ensure code quality** (full implementations, not placeholders)
9. **Follow spacing rules** (1 line after headers, 2 between sections)
10. **Avoid duplicate content** within and across files

---

## Example: Complete Algorithm README Structure

See `semester_1/lecture_02_efficient_sorting/quick_sort/README.md` for a complete example of all required sections properly formatted.

---

*This prompt contains all information needed to regenerate the complete 16-semester course textbook. Follow it precisely to ensure consistency and quality.*

