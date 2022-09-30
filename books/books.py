import sys
from booksdatasource import *

def main(arguments):

    datasource = BooksDataSource('tinybooks.csv')

    if arguments['option'] == 'h':
        print(usage_statement())

    if arguments['option'] == 'b':
        if 'string' in arguments:
            booksource = datasource.books(arguments['string'])
            for book in booksource:
                print(book)
        else:
            booksource = datasource.books()
            for book in booksource:
                print(book)

    if arguments['option'] == 'a':
        if 'string' in arguments:
            author_source = datasource.authors(arguments['string'])
            for author in author_source:
                print(author)
        else:
            author_source = datasource.authors()
            for author in author_source:
                print(author)

    if arguments['option'] == 'p':
        if 'string' in arguments:
            booksource = datasource.books(arguments["string"], "year")
            for book in booksource: 
                print(book)
        else:
            booksource = datasource.books()
            for book in booksource: 
                print(book)

    if arguments['option'] == 'y':

        if 'year1' in arguments:
            if 'year2' in arguments:
                if arguments['year1'] > arguments['year2']:
                    raise Exception("Start date cannot be after end date")
                booksource = datasource.books_between_years(arguments['year1'], arguments['year2'])
                for book in booksource:
                    print(book)
            else:
                booksource = datasource.books_between_years(arguments['year1'])
                for book in booksource: 
                    print(book)
        else:
            if 'year2' in arguments:
                booksource = datasource.books_between_years(arguments['year2'])
                for book in booksource: 
                    print(book)
            else:
                booksource = datasource.books_between_years()
                for book in booksource: 
                    print(book)





def usage_statement():
    statement = f'Usage: book searching of various forms\n'
    return statement

def parse_command_line():
    arguments = {}


    
    #setting option to correct modifier
    for option in sys.argv:
        if option == '-a' or option == '--author':
            arguments['option'] = 'a'
        elif option == '-p' or option == '--publication':
            arguments['option'] = 'p'
        elif option == '-p' or option == '--help':
            arguments['option'] = 'h'
        elif option == '-y' or option == '--year':
            arguments['option'] = 'y'
            if len(sys.argv)>= 3:
                arguments['year1'] = sys.argv[2]

            if len(sys.argv) == 4:
                arguments['year2'] = sys.argv[3]


        else:
            arguments['option'] = 'b'

        if '-' not in sys.argv[-1] and 'books.py' not in sys.argv[-1]:
            arguments['string'] = sys.argv[-1]           
    
    main(arguments)
    return arguments

arguments = parse_command_line()