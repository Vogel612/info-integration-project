#!/bin/env python3

import re
import psycopg
from psycopg.rows import dict_row

STRING_PATTERN = re.compile("'.+?(?<!\\\\)'")
DURATION_PATTERN = "^((?P<hours>\\d+) hr\\.)?( ?(?P<minutes>\\d+) min\\.)?$"

def parse_list(input: str):
    return (str(m.group()[1:-1]) for m in STRING_PATTERN.finditer(input))

def parse_duration(input: str):
    if input == "-":
        return None
    duration = input.removesuffix(" per ep.")
    match = re.search(DURATION_PATTERN, duration)
    if not match:
        # special case for fucking Seto no Hayanome OVA specials
        if "sec." in input:
            return 1
        raise ValueError(f"Failed to parse duration string {input}")
    hours = match.group("hours")
    minutes = match.group("minutes")
    return (60 * (int(hours) if hours else 0)) + (int(minutes) if minutes else 0)

def parse_year(input: str):
    if input == "-":
        return None
    return int(input[0:4])

def get_or_create_ids(items, table, column, cursor):
    ids = []
    for item in items:
        cursor.execute(f"SELECT id FROM {table} WHERE {column} LIKE %s", (item,))
        result = cursor.fetchone()
        if not result:
            cursor.execute(f"INSERT INTO {table}({column}) VALUES (%s) RETURNING id", (item,))
            result = cursor.fetchone()
        ids.append(result["id"])
    return ids

def do_migration():
    with psycopg.connect("host=127.0.0.1 dbname=integrated_system user=postgres password=password", row_factory=dict_row) as conn:
        with conn.cursor() as cursor, conn.cursor() as update:
            cursor.execute("""SELECT title, type, episodes, start_airing, end_airing, release_season, broadcast_slot, producers, studios, sources, genres, duration, score, description FROM sources.anime_data""")

            for row in cursor:
                producers = parse_list(row["producers"])
                studios = parse_list(row["studios"])
                genres = parse_list(row["genres"])
        
                producer_ids = get_or_create_ids(producers, "result.producers", "producer", update)
                studio_ids = get_or_create_ids(studios, "result.studios", "studio", update)
                genre_ids = get_or_create_ids(genres, "result.genres", "genre", update)

                update.execute("""INSERT INTO result.anime_titles(
                    title, synopsis, duration_in_minutes, number_of_episodes, media_type, score, start_year, finish_year, season_of_release, source
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id""", (
                    row["title"],
                    row["description"],
                    parse_duration(row["duration"]),
                    row["episodes"] if row["episodes"] != "-" else None,
                    row["type"],
                    row["score"],
                    parse_year(row["start_airing"]),
                    parse_year(row["end_airing"]),
                    row["release_season"],
                    row["sources"]
                ))
                anime_id = update.fetchone()["id"]

                for mapping in producer_ids:
                    update.execute("INSERT INTO result.anime_titles_producers(anime_title_id, producer_id) VALUES (%s, %s)", (anime_id, mapping))
                for mapping in studio_ids:
                    update.execute("INSERT INTO result.anime_titles_studios(anime_title_id, studio_id) VALUES (%s, %s)", (anime_id, mapping))
                for mapping in genre_ids:
                    update.execute("INSERT INTO result.anime_titles_genres(anime_title_id, genre_id) VALUES (%s, %s)", (anime_id, mapping))

if __name__ == '__main__':
    do_migration()
