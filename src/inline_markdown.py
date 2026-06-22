from cgitb import text

from textnode import TextNode, TextType
import re



def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text:str) -> list[tuple]:
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    images_tuple = re.findall(pattern, text)
    return images_tuple


def extract_markdown_links(text:str) -> list[tuple]:
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    links_tuple =re.findall(pattern, text)
    return links_tuple

# noinspection DuplicatedCode
def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        images_tuple = extract_markdown_images(old_node.text)
        if len(images_tuple) == 0:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        current_text = old_node.text
        for image in images_tuple:
            image_alt = image[0]
            image_link = image[1]
            sections = current_text.split(f"![{image_alt}]({image_link})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, formatted section not closed")
            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            split_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            current_text = sections[1]
        if current_text != "":
            split_nodes.append(TextNode(current_text, TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes

# noinspection DuplicatedCode
def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        link_tuple = extract_markdown_links(old_node.text)
        if len(link_tuple) == 0:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        current_text = old_node.text
        for link in link_tuple:
            link_alt = link[0]
            link_link = link[1]
            sections = current_text.split(f"[{link_alt}]({link_link})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, formatted section not closed")
            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            split_nodes.append(TextNode(link_alt, TextType.LINK, link_link))
            current_text = sections[1]
        if current_text != "":
            split_nodes.append(TextNode(current_text, TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes


def text_to_textnodes(raw_text: str)-> list[TextNode]:
    raw_text_node = [(TextNode(raw_text, TextType.TEXT))]
    raw_text_node_bold = split_nodes_delimiter(old_nodes=raw_text_node,delimiter="**", text_type=TextType.BOLD)
    raw_text_node_italic = split_nodes_delimiter(old_nodes=raw_text_node_bold,delimiter="_", text_type=TextType.ITALIC)
    raw_text_node_code = split_nodes_delimiter(old_nodes=raw_text_node_italic,delimiter="`", text_type=TextType.CODE)
    text_node_images = split_nodes_image(old_nodes=raw_text_node_code)
    text_node_images_and_links = split_nodes_link(old_nodes=text_node_images)
    return text_node_images_and_links



