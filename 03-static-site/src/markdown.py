import html
import re

from .htmlnode import ParentNode
from .markdown_block import block_to_html_nodes, markdown_to_blocks


def preprocess_markdown(text: str) -> str:
    """
    Preprocess the markdown text.
    """
    # Normalize line endings to Unix style
    text = text.replace("\r\n", "\n")
    # --- BOOTDEV requirement
    # (Don't) Escape html characters
    # text = html.escape(text)
    # --- BOOTDEV requirement
    # Strip whitespaces in both sides
    text = text.strip()
    return text


def markdown_to_html(text: str) -> str:
    """
    Convert a markdown text to an HTML string under a div tag.
    """
    blocks = markdown_to_blocks(preprocess_markdown(text))
    html_nodes = []
    for block in blocks:
        html_nodes.extend(block_to_html_nodes(block))

    return ParentNode("div", html_nodes).to_html()


def extract_markdown_title(text: str) -> str:
    """
    Pull the first `h1` header from the markdown text.

    Note: The markdown file should strictly begin with this.
    HTML `<title>` element can only be one per document and does not support formatting.
    """
    text = preprocess_markdown(text)
    title_pattern = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)
    match = title_pattern.search(text)

    if match:
        return match.group(2).strip()
    else:
        raise Exception("No `h1` title found in the markdown text")


def generate_page(md_path: str, html_tmpl_path: str, html_path: str) -> None:
    """
    Create an HTML file from a markdown file with the given HTML template file.
    """
    print(f"Generating page from {md_path} to {html_path} using {html_tmpl_path}")
    with open(md_path, "r") as f:
        md = f.read()
        title = extract_markdown_title(md)
        content = markdown_to_html(md)

    with open(html_tmpl_path, "r") as f:
        tmpl = f.read()

    html = tmpl.replace("{{ Title }}", title).replace("{{ Content }}", content)
    with open(html_path, "w") as f:
        f.write(html)
