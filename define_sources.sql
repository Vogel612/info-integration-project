--CREATE DATABASE integrated_system
--    OWNER 'postgres'
--    LOCALE 'en_US.utf8';
-- assume we are connected to the integrated_system database
CREATE SCHEMA IF NOT EXISTS sources;
CREATE TABLE IF NOT EXISTS sources.animeplanet (
    aid INT GENERATED ALWAYS AS IDENTITY,
    title TEXT,
    media_type TEXT,
    eps INT,
    duration TEXT,
    ongoing TEXT,
    start_yr TEXT,
    finish_yr TEXT,
    release_season TEXT,
    description TEXT,
    studios TEXT,
    tags TEXT,
    content_warn TEXT,
    watched INT,
    watching INT,
    want_watch INT,
    dropped INT,
    rating FLOAT,
    votes FLOAT
);

CREATE TABLE IF NOT EXISTS sources.mal_anime (
    anime_id INT PRIMARY KEY,
    name TEXT,
    genre TEXT,
    type TEXT,
    episodes TEXT,
    rating FLOAT,
    members INT
);
CREATE TABLE IF NOT EXISTS sources.mal_ratings (
    user_id INT,
    anime_id INT,
    rating INT
);

CREATE TABLE IF NOT EXISTS sources.anime_data (
    aid INT GENERATED ALWAYS AS IDENTITY,
    title TEXT,
    type TEXT,
    episodes TEXT, -- because if no episode information is available we have "-"
    status TEXT,
    start_airing TEXT,
    end_airing TEXT,
    release_season TEXT,
    broadcast_slot TEXT,
    producers TEXT,
    licensors TEXT,
    studios TEXT,
    sources TEXT,
    genres TEXT,
    duration TEXT,
    esrb_rating TEXT,
    score FLOAT,
    scored_by INT,
    members INT,
    favorites INT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS sources.recommendations_db (
    anime_id INT,
    title TEXT,
    genre TEXT,
    synopsis TEXT,
    type TEXT,
    producer TEXT,
    studio TEXT,
    rating FLOAT,
    scored_by INT,
    popularity INT,
    members FLOAT,
    episodes INT,
    source TEXT,
    aired TEXT,
    link TEXT
);


SELECT COUNT(*) = 0 AS e FROM sources.animeplanet;
\gset
\if :e
    \copy sources.animeplanet(title, media_type, eps, duration, ongoing, start_yr, finish_yr, release_season, description, studios, tags, content_warn, watched, watching, want_watch, dropped, rating, votes) FROM '/home/vogel612/Documents/Uni/Master/current/InformationIntegration/project/datasets/animeplanet.csv' DELIMITER ',' CSV HEADER;
\endif

SELECT COUNT(*) = 0 AS e FROM sources.mal_anime;
\gset
\if :e
    \copy sources.mal_anime FROM '/home/vogel612/Documents/Uni/Master/current/InformationIntegration/project/datasets/myanimelist.csv' DELIMITER ',' CSV HEADER;
\endif

SELECT COUNT(*) = 0 AS e FROM sources.mal_ratings;
\gset
\if :e
    \copy sources.mal_ratings FROM '/home/vogel612/Documents/Uni/Master/current/InformationIntegration/project/datasets/mal_rating.csv' DELIMITER ',' CSV HEADER;
\endif

SELECT COUNT(*) = 0 AS e FROM sources.anime_data;
\gset
\if :e
    \copy sources.anime_data(title, type, episodes, status, start_airing, end_airing, release_season, broadcast_slot, producers, licensors, studios, sources, genres, duration, esrb_rating, score, scored_by, members, favorites, description) FROM '/home/vogel612/Documents/Uni/Master/current/InformationIntegration/project/datasets/dataanime.csv' DELIMITER ',' CSV HEADER;
\endif

SELECT COUNT(*) = 0 AS e FROM sources.recommendations_db;
\gset
\if :e
    \copy sources.recommendations_db FROM '/home/vogel612/Documents/Uni/Master/current/InformationIntegration/project/datasets/recommendation_data.csv' DELIMITER ',' CSV HEADER;
\endif