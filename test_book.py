import unittest
from main import Book

class Testbook(unittest.TestCase):

    def test_show_info(self):
        bok = Book("My Book", "My Author", 2000)
        resultat = bok.show_info()
        self.assertEqual(resultat, "Titel: My Book, Författare: My Author, År: 2000")

if __name__ == "__main__":
    unittest.main()