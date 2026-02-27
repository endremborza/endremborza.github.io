import json
import subprocess
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
import re
from html.parser import HTMLParser


@dataclass
class FileDiff:
    filepath: str
    status: str  # 'modified', 'new', 'deleted'
    details: str


class HTMLElement:
    """Simple representation of parsed HTML structure."""

    def __init__(self, tag: str, text: str = "", attrs: dict = None):
        self.tag = tag
        self.text = text
        self.attrs = attrs or {}
        self.children: list[HTMLElement] = []

    def __repr__(self):
        return f"<{self.tag}>{self.text[:30]}</{self.tag}>"


class SimpleHTMLParser(HTMLParser):
    """Parse HTML into a simple tree structure."""

    def __init__(self):
        super().__init__()
        self.root = HTMLElement("root")
        self.current = self.root
        self.text_buffer = ""

    def handle_starttag(self, tag, attrs):
        if self.text_buffer.strip():
            elem = HTMLElement("text", self.text_buffer.strip())
            self.current.children.append(elem)
            self.text_buffer = ""

        elem = HTMLElement(tag, attrs=dict(attrs))
        self.current.children.append(elem)
        self.current = elem

    def handle_endtag(self, tag):
        if self.text_buffer.strip():
            elem = HTMLElement("text", self.text_buffer.strip())
            self.current.children.append(elem)
            self.text_buffer = ""

        # Navigate back to parent (simple approach, assumes well-formed HTML)
        if self.current.tag == tag:
            self.current = self.root  # Simplified: go back to root

    def handle_data(self, data):
        self.text_buffer += data

    def get_tree(self):
        if self.text_buffer.strip():
            self.current.children.append(HTMLElement("text", self.text_buffer.strip()))
        return self.root


def parse_html_body(html_str: str) -> list[dict]:
    """Parse HTML body into a list of element descriptions."""
    parser = SimpleHTMLParser()
    parser.feed(html_str)
    tree = parser.get_tree()

    elements = []
    for child in tree.children:
        elem_desc = {"tag": child.tag}
        if child.text:
            elem_desc["text"] = child.text
        if child.attrs:
            elem_desc["attrs"] = child.attrs
        elements.append(elem_desc)

    return elements


def extract_html_text(html_str: str) -> str:
    """Extract plain text from HTML."""
    parser = SimpleHTMLParser()
    parser.feed(html_str)
    tree = parser.get_tree()

    def extract_text(elem):
        texts = []
        if elem.tag == "text":
            texts.append(elem.text)
        for child in elem.children:
            texts.extend(extract_text(child))
        return texts

    return " ".join(extract_text(tree)).strip()


def normalize_text(text: str) -> str:
    """Normalize whitespace in text for comparison."""
    return " ".join(text.split())


def compare_html_bodies(old_html: str, new_html: str) -> str:
    """Compare two HTML bodies semantically."""
    # Normalize whitespace in HTML itself
    old_html_norm = re.sub(r"\s+", " ", old_html).strip()
    new_html_norm = re.sub(r"\s+", " ", new_html).strip()

    if old_html_norm == new_html_norm:
        return "no changes"

    old_text = extract_html_text(old_html)
    new_text = extract_html_text(new_html)

    old_text_norm = normalize_text(old_text)
    new_text_norm = normalize_text(new_text)

    changes = []

    # Compare text content (normalized)
    if old_text_norm != new_text_norm:
        old_words = len(old_text_norm.split())
        new_words = len(new_text_norm.split())

        if old_words != new_words:
            changes.append(f"text: {old_words} → {new_words} words")
        else:
            changes.append("text: content changed (same word count)")

        # Find what was removed/added (only if word count differs)
        if old_words != new_words:
            old_sentences = [s.strip() for s in old_text_norm.split(".") if s.strip()]
            new_sentences = [s.strip() for s in new_text_norm.split(".") if s.strip()]

            removed_sents = [s for s in old_sentences if s not in new_text_norm]
            added_sents = [s for s in new_sentences if s not in old_text_norm]

            if removed_sents and len(removed_sents) <= 2:
                for sent in removed_sents:
                    preview = sent[:55] + ("..." if len(sent) > 55 else "")
                    changes.append(f'  - removed: "{preview}"')

            if added_sents and len(added_sents) <= 2:
                for sent in added_sents:
                    preview = sent[:55] + ("..." if len(sent) > 55 else "")
                    changes.append(f'  - added: "{preview}"')

    # Compare structure (number of tags)
    old_tags = re.findall(r"<[^/>]+>", old_html)
    new_tags = re.findall(r"<[^/>]+>", new_html)

    if len(old_tags) != len(new_tags):
        changes.append(f"structure: {len(old_tags)} → {len(new_tags)} tags")

    # Check for link changes
    old_links = re.findall(r'href=["\']([^"\']+)["\']', old_html)
    new_links = re.findall(r'href=["\']([^"\']+)["\']', new_html)

    if sorted(old_links) != sorted(new_links):
        added_links = [l for l in new_links if l not in old_links]
        removed_links = [l for l in old_links if l not in new_links]
        if removed_links:
            changes.append(f"removed links: {removed_links}")
        if added_links:
            changes.append(f"added links: {added_links}")

    if not changes:
        return "no meaningful changes (formatting only)"

    return "; ".join(changes)


