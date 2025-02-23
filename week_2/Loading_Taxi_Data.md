Tutorial 
https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/02-workflow-orchestration/README.md#3-etl-pipelines-in-kestra-detailed-walkthrough

Data
https://github.com/DataTalksClub/nyc-tlc-data/releases

You don't need to download the data, we will pull it directly from that git repo. 

Now let's follow the tutorial at https://youtu.be/OkfLX28Ecjg?si=vKbIyWo1TtjpNnvt

To start Kestra use the docker file under 
```
https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/02-workflow-orchestration/docker/combined
```
and type
```
docker compose up -d
```
you can then access Kestra on 
```
http://localhost:8080/
```

The kestra yaml files for this tutorial can be found here https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/02-workflow-orchestration/flows/02_postgres_taxi.yaml

Lets go through it, First we start with the inputs

inputs:
  - id: taxi
    type: SELECT
    displayName: Select taxi type
    values: [yellow, green]
    defaults: yellow

  - id: year
    type: SELECT
    displayName: Select year
    values: ["2019", "2020"]
    defaults: "2019"

  - id: month
    type: SELECT
    displayName: Select month
    values: ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    defaults: "01"

Fairly intuitive so far.

...except...

You'll find that if you have an error in your yaml file, you can't save it! who in their right mind thought of that. You can make a bunch of edits, have one error and you can't save your work until you've resolved the error instead of coming back to it like normal people! Come on Kestra team ...

Ideally, you want to test the file every step of the way, you know iteratively. So i want to test the inputs bit is working. To do that you will need to add a task otherwise you can't save the file! I added the following 

```
tasks:
  - id: "hello"
    type: "io.kestra.plugin.core.log.Log"
    level: INFO
    message: "hello this is a test {{ task.id }} > {{ taskrun.startDate }}"
```

You can find it in the examples section under the LOG plugin.

Now hit execute and the flow will ask for the inputs we defined above.

Next we add the variables based on the inputs 

```
variables:
  file: "{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv"
  staging_table: "public.{{inputs.taxi}}_tripdata_staging"
  table: "public.{{inputs.taxi}}_tripdata"
  data: "{{outputs.extract.outputFiles[inputs.taxi ~ '_tripdata_' ~ inputs.year ~ '-' ~ inputs.month ~ '.csv']}}"
```

If you look under executions in Kestra, there's a column named labels, we'll set that next for our flow under tasks.

```
tasks:
  - id: set_label
    type: io.kestra.plugin.core.execution.Labels
    labels:
      file: "{{render(vars.file)}}"
      taxi: "{{inputs.taxi}}"
```

Next we get the data from git

```
  - id: extract
    type: io.kestra.plugin.scripts.shell.Commands
    outputFiles:
      - "*.csv"
    taskRunner:
      type: io.kestra.plugin.core.runner.Process
    commands:
      - wget -qO- https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{{inputs.taxi}}/{{render(vars.file)}}.gz | gunzip > {{render(vars.file)}}
```


At this point, if you execute the flow, you should find the csv file under

Outputs > extract > outputFiles 

Pretty good, I'm alreay impressed :)

Next we will create the postgres table. The tutorial talks about another docker-compose files but Ised the one in the combined folder here 

```
https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/02-workflow-orchestration/docker/combined
```

The file starts Kestra, postgres and pgadmin so you're good to go with everything for this tutorial. 

You'll need to connect pgadmin to postgres, the details for the connection are in the docker-compose.yaml file. The only thing you need is the IP address of the database which you can find via the docker desktop app. 

Find the combinedc group of containers under 

![alt](https://https://github.com/yojackleon/Data-Engineering-Zoomcamp/tree/main/week_2/images/combined.jpg)

Click on postgres_zoomcamp

![alt](https://https://https://github.com/yojackleon/Data-Engineering-Zoomcamp/tree/main/week_2/images/ipaddress.jpg)


Hit inspect and scroll down. Use the value shown under IP address.

When you first connect there won't be any tables under our postgres_zoomcamp database.

So lets create the table if it doesn't exist already

```
  - id: if_yellow_taxi
    type: io.kestra.plugin.core.flow.If
    condition: "{{inputs.taxi == 'yellow'}}"
    then:
      - id: yellow_create_table
        type: io.kestra.plugin.jdbc.postgresql.Queries
        sql: |
          CREATE TABLE IF NOT EXISTS {{render(vars.table)}} (
              unique_row_id          text,
              filename               text,
              VendorID               text,
              tpep_pickup_datetime   timestamp,
              tpep_dropoff_datetime  timestamp,
              passenger_count        integer,
              trip_distance          double precision,
              RatecodeID             text,
              store_and_fwd_flag     text,
              PULocationID           text,
              DOLocationID           text,
              payment_type           integer,
              fare_amount            double precision,
              extra                  double precision,
              mta_tax                double precision,
              tip_amount             double precision,
              tolls_amount           double precision,
              improvement_surcharge  double precision,
              total_amount           double precision,
              congestion_surcharge   double precision
          );

```

For this task to work you will also need to add in the plugin defaults clause at the very bottom of your flow file

```
pluginDefaults:
  - type: io.kestra.plugin.jdbc.postgresql
    values:
      url: jdbc:postgresql://host.docker.internal:5432/postgres-zoomcamp
      username: kestra
      password: k3str4
```

Run this and check the table got created in pgadmin.

Note the unique_row_id column, this is how we prevent duplicates. We're going to take some unique attributes of the row such as pickup datetime, drop off datetime, vendor, pickup location, drop off location, fare, distance and calculate a hash. The same atteributes will produce the exact same hash, so we check this has to ensure we don't insert duplicates.

Now we're going to create the following dequence of tasks

1. Create the yellow taxi table using the Queries plugin 
2. Create the yellow taxi staging table using the Queries plugin 
3. Copy the CSV data into the staging table using the CopyIn plugin
4. Create a unique hash for each row in the staging table using Queries
5. Merge the staged yellow taxi data into the main yellow taxi table using Queries

Then we need to do the same for the green taxi data because the columns are slightly different.

Couple of cleanup activitie we need to be conscious of are 

1. Clearing down the staging table before loading more data using the following task.

```
      - id: yellow_truncate_staging_table
        type: io.kestra.plugin.jdbc.postgresql.Queries
        sql: |
          TRUNCATE TABLE {{render(vars.staging_table)}};
```

2. purging temporary files after each execution with the following task

```
  - id: purge_files
    type: io.kestra.plugin.core.storage.PurgeCurrentExecutionFiles
    description: This will remove output files. If you'd like to explore Kestra outputs, disable it.
```

There are 7.5m rows for yellow taxi data in Jan 2019 so yep, it might take a while. My cheap second hand laptop managed it in 3m 15s which is pretty impressive to be fair.






