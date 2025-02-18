while True:
  t_start=time()
  df = next( df_iter)
  
  df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
  df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

  df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')

  t_end=time()

  print( 'inserted another chunk ..., took%.3f seconds' % (t_end - t_start))
