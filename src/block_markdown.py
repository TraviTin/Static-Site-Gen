from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    split_markdown = markdown.split("\n\n")
    new_markdown = []
    for block in split_markdown:
        stripped = block.strip()
        if stripped == "":
            continue
        new_markdown.append(stripped)
    return new_markdown

def block_to_block_type(block: str) -> BlockType:
    split_by_lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(split_by_lines) >= 2 and split_by_lines[0].startswith("```") and split_by_lines[-1] == "```":
        return BlockType.CODE
    if block.startswith(">"):
        for line in split_by_lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in split_by_lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if not block.startswith("1. "):
        return BlockType.PARAGRAPH
    for num, line in enumerate(split_by_lines, start=1):
        if not line.startswith(f"{num}. "):
            return BlockType.PARAGRAPH
    return BlockType.ORDERED_LIST