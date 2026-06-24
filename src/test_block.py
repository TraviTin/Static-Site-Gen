import unittest
from block_markdown import *
from markdown_to_html import *

class TestTextNode(unittest.TestCase):
    def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )


    def test_markdown_to_blocks_two(self):
            md = """
This is **bolded** paragraph
This is another paragraph with _italic_ text and `code` here

This is the same paragraph on a new line
    """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                ["This is **bolded** paragraph\nThis is another paragraph with _italic_ text and `code` here", "This is the same paragraph on a new line"
                 ],
            blocks
            )

    def test_markdown_to_heading(self):
        block = "#### This is a h4 heading"
        answer = block_to_block_type(block)
        self.assertEqual(
            BlockType.HEADING,
            answer,
        )

    def test_markdown_to_code(self):
        block = ("```\n this is some code\n```")
        answer = block_to_block_type(block)
        self.assertEqual(
            BlockType.CODE,
            answer,
        )

    def test_markdown_to_quote(self):
        block = ">this is a quote\n>who said this <"
        answer = block_to_block_type(block)
        self.assertEqual(
            BlockType.QUOTE,
            answer,
        )
    def test_markdown_to_unordered_list(self):
        block = "- unordered\n- list\n- with items"
        answer = block_to_block_type(block)
        self.assertEqual(
            BlockType.UNORDERED_LIST,
            answer,
        )
    def test_markdown_to_ordered(self):
        block = "1. first\n2. second\n3. third"
        answer = block_to_block_type(block)
        self.assertEqual(
            BlockType.ORDERED_LIST,
            answer,
        )
    def test_markdown_to_ordered_fail(self):
        block = "1. first\n2. second\n5. third"
        answer = block_to_block_type(block)
        self.assertEqual(
            BlockType.PARAGRAPH,
            answer,
        )
    def test_markdown_to_para(self):
        block = "this is just a paragraph"
        answer = block_to_block_type(block)
        self.assertEqual(
            BlockType.PARAGRAPH,
            answer,
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
    "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_ordered_list(self):
        md = """
1. first
2. second
3. third
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first</li><li>second</li><li>third</li></ol></div>",
        )

if __name__ == "__main__":
    unittest.main()