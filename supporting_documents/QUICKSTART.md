# Quick Start Guide

## Installation

### Prerequisites
- Python 3.8 or higher
- Java 11 or higher (OpenJDK recommended)
- Maven 3.6+ (for Java builds)
- Git (optional)

### Setup Steps

1. **Clone or navigate to the project directory**
```bash
cd Professor
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Verify Java installation**
```bash
java -version
javac -version
```

4. **Optional: Build Java components**
```bash
mvn install
```

## Running Algorithms

### Method 1: Command Line Runner

Run any algorithm directly:
```bash
# Python example
python runner.py --semester 1 --lecture 01 --algorithm bubble_sort

# Java example
python runner.py --semester 1 --lecture 01 --algorithm bubble_sort --lang java

# Quick Sort
python runner.py --semester 1 --lecture 02 --algorithm quick_sort

# Binary Search
python runner.py --semester 1 --lecture 04 --algorithm binary_search
```

### Method 2: Web Interface

Start the web server:
```bash
python web_interface/app.py
```

Then open your browser to:
```
http://localhost:5000
```

Features:
- Browse all algorithms by semester
- Filter by category and complexity
- Run algorithms directly in browser
- View performance metrics
- Compare multiple algorithms

### Method 3: Direct Execution

Navigate to any algorithm folder and run directly:
```bash
# Python
cd semester_01/lecture_01_sorting_fundamentals/bubble_sort
python algorithm.py

# Java
cd semester_01/lecture_01_sorting_fundamentals/bubble_sort
javac Algorithm.java
java Algorithm
```

## Using the Performance Timer

```python
from framework.performance_timer import PerformanceTimer

# Create timer
timer = PerformanceTimer("My Algorithm")

# Measure performance
result, metrics = timer.measure(my_function, data)

# Print summary
timer.print_summary()
```

## Using the Algorithm Selector

```python
from framework.constraint_selector import (
    AlgorithmSelector, 
    Constraints, 
    ResourceLevel,
    print_recommendation
)

# Define your constraints
constraints = Constraints(
    memory=ResourceLevel.LOW,
    cpu_power=ResourceLevel.MEDIUM,
    dataset_size='large',
    is_edge_device=True,
    latency_requirement='low'
)

# Get sorting algorithm recommendation
recommendation = AlgorithmSelector.select_sorting_algorithm(constraints)
print_recommendation(recommendation)

# Get ML algorithm recommendation
ml_recommendation = AlgorithmSelector.select_ml_algorithm(
    constraints, 
    problem_type='classification'
)
print_recommendation(ml_recommendation)
```

## Course Navigation

### Semester 1: Foundations
```bash
cd semester_01
ls -la  # See all lectures
```

**Key Topics:**
- Sorting algorithms
- Searching algorithms  
- Trees and data structures

### Semester 2: Design Patterns
```bash
cd semester_02
```

**Key Topics:**
- SOLID principles
- Creational, Structural, Behavioral patterns
- Architectural patterns

### Semester 3: Advanced Algorithms & ML Foundations
```bash
cd semester_03
```

**Key Topics:**
- Graph algorithms
- Dynamic programming
- Basic ML algorithms (Linear Regression, KNN, Decision Trees)

### Semester 4: ML Algorithms & Enterprise
```bash
cd semester_04
```

**Key Topics:**
- Neural Networks
- CNN, RNN, LSTM
- Security patterns
- Integration patterns

### Semester 5: Deep Learning & AI
```bash
cd semester_05
```

**Key Topics:**
- Deep Learning architectures (ResNet, Transformers)
- Reinforcement Learning
- NLP algorithms

### Semester 6: Production ML
```bash
cd semester_06
```

**Key Topics:**
- MLOps patterns
- Distributed ML
- Model optimization
- Deployment patterns

## Example Workflows

### 1. Compare Sorting Algorithms
```python
from framework.performance_timer import compare_algorithms

# Import your sorting functions
from semester_01.lecture_01_sorting_fundamentals.bubble_sort.algorithm import bubble_sort
from semester_01.lecture_02_efficient_sorting.quick_sort.algorithm import quick_sort

algorithms = [
    ("Bubble Sort", bubble_sort),
    ("Quick Sort", quick_sort),
]

compare_algorithms(algorithms, dataset_size=1000)
```

### 2. Benchmark an Algorithm
```python
from framework.performance_timer import benchmark

@benchmark(dataset_sizes=[10, 100, 1000, 10000])
def my_sort(arr):
    return sorted(arr)

my_sort([1, 2, 3])  # Triggers benchmark
```

### 3. Analyze Resource Constraints
```python
from framework.performance_timer import PerformanceTimer, ResourceAnalyzer

timer = PerformanceTimer("Algorithm Name")
result, metrics = timer.measure(my_function, data)

analysis = ResourceAnalyzer.analyze_constraints(
    algorithm_name="My Algorithm",
    time_complexity="O(n log n)",
    space_complexity="O(n)",
    metrics=timer.get_summary()
)

ResourceAnalyzer.print_analysis(analysis)
```

## Troubleshooting

### Python Issues
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check installed packages
pip list
```

### Java Issues
```bash
# Check Java version
java -version  # Should be 11+
javac -version

# Clean and rebuild
mvn clean install
```

### Web Interface Issues
```bash
# Check if Flask is installed
pip show flask

# Run with debug mode
python web_interface/app.py --debug

# Check port availability
netstat -an | grep 5000
```

### Common Errors

**Error: Module not found**
```bash
# Make sure you're in the project root
cd /path/to/Professor

# Install requirements
pip install -r requirements.txt
```

**Error: Java file not found**
```bash
# Compile first
javac Algorithm.java
# Then run
java Algorithm
```

**Error: Port 5000 already in use**
```bash
# Kill the process
# On Linux/Mac:
lsof -ti:5000 | xargs kill -9

# On Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

## Performance Tips

1. **For large datasets**: Use optimized algorithms (Quick Sort, Merge Sort)
2. **For low memory**: Use in-place algorithms (Heap Sort, Quick Sort)
3. **For edge devices**: Use lightweight algorithms (Linear/Logistic Regression)
4. **For production ML**: Use ensemble methods (Random Forest, XGBoost)
5. **For real-time inference**: Use cached models and quantization

## Next Steps

1. **Explore the course plan**: Read `COURSE_PLAN_6SEMESTERS.md`
2. **Try different algorithms**: Navigate through semesters
3. **Use the web interface**: Visual exploration of algorithms
4. **Benchmark algorithms**: Compare performance
5. **Get recommendations**: Use constraint-based selector

## Getting Help

- Read the main `README.md`
- Check `COURSE_PLAN_6SEMESTERS.md` for course structure
- See `GPT_GENERATION_PROMPT.md` for detailed specifications
- Each algorithm has its own `README.md` with detailed documentation

## Contributing

To add new algorithms:
1. Follow the template structure
2. Include performance timing
3. Add resource constraint analysis
4. Update web interface
5. Document thoroughly

## License

MIT License - See LICENSE file for details

