import unittest
from textnode import TextNode, TextType
from htmlnode import *

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_single_code_block(self):
        text1 = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        text2 = [("rick roll","https://i.imgur.com/aKaOqIh.gif"),("obi wan","https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extract_markdown_images(text1),text2)

    def test_single_bold_phrase(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.Normal)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is text with a ", TextType.Normal),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.Normal),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_single_italic_phrase(self):
        node = TextNode("This is text with an _italic phrase_ here", TextType.Normal)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected_nodes = [
            TextNode("This is text with an ", TextType.Normal),
            TextNode("italic phrase", TextType.ITALIC),
            TextNode(" here", TextType.Normal),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_multiple_delimiters(self):
        node = TextNode("This is **bold** and `code` and _italic_ text.", TextType.Normal)
        
        nodes_after_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_after_bold = [
            TextNode("This is ", TextType.Normal),
            TextNode("bold", TextType.BOLD),
            TextNode(" and `code` and _italic_ text.", TextType.Normal),
        ]
        self.assertEqual(nodes_after_bold, expected_after_bold)

        
        nodes_after_code = split_nodes_delimiter(nodes_after_bold, "`", TextType.CODE)
        expected_after_code = [
            TextNode("This is ", TextType.Normal),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.Normal),
            TextNode("code", TextType.CODE),
            TextNode(" and _italic_ text.", TextType.Normal),
        ]
        self.assertEqual(nodes_after_code, expected_after_code)

        
        nodes_after_italic = split_nodes_delimiter(nodes_after_code, "_", TextType.ITALIC)
        expected_after_italic = [
            TextNode("This is ", TextType.Normal),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.Normal),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.Normal),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.Normal),
        ]
        self.assertEqual(nodes_after_italic, expected_after_italic)

    def test_multiple_same_delimiter(self):
        node = TextNode("This is **bold** and **more bold** text.", TextType.Normal)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is ", TextType.Normal),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.Normal),
            TextNode("more bold", TextType.BOLD),
            TextNode(" text.", TextType.Normal),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_delimiter_at_start_and_end(self):
        node = TextNode("**Bold text**", TextType.Normal)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("Bold text", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected_nodes)

        node = TextNode("`Code block`", TextType.Normal)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("Code block", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_no_delimiter(self):
        node = TextNode("This is plain text.", TextType.Normal)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is plain text.", TextType.Normal),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_unmatched_delimiter(self):
        node = TextNode("This has an **unmatched delimiter.", TextType.Normal)
        with self.assertRaisesRegex(ValueError, r"Invalid Markdown syntax: Unmatched delimiter '\*\*' found in text: This has an \*\*unmatched delimiter."):
            split_nodes_delimiter([node], "**", TextType.BOLD)

        node = TextNode("`Unmatched code", TextType.Normal)
        with self.assertRaisesRegex(ValueError, r"Invalid Markdown syntax: Unmatched delimiter '`' found in text: `Unmatched code"):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_empty_string_between_delimiters(self):
        node = TextNode("Text with **empty** ` ` code.", TextType.Normal)
        nodes_after_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_after_bold = [
            TextNode("Text with ", TextType.Normal),
            TextNode("empty", TextType.BOLD),
            TextNode(" ` ` code.", TextType.Normal),
        ]
        self.assertEqual(nodes_after_bold, expected_after_bold)

        nodes_after_code = split_nodes_delimiter(nodes_after_bold, "`", TextType.CODE)
        expected_after_code = [
            TextNode("Text with ", TextType.Normal),
            TextNode("empty", TextType.BOLD),
            TextNode(" ", TextType.Normal), # This is the space between the delimiters
            TextNode(" ", TextType.CODE),  # This is the empty string inside the delimiters
            TextNode(" code.", TextType.Normal),
        ]
        self.assertEqual(nodes_after_code, expected_after_code)


    def test_already_processed_node(self):
        # A node that is already bold should not be processed by split_nodes_delimiter for bold
        node = TextNode("This is already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is already bold", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected_nodes)

        node = TextNode("This is already code", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is already code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_multiple_nodes_input(self):
        node1 = TextNode("First **bold** part.", TextType.Normal)
        node2 = TextNode("Second _italic_ part.", TextType.Normal)
        node3 = TextNode("Third `code` part.", TextType.Normal)

        nodes_input = [node1, node2, node3]

        # Process bold
        result_bold = split_nodes_delimiter(nodes_input, "**", TextType.BOLD)
        expected_bold = [
            TextNode("First ", TextType.Normal),
            TextNode("bold", TextType.BOLD),
            TextNode(" part.", TextType.Normal),
            TextNode("Second _italic_ part.", TextType.Normal),
            TextNode("Third `code` part.", TextType.Normal),
        ]
        self.assertEqual(result_bold, expected_bold)

        # Process italic on the result of bold
        result_italic = split_nodes_delimiter(result_bold, "_", TextType.ITALIC)
        expected_italic = [
            TextNode("First ", TextType.Normal),
            TextNode("bold", TextType.BOLD),
            TextNode(" part.", TextType.Normal),
            TextNode("Second ", TextType.Normal),
            TextNode("italic", TextType.ITALIC),
            TextNode(" part.", TextType.Normal),
            TextNode("Third `code` part.", TextType.Normal),
        ]
        self.assertEqual(result_italic, expected_italic)

        # Process code on the result of italic
        result_code = split_nodes_delimiter(result_italic, "`", TextType.CODE)
        expected_code = [
            TextNode("First ", TextType.Normal),
            TextNode("bold", TextType.BOLD),
            TextNode(" part.", TextType.Normal),
            TextNode("Second ", TextType.Normal),
            TextNode("italic", TextType.ITALIC),
            TextNode(" part.", TextType.Normal),
            TextNode("Third ", TextType.Normal),
            TextNode("code", TextType.CODE),
            TextNode(" part.", TextType.Normal),
        ]
        self.assertEqual(result_code, expected_code)


if __name__ == '__main__':
    unittest.main()
