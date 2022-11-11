'''
    api.py
    Ariana Borlak, Elek Thomas-Toth

    Flask API
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

@api.route('/years')
def get_years():
    ''' Returns a list of all the years in the database
    '''
    query = '''SELECT DISTINCT year
               FROM songs_years
               ORDER BY year DESC
            '''
    year_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, tuple())
        for row in cursor:
            year = {'year': row[0]}
            year_list.append(year)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(year_list)

@api.route('/years/<year>')
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

@api.route('/search/<parameter>/<search_text>')
def search_with_parameter(parameter, search_text):
    if parameter == "Artists":
        query = '''SELECT artist_name FROM authors
                   WHERE artist_name LIKE %s '''

    elif parameter == "Songs":
        query = '''SELECT title, artist_name
                   FROM songs, artists, artists_songs
                   WHERE songs.id = artists_songs.song_id
                   AND artists.id = artists_songs.artist_id
                   AND songs.title LIKE %s
                '''

    elif parameter == "Lyrics":
        query = '''SELECT title, artist_name
                   FROM songs, artists, artists_songs
                   WHERE songs.id = artists_songs.song_id
                   AND artists.id = artists_songs.artist_id
                   AND songs.lyrics LIKE %s
                '''
    else:
        return

    result_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (search_text,))
        for row in cursor:
            if parameter == "Artist":
                result = {'title':row[0], 'artist_name':row[1]}
            else:
                result = {'artist_name':row[0]}
            result_list.append(result)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)
    return json.dumps(result_list)

@api.route('/artist/<artist>')
def get_artist_songs(artist_name):
    query = '''SELECT title, rank, year
               FROM songs, artists, artists_songs, songs_years
               WHERE artist_name = %s
               AND artists.id = artists_songs.artist_id
               AND songs.id = artists_songs.song_id
               AND songs.id = songs_years.song_id
               ORDER BY rank'''

    song_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (artist_name,))
        for row in cursor:
            song = {'title':row[0],
                    'rank':row[1],
                    'year':row[2]}
            song_list.append(song)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(song_list)

@api.route('/artist/<artist>/song/<song>')
def get_song_info(artist_name, title):

    query = '''SELECT title, artist_name, year, rank, lyrics
               FROM songs, artists, artists_songs, songs_years
               WHERE title = %s
               AND artist_name = %s
               AND artists.id = artists_songs.artist_id
               AND songs.id = artists_songs.song_id
               AND songs.id = songs_years.song_id
               ORDER BY rank'''

    song_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (title, artist_name))
        for row in cursor:
            song = {'title':row[0],
                    'artist_name':row[1],
                    'year':row[2],
                    'rank':row[3],
                    'lyrics':row[4]}
            song_list.append(song)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(song_list)