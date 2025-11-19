#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate PDF textbooks from markdown files.

Requires: pip install markdown reportlab pymdown-extensions
"""

import os
import sys
from pathlib import Path
from typing import List
import markdown
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
    Image as RLImage,
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import datetime


class PDFGenerator:
    """Generate PDF from markdown files."""

    def __init__(self, output_file: str, title: str):
        """Initialize PDF generator."""
        self.output_file = output_file
        self.title = title
        self.doc = SimpleDocTemplate(
            output_file,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )
        self.styles = getSampleStyleSheet()
        self.story = []

        # Custom styles
        self.styles.add(
            ParagraphStyle(
                name="CustomTitle",
                parent=self.styles["Title"],
                fontSize=24,
                textColor=colors.HexColor("#667eea"),
                spaceAfter=30,
                alignment=TA_CENTER,
            )
        )

        self.styles.add(
            ParagraphStyle(
                name="CustomHeading1",
                parent=self.styles["Heading1"],
                fontSize=18,
                textColor=colors.HexColor("#764ba2"),
                spaceAfter=12,
                spaceBefore=12,
            )
        )

        self.styles.add(
            ParagraphStyle(
                name="Code",
                parent=self.styles["Code"],
                fontSize=9,
                leftIndent=20,
                rightIndent=20,
                spaceAfter=10,
                spaceBefore=10,
            )
        )

    def add_cover_page(self):
        """Add cover page."""
        self.story.append(Spacer(1, 2 * inch))

        title = Paragraph(self.title, self.styles["CustomTitle"])
        self.story.append(title)
        self.story.append(Spacer(1, 0.3 * inch))

        subtitle = Paragraph(
            "Computer Science Algorithms Course<br/>6 Semesters",
            self.styles["Heading2"],
        )
        self.story.append(subtitle)
        self.story.append(Spacer(1, 0.5 * inch))

        author = Paragraph(
            "University Professor of Computer Science", self.styles["Normal"]
        )
        self.story.append(author)
        self.story.append(Spacer(1, 0.2 * inch))

        date = Paragraph(
            f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d')}",
            self.styles["Normal"],
        )
        self.story.append(date)

        self.story.append(PageBreak())

    def add_markdown_file(self, filepath: Path):
        """Add markdown file to PDF."""
        if not filepath.exists():
            print(f"Warning: {filepath} not found")
            return

        content = filepath.read_text(encoding="utf-8")

        # Convert markdown to HTML
        html = markdown.markdown(
            content, extensions=["tables", "fenced_code", "codehilite"]
        )

        # Convert HTML to ReportLab elements
        self._html_to_elements(html)

    def _html_to_elements(self, html: str):
        """Convert HTML to ReportLab elements."""
        # Simple HTML parsing (you may want to use a proper HTML parser)
        lines = html.split("\n")

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Headings
            if line.startswith("<h1>"):
                text = line.replace("<h1>", "").replace("</h1>", "")
                self.story.append(Paragraph(text, self.styles["CustomHeading1"]))
                self.story.append(Spacer(1, 0.2 * inch))
            elif line.startswith("<h2>"):
                text = line.replace("<h2>", "").replace("</h2>", "")
                self.story.append(Paragraph(text, self.styles["Heading2"]))
                self.story.append(Spacer(1, 0.1 * inch))
            elif line.startswith("<h3>"):
                text = line.replace("<h3>", "").replace("</h3>", "")
                self.story.append(Paragraph(text, self.styles["Heading3"]))
            # Code
            elif line.startswith("<code>"):
                text = line.replace("<code>", "").replace("</code>", "")
                self.story.append(Paragraph(text, self.styles["Code"]))
            # Paragraphs
            elif line.startswith("<p>"):
                text = line.replace("<p>", "").replace("</p>", "")
                self.story.append(Paragraph(text, self.styles["Normal"]))
                self.story.append(Spacer(1, 0.1 * inch))

    def add_table_of_contents(self, sections: List[str]):
        """Add table of contents."""
        self.story.append(Paragraph("Table of Contents", self.styles["CustomHeading1"]))
        self.story.append(Spacer(1, 0.2 * inch))

        for i, section in enumerate(sections, 1):
            text = f"{i}. {section}"
            self.story.append(Paragraph(text, self.styles["Normal"]))
            self.story.append(Spacer(1, 0.1 * inch))

        self.story.append(PageBreak())

    def build(self):
        """Build the PDF."""
        try:
            self.doc.build(self.story)
            print(f"✓ PDF generated: {self.output_file}")
            return True
        except Exception as e:
            print(f"✗ Error generating PDF: {e}")
            return False


def generate_main_textbook():
    """Generate main course textbook PDF."""
    print("\n" + "=" * 70)
    print("Generating Main Course Textbook PDF")
    print("=" * 70)

    pdf = PDFGenerator(
        "Algorithms_Course_Textbook.pdf", "Algorithms Course - 6 Semesters"
    )

    # Add cover
    pdf.add_cover_page()

    # Add table of contents
    sections = [
        "Introduction",
        "Course Overview",
        "Semester 1: Foundations",
        "Semester 2: Design Patterns",
        "Semester 3: Advanced Algorithms & ML",
        "Semester 4: ML & Enterprise",
        "Semester 5: Deep Learning & AI",
        "Semester 6: Production ML",
        "Algorithm Index",
        "References",
    ]
    pdf.add_table_of_contents(sections)

    # Add main content
    files_to_include = [
        "README.md",
        "COURSE_PLAN_6SEMESTERS.md",
        "ALGORITHM_INDEX.md",
        "semester_01/README.md",
        "semester_02/README.md",
        "semester_03/README.md",
        "semester_04/README.md",
        "semester_05/README.md",
        "semester_06/README.md",
    ]

    for filepath in files_to_include:
        path = Path(filepath)
        if path.exists():
            print(f"Adding: {filepath}")
            pdf.add_markdown_file(path)
            pdf.story.append(PageBreak())

    # Build PDF
    success = pdf.build()

    if success:
        file_size = Path("Algorithms_Course_Textbook.pdf").stat().st_size
        print(f"File size: {file_size / 1024 / 1024:.2f} MB")

    return success


def generate_improvements_pdf():
    """Generate improvements and critiques PDF."""
    print("\n" + "=" * 70)
    print("Generating Improvements & Critiques PDF")
    print("=" * 70)

    pdf = PDFGenerator(
        "Algorithms_Course_Improvements.pdf", "Professional Critiques & Improvements"
    )

    # Add cover
    pdf.add_cover_page()

    # Add table of contents
    sections = [
        "Overview",
        "Teacher's Critique",
        "Programmer's Critique",
        "Student's Critique",
        "Implementation Plan",
        "Priority Matrix",
        "Impact Analysis",
    ]
    pdf.add_table_of_contents(sections)

    # Add critiques
    files = [
        "CRITIQUES.md",
        "IMPLEMENTATION_STATUS.md",
        "AI_IMPLEMENTATION_GUIDE.md",
    ]

    for filepath in files:
        path = Path(filepath)
        if path.exists():
            print(f"Adding: {filepath}")
            pdf.add_markdown_file(path)
            pdf.story.append(PageBreak())

    # Build PDF
    success = pdf.build()

    if success:
        file_size = Path("Algorithms_Course_Improvements.pdf").stat().st_size
        print(f"File size: {file_size / 1024 / 1024:.2f} MB")

    return success


def main():
    """Main entry point."""
    print("\n" + "=" * 70)
    print("PDF GENERATION SYSTEM")
    print("=" * 70)
    print()

    # Check dependencies
    try:
        import markdown
        import reportlab

        print("✓ Dependencies installed")
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("\nInstall with:")
        print("pip install markdown reportlab pymdown-extensions")
        return 1

    # Generate PDFs
    print("\nGenerating PDFs...")
    print()

    success1 = generate_main_textbook()
    success2 = generate_improvements_pdf()

    print("\n" + "=" * 70)
    if success1 and success2:
        print("✅ All PDFs generated successfully!")
        print()
        print("Generated files:")
        print("  1. Algorithms_Course_Textbook.pdf")
        print("  2. Algorithms_Course_Improvements.pdf")
    else:
        print("⚠️ Some PDFs failed to generate")
    print("=" * 70)

    return 0 if (success1 and success2) else 1


if __name__ == "__main__":
    sys.exit(main())
