'''
    api.py
    Ariana Borlak, Elek Thomas-Toth

    Tiny Flask API
'''
import sys
import flask
import json
import config
import psycopg2

api = flask.Blueprint('api', __name__)

def get_connection():
    ''' Returns a connection to the database described in the
        config module. May raise an exception as described in the
        documentation for psycopg2.connect. '''
    return psycopg2.connect(database=config.database,
                            user=config.user,
                            password=config.password)

@api.route('/year/<year>')
def get_songs_from_year(year):
    ''' Returns a list of all the songs for a particular year in our database.

        By default, the list is presented in alphabetical order
        by surname, then given_name. You may, however, use
        the GET parameter sort to request sorting by birth year.

            http://.../authors/?sort=birth_year

        Returns an empty list if there's any database failure.
    '''
    query = '''SELECT title, artist_name, rank
               FROM songs, artists, artists_songs, songs_years
               WHERE year = 2015
               AND artists.id = artists_songs.artist_id
               AND songs.id = artists_songs.song_id
               AND songs.id = songs_years.song_id
               ORDER BY rank'''

    song_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (year,))
        for row in cursor:
            song = {'title':row[0],
                    'artist_name':row[1],
                    'rank':row[2]}
            song_list.append(song)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(song_list)

# @api.route('/books/author/<author_id>')
# def get_books_for_author(author_id):
#     query = '''SELECT books.id, books.title, books.publication_year
#                FROM books, authors, books_authors
#                WHERE books.id = books_authors.book_id
#                  AND authors.id = books_authors.author_id
#                  AND authors.id = %s
#                ORDER BY books.publication_year'''
#     book_list = []
#     try:
#         connection = get_connection()
#         cursor = connection.cursor()
#         cursor.execute(query, (author_id,))
#         for row in cursor:
#             book = {'id':row[0], 'title':row[1], 'publication_year':row[2]}
#             book_list.append(book)
#         cursor.close()
#         connection.close()
#     except Exception as e:
#         print(e, file=sys.stderr)
#
#     return json.dumps(book_list)
#
