import pandas as pd
# import mysql.connector
from sqlalchemy import create_engine, Column, Integer, Numeric, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the connection parameters

user = ''
password = ''
host = 'localhost'  # or your MySQL server address
# host = '34.95.145.117'
database = 'hydronet'
port = '34470'

# # Create a SQLAlchemy engine
engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}')

add_primary_key_sql = """
ALTER TABLE dados_sensores
ADD PRIMARY KEY (ID);
"""

try:
    # Read the CSV file into a pandas DataFrame
    file_path = 'dados_sensores_updated.csv'
    df = pd.read_csv(file_path, delimiter=',')
    df['ID'] = range(len(df))
    df['ID'] = df['ID'] + 1

    # Write the DataFrame to the MySQL table using the SQLAlchemy engine
    df.to_sql('dados_sensores', con=engine, if_exists='replace', index=False)
    with engine.connect() as con:
        con.execute(text(add_primary_key_sql))

    print("Data imported successfully!")
except Exception as e:
    print(f"An error occurred: {e}")

add_primary_key_sql = """
ALTER TABLE dados_met
ADD PRIMARY KEY (ID);
"""

try:
    # Read the CSV file into a pandas DataFrame
    file_path = 'dados_met_updated.txt'
    df = pd.read_csv(file_path, delimiter=';')
    df['ID'] = range(len(df))
    df['ID'] = df['ID'] + 1

    # Write the DataFrame to the MySQL table using the SQLAlchemy engine
    df.to_sql('dados_met', con=engine, if_exists='replace', index=False)
    with engine.connect() as con:
        con.execute(text(add_primary_key_sql))

    print("Data imported successfully!")
except Exception as e:
    print(f"An error occurred: {e}")
