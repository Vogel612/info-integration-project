#!/bin/env python3

import re
import psycopg
from psycopg.rows import dict_row

STRING_PATTERN = re.compile("'.+?(?<!\\\\)'")

def parse_list(input: str):
    if not input:
        return ""
    return (str(m.group()[1:-1]) for m in STRING_PATTERN.finditer(input))

def do_migration():
    with psycopg.connect("host=127.0.0.1 dbname=integrated_system user=postgres password=password", row_factory=dict_row) as conn:
        with conn.cursor() as cursor, conn.cursor() as update:
            cursor.execute("""SELECT name, genre, type, episodes, rating FROM sources.mal_anime;""")
            for row in cursor:
                genres = parse_list(row["genre"])
                genre_ids = []

                for genre in genres:
                    update.execute("SELECT id FROM result.genres WHERE genre LIKE %s", (genre,))
                    result = update.fetchone()
                    if not result:
                        update.execute("INSERT INTO result.genres(genre) VALUES (%s) RETURNING id", (genre,))
                        result = update.fetchone()
                    genre_ids.append(result["id"])

                update.execute("""INSERT INTO result.anime_titles
                (title, number_of_episodes, media_type, score) 
                VALUES (%s, %s, %s, %s) RETURNING id""",
                (row["name"], row["episodes"] if row["episodes"] != "Unknown" else None, row["type"], row["rating"]))
                anime_id = update.fetchone()["id"]

                for mapping in genre_ids:
                    update.execute("INSERT INTO result.anime_titles_genres(anime_title_id, genre_id) VALUES (%s, %s)", (anime_id, mapping))

if __name__ == '__main__':
    do_migration()
