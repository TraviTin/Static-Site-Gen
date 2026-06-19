import unittest

from htmlnode import HtmlNode
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_dif(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_default(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.LINK, None)
        self.assertIsNone(node.url)
        self.assertIsNone(node2.url)

    def test_types(self):
        node = TextNode("This is a text node", TextType.BOLD, "bootdev.com")
        self.assertTrue(isinstance(node, TextNode))

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

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_bold(self):
        node = TextNode("This is a BOLD TEXT node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a BOLD TEXT node")

    def test_text_link(self):
        node = TextNode("google", TextType.LINK, "google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "google")
        self.assertEqual(html_node.props, {"href":"google.com"})

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )



if __name__ == "__main__":
    unittest.main()