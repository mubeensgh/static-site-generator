import re
from enum import Enum

class TextType(Enum):
    Normal = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return NotImplemented 
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'

def text_node_to_html_node(text_node):
    from src.htmlnode import LeafNode 

    match text_node.text_type:
        case TextType.Normal:
            return LeafNode("",text_node.text)
        case TextType.BOLD:
            return LeafNode("b",text_node.text)
        case TextType.ITALIC:
            return LeafNode("i",text_node.text)
        case TextType.CODE:
            return LeafNode("code",text_node.text)
        case TextType.LINK:
            return LeafNode("a",text_node.text,{"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img","",{"src":text_node.url,"alt":text_node.text})

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.Normal:
            new_nodes.append(old_node)
            continue

        if not old_node.text:
            new_nodes.append(old_node)
            continue

        splitted = old_node.text.split(delimiter)
        if len(splitted) % 2 == 0:
            raise ValueError(f"Invalid Markdown syntax: Unmatched delimiter '{delimiter}' found in text: {old_node.text}")
        
        for index, item in enumerate(splitted):
            if item == "" and len(splitted) > 1:
                continue
            
            if index % 2 == 0:
                new_nodes.append(TextNode(item, TextType.Normal))
            else:
                new_nodes.append(TextNode(item, text_type))
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    image_regex = r"!\[(.*?)\]\((.*?)\)" 
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.Normal:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        parts = re.split(image_regex, text)

        if len(parts) == 1 and parts[0] == text:
            new_nodes.append(old_node)
            continue

        for i in range(0, len(parts), 3):
            normal_text_segment = parts[i]

            if normal_text_segment:
                new_nodes.append(TextNode(normal_text_segment, TextType.Normal))

            if i + 1 < len(parts):
                alt_text = parts[i+1]
                image_url = parts[i+2]
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_url))
            
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    link_regex = r"\[(.*?)\]\((.*?)\)" 
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.Normal:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        parts = re.split(link_regex, text)


        if len(parts) == 1 and parts[0] == text:
            new_nodes.append(old_node)
            continue

        for i in range(0, len(parts), 3):
            normal_text_segment = parts[i]

            if normal_text_segment: 
                new_nodes.append(TextNode(normal_text_segment, TextType.Normal))

            if i + 1 < len(parts):
                link_text = parts[i+1]
                link_url = parts[i+2]
                new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:


    nodes = [TextNode(text, TextType.Normal)]

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes
