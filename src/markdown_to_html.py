from block_markdown import *
from textnode import *
from inline_markdown import *
from htmlnode import *


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children_list = []
    for block in blocks:
        html_block = block_to_html_node(block)
        children_list.append(html_block)
    div = ParentNode(tag="div", children=children_list)
    return div

def block_to_html_node(block: str) -> ParentNode:
    determine_type = block_to_block_type(block)
    match determine_type:
        case BlockType.PARAGRAPH:
            html_block = paragraph_node(block)
        case BlockType.HEADING:
            html_block = heading_node(block)
        case BlockType.CODE:
            html_block = code_node(block)
        case BlockType.QUOTE:
            html_block = quote_node(block)
        case BlockType.UNORDERED_LIST:
            html_block = unordered_list_node(block)
        case BlockType.ORDERED_LIST:
            html_block = ordered_list_node(block)
        case _:
            raise ValueError("invalid block type")
    return html_block


def paragraph_node(block: str) -> ParentNode:
    lines = block.split("\n")
    paragraph = " ".join(lines)
    nodes = text_to_children(paragraph)
    return ParentNode(tag="p", children=nodes)


def heading_node(block: str) -> ParentNode:
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text_block = block[level + 1:]
    nodes = text_to_children(text_block)
    return ParentNode(tag=f"h{level}", children=nodes)


def code_node(block: str) -> ParentNode:
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    stripped = block[4:-3]
    stripped_node = TextNode(text=stripped, text_type=TextType.TEXT)
    stripped_html_node = text_node_to_html_node(stripped_node)
    code = ParentNode(tag="code", children=[stripped_html_node])
    return ParentNode(tag="pre", children=[code])


def quote_node(block: str) -> ParentNode:
    split_by_lines = block.split("\n")
    cleaned_lines = []
    for line in split_by_lines:
        if line.startswith(">"):
            cleaned_lines.append(line.lstrip(">").strip())
    cleaned_lines = " ".join(cleaned_lines)
    node = text_to_children(cleaned_lines)
    return ParentNode(tag="blockquote", children=node)


def unordered_list_node(block: str) -> HtmlNode:
    split_by_lines = block.split("\n")
    list_of_all_nodes = []
    for lines in split_by_lines:
        if not lines.startswith(">"):
            raise ValueError("invalid quote block")
        stripped = lines[2:]
        list_nodes = text_to_children(stripped)
        node = ParentNode(tag="li", children=list_nodes)
        list_of_all_nodes.append(node)
    return ParentNode(tag="ul", children=list_of_all_nodes)


def ordered_list_node(block: str) -> HtmlNode:
    split_by_lines = block.split("\n")
    list_of_final_nodes = []
    for lines in split_by_lines:
        separate_lines = lines.split(". ", 1)
        line = separate_lines[1]
        stripped_line = line.strip()
        list_nodes = text_to_children(stripped_line)
        node = ParentNode(tag="li", children=list_nodes)
        list_of_final_nodes.append(node)
    return ParentNode(tag="ol", children=list_of_final_nodes)


def text_to_children(block: str) -> list[HtmlNode]:
    text_node_block = text_to_textnodes(block)
    html_children = []
    for node in text_node_block:
        nodes = text_node_to_html_node(node)
        html_children.append(nodes)
    return html_children
