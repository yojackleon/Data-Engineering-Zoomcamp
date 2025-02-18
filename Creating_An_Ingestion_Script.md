# Ingest taxi trips
Create a data ingestion python script

Use the commands from Data_Ingestion.md and copy them into into ingest_data.py

To call that we need loads of parameters

You can pass in the data file name as well but I hard coded it into the script as we downloaded it anyway.

```console
python ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_trips
```

# Ingest zones

Similarly we're going to ingest the zones data file taxi_zone_lookup.csv 
Take a look at ingest_zones.py, no iterator or while loop because the file isn't that long and we're just going to upload everything in one go.



# Using Dockerfile to run the script
We want to create a docker container that runs the ingestion script for us. We will do this by creating a python container and copying the script across to it.

Take a look at the Dockerfile in this project.

`FROM python:3.9.1`
Create a container using python, we specify the version of python here 

Install some libraries we're going to need.
`RUN apt-get install wget`
`RUN pip install pandas sqlalchemy psycopg2`

Create and cd into app directory
`WORKDIR /app`

Copy the script across
`COPY ingest_data.py ingest_data.py`
`COPY ingest_zones.py ingest_zones.py`

Copy the data across ( you don't need to install wget if you're moving the data across like this ) 
`COPY yellow_tripdata_2021-01.csv yellow_tripdata_2021-01.csv`

Specify the start command when the container is run.
`ENTRYPOINT ["python", "ingest_data.py"]`

All that goes in the Dockerfile, and now we can build the container. 

`docker build -t taxi_ingest:v001 .`

Sweet, now to run the ingest script from inside docker
Remember to use the pg-network, and the host is now pg-database

```console
docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips 
```



