import os
import pyodbc
import pandas as pd
import helper

# Define veriables
driver = "{ODBC Driver 18 for SQL Server}"
username = os.environ.get("SQL_SERVER_USERNAME")
server = os.environ.get("SQL_SERVER_ENDPOINT")
password = os.environ.get("SQL_SERVER_PASSWORD")  
database = os.environ.get("SQL_SERVER_DATABASE")

print(f'uid:{username}, server;{server}, database:{database}')

# Load titanic dataset into a pandas dataframe
titanic = pd.read_csv("titanic.csv").fillna(value=0)
#print(titanic.head())

# Connect to Azure SQL DB
cnxn = pyodbc.connect(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}')  
cursor = cnxn.cursor()  

# Define the create table statement
create_table_query = """
CREATE TABLE Passengers (
    PassengerId int PRIMARY KEY,
    Survived bit NOT NULL,
    Pclass int NOT NULL,
    Name varchar(100) NOT NULL,
    Sex varchar(10) NOT NULL,
    Age float NULL,
    SibSp int NOT NULL,
    Parch int NOT NULL,
    Ticket varchar(20) NOT NULL,
    Fare float NOT NULL,
    Cabin varchar(20) NULL,
    Embarked char(1) NULL
);
"""

# Execute the statement using cursor.execute
cursor.execute(create_table_query)

for index, row in titanic.iterrows():
     cursor.execute(
        "INSERT INTO dbo.[Passengers] (PassengerId, Survived, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked) values(?,?,?,?,?,?,?,?,?,?,?,?)",
        row.PassengerId,
        row.Survived,
        row.Pclass,
        row.Name,
        row.Sex,
        row.Age,
        row.SibSp,
        row.Parch,
        row.Ticket,
        row.Fare,
        row.Cabin,
        row.Embarked
     )
cnxn.commit()
cursor.close()