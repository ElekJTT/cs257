import sys
from booksdatasource import *

def main(arguments):

    datasource = BooksDataSource('books1.csv')


    if arguments['option'] == 'h':
        print(usage_statement)

    if arguments['option'] == 'b':
        if 'string' in arguments:
            print(datasource.books(self, arguments['string']))
        else:
            print(datasource.books(self))

    if arguments['option'] == 'a':
        if 'string' in arguments:
            print(datasource.authors(self, arguments['string']))
        else:
            print(datasource.authors(self))

    if arguments['option'] == 'p':
        if 'string' in arguments:
            print(datasource.books(self, arguments['string'], 'year'))
        else:
            print(datasource.books(self, None, 'year'))

    if arguments['option'] == 'y':

        if 'year1' in arguments:
            if 'year2' in arguments:
                print(datasource.books_between_years(self, arguments['year1'], arguments['year2']))
            else:
                print(datasource.books_between_years(self, arguments['year1']))
        else:
            if 'year2' in arguments:
                print(datasource.books_between_years(self, arguments['year2']))
            else:
                print(datasource.books_between_years(self))





def usage_statement():
    statement = f'Usage: book searching of various forms\n'
    return statement

def parse_command_line():
    arguments = {}

        #parsing args for between years command
        if sys.argv[1] == '--year' or sys.argv[1] == '-y':

            if len(sys.argv)>= 3:
                arguments['year1'] = sys.argv[2]

            if len(sys.argv) == 4:
                arguments['year2'] = sys.argv[3]

        
        #setting option to correct modifier
        else:
            for option in sys.argv:
                if option == '-a' or option == '--author':
                    arguments['option'] = 'a'
                elif option == '-p' or option == '--publication':
                    arguments['option'] = 'p'
                elif option == '-p' or option == '--help':
                    arguments['option'] = 'h'
                elif option == '-y' or option == '--year':
                    arguments['option'] = 'y'
                else:
                    arguments['option'] = 'b'
        
            if '-' not in sys.argv[-1]:
                arguments['string'] = sys.argv[-1]           
    
    return arguments

arguments = parse_command_line()