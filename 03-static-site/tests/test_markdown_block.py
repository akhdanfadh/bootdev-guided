import unittest

from src.markdown_block import BlockType, block_to_block_type, markdown_to_blocks


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
# This is a heading

This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

```
This is a code block
```

> This is a quote

1. This is an ordered list
2. With items
"""
        self.assertEqual(
            markdown_to_blocks(text),
            [
                "# This is a heading",
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
                "```\nThis is a code block\n```",
                "> This is a quote",
                "1. This is an ordered list\n2. With items",
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


class TestBlockToBlockType(unittest.TestCase):
    # Heading tests
    def test_heading_single_hash(self):
        block = "# Heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_multiple_hashes(self):
        block = "###### Heading 6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_many_spaces(self):
        block = "#    Heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_tabs(self):
        block = "#\tHeading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_tabs_and_spaces(self):
        block = "#    \tHeading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_no_spaces(self):
        block = "###This is actually paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_too_many_hashes(self):
        block = "####### This is actually paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_incorrect_hashes(self):
        block = "##1## This is actually paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # Code block tests
    def test_code_block_simple(self):
        block = """```
code here
```"""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_inline(self):
        block = "```print('hi')```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_many_backticks(self):
        block = "````print('hi')````"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_incorrect_backticks(self):
        block = "````print('hi')```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # Quote block tests
    def test_quote_block_single(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_multiple(self):
        block = "> Line 1\n> Line 2\n> Line 3"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_multiple_but_incorrect(self):
        block = "> Line 1\n> Line 2\nLine 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_block_many_signs(self):
        block = ">>>> This is a quote\n>> haha"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    # Unordered list block tests
    def test_unordered_list_single(self):
        block = "- item 1"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_multiple(self):
        block = "- item 1\n- item 2\n- item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_but_incorrect(self):
        block = "- item 1\n- item 2\nitem 3\n- item 4"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_many_dashes_but_incorrect(self):
        block = "--- item 1\n--- item 2\nitem 3\n--- item 4"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # Ordered list block tests
    def test_ordered_list_single(self):
        block = "1. first"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_multiple(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_not_from_one(self):
        block = "2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # Paragraph tests
    def test_paragraph_simple(self):
        block = "This is a simple paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_with_newlines(self):
        block = "This is a paragraph\nwith a newline."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
