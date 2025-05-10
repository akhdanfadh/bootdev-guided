import re
from enum import Enum


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
