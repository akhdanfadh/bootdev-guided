import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestParentNode(unittest.TestCase):
    def test_parentnode_init(self):
        children = [LeafNode("span", "child")]
        props = {"class": "container"}
        node = ParentNode("div", children, props=props)
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)
        self.assertIsNone(node.value)

    def test_to_html_with_no_children_raises(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None)
        with self.assertRaises(ValueError):
            ParentNode("div", [])

    def test_to_html_with_no_tag_raises(self):
        child = LeafNode("span", "child")
        with self.assertRaises(ValueError):
            ParentNode(None, [child])
        with self.assertRaises(ValueError):
            ParentNode("", [child])

    def test_repr(self):
        children = [LeafNode("span", "child")]
        props = {"class": "container"}
        node = ParentNode("div", children, props=props)
        self.assertEqual(repr(node), f"HTMLNode('div', 'None', {children}, {props})")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("span", "child1")
        child2 = LeafNode("b", "child2")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent.to_html(), "<div><span>child1</span><b>child2</b></div>"
        )

    def test_to_html_deeply_nested(self):
        leaf = LeafNode("i", "deep")
        inner = ParentNode("span", [leaf])
        middle = ParentNode("section", [inner])
        outer = ParentNode("div", [middle])
        self.assertEqual(
            outer.to_html(), "<div><section><span><i>deep</i></span></section></div>"
        )

    def test_to_html_with_props(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child], props={"class": "container", "id": "main"})
        html = parent.to_html()
        self.assertTrue(html.startswith("<div "))
        self.assertIn("class=container", html)
        self.assertIn("id=main", html)
        self.assertIn("<span>child</span>", html)

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_nested_parentnodes_and_multiple_children(self):
        leaf1 = LeafNode("b", "one")
        leaf2 = LeafNode("i", "two")
        child = ParentNode("span", [leaf1, leaf2])
        parent = ParentNode("div", [child, LeafNode("u", "three")])
        self.assertEqual(
            parent.to_html(), "<div><span><b>one</b><i>two</i></span><u>three</u></div>"
        )


if __name__ == "__main__":
    unittest.main()
