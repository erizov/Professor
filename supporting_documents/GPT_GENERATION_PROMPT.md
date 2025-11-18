# GPT Generation Prompt for Algorithms Course Project

## Project Overview Prompt

```
You are university professor of computer science with fundamental education in mathematics. Create a detailed plan of 6 semester course in algorithms starting from simple sorting, searching, SOLID, common patterns, enterprise patterns, integration patterns, ML algorithms (emphasis on AI/ML for 3+ semesters), security patterns, deployment and testing patterns.

Create approximately 180-200 folders for each lecture/algorithm. Each algorithm should have:

### Required Components:
1. **Advantages** - Clear benefits of using this algorithm
2. **Disadvantages** - Limitations and weaknesses
3. **Usage Examples** - Real-world applications
4. **Common Mistakes** - Typical errors developers make
5. **Misconceptions** - Wrong beliefs about the algorithm
6. **Executive Summaries** - Quick overview for decision makers
7. **When to Use** - Specific scenarios where it excels
8. **When NOT to Use** - Situations to avoid this algorithm
9. **Examples in Python and Java** - Full working implementations
10. **Other Languages** - Only if algorithm is language-specific

### Performance & Resource Analysis:
- **Time each algorithm** with real execution measurements
- **Space requirements** - Memory footprint analysis
- **Resource requirements** - CPU, GPU, Network, Storage needs
- **Constraint analysis** - Algorithm choice given:
  - Limited memory
  - Low CPU power
  - Network bandwidth constraints
  - Edge device deployment
  - Power consumption limits
  - Cost optimization
  - Latency requirements

### Data Handling:
- Limit the amount of data used to save space as much as possible
- If algorithm needs big data, give a reference to it
- DO NOT download large datasets
- Use small representative samples

### Documentation:
- Save common README file with short plan for each lecture
- Each algorithm folder structure:
  ```
  algorithm_name/
  ├── README.md          # Comprehensive documentation
  ├── metadata.json      # Complexity, properties, constraints
  ├── algorithm.py       # Python implementation with timing
  ├── Algorithm.java     # Java implementation
  ├── test.py           # Python tests
  └── AlgorithmTest.java # Java tests
  ```

### Execution Framework:
Create a common framework to run any of the Python and Java examples with all dependencies:
- `requirements.txt` for Python dependencies
- `pom.xml` for Java/Maven dependencies
- `runner.py` - Universal runner script
- Performance timing utilities
- Resource measurement tools
- Constraint-based algorithm selector

### Web Interface:
Create simple webpage to see all algorithms and run them:
- Browse by semester/category
- Filter by complexity, resource requirements
- Run algorithms in browser
- Display O notation and complexity
- Show performance metrics
- Compare algorithms side-by-side
- Constraint-based recommendations

## Course Structure (6 Semesters)

### Semester 1: Foundations (15 weeks)
- Algorithm complexity and Big O notation
- Sorting algorithms (10+ variants)
- Searching algorithms (6+ variants)
- Basic data structures (Arrays, Lists, Stacks, Queues, Hash Tables)
- Tree structures (Binary, BST, AVL, Red-Black, B-Trees)
- **Focus**: Memory vs Time trade-offs, Cache efficiency

### Semester 2: Software Engineering Patterns (15 weeks)
- SOLID principles (5 patterns)
- Creational patterns (6 patterns)
- Structural patterns (7 patterns)
- Behavioral patterns (10+ patterns)
- Architectural patterns (MVC, MVVM, Clean Architecture)
- Concurrency patterns
- **Focus**: Code quality, maintainability, scalability

### Semester 3: Advanced Algorithms & ML Foundations (15 weeks)
- Graph algorithms (12+ variants)
- Dynamic programming (7+ problems)
- ML Foundations:
  - Linear/Logistic Regression
  - K-Nearest Neighbors
  - Decision Trees
  - K-Means Clustering
  - Naive Bayes
  - PCA
- String algorithms
- **Focus**: Dataset size, feature dimensions, training time

### Semester 4: ML Algorithms & Enterprise (15 weeks)
- Advanced ML:
  - Random Forest
  - Gradient Boosting (XGBoost, LightGBM)
  - Support Vector Machines
  - Neural Networks (Feedforward)
  - Backpropagation
  - CNN/RNN basics
  - LSTM
  - Attention mechanisms
- ML Optimization techniques
- Enterprise integration patterns
- Security patterns (Authentication, Authorization, Encryption)
- **Focus**: GPU vs CPU, batch size, training vs inference

### Semester 5: Deep Learning & AI Systems (15 weeks)
- Deep Learning Architectures:
  - Transfer Learning
  - ResNet, VGG, Inception
  - YOLO, U-Net
  - Transformer, BERT, GPT basics
- Advanced ML:
  - Ensemble methods
  - Hyperparameter optimization
  - Feature engineering
  - Anomaly detection
  - Time series forecasting
- Reinforcement Learning:
  - Q-Learning
  - Deep Q-Networks
  - Policy Gradients
  - PPO
- Natural Language Processing
- **Focus**: Model size, VRAM, inference speed, quantization

### Semester 6: Production ML & Scalable AI (15 weeks)
- MLOps:
  - Model versioning
  - A/B testing
  - Feature stores
  - Monitoring & drift detection
  - Retraining strategies
- Distributed ML:
  - Data/Model parallelism
  - Parameter servers
  - Federated learning
  - MapReduce for ML
- Model Optimization:
  - Quantization (INT8, FP16)
  - Pruning
  - Knowledge distillation
  - Neural Architecture Search
  - Edge deployment
- Deployment patterns:
  - Blue-Green, Canary, Shadow
  - Circuit breaker, Rate limiting
  - Caching, Load balancing
- **Focus**: Inference cost, latency SLAs, auto-scaling

## Resource Constraint Matrix

Each algorithm must include analysis for:

| Constraint | Measurement |
|------------|-------------|
| **Memory** | Heap size, stack depth, auxiliary space (KB/MB/GB) |
| **CPU** | Single-core vs multi-core, clock cycles, utilization |
| **GPU** | CUDA cores required, VRAM usage, tensor operations |
| **Network** | Bandwidth (Mbps), latency (ms), packet size |
| **Storage** | Dataset size, model size, checkpoint storage (MB/GB/TB) |
| **Power** | Battery impact, thermal constraints (Watts) |
| **Cost** | Cloud compute costs ($/hour), inference pricing |
| **Time** | Real execution time (ms/s/min) |

## Performance Benchmarking Requirements

Test all algorithms on:
1. **Small dataset**: n ≤ 100
2. **Medium dataset**: 100 < n ≤ 10,000
3. **Large dataset**: n > 10,000

With resource profiles:
- **Low memory**: < 1 GB
- **Standard memory**: 1-8 GB
- **High memory**: > 8 GB
- **CPU-only**: No GPU available
- **GPU-accelerated**: CUDA/Metal available
- **Edge device**: Mobile/IoT constraints
- **Cloud**: Unlimited resources

## Algorithm Selection Decision Framework

Provide decision trees for:
1. **Sorting**: Quick vs Merge vs Tim vs Heap vs Counting
2. **Searching**: Linear vs Binary vs Hash vs Tree-based
3. **ML Classification**: Linear vs Tree vs SVM vs Neural Network
4. **ML Regression**: Linear vs Polynomial vs Tree-based vs DL
5. **Clustering**: K-Means vs Hierarchical vs DBSCAN
6. **Deployment**: Edge vs Cloud vs Hybrid

Each decision includes:
- Constraint thresholds
- Performance expectations
- Cost implications
- Trade-off analysis

## Code Quality Standards

### Python (PEP 8):
- UTF-8 encoding
- 4 spaces indentation
- Line length ≤ 79
- Type hints required
- Docstrings (PEP 257)
- snake_case naming
- Logging instead of print

### Java (Oracle Style):
- UTF-8 encoding
- 4 spaces indentation
- CamelCase for classes
- camelCase for methods
- Comprehensive JavaDoc
- Proper exception handling

## Project Structure

```
.
├── README.md                    # Project overview
├── COURSE_PLAN_6SEMESTERS.md   # Detailed course plan
├── GPT_GENERATION_PROMPT.md    # This file
├── requirements.txt             # Python dependencies
├── pom.xml                     # Java dependencies
├── runner.py                   # Universal runner
├── generate_algorithms.py      # Batch generator
│
├── framework/
│   ├── performance_timer.py    # Timing utilities
│   ├── constraint_selector.py  # Algorithm selector
│   └── algorithm_template.py   # Template generator
│
├── web_interface/
│   ├── app.py                  # Flask backend
│   └── templates/
│       └── index.html          # Frontend UI
│
├── semester_01/
│   ├── README.md
│   ├── lecture_01_sorting_fundamentals/
│   │   ├── README.md
│   │   ├── bubble_sort/
│   │   ├── selection_sort/
│   │   └── insertion_sort/
│   └── ...
│
├── semester_02/ ... semester_06/
│
└── docs/
    ├── algorithm_selection_guide.md
    ├── constraint_analysis.md
    └── performance_benchmarks.md
