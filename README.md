# Algorithms and Design Patterns Course
## 16-Semester Comprehensive Computer Science Curriculum

[![Status](https://img.shields.io/badge/Status-Active%20Development-green)]()
[![Progress](https://img.shields.io/badge/Progress-40%25%20Complete-yellow)]()
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)]()
[![Java](https://img.shields.io/badge/Java-11%2B-orange)]()

> **A production-ready, educational resource** covering 600+ algorithms, design patterns, and computational intelligence techniques with implementations in Python and Java.

## 📚 Course Overview

This repository contains a **complete 16-semester course** (8 undergraduate + 8 graduate) in algorithms, data structures, design patterns, computational intelligence, system design, operating systems, LLMs, CI/CD, quantum computing, blockchain, and database systems. Each algorithm includes:

- ✅ **Full Python & Java implementations**
- ✅ **TL;DR sections** for quick understanding
- ✅ **Learning Objectives** clearly defined
- ✅ **Prerequisites** listed for each algorithm
- ✅ **Self-Assessment Questions** to test understanding
- ✅ **Algorithm Visualizations** with ASCII diagrams
- ✅ **Practice Exercises** with graduated difficulty levels
- ✅ **Real-World Applications** with industry examples
- ✅ **Common Misconceptions** clarified
- ✅ **Real-world examples** and use cases
- ✅ **Performance measurements** and complexity analysis
- ✅ **Common mistakes** and best practices
- ✅ **When to use** and when NOT to use
- ✅ **Framework integration examples** (Spring, J2EE, .NET, Docker, Kubernetes, Kafka)
- ✅ **"Often Used Together With"** sections
- ✅ **"Do Not Confuse With"** sections
- ✅ **Learning paths** (Interview Prep, Full Stack, CI Engineer, Complete)
- ✅ **Worked examples** with step-by-step walkthroughs
- ✅ **Testing framework** for algorithm validation
- ✅ **Assessment framework** with grading rubrics
- ✅ **Metacognitive strategies** guide for effective learning
- ✅ **Spaced repetition system** for long-term retention
- ✅ **Gamification system** with badges, points, and challenges
- ✅ **Client-ready templates** for professional services
- ✅ **Interactive HTML textbook** with search and filters
- ✅ **Table of contents** with multiple navigation views
- ✅ **Bidirectional sync** for amendment files

## 🎯 Current Status

**Implementation Progress**: 78+ / 600+ algorithms (13%+)
- **Fully Implemented**: 78 algorithms (Python + Java)
- **Placeholders Remaining**: ~520 algorithms (mostly graduate-level)
- **Total Algorithms**: 600+ across 16 semesters
- **Undergraduate Semesters (1-8)**: 300+ algorithms
- **Graduate Semesters (9-16)**: 300+ advanced algorithms

### Documentation & Navigation

**Enhanced README Structure**:
- **Individual algorithm links**: Direct links to all 680+ algorithms in main README
- **Code file links**: Each algorithm README includes links to Python, Java, and test files
- **Lesson navigation**: Quick access to all lectures across 16 semesters
- **Visualization guide**: Comprehensive recommendations for improving algorithm visualizations

### Testing & Code Quality

**Automated Testing System**:
- **680+ test files** (Python and Java)
- **Automated fixing system** for import errors, API usage errors, and compilation issues
- **Java auto-fix script** with comprehensive error detection and fixing
- **Database tracking** of test results with status history
- **Web interface** for monitoring test progress and results
- **Fixed statistics filter**: Resolved discrepancy in test reports filtering

**Code Quality Improvements**:
- **Java logger standardization**: Replacing `System.out.println/printf` with `logger.info()` for consistent logging
- **Java compilation fixes**: Automatic fixes for package errors, class name mismatches, missing methods, syntax errors, invalid parameter syntax, and Python-style None in Java
- **Python import fixes**: Automatic correction of import errors and API usage issues
- **2,800+ successful Java tests** recorded in database
- **4,700+ total test records** tracked
- **Repository cleanup**: Removed 827 .class files from git tracking, added to .gitignore

### Algorithm Execution Framework

**Unified Algorithm Executor:**
- **Web-based executor** for both Java and Python algorithms
- **Language selector**: Filter and execute algorithms by language
- **Code viewer**: Real-time source code display with syntax highlighting
- **Execution monitoring**: Real-time output display with execution time tracking
- **Filtering**: By semester, lecture, and algorithm name
- **Framework integration**: Uses `framework/java_executor.py` and `framework/python_executor.py`
- **Access**: Available at `/algorithm-executor` route in web interface

### Student Sandbox & Learning Environment (Planned)

**Comprehensive Plan Created:**
- **Student Sandbox System**: Isolated workspace for students to modify and test algorithms
- **Version Control**: Full version history with rollback capabilities
- **Comparison System**: Performance, resource usage, and correctness comparison with original
- **Code Editor**: Web-based editor with split view (original vs student code)
- **Testing Framework**: Enhanced test suite with correctness, performance, and resource tests
- **Visualization**: Interactive charts, test matrices, and code diff visualization
- **Security**: Docker-based isolation with resource limits
- **Role-Based Access**: Visitor (read-only), Student, Professor, Admin roles
- **Detailed Plan**: See `docs/STUDENT_SANDBOX_PLAN.md` for complete implementation roadmap

### Completed Sections

#### ✅ Semester 1: Fundamentals (69% complete)
- **Sorting**: All 8 algorithms (Bubble, Selection, Insertion, Merge, Quick, Heap, Counting, Radix, Bucket)
- **Trees**: AVL, Red-Black, B-Tree, BST, Binary Tree
- **Graph**: DFS, BFS (Dijkstra, Bellman-Ford in progress)
- **Searching**: Linear, Binary, Jump, Interpolation

#### 🔄 Semester 2: Design Patterns (6% complete)
- **Creational**: Singleton, Factory
- **Structural**: (In progress)
- **Behavioral**: (Planned)

#### 🔄 Semester 3: Machine Learning (29% complete)
- **Supervised**: Linear Regression, Logistic Regression, KNN, Decision Tree
- **Unsupervised**: K-Means
- **Advanced**: Random Forest, Gradient Boosting, Neural Networks

#### ⏳ Semesters 4-6: In Progress
- Integration patterns
- Security patterns
- Advanced AI/ML
- MLOps and deployment

## 🚀 Quick Start

### Prerequisites
```bash
# Python 3.8+
python --version

# Java 11+
java --version

# Required Python packages
pip install -r requirements.txt

# Required Java dependencies (Maven)
mvn install
```

### Running Examples

#### Python
```bash
# Run any algorithm
python semester_01/lecture_02_efficient_sorting/merge_sort/algorithm.py

# Run with performance timing
python runner.py --algorithm merge_sort

# Run all algorithms in a lecture
python runner.py --lecture lecture_02_efficient_sorting
```

#### Java
```bash
# Compile and run
cd semester_01/lecture_02_efficient_sorting/merge_sort
javac Algorithm.java
java Algorithm

# Or use Maven
mvn exec:java -Dexec.mainClass="Algorithm"
```

### Web Interface
```bash
# Start web interface to browse all algorithms
cd web_interface
python app.py

# Open browser to http://localhost:5000
```

**Available Routes:**
- `/` - Main index page with algorithm browser
- `/algorithm-executor` - Unified Algorithm Executor (Java + Python)
- `/java-executor` - Java-only algorithm executor
- `/test-reports` - Test results and statistics dashboard
- `/readme/<path>` - View algorithm README files
- `/code/<path>` - View algorithm source code with syntax highlighting

### Testing and Auto-Fixing

**Run all tests:**
```bash
python scripts/test_runner.py
```

**Automatically fix test errors:**
```bash
# Tests each file, fixes import/API errors, and commits successful fixes
python -m scripts.fix_imports_one_by_one
```

**Current Capabilities:**
The auto-fix script automatically fixes multiple types of errors:

1. **Import Errors** ✅
   - Fixes incorrect imports (e.g., importing `__init__` instead of actual class/function)
   - Fixes nonexistent imports (replaces with correct main export)
   - Fixes duplicated names in assignments
   - Detects and comments out wrong imports from different algorithm modules

2. **API Usage Errors** ✅ **NEW**
   - Parses function/class signatures using AST
   - Detects missing required arguments
   - Automatically fixes calls with wrong number of arguments
   - Handles class instantiation errors (missing constructor arguments)
   - Uses placeholders for missing arguments (may need manual adjustment)

**Features:**
- Tests each Python test file sequentially (680+ files)
- Automatically fixes import and API usage errors
- Retests after each fix attempt
- Continues until test passes or max attempts reached
- Commits successful fixes (no push)
- Reports progress after each file
- Status updates every 3 minutes
- Graceful interruption handling

**What it can fix:**
- ✅ Import errors (wrong module, wrong name, nonexistent imports)
- ✅ API usage errors (missing arguments, wrong function signatures)
- ✅ Duplicated names in assignments
- ✅ Wrong imports from different algorithm modules

**What it cannot fix:**
- ❌ Algorithm logic errors (wrong calculations, missing memoization)
- ❌ Complex API patterns requiring test logic rewrites
- ❌ Test expectation errors (test expects wrong behavior)

**Status:** The script has successfully fixed 6+ files automatically and identified patterns for manual fixes.

See [scripts/TESTING_SYSTEM_README.md](scripts/TESTING_SYSTEM_README.md) for detailed testing documentation.
See [FAILURE_ANALYSIS.md](FAILURE_ANALYSIS.md) for analysis of fixable vs non-fixable errors.

### 📚 Interactive Textbook

The comprehensive textbook includes search and filter functionality:

**To regenerate TOC:**
```bash
python scripts/generate_textbook_toc.py
```

**To regenerate interactive HTML:**
```bash
python scripts/generate_interactive_textbook.py
```

**To use the interactive textbook:**
1. Open `COMPREHENSIVE_COURSE_TEXTBOOK.html` in your web browser
2. Use the search box to find algorithms by name
3. Use the dropdown filters to narrow down by semester or category
4. Check/uncheck language or difficulty boxes to filter
5. The results counter shows how many algorithms match your criteria
6. Click "Clear All Filters" to reset

The interactive textbook features:
- 🔍 **Search by Name**: Real-time search as you type
- 📅 **Filter by Semester**: Select specific semesters (1-16)
- 🏷️ **Filter by Category**: Sort by algorithm type (Sorting, Searching, etc.)
- 💻 **Filter by Language**: Python, Java, SQL
- 📊 **Filter by Difficulty**: Undergraduate or Graduate level

See [scripts/TEXTBOOK_FEATURES_README.md](scripts/TEXTBOOK_FEATURES_README.md) for detailed documentation.

### 📝 Amendment Files (Bidirectional Sync)

The following amendment files are bidirectionally synchronized with the comprehensive textbook:

- **ASSESSMENT_FRAMEWORK.md** - Comprehensive evaluation system
- **CLIENT_READY_TEMPLATES.md** - Professional service templates
- **CODE_OF_CONDUCT.md** - Community guidelines
- **COLLABORATION_TOOLS.md** - Collaboration and communication tools
- **GAMIFICATION_SYSTEM.md** - Gamification and engagement system
- **LEARNING_PATHS.md** - Learning path guides
- **METACOGNITIVE_STRATEGIES.md** - Learning strategies
- **MLOPS_INTEGRATION_GUIDE.md** - MLOps integration guide
- **STRATEGIC_DOCUMENTATION.md** - Documentation strategies
- **TEACHING_RESOURCES.md** - Teaching resources and materials

**To sync amendment files with textbook:**
```bash
# Sync from amendment files to textbook (default)
python scripts/sync_amendments_bidirectional.py --sync-to-textbook

# Sync from textbook to amendment files
python scripts/sync_amendments_bidirectional.py --sync-from-textbook

# Sync in both directions
python scripts/sync_amendments_bidirectional.py --sync-both
```

**Note**: Changes to either the amendment files or the textbook sync sections will be reflected in both locations. See [scripts/AMENDMENT_SYNC_README.md](scripts/AMENDMENT_SYNC_README.md) for detailed documentation.

## 📖 Course Structure

> **📋 Quick Navigation**: Jump to [Lesson Links](#-course-structure-with-lesson-links) below for direct links to all lectures.

### Semester 1: Fundamentals (26 algorithms)
- **Week 1-2**: Sorting (Bubble, Selection, Insertion, Merge, Quick, Heap)
- **Week 3-4**: Specialized Sorting (Counting, Radix, Bucket)
- **Week 5-6**: Searching (Linear, Binary, Jump, Interpolation)
- **Week 7-8**: Trees (Binary, BST, AVL, Red-Black, B-Tree)
- **Week 9-10**: Heaps & Hash Tables
- **Week 11-12**: Graph Algorithms (DFS, BFS, Dijkstra, Bellman-Ford)
- **Week 13-14**: Dynamic Programming
- **Week 15**: String Algorithms

### Semester 2: Design Patterns

> **📋 Complete Algorithm Index**: See [ALGORITHM_LINKS.md](ALGORITHM_LINKS.md) for links to all algorithms in this semester.

**SOLID Principles** (5 patterns), **Creational Patterns** (5), **Structural Patterns** (7), **Behavioral Patterns** (10), **Architectural Patterns** (5)

Key patterns include: Singleton, Factory, Abstract Factory, Builder, Prototype, Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy, Observer, Strategy, Command, Iterator, MVC, MVVM, Clean Architecture, and more.

### Semester 3: Machine Learning

> **📋 Complete Algorithm Index**: See [ALGORITHM_LINKS.md](ALGORITHM_LINKS.md) for links to all algorithms in this semester.

**Supervised Learning**: Regression, Classification (KNN, Decision Tree, SVM, Naive Bayes), **Unsupervised Learning**: K-Means, Hierarchical Clustering, DBSCAN, **Ensemble Methods**: Random Forest, Gradient Boosting, XGBoost, **Neural Networks**: Basic MLP, Backpropagation, **Deep Learning Intro**: CNN, RNN basics, **Feature Engineering**: PCA, Feature Selection

### Semester 4: Integration & Security

> **📋 Complete Algorithm Index**: See [ALGORITHM_LINKS.md](ALGORITHM_LINKS.md) for links to all algorithms in this semester.

**Integration Patterns**: Message Queue, Pub-Sub, Event Sourcing, CQRS, **Security Patterns**: Authentication, Authorization, OAuth, JWT, Encryption, **Testing Patterns**: Unit Testing, Integration Testing, TDD, Mocking, **Deployment Patterns**: Blue-Green, Canary, Circuit Breaker

### Semester 5: Advanced AI/ML

> **📋 Complete Algorithm Index**: See [ALGORITHM_LINKS.md](ALGORITHM_LINKS.md) for links to all algorithms in this semester.

**Transfer Learning**: Fine-tuning, Feature Extraction, **Advanced CNN**: ResNet, VGG, Inception, EfficientNet, **Object Detection**: YOLO, R-CNN, SSD, **Transformers**: BERT, GPT, Attention mechanisms, **Reinforcement Learning**: Q-Learning, DQN, Policy Gradient, **Time Series**: ARIMA, LSTM, Prophet

### Semester 6: MLOps & Production

> **📋 Complete Algorithm Index**: See [ALGORITHM_LINKS.md](ALGORITHM_LINKS.md) for links to all algorithms in this semester.

**Model Deployment**: Batch, Real-time, Edge deployment, **Monitoring**: Model drift, performance tracking, alerting, **Optimization**: Quantization, Pruning, Knowledge Distillation, **Distributed Training**: Data/Model Parallelism, Federated Learning, **Cost Optimization**: Autoscaling, Spot Instances, Serverless

### Semester 7: Advanced Topics

> **📋 Complete Algorithm Index**: See [ALGORITHM_LINKS.md](ALGORITHM_LINKS.md) for links to all algorithms in this semester.

**Operating Systems**: Process scheduling, memory management, file systems, virtual memory, deadlock detection, **LLM Fundamentals**: Architecture, tokenization, attention mechanisms, prompt engineering, fine-tuning, RAG, **LLM Advanced**: Chain of thought, few-shot learning, instruction tuning, RLHF, quantization, distillation, **CI/CD Fundamentals**: Continuous integration, deployment, pipeline automation, test/build automation, **CI/CD Advanced**: Blue-green, canary, feature flags, IaC, GitOps, chaos engineering, **Quantum Computing**: Quantum gates, superposition, entanglement, quantum algorithms, Shor, Grover, **Blockchain Fundamentals**: Structure, consensus, PoW, PoS, smart contracts, Merkle trees, **Blockchain Advanced**: Scalability, Layer 2, cross-chain, decentralized storage, wallets, NFTs

### Semester 8: Support, Documentation & Databases

> **📋 Complete Algorithm Index**: See [ALGORITHM_LINKS.md](ALGORITHM_LINKS.md) for links to all algorithms in this semester.

**Support Systems**: Ticket management, knowledge base, incident response, SLA management, automation, **Documentation**: API docs, code docs, technical writing, doc generation, version control, user guides, **SQL Fundamentals**: Queries, joins, indexes, transactions, stored procedures, triggers, **SQL Advanced**: Query optimization, database design, normalization, denormalization, partitioning, replication, **NoSQL Fundamentals**: Document DBs, key-value stores, column family, graph DBs, querying, indexing, **NoSQL Advanced**: Scalability, consistency, sharding, replication, hybrid DBs, migration, **Database Operations**: Backup strategies, disaster recovery, monitoring, performance tuning, capacity planning, security, **Data Modeling**: ER modeling, dimensional modeling, data warehousing, data lakes, ETL, data governance

### Graduate Semesters (9-16): Advanced Topics

> **📋 Complete Algorithm Index**: See [ALGORITHM_LINKS.md](ALGORITHM_LINKS.md) for links to all 300+ algorithms in graduate semesters.

#### Semester 9: Advanced OS & Concurrency (48 algorithms)
- **Advanced OS**: Microkernel, exokernel, distributed OS, real-time systems, OS security, container runtimes
- **OS Performance**: CPU scheduling, memory optimization, I/O scheduling, cache optimization, kernel tuning
- **Advanced Concurrency**: Lock-free structures, wait-free algorithms, transactional memory, actor/CSP models
- **Parallel Computing**: Parallel algorithms, GPU computing, vectorization, SIMD, parallel reduction/prefix
- **Distributed Systems**: Consensus, Byzantine fault tolerance, distributed transactions, vector clocks, CRDTs
- **System Design**: Microservices, service mesh, API gateway, event-driven, CQRS, event sourcing
- **Cloud Native**: Serverless, FaaS, container orchestration, service discovery, config/secrets management
- **Observability**: Distributed tracing, metrics, log aggregation, APM, synthetic monitoring, chaos engineering

#### Semester 10: Advanced AI & LLM

> **📋 See [ALGORITHM_LINKS.md](ALGORITHM_LINKS.md) for complete algorithm list**
- **Advanced AI**: Meta-learning, transfer learning, few-shot/zero-shot learning, continual/lifelong learning
- **LLM Architecture**: Transformer optimization, sparse attention, mixture of experts, long context, multimodal
- **LLM Training**: Distributed training, gradient checkpointing, mixed precision, model/pipeline/tensor parallelism
- **LLM Inference**: KV cache optimization, speculative decoding, batch inference, continuous batching, quantization
- **Advanced RAG**: Hybrid search, reranking, query expansion, context compression, multi-hop, agentic RAG
- **LLM Evaluation**: Evaluation metrics, benchmark suites, human evaluation, adversarial testing, bias detection
- **AI Ethics**: Fairness algorithms, bias mitigation, explainability, interpretability, adversarial robustness
- **AI Governance**: Model governance, data governance, compliance frameworks, audit trails, risk assessment

#### Semester 11: Advanced CI/CD & DevOps

> **📋 See [ALGORITHM_LINKS.md](ALGORITHM_LINKS.md) for complete algorithm list**
- **Advanced CI/CD**: Multi-stage pipelines, parallel pipelines, conditional execution, templates, optimization
- **Infrastructure**: Infrastructure patterns, multi-cloud, edge computing, hybrid cloud, monitoring, cost optimization
- **DevSecOps**: Security scanning, vulnerability management, secrets rotation, compliance automation, threat modeling
- **Automation**: Self-healing systems, auto-scaling, predictive scaling, automated remediation, intelligent automation
- **GitOps**: GitOps patterns, progressive delivery, canary analysis, feature management, environment management
- **Platform Engineering**: Internal developer platforms, developer experience, self-service platforms, portals
- **Chaos Engineering**: Chaos experiments, fault injection, resilience testing, chaos automation, game days
- **Observability Platforms**: Observability stack, unified observability, AIOps, anomaly detection, RCA

#### Semester 12: Advanced Quantum Computing (48 algorithms)
- **Quantum Algorithms**: Quantum CI, optimization, simulation, cryptography, error correction, teleportation
- **Quantum Computing**: Quantum circuits, compilation, noise, benchmarking, architectures, networking
- **Quantum Applications**: Quantum chemistry, finance, logistics, AI, database, search
- **Hybrid Quantum**: Variational quantum, quantum-classical hybrid, approximate optimization, ML/simulation hybrid
- **Quantum Software**: Quantum programming, software stack, debugging, testing, verification, optimization tools
- **Quantum Hardware**: Quantum processors, control, calibration, characterization, control systems, readout
- **Quantum Networking**: Quantum communication, key distribution, repeaters, quantum internet, switching, routing
- **Quantum Security**: Post-quantum cryptography, quantum-resistant, quantum attacks/defense, key management

#### Semester 13: Advanced Blockchain (48 algorithms)
- **Blockchain Advanced**: Scalability solutions, sharding, state channels, sidechains, rollups, plasma
- **Consensus Advanced**: PBFT, Raft, DPoS advanced, Tendermint, HotStuff, Algorand
- **DeFi**: Automated market makers, liquidity pools, yield farming, lending protocols, derivatives, stablecoins
- **Blockchain Security**: Smart contract security, formal verification, audit techniques, vulnerability detection
- **Blockchain Privacy**: Zero-knowledge proofs, zk-SNARKs, zk-STARKs, ring signatures, confidential transactions
- **Interoperability**: Cross-chain bridges, atomic swaps, interoperability protocols, multi-chain apps
- **Governance**: DAO governance, voting mechanisms, proposal systems, treasury management, upgrade mechanisms
- **Analytics**: On-chain analytics, transaction analysis, address clustering, flow analysis, anomaly detection

#### Semester 14: Advanced Support & Documentation (48 algorithms)
- **Support Advanced**: AI-powered support, advanced chatbots, sentiment analysis, AI ticket routing, knowledge graphs
- **Incident Management**: Incident response automation, postmortem automation, correlation, alert fatigue reduction
- **Knowledge Management**: AI knowledge base, content curation, knowledge graph construction, semantic search
- **Documentation Advanced**: Automated documentation, doc-as-code, interactive docs, advanced API docs
- **Technical Writing**: Writing automation, content generation, style guides, translation automation
- **AI Documentation**: AI doc generation, code-to-docs, natural language docs, intelligent search, contextual help
- **Developer Experience**: Onboarding automation, developer portals, API explorer, sandbox environments
- **Community Management**: Community platforms, contribution management, moderation automation, analytics

#### Semester 15: Advanced SQL & NoSQL (48 algorithms)
- **SQL Advanced**: Advanced joins, window functions, recursive queries, CTEs, pivot/unpivot, SQL analytics
- **Database Performance**: Query optimization, index strategies, partitioning, materialized views, statistics
- **Database Architecture**: Clustering, read replicas, write scaling, advanced sharding, multi-tenant, federation
- **NoSQL Advanced**: Data modeling, query optimization, consistency models, transactions, aggregation, analytics
- **Time Series**: Time series storage, queries, downsampling, retention policies, compression, analytics
- **Graph Databases**: Graph algorithms, traversal, pattern matching, analytics, visualization, graph CI
- **Database Security**: Encryption at rest/transit, row/column-level security, audit logging, data masking
- **Database Migration**: Schema/data migration, zero-downtime migration, strategies, testing, rollback

#### Semester 16: Advanced Data Systems (48 algorithms)
- **Data Engineering**: Advanced pipelines, stream/batch processing, lambda/kappa architecture, data mesh
- **Data Warehousing**: Warehouse architecture, dimensional modeling, star/snowflake schema, data vault
- **Data Lakes**: Lakehouse architecture, data cataloging, lineage, quality, profiling, discovery
- **Real-Time Analytics**: Streaming analytics, complex event processing, real-time dashboards, CI, aggregation
- **Data Governance**: Data catalog, lineage tracking, quality frameworks, privacy, GDPR compliance, retention
- **DataOps**: Pipeline CI/CD, data testing, monitoring, observability, reliability, versioning
- **MLOps Advanced**: Model serving, A/B testing, monitoring, feature stores, model registry, pipelines
- **Data Platforms**: Unified platforms, self-service analytics, data marketplace, sharing, collaboration

## 📚 Course Structure with Lesson Links

## 📚 Individual Algorithm Links

> **Quick Navigation**: Browse individual algorithms by semester and lecture.

### Semester 1

#### 01: Sorting Fundamentals

- [Bubble Sort](semester_01/lecture_01_sorting_fundamentals/bubble_sort/README.md)
- [Insertion Sort](semester_01/lecture_01_sorting_fundamentals/insertion_sort/README.md)
- [Selection Sort](semester_01/lecture_01_sorting_fundamentals/selection_sort/README.md)

#### 02: Efficient Sorting

- [Heap Sort](semester_01/lecture_02_efficient_sorting/heap_sort/README.md)
- [Merge Sort](semester_01/lecture_02_efficient_sorting/merge_sort/README.md)
- [Quick Sort](semester_01/lecture_02_efficient_sorting/quick_sort/README.md)

#### 03: Specialized Sorting

- [Bucket Sort](semester_01/lecture_03_specialized_sorting/bucket_sort/README.md)
- [Counting Sort](semester_01/lecture_03_specialized_sorting/counting_sort/README.md)
- [Radix Sort](semester_01/lecture_03_specialized_sorting/radix_sort/README.md)

#### 04: Searching

- [Binary Search](semester_01/lecture_04_searching/binary_search/README.md)
- [Interpolation Search](semester_01/lecture_04_searching/interpolation_search/README.md)
- [Jump Search](semester_01/lecture_04_searching/jump_search/README.md)
- [Linear Search](semester_01/lecture_04_searching/linear_search/README.md)

#### 05: Trees

- [Avl Tree](semester_01/lecture_05_trees/avl_tree/README.md)
- [Binary Search Tree](semester_01/lecture_05_trees/binary_search_tree/README.md)
- [Binary Tree](semester_01/lecture_05_trees/binary_tree/README.md)

#### 06: Advanced Trees

- [Avl Tree](semester_01/lecture_06_advanced_trees/avl_tree/README.md)
- [B Tree](semester_01/lecture_06_advanced_trees/b_tree/README.md)
- [Red Black Tree](semester_01/lecture_06_advanced_trees/red_black_tree/README.md)
- [Trie](semester_01/lecture_06_advanced_trees/trie/README.md)

#### 07: Heaps Priority

- [Binary Heap](semester_01/lecture_07_heaps_priority/binary_heap/README.md)
- [Fibonacci Heap](semester_01/lecture_07_heaps_priority/fibonacci_heap/README.md)
- [Priority Queue](semester_01/lecture_07_heaps_priority/priority_queue/README.md)

#### 08: Hash Tables

- [Chaining](semester_01/lecture_08_hash_tables/chaining/README.md)
- [Hash Table](semester_01/lecture_08_hash_tables/hash_table/README.md)
- [Open Addressing](semester_01/lecture_08_hash_tables/open_addressing/README.md)

#### 09: Graph Algorithms

- [Bellman Ford](semester_01/lecture_09_graph_algorithms/bellman_ford/README.md)
- [Bfs](semester_01/lecture_09_graph_algorithms/bfs/README.md)
- [Dfs](semester_01/lecture_09_graph_algorithms/dfs/README.md)
- [Dijkstra](semester_01/lecture_09_graph_algorithms/dijkstra/README.md)
- [Floyd Warshall](semester_01/lecture_09_graph_algorithms/floyd_warshall/README.md)

#### 11: Dynamic Programming

- [Edit Distance](semester_01/lecture_11_dynamic_programming/edit_distance/README.md)
- [Fibonacci](semester_01/lecture_11_dynamic_programming/fibonacci/README.md)
- [Knapsack](semester_01/lecture_11_dynamic_programming/knapsack/README.md)
- [Longest Common Subsequence](semester_01/lecture_11_dynamic_programming/longest_common_subsequence/README.md)

#### 12: String Algorithms

- [Kmp](semester_01/lecture_12_string_algorithms/kmp/README.md)

### Semester 2

#### 06: Solid Principles

- [Dependency Inversion](semester_02/lecture_06_solid_principles/dependency_inversion/README.md)
- [Interface Segregation](semester_02/lecture_06_solid_principles/interface_segregation/README.md)
- [Liskov Substitution](semester_02/lecture_06_solid_principles/liskov_substitution/README.md)
- [Open Closed](semester_02/lecture_06_solid_principles/open_closed/README.md)
- [Single Responsibility](semester_02/lecture_06_solid_principles/single_responsibility/README.md)

#### 07: Creational Patterns

- [Abstract Factory](semester_02/lecture_07_creational_patterns/abstract_factory/README.md)
- [Builder](semester_02/lecture_07_creational_patterns/builder/README.md)
- [Factory](semester_02/lecture_07_creational_patterns/factory/README.md)
- [Prototype](semester_02/lecture_07_creational_patterns/prototype/README.md)
- [Singleton](semester_02/lecture_07_creational_patterns/singleton/README.md)

#### 08: Structural Patterns

- [Adapter](semester_02/lecture_08_structural_patterns/adapter/README.md)
- [Bridge](semester_02/lecture_08_structural_patterns/bridge/README.md)
- [Composite](semester_02/lecture_08_structural_patterns/composite/README.md)
- [Decorator](semester_02/lecture_08_structural_patterns/decorator/README.md)
- [Facade](semester_02/lecture_08_structural_patterns/facade/README.md)
- [Proxy](semester_02/lecture_08_structural_patterns/proxy/README.md)

#### 09: Behavioral Patterns

- [Chain Of Responsibility](semester_02/lecture_09_behavioral_patterns/chain_of_responsibility/README.md)
- [Command](semester_02/lecture_09_behavioral_patterns/command/README.md)
- [Iterator](semester_02/lecture_09_behavioral_patterns/iterator/README.md)
- [Observer](semester_02/lecture_09_behavioral_patterns/observer/README.md)
- [Strategy](semester_02/lecture_09_behavioral_patterns/strategy/README.md)
- [Template Method](semester_02/lecture_09_behavioral_patterns/template_method/README.md)

#### 10: Architectural Patterns

- [Clean Architecture](semester_02/lecture_10_architectural_patterns/clean_architecture/README.md)
- [Hexagonal](semester_02/lecture_10_architectural_patterns/hexagonal/README.md)
- [Mvc](semester_02/lecture_10_architectural_patterns/mvc/README.md)
- [Mvvm](semester_02/lecture_10_architectural_patterns/mvvm/README.md)

#### 10: Behavioral Patterns

- [Observer](semester_02/lecture_10_behavioral_patterns/observer/README.md)
- [Strategy](semester_02/lecture_10_behavioral_patterns/strategy/README.md)

#### 11: Repository Patterns

- [Data Mapper](semester_02/lecture_11_repository_patterns/data_mapper/README.md)
- [Repository](semester_02/lecture_11_repository_patterns/repository/README.md)
- [Unit Of Work](semester_02/lecture_11_repository_patterns/unit_of_work/README.md)

#### 12: Concurrency Patterns

- [Producer Consumer](semester_02/lecture_12_concurrency_patterns/producer_consumer/README.md)
- [Readers Writers](semester_02/lecture_12_concurrency_patterns/readers_writers/README.md)
- [Thread Pool](semester_02/lecture_12_concurrency_patterns/thread_pool/README.md)

### Semester 3

#### 10: Graph Algorithms

- [Bellman Ford](semester_03/lecture_10_graph_algorithms/bellman_ford/README.md)
- [Bfs](semester_03/lecture_10_graph_algorithms/bfs/README.md)
- [Dfs](semester_03/lecture_10_graph_algorithms/dfs/README.md)
- [Dijkstra](semester_03/lecture_10_graph_algorithms/dijkstra/README.md)
- [Floyd Warshall](semester_03/lecture_10_graph_algorithms/floyd_warshall/README.md)

#### 11: Dynamic Programming

- [Edit Distance](semester_03/lecture_11_dynamic_programming/edit_distance/README.md)
- [Fibonacci](semester_03/lecture_11_dynamic_programming/fibonacci/README.md)
- [Knapsack](semester_03/lecture_11_dynamic_programming/knapsack/README.md)
- [Longest Common Subsequence](semester_03/lecture_11_dynamic_programming/longest_common_subsequence/README.md)

#### 12: Ml Algorithms

- [Decision Tree](semester_03/lecture_12_ml_algorithms/decision_tree/README.md)
- [Kmeans](semester_03/lecture_12_ml_algorithms/kmeans/README.md)
- [Knn](semester_03/lecture_12_ml_algorithms/knn/README.md)
- [Linear Regression](semester_03/lecture_12_ml_algorithms/linear_regression/README.md)
- [Logistic Regression](semester_03/lecture_12_ml_algorithms/logistic_regression/README.md)
- [Naive Bayes](semester_03/lecture_12_ml_algorithms/naive_bayes/README.md)
- [Svm](semester_03/lecture_12_ml_algorithms/svm/README.md)

#### 13: Clustering

- [K Means](semester_03/lecture_13_clustering/k_means/README.md)

#### 13: Integration Patterns

- [Cqrs](semester_03/lecture_13_integration_patterns/cqrs/README.md)
- [Event Sourcing](semester_03/lecture_13_integration_patterns/event_sourcing/README.md)
- [Message Queue](semester_03/lecture_13_integration_patterns/message_queue/README.md)
- [Publish Subscribe](semester_03/lecture_13_integration_patterns/publish_subscribe/README.md)

#### 14: String Algorithms

- [Boyer Moore](semester_03/lecture_14_string_algorithms/boyer_moore/README.md)
- [Kmp](semester_03/lecture_14_string_algorithms/kmp/README.md)
- [Rabin Karp](semester_03/lecture_14_string_algorithms/rabin_karp/README.md)

#### 15: Greedy Algorithms

- [Activity Selection](semester_03/lecture_15_greedy_algorithms/activity_selection/README.md)
- [Fractional Knapsack](semester_03/lecture_15_greedy_algorithms/fractional_knapsack/README.md)
- [Huffman](semester_03/lecture_15_greedy_algorithms/huffman/README.md)

#### 16: Advanced Ml

- [Gradient Descent](semester_03/lecture_16_advanced_ml/gradient_descent/README.md)
- [Neural Network](semester_03/lecture_16_advanced_ml/neural_network/README.md)
- [Random Forest](semester_03/lecture_16_advanced_ml/random_forest/README.md)
- [Svm](semester_03/lecture_16_advanced_ml/svm/README.md)

### Semester 4

#### 14: Security Patterns

- [Authentication](semester_04/lecture_14_security_patterns/authentication/README.md)
- [Authorization](semester_04/lecture_14_security_patterns/authorization/README.md)
- [Encryption](semester_04/lecture_14_security_patterns/encryption/README.md)
- [Jwt](semester_04/lecture_14_security_patterns/jwt/README.md)
- [Oauth](semester_04/lecture_14_security_patterns/oauth/README.md)

#### 15: Testing Patterns

- [Integration Testing](semester_04/lecture_15_testing_patterns/integration_testing/README.md)
- [Mocking](semester_04/lecture_15_testing_patterns/mocking/README.md)
- [Tdd](semester_04/lecture_15_testing_patterns/tdd/README.md)
- [Unit Testing](semester_04/lecture_15_testing_patterns/unit_testing/README.md)

#### 16: Deployment Patterns

- [Blue Green](semester_04/lecture_16_deployment_patterns/blue_green/README.md)
- [Canary](semester_04/lecture_16_deployment_patterns/canary/README.md)
- [Circuit Breaker](semester_04/lecture_16_deployment_patterns/circuit_breaker/README.md)
- [Retry Pattern](semester_04/lecture_16_deployment_patterns/retry_pattern/README.md)

#### 17: Performance

- [Caching](semester_04/lecture_17_performance/caching/README.md)
- [Load Balancing](semester_04/lecture_17_performance/load_balancing/README.md)
- [Rate Limiting](semester_04/lecture_17_performance/rate_limiting/README.md)

#### 18: Crypto Algorithms

- [Aes](semester_04/lecture_18_crypto_algorithms/aes/README.md)
- [Bcrypt](semester_04/lecture_18_crypto_algorithms/bcrypt/README.md)
- [Rsa](semester_04/lecture_18_crypto_algorithms/rsa/README.md)
- [Sha256](semester_04/lecture_18_crypto_algorithms/sha256/README.md)

#### 19: Distributed Patterns

- [Consistent Hashing](semester_04/lecture_19_distributed_patterns/consistent_hashing/README.md)
- [Gossip Protocol](semester_04/lecture_19_distributed_patterns/gossip_protocol/README.md)
- [Leader Election](semester_04/lecture_19_distributed_patterns/leader_election/README.md)
- [Two Phase Commit](semester_04/lecture_19_distributed_patterns/two_phase_commit/README.md)

#### 20: Monitoring Observability

- [Distributed Tracing](semester_04/lecture_20_monitoring_observability/distributed_tracing/README.md)
- [Log Aggregation](semester_04/lecture_20_monitoring_observability/log_aggregation/README.md)
- [Metrics Collection](semester_04/lecture_20_monitoring_observability/metrics_collection/README.md)

### Semester 5

#### 21: Transfer Learning

- [Feature Extraction](semester_05/lecture_21_transfer_learning/feature_extraction/README.md)
- [Fine Tuning](semester_05/lecture_21_transfer_learning/fine_tuning/README.md)
- [Transfer Learning](semester_05/lecture_21_transfer_learning/transfer_learning/README.md)

#### 22: Cnn Architectures

- [Efficientnet](semester_05/lecture_22_cnn_architectures/efficientnet/README.md)
- [Inception](semester_05/lecture_22_cnn_architectures/inception/README.md)
- [Resnet](semester_05/lecture_22_cnn_architectures/resnet/README.md)
- [Vgg](semester_05/lecture_22_cnn_architectures/vgg/README.md)

#### 23: Object Detection

- [Rcnn](semester_05/lecture_23_object_detection/rcnn/README.md)
- [Ssd](semester_05/lecture_23_object_detection/ssd/README.md)
- [Yolo](semester_05/lecture_23_object_detection/yolo/README.md)

#### 24: Segmentation

- [Fcn](semester_05/lecture_24_segmentation/fcn/README.md)
- [Mask Rcnn](semester_05/lecture_24_segmentation/mask_rcnn/README.md)
- [Unet](semester_05/lecture_24_segmentation/unet/README.md)

#### 25: Transformers

- [Attention](semester_05/lecture_25_transformers/attention/README.md)
- [Bert](semester_05/lecture_25_transformers/bert/README.md)
- [Gpt](semester_05/lecture_25_transformers/gpt/README.md)
- [Transformer](semester_05/lecture_25_transformers/transformer/README.md)

#### 26: Ensemble Methods

- [Bagging](semester_05/lecture_26_ensemble_methods/bagging/README.md)
- [Boosting](semester_05/lecture_26_ensemble_methods/boosting/README.md)
- [Stacking](semester_05/lecture_26_ensemble_methods/stacking/README.md)

#### 27: Hyperparameter Optimization

- [Bayesian Optimization](semester_05/lecture_27_hyperparameter_optimization/bayesian_optimization/README.md)
- [Grid Search](semester_05/lecture_27_hyperparameter_optimization/grid_search/README.md)
- [Optuna](semester_05/lecture_27_hyperparameter_optimization/optuna/README.md)
- [Random Search](semester_05/lecture_27_hyperparameter_optimization/random_search/README.md)

#### 28: Reinforcement Learning

- [Actor Critic](semester_05/lecture_28_reinforcement_learning/actor_critic/README.md)
- [Dqn](semester_05/lecture_28_reinforcement_learning/dqn/README.md)
- [Policy Gradient](semester_05/lecture_28_reinforcement_learning/policy_gradient/README.md)
- [Ppo](semester_05/lecture_28_reinforcement_learning/ppo/README.md)
- [Q Learning](semester_05/lecture_28_reinforcement_learning/q_learning/README.md)

#### 29: Nlp Advanced

- [Glove](semester_05/lecture_29_nlp_advanced/glove/README.md)
- [Ner](semester_05/lecture_29_nlp_advanced/ner/README.md)
- [Seq2Seq](semester_05/lecture_29_nlp_advanced/seq2seq/README.md)
- [Word2Vec](semester_05/lecture_29_nlp_advanced/word2vec/README.md)

#### 30: Time Series

- [Arima](semester_05/lecture_30_time_series/arima/README.md)
- [Lstm Timeseries](semester_05/lecture_30_time_series/lstm_timeseries/README.md)
- [Prophet](semester_05/lecture_30_time_series/prophet/README.md)

### Semester 6

#### 31: Mlops

- [Ab Testing](semester_06/lecture_31_mlops/ab_testing/README.md)
- [Data Drift](semester_06/lecture_31_mlops/data_drift/README.md)
- [Feature Store](semester_06/lecture_31_mlops/feature_store/README.md)
- [Model Monitoring](semester_06/lecture_31_mlops/model_monitoring/README.md)
- [Model Versioning](semester_06/lecture_31_mlops/model_versioning/README.md)

#### 32: Distributed Ml

- [Allreduce](semester_06/lecture_32_distributed_ml/allreduce/README.md)
- [Data Parallelism](semester_06/lecture_32_distributed_ml/data_parallelism/README.md)
- [Federated Learning](semester_06/lecture_32_distributed_ml/federated_learning/README.md)
- [Model Parallelism](semester_06/lecture_32_distributed_ml/model_parallelism/README.md)
- [Parameter Server](semester_06/lecture_32_distributed_ml/parameter_server/README.md)

#### 33: Model Optimization

- [Knowledge Distillation](semester_06/lecture_33_model_optimization/knowledge_distillation/README.md)
- [Nas](semester_06/lecture_33_model_optimization/nas/README.md)
- [Onnx](semester_06/lecture_33_model_optimization/onnx/README.md)
- [Pruning](semester_06/lecture_33_model_optimization/pruning/README.md)
- [Quantization](semester_06/lecture_33_model_optimization/quantization/README.md)
- [Tensorrt](semester_06/lecture_33_model_optimization/tensorrt/README.md)

#### 34: Edge Ai

- [Edge Deployment](semester_06/lecture_34_edge_ai/edge_deployment/README.md)
- [Iot Ml](semester_06/lecture_34_edge_ai/iot_ml/README.md)
- [Mobile Optimization](semester_06/lecture_34_edge_ai/mobile_optimization/README.md)
- [Tflite](semester_06/lecture_34_edge_ai/tflite/README.md)

#### 35: Deployment Patterns

- [Blue Green Ml](semester_06/lecture_35_deployment_patterns/blue_green_ml/README.md)
- [Canary Ml](semester_06/lecture_35_deployment_patterns/canary_ml/README.md)
- [Multi Armed Bandit](semester_06/lecture_35_deployment_patterns/multi_armed_bandit/README.md)
- [Shadow Deployment](semester_06/lecture_35_deployment_patterns/shadow_deployment/README.md)

#### 36: Inference Optimization

- [Batch Inference](semester_06/lecture_36_inference_optimization/batch_inference/README.md)
- [Gpu Optimization](semester_06/lecture_36_inference_optimization/gpu_optimization/README.md)
- [Inference Pipeline](semester_06/lecture_36_inference_optimization/inference_pipeline/README.md)
- [Model Caching](semester_06/lecture_36_inference_optimization/model_caching/README.md)

#### 37: Cost Optimization

- [Autoscaling](semester_06/lecture_37_cost_optimization/autoscaling/README.md)
- [Cost Analysis](semester_06/lecture_37_cost_optimization/cost_analysis/README.md)
- [Serverless Ml](semester_06/lecture_37_cost_optimization/serverless_ml/README.md)
- [Spot Instances](semester_06/lecture_37_cost_optimization/spot_instances/README.md)

#### 38: Monitoring Production

- [Alerting](semester_06/lecture_38_monitoring_production/alerting/README.md)
- [Grafana Dashboards](semester_06/lecture_38_monitoring_production/grafana_dashboards/README.md)
- [Performance Profiling](semester_06/lecture_38_monitoring_production/performance_profiling/README.md)
- [Prometheus Ml](semester_06/lecture_38_monitoring_production/prometheus_ml/README.md)

### Semester 7

#### 39: Operating Systems

- [Deadlock Detection](semester_07/lecture_39_operating_systems/deadlock_detection/README.md)
- [File Systems](semester_07/lecture_39_operating_systems/file_systems/README.md)
- [Interrupt Handling](semester_07/lecture_39_operating_systems/interrupt_handling/README.md)
- [Memory Management](semester_07/lecture_39_operating_systems/memory_management/README.md)
- [Process Scheduling](semester_07/lecture_39_operating_systems/process_scheduling/README.md)
- [Virtual Memory](semester_07/lecture_39_operating_systems/virtual_memory/README.md)

#### 40: Llm Fundamentals

- [Attention Mechanisms](semester_07/lecture_40_llm_fundamentals/attention_mechanisms/README.md)
- [Fine Tuning Llm](semester_07/lecture_40_llm_fundamentals/fine_tuning_llm/README.md)
- [Llm Architecture](semester_07/lecture_40_llm_fundamentals/llm_architecture/README.md)
- [Prompt Engineering](semester_07/lecture_40_llm_fundamentals/prompt_engineering/README.md)
- [Retrieval Augmented Generation](semester_07/lecture_40_llm_fundamentals/retrieval_augmented_generation/README.md)
- [Tokenization](semester_07/lecture_40_llm_fundamentals/tokenization/README.md)

#### 41: Llm Advanced

- [Chain Of Thought](semester_07/lecture_41_llm_advanced/chain_of_thought/README.md)
- [Few Shot Learning](semester_07/lecture_41_llm_advanced/few_shot_learning/README.md)
- [Instruction Tuning](semester_07/lecture_41_llm_advanced/instruction_tuning/README.md)
- [Llm Distillation](semester_07/lecture_41_llm_advanced/llm_distillation/README.md)
- [Llm Quantization](semester_07/lecture_41_llm_advanced/llm_quantization/README.md)
- [Reinforcement Learning Hf](semester_07/lecture_41_llm_advanced/reinforcement_learning_hf/README.md)

#### 42: Ci Cd Fundamentals

- [Build Automation](semester_07/lecture_42_ci_cd_fundamentals/build_automation/README.md)
- [Continuous Deployment](semester_07/lecture_42_ci_cd_fundamentals/continuous_deployment/README.md)
- [Continuous Integration](semester_07/lecture_42_ci_cd_fundamentals/continuous_integration/README.md)
- [Deployment Strategies](semester_07/lecture_42_ci_cd_fundamentals/deployment_strategies/README.md)
- [Pipeline Automation](semester_07/lecture_42_ci_cd_fundamentals/pipeline_automation/README.md)
- [Test Automation](semester_07/lecture_42_ci_cd_fundamentals/test_automation/README.md)

#### 43: Ci Cd Advanced

- [Blue Green Deployment](semester_07/lecture_43_ci_cd_advanced/blue_green_deployment/README.md)
- [Canary Deployment](semester_07/lecture_43_ci_cd_advanced/canary_deployment/README.md)
- [Chaos Engineering](semester_07/lecture_43_ci_cd_advanced/chaos_engineering/README.md)
- [Feature Flags](semester_07/lecture_43_ci_cd_advanced/feature_flags/README.md)
- [Gitops](semester_07/lecture_43_ci_cd_advanced/gitops/README.md)
- [Infrastructure As Code](semester_07/lecture_43_ci_cd_advanced/infrastructure_as_code/README.md)

#### 44: Quantum Computing

- [Grover Algorithm](semester_07/lecture_44_quantum_computing/grover_algorithm/README.md)
- [Quantum Algorithms](semester_07/lecture_44_quantum_computing/quantum_algorithms/README.md)
- [Quantum Entanglement](semester_07/lecture_44_quantum_computing/quantum_entanglement/README.md)
- [Quantum Gates](semester_07/lecture_44_quantum_computing/quantum_gates/README.md)
- [Quantum Superposition](semester_07/lecture_44_quantum_computing/quantum_superposition/README.md)
- [Shor Algorithm](semester_07/lecture_44_quantum_computing/shor_algorithm/README.md)

#### 45: Blockchain Fundamentals

- [Blockchain Structure](semester_07/lecture_45_blockchain_fundamentals/blockchain_structure/README.md)
- [Consensus Mechanisms](semester_07/lecture_45_blockchain_fundamentals/consensus_mechanisms/README.md)
- [Merkle Trees](semester_07/lecture_45_blockchain_fundamentals/merkle_trees/README.md)
- [Proof Of Stake](semester_07/lecture_45_blockchain_fundamentals/proof_of_stake/README.md)
- [Proof Of Work](semester_07/lecture_45_blockchain_fundamentals/proof_of_work/README.md)
- [Smart Contracts](semester_07/lecture_45_blockchain_fundamentals/smart_contracts/README.md)

#### 46: Blockchain Advanced

- [Blockchain Scalability](semester_07/lecture_46_blockchain_advanced/blockchain_scalability/README.md)
- [Cross Chain](semester_07/lecture_46_blockchain_advanced/cross_chain/README.md)
- [Cryptocurrency Wallets](semester_07/lecture_46_blockchain_advanced/cryptocurrency_wallets/README.md)
- [Decentralized Storage](semester_07/lecture_46_blockchain_advanced/decentralized_storage/README.md)
- [Layer2 Solutions](semester_07/lecture_46_blockchain_advanced/layer2_solutions/README.md)
- [Nft Standards](semester_07/lecture_46_blockchain_advanced/nft_standards/README.md)

### Semester 8

#### 47: Support Systems

- [Customer Support Automation](semester_08/lecture_47_support_systems/customer_support_automation/README.md)
- [Escalation Procedures](semester_08/lecture_47_support_systems/escalation_procedures/README.md)
- [Incident Response](semester_08/lecture_47_support_systems/incident_response/README.md)
- [Knowledge Base](semester_08/lecture_47_support_systems/knowledge_base/README.md)
- [Sla Management](semester_08/lecture_47_support_systems/sla_management/README.md)
- [Ticket Management](semester_08/lecture_47_support_systems/ticket_management/README.md)

#### 48: Documentation

- [Api Documentation](semester_08/lecture_48_documentation/api_documentation/README.md)
- [Code Documentation](semester_08/lecture_48_documentation/code_documentation/README.md)
- [Documentation Generation](semester_08/lecture_48_documentation/documentation_generation/README.md)
- [Technical Writing](semester_08/lecture_48_documentation/technical_writing/README.md)
- [User Guides](semester_08/lecture_48_documentation/user_guides/README.md)
- [Version Control Docs](semester_08/lecture_48_documentation/version_control_docs/README.md)

#### 49: Sql Fundamentals

- [Indexes](semester_08/lecture_49_sql_fundamentals/indexes/README.md)
- [Joins](semester_08/lecture_49_sql_fundamentals/joins/README.md)
- [Sql Queries](semester_08/lecture_49_sql_fundamentals/sql_queries/README.md)
- [Stored Procedures](semester_08/lecture_49_sql_fundamentals/stored_procedures/README.md)
- [Transactions](semester_08/lecture_49_sql_fundamentals/transactions/README.md)
- [Triggers](semester_08/lecture_49_sql_fundamentals/triggers/README.md)

#### 50: Sql Advanced

- [Database Design](semester_08/lecture_50_sql_advanced/database_design/README.md)
- [Denormalization](semester_08/lecture_50_sql_advanced/denormalization/README.md)
- [Normalization](semester_08/lecture_50_sql_advanced/normalization/README.md)
- [Partitioning](semester_08/lecture_50_sql_advanced/partitioning/README.md)
- [Query Optimization](semester_08/lecture_50_sql_advanced/query_optimization/README.md)
- [Replication](semester_08/lecture_50_sql_advanced/replication/README.md)

#### 51: Nosql Fundamentals

- [Column Family](semester_08/lecture_51_nosql_fundamentals/column_family/README.md)
- [Document Databases](semester_08/lecture_51_nosql_fundamentals/document_databases/README.md)
- [Graph Databases](semester_08/lecture_51_nosql_fundamentals/graph_databases/README.md)
- [Key Value Stores](semester_08/lecture_51_nosql_fundamentals/key_value_stores/README.md)
- [Nosql Indexing](semester_08/lecture_51_nosql_fundamentals/nosql_indexing/README.md)
- [Nosql Querying](semester_08/lecture_51_nosql_fundamentals/nosql_querying/README.md)

#### 52: Nosql Advanced

- [Hybrid Databases](semester_08/lecture_52_nosql_advanced/hybrid_databases/README.md)
- [Nosql Consistency](semester_08/lecture_52_nosql_advanced/nosql_consistency/README.md)
- [Nosql Migration](semester_08/lecture_52_nosql_advanced/nosql_migration/README.md)
- [Nosql Replication](semester_08/lecture_52_nosql_advanced/nosql_replication/README.md)
- [Nosql Scalability](semester_08/lecture_52_nosql_advanced/nosql_scalability/README.md)
- [Nosql Sharding](semester_08/lecture_52_nosql_advanced/nosql_sharding/README.md)

#### 53: Database Operations

- [Backup Strategies](semester_08/lecture_53_database_operations/backup_strategies/README.md)
- [Capacity Planning](semester_08/lecture_53_database_operations/capacity_planning/README.md)
- [Database Monitoring](semester_08/lecture_53_database_operations/database_monitoring/README.md)
- [Database Security](semester_08/lecture_53_database_operations/database_security/README.md)
- [Disaster Recovery](semester_08/lecture_53_database_operations/disaster_recovery/README.md)
- [Performance Tuning](semester_08/lecture_53_database_operations/performance_tuning/README.md)

#### 54: Data Modeling

- [Data Governance](semester_08/lecture_54_data_modeling/data_governance/README.md)
- [Data Lakes](semester_08/lecture_54_data_modeling/data_lakes/README.md)
- [Data Warehousing](semester_08/lecture_54_data_modeling/data_warehousing/README.md)
- [Dimensional Modeling](semester_08/lecture_54_data_modeling/dimensional_modeling/README.md)
- [Entity Relationship](semester_08/lecture_54_data_modeling/entity_relationship/README.md)
- [Etl Processes](semester_08/lecture_54_data_modeling/etl_processes/README.md)

### Semester 9

#### 55: Advanced Os

- [Container Runtimes](semester_09/lecture_55_advanced_os/container_runtimes/README.md)
- [Distributed Os](semester_09/lecture_55_advanced_os/distributed_os/README.md)
- [Exokernel Design](semester_09/lecture_55_advanced_os/exokernel_design/README.md)
- [Microkernel Architecture](semester_09/lecture_55_advanced_os/microkernel_architecture/README.md)
- [Os Security Models](semester_09/lecture_55_advanced_os/os_security_models/README.md)
- [Real Time Systems](semester_09/lecture_55_advanced_os/real_time_systems/README.md)

#### 56: Os Performance

- [Cache Optimization](semester_09/lecture_56_os_performance/cache_optimization/README.md)
- [Cpu Scheduling Advanced](semester_09/lecture_56_os_performance/cpu_scheduling_advanced/README.md)
- [Io Scheduling](semester_09/lecture_56_os_performance/io_scheduling/README.md)
- [Kernel Tuning](semester_09/lecture_56_os_performance/kernel_tuning/README.md)
- [Memory Optimization](semester_09/lecture_56_os_performance/memory_optimization/README.md)
- [Performance Profiling](semester_09/lecture_56_os_performance/performance_profiling/README.md)

#### 57: Concurrency Advanced

- [Actor Model](semester_09/lecture_57_concurrency_advanced/actor_model/README.md)
- [Concurrent Data Structures](semester_09/lecture_57_concurrency_advanced/concurrent_data_structures/README.md)
- [Csp Model](semester_09/lecture_57_concurrency_advanced/csp_model/README.md)
- [Lock Free Data Structures](semester_09/lecture_57_concurrency_advanced/lock_free_data_structures/README.md)
- [Transactional Memory](semester_09/lecture_57_concurrency_advanced/transactional_memory/README.md)
- [Wait Free Algorithms](semester_09/lecture_57_concurrency_advanced/wait_free_algorithms/README.md)

#### 58: Parallel Computing

- [Gpu Computing](semester_09/lecture_58_parallel_computing/gpu_computing/README.md)
- [Parallel Algorithms](semester_09/lecture_58_parallel_computing/parallel_algorithms/README.md)
- [Parallel Prefix](semester_09/lecture_58_parallel_computing/parallel_prefix/README.md)
- [Parallel Reduction](semester_09/lecture_58_parallel_computing/parallel_reduction/README.md)
- [Simd Optimization](semester_09/lecture_58_parallel_computing/simd_optimization/README.md)
- [Vectorization](semester_09/lecture_58_parallel_computing/vectorization/README.md)

#### 59: Distributed Systems Advanced

- [Byzantine Fault Tolerance](semester_09/lecture_59_distributed_systems_advanced/byzantine_fault_tolerance/README.md)
- [Consensus Algorithms](semester_09/lecture_59_distributed_systems_advanced/consensus_algorithms/README.md)
- [Crdt](semester_09/lecture_59_distributed_systems_advanced/crdt/README.md)
- [Distributed Transactions](semester_09/lecture_59_distributed_systems_advanced/distributed_transactions/README.md)
- [Eventual Consistency](semester_09/lecture_59_distributed_systems_advanced/eventual_consistency/README.md)
- [Vector Clocks](semester_09/lecture_59_distributed_systems_advanced/vector_clocks/README.md)

#### 60: System Design Advanced

- [Api Gateway](semester_09/lecture_60_system_design_advanced/api_gateway/README.md)
- [Cqrs Advanced](semester_09/lecture_60_system_design_advanced/cqrs_advanced/README.md)
- [Event Driven Architecture](semester_09/lecture_60_system_design_advanced/event_driven_architecture/README.md)
- [Event Sourcing Advanced](semester_09/lecture_60_system_design_advanced/event_sourcing_advanced/README.md)
- [Microservices Architecture](semester_09/lecture_60_system_design_advanced/microservices_architecture/README.md)
- [Service Mesh](semester_09/lecture_60_system_design_advanced/service_mesh/README.md)

#### 61: Cloud Native

- [Config Management](semester_09/lecture_61_cloud_native/config_management/README.md)
- [Container Orchestration](semester_09/lecture_61_cloud_native/container_orchestration/README.md)
- [Function As Service](semester_09/lecture_61_cloud_native/function_as_service/README.md)
- [Secrets Management](semester_09/lecture_61_cloud_native/secrets_management/README.md)
- [Serverless Architecture](semester_09/lecture_61_cloud_native/serverless_architecture/README.md)
- [Service Discovery](semester_09/lecture_61_cloud_native/service_discovery/README.md)

#### 62: Observability Advanced

- [Apm](semester_09/lecture_62_observability_advanced/apm/README.md)
- [Chaos Engineering Advanced](semester_09/lecture_62_observability_advanced/chaos_engineering_advanced/README.md)
- [Distributed Tracing](semester_09/lecture_62_observability_advanced/distributed_tracing/README.md)
- [Log Aggregation Advanced](semester_09/lecture_62_observability_advanced/log_aggregation_advanced/README.md)
- [Metrics Collection](semester_09/lecture_62_observability_advanced/metrics_collection/README.md)
- [Synthetic Monitoring](semester_09/lecture_62_observability_advanced/synthetic_monitoring/README.md)

### Semester 10

#### 63: Ai Advanced

- [Continual Learning](semester_10/lecture_63_ai_advanced/continual_learning/README.md)
- [Few Shot Learning Advanced](semester_10/lecture_63_ai_advanced/few_shot_learning_advanced/README.md)
- [Lifelong Learning](semester_10/lecture_63_ai_advanced/lifelong_learning/README.md)
- [Meta Learning](semester_10/lecture_63_ai_advanced/meta_learning/README.md)
- [Transfer Learning Advanced](semester_10/lecture_63_ai_advanced/transfer_learning_advanced/README.md)
- [Zero Shot Learning](semester_10/lecture_63_ai_advanced/zero_shot_learning/README.md)

#### 64: Llm Architecture Advanced

- [Llm Compression](semester_10/lecture_64_llm_architecture_advanced/llm_compression/README.md)
- [Long Context Models](semester_10/lecture_64_llm_architecture_advanced/long_context_models/README.md)
- [Mixture Of Experts](semester_10/lecture_64_llm_architecture_advanced/mixture_of_experts/README.md)
- [Multimodal Llms](semester_10/lecture_64_llm_architecture_advanced/multimodal_llms/README.md)
- [Sparse Attention](semester_10/lecture_64_llm_architecture_advanced/sparse_attention/README.md)
- [Transformer Optimization](semester_10/lecture_64_llm_architecture_advanced/transformer_optimization/README.md)

#### 65: Llm Training Advanced

- [Distributed Training Llm](semester_10/lecture_65_llm_training_advanced/distributed_training_llm/README.md)
- [Gradient Checkpointing](semester_10/lecture_65_llm_training_advanced/gradient_checkpointing/README.md)
- [Mixed Precision Training](semester_10/lecture_65_llm_training_advanced/mixed_precision_training/README.md)
- [Model Parallelism](semester_10/lecture_65_llm_training_advanced/model_parallelism/README.md)
- [Pipeline Parallelism](semester_10/lecture_65_llm_training_advanced/pipeline_parallelism/README.md)
- [Tensor Parallelism](semester_10/lecture_65_llm_training_advanced/tensor_parallelism/README.md)

#### 66: Llm Inference

- [Batch Inference](semester_10/lecture_66_llm_inference/batch_inference/README.md)
- [Continuous Batching](semester_10/lecture_66_llm_inference/continuous_batching/README.md)
- [Kv Cache Optimization](semester_10/lecture_66_llm_inference/kv_cache_optimization/README.md)
- [Pruning Inference](semester_10/lecture_66_llm_inference/pruning_inference/README.md)
- [Quantization Inference](semester_10/lecture_66_llm_inference/quantization_inference/README.md)
- [Speculative Decoding](semester_10/lecture_66_llm_inference/speculative_decoding/README.md)

#### 67: Rag Advanced

- [Agentic Rag](semester_10/lecture_67_rag_advanced/agentic_rag/README.md)
- [Context Compression](semester_10/lecture_67_rag_advanced/context_compression/README.md)
- [Hybrid Search](semester_10/lecture_67_rag_advanced/hybrid_search/README.md)
- [Multi Hop Rag](semester_10/lecture_67_rag_advanced/multi_hop_rag/README.md)
- [Query Expansion](semester_10/lecture_67_rag_advanced/query_expansion/README.md)
- [Reranking](semester_10/lecture_67_rag_advanced/reranking/README.md)

#### 68: Llm Evaluation

- [Adversarial Testing](semester_10/lecture_68_llm_evaluation/adversarial_testing/README.md)
- [Benchmark Suites](semester_10/lecture_68_llm_evaluation/benchmark_suites/README.md)
- [Bias Detection](semester_10/lecture_68_llm_evaluation/bias_detection/README.md)
- [Evaluation Metrics](semester_10/lecture_68_llm_evaluation/evaluation_metrics/README.md)
- [Human Evaluation](semester_10/lecture_68_llm_evaluation/human_evaluation/README.md)
- [Safety Evaluation](semester_10/lecture_68_llm_evaluation/safety_evaluation/README.md)

#### 69: Ai Ethics

- [Adversarial Robustness](semester_10/lecture_69_ai_ethics/adversarial_robustness/README.md)
- [Ai Safety](semester_10/lecture_69_ai_ethics/ai_safety/README.md)
- [Bias Mitigation](semester_10/lecture_69_ai_ethics/bias_mitigation/README.md)
- [Explainability](semester_10/lecture_69_ai_ethics/explainability/README.md)
- [Fairness Algorithms](semester_10/lecture_69_ai_ethics/fairness_algorithms/README.md)
- [Interpretability](semester_10/lecture_69_ai_ethics/interpretability/README.md)

#### 70: Ai Governance

- [Audit Trails](semester_10/lecture_70_ai_governance/audit_trails/README.md)
- [Compliance Frameworks](semester_10/lecture_70_ai_governance/compliance_frameworks/README.md)
- [Data Governance Ai](semester_10/lecture_70_ai_governance/data_governance_ai/README.md)
- [Model Governance](semester_10/lecture_70_ai_governance/model_governance/README.md)
- [Model Registry](semester_10/lecture_70_ai_governance/model_registry/README.md)
- [Risk Assessment](semester_10/lecture_70_ai_governance/risk_assessment/README.md)

### Semester 11

#### 71: Cicd Advanced

- [Conditional Execution](semester_11/lecture_71_cicd_advanced/conditional_execution/README.md)
- [Dynamic Pipelines](semester_11/lecture_71_cicd_advanced/dynamic_pipelines/README.md)
- [Multi Stage Pipelines](semester_11/lecture_71_cicd_advanced/multi_stage_pipelines/README.md)
- [Parallel Pipelines](semester_11/lecture_71_cicd_advanced/parallel_pipelines/README.md)
- [Pipeline Optimization](semester_11/lecture_71_cicd_advanced/pipeline_optimization/README.md)
- [Pipeline Templates](semester_11/lecture_71_cicd_advanced/pipeline_templates/README.md)

#### 72: Infrastructure Advanced

- [Cost Optimization](semester_11/lecture_72_infrastructure_advanced/cost_optimization/README.md)
- [Edge Computing](semester_11/lecture_72_infrastructure_advanced/edge_computing/README.md)
- [Hybrid Cloud](semester_11/lecture_72_infrastructure_advanced/hybrid_cloud/README.md)
- [Infrastructure Monitoring](semester_11/lecture_72_infrastructure_advanced/infrastructure_monitoring/README.md)
- [Infrastructure Patterns](semester_11/lecture_72_infrastructure_advanced/infrastructure_patterns/README.md)
- [Multi Cloud Strategies](semester_11/lecture_72_infrastructure_advanced/multi_cloud_strategies/README.md)

#### 73: Security Devops

- [Compliance Automation](semester_11/lecture_73_security_devops/compliance_automation/README.md)
- [Secrets Rotation](semester_11/lecture_73_security_devops/secrets_rotation/README.md)
- [Security Scanning](semester_11/lecture_73_security_devops/security_scanning/README.md)
- [Security Testing](semester_11/lecture_73_security_devops/security_testing/README.md)
- [Threat Modeling](semester_11/lecture_73_security_devops/threat_modeling/README.md)
- [Vulnerability Management](semester_11/lecture_73_security_devops/vulnerability_management/README.md)

#### 74: Automation Advanced

- [Auto Scaling Advanced](semester_11/lecture_74_automation_advanced/auto_scaling_advanced/README.md)
- [Automated Remediation](semester_11/lecture_74_automation_advanced/automated_remediation/README.md)
- [Intelligent Automation](semester_11/lecture_74_automation_advanced/intelligent_automation/README.md)
- [Predictive Scaling](semester_11/lecture_74_automation_advanced/predictive_scaling/README.md)
- [Self Healing Systems](semester_11/lecture_74_automation_advanced/self_healing_systems/README.md)
- [Workflow Automation](semester_11/lecture_74_automation_advanced/workflow_automation/README.md)

#### 75: Gitops Advanced

- [Canary Analysis](semester_11/lecture_75_gitops_advanced/canary_analysis/README.md)
- [Environment Management](semester_11/lecture_75_gitops_advanced/environment_management/README.md)
- [Feature Management](semester_11/lecture_75_gitops_advanced/feature_management/README.md)
- [Gitops Patterns](semester_11/lecture_75_gitops_advanced/gitops_patterns/README.md)
- [Gitops Security](semester_11/lecture_75_gitops_advanced/gitops_security/README.md)
- [Progressive Delivery](semester_11/lecture_75_gitops_advanced/progressive_delivery/README.md)

#### 76: Platform Engineering

- [Developer Experience](semester_11/lecture_76_platform_engineering/developer_experience/README.md)
- [Developer Portals](semester_11/lecture_76_platform_engineering/developer_portals/README.md)
- [Internal Developer Platforms](semester_11/lecture_76_platform_engineering/internal_developer_platforms/README.md)
- [Platform Abstraction](semester_11/lecture_76_platform_engineering/platform_abstraction/README.md)
- [Platform Metrics](semester_11/lecture_76_platform_engineering/platform_metrics/README.md)
- [Self Service Platforms](semester_11/lecture_76_platform_engineering/self_service_platforms/README.md)

#### 77: Chaos Engineering Advanced

- [Chaos Automation](semester_11/lecture_77_chaos_engineering_advanced/chaos_automation/README.md)
- [Chaos Experiments](semester_11/lecture_77_chaos_engineering_advanced/chaos_experiments/README.md)
- [Chaos Metrics](semester_11/lecture_77_chaos_engineering_advanced/chaos_metrics/README.md)
- [Fault Injection](semester_11/lecture_77_chaos_engineering_advanced/fault_injection/README.md)
- [Game Day Exercises](semester_11/lecture_77_chaos_engineering_advanced/game_day_exercises/README.md)
- [Resilience Testing](semester_11/lecture_77_chaos_engineering_advanced/resilience_testing/README.md)

#### 78: Observability Platform

- [Aiops](semester_11/lecture_78_observability_platform/aiops/README.md)
- [Anomaly Detection](semester_11/lecture_78_observability_platform/anomaly_detection/README.md)
- [Incident Management](semester_11/lecture_78_observability_platform/incident_management/README.md)
- [Observability Stack](semester_11/lecture_78_observability_platform/observability_stack/README.md)
- [Root Cause Analysis](semester_11/lecture_78_observability_platform/root_cause_analysis/README.md)
- [Unified Observability](semester_11/lecture_78_observability_platform/unified_observability/README.md)

### Semester 12

#### 79: Quantum Algorithms Advanced

- [Quantum Cryptography](semester_12/lecture_79_quantum_algorithms_advanced/quantum_cryptography/README.md)
- [Quantum Error Correction](semester_12/lecture_79_quantum_algorithms_advanced/quantum_error_correction/README.md)
- [Quantum Machine Learning](semester_12/lecture_79_quantum_algorithms_advanced/quantum_machine_learning/README.md)
- [Quantum Optimization](semester_12/lecture_79_quantum_algorithms_advanced/quantum_optimization/README.md)
- [Quantum Simulation](semester_12/lecture_79_quantum_algorithms_advanced/quantum_simulation/README.md)
- [Quantum Teleportation](semester_12/lecture_79_quantum_algorithms_advanced/quantum_teleportation/README.md)

#### 80: Quantum Computing Advanced

- [Quantum Architectures](semester_12/lecture_80_quantum_computing_advanced/quantum_architectures/README.md)
- [Quantum Benchmarking](semester_12/lecture_80_quantum_computing_advanced/quantum_benchmarking/README.md)
- [Quantum Circuits](semester_12/lecture_80_quantum_computing_advanced/quantum_circuits/README.md)
- [Quantum Compilation](semester_12/lecture_80_quantum_computing_advanced/quantum_compilation/README.md)
- [Quantum Networking](semester_12/lecture_80_quantum_computing_advanced/quantum_networking/README.md)
- [Quantum Noise](semester_12/lecture_80_quantum_computing_advanced/quantum_noise/README.md)

#### 81: Quantum Applications

- [Quantum Ai](semester_12/lecture_81_quantum_applications/quantum_ai/README.md)
- [Quantum Chemistry](semester_12/lecture_81_quantum_applications/quantum_chemistry/README.md)
- [Quantum Database](semester_12/lecture_81_quantum_applications/quantum_database/README.md)
- [Quantum Finance](semester_12/lecture_81_quantum_applications/quantum_finance/README.md)
- [Quantum Logistics](semester_12/lecture_81_quantum_applications/quantum_logistics/README.md)
- [Quantum Search](semester_12/lecture_81_quantum_applications/quantum_search/README.md)

#### 82: Hybrid Quantum

- [Quantum Approximate](semester_12/lecture_82_hybrid_quantum/quantum_approximate/README.md)
- [Quantum Classical Hybrid](semester_12/lecture_82_hybrid_quantum/quantum_classical_hybrid/README.md)
- [Quantum Ml Hybrid](semester_12/lecture_82_hybrid_quantum/quantum_ml_hybrid/README.md)
- [Quantum Optimization Hybrid](semester_12/lecture_82_hybrid_quantum/quantum_optimization_hybrid/README.md)
- [Quantum Simulation Hybrid](semester_12/lecture_82_hybrid_quantum/quantum_simulation_hybrid/README.md)
- [Variational Quantum](semester_12/lecture_82_hybrid_quantum/variational_quantum/README.md)

#### 83: Quantum Software

- [Quantum Debugging](semester_12/lecture_83_quantum_software/quantum_debugging/README.md)
- [Quantum Optimization Tools](semester_12/lecture_83_quantum_software/quantum_optimization_tools/README.md)
- [Quantum Programming](semester_12/lecture_83_quantum_software/quantum_programming/README.md)
- [Quantum Software Stack](semester_12/lecture_83_quantum_software/quantum_software_stack/README.md)
- [Quantum Testing](semester_12/lecture_83_quantum_software/quantum_testing/README.md)
- [Quantum Verification](semester_12/lecture_83_quantum_software/quantum_verification/README.md)

#### 84: Quantum Hardware

- [Quantum Calibration](semester_12/lecture_84_quantum_hardware/quantum_calibration/README.md)
- [Quantum Characterization](semester_12/lecture_84_quantum_hardware/quantum_characterization/README.md)
- [Quantum Control](semester_12/lecture_84_quantum_hardware/quantum_control/README.md)
- [Quantum Control Systems](semester_12/lecture_84_quantum_hardware/quantum_control_systems/README.md)
- [Quantum Processors](semester_12/lecture_84_quantum_hardware/quantum_processors/README.md)
- [Quantum Readout](semester_12/lecture_84_quantum_hardware/quantum_readout/README.md)

#### 85: Quantum Networking

- [Quantum Communication](semester_12/lecture_85_quantum_networking/quantum_communication/README.md)
- [Quantum Internet](semester_12/lecture_85_quantum_networking/quantum_internet/README.md)
- [Quantum Key Distribution](semester_12/lecture_85_quantum_networking/quantum_key_distribution/README.md)
- [Quantum Repeaters](semester_12/lecture_85_quantum_networking/quantum_repeaters/README.md)
- [Quantum Routing](semester_12/lecture_85_quantum_networking/quantum_routing/README.md)
- [Quantum Switching](semester_12/lecture_85_quantum_networking/quantum_switching/README.md)

#### 86: Quantum Security

- [Post Quantum Cryptography](semester_12/lecture_86_quantum_security/post_quantum_cryptography/README.md)
- [Quantum Attacks](semester_12/lecture_86_quantum_security/quantum_attacks/README.md)
- [Quantum Defense](semester_12/lecture_86_quantum_security/quantum_defense/README.md)
- [Quantum Key Management](semester_12/lecture_86_quantum_security/quantum_key_management/README.md)
- [Quantum Resistant](semester_12/lecture_86_quantum_security/quantum_resistant/README.md)
- [Quantum Security Protocols](semester_12/lecture_86_quantum_security/quantum_security_protocols/README.md)

### Semester 13

#### 87: Blockchain Advanced

- [Blockchain Scalability Solutions](semester_13/lecture_87_blockchain_advanced/blockchain_scalability_solutions/README.md)
- [Plasma](semester_13/lecture_87_blockchain_advanced/plasma/README.md)
- [Rollups](semester_13/lecture_87_blockchain_advanced/rollups/README.md)
- [Sharding Blockchain](semester_13/lecture_87_blockchain_advanced/sharding_blockchain/README.md)
- [Sidechains](semester_13/lecture_87_blockchain_advanced/sidechains/README.md)
- [State Channels](semester_13/lecture_87_blockchain_advanced/state_channels/README.md)

#### 88: Consensus Advanced

- [Algorand](semester_13/lecture_88_consensus_advanced/algorand/README.md)
- [Dpos Advanced](semester_13/lecture_88_consensus_advanced/dpos_advanced/README.md)
- [Hotstuff](semester_13/lecture_88_consensus_advanced/hotstuff/README.md)
- [Pbft](semester_13/lecture_88_consensus_advanced/pbft/README.md)
- [Raft Blockchain](semester_13/lecture_88_consensus_advanced/raft_blockchain/README.md)
- [Tendermint](semester_13/lecture_88_consensus_advanced/tendermint/README.md)

#### 89: Defi

- [Automated Market Makers](semester_13/lecture_89_defi/automated_market_makers/README.md)
- [Derivatives](semester_13/lecture_89_defi/derivatives/README.md)
- [Lending Protocols](semester_13/lecture_89_defi/lending_protocols/README.md)
- [Liquidity Pools](semester_13/lecture_89_defi/liquidity_pools/README.md)
- [Stablecoins](semester_13/lecture_89_defi/stablecoins/README.md)
- [Yield Farming](semester_13/lecture_89_defi/yield_farming/README.md)

#### 90: Blockchain Security

- [Audit Techniques](semester_13/lecture_90_blockchain_security/audit_techniques/README.md)
- [Exploit Prevention](semester_13/lecture_90_blockchain_security/exploit_prevention/README.md)
- [Formal Verification](semester_13/lecture_90_blockchain_security/formal_verification/README.md)
- [Security Patterns](semester_13/lecture_90_blockchain_security/security_patterns/README.md)
- [Smart Contract Security](semester_13/lecture_90_blockchain_security/smart_contract_security/README.md)
- [Vulnerability Detection](semester_13/lecture_90_blockchain_security/vulnerability_detection/README.md)

#### 91: Blockchain Privacy

- [Confidential Transactions](semester_13/lecture_91_blockchain_privacy/confidential_transactions/README.md)
- [Privacy Coins](semester_13/lecture_91_blockchain_privacy/privacy_coins/README.md)
- [Ring Signatures](semester_13/lecture_91_blockchain_privacy/ring_signatures/README.md)
- [Zero Knowledge Proofs](semester_13/lecture_91_blockchain_privacy/zero_knowledge_proofs/README.md)
- [Zk Snarks](semester_13/lecture_91_blockchain_privacy/zk_snarks/README.md)
- [Zk Starks](semester_13/lecture_91_blockchain_privacy/zk_starks/README.md)

#### 92: Blockchain Interoperability

- [Atomic Swaps](semester_13/lecture_92_blockchain_interoperability/atomic_swaps/README.md)
- [Chain Abstraction](semester_13/lecture_92_blockchain_interoperability/chain_abstraction/README.md)
- [Cross Chain Bridges](semester_13/lecture_92_blockchain_interoperability/cross_chain_bridges/README.md)
- [Interoperability Protocols](semester_13/lecture_92_blockchain_interoperability/interoperability_protocols/README.md)
- [Multi Chain Apps](semester_13/lecture_92_blockchain_interoperability/multi_chain_apps/README.md)
- [Universal Protocols](semester_13/lecture_92_blockchain_interoperability/universal_protocols/README.md)

#### 93: Blockchain Governance

- [Dao Governance](semester_13/lecture_93_blockchain_governance/dao_governance/README.md)
- [Governance Tokens](semester_13/lecture_93_blockchain_governance/governance_tokens/README.md)
- [Proposal Systems](semester_13/lecture_93_blockchain_governance/proposal_systems/README.md)
- [Treasury Management](semester_13/lecture_93_blockchain_governance/treasury_management/README.md)
- [Upgrade Mechanisms](semester_13/lecture_93_blockchain_governance/upgrade_mechanisms/README.md)
- [Voting Mechanisms](semester_13/lecture_93_blockchain_governance/voting_mechanisms/README.md)

#### 94: Blockchain Analytics

- [Address Clustering](semester_13/lecture_94_blockchain_analytics/address_clustering/README.md)
- [Anomaly Detection Blockchain](semester_13/lecture_94_blockchain_analytics/anomaly_detection_blockchain/README.md)
- [Compliance Tools](semester_13/lecture_94_blockchain_analytics/compliance_tools/README.md)
- [Flow Analysis](semester_13/lecture_94_blockchain_analytics/flow_analysis/README.md)
- [On Chain Analytics](semester_13/lecture_94_blockchain_analytics/on_chain_analytics/README.md)
- [Transaction Analysis](semester_13/lecture_94_blockchain_analytics/transaction_analysis/README.md)

### Semester 14

#### 100: Documentation Ai

- [Ai Doc Generation](semester_14/lecture_100_documentation_ai/ai_doc_generation/README.md)
- [Code To Docs](semester_14/lecture_100_documentation_ai/code_to_docs/README.md)
- [Contextual Help](semester_14/lecture_100_documentation_ai/contextual_help/README.md)
- [Intelligent Search](semester_14/lecture_100_documentation_ai/intelligent_search/README.md)
- [Natural Language Docs](semester_14/lecture_100_documentation_ai/natural_language_docs/README.md)
- [Personalized Docs](semester_14/lecture_100_documentation_ai/personalized_docs/README.md)

#### 101: Developer Experience

- [Api Explorer](semester_14/lecture_101_developer_experience/api_explorer/README.md)
- [Developer Portals](semester_14/lecture_101_developer_experience/developer_portals/README.md)
- [Feedback Loops](semester_14/lecture_101_developer_experience/feedback_loops/README.md)
- [Onboarding Automation](semester_14/lecture_101_developer_experience/onboarding_automation/README.md)
- [Sandbox Environments](semester_14/lecture_101_developer_experience/sandbox_environments/README.md)
- [Tutorial Systems](semester_14/lecture_101_developer_experience/tutorial_systems/README.md)

#### 102: Community Management

- [Community Analytics](semester_14/lecture_102_community_management/community_analytics/README.md)
- [Community Platforms](semester_14/lecture_102_community_management/community_platforms/README.md)
- [Contribution Management](semester_14/lecture_102_community_management/contribution_management/README.md)
- [Engagement Metrics](semester_14/lecture_102_community_management/engagement_metrics/README.md)
- [Knowledge Sharing](semester_14/lecture_102_community_management/knowledge_sharing/README.md)
- [Moderation Automation](semester_14/lecture_102_community_management/moderation_automation/README.md)

#### 95: Support Advanced

- [Ai Powered Support](semester_14/lecture_95_support_advanced/ai_powered_support/README.md)
- [Chatbot Advanced](semester_14/lecture_95_support_advanced/chatbot_advanced/README.md)
- [Knowledge Graph](semester_14/lecture_95_support_advanced/knowledge_graph/README.md)
- [Sentiment Analysis](semester_14/lecture_95_support_advanced/sentiment_analysis/README.md)
- [Support Analytics](semester_14/lecture_95_support_advanced/support_analytics/README.md)
- [Ticket Routing Ai](semester_14/lecture_95_support_advanced/ticket_routing_ai/README.md)

#### 96: Incident Management Advanced

- [Alert Fatigue Reduction](semester_14/lecture_96_incident_management_advanced/alert_fatigue_reduction/README.md)
- [Blameless Culture](semester_14/lecture_96_incident_management_advanced/blameless_culture/README.md)
- [Incident Correlation](semester_14/lecture_96_incident_management_advanced/incident_correlation/README.md)
- [Incident Prediction](semester_14/lecture_96_incident_management_advanced/incident_prediction/README.md)
- [Incident Response Automation](semester_14/lecture_96_incident_management_advanced/incident_response_automation/README.md)
- [Postmortem Automation](semester_14/lecture_96_incident_management_advanced/postmortem_automation/README.md)

#### 97: Knowledge Management

- [Content Curation](semester_14/lecture_97_knowledge_management/content_curation/README.md)
- [Knowledge Base Ai](semester_14/lecture_97_knowledge_management/knowledge_base_ai/README.md)
- [Knowledge Extraction](semester_14/lecture_97_knowledge_management/knowledge_extraction/README.md)
- [Knowledge Graph Construction](semester_14/lecture_97_knowledge_management/knowledge_graph_construction/README.md)
- [Knowledge Validation](semester_14/lecture_97_knowledge_management/knowledge_validation/README.md)
- [Semantic Search](semester_14/lecture_97_knowledge_management/semantic_search/README.md)

#### 98: Documentation Advanced

- [Api Docs Advanced](semester_14/lecture_98_documentation_advanced/api_docs_advanced/README.md)
- [Automated Documentation](semester_14/lecture_98_documentation_advanced/automated_documentation/README.md)
- [Doc Analytics](semester_14/lecture_98_documentation_advanced/doc_analytics/README.md)
- [Doc As Code](semester_14/lecture_98_documentation_advanced/doc_as_code/README.md)
- [Documentation Testing](semester_14/lecture_98_documentation_advanced/documentation_testing/README.md)
- [Interactive Docs](semester_14/lecture_98_documentation_advanced/interactive_docs/README.md)

#### 99: Technical Writing Advanced

- [Accessibility Docs](semester_14/lecture_99_technical_writing_advanced/accessibility_docs/README.md)
- [Content Generation](semester_14/lecture_99_technical_writing_advanced/content_generation/README.md)
- [Multimedia Docs](semester_14/lecture_99_technical_writing_advanced/multimedia_docs/README.md)
- [Style Guides](semester_14/lecture_99_technical_writing_advanced/style_guides/README.md)
- [Translation Automation](semester_14/lecture_99_technical_writing_advanced/translation_automation/README.md)
- [Writing Automation](semester_14/lecture_99_technical_writing_advanced/writing_automation/README.md)

### Semester 15

#### 103: Sql Advanced Topics

- [Advanced Joins](semester_15/lecture_103_sql_advanced_topics/advanced_joins/README.md)
- [Common Table Expressions](semester_15/lecture_103_sql_advanced_topics/common_table_expressions/README.md)
- [Pivot Unpivot](semester_15/lecture_103_sql_advanced_topics/pivot_unpivot/README.md)
- [Recursive Queries](semester_15/lecture_103_sql_advanced_topics/recursive_queries/README.md)
- [Sql Analytics](semester_15/lecture_103_sql_advanced_topics/sql_analytics/README.md)
- [Window Functions](semester_15/lecture_103_sql_advanced_topics/window_functions/README.md)

#### 104: Database Performance

- [Index Strategies](semester_15/lecture_104_database_performance/index_strategies/README.md)
- [Materialized Views](semester_15/lecture_104_database_performance/materialized_views/README.md)
- [Partitioning Strategies](semester_15/lecture_104_database_performance/partitioning_strategies/README.md)
- [Query Hints](semester_15/lecture_104_database_performance/query_hints/README.md)
- [Query Optimization Advanced](semester_15/lecture_104_database_performance/query_optimization_advanced/README.md)
- [Statistics Management](semester_15/lecture_104_database_performance/statistics_management/README.md)

#### 105: Database Architecture

- [Database Clustering](semester_15/lecture_105_database_architecture/database_clustering/README.md)
- [Database Federation](semester_15/lecture_105_database_architecture/database_federation/README.md)
- [Database Sharding Advanced](semester_15/lecture_105_database_architecture/database_sharding_advanced/README.md)
- [Multi Tenant Databases](semester_15/lecture_105_database_architecture/multi_tenant_databases/README.md)
- [Read Replicas](semester_15/lecture_105_database_architecture/read_replicas/README.md)
- [Write Scaling](semester_15/lecture_105_database_architecture/write_scaling/README.md)

#### 106: Nosql Advanced Topics

- [Nosql Aggregation](semester_15/lecture_106_nosql_advanced_topics/nosql_aggregation/README.md)
- [Nosql Analytics](semester_15/lecture_106_nosql_advanced_topics/nosql_analytics/README.md)
- [Nosql Consistency Models](semester_15/lecture_106_nosql_advanced_topics/nosql_consistency_models/README.md)
- [Nosql Data Modeling](semester_15/lecture_106_nosql_advanced_topics/nosql_data_modeling/README.md)
- [Nosql Query Optimization](semester_15/lecture_106_nosql_advanced_topics/nosql_query_optimization/README.md)
- [Nosql Transactions](semester_15/lecture_106_nosql_advanced_topics/nosql_transactions/README.md)

#### 107: Time Series Databases

- [Downsampling](semester_15/lecture_107_time_series_databases/downsampling/README.md)
- [Retention Policies](semester_15/lecture_107_time_series_databases/retention_policies/README.md)
- [Time Series Analytics](semester_15/lecture_107_time_series_databases/time_series_analytics/README.md)
- [Time Series Compression](semester_15/lecture_107_time_series_databases/time_series_compression/README.md)
- [Time Series Queries](semester_15/lecture_107_time_series_databases/time_series_queries/README.md)
- [Time Series Storage](semester_15/lecture_107_time_series_databases/time_series_storage/README.md)

#### 108: Graph Databases Advanced

- [Graph Algorithms Db](semester_15/lecture_108_graph_databases_advanced/graph_algorithms_db/README.md)
- [Graph Analytics](semester_15/lecture_108_graph_databases_advanced/graph_analytics/README.md)
- [Graph Ml](semester_15/lecture_108_graph_databases_advanced/graph_ml/README.md)
- [Graph Pattern Matching](semester_15/lecture_108_graph_databases_advanced/graph_pattern_matching/README.md)
- [Graph Traversal](semester_15/lecture_108_graph_databases_advanced/graph_traversal/README.md)
- [Graph Visualization](semester_15/lecture_108_graph_databases_advanced/graph_visualization/README.md)

#### 109: Database Security Advanced

- [Audit Logging](semester_15/lecture_109_database_security_advanced/audit_logging/README.md)
- [Column Level Security](semester_15/lecture_109_database_security_advanced/column_level_security/README.md)
- [Data Masking](semester_15/lecture_109_database_security_advanced/data_masking/README.md)
- [Encryption At Rest](semester_15/lecture_109_database_security_advanced/encryption_at_rest/README.md)
- [Encryption In Transit](semester_15/lecture_109_database_security_advanced/encryption_in_transit/README.md)
- [Row Level Security](semester_15/lecture_109_database_security_advanced/row_level_security/README.md)

#### 110: Database Migration

- [Data Migration](semester_15/lecture_110_database_migration/data_migration/README.md)
- [Migration Strategies](semester_15/lecture_110_database_migration/migration_strategies/README.md)
- [Migration Testing](semester_15/lecture_110_database_migration/migration_testing/README.md)
- [Rollback Strategies](semester_15/lecture_110_database_migration/rollback_strategies/README.md)
- [Schema Migration](semester_15/lecture_110_database_migration/schema_migration/README.md)
- [Zero Downtime Migration](semester_15/lecture_110_database_migration/zero_downtime_migration/README.md)

### Semester 16

#### 111: Data Engineering Advanced

- [Batch Processing Advanced](semester_16/lecture_111_data_engineering_advanced/batch_processing_advanced/README.md)
- [Data Mesh](semester_16/lecture_111_data_engineering_advanced/data_mesh/README.md)
- [Data Pipelines Advanced](semester_16/lecture_111_data_engineering_advanced/data_pipelines_advanced/README.md)
- [Kappa Architecture](semester_16/lecture_111_data_engineering_advanced/kappa_architecture/README.md)
- [Lambda Architecture](semester_16/lecture_111_data_engineering_advanced/lambda_architecture/README.md)
- [Stream Processing Advanced](semester_16/lecture_111_data_engineering_advanced/stream_processing_advanced/README.md)

#### 112: Data Warehousing Advanced

- [Data Vault](semester_16/lecture_112_data_warehousing_advanced/data_vault/README.md)
- [Dimensional Modeling Advanced](semester_16/lecture_112_data_warehousing_advanced/dimensional_modeling_advanced/README.md)
- [Snowflake Schema](semester_16/lecture_112_data_warehousing_advanced/snowflake_schema/README.md)
- [Star Schema](semester_16/lecture_112_data_warehousing_advanced/star_schema/README.md)
- [Warehouse Architecture](semester_16/lecture_112_data_warehousing_advanced/warehouse_architecture/README.md)
- [Warehouse Optimization](semester_16/lecture_112_data_warehousing_advanced/warehouse_optimization/README.md)

#### 113: Data Lakes Advanced

- [Data Cataloging](semester_16/lecture_113_data_lakes_advanced/data_cataloging/README.md)
- [Data Discovery](semester_16/lecture_113_data_lakes_advanced/data_discovery/README.md)
- [Data Lineage](semester_16/lecture_113_data_lakes_advanced/data_lineage/README.md)
- [Data Profiling](semester_16/lecture_113_data_lakes_advanced/data_profiling/README.md)
- [Data Quality](semester_16/lecture_113_data_lakes_advanced/data_quality/README.md)
- [Lakehouse Architecture](semester_16/lecture_113_data_lakes_advanced/lakehouse_architecture/README.md)

#### 114: Real Time Analytics

- [Complex Event Processing](semester_16/lecture_114_real_time_analytics/complex_event_processing/README.md)
- [Real Time Aggregation](semester_16/lecture_114_real_time_analytics/real_time_aggregation/README.md)
- [Real Time Alerts](semester_16/lecture_114_real_time_analytics/real_time_alerts/README.md)
- [Real Time Dashboards](semester_16/lecture_114_real_time_analytics/real_time_dashboards/README.md)
- [Real Time Ml](semester_16/lecture_114_real_time_analytics/real_time_ml/README.md)
- [Streaming Analytics](semester_16/lecture_114_real_time_analytics/streaming_analytics/README.md)

#### 115: Data Governance Advanced

- [Data Catalog](semester_16/lecture_115_data_governance_advanced/data_catalog/README.md)
- [Data Lineage Tracking](semester_16/lecture_115_data_governance_advanced/data_lineage_tracking/README.md)
- [Data Privacy](semester_16/lecture_115_data_governance_advanced/data_privacy/README.md)
- [Data Quality Frameworks](semester_16/lecture_115_data_governance_advanced/data_quality_frameworks/README.md)
- [Data Retention](semester_16/lecture_115_data_governance_advanced/data_retention/README.md)
- [Gdpr Compliance](semester_16/lecture_115_data_governance_advanced/gdpr_compliance/README.md)

#### 116: Data Ops

- [Data Monitoring](semester_16/lecture_116_data_ops/data_monitoring/README.md)
- [Data Observability](semester_16/lecture_116_data_ops/data_observability/README.md)
- [Data Pipeline Ci Cd](semester_16/lecture_116_data_ops/data_pipeline_ci_cd/README.md)
- [Data Reliability](semester_16/lecture_116_data_ops/data_reliability/README.md)
- [Data Testing](semester_16/lecture_116_data_ops/data_testing/README.md)
- [Data Versioning](semester_16/lecture_116_data_ops/data_versioning/README.md)

#### 117: Ml Ops Advanced

- [A B Testing Ml](semester_16/lecture_117_ml_ops_advanced/a_b_testing_ml/README.md)
- [Feature Stores Advanced](semester_16/lecture_117_ml_ops_advanced/feature_stores_advanced/README.md)
- [Ml Pipelines Advanced](semester_16/lecture_117_ml_ops_advanced/ml_pipelines_advanced/README.md)
- [Model Monitoring Advanced](semester_16/lecture_117_ml_ops_advanced/model_monitoring_advanced/README.md)
- [Model Registry Advanced](semester_16/lecture_117_ml_ops_advanced/model_registry_advanced/README.md)
- [Model Serving Advanced](semester_16/lecture_117_ml_ops_advanced/model_serving_advanced/README.md)

#### 118: Data Platforms

- [Data Collaboration](semester_16/lecture_118_data_platforms/data_collaboration/README.md)
- [Data Marketplace](semester_16/lecture_118_data_platforms/data_marketplace/README.md)
- [Data Platform Architecture](semester_16/lecture_118_data_platforms/data_platform_architecture/README.md)
- [Data Sharing](semester_16/lecture_118_data_platforms/data_sharing/README.md)
- [Self Service Analytics](semester_16/lecture_118_data_platforms/self_service_analytics/README.md)
- [Unified Data Platforms](semester_16/lecture_118_data_platforms/unified_data_platforms/README.md)

### Semester 1
- [01: Sorting Fundamentals](semester_01/lecture_01_sorting_fundamentals/)
- [02: Efficient Sorting](semester_01/lecture_02_efficient_sorting/)
- [03: Specialized Sorting](semester_01/lecture_03_specialized_sorting/)
- [04: Searching](semester_01/lecture_04_searching/)
- [05: Trees](semester_01/lecture_05_trees/)
- [06: Advanced Trees](semester_01/lecture_06_advanced_trees/)
- [07: Heaps Priority](semester_01/lecture_07_heaps_priority/)
- [08: Hash Tables](semester_01/lecture_08_hash_tables/)
- [09: Graph Algorithms](semester_01/lecture_09_graph_algorithms/)
- [11: Dynamic Programming](semester_01/lecture_11_dynamic_programming/)
- [12: String Algorithms](semester_01/lecture_12_string_algorithms/)

### Semester 2
- [06: Solid Principles](semester_02/lecture_06_solid_principles/)
- [07: Creational Patterns](semester_02/lecture_07_creational_patterns/)
- [08: Structural Patterns](semester_02/lecture_08_structural_patterns/)
- [09: Behavioral Patterns](semester_02/lecture_09_behavioral_patterns/)
- [10: Architectural Patterns](semester_02/lecture_10_architectural_patterns/)
- [11: Repository Patterns](semester_02/lecture_11_repository_patterns/)
- [12: Concurrency Patterns](semester_02/lecture_12_concurrency_patterns/)

### Semester 3
- [10: Graph Algorithms](semester_03/lecture_10_graph_algorithms/)
- [11: Dynamic Programming](semester_03/lecture_11_dynamic_programming/)
- [12: Ml Algorithms](semester_03/lecture_12_ml_algorithms/)
- [13: Clustering](semester_03/lecture_13_clustering/)
- [13: Integration Patterns](semester_03/lecture_13_integration_patterns/)
- [14: String Algorithms](semester_03/lecture_14_string_algorithms/)
- [15: Greedy Algorithms](semester_03/lecture_15_greedy_algorithms/)
- [16: Advanced Ml](semester_03/lecture_16_advanced_ml/)

### Semester 4
- [14: Security Patterns](semester_04/lecture_14_security_patterns/)
- [15: Testing Patterns](semester_04/lecture_15_testing_patterns/)
- [16: Deployment Patterns](semester_04/lecture_16_deployment_patterns/)
- [17: Performance](semester_04/lecture_17_performance/)
- [18: Crypto Algorithms](semester_04/lecture_18_crypto_algorithms/)
- [19: Distributed Patterns](semester_04/lecture_19_distributed_patterns/)
- [20: Monitoring Observability](semester_04/lecture_20_monitoring_observability/)

### Semester 5
- [21: Transfer Learning](semester_05/lecture_21_transfer_learning/)
- [22: Cnn Architectures](semester_05/lecture_22_cnn_architectures/)
- [23: Object Detection](semester_05/lecture_23_object_detection/)
- [24: Segmentation](semester_05/lecture_24_segmentation/)
- [25: Transformers](semester_05/lecture_25_transformers/)
- [26: Ensemble Methods](semester_05/lecture_26_ensemble_methods/)
- [27: Hyperparameter Optimization](semester_05/lecture_27_hyperparameter_optimization/)
- [28: Reinforcement Learning](semester_05/lecture_28_reinforcement_learning/)
- [29: Nlp Advanced](semester_05/lecture_29_nlp_advanced/)
- [30: Time Series](semester_05/lecture_30_time_series/)

### Semester 6
- [31: Mlops](semester_06/lecture_31_mlops/)
- [32: Distributed Ml](semester_06/lecture_32_distributed_ml/)
- [33: Model Optimization](semester_06/lecture_33_model_optimization/)
- [34: Edge Ai](semester_06/lecture_34_edge_ai/)
- [35: Deployment Patterns](semester_06/lecture_35_deployment_patterns/)
- [36: Inference Optimization](semester_06/lecture_36_inference_optimization/)
- [37: Cost Optimization](semester_06/lecture_37_cost_optimization/)
- [38: Monitoring Production](semester_06/lecture_38_monitoring_production/)

### Semester 7
- [39: Operating Systems](semester_07/lecture_39_operating_systems/)
- [40: Llm Fundamentals](semester_07/lecture_40_llm_fundamentals/)
- [41: Llm Advanced](semester_07/lecture_41_llm_advanced/)
- [42: Ci Cd Fundamentals](semester_07/lecture_42_ci_cd_fundamentals/)
- [43: Ci Cd Advanced](semester_07/lecture_43_ci_cd_advanced/)
- [44: Quantum Computing](semester_07/lecture_44_quantum_computing/)
- [45: Blockchain Fundamentals](semester_07/lecture_45_blockchain_fundamentals/)
- [46: Blockchain Advanced](semester_07/lecture_46_blockchain_advanced/)

### Semester 8
- [47: Support Systems](semester_08/lecture_47_support_systems/)
- [48: Documentation](semester_08/lecture_48_documentation/)
- [49: Sql Fundamentals](semester_08/lecture_49_sql_fundamentals/)
- [50: Sql Advanced](semester_08/lecture_50_sql_advanced/)
- [51: Nosql Fundamentals](semester_08/lecture_51_nosql_fundamentals/)
- [52: Nosql Advanced](semester_08/lecture_52_nosql_advanced/)
- [53: Database Operations](semester_08/lecture_53_database_operations/)
- [54: Data Modeling](semester_08/lecture_54_data_modeling/)

### Semester 9
- [55: Advanced Os](semester_09/lecture_55_advanced_os/)
- [56: Os Performance](semester_09/lecture_56_os_performance/)
- [57: Concurrency Advanced](semester_09/lecture_57_concurrency_advanced/)
- [58: Parallel Computing](semester_09/lecture_58_parallel_computing/)
- [59: Distributed Systems Advanced](semester_09/lecture_59_distributed_systems_advanced/)
- [60: System Design Advanced](semester_09/lecture_60_system_design_advanced/)
- [61: Cloud Native](semester_09/lecture_61_cloud_native/)
- [62: Observability Advanced](semester_09/lecture_62_observability_advanced/)

### Semester 10
- [63: Ai Advanced](semester_10/lecture_63_ai_advanced/)
- [64: Llm Architecture Advanced](semester_10/lecture_64_llm_architecture_advanced/)
- [65: Llm Training Advanced](semester_10/lecture_65_llm_training_advanced/)
- [66: Llm Inference](semester_10/lecture_66_llm_inference/)
- [67: Rag Advanced](semester_10/lecture_67_rag_advanced/)
- [68: Llm Evaluation](semester_10/lecture_68_llm_evaluation/)
- [69: Ai Ethics](semester_10/lecture_69_ai_ethics/)
- [70: Ai Governance](semester_10/lecture_70_ai_governance/)

### Semester 11
- [71: Cicd Advanced](semester_11/lecture_71_cicd_advanced/)
- [72: Infrastructure Advanced](semester_11/lecture_72_infrastructure_advanced/)
- [73: Security Devops](semester_11/lecture_73_security_devops/)
- [74: Automation Advanced](semester_11/lecture_74_automation_advanced/)
- [75: Gitops Advanced](semester_11/lecture_75_gitops_advanced/)
- [76: Platform Engineering](semester_11/lecture_76_platform_engineering/)
- [77: Chaos Engineering Advanced](semester_11/lecture_77_chaos_engineering_advanced/)
- [78: Observability Platform](semester_11/lecture_78_observability_platform/)

### Semester 12
- [79: Quantum Algorithms Advanced](semester_12/lecture_79_quantum_algorithms_advanced/)
- [80: Quantum Computing Advanced](semester_12/lecture_80_quantum_computing_advanced/)
- [81: Quantum Applications](semester_12/lecture_81_quantum_applications/)
- [82: Hybrid Quantum](semester_12/lecture_82_hybrid_quantum/)
- [83: Quantum Software](semester_12/lecture_83_quantum_software/)
- [84: Quantum Hardware](semester_12/lecture_84_quantum_hardware/)
- [85: Quantum Networking](semester_12/lecture_85_quantum_networking/)
- [86: Quantum Security](semester_12/lecture_86_quantum_security/)

### Semester 13
- [87: Blockchain Advanced](semester_13/lecture_87_blockchain_advanced/)
- [88: Consensus Advanced](semester_13/lecture_88_consensus_advanced/)
- [89: Defi](semester_13/lecture_89_defi/)
- [90: Blockchain Security](semester_13/lecture_90_blockchain_security/)
- [91: Blockchain Privacy](semester_13/lecture_91_blockchain_privacy/)
- [92: Blockchain Interoperability](semester_13/lecture_92_blockchain_interoperability/)
- [93: Blockchain Governance](semester_13/lecture_93_blockchain_governance/)
- [94: Blockchain Analytics](semester_13/lecture_94_blockchain_analytics/)

### Semester 14
- [95: Support Advanced](semester_14/lecture_95_support_advanced/)
- [96: Incident Management Advanced](semester_14/lecture_96_incident_management_advanced/)
- [97: Knowledge Management](semester_14/lecture_97_knowledge_management/)
- [98: Documentation Advanced](semester_14/lecture_98_documentation_advanced/)
- [99: Technical Writing Advanced](semester_14/lecture_99_technical_writing_advanced/)
- [100: Documentation Ai](semester_14/lecture_100_documentation_ai/)
- [101: Developer Experience](semester_14/lecture_101_developer_experience/)
- [102: Community Management](semester_14/lecture_102_community_management/)

### Semester 15
- [103: Sql Advanced Topics](semester_15/lecture_103_sql_advanced_topics/)
- [104: Database Performance](semester_15/lecture_104_database_performance/)
- [105: Database Architecture](semester_15/lecture_105_database_architecture/)
- [106: Nosql Advanced Topics](semester_15/lecture_106_nosql_advanced_topics/)
- [107: Time Series Databases](semester_15/lecture_107_time_series_databases/)
- [108: Graph Databases Advanced](semester_15/lecture_108_graph_databases_advanced/)
- [109: Database Security Advanced](semester_15/lecture_109_database_security_advanced/)
- [110: Database Migration](semester_15/lecture_110_database_migration/)

### Semester 16
- [111: Data Engineering Advanced](semester_16/lecture_111_data_engineering_advanced/)
- [112: Data Warehousing Advanced](semester_16/lecture_112_data_warehousing_advanced/)
- [113: Data Lakes Advanced](semester_16/lecture_113_data_lakes_advanced/)
- [114: Real Time Analytics](semester_16/lecture_114_real_time_analytics/)
- [115: Data Governance Advanced](semester_16/lecture_115_data_governance_advanced/)
- [116: Data Ops](semester_16/lecture_116_data_ops/)
- [117: Ml Ops Advanced](semester_16/lecture_117_ml_ops_advanced/)
- [118: Data Platforms](semester_16/lecture_118_data_platforms/)

## 💡 Key Features

### 1. Educational Excellence
- **Why, not just How**: Understand the reasoning
- **Real-world Context**: Practical applications
- **Common Mistakes**: Learn from pitfalls
- **Trade-offs**: When to use which algorithm

### 2. Production Quality
- **Error Handling**: Robust implementations
- **Performance Metrics**: Actual measurements
- **Type Hints**: Python type annotations
- **Best Practices**: Industry standards

### 3. Comprehensive Examples
- **Multiple Scenarios**: Simple to complex
- **Edge Cases**: Boundary conditions tested
- **Visualizations**: Where applicable
- **Comparisons**: Algorithm vs algorithm

### 4. Performance Framework
```python
from framework.performance_timer import PerformanceTimer

timer = PerformanceTimer("My Algorithm")
result, metrics = timer.measure(my_function, args)
print(f"Time: {metrics['execution_time_ms']} ms")
print(f"Memory: {metrics['memory_peak_kb']} KB")
```

### 5. Constraint-based Selection
```python
from framework.constraint_selector import AlgorithmSelector, Constraints

selector = AlgorithmSelector()
constraints = Constraints(
    max_memory_mb=100,
    max_time_ms=1000,
    dataset_size=10000
)
recommended = selector.select_algorithm("sorting", constraints)
```

## 📊 Complexity Reference

Quick reference table for algorithm complexities:

| Algorithm | Time (Best) | Time (Avg) | Time (Worst) | Space |
|-----------|------------|------------|--------------|-------|
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) |
| Binary Search | O(1) | O(log n) | O(log n) | O(1) |
| DFS/BFS | O(V+E) | O(V+E) | O(V+E) | O(V) |
| Dijkstra | - | O((V+E)log V) | O((V+E)log V) | O(V) |

[Full complexity table →](ALGORITHM_INDEX.md)

## 🎓 For Students

### Learning Path
1. Start with **Semester 1** - fundamentals
2. Practice each algorithm with provided examples
3. Understand complexity analysis
4. Learn when to apply each algorithm
5. Progress through semesters systematically

### Study Tips
- **Run the code**: Don't just read, execute
- **Modify examples**: Experiment with parameters
- **Compare algorithms**: Run performance tests
- **Solve problems**: Apply to real scenarios

## 👨‍🏫 For Instructors

### Teaching Resources
- Complete lecture materials
- Ready-to-run examples
- Performance demonstrations
- Assessment ideas built-in

### Customization
- Fork and modify for your course
- Add your own examples
- Adjust difficulty levels
- Create assignments from examples

## 👨‍💻 For Practitioners

### Production Use
- Reference implementations
- Performance benchmarks
- Best practices included
- Real-world patterns

### Quick Lookup
- Find algorithm by use case
- Check complexity quickly
- See example usage
- Copy production-ready code

## 🛠️ Development

### Project Structure
```
Professor/
├── semester_01/               # Fundamentals
│   ├── lecture_01_sorting_fundamentals/
│   │   ├── bubble_sort/
│   │   │   ├── algorithm.py
│   │   │   ├── Algorithm.java
│   │   │   ├── metadata.json
│   │   │   └── README.md
│   │   └── ...
│   └── ...
├── semester_02/               # Design Patterns
├── semester_03/               # Machine Learning
├── semester_04/               # Integration & Security
├── semester_05/               # Advanced AI/ML
├── semester_06/               # MLOps
├── framework/                # Common utilities
│   ├── performance_timer.py
│   └── constraint_selector.py
├── web_interface/            # Web UI
│   ├── app.py
│   └── templates/
├── requirements.txt
├── pom.xml
└── README.md
```

### Contributing
Contributions welcome! See implementation progress and pick an algorithm to implement.

1. Follow the existing code style
2. Include both Python and Java
3. Add comprehensive examples
4. Include performance metrics
5. Document complexity and use cases

## 📈 Progress Tracking

Track implementation progress:
```bash
python track_implementations.py --check
```

See detailed progress: [IMPLEMENTATION_PROGRESS.md](IMPLEMENTATION_PROGRESS.md)

## 📝 Documentation

- **[Quick Start](QUICKSTART.md)**: Get started in 5 minutes
- **[Course Plan](COURSE_PLAN_6SEMESTERS.md)**: Detailed semester breakdown (6 semesters)
- **[Comprehensive Textbook](COMPREHENSIVE_COURSE_TEXTBOOK.md)**: Complete course in one document
- **[Algorithm Index](ALGORITHM_INDEX.md)**: Complete algorithm list
- **[Implementation Guide](AI_IMPLEMENTATION_GUIDE.md)**: How to add algorithms
- **[Progress Report](IMPLEMENTATION_PROGRESS.md)**: Current status
- **[Critiques & Improvements](CRITIQUES.md)**: Teacher, programmer, and student perspectives
- **[Updated GPT Prompt](UPDATE_GPT_PROMPT.md)**: Current project state and requirements

## 🎯 Next Steps

See [NEXT_STEPS.md](NEXT_STEPS.md) for implementation roadmap.

**Immediate priorities:**
1. Complete graph algorithms (Dijkstra, Bellman-Ford)
2. Add core design patterns (Observer, Strategy, Builder)
3. Implement remaining ML algorithms (SVM, Naive Bayes)
4. Add dynamic programming suite

## 📜 License

This project is created for educational purposes. All implementations are provided as-is for learning and reference.

## 🙏 Acknowledgments

This course synthesizes best practices from:
- "Introduction to Algorithms" (CLRS)
- "Design Patterns" (Gang of Four)
- "Hands-On Machine Learning" (Aurélien Géron)
- Industry experience and real-world applications

## 📧 Contact

For questions, suggestions, or contributions, please open an issue or pull request.

---

**Note**: This is an actively developed educational resource. Check back regularly for new implementations and improvements.

**Last Updated**: 2025-11-21
**Version**: 0.7.0
**Status**: Active Development (40% Complete)
**Testing**: 680+ test files (Python + Java) with automated fixing system
**Java Tests**: 2,800+ successful tests recorded, 4,700+ total test records
**Documentation**: 680+ algorithm READMEs with code file links, comprehensive visualization guide
**Execution Framework**: Unified Algorithm Executor for Java and Python
**Future Plans**: Student Sandbox System with version control and comparison tools

## 🆕 Recent Updates

### 2025-11-21
- ✅ **Unified Algorithm Executor** - Created web-based executor for both Java and Python algorithms
  - Language selector, code viewer, execution monitoring
  - Filtering by semester, lecture, and algorithm
  - Real-time source code display with syntax highlighting
- ✅ **Student Sandbox Plan** - Comprehensive plan for interactive learning environment
  - Detailed architecture for sandbox system, version control, and comparison tools
  - Security and isolation strategies
  - 8-phase implementation roadmap (14 weeks)
  - See `docs/STUDENT_SANDBOX_PLAN.md` for complete details
- ✅ **Enhanced Java fix script** - Added fixes for invalid parameter syntax and Python-style None in Java
- ✅ **Progress monitoring** - Created `monitor_fix_progress.py` for real-time fix progress tracking
- ✅ **Missing examples checker** - Created script to identify missing example implementations
- ✅ **Enhanced README navigation** - Added individual algorithm links (680+ algorithms) to main README
- ✅ **Code file links** - Updated all algorithm README files with direct links to Python, Java, and test files
- ✅ **Visualization improvements guide** - Created comprehensive guide for static visual materials to enhance memorization
- ✅ **Repository cleanup** - Removed 827 .class files from git tracking, added `*.class` to .gitignore
- ✅ **Test reports fix** - Fixed statistics filter discrepancy in web interface
- ✅ **Java auto-fix script** - Comprehensive Java compilation error fixing system
- ✅ **Logger standardization** - Automatic replacement of `System.out.println/printf` with `logger.info()` in Java files
- ✅ **Java testing system** - 680+ Java files with automated testing and fixing
- ✅ **Database tracking** - SQLite database for tracking test results and status history
- ✅ **Web interface** - Real-time monitoring of test progress and results
- ✅ **Fixed multiple Java files** - Resolved compilation errors in message_queue, publish_subscribe, authorization, encryption, jwt, mocking, integration_testing, tdd, unit_testing

### 2025-11-20
- ✅ **Enhanced all READMEs** with introduction, "Often Used Together With", "Do Not Confuse With", and framework examples
- ✅ **Added Semesters 7-8** covering Operating Systems, LLMs, CI/CD, Quantum Computing, Blockchain, Support, Documentation, SQL/NoSQL
- ✅ **Generated comprehensive PDF** textbook with all course content
- ✅ **Updated GPT prompt** based on current project state
- ✅ **78+ algorithms fully implemented** with Python and Java
- ✅ **Enhanced auto-fix script** with function signature analysis for API usage errors
- ✅ **Added API usage error fixing** - automatically fixes missing arguments and wrong function signatures
- ✅ **Comprehensive testing system** - 680+ test files with automated fixing capabilities
