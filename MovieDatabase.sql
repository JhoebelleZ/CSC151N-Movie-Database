CREATE TABLE IF NOT EXISTS Movies(
    Movie_id INTEGER(5) NOT NULL PRIMARY KEY,
    Title VARCHAR(50) NOT NULL ,
    Synopsis TEXT(500) NOT NULL ,
    Movie_Duration INTEGER(4) NOT NULL ,
    Year_Released INTEGER(4) NOT NULL ,
    Photo VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Directors(
    Director_ID INTEGER(5) PRIMARY KEY NOT NULL ,
    Firstname VARCHAR(50) NOT NULL ,
    Lastname VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Production(
    Production_ID INTEGER(5) PRIMARY KEY NOT NULL ,
    Production_Name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Actors(
    Actor_ID INTEGER(5) PRIMARY KEY NOT NULL ,
    Screen_Name VARCHAR(50) NOT NULL
);


CREATE TABLE IF NOT EXISTS Acts(
  Actor_ID INTEGER(5) NOT NULL ,
  Movie_ID INTEGER(5) NOT NULL ,
  Character_Name VARCHAR(50) NOT NULL ,
  PRIMARY KEY (Actor_ID, Movie_ID),
  FOREIGN KEY (Actor_ID) REFERENCES Actors(Actor_ID) ON UPDATE CASCADE ON DELETE CASCADE ,
  FOREIGN KEY (Movie_ID) REFERENCES Movies(Movie_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Directs(
    Movie_ID INTEGER(5) NOT NULL ,
    Director_ID INTEGER(5) NOT NULL ,
    PRIMARY KEY (Movie_ID, Director_ID),
    FOREIGN KEY (Movie_ID) REFERENCES Movies(Movie_id) ON UPDATE CASCADE ON DELETE CASCADE ,
    FOREIGN KEY (Director_ID) REFERENCES Directors(Director_ID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Owns(
    Movie_ID INTEGER(5) NOT NULL ,
    Production_ID INTEGER(5) NOT NULL ,
    PRIMARY KEY (Movie_ID, Production_ID),
    FOREIGN KEY (Movie_ID) REFERENCES Movies(Movie_id) ON UPDATE CASCADE ON DELETE CASCADE ,
    FOREIGN KEY (Production_ID) REFERENCES Production(Production_ID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Genre(
    Movie_ID INTEGER(5) NOT NULL ,
    Genre VARCHAR(50) NOT NULL ,
    PRIMARY KEY (Movie_ID, Genre),
    FOREIGN KEY (Movie_ID) REFERENCES Movies(Movie_id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- INSERT INTO Movies (Movie_ID, Title, Synopsis, Movie_Duration, Year_Released, Photo)
-- VALUES (001, 'Cruella', 'Estella is a young and clever grifter whos determined to make a name for herself in the fashion world. She soon meets a pair of thieves who appreciate her appetite for mischief, and together they build a life for themselves on the streets of London. However, when Estella befriends fashion legend Baroness von Hellman, she embraces her wicked side to become the raucous and revenge-bent Cruella.',
--         134, 2021,  'movies/Cruella.jpg'),
--     (002, 'Raya and the Last Dragon',  'Raya, a warrior, sets out to track down Sisu, a dragon, who transferred all her powers into a magical gem which is now scattered all over the kingdom of Kumandra, dividing its people.', 117, 2021, 'movies/RayaAndTheLastDragon.jpg'),
-- 	(003, 'Godzilla vs. Kong', 'King Kong is transported out of his containment zone after Godzilla resurfaces and creates mayhem. Humans need his help to reach Hollow Earth and find a way to subdue the king of monsters.',
-- 	113, 2021, 'movies/GodzillavsKong.jpeg');
--
-- INSERT INTO Directors VALUES (1, 'Craig', 'Gillespie'), (2, 'Carlos', ' López Estrada'), (3, 'Don', 'Hall'),
--                              (4, 'Adam', 'Wingard');
--
-- INSERT INTO Directs VALUES (1,1), (2,2), (2,3), (3,4);
--
-- INSERT INTO Actors VALUES (1, 'Emma Stone'),
--                           (2, 'Emma Thompson'),
--                           (3, 'Joel Fry'),
--                           (4, 'Mark Strong');
--
-- INSERT INTO Acts VALUES (1, 1, 'Cruella'),
--                         (2, 1, 'The Baroness'),
--                         (3, 1, 'Jasper'),
--                         (4, 1, 'John the Valet');
--
-- INSERT INTO Owns VALUES (1,1), (1,2), (1,3);
--
-- INSERT INTO Genre VALUES (1, 'Crime'), (1, 'Comedy'), (2, 'Animation'),
--                          (2, 'Action'), (2, 'Adventure'), (3, 'Sci-Fi'),
--                          (3, 'Action');

