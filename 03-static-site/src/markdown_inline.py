# For simplicity's sake, currently we don't care about nested inline elements.
# For example, `This is an _italic and **bold** word_.` is not supported.

import re

from .htmlnode import HTMLNode
from .textnode import TextNode, TextType, text_node_to_html_node


def text_to_html_nodes(text: str) -> list[HTMLNode]:
    """
    Convert inline markdown string to a list of HTML nodes.
    """
    return list(map(text_node_to_html_node, text_to_text_nodes(text)))


def text_to_text_nodes(text: str) -> list[TextNode]:
    """
    Convert a string to a list of `TextNode` objects.
    """
    # Order of operations is important, we want to split for the longest delimiters first
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "__", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    """
    Split the nodes at the delimiter and return a new list of nodes,
    where any "text" type nodes in the input lists are (potentially)
    split into multiple nodes based on the syntax.

    For example, given the following input:
    ```md
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    ```
    `new_nodes` becomes:
    ```md
    [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),
    ]
    ```

    Args:
        old_nodes: A list of `TextNode` objects.
        delimiter: A string that delimits the new nodes.
        text_type: The type of the new nodes.

    Returns:
        A new list of `TextNode` objects.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            # we only attempt to split text nodes
            new_nodes.append(node)
            continue

        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise Exception("Invalid Markdown syntax: no matching delimiter found")

        for i in range(0, len(split_text)):
            if split_text[i] != "":
                new_nodes.append(
                    TextNode(split_text[i], TextType.TEXT if i % 2 == 0 else text_type)
                )

    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    """
    Extract all images from the given text and return a list of tuples,
    where each tuple contains the alt text and the URL.

    For example:
    ```
    text = "This is a [link](https://example.com) and an image ![alt text](https://example.com/image.png)"
    extract_markdown_images(text)
    # [("alt text", "https://example.com/image.png")]
    ```
    """
    # Pattern explanation:
    # ! - literal exclamation mark
    # [...] - alt text between square brackets, no nested brackets allowed
    # (...) - URL between parentheses, no nested parentheses allowed
    alt_text_pattern = r"\[([^\[\]]*)\]"  # captures text between []
    url_pattern = r"\(([^\(\)]*)\)"  # captures text between ()
    return re.findall(f"!{alt_text_pattern}{url_pattern}", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    (potentially) Split the nodes at the image and return a new list of nodes.

    For example:
    ```
    node = TextNode("This is a [link](https://example.com) and an image ![alt text](https://example.com/image.png) to be split.", TextType.TEXT)
    split_nodes_image([node])
    # [
    #     TextNode("This is a [link](https://example.com) and an image ", TextType.TEXT),
    #     TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"),
    #     TextNode(" to be split.", TextType.TEXT),
    # ]
    ```
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue

        text = node.text
        curr_index = 0

        for alt_text, url in images:
            image_pattern = f"![{alt_text}]({url})"
            image_index = text.find(image_pattern, curr_index)

            if image_index > curr_index:
                new_nodes.append(TextNode(text[curr_index:image_index], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

            curr_index = image_index + len(image_pattern)

        if curr_index < len(text):
            new_nodes.append(TextNode(text[curr_index:], TextType.TEXT))

    return new_nodes


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    """
    Extract all links from the given text and return a list of tuples,
    where each tuple contains the anchor text and the URL.

    For example:
    ```
    text = "This is a [link](https://example.com) and an image ![alt text](https://example.com/image.png)"
    extract_markdown_links(text)
    # [("link", "https://example.com")]
    ```
    """
    # Pattern explanation:
    # (?<!!) - negative lookbehind to ensure not preceded by ! (to exclude images)
    # [...] - anchor text between square brackets, no nested brackets allowed
    # (...) - URL between parentheses, no nested parentheses allowed
    anchor_text_pattern = r"\[([^\[\]]*)\]"  # captures text between []
    url_pattern = r"\(([^\(\)]*)\)"  # captures text between ()
    negative_lookbehind = r"(?<!!)"  # ensure not preceded by !
    return re.findall(f"{negative_lookbehind}{anchor_text_pattern}{url_pattern}", text)


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    (potentially) Split the nodes at the link and return a new list of nodes.

    For example:
    ```
    node = TextNode("This is a [link](https://example.com) and an image ![alt text](https://example.com/image.png) to be split.", TextType.TEXT)
    split_nodes_link([node])
    # [
    #     TextNode("This is a ", TextType.TEXT),
    #     TextNode("link", TextType.LINK, "https://example.com"),
    #     TextNode(" and an image ![alt text](https://example.com/image.png) to be split.", TextType.TEXT),
    # ]
    ```
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue

        text = node.text
        curr_index = 0

        for anchor_text, url in links:
            link_pattern = f"[{anchor_text}]({url})"
            link_index = text.find(link_pattern, curr_index)

            if link_index > curr_index:
                new_nodes.append(TextNode(text[curr_index:link_index], TextType.TEXT))
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))

            curr_index = link_index + len(link_pattern)

        if curr_index < len(text):
            new_nodes.append(TextNode(text[curr_index:], TextType.TEXT))

    return new_nodes