```

## Web Interface Requirements

### Features:
1. **Browse Algorithms**
   - Grid/list view
   - Semester-based navigation
   - Category filters
   - Search functionality

2. **Algorithm Details**
   - README content display
   - Complexity visualization
   - Code syntax highlighting
   - Resource requirements table

3. **Run Algorithms**
   - Execute Python/Java in sandbox
   - Show output and timing
   - Display memory usage
   - Compare multiple algorithms

4. **Performance Dashboard**
   - Execution time charts
   - Memory usage graphs
   - Complexity comparison
   - Resource utilization

5. **Recommendation Engine**
   - Input constraints
   - Get algorithm recommendations
   - See reasoning and alternatives
   - Compare trade-offs

## Implementation Priorities

1. **Core Framework** (Priority 1)
   - Runner script
   - Performance timing
   - Basic web interface

2. **Semester 1-2** (Priority 2)
   - Fundamental algorithms
   - Design patterns
   - Full documentation

3. **Semester 3-4** (Priority 3)
   - ML algorithms
   - Performance benchmarks
   - Constraint analysis

4. **Semester 5-6** (Priority 4)
   - Advanced AI/ML
   - Production patterns
   - Optimization techniques

5. **Enhancement** (Priority 5)
   - Advanced visualizations
   - Interactive tutorials
   - Video demonstrations

## Usage Examples

### Run Algorithm:
```bash
python runner.py --semester 1 --lecture 01 --algorithm bubble_sort --lang python
```

### Start Web Interface:
```bash
python web_interface/app.py
# Navigate to http://localhost:5000
```

### Get Algorithm Recommendation:
```python
from framework.constraint_selector import AlgorithmSelector, Constraints, ResourceLevel

