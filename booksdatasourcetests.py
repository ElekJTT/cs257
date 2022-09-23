'''
   booksdatasourcetest.py
   Jeff Ondich, 24 September 2021
'''

from booksdatasource import Author, Book, BooksDataSource
import unittest

class BooksDataSourceTester(unittest.TestCase):
    def setUp(self):
        self.data_source = BooksDataSource('books1.csv')

    def tearDown(self):
        pass

    def test_unique_author(self):
        authors = self.data_source.authors('Pratchett')
        self.assertTrue(len(authors) == 1)
        self.assertTrue(authors[0] == Author('Pratchett', 'Terry'))

    def test_all_books(self):
        tiny_data_source = BooksDataSource('tinybooks.csv')
        books = tiny_data_source.books()
        self.assertTrue(len(books) == 3)
        self.assertTrue(books[0].title == 'Emma')
        self.assertTrue(books[1].title == 'Neverwhere')
        self.assertTrue(books[2].title == 'Omoo')

    def test_authors(self):
	tiny_data_source = BooksDataSource('tinybooks.csv')
	authors = tiny_data_source.authors()
	self.assertTrue = (len(authors) == 3) 
	self.assertTrue(author[0].given_name == 'Jane Austen')
	self.assertTrue(author[1].given_name == 'Neil Gaiman')
	self.assertTrue(author[2].given_name == 'Herman Melville')


if __name__ == '__main__':
    unittest.main()

