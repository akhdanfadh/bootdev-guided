import re
from enum import Enum

from .htmlnode import HTMLNode, ParentNode
from .markdown_inline import text_to_html_nodes
from .textnode import TextNode, TextType, text_node_to_html_node


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
    # Split by double newlines (with optional whitespace) to get the blocks
    blocks = re.split(r"\n\s*\n+", text)
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
    # --- BOOTDEV requirement
    # No escaping HTML
    elif all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    # --- BOOTDEV requirement
    elif all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    elif all(line.startswith(f"{i + 1}. ") for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def block_to_html_nodes(block: str) -> list[HTMLNode]:
    html_nodes = []
    match block_to_block_type(block):
        case BlockType.HEADING:
            lines = block.split("\n")

            # Handle the heading line (first line)
            heading_line = lines.pop(0)
            match = re.match(r"^(#{1,6})\s+(.*)", heading_line)
            hash_count = len(match.group(1))
            head_html_nodes = text_to_html_nodes(match.group(2))
            html_nodes.append(ParentNode(f"h{str(hash_count)}", head_html_nodes))

            # If there are lines after heading, they are paragraph block
            if lines:
                html_nodes.extend(block_paragraph_to_html_nodes("\n".join(lines)))
            return html_nodes

        case BlockType.CODE:
            # Remove the backticks
            backticks = re.match(r"^(`{3,})", block)
            backticks_count = len(backticks.group(1))
            content = block[backticks_count:-backticks_count].strip()
            # Convert to HTML node without any inline parsing
            content_node = text_node_to_html_node(TextNode(content, TextType.CODE))

            html_nodes.append(ParentNode("pre", [content_node]))
            return html_nodes

        case BlockType.QUOTE:
            # Combine all lines and make a paragraph block
            content = []
            for line in block.split("\n"):
                # Remove '>' every lines
                # --- BOOTDEV requirement
                # No escaping HTML
                signs = re.match(r"^(>+\s*)", line)
                # --- BOOTDEV requirement
                signs_char_len = len(signs.group(1))
                line = line[signs_char_len:]
                content.append(line)
            # --- BOOTDEV requirement
            # Generally the content of quote is under paragraph
            content_node = text_to_html_nodes(" ".join(content))
            # --- BOOTDEV requirement

            html_nodes.append(ParentNode("blockquote", content_node))
            return html_nodes

        case BlockType.UNORDERED_LIST:
            return block_list_to_html_nodes(block, False)

        case BlockType.ORDERED_LIST:
            return block_list_to_html_nodes(block, True)

        case BlockType.PARAGRAPH:
            return block_paragraph_to_html_nodes(block)


def block_list_to_html_nodes(block: str, ordered: bool) -> list[HTMLNode]:
    content_nodes = []
    pattern = r"^(\d+. )" if ordered else r"^(- )"
    for line in block.split("\n"):
        # Remove the pattern
        signs = re.match(pattern, line)
        line = line[len(signs.group(1)) :]
        # --- BOOTDEV requirement
        # Generally the content of list is under paragraph,
        content_node = text_to_html_nodes(line)
        content_nodes.append(ParentNode("li", content_node))
        # --- BOOTDEV requirement

    tag = "ol" if ordered else "ul"
    return [ParentNode(tag, content_nodes)]


def block_paragraph_to_html_nodes(block: str) -> list[HTMLNode]:
    # Block-wise, it is already stripped in markdown_to_blocks function
    # CommonMark 0.31.2 ex222: leading spaces or tabs are skipped
    lines = [line.lstrip() for line in block.split("\n")]
    content_nodes = []

    for line in lines:
        # CommonMark 0.31.2 ex226: hard line break
        line = re.sub(r"\s{2,}$", "<br />", line)
        content_nodes.extend(text_to_html_nodes(line))

    return [ParentNode("p", content_nodes)]
