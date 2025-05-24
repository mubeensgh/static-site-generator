import unittest
from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        node1 = LeafNode("a", "Hello, world!", {"href" : "value", "link" : "value2"})
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(node1.to_html(), '<a href="value" link="value2">Hello, world!</a>')
class TestParentNode(unittest.TestCase):
     def test_to_html_with_children(self):
         child_node = LeafNode("span", "child")
         parent_node = ParentNode("div", [child_node])
         self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
     def test_to_html_with_grandchildren(self):
         grandchild_node = LeafNode("b", "grandchild")
         child_node = ParentNode("span", [grandchild_node])
         parent_node = ParentNode("div", [child_node])
         self.assertEqual(parent_node.to_html(),"<div><span><b>grandchild</b></span></div>",)

if __name__=="__main__":
    unittest.main()