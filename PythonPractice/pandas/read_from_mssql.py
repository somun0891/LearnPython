import os
import pandas as pd
from sqlalchemy import create_engine
import pyodbc
import snowflake.connector as sf
from snowflake.connector.pandas_tools import write_pandas
from concurrent.futures import ThreadPoolExecutor
#from concurrent.futures import future,concurrent
import concurrent.futures
import numpy as np
import psutil
from sys import getsizeof,path

path.append("D:\\LearnPython\\PythonPractice\\")

server = 'STORM'
database = 'AdventureWorks2017'
driver = '{ODBC Driver 17 for SQL Server}'
username = 'CustomLogin'
password = 'QAWS123qaws'

odbc_params = f"DRIVER={driver};SERVER=tcp:{server};PORT=1433;DATABASE={database};UID={username};PWD={password};Trusted_Connection=yes;"

connection_string = f'mssql+pyodbc:///?odbc_connect={odbc_params}'

engine = create_engine(connection_string)

sql_query = '''
  select  NAME,PRODUCTID from Production.product_copy
'''

snow_sql_query = '''
  select top 10 * from TESTDB.PUBLIC.EMPLOYEES;
'''

# Snow conn setup
snowconn = sf.connect(
    user='MEETNANU',
    password='QAWS123qaws',
    account='hhvqkhk-gbb36396',
    warehouse='COMPUTE_WH',
    database='TESTDB',
    schema='PUBLIC'
    )

sfcursor = snowconn.cursor()

#test out the connection
sfcursor.execute(
    "CREATE OR REPLACE TABLE "
    "TESTDB.PUBLIC.EMPLOYEES_CLONE_1 AS SELECT * FROM TESTDB.PUBLIC.EMPLOYEES WHERE False" 
)

sfcursor.execute(
    "CREATE OR REPLACE TABLE "
    "TESTDB.PUBLIC.PRODUCT (NAME VARCHAR , PRODUCTID VARCHAR , UPDATE_DT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP)" 
)

#OR

sfcursor.execute(
    "TRUNCATE TABLE IF EXISTS "
    "TESTDB.PUBLIC.PRODUCT" 
)

# sfcursor.execute(
#     "INSERT INTO test_table(col1, col2) VALUES " + 
#     "    (123, 'test string1'), " + 
#     "    (456, 'test string2')")


#read data from snowflake
sfcursor.execute(snow_sql_query,timeout=60 * 10)
# df = sfcursor.fetch_pandas_all()
# print(df.head(3))


#parameters to write_pandas
emp_table = 'EMPLOYEES_CLONE'
emp_table_clone = 'EMPLOYEES_CLONE_1'
product_table = 'PRODUCT'
database = 'TESTDB'
schema = 'PUBLIC'
compression = 'gzip' #intermediate parquet file compression type , snappy/gzip
load_chunk_size = 5000


# chunk_num=0
# loaded_rows = 0

"""
chunk_iter = pd.read_sql_query(sql = sql_query , con =  engine, chunksize = 100, 
                               #dtype = {"TITLE":object, "EMPLOYEE_ID":np.int32 , "Manager_ID":np.int32} 
                               # dtype = {"ProductID":object, "Name":object }              
                                 )
"""
                                 
"""
for chunk_df in  chunk_iter:
#for chunk_df in  sfcursor.fetch_pandas_batches():
     #rows += chunk_df.shape[0]
    print(chunk_df)
    print(chunk_df.dtypes)
    chunk_num+=1

    success, nchunks, nrows, _ = write_pandas(
                                    conn = snowconn, 
                                    df = chunk_df, 
                                    table_name = product_table,
                                    database = database,
                                    schema = schema,
                                    #chunk_size = load_chunk_size,
                                    #auto_create_table=True,
                                    #table_type='Transient'
                                    compression=compression
                                    
                               )
    loaded_rows += nrows
    print(success)
    snowconn.close()
    print(f" loaded rows by the executor: {loaded_rows}")

"""

# Method-1 - using generator to efficient memory use + load in sequence one chunk at a time
"""
def gen_data(query , engine , chunksize):
    for chunk_df in pd.read_sql_query(sql = query, con =  engine, chunksize = chunksize ):
        yield chunk_df


def write_to_snowflake():
    count = 0
    for df in gen_data(sql_query, engine , 100 ):
        count += 1
        print(f"The length of chunk - {count}",len(df))
    
write_to_snowflake()    
"""

