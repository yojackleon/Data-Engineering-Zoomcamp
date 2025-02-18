
Created the docker-compose file 

We don't want to have to remember all those long commands so we will put everything into a docker compose file and then we can happily juse type 

```console
docker-compose up -d 
```
To bring up any number of containers with the config we need

```console
docker-compose down
```
To cleanly shutdown all the containers from the docker-compose file.



#read in the zones data file using file ingest_zones.py

#call using 

python ingest_zones.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=zones


#some sql

select
CAST( tpep_dropoff_datetime as DATE ) as day,
"DOLocationID",
count(1) as count,
max(total_amount),
max(passenger_count)
from
yellow_taxi_trips t
GROUP BY 
1,2
order by 1,2 desc
limit 100;





    