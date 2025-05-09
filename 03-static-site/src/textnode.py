from enum import Enum

from .htmlnode import HTMLNode, LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    """
    Represents an inline text element in Markdown, serving as an intermediate representation before converting to HTML.

    This class is used to model all types of inline text that can appear within a block of Markdown text, including:
    - Normal text
    - Bold text (e.g., **Bold text**)
    - Italic text (e.g., _Italic text_)
    - Code text (e.g., `Code text`)
    - Links (e.g., [anchor text](url))
    - Images (e.g., ![alt text](url))

    Block-level elements such as headings, paragraphs, and lists are not represented by this class.

    Attributes:
        text (str): The text content or alt text for images.
        text_type (TextType): The type of inline text (e.g., TEXT, BOLD, ITALIC, CODE, LINK, IMAGE).
        url (str, optional): The URL for links and images. Defaults to None.
    """

    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: "TextNode"):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode('{self.text}', {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    """
    Convert a TextNode to an HTMLNode.
    """
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case TextType.IMAGE:
            return LeafNode(
                tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
            )
        case _:
            raise ValueError(f"Unsupported text type: {text_node.text_type}")