def get_git_file_content(filepath: str, ref: str = "HEAD") -> Optional[str]:
    """Get file content from git at specified ref."""
    try:
        result = subprocess.run(
            ["git", "show", f"{ref}:{filepath}"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )
        return result.stdout if result.returncode == 0 else None
    except Exception as e:
        print(f"Error fetching {filepath} from git: {e}", file=sys.stderr)
        return None


def read_file(filepath: Path) -> Optional[str]:
    """Read file from filesystem."""
    try:
        return filepath.read_text()
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
        return None


def compare_json_trees(old: list[dict], new: list[dict]) -> str:
    """Compare two JSON tree structures logically, with HTML body parsing."""
    old_by_id = {node["id"]: node for node in old}
    new_by_id = {node["id"]: node for node in new}

    changes = []

    # Find added and modified nodes
    for node_id, new_node in new_by_id.items():
        if node_id not in old_by_id:
            changes.append(
                f"- **Added node**: `{node_id}` - {new_node.get('title', 'untitled')}"
            )
        else:
            old_node = old_by_id[node_id]
            node_changes = []

            if old_node.get("title") != new_node.get("title"):
                node_changes.append(
                    f"title: `{old_node.get('title')}` → `{new_node.get('title')}`"
                )

            if old_node.get("body") != new_node.get("body"):
                body_changes = compare_html_bodies(
                    old_node.get("body", ""), new_node.get("body", "")
                )
                # Only include body changes if they're meaningful (not just formatting)
                if not body_changes.startswith("no"):
                    node_changes.append(f"body: {body_changes}")

            old_children = set(old_node.get("children", []))
            new_children = set(new_node.get("children", []))
            if old_children != new_children:
                added = new_children - old_children
                removed = old_children - new_children
                if added:
                    node_changes.append(f"children +{list(added)}")
                if removed:
                    node_changes.append(f"children -{list(removed)}")

            if node_changes:
                changes.append(
                    f"- **Modified node**: `{node_id}`\n  - "
                    + "\n  - ".join(node_changes)
                )

    # Find deleted nodes
    for node_id in old_by_id:
        if node_id not in new_by_id:
            changes.append(
                f"- **Deleted node**: `{node_id}` - {old_by_id[node_id].get('title', 'untitled')}"
            )

    if not changes:
        return "No changes detected."

    return "\n".join(changes)


def parse_latex_sections(content: str) -> dict[str, str]:
    """Extract LaTeX section content."""
    sections = {}
    # Match \section{name} ... \section{next} or end of file
    pattern = r"\\section\{([^}]+)\}(.*?)(?=\\section\{|\\end\{document\})"
    matches = re.finditer(pattern, content, re.DOTALL)

    for match in matches:
        section_name = match.group(1)
        section_content = match.group(2).strip()
        sections[section_name] = section_content

    return sections


def compare_latex_files(old: str, new: str) -> str:
    """Compare LaTeX CV files by sections."""
    old_sections = parse_latex_sections(old)
    new_sections = parse_latex_sections(new)

    changes = []

    all_sections = set(old_sections.keys()) | set(new_sections.keys())

    for section in sorted(all_sections):
        old_content = old_sections.get(section, "")
        new_content = new_sections.get(section, "")

        if old_content == new_content:
            continue

        if section not in old_sections:
            changes.append(f"- **New section**: `{section}`")
        elif section not in new_sections:
            changes.append(f"- **Removed section**: `{section}`")
        else:
            # Extract entries (roughly)
            old_entries = re.findall(r"\\entry\{[^}]+\}\{[^}]+\}", old_content)
            new_entries = re.findall(r"\\entry\{[^}]+\}\{[^}]+\}", new_content)

            if len(old_entries) != len(new_entries):
                changes.append(
                    f"- **Modified section**: `{section}` - {len(old_entries)} → {len(new_entries)} entries"
                )
            elif old_content != new_content:
                changes.append(f"- **Modified section**: `{section}` - content updated")

    if not changes:
        return "No changes detected."

    return "\n".join(changes)


def main():
    root = Path(__file__).parent.parent

    files_to_check = [
        ("src/lib/data/tree-data.json", "json"),
        ("static/cv/src/cv.tex", "latex"),
    ]

    report_lines = ["# Generated Diffs Report\n"]

    for filepath_str, file_type in files_to_check:
        filepath = root / filepath_str
        print(f"\n📊 Comparing {filepath_str}...")

        current_content = read_file(filepath)
        previous_content = get_git_file_content(filepath_str)

        if current_content is None:
            report_lines.append(
                f"## {filepath_str}\n\n**Error**: Could not read current file.\n"
            )
            continue

        if previous_content is None:
            report_lines.append(
                f"## {filepath_str}\n\n**Status**: New file (not in previous commit).\n"
            )
            continue

        report_lines.append(f"## {filepath_str}\n")

        try:
            if file_type == "json":
                old_data = json.loads(previous_content)
                new_data = json.loads(current_content)
                diff_summary = compare_json_trees(old_data, new_data)
            elif file_type == "latex":
                diff_summary = compare_latex_files(previous_content, current_content)
            else:
                diff_summary = "Unknown file type"

            report_lines.append(f"\n{diff_summary}\n")
            print(f"✓ {filepath_str} checked")

        except Exception as e:
            report_lines.append(f"\n**Error parsing**: {e}\n")
            print(f"✗ Error: {e}", file=sys.stderr)

    # Output
    report = "\n".join(report_lines)
    print("\n" + "=" * 60)
    print(report)
    print("=" * 60)

    # Save to file
    output_file = root / "last-diffs.md"
    output_file.write_text(report)
    print(f"\n✓ Report saved to {output_file}")


if __name__ == "__main__":
    main()
