"""
markdown_parser.py

Parse algorithm markdown files (school.en.md, school.ru.md, univer.en.md, univer.ru.md)
and extract structured content for database storage.
"""

import re
from pathlib import Path
from typing import Dict, Optional, List
from dataclasses import dataclass


@dataclass
class ParsedMarkdown:
    """Structured representation of parsed markdown content."""
    title: str = ""
    discipline: str = ""
    algorithm_name: str = ""
    
    # School level fields
    simple_explanation: str = ""
    where_its_used: str = ""
    example: str = ""
    
    # University level fields
    algorithm_definition: str = ""
    technical_description: str = ""
    application: str = ""
    step_by_step: str = ""
    
    # Common fields
    self_check_basic: str = ""
    self_check_intermediate: str = ""
    self_check_advanced: str = ""
    practical_tasks_basic: str = ""
    practical_tasks_applied: str = ""
    practical_tasks_research: str = ""
    ethical_reasoning: str = ""
    ethical_note: str = ""  # school level uses "Ethical Note"
    
    # Extra content stored as dict
    extra: Dict = None
    
    def __post_init__(self):
        if self.extra is None:
            self.extra = {}


def extract_section_content(markdown_text: str, section_pattern: str, 
                           next_section_pattern: Optional[str] = None) -> str:
    """
    Extract content of a section from markdown text.
    
    Args:
        markdown_text: Full markdown text
        section_pattern: Regex pattern to match section header
        next_section_pattern: Optional pattern for next section to stop at
    
    Returns:
        Extracted content as string
    """
    # Find the section
    section_match = re.search(section_pattern, markdown_text, re.IGNORECASE | re.MULTILINE)
    if not section_match:
        return ""
    
    start_pos = section_match.end()
    
    # Find end position (next section or end of text)
    if next_section_pattern:
        next_match = re.search(next_section_pattern, markdown_text[start_pos:], re.IGNORECASE | re.MULTILINE)
        if next_match:
            end_pos = start_pos + next_match.start()
        else:
            end_pos = len(markdown_text)
    else:
        # Look for next ## or ### header
        next_header = re.search(r'^##+ ', markdown_text[start_pos:], re.MULTILINE)
        if next_header:
            end_pos = start_pos + next_header.start()
        else:
            end_pos = len(markdown_text)
    
    content = markdown_text[start_pos:end_pos].strip()
    # Remove leading/trailing whitespace and normalize
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content.strip()


def extract_list_items(content: str) -> str:
    """Extract list items and format them."""
    lines = content.split('\n')
    items = []
    for line in lines:
        line = line.strip()
        if line.startswith('-') or line.startswith('*') or re.match(r'^\d+\.', line):
            items.append(line)
        elif line and not line.startswith('#'):
            # Continuation of previous item
            if items:
                items[-1] += ' ' + line
            else:
                items.append(line)
    return '\n'.join(items) if items else content


