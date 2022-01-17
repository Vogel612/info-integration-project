#!/bin/env python3

import re

STRING_PATTERN = re.compile("'.+?(?<!\\\\)'")

def parse_list(input: str):
    return (str(m.group()[1:-1]) for m in STRING_PATTERN.finditer(input))

def do_migration():
    import psycopg
    from psycopg.rows import dict_row
    with psycopg.connect("host=127.0.0.1 dbname=integrated_system user=postgres password=password", row_factory=dict_row) as conn:
        with conn.cursor() as cursor, conn.cursor() as update:
            cursor.execute("""SELECT title, media_type, eps, duration, ongoing,
                start_yr, finish_yr, release_season, description, studios, tags,
                content_warn, rating, votes FROM sources.animeplanet;
            """)
            for row in cursor:
                studios = parse_list(row["studios"])
                cws = parse_list(row["content_warn"])
                genres = parse_list(row["tags"])

                studio_ids = []
                cw_ids = []
                genre_ids = []
                for studio in studios:
                    update.execute("SELECT id FROM result.studios WHERE studio LIKE %s", (studio,))
                    result = update.fetchone()
                    if not result:
                        update.execute("INSERT INTO result.studios(studio) VALUES (%s) RETURNING id", (studio,))
                        result = update.fetchone()
                    studio_ids.append(result["id"])
                
                for cw in cws:
                    update.execute("SELECT id FROM result.content_warnings WHERE warning LIKE %s", (cw,))
                    result = update.fetchone()
                    if not result:
                        update.execute("INSERT INTO result.content_warnings(warning) VALUES (%s) RETURNING id", (cw,))
                        result = update.fetchone()
                    cw_ids.append(result["id"])
                
                for genre in genres:
                    update.execute("SELECT id FROM result.genres WHERE genre LIKE %s", (genre,))
                    result = update.fetchone()
                    if not result:
                        update.execute("INSERT INTO result.genres(genre) VALUES (%s) RETURNING id", (genre,))
                        result = update.fetchone()
                    genre_ids.append(result["id"])

                update.execute("""INSERT INTO result.anime_titles(title, synopsis, duration_in_minutes,
                    number_of_episodes, media_type, score, scored_by, start_year, finish_year, season_of_release) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id""",
                        (row["title"], row["description"], row["duration"], row["eps"], row["media_type"],
                        row["rating"] * 2, row["votes"], row["start_yr"], row["finish_yr"], row["release_season"]))
                anime_id = update.fetchone()["id"]
                for mapping in cw_ids:
                    update.execute("INSERT INTO result.anime_titles_content_warnings(anime_title_id, content_warning_id) VALUES (%s, %s)", (anime_id, mapping))
                for mapping in studio_ids:
                    update.execute("INSERT INTO result.anime_titles_studios(anime_title_id, studio_id) VALUES (%s, %s)", (anime_id, mapping))
                for mapping in genre_ids:
                    update.execute("INSERT INTO result.anime_titles_genres(anime_title_id, genre_id) VALUES (%s, %s)", (anime_id, mapping))

if __name__ == '__main__':
    do_migration()
