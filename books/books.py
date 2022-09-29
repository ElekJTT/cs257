import sys
from booksdatasource import *

def main(arguments):
    print(usage_statement) #temp

   # sys.argv... blah blah blah 
    datasource = BooksDataSource('books1.csv')

def usage_statement():
    statement = f'Usage: book searching of various forms\n'
    return statement

def parse_command_line():
    arguments = {}

        #parsing for between years command
        if sys.argv[1] == year:

            if len(sys.argv)>= 3:
                arguments['year1'] = sys.argv[2]

            if len(sys.argv) == 4:
                arguments['year2'] = sys.argv[3]

        
        #parsing for any other options
        else:
            arguments['option'] = sys.argv[1]

#.contains?
            if arguments['option'] == 'a' or arguments['options'] == 'author'

            if arguments['option'] == 'h' or arguments['options'] == 'help'

            if arguments['option'] == 'p' or arguments['options'] == 'publication'


            
    
    return arguments

arguments = parse_command_line()