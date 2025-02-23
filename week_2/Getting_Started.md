Current
https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/02-workflow-orchestration/README.md

https://www.youtube.com/watch?v=o79n-EVpics


copy docker-compose.yaml from week_2/docker/composed 
and start up the containers

docker compose up -d

If there are any problems and its your first time running this command it might be a sequencing problem as the images are being downloaded. Shut everything down again and restart using.

docker compose down


You can access Kestra on http://localhost:8080

We're going to import the getting started flow from 

https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/02-workflow-orchestration/flows/01_getting_started_data_pipeline.yaml

Download it to your local file system.

Make sure your containers are running and open Kestra using the link above. 

You can import the flow using the import menu at the top right. Just select the yaml file and you're good to go. 

Now go to flows and hit the purple execute button on the top right.

Lets have a quick look at the tasks in the Kestra flow file

```
  - id: extract
    type: io.kestra.plugin.core.http.Download
    uri: https://dummyjson.com/products
```

Kestra comes with a load of convenient plugins, here we're using a Download plugin and pointing it at a URI where it will find some dummy data

the downloaded data will ne available in a variable named

outputs.<task>.<command>

so in our case

outputs.extract.uri

Simples :)

Next is the teransform task

```
  - id: transform
    type: io.kestra.plugin.scripts.python.Script
    containerImage: python:3.11-alpine
    inputFiles:
      data.json: "{{outputs.extract.uri}}"
    outputFiles:
      - "*.json"
    env:
      COLUMNS_TO_KEEP: "{{inputs.columns_to_keep}}"
    script: |
      import json
      import os

      columns_to_keep_str = os.getenv("COLUMNS_TO_KEEP")
      columns_to_keep = json.loads(columns_to_keep_str)

      with open("data.json", "r") as file:
          data = json.load(file)

      filtered_data = [
          {column: product.get(column, "N/A") for column in columns_to_keep}
          for product in data["products"]
      ]

      with open("products.json", "w") as file:
          json.dump(filtered_data, file, indent=4)
```

Normally the python script would be in a separate file. 

The plugin used in this task pulls down a python image and runs it using docker to exercute the python script. 

Once you've run this flow you can preview the products.json file under

outputs > transform > outputfiles > products.json > preview

If you need to find previous runs, they're under executions. 

Finally the last task loads the products.json file into an in memory database called DuckDB and queries it. 

  - id: query
    type: io.kestra.plugin.jdbc.duckdb.Query
    inputFiles:
      products.json: "{{outputs.transform.outputFiles['products.json']}}"
    sql: |
      INSTALL json;
      LOAD json;
      SELECT brand, round(avg(price), 2) as avg_price
      FROM read_json_auto('{{workingDir}}/products.json')
      GROUP BY brand
      ORDER BY avg_price DESC;
    fetchType: STORE


Again using a convenient kestra plugin. You can see the output of the query under

outputs > query > uri > preview




