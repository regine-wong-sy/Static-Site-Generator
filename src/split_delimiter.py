from htmlnode import LeafNode, ParentNode, HTMLNode
from textnode import TextNode, text_node_to_html_node, TextType
from extract_markdown import extract_markdown_images, extract_markdown_links
from enum import Enum

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")

        for i, section in enumerate(sections):
            if section == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(section, TextType.TEXT))
            else:
                new_nodes.append(TextNode(section, text_type))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        for alt, url in images:
            sections = original_text.split(f"![{alt}]({url})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        for text, url in links:
            sections = original_text.split(f"[{text}]({url})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(text, TextType.LINK, url))
            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def text_to_children(text: str) -> list:
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children


def markdown_to_blocks(markdown:str) -> list[str]:
    newlst = []
    blocks = markdown.split("\n\n")
    for line in blocks:
        lines = line.split("\n")
        cleaned_lines = []
        for l in lines:
            cleaned_lines.append(l.strip())
        stripped = "\n".join(cleaned_lines).strip()
        if stripped != "":
            newlst.append(stripped)
    return newlst

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST= "ordered_list"

def block_to_block_type(markdown: str) -> BlockType:
    for x in range(1, 7):
        if markdown.startswith("#" * x + " "):
            return BlockType.HEADING
    lines = markdown.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
            return BlockType.UNORDERED_LIST
    if markdown.startswith("`" * 3) and markdown.endswith("`" * 3):
        return BlockType.CODE
    if all(line.startswith(f"{i}. ") for i, line in enumerate(lines, start=1)):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            html_node = ParentNode("p", text_to_children(block))

        elif block_type == BlockType.HEADING:
            for x in range(1, 7):
                if block.startswith("#" * x + " "):
                    level = x
                    text = block[x + 1:]
                    break
            html_node = ParentNode(f"h{level}", text_to_children(text))

        elif block_type == BlockType.CODE:
            text = block[4:-3]  # strip leading "```\n" and trailing "```"
            code_text_node = TextNode(text, TextType.TEXT)
            code_leaf = text_node_to_html_node(code_text_node)
            html_node = ParentNode("pre", [ParentNode("code", [code_leaf])])

        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            new_lines = [line.lstrip(">").strip() for line in lines]
            text = "\n".join(new_lines)
            html_node = ParentNode("blockquote", text_to_children(text))

        elif block_type == BlockType.UNORDERED_LIST:
            items = block.split("\n")
            list_items = []
            for item in items:
                item_text = item[2:]  # strip "- "
                list_items.append(ParentNode("li", text_to_children(item_text)))
            html_node = ParentNode("ul", list_items)

        elif block_type == BlockType.ORDERED_LIST:
            items = block.split("\n")
            list_items = []
            for i, item in enumerate(items, start=1):
                prefix = f"{i}. "
                item_text = item[len(prefix):]
                list_items.append(ParentNode("li", text_to_children(item_text)))
            html_node = ParentNode("ol", list_items)

        children.append(html_node)

    return ParentNode("div", children)
