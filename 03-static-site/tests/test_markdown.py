import unittest

from src.markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
)
from src.textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_bold(self):
        node = TextNode(
            "This is text with a **bolded phrase** in the middle", TextType.TEXT
        )
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_italic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_no_delimiter(self):
        node = TextNode("No special formatting here", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [TextNode("No special formatting here", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_multiple_nodes(self):
        nodes = [
            TextNode("First `code`", TextType.TEXT),
            TextNode("Second **bold**", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        result = split_nodes_delimiter(result, "**", TextType.BOLD)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("Second ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_invalid_syntax_raises(self):
        node = TextNode("Unmatched **bold", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        text = "Here is an image ![alt text](http://example.com/image.png) in markdown."
        expected = [("alt text", "http://example.com/image.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_multiple_images(self):
        text = "![img1](url1) and ![img2](url2)"
        expected = [("img1", "url1"), ("img2", "url2")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_no_images(self):
        text = "No images here!"
        self.assertEqual(extract_markdown_images(text), [])

    def test_image_with_empty_alt(self):
        text = "![](url)"
        expected = [("", "url")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_with_empty_url(self):
        text = "![alt]()"
        expected = [("alt", "")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_with_empty_alt_and_url(self):
        text = "![]()"
        expected = [("", "")]
        self.assertEqual(extract_markdown_images(text), expected)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        text = "Here is a [link](http://example.com) in markdown."
        expected = [("link", "http://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_multiple_links(self):
        text = "[first](url1) and [second](url2)"
        expected = [("first", "url1"), ("second", "url2")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_no_links(self):
        text = "No links here!"
        self.assertEqual(extract_markdown_links(text), [])

    def test_link_and_image(self):
        text = "[link](url) and ![img](imgurl)"
        expected = [("link", "url")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_with_empty_text(self):
        text = "[](url)"
        expected = [("", "url")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_with_empty_url(self):
        text = "[text]()"
        expected = [("text", "")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_with_empty_text_and_url(self):
        text = "[]()"
        expected = [("", "")]
        self.assertEqual(extract_markdown_links(text), expected)


if __name__ == "__main__":
    unittest.main()
