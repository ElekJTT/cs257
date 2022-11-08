"""
Convert.py written by Elek Thomas-Toth for Jeff Ondich project due 10/11/2022

Olympics data taken from https://www.kaggle.com/heesoo37/120-years-of-olympic-history-athletes-and-results

"""
from asyncore import write
from dataclasses import asdict
import csv

from xml.sax import default_parser_list



songs_dict = {}
artists_dict= {}

with open ("billboard_lyrics_1964-2015.csv", 'r', encoding= 'latin-1') as reader:
    data = csv.reader(reader, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
    header = next(data)

    with open('artists.csv', 'w', newline='') as output_one:
        artists = csv.writer(output_one)
        with open('songs.csv', 'w', newline='') as output_two:
            songs = csv.writer(output_two)
            with open("artists_songs.csv", 'w') as output_three:
                artists_songs = csv.writer(output_three)
                with open("songs_years.csv", 'w') as output_four:
                    songs_years = csv.writer(output_four)
                    for dataList in data:
                        rank = int(dataList[0])
                        song_title = str(dataList[1])
                        artist_name = str(dataList[2])
                        year = str(dataList[3])
                        lyrics = str(dataList[4])
                        
                        if song_title not in songs_dict:
                            song_id = len(songs_dict) + 1
                            songs_dict[song_title] = song_id
                            songs.writerow([song_id, song_title, lyrics])

                        if artist_name not in artists_dict:
                            artist_id = len(artists_dict) + 1
                            artists_dict[artist_name] = artist_id
                            artists.writerow([artist_id, artist_name])

                        artists_songs.writerow([artists_dict[artist_name], songs_dict[song_title]])
                        songs_years.writerow([songs_dict[song_title], year, rank])


                

                
            











                            

                            





