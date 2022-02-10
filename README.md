# info-integration-project

## How to run the application
#### 1. `./env.sh datasets/ds1.csv datasets/ds2.csv datasets/ds3.csv datasets/ds4.csv` - setup the docker postgreSQL database with necessary schema
#### 2. `./etl/etl_anime_data.py` `./etl/etl_animeplanet.py` `./etl/etl_myanimelist.py` `./etl/etl_recommendations_db.py` - import data from sources
#### 3. `./etl/data_fusion.py` - run data fusion process