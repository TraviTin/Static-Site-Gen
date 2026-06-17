import unittest

from htmlnode import HtmlNode
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_HTML_props(self):
        node = HtmlNode(None, None, None, { "href": "https://www.google.com","target": "_blank",})
        self.assertTrue(isinstance(node, HtmlNode))

    def test_html_none_default(self):
        node = HtmlNode()
        self.assertIsNone(node.tag, node.value)
        self.assertIsNone(node.props)
        self.assertIsNone(node.children)

    def test_html_eq(self):
        node = HtmlNode("<p>","hello", [], {})
        node2 = HtmlNode("<p>","hello", [], {})
        self.assertEqual(node.tag, node2.tag)

if __name__ == "__main__":
    unittest.main()