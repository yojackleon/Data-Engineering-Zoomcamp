import pandas as pd
import argparse
import os
from time import time
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    #url = params.url
    csv_name='output.csv'
    #we don't need to get the file as we already have it downloaded locally 
    #os.system(f"wget {url} -O {csv_name}")
    csv_name='yellow_tripdata_2021-01.csv'
    
    engine=create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    #engine.connect()

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    df = next(df_iter) 
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')

    while True:
        t_start=time()
        df = next( df_iter)
  
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql(name=table_name, con=engine, if_exists='append')

        t_end=time()

        print( 'inserted another chunk ..., took%.3f seconds' % (t_end - t_start))



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Ingest csv data to postgres')


    parser.add_argument('--user', help='postgres username')
    parser.add_argument('--password', help='postgres password')
    parser.add_argument('--host', help='postgres host')
    parser.add_argument('--port', help='postgres port')
    parser.add_argument('--db', help='postgres db name')
    parser.add_argument('--table_name', help='postgres destination table')
    #parser.add_argument('--url', help='url of csv')


    args = parser.parse_args()
    
    main(args)




