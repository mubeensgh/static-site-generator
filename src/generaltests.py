import unittest
from markdown_parser import markdown_to_html_node, BlockType
from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType

class TestMarkdownToHtmlNode(unittest.TestCase):

    def test_markdown_to_html_node_paragraph(self):
        md = "This is a **bold** paragraph with _italic_ text."
        expected_html = ParentNode("div", [
            ParentNode("p", [
                TextNode("This is a ", TextType.Normal),
                TextNode("bold", TextType.BOLD),
                TextNode(" paragraph with ", TextType.Normal),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text.", TextType.Normal),
            ])
        ])

       
    

    def test_markdown_to_html_node_heading(self):
        md = "# Main **Heading**\n\n## Sub _Heading_"
        expected_html = ParentNode("div", [
            ParentNode("h1", [
                LeafNode("", "Main "),
                LeafNode("b", "Heading"),
            ]),
            ParentNode("h2", [
                LeafNode("", "Sub "),
                LeafNode("i", "Heading"),
            ])
        ])
        self.assertEqual(markdown_to_html_node(md), expected_html)

    def test_markdown_to_html_node_code(self):
        md = "```\nprint('Hello, **World**!')\n```"
        expected_html = ParentNode("div", [
            ParentNode("pre", [
                LeafNode("code", "print('Hello, **World**!')")
            ])
        ])
        self.assertEqual(markdown_to_html_node(md), expected_html)

    def test_markdown_to_html_node_quote(self):
        md = "> This is a quote.\n> It has two lines."
        expected_html = ParentNode("div", [
            ParentNode("blockquote", [
                LeafNode("", "This is a quote."), 
                LeafNode("", "It has two lines."),
            ])
        ])
        self.assertEqual(markdown_to_html_node(md), expected_html)
        
        # Test with inline markdown in quote
        md_with_inline = "> This is a **bold** quote.\n> And _another_ line."
        expected_html_with_inline = ParentNode("div", [
            ParentNode("blockquote", [
                LeafNode("", "This is a "),
                LeafNode("b", "bold"),
                LeafNode("", " quote."),
                LeafNode("", "And "),
                LeafNode("i", "another"),
                LeafNode("", " line."),
            ])
        ])
        self.assertEqual(markdown_to_html_node(md_with_inline), expected_html_with_inline)