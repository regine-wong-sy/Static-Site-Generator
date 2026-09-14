import unittest
from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_strips_whitespace(self):
        self.assertEqual(extract_title("#   Hello World   "), "Hello World")

    def test_ignores_lower_headings(self):
        markdown = "## Not this one\n# This one\nSome text"
        self.assertEqual(extract_title(markdown), "This one")

    def test_title_not_on_first_line(self):
        markdown = "Some intro text\n\n# The Real Title\n\nMore text"
        self.assertEqual(extract_title(markdown), "The Real Title")

    def test_no_h1_raises(self):
        markdown = "## Only a subheading\nSome text"
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_empty_string_raises(self):
        with self.assertRaises(ValueError):
            extract_title("")


if __name__ == "__main__":
    unittest.main()
