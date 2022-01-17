CREATE SCHEMA IF NOT EXISTS result;

CREATE TABLE IF NOT EXISTS result.content_warnings(
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    warning TEXT
);
CREATE TABLE IF NOT EXISTS result.producers(
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    producer TEXT
);
CREATE TABLE IF NOT EXISTS result.genres(
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    genre TEXT
);
CREATE TABLE IF NOT EXISTS result.studios(
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    studio TEXT
);
-- Skipping Licensors, because lack of interest
CREATE TABLE IF NOT EXISTS result.anime_titles(
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    title TEXT NOT NULL,
    synopsis TEXT,
    duration_in_minutes INT,
    number_of_episodes INT,
    media_type TEXT,
    score DECIMAL(4,2),
    scored_by INT,
    popularity INT,
    source text,
    start_year INT,
    finish_year INT,
    season_of_release TEXT,
    esrb_rating TEXT,
    broadcast_time TIME
);

CREATE TABLE IF NOT EXISTS result.anime_titles_content_warnings(
    anime_title_id INT REFERENCES result.anime_titles(id),
    content_warning_id INT REFERENCES result.content_warnings(id)
);

CREATE TABLE IF NOT EXISTS result.anime_titles_producers(
    anime_title_id INT REFERENCES result.anime_titles(id),
    producer_id INT REFERENCES result.producers(id)
);

CREATE TABLE IF NOT EXISTS result.anime_titles_genres(
    anime_title_id INT REFERENCES result.anime_titles(id),
    genre_id INT REFERENCES result.genres(id)
);

CREATE TABLE IF NOT EXISTS result.anime_titles_studios(
    anime_title_id INT REFERENCES result.anime_titles(id),
    studio_id INT REFERENCES result.studios(id)
);

