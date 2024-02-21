import os
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI

from langchain.chains import GraphSparqlQAChain
from langchain_community.graphs import RdfGraph

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

if __name__ == '__main__':
    graph = RdfGraph(
        source_file="https://pastebin.com/raw/HVencPXt",
        standard="json-ld",
        local_copy="test.ttl",
    )

    graph.load_schema()

    def query_name():
        q = """
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    
            SELECT ?name
            WHERE {
                ?p rdf:type foaf:Person .
                ?p foaf:name ?name .
            }
        """

        # Apply the query to the graph and iterate through results
        for r in graph.query(q):
            print(r["name"])

    def query_from_gpt():
        chain = GraphSparqlQAChain.from_llm(
            ChatOpenAI(temperature=0), graph=graph, verbose=True
        )

        chain.invoke({'query': "What is the artwork name?"})

    #query_name()
    query_from_gpt()
