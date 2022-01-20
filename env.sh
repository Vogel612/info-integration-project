#!/bin/bash

if [[ $# != 0 && $# != 4 ]]; then
    echo """Usage:

    env [ds1.csv ds2.csv ds3.csv ds4.csv]

    With no arguments the docker container is started, with four arguments
    additionally the initial dataset is imported."""
    exit 1
fi;

password='password'

docker run -d --rm \
    --name=info-integration-db \
    --hostname=info-integration-db \
    --publish 5432:5432 \
    -e POSTGRES_PASSWORD=$password \
    -e PGDATA=/var/lib/postgresql/data/pgdata \
    -v "$(pwd)"/datadir:/var/lib/postgresql/data \
    postgres

if [[ $? != 0 ]]
then
    exit_code = $?
    echo "Could not run docker."
    exit exit_code
fi

if [[ $# = 4 ]]
then
    echo "Creating database integrated_system and defining schemata 'sources' and 'result'"
    PGPASSWORD=$password psql -h 127.0.0.1 -U postgres -c "CREATE DATABASE integrated_system OWNER 'postgres' LOCALE 'en_US.utf8';"
    PGPASSWORD=$password psql -h 127.0.0.1 -U postgres integrated_system < define_sources.sql;
    PGPASSWORD=$password psql -h 127.0.0.1 -U postgres integrated_system < define_global_schema.sql

    if [[ -r $1 && -r $2 && -r $3 && -r $4 ]]
    then
        echo "Importing $1 into sources.animeplanet"
        PGPASSWORD=$password psql -h 127.0.0.1 -U postgres integrated_system -c "COPY sources.animeplanet(title, media_type, eps, duration, ongoing, start_yr, finish_yr, release_season, description, studios, tags, content_warn, watched, watching, want_watch, dropped, rating, votes) FROM STDIN CSV HEADER" < $1
        echo "Importing $2 into sources.mal_anime"
        PGPASSWORD=$password psql -h 127.0.0.1 -U postgres integrated_system -c "COPY sources.mal_anime(anime_id, name, genre, type, episodes, rating, members) FROM STDIN CSV HEADER" < $2
        echo "Importing $3 into sources.anime_data"
        PGPASSWORD=$password psql -h 127.0.0.1 -U postgres integrated_system -c "COPY sources.anime_data(title, type, episodes, status, start_airing, end_airing, release_season, broadcast_slot, producers, licensors, studios, sources, genres, duration, esrb_rating, score, scored_by, members, favorites, description) FROM STDIN CSV HEADER" < $3
        echo "Importing $4 into sources.recommendations.db"
        PGPASSWORD=$password psql -h 127.0.0.1 -U postgres integrated_system -c "COPY sources.recommendations_db(anime_id, title, genre, synopsis, type, producer, studio, rating, scored_by, popularity, members, episodes, source, aired, link) FROM STDIN CSV HEADER" < $4
    else
        echo "Not all files existed and were readable. Aborting data import."
    fi
fi
