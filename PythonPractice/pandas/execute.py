import pyodbc
import os
import logging
from datetime import datetime


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

        return None # Indicate failure to get necessary config

    try:
        # Connection string - adjust based on your authentication method
        # Option 1: SQL Server Authentication (requires DB_USER, DB_PASSWORD)
        # if DB_USER and DB_PASSWORD:
        #     logger.info(f"Attempting SQL Server Authentication to {DB_SERVER}/{DB_NAME} as user {DB_USER}")
        #     conn_str = (
        #         f"DRIVER={{ODBC Driver 17 for SQL Server}};" # Specify driver explicitly or remove if default works
        #         f"SERVER={DB_SERVER};"
        #         f"DATABASE={DB_NAME};"
        #         f"UID={DB_USER};"
        #         f"PWD={DB_PASSWORD};"
        #         # Recommended options for reliability:
        #         "Encrypt=yes;"
        #         "TrustServerCertificate=no;" # Set to yes if using self-signed cert or can't validate
        #         "Connection Timeout=30;"
        #     )
        # Option 2: Windows Authentication (Integrated Security) - does not use DB_USER/DB_PASSWORD

        logger.info(f"Attempting Windows Authentication (Integrated Security) to {DB_SERVER}/{DB_NAME}")
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};" # Specify driver explicitly or remove if default works
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_NAME};"
            "Trusted_Connection=yes;" # Key for Windows Authentication
            # Recommended options for reliability:
            "Encrypt=no;"
            "TrustServerCertificate=no;"
            "Connection Timeout=30;"
        )

        # Establish connection
        conn = pyodbc.connect(conn_str, autocommit=False) # Start with autocommit off for transaction control
        logger.info(f"Successfully connected to SQL Server: {DB_SERVER}/{DB_NAME}")

        # Optional: Set connection properties if needed
        # conn.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
        # conn.setencoding(encoding='utf-8')

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
    """
    Executes SQL Server script content (potentially a batch with DECLARE)
    with parameters using pyodbc. Handles transaction commit/rollback.
    """
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
        rows_affected = cursor.rowcount
        conn.commit()  # Commit the transaction explicitly since autocommit is off

        logger.info(f"Successfully executed script and committed transaction. Rows affected: {rows_affected}")
        return True, rows_affected
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        logger.error(f"Error executing SQL Server script. SQLSTATE: {sqlstate}", exc_info=True)
        logger.error(f"Parameters passed: {params}") # Log parameters on error for debugging (be mindful of sensitive data)
        try:
            logger.warning("Attempting to roll back transaction due to error.")
            conn.rollback() # Rollback changes on error
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
        # Ensure the cursor is closed if it was created
        if cursor:
            cursor.close()
            logger.debug("Database cursor closed.")

# --- Example Table Setup Function (for demonstration) ---
# You would typically manage schema outside the application script (e.g., migrations)

def setup_sql_server_table(conn):
    """ Creates the example table if it doesn't exist (for demo purposes). """
    if not conn: return
    table_check_sql = """
    IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
                   WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'UserProfiles')
    BEGIN
        CREATE TABLE dbo.UserProfiles (
            UserID INT PRIMARY KEY,
            UserName NVARCHAR(100) NOT NULL UNIQUE,
            StatusCode INT DEFAULT 1, -- 1: Active, 2: Inactive, 3: Pending
            LastStatusChange DATETIME2 DEFAULT GETDATE(),
            StatusDescription NVARCHAR(100) NULL
        );
        -- Add some initial data for testing update
        INSERT INTO dbo.UserProfiles (UserID, UserName, StatusCode) VALUES (101, 'test_user_1', 1);
        INSERT INTO dbo.UserProfiles (UserID, UserName, StatusCode) VALUES (102, 'test_user_2', 1);
        PRINT 'Table dbo.UserProfiles created and sample data inserted.'
    END
    ELSE
        PRINT 'Table dbo.UserProfiles already exists.'
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(table_check_sql)
        conn.commit() # Commit schema changes if any
        logger.info("Checked/created dbo.UserProfiles table.")
    except pyodbc.Error as e:
        logger.error(f"Error setting up dbo.UserProfiles table: {e}", exc_info=True)
        conn.rollback() # Rollback if table creation fails
        raise

# --- Main Execution Logic ---

def main():
    """ Main function to orchestrate the process """
    logger.info("--- SQL Server Script Execution Started ---")
    sql_script_path = 'update_user_status.sql'
    conn = None

    try:
        # 1. Establish Database Connection
        conn = create_sql_server_connection()
        if not conn:

             logger.critical("Failed to establish database connection. Check configuration and logs.")
             return # Exit script if no connection

        # 2. Setup Database Table (for demo - usually done separately)
        setup_sql_server_table(conn) # Uncomment if needed for first run

        sql_script_path = 'D:\\LearnPython - Copy\\PythonPractice\\pandas\\update_user_status.sql'

        # 3. Read the SQL Script File
        sql_to_execute = read_sql_script(sql_script_path)

        # 4. Define Parameters for the Query
        # IMPORTANT: Order MUST match the '?' placeholders in update_user_status.sql
        # Placeholder 1 in SET: new_status_code
        # Placeholder 2 in SET: new_status_code
        # Placeholder 3 in WHERE: user_id
        # Parameter order for pyodbc: (param_for_first_?, param_for_second_?, ...)
        user_id_to_update = 101
        new_status = 2 # Update status to 'Inactive'

        # Parameters tuple in the order they appear in the script:
        # First ?: new_status_code (in SET @StatusDescription)
        # Second ?: new_status_code (in UPDATE SET StatusCode)
        # Third ?: user_id (in WHERE UserID)
        script_params = (
            new_status,        # Corresponds to the first '?' (in SET @StatusDescription)
            new_status,        # Corresponds to the second '?' (in UPDATE SET StatusCode)
            user_id_to_update  # Corresponds to the third '?' (in WHERE UserID)
        )
        logger.info(f"Preparing to execute script for UserID: {user_id_to_update} with New Status: {new_status}")

        # 5. Execute the Parametrized Script
        success, rows = execute_parametrized_sql_server_script(conn, sql_to_execute, script_params)

        if success:
            logger.info(f"SQL Server script executed successfully. Rows affected: {rows}")
            # You could add a SELECT query here to verify the update
        else:
            logger.error("SQL Server script execution failed. Check previous logs for errors.")

    except FileNotFoundError:
        logger.critical(f"Fatal Error: SQL script file '{sql_script_path}' not found.")
    except pyodbc.Error as db_err:
        # Catch errors specifically from pyodbc if not caught earlier (e.g., during setup)
        logger.critical(f"Fatal Database Error: {db_err}", exc_info=True)
    except Exception as e:
        # Catch any other unexpected exceptions
        logger.critical(f"An unexpected fatal error occurred: {e}", exc_info=True)
    finally:
        # 6. Close the Database Connection
        if conn:
            try:
                conn.close()
                logger.info("Database connection closed.")
            except pyodbc.Error as e:
                logger.error(f"Error closing the database connection: {e}", exc_info=True)
        logger.info("--- SQL Server Script Execution Finished ---")


if __name__ == "__main__":

    main()