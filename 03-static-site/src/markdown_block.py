import re
from enum import Enum

from .htmlnode import HTMLNode, ParentNode
from .markdown_inline import text_to_html_nodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(text: str) -> list[str]:
    """
    Convert a markdown text to a list of text blocks.
    """
    # Normalize line endings to Unix style
    text = text.replace("\r\n", "\n")
    # Split by double newlines (with optional whitespace) to get the blocks
    blocks = re.split(r"\n\s*\n+", text.strip())
    # Remove empty strings and strip whitespace from blocks
    return [block.strip() for block in blocks if block.strip()]


def block_to_block_type(block: str) -> BlockType:
    """
    Convert a markdown string block to a `BlockType`.

    Note that this function does not strictly follow the [CommonMark](https://spec.commonmark.org/) spec,
    but rather is a simplified version that is sufficient for our purposes.
    """
    lines = block.split("\n")
    if re.match(r"^#{1,6}\s+", block):
        return BlockType.HEADING
    elif (match := re.match(r"^(`{3,})", block)) and block.endswith(match.group(1)):
        return BlockType.CODE
    elif all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    elif all(line.startswith(f"{i + 1}. ") for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def block_to_html_nodes(block: str) -> list[HTMLNode]:
    lines = block.split("\n")
    html_nodes = []
    match block_to_block_type(block):
        case BlockType.HEADING:
            # Handle the heading line (first line)
            heading_line = lines.pop(0)
            match = re.match(r"^(#{1,6})\s+(.*)", heading_line)
            hash_count = len(match.group(1))
            head_html_nodes = text_to_html_nodes(match.group(2))

            # If there are lines after heading, treat them as inline text
            html_nodes.append(ParentNode(f"h{str(hash_count)}", head_html_nodes))
            for line in lines:
                html_nodes.extend(text_to_html_nodes(line))
            return html_nodes

        case BlockType.CODE:
            pass
        case BlockType.QUOTE:
            pass
        case BlockType.UNORDERED_LIST:
            pass
        case BlockType.ORDERED_LIST:
            pass
        case BlockType.PARAGRAPH:
            pass
