import unittest
from textnode import TextType, TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1  = TextNode("This is a text node",TextType.BOLD)
        node2 = TextNode("This is a text node",TextType.BOLD)
        node3 = TextNode("This is a text node",TextType.BOLD, "www.google.com")
        node4 = TextNode("This is a text node",TextType.BOLD, None)
        node5 = TextNode("This is a text node",TextType.Normal, "www.google.com")
        self.assertEqual(node1,node2)
        self.assertEqual(node1,node4)
        self.assertNotEqual(node1,node3)
        self.assertNotEqual(node5,node3)
if __name__ == "__main__":
    unittest.main()