def parse_school_markdown(markdown_path: Path) -> Optional[ParsedMarkdown]:
    """
    Parse school-level markdown file (school.en.md or school.ru.md).
    
    Expected structure:
    - # Title
    - ## Simple Explanation
    - ## Where It's Used
    - ## Example
    - ## Self-Check Questions (with ### Basic, ### Intermediate, ### Advanced)
    - ## Practical Tasks (with ### Level 1, ### Level 2, ### Level 3)
    - ## Ethical Note (or --- followed by **Ethical Note:**)
    """
    if not markdown_path.exists():
        return None
    
    try:
        content = markdown_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {markdown_path}: {e}")
        return None
    
    parsed = ParsedMarkdown()
    
    # Extract title (first H1)
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        parsed.title = title_match.group(1).strip()
    
    # Simple Explanation
    parsed.simple_explanation = extract_section_content(
        content, 
        r'^##\s+Simple Explanation|^##\s+Простое объяснение',
        r'^##\s+'
    )
    
    # Where It's Used
    parsed.where_its_used = extract_section_content(
        content,
        r'^##\s+Where It\'s Used|^##\s+Где применяется',
        r'^##\s+'
    )
    parsed.where_its_used = extract_list_items(parsed.where_its_used)
    
    # Example
    parsed.example = extract_section_content(
        content,
        r'^##\s+Example|^##\s+Пример',
        r'^##\s+'
    )
    
    # Self-Check Questions
    self_check_section = extract_section_content(
        content,
        r'^##\s+Self-Check Questions|^##\s+Вопросы для самопроверки',
        r'^##\s+'
    )
    
    # Extract Basic level
    basic_match = re.search(r'^###\s+Basic|^###\s+Базовые', self_check_section, re.MULTILINE | re.IGNORECASE)
    if basic_match:
        intermediate_match = re.search(r'^###\s+Intermediate|^###\s+Средние', 
                                       self_check_section[basic_match.end():], re.MULTILINE | re.IGNORECASE)
        end_pos = basic_match.end() + (intermediate_match.start() if intermediate_match else len(self_check_section))
        parsed.self_check_basic = self_check_section[basic_match.end():end_pos].strip()
        parsed.self_check_basic = extract_list_items(parsed.self_check_basic)
    
    # Extract Intermediate level
    intermediate_match = re.search(r'^###\s+Intermediate|^###\s+Средние', self_check_section, re.MULTILINE | re.IGNORECASE)
    if intermediate_match:
        advanced_match = re.search(r'^###\s+Advanced|^###\s+Сложные',
                                   self_check_section[intermediate_match.end():], re.MULTILINE | re.IGNORECASE)
        end_pos = intermediate_match.end() + (advanced_match.start() if advanced_match else len(self_check_section))
        parsed.self_check_intermediate = self_check_section[intermediate_match.end():end_pos].strip()
        parsed.self_check_intermediate = extract_list_items(parsed.self_check_intermediate)
    
    # Extract Advanced level
    advanced_match = re.search(r'^###\s+Advanced|^###\s+Сложные', self_check_section, re.MULTILINE | re.IGNORECASE)
    if advanced_match:
        parsed.self_check_advanced = self_check_section[advanced_match.end():].strip()
        parsed.self_check_advanced = extract_list_items(parsed.self_check_advanced)
    
    # Practical Tasks
    practical_section = extract_section_content(
        content,
        r'^##\s+Practical Tasks|^##\s+Практические задания',
        r'^##\s+'
    )
    
    # Extract Level 1
    level1_match = re.search(r'^###\s+Level\s+1|^###\s+Уровень\s+1', practical_section, re.MULTILINE | re.IGNORECASE)
    if level1_match:
        level2_match = re.search(r'^###\s+Level\s+2|^###\s+Уровень\s+2',
                                 practical_section[level1_match.end():], re.MULTILINE | re.IGNORECASE)
        end_pos = level1_match.end() + (level2_match.start() if level2_match else len(practical_section))
        parsed.practical_tasks_basic = practical_section[level1_match.end():end_pos].strip()
    
    # Extract Level 2
    level2_match = re.search(r'^###\s+Level\s+2|^###\s+Уровень\s+2', practical_section, re.MULTILINE | re.IGNORECASE)
    if level2_match:
        level3_match = re.search(r'^###\s+Level\s+3|^###\s+Уровень\s+3',
                                practical_section[level2_match.end():], re.MULTILINE | re.IGNORECASE)
        end_pos = level2_match.end() + (level3_match.start() if level3_match else len(practical_section))
        parsed.practical_tasks_applied = practical_section[level2_match.end():end_pos].strip()
    
    # Extract Level 3
    level3_match = re.search(r'^###\s+Level\s+3|^###\s+Уровень\s+3', practical_section, re.MULTILINE | re.IGNORECASE)
    if level3_match:
        parsed.practical_tasks_research = practical_section[level3_match.end():].strip()
    
    # Ethical Note
    ethical_match = re.search(r'^---\s*\n\s*\*\*Ethical Note:\*\*|^---\s*\n\s*\*\*Этическое замечание:\*\*', 
                             content, re.MULTILINE | re.IGNORECASE)
    if ethical_match:
        parsed.ethical_note = content[ethical_match.end():].strip()
    else:
        # Try alternative pattern
        ethical_match = re.search(r'\*\*Ethical Note:\*\*|\*\*Этическое замечание:\*\*', content, re.IGNORECASE)
        if ethical_match:
            parsed.ethical_note = content[ethical_match.end():].strip()
    
    return parsed