# Method-2 - using ThreadPoolExecutor to load in parallel
chunk_iter = pd.read_sql_query(sql = sql_query , con =  engine, chunksize = 100)
print("Showing all chunks in the iterator dataframe....",end = "\n")

print([(idx, f"{len(chunk)} rows" ,f"{getsizeof(chunk)} bytes ") for idx,chunk in enumerate(list(chunk_iter))])
#function below submitted to executor of type ThreadPoolExecutor

#chunk_iter =  sfcursor.fetch_pandas_batches()  #DATA FETCH FROM SNOWFLAKE

def process_chunk(chunk):

    #for chunk in  sfcursor.fetch_pandas_batches():
     #rows += chunk_df.shape[0]
    #print(chunk)
      #chunk_num+=1
    success, nchunks, nrows, _ = write_pandas(
                                    conn = snowconn, 
                                    df = chunk, 
                                    table_name = product_table, #emp_table_clone, #variable
                                    database = database,
                                    schema = schema,
                                    #chunk_size = load_chunk_size,
                                    auto_create_table=False, # auto_create_table=False and overwrite=False,  appends data
                                    overwrite=False, # auto_create_table=False and overwrite=true,  truncate and load data
                                    #table_type='Transient'
                                    compression=compression,
                                    #parallel = 2
                               )
    

    #loaded_rows += nrows

    #print(f"Total loaded rows by the executor: {loaded_rows}")

    #print(f"Chunk number {nchunks} :Processed with {nrows} records...")



def process_data_in_parallel():
    
    with ThreadPoolExecutor(max_workers=2 , thread_name_prefix = 'Wrk_') as executor:
      
        #chunk_num=0
        
        # loaded_rows = 0
        for chunk in  chunk_iter:
           #chunk_num += 1
           executor.submit(process_chunk ,chunk)  #takes a functions and its parameters as arguments

        #futures = [executor.submit(process_chunk , chunk ) for chunk in  chunk_iter]
        # for future in concurrent.futures.as_completed(futures):
        #    print(future.result())

        executor.shutdown(wait = True)


process_data_in_parallel()




# engine = create_engine('sqlite:///sample_data.db')


# Estimate the memory footprint of one row
def estimate_chunksize(query):
   
   df = pd.read_sql(query , engine)
   average_row_size = getsizeof(df) / len(df) #sys module
   print(f"Average memory size per row: {average_row_size} bytes")
   
   # Assess your available memory
   available_memory = psutil.virtual_memory().available * 0.5  # using 50% of available memory
   
   # Calculate a safe chunksize
   safe_chunksize = available_memory // average_row_size
   print(f"Safe chunksize: {safe_chunksize} rows per chunk")

query_for_estimation = 'SELECT * FROM  Production.Product'
#estimate_chunksize(query_for_estimation)





engine.dispose()

# connection_string = f'DRIVER={driver};SERVER=tcp:{server};PORT=1433;DATABASE={database};UID={username};PWD={password}'

# # query system views

# with pyodbc.connect(connection_string) as conn:
#     query = '''
#           select * from Production.TransactionHistory
#     '''

#     df = pd.read_sql(sql=query, con=conn)
#     print(df.head())


"""
Prerequisites- 
Required libraries - pyodbc , azure-identity , azure-keyvault-secrets , snowflake-connector-python[pandas] , snowflake-sqlalchemy
Make sure to create an engine object to read fron mssql/azuresql and another snowflake conn object to read/write from snowflake.
Reading from Azure sql requires safely accessing credential thru azure key vault (get uri and secret names and add clientIP to azure db server firewall)
1. Use snowflake connector to fetch load master data and store config values into variables.
2. Use pandas with generators to yield df using pd.read_sql_query(...)
3. Load to snowflake staging using write_pandas.
4. Update load_log with load_start_time , load_end_time , rows_parsed , rows_loaded , last_updated_date , active_fl.
5. Implement exception handling and python logging.
load_master
==========
source_table , sql_command , batch_size , target_table 

load_log
========
load_start_time , load_end_time , rows_parsed , rows_loaded , last_updated_date , active_fl


"""