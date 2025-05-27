import re
from enum import Enum

from src.textnode import TextNode, TextType, text_to_textnodes, text_node_to_html_node
from src.htmlnode import HTMLNode, LeafNode, ParentNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:

    blocks = markdown.strip().split("\n\n")
    
    filtered_blocks = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:
            filtered_blocks.append(stripped_block)
            
    return filtered_blocks

def block_to_block_type(block: str) -> BlockType:

    lines = block.split('\n')


    if block.startswith("#"):
        num_hashes = 0
        for char in block:
            if char == '#':
                num_hashes += 1
            else:
                break
        if 1 <= num_hashes <= 6 and block[num_hashes] == ' ':
            return BlockType.HEADING


    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE


    is_quote = True
    for line in lines:
        if not line.startswith(">"):
            is_quote = False
            break
    if is_quote:
        return BlockType.QUOTE


    is_unordered_list = True
    for line in lines:
        if not (line.startswith("- ") or line.startswith("* ")):
            is_unordered_list = False
            break
    if is_unordered_list:
        return BlockType.UNORDERED_LIST


    is_ordered_list = True
    expected_num = 1
    for line in lines:
        parts = line.split('.', 1)
        if len(parts) < 2 or not parts[0].isdigit() or int(parts[0]) != expected_num or not parts[1].startswith(' '):
            is_ordered_list = False
            break
        expected_num += 1
    if is_ordered_list:
        return BlockType.ORDERED_LIST


    return BlockType.PARAGRAPH

def text_to_children(text: str) -> list[HTMLNode]:

    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children_html_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.PARAGRAPH:
            children_html_nodes.append(ParentNode("p", text_to_children(block)))
        
        elif block_type == BlockType.HEADING:
            num_hashes = 0
            for char in block:
                if char == '#':
                    num_hashes += 1
                else:
                    break
            heading_text = block[num_hashes + 1:].strip()
            children_html_nodes.append(ParentNode(f"h{num_hashes}", text_to_children(heading_text)))
        
        elif block_type == BlockType.CODE:
            code_content = block[3:-3].strip()
            children_html_nodes.append(ParentNode("pre", [LeafNode("code", code_content)]))
        
        elif block_type == BlockType.QUOTE:
            quote_lines = block.split('\n')
            quote_content_nodes = []
            for line in quote_lines:
                stripped_line = line[1:].strip()
                quote_content_nodes.extend(text_to_children(stripped_line))
            children_html_nodes.append(ParentNode("blockquote", quote_content_nodes))
        
        elif block_type == BlockType.UNORDERED_LIST:
            list_items = block.split('\n')
            ul_children = []
            for item_text in list_items:
                stripped_item_text = item_text[2:].strip()
                ul_children.append(ParentNode("li", text_to_children(stripped_item_text)))
            children_html_nodes.append(ParentNode("ul", ul_children))
        
        elif block_type == BlockType.ORDERED_LIST:
            list_items = block.split('\n')
            ol_children = []
            for item_text in list_items:
                dot_index = item_text.find('.')
                stripped_item_text = item_text[dot_index + 1:].strip()
                ol_children.append(ParentNode("li", text_to_children(stripped_item_text)))
            children_html_nodes.append(ParentNode("ol", ol_children))
        
        else:
            children_html_nodes.append(ParentNode("p", text_to_children(block)))

    return ParentNode("div", children_html_nodes)

def extract_title(markdown:str)-> str:
    res=""
    lines = markdown.split("\n")
    for line in lines:
        if line.strip().startswith("#") and not line.strip().startswith("##"):
            return line.strip()[2:].strip()
    raise ValueError("No H1 header found in the markdown document.")
    