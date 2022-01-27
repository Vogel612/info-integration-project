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
    popularity FLOAT,
    members FLOAT,
    episodes INT,
    source TEXT,
    aired TEXT,
    link TEXT
);