import os
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI


from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

if __name__ == '__main__':
    db = SQLDatabase.from_uri("sqlite:///Chinook.db")

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    chain = create_sql_query_chain(llm, db)
    response = chain.invoke({"question": "How many employees are there"})
    print(response)

    print(db.run(response))

    print()
    #chain.get_prompts()[0].pretty_print()