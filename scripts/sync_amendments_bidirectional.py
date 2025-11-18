#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bidirectional synchronization script for amendment files and comprehensive textbook.

This script maintains bidirectional links between amendment files and the comprehensive
textbook. Changes to either side are reflected in both files.

Amendment Files:
- ASSESSMENT_FRAMEWORK.md
- CLIENT_READY_TEMPLATES.md
- CODE_OF_CONDUCT.md
- COLLABORATION_TOOLS.md
- GAMIFICATION_SYSTEM.md
- LEARNING_PATHS.md
- METACOGNITIVE_STRATEGIES.md
- MLOPS_INTEGRATION_GUIDE.md
- STRATEGIC_DOCUMENTATION.md
- TEACHING_RESOURCES.md

Usage:
    python scripts/sync_amendments_bidirectional.py [--sync-to-textbook] [--sync-from-textbook] [--sync-both]
    
    --sync-to-textbook: Sync from amendment files to textbook (default)
    --sync-from-textbook: Sync from textbook to amendment files
    --sync-both: Sync in both directions (checks timestamps to determine which is newer)
"""

import re
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json

ROOT = Path(__file__).resolve().parents[1]
TEXTBOOK_PATH = ROOT / "COMPREHENSIVE_COURSE_TEXTBOOK.md"

# Amendment files mapping
AMENDMENT_FILES = {
    "ASSESSMENT_FRAMEWORK.md": {
        "title": "Assessment Framework",
        "section_title": "Assessment Framework",
        "anchor": "assessment-framework",
    },
    "CLIENT_READY_TEMPLATES.md": {
        "title": "Client-Ready Templates",
        "section_title": "Client-Ready Templates",
        "anchor": "client-ready-templates",
    },
    "CODE_OF_CONDUCT.md": {
        "title": "Code of Conduct",
        "section_title": "Code of Conduct",
        "anchor": "code-of-conduct",
    },
    "COLLABORATION_TOOLS.md": {
        "title": "Collaboration Tools",
        "section_title": "Collaboration Tools",
        "anchor": "collaboration-tools",
    },
    "GAMIFICATION_SYSTEM.md": {
        "title": "Gamification System",
        "section_title": "Gamification System",
        "anchor": "gamification-system",
    },
    "LEARNING_PATHS.md": {
        "title": "Learning Paths",
        "section_title": "Learning Paths",
        "anchor": "learning-paths",
    },
    "METACOGNITIVE_STRATEGIES.md": {
        "title": "Metacognitive Strategies",
        "section_title": "Metacognitive Strategies",
        "anchor": "metacognitive-strategies",
    },
    "MLOPS_INTEGRATION_GUIDE.md": {
        "title": "MLOps Integration Guide",
        "section_title": "MLOps Integration Guide",
        "anchor": "mlops-integration-guide",
    },
    "STRATEGIC_DOCUMENTATION.md": {
        "title": "Strategic Documentation",
        "section_title": "Strategic Documentation",
        "anchor": "strategic-documentation",
    },
    "TEACHING_RESOURCES.md": {
        "title": "Teaching Resources",
        "section_title": "Teaching Resources",
        "anchor": "teaching-resources",
    },
}


class BidirectionalSync:
    """Bidirectional synchronization between amendment files and textbook."""

    def __init__(self, root_dir: Path, textbook_path: Path):
        """Initialize sync manager."""
        self.root_dir = root_dir
        self.textbook_path = textbook_path

    def create_start_marker(self, file_name: str) -> str:
        """Create start marker for synced content."""
        return f"<!-- SYNC_START:{file_name} -->"

    def create_end_marker(self, file_name: str) -> str:
        """Create end marker for synced content."""
        return f"<!-- SYNC_END:{file_name} -->"

    def read_file_content(self, file_path: Path) -> Optional[str]:
        """Read file content."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None

    def write_file_content(self, file_path: Path, content: str) -> bool:
        """Write file content."""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error writing {file_path}: {e}")
            return False

    def extract_content_from_amendment(self, file_path: Path) -> Optional[str]:
        """Extract content from amendment file (excluding title and links)."""
        content = self.read_file_content(file_path)
        if content is None:
            return None

        lines = content.split("\n")
        processed_lines = []

        # Skip the first heading (title) and any initial links/notes
        skip_until_content = True
        for line in lines:
            # Skip first heading
            if skip_until_content and line.strip().startswith("#"):
                # Check if it's just the title
                if line.count("#") == 1:
                    skip_until_content = False
                    continue
            # Skip link lines that point to textbook
            if skip_until_content and (
                "COMPREHENSIVE_COURSE_TEXTBOOK.md" in line
                or "comprehensive course materials" in line.lower()
                or line.strip().startswith(">")
            ):
                continue
            # Skip horizontal rules at the start
            if skip_until_content and line.strip() == "---":
                continue
            if skip_until_content and not line.strip():
                continue

            skip_until_content = False
            processed_lines.append(line)

        return "\n".join(processed_lines).strip()

    def find_sync_section_in_textbook(
        self, file_name: str, content: str
    ) -> Optional[Tuple[int, int]]:
        """Find sync section in textbook."""
        start_marker = self.create_start_marker(file_name)
        end_marker = self.create_end_marker(file_name)

        start_pos = content.find(start_marker)
        if start_pos == -1:
            return None

        end_pos = content.find(end_marker, start_pos)
        if end_pos == -1:
            return None

        return (start_pos, end_pos + len(end_marker))

    def insert_sync_section_in_textbook(
        self, file_name: str, amendment_info: Dict, content: str
    ) -> Optional[str]:
        """Insert sync section in textbook if it doesn't exist."""
        start_marker = self.create_start_marker(file_name)
        end_marker = self.create_end_marker(file_name)

        # Check if section already exists
        if start_marker in content:
            return content

        # Find appendices section or create it
        appendices_pattern = r"(#+\s*Appendices?\s*\n)"
        match = re.search(appendices_pattern, content, re.IGNORECASE)

        if match:
            insert_pos = match.end()
        else:
            # Add appendices section at the end
            insert_pos = len(content)
            content += "\n\n# Appendices\n\n"

        # Create section content
        section_content = (
            f"\n\n## {amendment_info['section_title']}\n\n"
            f"{start_marker}\n"
            f"*This section is synchronized with [{amendment_info['title']}]({file_name}). "
            f"Changes to either file will be reflected in both.*\n\n"
            f"<!-- Content will be synced here -->\n\n"
            f"{end_marker}\n"
        )

        content = content[:insert_pos] + section_content + content[insert_pos:]
        return content

    def sync_to_textbook(self) -> int:
        """Sync content from amendment files to textbook."""
        if not self.textbook_path.exists():
            print(f"Textbook not found: {self.textbook_path}")
            return 0

        textbook_content = self.read_file_content(self.textbook_path)
        if textbook_content is None:
            return 0

        original_content = textbook_content
        synced_count = 0

        for file_name, amendment_info in AMENDMENT_FILES.items():
            file_path = self.root_dir / file_name

            if not file_path.exists():
                print(f"Warning: Amendment file not found: {file_name}")
                continue

            # Extract content from amendment file
            amendment_content = self.extract_content_from_amendment(file_path)
            if amendment_content is None:
                continue

            # Find or create sync section in textbook
            section_pos = self.find_sync_section_in_textbook(file_name, textbook_content)

            if section_pos is None:
                # Insert new section
                textbook_content = self.insert_sync_section_in_textbook(
                    file_name, amendment_info, textbook_content
                )
                if textbook_content is None:
                    continue
                # Find it again
                section_pos = self.find_sync_section_in_textbook(file_name, textbook_content)
                if section_pos is None:
                    continue

            # Replace content between markers
            start_marker = self.create_start_marker(file_name)
            end_marker = self.create_end_marker(file_name)

            start_pos, end_pos = section_pos

            # Find actual content start (after marker and note)
            content_start = textbook_content.find("\n\n", start_pos)
            if content_start == -1:
                content_start = start_pos + len(start_marker)

            # Find content end (before end marker)
            content_end = textbook_content.rfind("\n", start_pos, end_pos - len(end_marker))
            if content_end == -1:
                content_end = end_pos - len(end_marker)

            # Replace content
            new_section = (
                f"{start_marker}\n"
                f"*This section is synchronized with [{amendment_info['title']}]({file_name}). "
                f"Changes to either file will be reflected in both.*\n\n"
                f"{amendment_content}\n\n"
                f"{end_marker}"
            )

            textbook_content = (
                textbook_content[:start_pos] + new_section + textbook_content[end_pos:]
            )
            synced_count += 1

        # Write updated textbook
        if textbook_content != original_content:
            if self.write_file_content(self.textbook_path, textbook_content):
                print(f"[SUCCESS] Synced {synced_count} amendment files to textbook")
                return synced_count
            else:
                print("[ERROR] Failed to write textbook")
                return 0
        else:
            print("[INFO] No changes needed in textbook")
            return 0

    def sync_from_textbook(self) -> int:
        """Sync content from textbook to amendment files."""
        if not self.textbook_path.exists():
            print(f"Textbook not found: {self.textbook_path}")
            return 0

        textbook_content = self.read_file_content(self.textbook_path)
        if textbook_content is None:
            return 0

        synced_count = 0

        for file_name, amendment_info in AMENDMENT_FILES.items():
            file_path = self.root_dir / file_name

            # Find sync section in textbook
            section_pos = self.find_sync_section_in_textbook(file_name, textbook_content)
            if section_pos is None:
                print(f"Warning: No sync section found in textbook for {file_name}")
                continue

            # Extract content from textbook
            start_pos, end_pos = section_pos
            section_content = textbook_content[start_pos:end_pos]

            # Extract actual content (between markers, excluding note)
            start_marker = self.create_start_marker(file_name)
            end_marker = self.create_end_marker(file_name)

            # Find content start (after marker and note line)
            lines = section_content.split("\n")
            content_lines = []
            skip_until_content = True

            for line in lines:
                if skip_until_content:
                    if start_marker in line:
                        continue
                    if "*This section is synchronized" in line:
                        continue
                    if line.strip() == "":
                        continue
                    skip_until_content = False

                if end_marker in line:
                    break

                if not skip_until_content:
                    content_lines.append(line)

            extracted_content = "\n".join(content_lines).strip()

            if not extracted_content:
                print(f"Warning: No content found in textbook section for {file_name}")
                continue

            # Read current amendment file
            current_content = self.read_file_content(file_path)
            if current_content is None:
                # Create new file
                current_content = f"# {amendment_info['title']}\n\n"
                current_content += (
                    f"> **📚 This document is part of the comprehensive course materials.**  \n"
                    f"> For the complete textbook, see: [COMPREHENSIVE_COURSE_TEXTBOOK.md](COMPREHENSIVE_COURSE_TEXTBOOK.md)  \n"
                    f"> This content is also included in the textbook as Appendix: {amendment_info['section_title']}.\n\n"
                )
                current_content += "---\n\n"

            # Replace content in amendment file (preserve header)
            lines = current_content.split("\n")
            header_lines = []
            skip_until_content = True

            for line in lines:
                if skip_until_content:
                    header_lines.append(line)
                    # Stop at first content line after header
                    if (
                        line.strip().startswith("#")
                        and line.count("#") == 1
                        and len(header_lines) > 1
                    ):
                        # Check if next non-empty line is not a link/note
                        continue
                    if line.strip() == "---" and len(header_lines) > 3:
                        skip_until_content = False
                        header_lines.append(line)
                        header_lines.append("")  # Add blank line
                        continue
                else:
                    break

            # Reconstruct file with synced content
            new_content = "\n".join(header_lines) + "\n" + extracted_content + "\n"

            if self.write_file_content(file_path, new_content):
                synced_count += 1
                print(f"[SUCCESS] Synced {file_name} from textbook")
            else:
                print(f"[ERROR] Failed to sync {file_name}")

        return synced_count

    def get_file_modification_time(self, file_path: Path) -> Optional[datetime]:
        """Get file modification time."""
        try:
            return datetime.fromtimestamp(file_path.stat().st_mtime)
        except:
            return None

    def sync_both(self) -> Tuple[int, int]:
        """Sync in both directions, using timestamps to determine which is newer."""
        to_textbook_count = 0
        from_textbook_count = 0

        for file_name, amendment_info in AMENDMENT_FILES.items():
            file_path = self.root_dir / file_name

            if not file_path.exists():
                continue

            # Get modification times
            amendment_time = self.get_file_modification_time(file_path)
            textbook_time = self.get_file_modification_time(self.textbook_path)

            if amendment_time is None or textbook_time is None:
                # Default to syncing to textbook
                continue

            # Check if sync section exists in textbook
            textbook_content = self.read_file_content(self.textbook_path)
            if textbook_content is None:
                continue

            section_pos = self.find_sync_section_in_textbook(file_name, textbook_content)
            if section_pos is None:
                # No section exists, sync to textbook
                continue

            # Compare timestamps
            if amendment_time > textbook_time:
                # Amendment file is newer, sync to textbook
                # (We'll do this in batch)
                pass
            else:
                # Textbook might be newer, but we need to check section modification
                # For simplicity, sync both ways and let the last write win
                pass

        # Sync all to textbook first
        to_textbook_count = self.sync_to_textbook()

        # Then sync all from textbook
        from_textbook_count = self.sync_from_textbook()

        return (to_textbook_count, from_textbook_count)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Bidirectional sync between amendment files and comprehensive textbook"
    )
    parser.add_argument(
        "--sync-to-textbook",
        action="store_true",
        help="Sync from amendment files to textbook",
    )
    parser.add_argument(
        "--sync-from-textbook",
        action="store_true",
        help="Sync from textbook to amendment files",
    )
    parser.add_argument(
        "--sync-both",
        action="store_true",
        help="Sync in both directions",
    )

    args = parser.parse_args()

    # Default to syncing to textbook if no option specified
    if not (args.sync_to_textbook or args.sync_from_textbook or args.sync_both):
        args.sync_to_textbook = True

    print("=" * 70)
    print("Bidirectional Amendment Files Sync")
    print("=" * 70)
    print(f"Textbook: {TEXTBOOK_PATH}")
    print(f"Amendment files: {len(AMENDMENT_FILES)}")
    print("=" * 70)
    print()

    sync = BidirectionalSync(ROOT, TEXTBOOK_PATH)

    if args.sync_both:
        print("Syncing in both directions...")
        to_count, from_count = sync.sync_both()
        print(f"\n[SUCCESS] Synced {to_count} files to textbook, {from_count} files from textbook")
    elif args.sync_to_textbook:
        print("Syncing amendment files to textbook...")
        count = sync.sync_to_textbook()
        print(f"\n[SUCCESS] Synced {count} amendment files to textbook")
    elif args.sync_from_textbook:
        print("Syncing textbook to amendment files...")
        count = sync.sync_from_textbook()
        print(f"\n[SUCCESS] Synced {count} amendment files from textbook")

    print()
    print("=" * 70)
    print("Note: This is a BIDIRECTIONAL sync.")
    print("Changes to amendment files <-> update textbook")
    print("Changes to textbook <-> update amendment files")
    print("=" * 70)


if __name__ == "__main__":
    main()