def parse_university_markdown(markdown_path: Path) -> Optional[ParsedMarkdown]:
    """
    Parse university-level markdown file (univer.en.md or univer.ru.md).
    
    Expected structure:
    - # Title
    - **Algorithm:** name
    - **Discipline:** discipline
    - ## Algorithm Definition
    - ## Technical Description
    - ## Application in Machine Learning / AI
    - ## Step-by-Step Scenario
    - ## Self-Check Questions (with ### Basic Level, ### Intermediate Level, ### Advanced Level)
    - ## Practical Tasks (with ### Level 1 — Basic, ### Level 2 — Applied, ### Level 3 — Research)
    - ## Ethical Reasoning
    """
    if not markdown_path.exists():
        return None
    
    try:
        content = markdown_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {markdown_path}: {e}")
        return None
    
    parsed = ParsedMarkdown()
    
    # Extract title (first H1)
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        parsed.title = title_match.group(1).strip()
    
    # Extract Algorithm name from metadata
    algo_match = re.search(r'\*\*Algorithm:\*\*\s*(.+)', content, re.IGNORECASE)
    if algo_match:
        parsed.algorithm_name = algo_match.group(1).strip()
    
    # Extract Discipline
    discipline_match = re.search(r'\*\*Discipline:\*\*\s*(.+)', content, re.IGNORECASE)
    if discipline_match:
        parsed.discipline = discipline_match.group(1).strip()
    
    # Algorithm Definition
    parsed.algorithm_definition = extract_section_content(
        content,
        r'^##\s+Algorithm Definition|^##\s+Определение алгоритма',
        r'^##\s+'
    )
    
    # Technical Description
    parsed.technical_description = extract_section_content(
        content,
        r'^##\s+Technical Description|^##\s+Техническое описание',
        r'^##\s+'
    )
    
    # Application
    parsed.application = extract_section_content(
        content,
        r'^##\s+Application in Machine Learning|^##\s+Применение в Machine Learning',
        r'^##\s+'
    )
    parsed.application = extract_list_items(parsed.application)
    
    # Step-by-Step Scenario
    parsed.step_by_step = extract_section_content(
        content,
        r'^##\s+Step-by-Step Scenario|^##\s+Пример сценария по шагам',
        r'^##\s+'
    )
    
    # Self-Check Questions
    self_check_section = extract_section_content(
        content,
        r'^##\s+Self-Check Questions|^##\s+Вопросы для самопроверки',
        r'^##\s+'
    )
    
    # Extract Basic Level
    basic_match = re.search(r'^###\s+Basic Level|^###\s+Базовый уровень', 
                           self_check_section, re.MULTILINE | re.IGNORECASE)
    if basic_match:
        intermediate_match = re.search(r'^###\s+Intermediate Level|^###\s+Средний уровень',
                                       self_check_section[basic_match.end():], re.MULTILINE | re.IGNORECASE)
        end_pos = basic_match.end() + (intermediate_match.start() if intermediate_match else len(self_check_section))
        parsed.self_check_basic = self_check_section[basic_match.end():end_pos].strip()
        parsed.self_check_basic = extract_list_items(parsed.self_check_basic)
    
    # Extract Intermediate Level
    intermediate_match = re.search(r'^###\s+Intermediate Level|^###\s+Средний уровень',
                                  self_check_section, re.MULTILINE | re.IGNORECASE)
    if intermediate_match:
        advanced_match = re.search(r'^###\s+Advanced Level|^###\s+Продвинутый уровень',
                                  self_check_section[intermediate_match.end():], re.MULTILINE | re.IGNORECASE)
        end_pos = intermediate_match.end() + (advanced_match.start() if advanced_match else len(self_check_section))
        parsed.self_check_intermediate = self_check_section[intermediate_match.end():end_pos].strip()
        parsed.self_check_intermediate = extract_list_items(parsed.self_check_intermediate)
    
    # Extract Advanced Level
    advanced_match = re.search(r'^###\s+Advanced Level|^###\s+Продвинутый уровень',
                               self_check_section, re.MULTILINE | re.IGNORECASE)
    if advanced_match:
        parsed.self_check_advanced = self_check_section[advanced_match.end():].strip()
        parsed.self_check_advanced = extract_list_items(parsed.self_check_advanced)
    
    # Practical Tasks
    practical_section = extract_section_content(
        content,
        r'^##\s+Practical Tasks|^##\s+Практические задания',
        r'^##\s+'
    )
    
    # Extract Level 1 — Basic
    level1_match = re.search(r'^###\s+Level\s+1\s*—\s*Basic|^###\s+Уровень\s+1\s*—\s*базовый',
                            practical_section, re.MULTILINE | re.IGNORECASE)
    if level1_match:
        level2_match = re.search(r'^###\s+Level\s+2|^###\s+Уровень\s+2',
                                practical_section[level1_match.end():], re.MULTILINE | re.IGNORECASE)
        end_pos = level1_match.end() + (level2_match.start() if level2_match else len(practical_section))
        parsed.practical_tasks_basic = practical_section[level1_match.end():end_pos].strip()
    
    # Extract Level 2 — Applied
    level2_match = re.search(r'^###\s+Level\s+2\s*—\s*Applied|^###\s+Уровень\s+2\s*—\s*прикладной',
                             practical_section, re.MULTILINE | re.IGNORECASE)
    if level2_match:
        level3_match = re.search(r'^###\s+Level\s+3|^###\s+Уровень\s+3',
                                practical_section[level2_match.end():], re.MULTILINE | re.IGNORECASE)
        end_pos = level2_match.end() + (level3_match.start() if level3_match else len(practical_section))
        parsed.practical_tasks_applied = practical_section[level2_match.end():end_pos].strip()
    
    # Extract Level 3 — Research
    level3_match = re.search(r'^###\s+Level\s+3\s*—\s*Research|^###\s+Уровень\s+3\s*—\s*исследовательский',
                            practical_section, re.MULTILINE | re.IGNORECASE)
    if level3_match:
        parsed.practical_tasks_research = practical_section[level3_match.end():].strip()
    
    # Ethical Reasoning
    parsed.ethical_reasoning = extract_section_content(
        content,
        r'^##\s+Ethical Reasoning|^##\s+Этическое рассуждение',
        r'^##\s+'
    )
    
    return parsed


def parse_markdown_file(markdown_path: Path) -> Optional[ParsedMarkdown]:
    """
    Parse a markdown file, automatically detecting if it's school or university level.
    
    Args:
        markdown_path: Path to markdown file (school.en.md, school.ru.md, univer.en.md, univer.ru.md)
    
    Returns:
        ParsedMarkdown object or None if parsing fails
    """
    filename = markdown_path.name.lower()
    
    if filename.startswith('school.'):
        return parse_school_markdown(markdown_path)
    elif filename.startswith('univer.'):
        return parse_university_markdown(markdown_path)
    else:
        # Try to detect by content
        try:
            content = markdown_path.read_text(encoding='utf-8')
            if 'Simple Explanation' in content or 'Простое объяснение' in content:
                return parse_school_markdown(markdown_path)
            elif 'Algorithm Definition' in content or 'Определение алгоритма' in content:
                return parse_university_markdown(markdown_path)
        except Exception:
            pass
    
    return None

