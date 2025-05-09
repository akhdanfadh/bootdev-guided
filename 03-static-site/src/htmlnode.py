class HTMLNode:
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: list["HTMLNode"] = None,
        props: dict = None,
    ):
        """
        A class representing a "node" in an HTML document tree.

        For example, a `<p>` tag and its contents, or an `<a>` tag and its contents. It can be block level or inline, and is designed to only output HTML.

        Args:
            tag: The HTML tag name, e.g. "p", "a", "div", etc.
            value: The value of the HTML tag, e.g. text inside a paragraph tag.
            children: A list of `HTMLNode` objects representing the children of this node.
            props: A dictionary of the tag's attributes, e.g. `<a>` tag might have `{"href": "https://www.google.com"}`.
        """
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