constraints = Constraints(
    memory=ResourceLevel.LOW,
    dataset_size='large',
    is_edge_device=True
)

recommendation = AlgorithmSelector.select_sorting_algorithm(constraints)
print_recommendation(recommendation)
```

### Benchmark Algorithm:
```python
from framework.performance_timer import benchmark

@benchmark(dataset_sizes=[100, 1000, 10000])
def my_algorithm(data):
    return sorted(data)
```

## Success Criteria

✓ 180-200 algorithm implementations
✓ All algorithms have timing measurements
✓ Resource constraint analysis for each
✓ Python and Java implementations
✓ Comprehensive documentation
✓ Working web interface
✓ Algorithm selector tool
✓ 6 semesters with ML focus (3+ semesters)
✓ Decision trees for algorithm selection
✓ Performance benchmarks
✓ Space-efficient (no large datasets)
✓ Educational and production-ready

## Maintenance & Enhancement

To regenerate or enhance:
1. Use this prompt with GPT-4 or similar
2. Specify which semester/module to enhance
3. Add new algorithms following the template
4. Update web interface to include new content
5. Re-run performance benchmarks
6. Update documentation

## License & Attribution

- Educational use: MIT License
- Commercial use: Contact author
- Attribution: University Computer Science Department
- Contributions: Follow template structure

---

**Last Updated**: 2025-11-15
**Version**: 1.0
**Course Duration**: 6 Semesters (90 weeks)
**Total Algorithms**: ~195 implementations
```

## Quick Regeneration Command

To regenerate this entire project from scratch, use this prompt with AI:

```
Using the detailed specifications in GPT_GENERATION_PROMPT.md, create a complete 6-semester algorithms course with 180-200 algorithm implementations, performance timing, resource constraint analysis, and a web interface. Focus on AI/ML algorithms for 3+ semesters with emphasis on real-world deployment constraints (memory, CPU, GPU, network, power). Include Python and Java implementations, comprehensive documentation, and an algorithm selection tool based on resource constraints.
```

