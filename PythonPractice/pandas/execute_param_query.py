import pyodbc
import os
import logging
from datetime import datetime
import pandas as pd


DB_SERVER = 'STORM' 
DB_NAME = 'AdventureWorks2017'    
DB_USER = 'CustomLogin'   
DB_PASSWORD = 'QAWS123qaws' 


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def create_sql_server_connection():
    """ Create a database connection to the SQL Server database """
    conn = None

    if not all([DB_SERVER, DB_NAME]):
        logger.error("Missing required environment variables: DB_SERVER and DB_NAME must be set.")

        return None 

    try:
       
        if DB_USER and DB_PASSWORD:
            logger.info(f"Attempting SQL Server Authentication to {DB_SERVER}/{DB_NAME} as user {DB_USER}")
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};" # Specify driver explicitly or remove if default works
                f"SERVER={DB_SERVER};"
                f"DATABASE={DB_NAME};"
                f"UID={DB_USER};"
                f"PWD={DB_PASSWORD};"
                "Encrypt=no;"
                "TrustServerCertificate=no;" # Set to yes if using self-signed cert or can't validate
                "Connection Timeout=30;"
            )
  
        # # Establish connection
        conn = pyodbc.connect(conn_str, autocommit=False) 
        logger.info(f"Successfully connected to SQL Server: {DB_SERVER}/{DB_NAME}")


        return conn

    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        logger.error(f"Error connecting to SQL Server ({DB_SERVER}/{DB_NAME}). SQLSTATE: {sqlstate}", exc_info=True)
        logger.error(f"Connection String (Password Redacted): {conn_str.replace(DB_PASSWORD, '****') if DB_PASSWORD else conn_str}")
        raise 
    except Exception as e:
        logger.error(f"An unexpected error occurred during connection setup: {e}", exc_info=True)
        raise



def read_sql_script(file_path):
    """ Reads the content of an SQL script file. """
    logger.info(f"Reading SQL script from: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
            if not sql_content.strip():
                logger.warning(f"SQL script file is empty: {file_path}")
                return None
            logger.info(f"Successfully read SQL script: {file_path}")
            return sql_content
    except FileNotFoundError:
        logger.error(f"SQL script file not found: {file_path}")
        raise
    except IOError as e:
        logger.error(f"Error reading SQL script file {file_path}: {e}", exc_info=True)
        raise

def execute_parametrized_sql_server_script(conn, sql_script_content, params):

    if not sql_script_content:
        logger.warning("SQL script content is empty, skipping execution.")
        return False, 0 # Return success status and rows affected
    if not conn:
        logger.error("Database connection is not available, cannot execute script.")
        return False, 0

    cursor = None
    rows_affected = 0
    try:
        cursor = conn.cursor()
        logger.info("Executing parametrized SQL Server script...")

        # Pass parameters as a tuple/list - order must match '?' placeholders in the script
        cursor.execute(sql_script_content, params)

        data_rows = cursor.execute('select * from userprofile_tmp').fetchall()

        #rows_affected = cursor.rowcount
        #print(rows_affected)
        #print(data_rows)    

        conn.commit()  # Commit the transaction explicitly since autocommit is off

        #columns = [column[0] for column in cursor.description]

        mssql_data_df = pd.DataFrame(data_rows)
        
        #print(mssql_data_df.head(5))

        logger.info(f"Successfully executed script and committed transaction. Rows affected: {rows_affected}")
        
        return True, rows_affected ,mssql_data_df
    
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        logger.error(f"Error executing SQL Server script. SQLSTATE: {sqlstate}", exc_info=True)
        logger.error(f"Parameters passed: {params}")
        try:
            logger.warning("Attempting to roll back transaction due to error.")
            conn.rollback() 
        except pyodbc.Error as rb_ex:
            logger.error(f"CRITICAL: Error during transaction rollback: {rb_ex}", exc_info=True)
        return False, 0
    except Exception as e:
         logger.error(f"An unexpected error occurred during script execution: {e}", exc_info=True)
         try:
             logger.warning("Attempting to roll back transaction due to unexpected error.")
             conn.rollback()
         except pyodbc.Error as rb_ex:
            logger.error(f"CRITICAL: Error during transaction rollback after unexpected error: {rb_ex}", exc_info=True)
         return False, 0
    finally:
        if cursor:
            cursor.close()
            logger.debug("Database cursor closed.")



def main():

    logger.info("--- SQL Server Script Execution Started ---")
    sql_script_path = 'update_user_status.sql'
    conn = None

    try:
        conn = create_sql_server_connection()
        if not conn:

             logger.critical("Failed to establish database connection. Check configuration and logs.")
             return

        sql_script_path = 'D:\\LearnPython - Copy\\PythonPractice\\pandas\\update_user_status.sql'

        sql_to_execute = read_sql_script(sql_script_path)

        user_id_to_update = 101
        new_status = 2

        script_params = (
            new_status,       
            new_status,       
            user_id_to_update 
        )
        logger.info(f"Preparing to execute script for UserID: {user_id_to_update} with New Status: {new_status}")

        # Execute the Parametrized Script
        result  = execute_parametrized_sql_server_script(conn, sql_to_execute, script_params)

        success, rows, mssql_data_df = result

        print(mssql_data_df.head(10))

        if success:
            logger.info(f"SQL Server script executed successfully. Rows affected: {rows}")
            # You could add a SELECT query here to verify the update
        else:
            logger.error("SQL Server script execution failed. Check previous logs for errors.")

    except FileNotFoundError:
        logger.critical(f"Fatal Error: SQL script file '{sql_script_path}' not found.")

    except pyodbc.Error as db_err:
        logger.critical(f"Fatal Database Error: {db_err}", exc_info=True)

    except Exception as e:
        logger.critical(f"An unexpected fatal error occurred: {e}", exc_info=True)
    finally:
        if conn:
            try:
                conn.close()
                logger.info("Database connection closed.")
            except pyodbc.Error as e:
                logger.error(f"Error closing the database connection: {e}", exc_info=True)
        logger.info("--- SQL Server Script Execution Finished ---")


if __name__ == "__main__":

    main()