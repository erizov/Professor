# PDF Generation Guide

## 📚 How to Generate PDF Textbooks

This guide explains how to convert the course materials into professional PDF textbooks.

---

## Prerequisites

Install required tools:

```bash
# Option 1: Pandoc (Recommended - Best Quality)
# Download from https://pandoc.org/installing.html

# On Windows with Chocolatey:
choco install pandoc miktex

# On macOS:
brew install pandoc basictex

# On Linux (Ubuntu/Debian):
sudo apt-get install pandoc texlive-xelatex texlive-fonts-recommended

# Option 2: Node.js md-to-pdf (Simpler)
npm install -g md-to-pdf

# Option 3: Python markdown-pdf
pip install markdown-pdf
```

---

## Generate Complete Course Textbook

### Method 1: Using Pandoc (Professional Quality)

```bash
# Basic PDF
pandoc COMPLETE_TEXTBOOK.md -o algorithms_textbook.pdf --toc

# Professional PDF with all features
pandoc COMPLETE_TEXTBOOK.md \
  -o algorithms_textbook.pdf \
  --toc \
  --toc-depth=3 \
  --number-sections \
  --highlight-style=tango \
  --pdf-engine=xelatex \
  -V geometry:margin=1in \
  -V fontsize=11pt \
  -V documentclass=book \
  -V papersize=letter \
  -V linkcolor=blue \
  -V urlcolor=blue \
  -V toccolor=black \
  --include-in-header=header.tex
```

### Method 2: Using md-to-pdf (Quick & Easy)

```bash
# Simple conversion
md-to-pdf COMPLETE_TEXTBOOK.md

# With options
md-to-pdf COMPLETE_TEXTBOOK.md \
  --pdf-options '{"format": "Letter", "margin": "1in"}'
```

### Method 3: Using Python

```python
# generate_pdf.py
import markdown
from weasyprint import HTML, CSS

def generate_pdf(markdown_file, output_pdf):
    with open(markdown_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    html = markdown.markdown(text, extensions=['extra', 'codehilite'])
    
    html_doc = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 1in; }}
            code {{ background: #f4f4f4; padding: 2px 5px; }}
            pre {{ background: #f4f4f4; padding: 10px; }}
        </style>
    </head>
    <body>{html}</body>
    </html>
    """
    
    HTML(string=html_doc).write_pdf(output_pdf)

generate_pdf('COMPLETE_TEXTBOOK.md', 'algorithms_textbook.pdf')
```

---

## Generate Critiques PDF

```bash
# Pandoc
pandoc CRITIQUES_AND_IMPROVEMENTS.md \
  -o critiques_improvements.pdf \
  --toc \
  --number-sections \
  -V geometry:margin=1in

# md-to-pdf
md-to-pdf CRITIQUES_AND_IMPROVEMENTS.md
```

---

## Generate Individual Semester PDFs

```bash
# Create PDFs for each semester
for i in {1..6}; do
  pandoc semester_$i/README.md \
    -o semester_${i}_textbook.pdf \
    --toc \
    -V documentclass=report
done
```

---

## Advanced: Combine All Content

### Step 1: Create Master Document

```bash
# combine_all.sh
#!/bin/bash

echo "# Complete Algorithms Course" > FULL_COURSE.md
echo "## All Content Combined" >> FULL_COURSE.md
echo "" >> FULL_COURSE.md

# Add main documentation
cat COURSE_PLAN_6SEMESTERS.md >> FULL_COURSE.md
echo -e "\n---\n" >> FULL_COURSE.md

# Add each semester
for i in {1..6}; do
  echo "# Semester $i" >> FULL_COURSE.md
  cat semester_$i/README.md >> FULL_COURSE.md
  echo -e "\n---\n" >> FULL_COURSE.md
  
  # Add each lecture
  for lecture in semester_$i/lecture_*/README.md; do
    if [ -f "$lecture" ]; then
      cat "$lecture" >> FULL_COURSE.md
      echo -e "\n---\n" >> FULL_COURSE.md
    fi
  done
done

# Add critiques
echo "# Critiques and Improvements" >> FULL_COURSE.md
cat CRITIQUES_AND_IMPROVEMENTS.md >> FULL_COURSE.md

echo "Master document created: FULL_COURSE.md"
```

