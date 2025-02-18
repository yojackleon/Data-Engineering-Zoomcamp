
# Start a postgres container

`docker run -it \
	-e POSTGRES_USER="root" \
	-e POSTGRES_PASSWORD="root" \
	-e POSTGRES_DB="ny_taxi" \
	-v C:/Study/DE/week_1/2_docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data \
	-p 5432:5432 \
	postgres:13 `

you need to have docker running the in background

# Command line DB admin using pgcli

`pgcli -h localhost -p 5432 -u root -d ny_taxi`

## Install Python 

You need python installed locally. In windows you have 2 options
- Use the Microsoft Store
- Use the installer from the Python website

### Microsoft Store
Just go to your start menu, type store, bring up the store app on windows, search for python. Hit install. 
### Python website
Go here https://www.python.org/downloads/windows/ you most likely need the 64-bit version, download and install. 

Check if it installed correctly
`python --version`

if you get an error you probably need to put it on yoru windows path, follow these instructions https://www.geeksforgeeks.org/how-to-add-python-to-windows-path/

## Using pgcli

Now we're ready to use pgcli, or are we ...
Check if the command is recognised
`pgcli --version`

It's a Python module but doesn't always work directly like this. Don't worry if it doesn't, you can call any Python module using 
`python -m <module name>`

So try 
`python -m pgcli --version`

If that doesn't work, something has gone wrong with your Python install, I would reinstall Python and make sure its on your system path as show in the link above.

Now go back to the original command to start pgcli

# Using a Jupyter Notebook

## Installing Jupyter

Simples
`pip install jupyter`

Now to run Jupyter just type
`jupyter notebook`

# Load the data


The set of commands we need to run to load the dataset are show in the notebook named upload-data.ipynb

To connect to the database you will need to install sqlalchemy. That didn't work for me, it caused all kinds of compability issues with jupyter, sqlalchemay, psycopg2 and other modules I can't remember the names of. I tried all kinds of suggestions from forums, Stackoverflow and the course slack channel but simply couldn't get it to work. 

So I did everything on the command line and that worked fine. I use Git bash for everything


So open git bash and start thhe python interpreter

`python`
`import pandas as pd`

Check pandas came in

`pd.__version__`

I downloaded and unzipped the data file https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz and put it in week1 directory to make things easier.

So lets create a dataframe and see what it looks like

`df = pd.read_csv('yellow_tripdata_2021-01.csv', nrows=100)`
`df`

Now we need to extract a schema

`print( pd.io.sql.get_schema( df, name='yellow_taxi_data'))`

We need to adjust the data type used in the datetime columns 

`df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)`
`df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)`

OK how does that look 

`print( pd.io.sql.get_schema( df, name='yellow_taxi_data'))`

Hopefull the correct data types are showing now

Now we connect to postgres to create a postgres specific schema def so that we can create the target table in our DB
( This is the step I couldn't get to work via Jupyter notebook )

`from sqlalchemy import create_engine`
`engine=create_engine('postgresql://root:root@localhost:5432/ny_taxi')`
`engine.connect()`

Let's have a look at teh schema we're going to use. 

`print( pd.io.sql.get_schema( df, name='yellow_taxi_data', con=engine))`

No create an iterator for the data from our csv file

`df_iter = pd.read_csv('yellow_tripdata_2021-01.csv', iterator=True, chunksize=100000)`

Check its type to see if it was created correctly. 

`df_iter`

Pull out the first chunk

`df = next(df_iter) `
`len(df)`

Correct the types again

`df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)`
`df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)`

Get the headers

`df.head(n=0)`

Create the table

`df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')`

We're going to use pgcli to check the the table was created before proceeding. You can also use pgadmin

Running pgcli from the command line didn't work although i already insstalled it using pip
So I am using `python -m pgcli`

`python -m pgcli -h localhost -p 5432 -u root -d ny_taxi`

Now we can Check the table description using the following

`\d yellow_taxi_data`

OK back to the python interpreter to get some data in there

`df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')`

Before we throw the rest of the data in, lets double check that this chunk went in. 
So back to pgcli

`select count(1) from yellow_taxi_data`

It should show 100000 rows

Back to python, we're going to write a little while loop to call the iterator until all the chunks have been loaded.

```python
while True:
  df = next( df_iter)`
  
  df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
  df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

  df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')

  print( 'inserted another chunk ..., took%.3f seconds' % (t_end - t_start))
```

I actually typed this loop into a file (df_iterator.py) and called it from the python interpretor using 

`exec(open("df_iterator.py").read())`

Back to pgcli check we got all the rows  

`select count(1) from yellow_taxi_data`

Do a wordcount on the CSV to compare

`wc-l yellow_tripdata_2021-01.csv`

