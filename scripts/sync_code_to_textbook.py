#!/usr/bin/env python3
"""
One-directional code synchronization script.

This script extracts code from individual algorithm files (Python, Java, SQL)
and updates the comprehensive textbook with the latest code.

IMPORTANT: This is ONE-DIRECTIONAL - changes to source files update the textbook,
but manual changes to the textbook do NOT affect source files. This ensures
individual files remain working and testable.

Usage:
    python scripts/sync_code_to_textbook.py [--insert-markers] [--update-code]
    
    --insert-markers: Insert code markers in textbook (one-time setup)
    --update-code: Update code blocks in textbook from source files (default)
"""

import re
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json


class CodeSync:
    """Synchronize code from algorithm files to textbook."""

    def __init__(self, root_dir: Path, textbook_path: Path):
        """
        Initialize code synchronizer.

        Args:
            root_dir: Root directory of the project
            textbook_path: Path to the comprehensive textbook markdown file
        """
        self.root_dir = root_dir
        self.textbook_path = textbook_path
        self.code_cache: Dict[str, str] = {}

    def find_algorithm_folders(self) -> List[Path]:
        """
        Find all algorithm folders in the project.

        Returns:
            List of algorithm folder paths
        """
        algorithm_folders = []
        semester_dirs = sorted(self.root_dir.glob("semester_*/lecture_*/*"))

        for path in semester_dirs:
            if path.is_dir():
                # Check if it's an algorithm folder (has algorithm.py or Algorithm.java)
                if (path / "algorithm.py").exists() or (path / "Algorithm.java").exists():
                    algorithm_folders.append(path)

        return algorithm_folders

    def read_code_file(self, file_path: Path) -> Optional[str]:
        """
        Read code from a file.

        Args:
            file_path: Path to the code file

        Returns:
            File contents or None if file doesn't exist
        """
        if not file_path.exists():
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None

    def get_relative_path(self, file_path: Path) -> str:
        """
        Get relative path from root directory.

        Args:
            file_path: Path to convert

        Returns:
            Relative path string
        """
        try:
            return str(file_path.relative_to(self.root_dir)).replace("\\", "/")
        except ValueError:
            return str(file_path)

    def extract_code_from_folder(self, folder: Path) -> Dict[str, str]:
        """
        Extract all code files from an algorithm folder.

        Args:
            folder: Algorithm folder path

        Returns:
            Dictionary mapping file types to code content
        """
        codes = {}

        # Python code
        python_file = folder / "algorithm.py"
        if python_file.exists():
            codes["python"] = self.read_code_file(python_file)

        # Java code
        java_file = folder / "Algorithm.java"
        if java_file.exists():
            codes["java"] = self.read_code_file(java_file)

        # SQL code
        sql_file = folder / "algorithm.sql"
        if sql_file.exists():
            codes["sql"] = self.read_code_file(sql_file)

        return codes

    def create_code_marker(self, relative_path: str, file_type: str) -> str:
        """
        Create a code marker for the textbook.

        Args:
            relative_path: Relative path to the code file
            file_type: Type of code (python, java, sql)

        Returns:
            Marker string
        """
        return f"<!-- CODE:{relative_path}:{file_type} -->"

    def create_end_marker(self) -> str:
        """Create end marker for code block."""
        return "<!-- END_CODE -->"

    def find_code_blocks_in_textbook(self) -> List[Tuple[str, str, str, int, int]]:
        """
        Find all code block markers in the textbook.

        Returns:
            List of tuples: (relative_path, file_type, marker, start_pos, end_pos)
        """
        if not self.textbook_path.exists():
            return []

        with open(self.textbook_path, "r", encoding="utf-8") as f:
            content = f.read()

        code_blocks = []
        pattern = r"<!-- CODE:([^:]+):(python|java|sql) -->"

        for match in re.finditer(pattern, content):
            relative_path = match.group(1)
            file_type = match.group(2)
            start_pos = match.start()

            # Find the end marker
            end_pattern = r"<!-- END_CODE -->"
            end_match = re.search(end_pattern, content[start_pos:])
            if end_match:
                end_pos = start_pos + end_match.end()
                code_blocks.append(
                    (relative_path, file_type, match.group(0), start_pos, end_pos)
                )

        return code_blocks

    def find_algorithm_section_in_textbook(
        self, algorithm_name: str, folder_path: Path, content: str
    ) -> Optional[int]:
        """
        Find where an algorithm is mentioned in the textbook.

        Args:
            algorithm_name: Name of the algorithm
            folder_path: Path to algorithm folder
            content: Textbook content

        Returns:
            Position where algorithm section starts, or None
        """
        # Try multiple patterns to find algorithm in textbook
        patterns = [
            rf"#+\s*{re.escape(algorithm_name)}",  # ## Algorithm Name
            rf"##\s*{re.escape(algorithm_name)}",  # ## Algorithm Name
            rf"\*\*{re.escape(algorithm_name)}\*\*",  # **Algorithm Name**
            rf"###\s*{re.escape(algorithm_name)}",  # ### Algorithm Name
        ]

        # Also try with underscores/spaces variations
        name_variations = [
            algorithm_name,
            algorithm_name.replace("_", " "),
            algorithm_name.replace("_", "-"),
            algorithm_name.title(),
            algorithm_name.replace("_", " ").title(),
        ]

        for name_var in name_variations:
            for pattern in patterns:
                pattern = pattern.replace(re.escape(algorithm_name), re.escape(name_var))
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    return match.start()

        return None

    def insert_code_markers_in_textbook(
        self, algorithm_folders: List[Path]
    ) -> int:
        """
        Insert code markers in the textbook if they don't exist.

        This is a one-time setup to add markers where code should be inserted.

        Args:
            algorithm_folders: List of algorithm folder paths

        Returns:
            Number of markers inserted
        """
        if not self.textbook_path.exists():
            print(f"Textbook not found: {self.textbook_path}")
            return 0

        with open(self.textbook_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Find existing markers
        existing_markers = set()
        for match in re.finditer(r"<!-- CODE:([^:]+):(python|java|sql) -->", content):
            existing_markers.add((match.group(1), match.group(2)))

        markers_inserted = 0
        insertions = []  # Store (position, marker_text) tuples

        # For each algorithm folder, check if markers exist
        for folder in algorithm_folders:
            rel_path = self.get_relative_path(folder)
            algorithm_name = folder.name

            # Find algorithm section in textbook
            section_pos = self.find_algorithm_section_in_textbook(
                algorithm_name, folder, content
            )

            if section_pos is None:
                # Try to find by path pattern
                path_pattern = rel_path.replace("\\", "/")
                section_pos = content.find(path_pattern)
                if section_pos == -1:
                    # Skip if we can't find the section
                    continue

            # Check Python
            if (folder / "algorithm.py").exists():
                marker_key = (f"{rel_path}/algorithm.py", "python")
                if marker_key not in existing_markers:
                    marker_text = (
                        f"\n\n<!-- CODE:{rel_path}/algorithm.py:python -->\n"
                        f"```python\n"
                        f"# Code will be synced from source file\n"
                        f"```\n"
                        f"<!-- END_CODE -->\n"
                    )
                    # Find a good insertion point (after "Implementation" section or similar)
                    insert_pos = self.find_insertion_point(
                        content, section_pos, "Implementation"
                    )
                    if insert_pos:
                        insertions.append((insert_pos, marker_text))
                        markers_inserted += 1

            # Check Java
            if (folder / "Algorithm.java").exists():
                marker_key = (f"{rel_path}/Algorithm.java", "java")
                if marker_key not in existing_markers:
                    marker_text = (
                        f"\n\n<!-- CODE:{rel_path}/Algorithm.java:java -->\n"
                        f"```java\n"
                        f"// Code will be synced from source file\n"
                        f"```\n"
                        f"<!-- END_CODE -->\n"
                    )
                    insert_pos = self.find_insertion_point(
                        content, section_pos, "Implementation"
                    )
                    if insert_pos:
                        insertions.append((insert_pos, marker_text))
                        markers_inserted += 1

            # Check SQL
            if (folder / "algorithm.sql").exists():
                marker_key = (f"{rel_path}/algorithm.sql", "sql")
                if marker_key not in existing_markers:
                    marker_text = (
                        f"\n\n<!-- CODE:{rel_path}/algorithm.sql:sql -->\n"
                        f"```sql\n"
                        f"-- Code will be synced from source file\n"
                        f"```\n"
                        f"<!-- END_CODE -->\n"
                    )
                    insert_pos = self.find_insertion_point(
                        content, section_pos, "Implementation"
                    )
                    if insert_pos:
                        insertions.append((insert_pos, marker_text))
                        markers_inserted += 1

        # Apply insertions in reverse order to maintain positions
        if insertions:
            insertions.sort(key=lambda x: x[0], reverse=True)
            for pos, marker_text in insertions:
                content = content[:pos] + marker_text + content[pos:]

            with open(self.textbook_path, "w", encoding="utf-8") as f:
                f.write(content)

        return markers_inserted

    def find_insertion_point(
        self, content: str, section_start: int, section_name: str
    ) -> Optional[int]:
        """
        Find a good insertion point for code marker.

        Args:
            content: Textbook content
            section_start: Start position of algorithm section
            section_name: Name of section to look for (e.g., "Implementation")

        Returns:
            Position to insert marker, or None
        """
        # Look for "Implementation" section after algorithm section
        search_start = section_start
        search_end = min(section_start + 5000, len(content))  # Search next 5000 chars

        pattern = rf"##+\s*{re.escape(section_name)}"
        match = re.search(pattern, content[search_start:search_end], re.IGNORECASE)
        if match:
            # Find end of Implementation section or next section
            impl_end = search_start + match.end()
            # Look for end of code block or next section
            next_section = re.search(
                r"^##+", content[impl_end : impl_end + 2000], re.MULTILINE
            )
            if next_section:
                return impl_end + next_section.start()
            else:
                # Insert before next major section or at reasonable distance
                return impl_end + 500
        else:
            # If no Implementation section, insert after algorithm description
            # Look for end of first paragraph or code block
            para_end = content.find("\n\n", section_start, section_start + 2000)
            if para_end != -1:
                return para_end + 2

        return None

    def update_textbook_with_code(self) -> bool:
        """
        Update textbook with latest code from algorithm files.

        Returns:
            True if textbook was updated, False otherwise
        """
        if not self.textbook_path.exists():
            print(f"Textbook not found: {self.textbook_path}")
            return False

        # Read textbook
        with open(self.textbook_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # Find all code blocks
        code_blocks = self.find_code_blocks_in_textbook()

        if not code_blocks:
            print("No code markers found in textbook. Run insert_code_markers first.")
            return False

        # Update each code block
        # Process in reverse order to maintain positions
        for relative_path, file_type, marker, start_pos, end_pos in reversed(
            code_blocks
        ):
            # Read the actual code file
            code_file_path = self.root_dir / relative_path

            if not code_file_path.exists():
                print(f"Warning: Code file not found: {relative_path}")
                continue

            code_content = self.read_code_file(code_file_path)
            if code_content is None:
                continue

            # Determine code block language
            lang_map = {"python": "python", "java": "java", "sql": "sql"}

            # Extract existing code block (if any) to preserve formatting
            existing_block = content[start_pos:end_pos]

            # Check if there's already a code fence
            code_fence_pattern = rf"{re.escape(marker)}\s*```{lang_map.get(file_type, '')}.*?```\s*{re.escape(self.create_end_marker())}"
            code_fence_match = re.search(code_fence_pattern, existing_block, re.DOTALL)

            if code_fence_match:
                # Replace existing code
                new_block = f"{marker}\n```{lang_map.get(file_type, '')}\n{code_content}\n```\n{self.create_end_marker()}"
            else:
                # Insert new code block
                new_block = f"{marker}\n```{lang_map.get(file_type, '')}\n{code_content}\n```\n{self.create_end_marker()}"

            # Replace in content
            content = content[:start_pos] + new_block + content[end_pos:]

        # Write updated textbook
        if content != original_content:
            with open(self.textbook_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Updated textbook: {self.textbook_path}")
            return True
        else:
            print("No changes needed in textbook.")
            return False

    def sync_all(self, insert_markers: bool = False, update_code: bool = True) -> None:
        """
        Sync all code files to textbook.

        Args:
            insert_markers: If True, insert code markers in textbook
            update_code: If True, update code blocks from source files
        """
        print("Finding algorithm folders...")
        algorithm_folders = self.find_algorithm_folders()
        print(f"Found {len(algorithm_folders)} algorithm folders")

        if insert_markers:
            print("\nInserting code markers in textbook...")
            markers_inserted = self.insert_code_markers_in_textbook(algorithm_folders)
            print(f"Inserted {markers_inserted} code markers")

        if update_code:
            print("\nUpdating textbook with latest code...")
            updated = self.update_textbook_with_code()

            if updated:
                print("\n[SUCCESS] Textbook updated successfully!")
            else:
                print("\n[INFO] Textbook is already up to date.")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Sync code from algorithm files to comprehensive textbook"
    )
    parser.add_argument(
        "--insert-markers",
        action="store_true",
        help="Insert code markers in textbook (one-time setup)",
    )
    parser.add_argument(
        "--update-code",
        action="store_true",
        default=True,
        help="Update code blocks from source files (default: True)",
    )
    parser.add_argument(
        "--no-update",
        action="store_false",
        dest="update_code",
        help="Skip code updates (only insert markers)",
    )

    args = parser.parse_args()

    root_dir = Path(__file__).parent.parent
    textbook_path = root_dir / "COMPREHENSIVE_COURSE_TEXTBOOK.md"

    print("=" * 70)
    print("Code Synchronization Tool")
    print("=" * 70)
    print(f"Root directory: {root_dir}")
    print(f"Textbook: {textbook_path}")
    print("=" * 70)
    print()

    sync = CodeSync(root_dir, textbook_path)
    sync.sync_all(
        insert_markers=args.insert_markers, update_code=args.update_code
    )

    print()
    print("=" * 70)
    print("Note: This is a ONE-DIRECTIONAL sync.")
    print("Changes to source files → update textbook")
    print("Manual changes to textbook → do NOT affect source files")
    print("=" * 70)


if __name__ == "__main__":
    main()

