import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_init_defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_init_with_values(self):
        children = [HTMLNode(tag="span", value="child")]
        props = {"href": "https://example.com", "class": "link"}
        node = HTMLNode(tag="a", value="Click here", children=children, props=props)
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Click here")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    def test_repr(self):
        node = HTMLNode(tag="p", value="Hello", children=None, props=None)
        self.assertEqual(repr(node), "HTMLNode('p', 'Hello', None, None)")

    def test_props_to_html_none(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_props(self):
        props = {"href": "https://example.com", "class": "link"}
        node = HTMLNode(props=props)
        # The order of dict items is not guaranteed before Python 3.7
        html = node.props_to_html()
        self.assertTrue(html.startswith(" "))
        self.assertIn("href=https://example.com", html)
        self.assertIn("class=link", html)

    def test_to_html_not_implemented(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()


class TestLeafNode(unittest.TestCase):
    def test_leafnode_init(self):
        node = LeafNode(tag="span", value="test", props={"class": "highlight"})
        self.assertEqual(node.tag, "span")
        self.assertEqual(node.value, "test")
        self.assertIsNone(node.children)
        self.assertEqual(node.props, {"class": "highlight"})

    def test_leafnode_requires_value(self):
        with self.assertRaises(ValueError):
            LeafNode(tag="span", value=None)

    def test_leafnode_to_html_with_tag(self):
        node = LeafNode(tag="b", value="bold", props={"style": "font-weight:bold"})
        html = node.to_html()
        self.assertTrue(html.startswith("<b"))
        self.assertIn(">bold</b>", html)
        self.assertIn("style=font-weight:bold", html)

    def test_leafnode_to_html_without_tag(self):
        node = LeafNode(tag=None, value="just text")
        self.assertEqual(node.to_html(), "just text")


if __name__ == "__main__":
    unittest.main()
