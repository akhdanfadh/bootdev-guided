import unittest

from src.markdown import (
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_blocks,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
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


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_all_features(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_plain_text(self):
        text = "Just a simple sentence."
        result = text_to_textnodes(text)
        expected = [TextNode("Just a simple sentence.", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_mixed_bold_italic(self):
        text = "This is **bold** and *italic* and __also bold__ and _also italic_."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("also bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("also italic", TextType.ITALIC),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_single_block(self):
        text = "This is a single block."
        self.assertEqual(markdown_to_blocks(text), ["This is a single block."])

    def test_multiple_blocks(self):
        text = "Block one.\n\nBlock two.\n\nBlock three."
        self.assertEqual(
            markdown_to_blocks(text), ["Block one.", "Block two.", "Block three."]
        )

    def test_blocks_with_extra_newlines(self):
        text = "Block one.\n\n\nBlock two.\n\n\n\nBlock three."
        self.assertEqual(
            markdown_to_blocks(text), ["Block one.", "Block two.", "Block three."]
        )

    def test_blocks_with_leading_and_trailing_newlines(self):
        text = "\n\nBlock one.\n\nBlock two.\n\n\n"
        self.assertEqual(markdown_to_blocks(text), ["Block one.", "Block two."])

    def test_blocks_with_whitespace_newlines(self):
        text = "Block one.\n   \nBlock two.\n\t\nBlock three."
        self.assertEqual(
            markdown_to_blocks(text), ["Block one.", "Block two.", "Block three."]
        )

    def test_markdown_to_blocks_complex(self):
        text = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        self.assertEqual(
            markdown_to_blocks(text),
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_only_whitespace(self):
        text = "   \n  \n\t\n"
        self.assertEqual(markdown_to_blocks(text), [])

    def test_block_with_only_special_characters(self):
        text = "---\n\n***\n\nBlock"
        self.assertEqual(markdown_to_blocks(text), ["---", "***", "Block"])

    def test_windows_line_endings(self):
        text = "Block one.\r\n\r\nBlock two.\r\n\r\nBlock three."
        self.assertEqual(
            markdown_to_blocks(text),
            ["Block one.", "Block two.", "Block three."],
        )


if __name__ == "__main__":
    unittest.main()