### Step 2: Generate PDF

```bash
chmod +x combine_all.sh
./combine_all.sh

pandoc FULL_COURSE.md \
  -o complete_course.pdf \
  --toc \
  --toc-depth=2 \
  --number-sections \
  --pdf-engine=xelatex \
  -V documentclass=book \
  -V geometry:margin=1in \
  -V fontsize=10pt
```

---

## Customize PDF Appearance

### Create header.tex

```latex
% header.tex
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhead[L]{Algorithms Course}
\fancyhead[R]{\thepage}
\fancyfoot[C]{University Computer Science Department}

\usepackage{listings}
\lstset{
  basicstyle=\ttfamily\small,
  breaklines=true,
  frame=single,
  numbers=left,
  numberstyle=\tiny,
  keywordstyle=\color{blue},
  commentstyle=\color{gray},
  stringstyle=\color{red}
}
```

### Use with Pandoc

```bash
pandoc COMPLETE_TEXTBOOK.md \
  -o textbook.pdf \
  --include-in-header=header.tex \
  --toc \
  --pdf-engine=xelatex
```

---

## Generate Student vs. Instructor Versions

### Student Version (Without Solutions)

```bash
# Remove solution sections
sed '/## Solutions/,/## Next/d' COMPLETE_TEXTBOOK.md > STUDENT_VERSION.md

pandoc STUDENT_VERSION.md \
  -o student_textbook.pdf \
  --toc \
  -V documentclass=book
```

### Instructor Version (With Solutions)

```bash
pandoc COMPLETE_TEXTBOOK.md \
  -o instructor_textbook.pdf \
  --toc \
  --number-sections \
  -V documentclass=book
```

---

## Generate Chapter-by-Chapter PDFs

```bash
# generate_chapters.sh
#!/bin/bash

mkdir -p pdf_chapters

# Semester 1 chapters
cd semester_01
for lecture in lecture_*; do
  if [ -d "$lecture" ]; then
    echo "Generating PDF for $lecture"
    pandoc "$lecture/README.md" \
      -o "../pdf_chapters/${lecture}.pdf" \
      --toc \
      -V geometry:margin=1in
  fi
done
cd ..

echo "Chapter PDFs generated in pdf_chapters/"
```

---

## Online Conversion (No Installation)

If you don't want to install tools, use these online services:

1. **Pandoc Online**: https://pandoc.org/try/
   - Paste markdown
   - Select PDF output
   - Download

2. **Markdown to PDF**: https://www.markdowntopdf.com/
   - Upload markdown file
   - Download PDF

3. **Dillinger**: https://dillinger.io/
   - Open markdown
   - Export → PDF

4. **HackMD**: https://hackmd.io/
   - Create note
   - Export → PDF

---

## Batch Process All Documents

```bash
# generate_all_pdfs.sh
#!/bin/bash

echo "Generating all PDF documents..."

# Main documents
echo "1. Generating main textbook..."
pandoc COMPLETE_TEXTBOOK.md -o textbook.pdf --toc --number-sections

echo "2. Generating critiques..."
pandoc CRITIQUES_AND_IMPROVEMENTS.md -o critiques.pdf --toc

echo "3. Generating course plan..."
pandoc COURSE_PLAN_6SEMESTERS.md -o course_plan.pdf --toc

echo "4. Generating implementation guide..."
pandoc AI_IMPLEMENTATION_GUIDE.md -o implementation_guide.pdf --toc

echo "5. Generating quick start..."
pandoc QUICKSTART.md -o quickstart.pdf

# Create PDF directory
mkdir -p pdfs
mv *.pdf pdfs/

echo "All PDFs generated in pdfs/ directory!"
```

---

