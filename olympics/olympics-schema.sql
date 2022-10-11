
CREATE TABLE athletes (
    id SERIAL,
    athlete_name text,
    sex text

);

CREATE TABLE nocs (
    id SERIAL,
    abbreviation text,
    region text
);

CREATE TABLE events (
    id SERIAL,
    sport text,
    competition text
);


CREATE TABLE games (
    id SERIAL,
    year integer,
    season text,
    city text
);


CREATE TABLE events_results (
    athlete_id integer,
    event_id integer,
    games_id integer,
    medal text,
    age integer,
    height integer,
    mass integer
    
);

CREATE TABLE games_representation (
    games_id integer,
    athlete_id integer,
    noc_id integer
);

CREATE TABLE nocs_medals (
    noc_id integer,
    athlete_id integer,
    medal text
);