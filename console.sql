CREATE TABLE Movies (
id INTEGER PRIMARY KEY AUTO_INCREMENT,
title varchar(250) NOT NULL,
year_dis VARCHAR(10) DEFAULT NULL,
year integer NOT NULL,
budget integer,
length integer,
imdb_rating float,
mpaa_rating varchar(5),
genre varchar(80),
language varchar(30),
country varchar(30),
actor_rating float,
  UNIQUE (title, year_dis, year)
);

CREATE INDEX titleyear on Movies (title, year_dis, year);

CREATE INDEX titleyear_2 on Movies (title, year);

ALTER TABLE Movies CONVERT TO CHARACTER SET utf8mb4;

SELECT title, year from Movies WHERE title = 'Deus ex Machina';

ALTER DATABASE movie_db CHARACTER SET utf8 COLLATE utf8_bin;

DELETE FROM Movies WHERE length is NULL;

SELECT title, year_dis, year FROM Movies WHERE year_dis IS NOT NULL;

SELECT COUNT(id) FROM Movies WHERE budget IS NOT NULL AND year_dis IS NOT NULL;

UPDATE Movies SET .Movies.budget = 28000000 WHERE title = '30 Minutes or Less' and year = 2011;

ALTER TABLE Movies ADD COLUMN vote INTEGER DEFAULT NULL;

CREATE TABLE Countries (
id INTEGER PRIMARY KEY AUTO_INCREMENT,
country varchar(30),
movie_id INTEGER NOT NULL ,
  FOREIGN KEY (movie_id) REFERENCES Movies(id)
);

CREATE TABLE Language (
id INTEGER PRIMARY KEY UNIQUE,
language varchar(30),
movie_id INTEGER NOT NULL ,
  FOREIGN KEY (movie_id) REFERENCES Movies(id)
);

SELECT title FROM Movies WHERE id = 345;

INSERT INTO Countries(.Countries.movie_id, .Countries.country) VALUES ((SELECT id FROM Movies WHERE title = 'Deus Ex Machina' AND year_dis = 'I'), 'China');

CREATE TABLE Genre (
id INTEGER PRIMARY KEY UNIQUE,
genre varchar(30),
movie_id INTEGER NOT NULL ,
  FOREIGN KEY (movie_id) REFERENCES Movies(id)
);

SELECT title, year, year_dis FROM Movies WHERE title = 'Dark Side';

SELECT DISTINCT Language.language FROM Language