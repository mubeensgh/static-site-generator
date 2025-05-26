from textnode import *
import re

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        #tag and value are strings, children are HTMLNode Objects
        #props are a dictionary of key value pairs representing atribute and values
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        #children will override this
        pass
    def props_to_html(self):
        res = ""
        if self.props == None:
            return res
        for i,j in self.props.items():
            res+= f' {i}="{j}"'
        return res
    def __repr__(self):
        return f'tag = {self.tag}, value = {self.value}, children = {self.children}, props = {self.props}'

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value == None:
            raise ValueError("LeafNode requires a value.")
        super().__init__(tag, value, children=[], props=props)
    def to_html(self):
        if self.tag == None:
            return str(self.value)
        return f'<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        #tag and children are mandatory!! - therefore, no value argument
        if tag is None:
            raise ValueError("ParentNode requires a tag.")
        if not children:
            raise ValueError("ParentNode requires at least one child.")

        super().__init__(tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode requires a tag to render HTML.")
        if not self.children:
            raise ValueError("ParentNode must have children to render HTML.")

        # init the children html
        children_html = ""        
        #loop first for each item in children
        for child in self.children:
            #children_html = child.to_html()
            children_html += child.to_html()
        return f'<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>'

#This function
#1st argument is a LIST of TEXTNODES i.e [TextNode1,TextNode2,TextNode3]
#2nd argument is a string: can be one of 3: **, _ or `
#3rd argument is a text_type enumeration.
#Important! text_type should match the delimiter
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter:str, text_type:TextType):
    new_nodes=[]
    for old_node in old_nodes:
        if old_node.text_type != TextType.Normal:
            new_nodes.append(old_node)
            continue
        splitted = old_node.text.split(delimiter)
        if len(splitted) % 2 == 0: #make sure that all openings are closed
            raise ValueError(f"Invalid Markdown syntax: Unmatched delimiter '{delimiter}' found in text: {old_node.text}")
        for index, item in enumerate(splitted):
            if item == "":
                continue
            if index % 2 == 0: #text before starting delimiter or after ending delimiter
                new_nodes.append(TextNode(item,TextType.Normal))
            else: #text in between startng and ending delimiter
                new_nodes.append(TextNode(item,text_type))
    return new_nodes

def extract_markdown_images(text:str) -> list[tuple]:
    res= re.findall(r'!\[(.*?)\]\((.*?)\)', text)
    return res

def split_nodes_images(old_nodes):
    ...
def split_nodes_links(old_nodes):
    ...
    
