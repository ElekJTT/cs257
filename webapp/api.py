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

@api.route('/top100/<year>')
def get_songs_from_year(year):
    ''' Returns a list of all the songs for a particular year in our database.

        By default, the list is presented in alphabetical order
        by surname, then given_name. You may, however, use
        the GET parameter sort to request sorting by birth year.

        Returns an empty list if there's any database failure.
    '''
    query = '''SELECT title, artist_name, rank
               FROM songs, artists, artists_songs, songs_years
               WHERE year = %s
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
    if parameter == "artists":
        query = '''SELECT artist_name FROM artists
                   WHERE artist_name ILIKE CONCAT('%%', %s, '%%')  '''

    elif parameter == "songs":
        query = '''SELECT title, artist_name
                   FROM songs, artists, artists_songs
                   WHERE songs.id = artists_songs.song_id
                   AND artists.id = artists_songs.artist_id
                   AND songs.title ILIKE CONCAT('%%', %s, '%%')
                '''

    elif parameter == "lyrics":
        query = '''SELECT title, artist_name
                   FROM songs, artists, artists_songs
                   WHERE songs.id = artists_songs.song_id
                   AND artists.id = artists_songs.artist_id
                   AND songs.lyrics ILIKE CONCAT('%%', %s, '%%')
                '''
    else:
        return

    result_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (search_text,))
        for row in cursor:
            if parameter == "artist":
                result = {'artist_name':row[0]}
            else:
                result = {'title':row[0], 'artist_name':row[1]}
            result_list.append(result)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    if(result_list):
        return json.dumps(result_list)
    else:
        result_list.append({'artist_name':'Miley Cyrus'})
        return json.dumps(result_list)

@api.route('/artist/<artist>')
def get_artist_songs(artist):
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
        cursor.execute(query, (artist,))
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
def get_song_info(artist, song):

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
        cursor.execute(query, (song, artist))
        for row in cursor:
            song_info = {'title':row[0],
                    'artist_name':row[1],
                    'year':row[2],
                    'rank':row[3],
                    'lyrics':row[4]}
            song_list.append(song_info)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(song_list)

@api.route('/help')
def get_help():
    help_string = '''Request:/
    Response: A JSON list of artists/songs for the most recent year in the database

    Request:/search/<parameter>/<search_text>
    Response: Parameter can be artists, songs, or lyrics
        If the parameter is artists, return a JSON list containing artists whose names contain the search text
        If the parameter is songs, return a JSON list containing songs whose titles contain the search text
        If the parameter is lyrics, return a JSON list containing songs whose lyrics contain the search text

    Request:/years
    Response: A JSON list of all the years in the database, descending order.

    Request:/top100/<year>
    Response: A JSON list of the top 100 songs from the <year>

    Request: /artist/<artist>
    Response: A JSON list, representing a specific <artist>, of song dictionaries with the song title, rank, and year.
        Title-- (string) the name of the song
        Rank-- (int) the rank the song achieved in the year
        Year-- (int) the year the song placed in the top 100 songs

    Request: /artist/<artist>/song/<song>
    Response: A JSON dictionary with each item representing a song containing, in order, the title of the song, artist, year, rank, lyrics
     	Artist-- (string) the name of the artist
        Title-- (string) the name of the song
    	Lyrics– (string) the lyrics of the song
    	Year– (int) the year the song made top 100
    	Rank– (int) the rank the song achieved

    '''
    return help_string
