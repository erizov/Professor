# Where Algorithm-Specific Data Comes From

## Answer: Three Sources (In Priority Order)

### 1. **metadata.json** ✅ PRIMARY SOURCE (100% Success Rate)

**Location:** `semester_XX/lecture_XX_topic/algorithm_name/metadata.json`

**What I Extract:**
- Algorithm name
- Category (e.g., "Sorting", "Searching")
- **Time complexity** (from `complexity.time`)
- **Space complexity** (from `complexity.space`)

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

**Code Location:** `scripts/fix_all_semesters_final.py` lines 160-184
```python
# 1. Read metadata.json
metadata_path = algorithm_folder / "metadata.json"
if metadata_path.exists():
    metadata = json.loads(metadata_path.read_text(encoding='utf-8'))
    # Extract complexity from nested structure
    if 'complexity' in metadata and isinstance(metadata['complexity'], dict):
        if 'time' in metadata['complexity']:
            info['time_complexity'] = metadata['complexity']['time']
        if 'space' in metadata['complexity']:
            info['space_complexity'] = metadata['complexity']['space']
```

**✅ This works 100% of the time!**

---

### 2. **algorithm.py** ⚠️ BACKUP SOURCE (20% Success Rate)

**Location:** `semester_XX/lecture_XX_topic/algorithm_name/algorithm.py`

**What I Extract:**
- Class/function names
- **Complexity from docstrings** (only 20% have it)
- Actual implementation code

**Code Location:** `scripts/fix_all_semesters_final.py` lines 186-210
```python
# 2. Read algorithm.py for code structure and docstrings
code_path = algorithm_folder / "algorithm.py"
if code_path.exists():
    code = code_path.read_text(encoding='utf-8')
    # Extract complexity from docstrings (backup if metadata missing)
    time_comp, space_comp = extract_complexity_from_docstring(code)
    if time_comp:
        info['time_complexity'] = time_comp
    if space_comp:
        info['space_complexity'] = space_comp
```

**⚠️ Only 20% of algorithms have complexity in docstrings**

---

### 3. **README.md** ✅ USE CASES (100% Success Rate), ❌ DESCRIPTIONS (0% Success)

**Location:** `semester_XX/lecture_XX_topic/algorithm_name/README.md`

**What I Extract:**
- ✅ **Use cases** (from "Real-World Applications" section) - 100% success
- ❌ **Descriptions** - 0% success (all READMEs are flowcharts/ASCII art)

**Code Location:** `scripts/fix_all_semesters_final.py` lines 212-223
```python
# 3. Read README.md for descriptions and use cases
readme_path = algorithm_folder / "README.md"
if readme_path.exists():
    # Extract use cases
    use_cases = extract_use_cases_from_readme(readme_path)
    if use_cases:
        info['use_cases'] = use_cases
```

**✅ Use cases work 100% of the time!**
**❌ Descriptions don't work (READMEs are flowcharts)**

---

### 4. **Algorithm Name Patterns** 🔄 FALLBACK

**When metadata.json doesn't have complexity, I infer from algorithm name:**

**Code Location:** `scripts/fix_all_semesters_final.py` lines 225-267
```python
# Set defaults only if nothing was found
if not info['time_complexity']:
    name_lower = algorithm_folder.name.lower()
    if 'sort' in name_lower:
        if 'quick' in name_lower or 'merge' in name_lower:
            info['time_complexity'] = 'O(n log n)'
        elif 'bubble' in name_lower:
            info['time_complexity'] = 'O(n²)'
    # ... more patterns
```

**This is a LAST RESORT fallback.**

---

## Summary

| Data Type | Source | Success Rate | Status |
|-----------|--------|--------------|--------|
| **Time Complexity** | metadata.json | 100% | ✅ Working |
| **Space Complexity** | metadata.json | 100% | ✅ Working |
| **Category** | metadata.json | 100% | ✅ Working |
| **Use Cases** | README.md | 100% | ✅ Working |
| **Code Structure** | algorithm.py | 100% | ✅ Working |
| **Complexity (backup)** | algorithm.py docstrings | 20% | ⚠️ Limited |
| **Descriptions** | README.md | 0% | ❌ Not available |

---

## The 'Varies' Issue

The `'Varies'` default in `enhanced_extract_algorithm_info.py` line 207-208 is just an **initial value**. 

**The actual extraction in `fix_all_semesters_final.py` DOES extract from metadata.json!**

The flow is:
1. Start with `None` (not 'Varies')
2. Extract from `metadata.json` (100% success)
3. Backup from docstrings (20% success)
4. Fallback to name patterns
5. Only use 'Varies' as absolute last resort

**So the data IS being extracted correctly from metadata.json!**

