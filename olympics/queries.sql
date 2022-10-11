SELECT * FROM nocs
    ORDER BY abbreviation
;

SELECT DISTINCT athlete_name from athletes, nocs, games_representation
    WHERE athletes.id = games_representation.athlete_id
    AND nocs.id = games_representation.noc_id
    AND nocs.region = 'Jamaica' 
;

SELECT athletes.athlete_name, events.competition, events_results.medal, games.year from athletes, events, games, events_results
    WHERE athletes.id = events_results.athlete_id
    AND events.id = events_results.event_id
    AND games.id = events_results.games_id
    AND athletes.athlete_name LIKE '%Greg% %Louganis%'
    AND medal != 'NA'
    ORDER BY games.year
;

SELECT abbreviation, COUNT (medal) from nocs, nocs_medals
    WHERE nocs.id = nocs_medals.noc_id
    AND medal = 'Gold'
    GROUP BY abbreviation
;



