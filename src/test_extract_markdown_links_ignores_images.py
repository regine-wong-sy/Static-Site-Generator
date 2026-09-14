import unittest
from textnode import TextNode, TextType
from split_delimiter import text_to_textnodes,markdown_to_blocks


class TestTextToTextNodes(unittest.TestCase):
    def test_full_example(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a "
            "[link](https://boot.dev)"
        )
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_plain_text(self):
        nodes = text_to_textnodes("Just plain text, nothing special.")
        self.assertListEqual(
            [TextNode("Just plain text, nothing special.", TextType.TEXT)], nodes
        )

    def test_only_bold(self):
        nodes = text_to_textnodes("This is **bold** only.")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" only.", TextType.TEXT),
            ],
            nodes,
        )

    def test_only_image(self):
        nodes = text_to_textnodes("![alt](https://example.com/img.png)")
        self.assertListEqual(
            [TextNode("alt", TextType.IMAGE, "https://example.com/img.png")], nodes
        )


    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
                    blocks,
                    [
                        "This is **bolded** paragraph",
                        "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                        "- This is a list\n- with items",
                    ],
                )

if __name__ == "__main__":
    unittest.main()