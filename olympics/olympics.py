'''
olypmics.py written by Elek Thomas-Toth for assignment due 10.20.2022

 '''
import sys
import config
import psycopg2


def main(arguments):
    if arguments['option'] == 'h':
        usage_statement()

    elif arguments['option'] == 'a':
        for row in get_matching_athletes(arguments['string']):
            print(row)

    elif arguments['option'] == 'l':
        for row in get_noc_medals():
            print(row)

    elif arguments['option'] == 'w':
        for row in get_winningest():
            print(row)



def usage_statement():

    with open("usage.txt") as help:
        print(help.read())

def parse_command_line():
    arguments = {}


    
    #setting option to correct modifier
    for option in sys.argv:
        if option == '-a' or option == '--athlete':
            arguments['option'] = 'a'
            break
        elif option == '-w' or option == '--winningest':
            arguments['option'] = 'w'
            break
        elif option == '-h' or option == '--help':
            arguments['option'] = 'h'
            break
        else:
            arguments['option'] = 'l'

    if '-' not in sys.argv[-1] and 'olympics.py' not in sys.argv[-1]:
            arguments['string'] = sys.argv[-1]           
    
    main(arguments)
    return arguments


def get_connection():
    ''' Returns a database connection object with which you can create cursors,
        issue SQL queries, etc. This function is extremely aggressive about
        failed connections--it just prints an error message and kills the whole
        program. Sometimes that's the right choice, but it depends on your
        error-handling needs. '''
    try:
        return psycopg2.connect(database=config.database,
                                user=config.user,
                                password=config.password)
    except Exception as e:
        print(e, file=sys.stderr)
        exit()


def get_matching_athletes(noc):
    ''' Returns a list of the full names of all athletes in the database
        who competed for the specified NOC'''
    athletes = []
    try:
        query = '''SELECT DISTINCT athlete_name
                   FROM athletes, nocs, games_representation
                   WHERE nocs.abbreviation = %s
                   AND athletes.id = games_representation.athlete_id
                   AND nocs.id = games_representation.noc_id                   
                '''
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (noc,))
        for row in cursor:
            athlete_name = row[0]
            athletes.append(f'{athlete_name}')

    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return athletes

def get_noc_medals():
    ''' Returns a list of all nocs and how many gold medals they have won, sorted
        decreasing number of gold medals'''
    nocs = []
    try:
        # Create a "cursor", which is an object with which you can iterate
        # over query results.
        connection = get_connection()
        cursor = connection.cursor()

        # Execute the query
        query = '''SELECT abbreviation, COUNT (medal) from nocs, nocs_medals
                    WHERE nocs.id = nocs_medals.noc_id
                    AND nocs_medals.medal = 'Gold'
                    GROUP BY abbreviation 
                    ORDER BY COUNT(nocs_medals.medal) DESC      
                '''
        cursor.execute(query)

        # Iterate over the query results to produce the list of author names.
        for row in cursor:
            noc = row[0]
            medals = row[1]
            nocs.append(f'{noc}, {medals}')

    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return nocs

def get_winningest():
    ''' Returns a list of the 10 athletes who won the most gold medals
        sorted in descending order of medals'''
    athletes = []
    try:
        query = '''SELECT athlete_name, COUNT (events_results.medal) 
                   FROM athletes, events_results
                   WHERE athletes.id = events_results.athlete_id
                   AND events_results.medal = 'Gold'
                   GROUP BY athlete_name
                   ORDER BY COUNT(events_results.medal) DESC
                   Limit 10
                   '''
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        for row in cursor:
            athlete_name = row[0]
            num_medals = row[1]
            athletes.append(f'{athlete_name}, {num_medals}')

    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return athletes

arguments = parse_command_line()
