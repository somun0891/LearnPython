import configparser
import subprocess
import pandas as pd
from io import StringIO

# Load config
config = configparser.ConfigParser()
config.read('PythonPractice\pandas\config.ini')

# Get values
server = config['database']['server']
database = config['database']['database']
user = config['database']['user']
password = config['database']['password']

# Query to run
query = "SELECT TOP 10 * FROM person.ContactType"

# sqlcmd command
cmd = [
    'sqlcmd',
    '-S', server,
    '-d', database,
    '-U', user,
    '-P', password,
    '-Q', query,
    '-s', ',',
    '-W'
]

# Run sqlcmd
result = subprocess.run(cmd, capture_output=True, text=True)


print(result.stdout)
# Check for errors
if result.returncode != 0:
    print("SQLCMD Error:", result.stderr)
else:
    output = result.stdout.strip()
    lines = output.splitlines()

    # Find the line with column headers (first line with commas)
    header_index = next(i for i, line in enumerate(lines) if ',' in line)
    csv_data = '\n'.join(lines[header_index:])

    # Convert to DataFrame
    df = pd.read_csv(StringIO(csv_data))
    print(df)



# import re
# import os

# # Sample text with placeholders
# text = "Database user is <DB_USER> and password is <DB_PASS>"

# # Replacement function
# def replace_env_var(match):
#     var_name = match.group(1)
#     return os.environ.get(var_name, f"<{var_name}>")  # Keeps original if var is not set

# # Pattern to match <VAR_NAME>
# pattern = r'<(.*?)>'

# # Replace using re.sub with a function
# result = re.sub(pattern, replace_env_var, text)

# print(result)
