CREATE TABLE songs(
	id SERIAL,
	title text,
	lyrics text
);

CREATE TABLE artists(
	id SERIAL
	name text
	
);
CREATE TABLE years(
	id int
);

CREATE TABLE artists_songs(
	artist_id int,
	song_id int,
);

CREATE TABLE songs_years(
	song_id int,
	year_id int, 
	rank int
);
