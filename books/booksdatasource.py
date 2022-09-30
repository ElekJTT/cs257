#!/usr/bin/env python3
'''
    booksdatasource.py
    Jeff Ondich, 21 September 2022

    For use in the "books" assignment at the beginning of Carleton's
    CS 257 Software Design class, Fall 2022.
'''

import csv

class Author:
    def __init__(self, surname='', given_name='', birth_year=None, death_year=None):
        self.surname = surname
        self.given_name = given_name
        self.birth_year = birth_year
        self.death_year = death_year

    def __eq__(self, other):
        ''' For simplicity, we're going to assume that no two authors have the same name. '''
        return self.surname == other.surname and self.given_name == other.given_name

    def __lt__(self, other):
        if self.surname < other.surname:
            return True
        if self.surname == other.surname and self.given_name < other.given_name:
            return True
        return False

    def __str__(self):
        return self.given_name + " " + self.surname

class Book:
    def __init__(self, title='', publication_year=None, authors=[]):
        ''' Note that the self.authors instance variable is a list of
            references to Author objects. '''
        self.title = title
        self.publication_year = int(publication_year)
        self.authors = authors

    def __eq__(self, other):
        ''' We're going to make the excessively simplifying assumption that
            no two books have the same title, so "same title" is the same
            thing as "same book". '''
        return self.title == other.title

    def __lt__(self, other):
        if self.title < other.title:
            return True

        return False

    def __str__(self):
        return self.title


class BooksDataSource: #Not for user to use. There is a difference between user typing stuff to command line interface. 
    def __init__(self, books_csv_file_name):
        self.bookList = []

        self.authorsDict = {

        }

        self.author_objects = []

        #How do we deal with middle names?
        with open(books_csv_file_name, 'r') as books:
            booksReader = csv.reader(books)
            for row in booksReader: 
                authorSplit = row[2].replace(" and ", ",").split(", ")
  
                for item in authorSplit:
                    master_string_split = item.split("(")
                    full_name = master_string_split[0].strip()
                    if full_name not in self.authorsDict:
                        author_given = full_name[0].split()[0].strip()
                        author_last = full_name[0].split()[-1].strip()

                        date = master_string_split[1][:-1]
                        date_split = date.split("-")

                        birth_year = date_split[0].strip()
                        death_year = date_split[1].strip()

                        new_author = Author(author_last, author_given, birth_year, death_year)                        
                        self.authorsDict[full_name] = new_author

                        self.author_objects.append(new_author)
                    else: 
                        self.author_objects.append(self.authorsDict[full_name])

                newBook = Book(row[0].strip(), row[1].strip(), self.author_objects)
                self.bookList.append(newBook)

        ''' The books CSV file format looks like this:

                title,publication_year,author_description

            For example:

                All Clear,2010,Connie Willis (1945-)
                "Right Ho, Jeeves",1934,Pelham Grenville Wodehouse (1881-1975)

            This __init__ method parses the specified CSV file and creates
            suitable instance variables for the BooksDataSource object containing
            a collection of Author objects and a collection of Book objects.
        '''
        pass

    def authors(self, search_text=None):
        ''' Returns a list of all the Author objects in this data source whose names contain
            (case-insensitively) the search text. If search_text is None, then this method
            returns all of the Author objects. In either case, the returned list is sorted
            by surname, breaking ties using given name (e.g. Ann Brontë comes before Charlotte Brontë).
        '''
        authors_to_print = []

        if search_text == None:
            return sorted(self.author_objects)
        
        for author in sorted(self.author_objects):
            if search_text in author.given_name or search_text in author.surname:
                authors_to_print.append(author)
        
        if len(authors_to_print) < 1:
            return None

        return authors_to_print

    def books(self, search_text=None, sort_by='title'):
        ''' Returns a list of all the Book objects in this data source whose
            titles contain (case-insensitively) search_text. If search_text is None,
            then this method returns all of the books objects.

            The list of books is sorted in an order depending on the sort_by parameter:

                'year' -- sorts by publication_year, breaking ties with (case-insenstive) title
                'title' -- sorts by (case-insensitive) title, breaking ties with publication_year
                default -- same as 'title' (that is, if sort_by is anything other than 'year'
                            or 'title', just do the same thing you would do for 'title')
        '''

        if search_text == None:
            return sorted(self.bookList)

        books_to_print = []

        if sort_by == 'title':
            for book in sorted(self.bookList):
                if search_text in book.title:
                    books_to_print.append(book)

        else:

            for book in self.sort_books_by_year(sorted(self.bookList)):
                if search_text in book.title:
                    books_to_print.append(book)

        if len(books_to_print) < 1:
            return None
        else:
            return books_to_print

        




    def books_between_years(self, start_year=None, end_year=None):
        ''' Returns a list of all the Book objects in this data source whose publication
            years are between start_year and end_year, inclusive. The list is sorted
            by publication year, breaking ties by title (e.g. Neverwhere 1996 should
            come before Thief of Time 1996).

            If start_year is None, then any book published before or during end_year
            should be included. If end_year is None, then any book published after or
            during start_year should be included. If both are None, then all books
            should be included.
        '''
        books_between_years = []
        if start_year != None:
            start_year = int(start_year)
        if end_year != None:
            end_year = int(end_year)

        if start_year == None and end_year == None:
            return self.sort_books_by_year(self.bookList)

        elif start_year == None:
            for book in sorted(self.bookList):
                if book.publication_year <= end_year:
                    books_between_years.append(book)

        elif end_year == None:
            for book in sorted(self.bookList):
                if book.publication_year >= int(start_year):
                    books_between_years.append(book)

        else:
            for book in sorted(self.bookList):
                if book.publication_year >= int(start_year) and book.publication_year <= int(end_year):
                    books_between_years.append(book)

        if len(books_between_years) < 1:
            return None
        return self.sort_books_by_year(books_between_years)


    def sort_books_by_year(self, books):

        for step in range(1, len(books)):
            key = books[step].publication_year
            j = step - 1
            
            # Compare key with each element on the left of it until an element smaller than it is found
            # For descending order, change key<array[j] to key>array[j].        
            while j >= 0 and key < books[j].publication_year:
                books[j + 1].publication_year = books[j].publication_year
                j = j - 1

            
            # Place key at after the element just smaller than it.
            books[j + 1].publication_year = key

        return books

