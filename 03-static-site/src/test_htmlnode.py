import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()
