import unittest

from src.markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
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


class TestSplitNodesImage(unittest.TestCase):
    def test_no_images(self):
        node = TextNode("This is just text.", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [TextNode("This is just text.", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_single_image(self):
        node = TextNode("Here is an image ![alt](url).", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("Here is an image ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "url"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_images(self):
        node = TextNode("A ![one](url1) and ![two](url2) test.", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("A ", TextType.TEXT),
            TextNode("one", TextType.IMAGE, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.IMAGE, "url2"),
            TextNode(" test.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_image_at_start(self):
        node = TextNode("![alt](url) at the start.", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("alt", TextType.IMAGE, "url"),
            TextNode(" at the start.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_image_at_end(self):
        node = TextNode("At the end ![alt](url)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("At the end ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "url"),
        ]
        self.assertEqual(result, expected)

    def test_image_only(self):
        node = TextNode("![alt](url)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [TextNode("alt", TextType.IMAGE, "url")]
        self.assertEqual(result, expected)

    def test_image_with_empty_alt(self):
        node = TextNode("![](url)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [TextNode("", TextType.IMAGE, "url")]
        self.assertEqual(result, expected)

    def test_image_with_empty_url(self):
        node = TextNode("![alt]()", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [TextNode("alt", TextType.IMAGE, "")]
        self.assertEqual(result, expected)

    def test_image_with_empty_alt_and_url(self):
        node = TextNode("![]()", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [TextNode("", TextType.IMAGE, "")]
        self.assertEqual(result, expected)

    def test_multiple_nodes(self):
        nodes = [
            TextNode("First ![a](1)", TextType.TEXT),
            TextNode("Second ![b](2)", TextType.TEXT),
        ]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("a", TextType.IMAGE, "1"),
            TextNode("Second ", TextType.TEXT),
            TextNode("b", TextType.IMAGE, "2"),
        ]
        self.assertEqual(result, expected)

    def test_link_and_image(self):
        node = TextNode(
            "Here is a [link](url) and an image ![alt](imgurl).", TextType.TEXT
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("Here is a [link](url) and an image ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "imgurl"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)


class TestSplitNodesLink(unittest.TestCase):
    def test_no_links(self):
        node = TextNode("This is just text.", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [TextNode("This is just text.", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_single_link(self):
        node = TextNode("Here is a [link](url).", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("Here is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_links(self):
        node = TextNode("A [one](url1) and [two](url2) test.", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("A ", TextType.TEXT),
            TextNode("one", TextType.LINK, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.LINK, "url2"),
            TextNode(" test.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_link_at_start(self):
        node = TextNode("[start](url) of the line.", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("start", TextType.LINK, "url"),
            TextNode(" of the line.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_link_at_end(self):
        node = TextNode("At the end [end](url)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("At the end ", TextType.TEXT),
            TextNode("end", TextType.LINK, "url"),
        ]
        self.assertEqual(result, expected)

    def test_link_only(self):
        node = TextNode("[only](url)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [TextNode("only", TextType.LINK, "url")]
        self.assertEqual(result, expected)

    def test_link_with_empty_text(self):
        node = TextNode("[](url)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [TextNode("", TextType.LINK, "url")]
        self.assertEqual(result, expected)

    def test_link_with_empty_url(self):
        node = TextNode("[text]()", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [TextNode("text", TextType.LINK, "")]
        self.assertEqual(result, expected)

    def test_link_with_empty_text_and_url(self):
        node = TextNode("[]()", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [TextNode("", TextType.LINK, "")]
        self.assertEqual(result, expected)

    def test_multiple_nodes(self):
        nodes = [
            TextNode("First [a](1)", TextType.TEXT),
            TextNode("Second [b](2)", TextType.TEXT),
        ]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("a", TextType.LINK, "1"),
            TextNode("Second ", TextType.TEXT),
            TextNode("b", TextType.LINK, "2"),
        ]
        self.assertEqual(result, expected)

    def test_link_and_image(self):
        node = TextNode("Here is an ![img](imgurl) and a [link](url).", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("Here is an ![img](imgurl) and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