## Tips for Best Results

### 1. Clean Your Markdown

```bash
# Remove extra blank lines
sed -i '/^$/N;/^\n$/D' your_file.md

# Fix heading levels
# Ensure proper spacing around headers
```

### 2. Add Page Breaks

```markdown
<!-- For manual page breaks -->
\newpage

# Next Chapter
```

### 3. Include Images

```markdown
![Algorithm Visualization](images/merge_sort.png){ width=80% }
```

### 4. Add Footnotes

```markdown
This is text with a footnote[^1].

[^1]: This is the footnote content.
```

### 5. Custom Styling

Create `style.css`:
```css
body {
    font-family: 'Georgia', serif;
    line-height: 1.6;
    max-width: 800px;
    margin: auto;
}

code {
    background-color: #f4f4f4;
    padding: 2px 5px;
    border-radius: 3px;
}

pre {
    background-color: #f4f4f4;
    padding: 10px;
    border-left: 3px solid #333;
}
```

Use with Pandoc:
```bash
pandoc input.md -o output.pdf --css=style.css
```

---

## Troubleshooting

### Issue: "pdflatex not found"
**Solution**: Install TeX distribution (MiKTeX, TeXLive)

### Issue: Unicode characters not rendering
**Solution**: Use xelatex engine
```bash
pandoc input.md -o output.pdf --pdf-engine=xelatex
```

### Issue: Code blocks not syntax highlighted
**Solution**: Use highlight-style
```bash
pandoc input.md -o output.pdf --highlight-style=tango
```

### Issue: PDF too large
**Solution**: Compress images or split into multiple files

---

## Final PDF Package

After generation, you'll have:

```
pdfs/
├── textbook.pdf (Main course textbook)
├── critiques.pdf (Improvement suggestions)
├── course_plan.pdf (Detailed curriculum)
├── implementation_guide.pdf (AI implementation)
├── quickstart.pdf (Getting started)
├── semester_01.pdf (Semester 1 only)
├── semester_02.pdf (Semester 2 only)
├── semester_03.pdf (Semester 3 only)
├── semester_04.pdf (Semester 4 only)
├── semester_05.pdf (Semester 5 only)
└── semester_06.pdf (Semester 6 only)
```

---

## Automated Build Script

Create `build_pdfs.py`:

```python
#!/usr/bin/env python3
import subprocess
import os
from pathlib import Path

def run_pandoc(input_file, output_file, **options):
    """Run pandoc with options."""
    cmd = ['pandoc', str(input_file), '-o', str(output_file)]
    
    if options.get('toc'):
        cmd.append('--toc')
    if options.get('number_sections'):
        cmd.append('--number-sections')
    if options.get('pdf_engine'):
        cmd.extend(['--pdf-engine', options['pdf_engine']])
    
    print(f"Generating {output_file}...")
    subprocess.run(cmd, check=True)

def main():
    pdf_dir = Path('pdfs')
    pdf_dir.mkdir(exist_ok=True)
    
    documents = [
        ('COMPLETE_TEXTBOOK.md', 'textbook.pdf', {'toc': True, 'number_sections': True}),
        ('CRITIQUES_AND_IMPROVEMENTS.md', 'critiques.pdf', {'toc': True}),
        ('COURSE_PLAN_6SEMESTERS.md', 'course_plan.pdf', {'toc': True}),
        ('AI_IMPLEMENTATION_GUIDE.md', 'implementation_guide.pdf', {'toc': True}),
        ('QUICKSTART.md', 'quickstart.pdf', {}),
    ]
    
    for input_file, output_file, options in documents:
        if Path(input_file).exists():
            run_pandoc(input_file, pdf_dir / output_file, **options)
    
    print("\n✓ All PDFs generated successfully!")
    print(f"Output directory: {pdf_dir.absolute()}")

if __name__ == '__main__':
    main()
```

Run with:
```bash
python build_pdfs.py
```

---

**That's it!** You now have professional PDF textbooks from your markdown course materials.

