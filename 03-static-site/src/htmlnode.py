class HTMLNode:
    """
    A class representing a "node" in an HTML document tree.

    For example, a `<p>` tag and its contents, or an `<a>` tag and its contents. It can be block level or inline, and is designed to only output HTML.

    Args:
        tag: The HTML tag name, e.g. "p", "a", "div", etc.
        value: The value of the HTML tag, e.g. text inside a paragraph tag.
        children: A list of `HTMLNode` objects representing the children of this node.
        props: A dictionary of the tag's attributes, e.g. `<a>` tag might have `{"href": "https://www.google.com"}`.
    """

    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: list["HTMLNode"] = None,
        props: dict = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        return f"HTMLNode('{self.tag}', '{self.value}', {self.children}, {self.props})"

    def to_html(self) -> str:
        raise NotImplementedError("Subclasses must implement this method")

    def props_to_html(self) -> str:
        """
        Convert the props dictionary to a string of HTML attributes.

        The leading space is intentional, as it is used to separate the attributes from the tag name in the output HTML.
        """
        return (
            " " + " ".join(f"{k}={v}" for k, v in self.props.items())
            if self.props is not None
            else ""
        )


class LeafNode(HTMLNode):
    """
    Represents a leaf node in the HTML document tree, i.e., a node that cannot have children.

    Typically used for tags that contain only text or a value and do not have nested HTML elements. For example, a <span> or <a> tag with only text inside.

    Args:
        tag: The HTML tag name, e.g. "span", "a", etc.
        value: The text or value inside the tag. Must not be None, empty string is allowed.
        props: Optional dictionary of HTML attributes for the tag.
    """

    def __init__(self, tag: str, value: str, props: dict = None):
        super().__init__(tag, value, props=props)

        assert self.children is None
        if self.value is None:
            raise ValueError("LeafNode must have a value")

    def to_html(self) -> str:
        return (
            f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
            if self.tag is not None
            else self.value
        )


class ParentNode(HTMLNode):
    """
    Represents a parent node in the HTML document tree, i.e., a node that can have one or more child nodes.

    Typically used for tags that contain other HTML elements, such as <div>, <ul>, <ol>, <p>, etc. The ParentNode does not have a value of its own, only children.

    Args:
        tag: The HTML tag name, e.g. "div", "ul", "ol", etc. Must not be None or empty string.
        children: A list of `HTMLNode` objects representing the children of this node. Must not be None or empty list.
        props: Optional dictionary of HTML attributes for the tag.
    """

    def __init__(self, tag: str, children: list["HTMLNode"], props: dict = None):
        super().__init__(tag=tag, children=children, props=props)

        assert self.value is None
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have children")

    def to_html(self) -> str:
        result = ""
        for child in self.children:
            result += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{result}</{self.tag}>"
