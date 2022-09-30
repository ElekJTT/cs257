'''
   booksdatasourcetest.py
   Ryan Dunn and Elek Thomas-Toth - Sept 23rd, September 2022
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
        self.assertEqual(authors[0].given_name,'Terry')

    def test_all_books(self):
        tiny_data_source = BooksDataSource('tinybooks.csv')
        books = tiny_data_source.books()
        self.assertTrue(len(books) == 3)
        self.assertTrue(books[0].title == 'Emma')
        self.assertTrue(books[1].title == 'Neverwhere')
        self.assertTrue(books[2].title == 'Omoo')
   
    def test_search_books(self):
        tiny_data_source = BooksDataSource('tinybooks.csv')
        books = tiny_data_source.books("M")
        self.assertEqual(books[0].title, "Emma")
        self.assertEqual(books[1].title,"Omoo")

    def test_sort_by_year_books(self):
        tiny_data_source = BooksDataSource('tinybooks.csv')
        books = tiny_data_source.books("m", "year")
        self.assertTrue(books[0].title == "Emma")
        self.assertTrue(books[1].title == "Omoo")

    def test_empty_search_books(self):
        tiny_data_source = BooksDataSource('tinybooks.csv')
        books = tiny_data_source.books("Bet you haven't heard of this book")
        self.assertIsNone(books)

    def test_all_authors(self):
        tiny_data_source = BooksDataSource('tinybooks.csv')
        authors = tiny_data_source.authors()
        self.assertTrue = (len(authors) == 3) 
        self.assertEqual(authors[0].given_name, 'Jane')
        self.assertEqual(authors[1].given_name, 'Neil')
        self.assertEqual(authors[2].given_name, 'Herman')
   
    def test_search_authors(self):
        tiny_data_source = BooksDataSource('tinybooks.csv')
        authors = tiny_data_source.authors("Jane")
        self.assertEqual(authors[0].given_name, "Jane")
        authors = tiny_data_source.authors("jaNe")
        self.assertEqual(authors[0].given_name, "Jane")

    def test_empty_search_authors(self):
        tiny_data_source = BooksDataSource("tinybooks.csv")
        authors = tiny_data_source.authors("Janet Boston")
        self.assertIsNone(authors)
 
    def test_books_between_years(self):
        tiny_data_source = BooksDataSource('tinybooks.csv')
        books  = tiny_data_source.books_between_years(1800, 1900)
        self.assertTrue(books[0].title == "Emma")
        self.assertTrue(books[1].title == "Omoo")

    def test_no_books_published_books_between_years(self):
        tiny_data_source = BooksDataSource('tinybooks.csv')
        books  = tiny_data_source.books_between_years(2100, 2200)
        self.assertIsNone(books)

    def test_wrong_order_books_between_years(self):
        tiny_data_source = BooksDataSource('tinybooks.csv')
        books  = tiny_data_source.books_between_years(1900, 1800)
        self.assertRaises(Exception)

    def test_no_date_books_between_years(self):
        tiny_data_source = BooksDataSource('tinybooks.csv')
        books  = tiny_data_source.books_between_years()
        self.assertTrue(len(books) == 3)
        self.assertTrue(books[0].title == 'Emma')
        self.assertTrue(books[1].title == 'Omoo')
        self.assertTrue(books[2].title == 'Neverwhere')
	
if __name__ == '__main__':
    unittest.main()

