import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode
from src.markdown_block import (
    BlockType,
    block_to_block_type,
    block_to_html_nodes,
    markdown_to_blocks,
    preprocess_markdown,
)


class TestPreprocessMarkdown(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_preprocess_all(self):
        md = """\n\t
Should be stripped\r\n and all Unix newline
this <inside chars> & **bold** "text" 'text_single' `code` _wow_\t
"""
        expected = """Should be stripped\n and all Unix newline
this &lt;inside chars&gt; &amp; **bold** &quot;text&quot; &#x27;text_single&#x27; `code` _wow_"""
        self.assertEqual(preprocess_markdown(md), expected)


class TestMarkdownToBlocks(unittest.TestCase):
    def process(self, text: str) -> str:
        return markdown_to_blocks(preprocess_markdown(text))

    def test_empty_string(self):
        self.assertEqual(self.process(""), [])

    def test_only_whitespace(self):
        md = "   \n  \n\t\n"
        self.assertEqual(self.process(md), [])

    def test_single_block(self):
        md = "This is a single block."
        self.assertEqual(self.process(md), ["This is a single block."])

    def test_multiple_blocks_complex(self):
        md = "\nBlock one.\n   \nBlock two.\n\n\t\n\nBlock three.\n\n\n"
        self.assertEqual(self.process(md), ["Block one.", "Block two.", "Block three."])


class TestBlockToBlockType(unittest.TestCase):
    def process(self, text: str) -> list[BlockType]:
        blocks = markdown_to_blocks(preprocess_markdown(text))
        return [block_to_block_type(block) for block in blocks]

    # Heading tests
    def test_heading_correct(self):
        md = """
# simple heading

#### subheading

#    \t heading with whitespaces

# this heading
has paragraph under it
"""
        self.assertEqual(self.process(md), [BlockType.HEADING] * 4)

    def test_heading_incorrect(self):
        md = """
###This is actually paragraph

####### This has too many hashes

##1## incorrect hashes
"""
        self.assertEqual(self.process(md), [BlockType.PARAGRAPH] * 3)

    # Code block tests
    def test_code_correct(self):
        md = """
```print('inline code')```

`````right_backtick have at least the amount of left_backtick`````

```
proper code block
```

````
this too is proper code block
`````
"""
        self.assertEqual(self.process(md), [BlockType.CODE] * 4)

    def test_code_incorrect(self):
        md = """
``
not enough backticks
``

````right_backtick don't have the amount of left_backtick```

```
code with blank lines

like this is two blocks paragraph sadly
```
"""
        self.assertEqual(self.process(md), [BlockType.PARAGRAPH] * 4)

    # Quote block tests
    def test_quote_correct(self):
        md = """
> This is simple quote

>This also works

> Multiline
> quote 
>should works

>>>> Many signs also works
>!! even like this
"""
        self.assertEqual(self.process(md), [BlockType.QUOTE] * 4)

    def test_quote_incorrect(self):
        md = """
> if even one line
like this
> does not have sign
"""
        self.assertEqual(self.process(md), [BlockType.PARAGRAPH])

    # Unordered list block tests
    def test_unordered_correct(self):
        md = """
- This is simple list

- multiline
- should
- works
"""
        self.assertEqual(self.process(md), [BlockType.UNORDERED_LIST] * 2)

    def test_unordered_incorrect(self):
        md = """
-If no space, it is incorrect

- multiline should have space too
-so this breaks it

- nested line will not work
    - sadly
- huhu

- multiline all should have dashes with space too
so this is wrong

--- many dashes won't work okay?
"""
        self.assertEqual(self.process(md), [BlockType.PARAGRAPH] * 5)

    # Ordered list block tests
    def test_ordered_correct(self):
        md = """
1. one item is okay

1. even more items
2. is better
"""
        self.assertEqual(self.process(md), [BlockType.ORDERED_LIST] * 2)

    def test_ordered_incorrect(self):
        md = """
2. sadly it should start at 1

1. the number should continuous
3. so this breaks

1. Item 1
    This breaks it also sadly
2. so sad right?
"""
        self.assertEqual(self.process(md), [BlockType.PARAGRAPH] * 3)

    # Paragraph tests
    def test_paragraph_correct(self):
        md = """
this is a simple paragraph

and this too
shall pass
"""
        self.assertEqual(self.process(md), [BlockType.PARAGRAPH] * 2)


class TestBlockToHtmlNodes(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def process(self, text: str) -> list[HTMLNode]:
        blocks = markdown_to_blocks(preprocess_markdown(text))
        result = []
        for block in blocks:
            result.extend(block_to_html_nodes(block))
        return result

    def test_paragraph(self):
        md = """
#welcome to _markdown_ and here is some `inline code` and a [link](url)

this is multiline resulting in multiple LeafNode
but it will render as a oneline

now let's try hard break with these multiple spaces   
or these multiple tabs\t\t\t
and we will see in html that it will break
"""
        expected = [
            ParentNode(
                "p",
                [
                    LeafNode(None, "#welcome to ", None),
                    LeafNode("i", "markdown", None),
                    LeafNode(None, " and here is some ", None),
                    LeafNode("code", "inline code", None),
                    LeafNode(None, " and a ", None),
                    LeafNode("a", "link", {"href": "url"}),
                ],
            ),
            ParentNode(
                "p",
                [
                    LeafNode(
                        None,
                        "this is multiline resulting in multiple LeafNode",
                        None,
                    ),
                    LeafNode(
                        None,
                        "but it will render as a oneline",
                        None,
                    ),
                ],
            ),
            ParentNode(
                "p",
                [
                    LeafNode(
                        None,
                        "now let&#x27;s try hard break with these multiple spaces<br />",
                        None,
                    ),
                    LeafNode(
                        None,
                        "or these multiple tabs<br />",
                        None,
                    ),
                    LeafNode(
                        None,
                        "and we will see in html that it will break",
                        None,
                    ),
                ],
            ),
        ]
        self.assertEqual(repr(self.process(md)), repr(expected))

    def test_heading(self):
        md = """
# this heading have _formatting_!

##      i don't know but this have whitespaces\t\t

### someone forgot to put
\tnewline i guess

###\tlet's try **something** [complex](this-is-url)
```like this <code> I wonder what happen```
"""
        expected = [
            ParentNode(
                "h1",
                [
                    LeafNode(None, "this heading have ", None),
                    LeafNode("i", "formatting", None),
                    LeafNode(None, "!", None),
                ],
            ),
            ParentNode(
                "h2",
                [LeafNode(None, "i don&#x27;t know but this have whitespaces", None)],
            ),
            ParentNode("h3", [LeafNode(None, "someone forgot to put", None)]),
            ParentNode("p", [LeafNode(None, "newline i guess", None)]),
            ParentNode(
                "h3",
                [
                    LeafNode(None, "let&#x27;s try ", None),
                    LeafNode("b", "something", None),
                    LeafNode(None, " ", None),
                    LeafNode("a", "complex", {"href": "this-is-url"}),
                ],
            ),
            ParentNode(
                "p",
                [LeafNode("code", "like this &lt;code&gt; I wonder what happen", None)],
            ),
        ]
        self.assertEqual(repr(self.process(md)), repr(expected))

    def test_code(self):
        md = '''
```
def test_preprocess_all(self):
    md = """
Should be stripped\r\n and all Unix newline
this <inside chars> & **bold** "text" 'text_single' `code` _wow_\t
"""
    expected = """Should be stripped\n and all Unix newline
this &lt;inside chars&gt; &amp; **bold** &quot;text&quot; &#x27;text_single&#x27; `code` _wow_"""
    self.assertEqual(preprocess_markdown(md), expected)
```
'''
        expected = [
            ParentNode(
                "pre",
                [
                    LeafNode(
                        "code",
                        """def test_preprocess_all(self):
    md = &quot;&quot;&quot;
Should be stripped\n and all Unix newline
this &lt;inside chars&gt; &amp; **bold** &quot;text&quot; &#x27;text_single&#x27; `code` _wow_\t
&quot;&quot;&quot;
    expected = &quot;&quot;&quot;Should be stripped\n and all Unix newline
this &amp;lt;inside chars&amp;gt; &amp;amp; **bold** &amp;quot;text&amp;quot; &amp;#x27;text_single&amp;#x27; `code` _wow_&quot;&quot;&quot;
    self.assertEqual(preprocess_markdown(md), expected)""",
                        None,
                    )
                ],
            )
        ]
        self.assertEqual(repr(self.process(md)), repr(expected))


if __name__ == "__main__":
    unittest.main()
