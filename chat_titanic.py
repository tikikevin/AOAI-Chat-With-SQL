import os
import helper
from sqlalchemy import create_engine
from langchain_openai import AzureChatOpenAI
from langchain.agents import AgentType
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

# To use this code, make sure you setup environment variables for the following:
# OPENAI_CHAT_MODEL
# OPENAI_API_BASE
# SQL_SERVER_ENDPOINT
# SQL_TITANIC_USERNAME
# SQL_TITANIC_PASSWORD
# SQL_DATABASE_NAME

driver = '{ODBC Driver 18 for SQL Server}'
odbc_str = 'mssql+pyodbc:///?odbc_connect=' \
                'Driver='+driver+ \
                ';Server=' + os.getenv("SQL_SERVER_ENDPOINT") +';PORT=1433' + \
                ';DATABASE='+ os.getenv("SQL_SERVER_ENDPOINT") + \
                ';Uid=' + os.getenv("SQL_TITANIC_USERNAME") + \
                ';Pwd=' + os.getenv("SQL_TITANIC_PASSWORD") + \
                ';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

db_engine = create_engine(odbc_str)

llm = AzureChatOpenAI(model=os.getenv("OPENAI_CHAT_MODEL"),
                      azure_endpoint=os.getenv("OPENAI_API_BASE"),
                      deployment_name=os.getenv("OPENAI_CHAT_MODEL"),
                      temperature=0)

from langchain.prompts.chat import ChatPromptTemplate

final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", 
         """
          You are a helpful AI assistant expert in querying Microsoft SQL Databases using Microsoft T-SQL to find answers to user's question about the Titanic Passenger Registry.
          Do not answer questions that aren't related to the Titanic Passenger Manifest Data. The Passenger Manifest is called 'Passengers'.
         """
         ),
        ("user", "{question}\n ai: "),
    ]
)

db = SQLDatabase(db_engine)

sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)
sql_toolkit.get_tools()

sqldb_agent = create_sql_agent(
    llm=llm,
    toolkit=sql_toolkit,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)


def prompt(prompt):
    sqldb_agent.invoke(final_prompt.format(
            #question="How many passengers were there?"
            #question="What was the survival rate percentage in terms of gender and compared to all passengers including those that didn't survive?"
            question=prompt

    ))

# prompt("How many passengers were there?")
user_prompt = ''

while user_prompt != 'bye':
    print("ask a question:")
    user_prompt = input()
    prompt(user_prompt)