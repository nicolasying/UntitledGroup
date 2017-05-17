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

CREATE TABLE Actor (
id INTEGER PRIMARY KEY UNIQUE AUTO_INCREMENT,
personnel_id INTEGER NOT NULL,
movie_id INTEGER NOT NULL ,
  FOREIGN KEY (movie_id) REFERENCES Movies(id),
  FOREIGN KEY (personnel_id) REFERENCES Personnel(personnel_id)
);

DROP TABLE Actor;

CREATE TABLE Personnel (
personnel_id INTEGER PRIMARY KEY UNIQUE AUTO_INCREMENT,
last_name varchar(30),
first_name VARCHAR(30)
);

ALTER TABLE Personnel ADD UNIQUE (last_name, first_name);

ALTER TABLE Actor ADD UNIQUE (personnel_id, movie_id);

SELECT id, title, year_dis, year FROM Movies WHERE title = 'Becoming Jane' or id = 45707;

SELECT movie_id, personnel_id FROM Actor WHERE movie_id = (SELECT id FROM Movies WHERE title = "Becoming Jane");

SELECT personnel_id FROM Personnel WHERE last_name = 'Hathaway' AND first_name = 'Anne';

SELECT movie_id, personnel_id FROM Actor WHERE personnel_id = 3126595;

SELECT id FROM Movies WHERE title = 'Becoming Jane' AND year_dis is null AND year = '2007';

START TRANSACTION;
DELETE FROM Personnel WHERE personnel_id NOT IN (SELECT DISTINCT personnel_id personnel_id FROM Actor);
COMMIT;

# SELECT COUNT(id) FROM Movies WHERE Movies.year IN (2015, 2016);
SELECT COUNT(id) FROM Movies WHERE Movies.country = "USA";

SELECT DISTINCT country FROM Movies;

SELECT COUNT( DISTINCT genre) FROM Genre;

SELECT DISTINCT genre FROM Genre;

SELECT genre, COUNT(DISTINCT movie_id) FROM Genre GROUP BY genre;

SELECT DISTINCT mpaa_rating FROM Movies;

SELECT count(id) FROM Movies WHERE imdb_rating IS NOT NULL AND year <= 2016 AND year >= 2000;

START TRANSACTION;
ROLLBACK;
ALTER TABLE Personnel ADD COLUMN name VARCHAR(120) AS (CONCAT_WS(' ', first_name, last_name));
ALTER TABLE Personnel ADD COLUMN ranking INT;

SELECT last_name FROM Personnel WHERE name = "Pom Klementieff";