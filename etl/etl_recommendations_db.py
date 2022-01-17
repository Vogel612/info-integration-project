#!/bin/env python3

import re

STRING_PATTERN = re.compile("'.+?(?<!\\\\)'")
YEAR_PATTERN = re.compile("\\d{4}")

def parse_list(input):
    if not input:
        return []
    return (str(m.group()[1:-1]) for m in STRING_PATTERN.finditer(input))

def extract_years(input: str):
    if not input:
        return []
    return YEAR_PATTERN.findall(input)

def do_migration():
    import psycopg
    from psycopg.rows import dict_row
    with psycopg.connect("host=127.0.0.1 dbname=integrated_system user=postgres password=password", row_factory=dict_row) as conn:
        with conn.cursor() as cursor, conn.cursor() as update:
            cursor.execute("""SELECT title, genre, synopsis, type, producer,
                studio, rating, scored_by, popularity, episodes,
                source, aired FROM sources.recommendations_db;
            """)
            for row in cursor:
                genres = parse_list(row["genre"])
                producers = parse_list(row["producer"])
                studios = parse_list(row["studio"])

                genre_ids = []
                producer_ids = []
                studio_ids = []
                for studio in studios:
                    update.execute("SELECT id FROM result.studios WHERE studio LIKE %s", (studio,))
                    result = update.fetchone()
                    if not result:
                        update.execute("INSERT INTO result.studios(studio) VALUES (%s) RETURNING id", (studio,))
                        result = update.fetchone()
                    studio_ids.append(result["id"])

                for genre in genres:
                    update.execute("SELECT id FROM result.genres WHERE genre LIKE %s", (genre,))
                    result = update.fetchone()
                    if not result:
                        update.execute("INSERT INTO result.genres(genre) VALUES (%s) RETURNING id", (genre,))
                        result = update.fetchone()
                    genre_ids.append(result["id"])

                for producer in producers:
                    update.execute("SELECT id FROM result.producers WHERE producer LIKE %s", (producer,))
                    result = update.fetchone()
                    if not result:
                        update.execute("INSERT INTO result.producers(producer) VALUES (%s) RETURNING id", (producer,))
                        result = update.fetchone()
                    producer_ids.append(result["id"])

                years = extract_years(row["aired"])
                if len(years) == 0:
                    years = [None, None]
                elif len(years) == 1:
                    years.append(None)
                elif len(years) != 2:
                    print("Extracted too many years: %s from row %s" % (years, row["title"]))
                    raise ValueError
                update.execute("""INSERT INTO result.anime_titles(title, synopsis, media_type, score, scored_by,
                    popularity, number_of_episodes, start_year, finish_year, source) VALUES (%s, %s, %s, %s, %s, %s,
                     %s, %s, %s, %s) RETURNING id""", (row["title"], row["synopsis"], row["type"], row["rating"],
                     row["scored_by"], row["popularity"], row["episodes"], years[0], years[1], row["source"]))
                anime_id = update.fetchone()["id"]
                for mapping in studio_ids:
                    update.execute("INSERT INTO result.anime_titles_studios(anime_title_id, studio_id) VALUES (%s, %s)", (anime_id, mapping))
                for mapping in producer_ids:
                    update.execute("INSERT INTO result.anime_titles_producers(anime_title_id, producer_id) VALUES (%s, %s)", (anime_id, mapping))
                for mapping in genre_ids:
                    update.execute("INSERT INTO result.anime_titles_genres(anime_title_id, genre_id) VALUES (%s, %s)", (anime_id, mapping))

if __name__ == '__main__':
    do_migration()