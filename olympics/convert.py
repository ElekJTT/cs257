"""
Convert.py written by Elek Thomas-Toth for Jeff Ondich project due 10/11/2022

Olympics data taken from https://www.kaggle.com/heesoo37/120-years-of-olympic-history-athletes-and-results

"""
from asyncore import write
from dataclasses import asdict
import csv

from xml.sax import default_parser_list



athletes_dict = {}
events_dict = {}
games_dict = {}
nocs_dict = {}

#populate main tables (athletes, events, games, and their dictionaries)
with open ("athlete_events.csv", 'r') as reader:
    data = csv.reader(reader, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
    header = next(data)

    with open('athletes.csv', 'w', newline='') as output_one:
        athletes = csv.writer(output_one)
        with open('events.csv', 'w', newline='') as output_two:
            events = csv.writer(output_two)
            with open('games.csv', 'w', newline='') as output_three:
                games = csv.writer(output_three)
                for dataList in data:
                    athlete_id = int(dataList[0])
                    athlete_name = str(dataList[1])
                    sex = str(dataList[2])
                    team = str(dataList[6])
                    noc = str(dataList[7])
                    games_name = str(dataList[8])
                    year = int(dataList[9])
                    season = str(dataList[10])
                    city = str(dataList[11])
                    sport = str(dataList[12])
                    event_name = str(dataList[13])
                    medal = str(dataList[14])

                    if athlete_id not in athletes_dict:
                        
                            athletes_dict[athlete_id] = athlete_name
                            athletes.writerow([athlete_id, athlete_name, sex])

                    if event_name not in events_dict:
                        event_id = len(events_dict) + 1
                        events_dict[event_name] = event_id
                        events.writerow([event_id, sport, event_name])

                    if games_name not in games_dict:
                        games_id = len(games_dict) + 1
                        games_dict[games_name] = games_id
                        games.writerow([games_id, year, season, city])

#populate nocs table and dict
with open('noc_regions.csv', 'r') as input:
    with open('nocs.csv', 'w', newline='') as output:
        reader = csv.reader(input)
        writer = csv.writer(output)
        header = next(reader)
        for row in reader:
            noc_id = len(nocs_dict) + 1
            abrv = row[0]
            region = row[1]
            nocs_dict[abrv] = noc_id
            writer.writerow([noc_id, abrv, region])
            
        #linking tables

#populate events_results (plundered from Jeff Ondich)
with open('athlete_events.csv') as input:
    with open('events_results.csv', 'w', newline='') as output:
        reader = csv.reader(input)
        writer = csv.writer(output)
        header = next(reader)
        for row in reader:
            athlete_id = row[0]
            event_name = row[13]
            event_id = events_dict[event_name]
            games = row[8]
            games_id = games_dict[games]
            medal = row[14]

            age = row[3]
            if(age == 'NA'):
                age = -1
            height = row[4]
            if(height == 'NA'):
                height = -1
            weight = row[5]
            if(weight == 'NA'):
                weight = -1

            writer.writerow([athlete_id, event_id, games_id, medal, age, int(float(height)), int(float(weight))])



#populate games_representation
with open('athlete_events.csv', 'r') as input:
    with open('games_representation.csv', 'w', newline='') as output:
        reader = csv.reader(input)
        writer = csv.writer(output)
        header = next(reader)
        for row in reader:
            athlete_id = row[0]
            noc = row[7]
            noc_id = nocs_dict[noc]
            games = row[8]
            games_id = games_dict[games]
            writer.writerow([games_id, athlete_id, noc_id])
            


#populate nocs_medals
with open('athlete_events.csv') as input:
    with open('nocs_medals.csv', 'w', newline='') as output:
        reader = csv.reader(input)
        writer = csv.writer(output)
        header = next(reader)
        for row in reader:
            medal = row[14]
            athlete_id = row[0]
            noc = row[7]
            noc_id = nocs_dict[noc]
            writer.writerow([noc_id, athlete_id, medal])







                
"""  with open('athletes_medals.csv', 'a') as athelete_medals:
    athelete_medals.write()

with open('athletes_events.csv', 'a') as athlete_events:
    athlete_events.write()

with open('athletes_nocs.csv', 'a') as athletes_noc:
    athletes_noc.write()

with open('games_athletes.csv', 'a') as games_athletes:
    games_athletes.write()

with open('games_nocs.csv', 'a') as games_nocs:
    games_nocs.write()

with open('nocs_medals.csv', 'a') as nocs_medals:
    nocs_medals.write() 


         """









                            

                            





