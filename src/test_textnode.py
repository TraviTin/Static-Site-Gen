import unittest
from cgitb import text

from htmlnode import HtmlNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

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


    def test_split_bold(self):
        node = [TextNode("This is **an** image", TextType.TEXT,)]
        split_node = split_nodes_delimiter(old_nodes=node, delimiter="**", text_type=TextType.BOLD)
        self.assertEqual(split_node,[
    TextNode("This is ", TextType.TEXT),
    TextNode("an", TextType.BOLD),
    TextNode(" image", TextType.TEXT),
])

    def test_split_italice(self):
        node = [TextNode("This is *an* image", TextType.TEXT,)]
        split_node = split_nodes_delimiter(old_nodes=node, delimiter="*", text_type=TextType.ITALIC)
        self.assertEqual(split_node,[
    TextNode("This is ", TextType.TEXT),
    TextNode("an", TextType.ITALIC),
    TextNode(" image", TextType.TEXT),
])

    def test_split_plain_text(self):
        node = [TextNode("This is an image", TextType.TEXT,)]
        split_node = split_nodes_delimiter(old_nodes=node, delimiter="**", text_type=TextType.BOLD)
        self.assertEqual(split_node,[
    TextNode("This is an image", TextType.TEXT),
])

    def test_extract_image(self):
        text =  "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        test1 = extract_markdown_images(text)
        self.assertEqual(test1, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])


    def test_extract_link(self):
        test = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        test1 = extract_markdown_links(test)
        self.assertEqual(test1, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_images_empty(self):
        node = TextNode("This does not have a link", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This does not have a link", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_empty(self):
        node = TextNode("This does not have a link", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This does not have a link", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_split_images_trailing_text(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and just with text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" and just with text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )


    def test_text_to_text_nodes_empty(self):
        text = "this is just text!"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [TextNode("this is just text!", TextType.TEXT)
        ],
        new_nodes,
        )

    def test_text_to_text_nodes_just_link(self):
        text = "this is just text! with a link! [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [TextNode("this is just text! with a link! ", TextType.TEXT),
             TextNode("link", TextType.LINK, "https://boot.dev"),
             ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()