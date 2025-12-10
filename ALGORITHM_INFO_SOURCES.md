# Algorithm-Specific Information Sources

## Current Implementation

### 1. **extract_algorithm_info() Function**

Currently extracts information from:

#### ✅ **metadata.json** (Used)
- `name`: Algorithm name
- `category`: Algorithm category (e.g., "Sorting", "Searching")
- `time_complexity`: Time complexity (if present)
- `space_complexity`: Space complexity (if present)

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

#### ✅ **algorithm.py** (Partially Used)
- Parses AST to extract:
  - Class names
  - Function/method names
- **NOT extracting:**
  - Docstrings (which contain descriptions!)
  - Complexity information from docstrings
  - Algorithm logic/approach

#### ❌ **README.md** (NOT Currently Used)
- Contains detailed descriptions
- Contains use cases
- Contains examples
- Contains complexity analysis
- **This is the BEST source but not being used!**

### 2. **generate_quick_summary() Function**

Currently uses:

#### ✅ **Hardcoded Database** (Limited)
- Only has `deadlock_detection` as example
- For other algorithms, generates generic placeholders:
  - `[algorithm purpose]`
  - `[key approach]`
  - `[key technique]`

#### ❌ **README.md Content** (NOT Used)
- Should extract descriptions from README
- Should extract use cases
- Should extract complexity from README sections

### 3. **generate_implementation_code() Function**

Currently:
- ✅ Extracts actual code from `algorithm.py`
- ✅ Shows real class/function implementations
- This works well!

## Problem

**The main issue:** We're not extracting the rich information available in:
1. **README.md files** - Best source for descriptions
2. **Docstrings in algorithm.py** - Best source for complexity and explanations
3. **Code analysis** - Could understand algorithm approach from code structure

## Solution: Enhanced Information Extraction

We should enhance `extract_algorithm_info()` to:

1. **Read README.md:**
   - Extract "Introduction" or "Short Description" sections
   - Extract "Real-World Applications"
   - Extract "Where It's Used"
   - Skip flowchart ASCII art

2. **Extract from Docstrings:**
   - Parse docstrings in `algorithm.py`
   - Extract complexity information
   - Extract algorithm description
   - Extract parameter descriptions

3. **Analyze Code Structure:**
   - Identify algorithm type (sorting, searching, graph, etc.)
   - Understand data structures used
   - Identify key operations

4. **Use Existing Scripts:**
   - `scripts/generate_ai_descriptions_final.py` already has:
     - `extract_detailed_description_from_readme()`
     - `extract_complexity_from_docstring()`
   - We should reuse these functions!

## Recommendation

**Enhance the extraction to use:**
1. ✅ `metadata.json` (already used)
2. ✅ `algorithm.py` code structure (already used)
3. ➕ **README.md** descriptions (should add)
4. ➕ **Docstrings** from `algorithm.py` (should add)
5. ➕ **Code analysis** to understand algorithm approach (should add)

This would give us much better algorithm-specific content instead of generic placeholders!

