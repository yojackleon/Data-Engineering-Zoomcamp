# Runing pgadmin in docker

```console
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  dpage/pgadmin4
```
Aha but they can't see each other because they're running in differnt containers and localhost is not the same for them.
So we need to create a network between them

First we create a network

```console
docker network create pg-network
```

No start postgres again using thisnetwork

```console
docker run -it \
	-e POSTGRES_USER="root" \
	-e POSTGRES_PASSWORD="root" \
	-e POSTGRES_DB="ny_taxi" \
	-v C:/Study/DE/week_1/2_docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data \
	-p 5432:5432 \
  --network=pg-network \
  --name=pg-database \
  postgres:13`
```

```console
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name=pgadmin \
  dpage/pgadmin4
```


Log into pgadmin and create a connection
The server name is the docker database name - pd_database


