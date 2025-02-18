import pandas as pd
import argparse
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name

    csv_name='taxi_zone_lookup.csv'
    
    engine=create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df = pd.read_csv(csv_name); 

    df.to_sql(name=table_name, con=engine, if_exists='replace')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Ingest csv data to postgres')


    parser.add_argument('--user', help='postgres username')
    parser.add_argument('--password', help='postgres password')
    parser.add_argument('--host', help='postgres host')
    parser.add_argument('--port', help='postgres port')
    parser.add_argument('--db', help='postgres db name')
    parser.add_argument('--table_name', help='postgres destination table')

    args = parser.parse_args()
    
    main(args)




