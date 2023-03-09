# info-integration-project

***Archival Note:*** This project was part of student work.
As such with it being handed in, it has finished its useful lifecycle.
This is not supposed to be used in basically any context, but left standing in case it's useful on the resumee of any of the students involved.

## Initial application setup

The Setup needs docker, python 3.7 or later and a correctly configured JAVA_HOME (for gradle).
Additional python libraries required are listed in `pip-libraries`.
In addition the setup presumes a Linux system with `bash` installed.

1. Set up the postgres database as docker container (ensure docker daemon is running):
    This will import the datasets as tables in a `sources` schema

    ```
    > ./env.sh datasets/ds1.csv datasets/ds2.csv datasets/ds3.csv datasets/ds4.csv
    ```
2. Run ETL scripts to import data from the sources tables into the target schema:
    This will transform all source data to the global schema and store them into the results schema tables.
    
    ```
    > ./etl/etl_anime_data.py
    > ./etl/etl_animeplanet.py
    > ./etl/etl_myanimelist.py
    > ./etl/etl_recommendations_db.py
    ```

3. Run Data fusion:
    This performs data fusion on the results schema and stores the final data result in the public tablespace:

    ```
    > ./etl/data_fusion.py
    ```

## How to run the application

Run the gradle task `bootRun` from within the `information-integration-web` folder:

```
information-integration-web> ./gradlew bootRun
```

The Application is now running on port 8080 on localhost.
The API is available on http://localhost:8080/api, the frontend is available on http://localhost:8080/index.html.

The data shown in the frontend can currently only be determined by issuing queries in the console.
For that to work, all API methods are exposed on a special object attached to the global `window` object of the website javascript context.
To invoke these methods, open the developer tools and call the methods you want on `window.interact`.

***Available Methods***

 - `window.interact.allTitles()`: All titles available in the Database
 - `window.interact.ranked()`: All titles, but ranked by their score
 - `window.interact.titlesBetween(startYear, endYear)`: Titles that started airing after or in `startYear` and stopped airing before `endYear`. The `endYear` can be omitted and then defaults to 2030.
 - `window.interact.withoutContentWarnings(['cw 1', 'cw 2', ...])`: A list of titles that are *not* associated with any of the content warnings passed to the method. Content Warnings are not currently displayed, but can be seen in API responses.
 - `window.interact.byGenre(genre)`: A list of titles that is associated with the given genre. The genres are shown on titles as small pill-shaped tags.
 - `window.interact.byProducer(producer)`: A list of titles that have been produced by the given producer. Producers can be retrieved from the API responses.
 - `window.interact.byStudio(studio)`: see above
 - `window.interact.undiscovered()`: Titles without a score
 - `window.interact.duration(minutes, episodes)`: Titles that are no longer than the given duration specification.
