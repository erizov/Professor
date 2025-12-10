# Where Algorithm-Specific Information Comes From

## Current Sources (What I'm Using Now)

### 1. **metadata.json** ✅ USED
**Location:** `semester_XX/lecture_XX_topic/algorithm_name/metadata.json`

**What I Extract:**
- Algorithm name
- Category (e.g., "Sorting", "Searching", "Operating Systems Fundamentals")
- Time complexity (if present in `complexity.time`)
- Space complexity (if present in `complexity.space`)

**Example:**
```json
{
  "name": "Bubble Sort",
  "category": "Sorting",
  "complexity": {
    "time": "O(n²)",
    "space": "O(1)"
  }
}
```

**Limitation:** Many metadata.json files only have basic info, not detailed descriptions.

---

### 2. **algorithm.py** ✅ PARTIALLY USED
**Location:** `semester_XX/lecture_XX_topic/algorithm_name/algorithm.py`

**What I Extract:**
- Class names (e.g., `DeadlockDetection`, `BubbleSort`)
- Function/method names (e.g., `bubble_sort`, `detect_deadlock`)
- **Actual implementation code** (for code examples)

**What I'm NOT Extracting (But Should):**
- ❌ Docstrings (contain descriptions and complexity!)
- ❌ Algorithm approach/strategy from code structure
- ❌ Data structures used

**Example Docstring (Currently Ignored):**
```python
def bubble_sort(arr: List[T]) -> List[T]:
    """
    Sort array using bubble sort algorithm.
    
    Time Complexity: O(n²) - average and worst case
    Space Complexity: O(1)
    """
```

---

### 3. **README.md** ❌ NOT USED (But Should Be!)
**Location:** `semester_XX/lecture_XX_topic/algorithm_name/README.md`

**What's Available (But Not Extracted):**
- ✅ Detailed algorithm descriptions
- ✅ Real-world applications
- ✅ Use cases
- ✅ Examples
- ✅ Complexity analysis
- ✅ Historical context

**Example from bubble_sort/README.md:**
```
Bubble sort, sometimes referred to as sinking sort, is a simple 
sorting algorithm that repeatedly steps through the input list 
element by element, comparing the current element with the one 
after it, swapping their values if needed...
```

**This is the BEST source for descriptions but I'm not using it!**

---

### 4. **Hardcoded Database** ⚠️ LIMITED
**Location:** Inside `generate_quick_summary()` function

**What I Have:**
- Only `deadlock_detection` has full algorithm-specific content
- All other algorithms get generic placeholders:
  - `[algorithm purpose]`
  - `[key approach]`
  - `[key technique]`

**This is why most algorithms still have placeholders!**

---

## The Problem

**Current Flow:**
1. Read `metadata.json` → Get basic info (name, category, complexity)
2. Read `algorithm.py` → Get class/function names
3. Generate content → Use hardcoded database (only 1 algorithm!) or generic placeholders
4. ❌ **Skip README.md** (best source!)
5. ❌ **Skip docstrings** (contain descriptions!)

**Result:** Most algorithms get generic placeholders instead of real descriptions.

---

## The Solution

I've created `scripts/enhanced_extract_algorithm_info.py` that:

1. ✅ Reads `metadata.json` (already doing this)
2. ✅ Reads `algorithm.py` structure (already doing this)
3. ➕ **Extracts from README.md:**
   - Descriptions (skipping flowcharts)
   - Use cases
   - Real-world applications
4. ➕ **Extracts from docstrings:**
   - Complexity information
   - Algorithm descriptions
5. ➕ **Analyzes code:**
   - Algorithm type (sorting, searching, graph, etc.)
   - Data structures used

**This would give us real algorithm-specific content instead of placeholders!**

---

## Next Steps

1. **Integrate enhanced extraction** into `fix_all_semesters_final.py`
2. **Use README.md descriptions** instead of generic placeholders
3. **Extract docstrings** for better complexity and descriptions
4. **Use Cursor's AI** to generate algorithm-specific content based on extracted info

This would fix the remaining 645 English files with placeholders!

