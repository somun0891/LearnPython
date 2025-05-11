
'''



File format - csv ( , | . ; \t ) , fwf (fixed width)
All the configurations will be read from yaml file. throw errors if mandatory config are missing for respective file formats.
A staging table will be created each time with the same name as filemask/fileconfig name .It will have 2 additional fields
  rowtype field - HDR , DTL  , sql_dtype - VARCHAR(10)
  filename - myfile_YYYYMMDD.csv - VARCHAR(256)


load_csv(...)
============
pd.read_csv(filepath_or_buffer, sep=’ ,’  , header=’infer|none|2’,  index_col=None,
                         usecols=None|<list>, engine=None|'python', skiprows=None|1, nrows=None) 


PARAMETERS AND ERROR HANDLING FOR CSV
====================================
usecols - mandatory 
          colspecs config
          column name list EXACTLY match the file field names
          It also should have respective sql_dtypes.
		  
      	  use zip function to create a list of tuples and access them in code
          
Error - column list and their sql_dtypes is mandatory for csv files.
	   			       
sep -   mandatory if file_format is csv , optional for fwf.
        field_delimiter
Error - field delimiter is mandatory for csv files.

skiprows - optional
           header_rows_to_skip config
           skip header rows based on header_rows_to_skip config 
           For e.g. this will be 1 , if first row contains - HDR 2 20250514
Error - NA
    
header -  hdr_cols_line_num config 
          file line number containing field names
          
Error - csv file must have a header row with field names
          
nrows  - read header separately, detail records will be read separately using separate call to pd.read_csv().
			e.g. hdr_df = pd.read_csv('somefile.csv', nrows=1)
                 dtl_df = pd.read_csv('somefile.csv', skiprows = 1, ....)

chunksize - read N rows at a time, large file processing.



load_fwf(...) 
==============
fwf files- 

both column list and corresponding position list are mandatory in fixed width files.
fwf files will have both position list and column list.


pd.read_fwf(fixed_width_file, widths=column_widths, names=column_names, chunksize=chunksize):

fixed_width_file - mandatory , fail if fileconfig name don't match cli args.
widths = position list , same order as column names to be able to map them.
names = column names 
chunksize - read N rows at a time, large file processing.

no header parameter present in read_fwf()  - so read the header as is ...
but should be able to add 2 additional fields - rowtype and filename just like in csv format.
distinguish header correctly using header_rows_to_skip config 
 for e.g  header_rows_to_skip config is set to 2 , then first 2 rows in the dataframe constitute headers
 and rest are detail records.


'''


import pandas as pd
import oracledb

# Enable "thin" mode (does not require Oracle Instant Client)
# or comment this out if using "thick" mode (i.e., with Oracle Client libraries installed)
oracledb.init_oracle_client()  # optional, needed only for thick mode or if errors occur

# Oracle DB connection info
conn = oracledb.connect(
    user="your_username",
    password="your_password",
    dsn="your_host:1521/your_service_name"  # or use a TNS entry if configured
)

# Parameters
fixed_width_file = "path_to_your_file.txt"

# Define column widths and names (example - adjust to your file)
column_widths = [10, 15, 20]  # Replace with actual widths
column_names = ['col1', 'col2', 'col3']  # Replace with actual column names

# SQL insert statement
insert_sql = "INSERT INTO your_table (col1, col2, col3) VALUES (:1, :2, :3)"

# Read and insert in chunks
chunksize = 50000  # Adjust as needed

with conn.cursor() as cursor:
    for chunk in pd.read_fwf(fixed_width_file, widths=column_widths, names=column_names, chunksize=chunksize):
        data = chunk.where(pd.notnull(chunk), None)  # Replace NaNs with None for Oracle
        cursor.executemany(insert_sql, data.values.tolist())
        conn.commit()

conn.close()
print("Data load complete.")
