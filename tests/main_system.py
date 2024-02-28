# import schema for chat messages and ChatOpenAI in order to query chatmodels GPT-3.5-turbo or GPT-4
import os
from time import sleep

from langchain.schema import (
    HumanMessage,
    SystemMessage
)
from langchain_openai import ChatOpenAI

from dkg import DKG
from dkg.providers import BlockchainProvider, NodeHTTPProvider

from dotenv import load_dotenv, find_dotenv

from consts import SPARQL_GENERATION_SELECT_TEMPLATE

load_dotenv(find_dotenv())

human_prompts = [
    "Give me all artworks whose name contains 'aleksa'",
    "Show me artworks where name contains mona",
    "Give me all artworks where author is 'aleksa'",
    "Give me all artworks related to fairies",
    "Give me all artworks related to fairies and elves, and their locations",
    "Show me artworks containing humans",
    "Show me artworks containing humans with black hair",
    "Show me artworks that are related to anime",
    "Show me some artwork on DKG with a flower motive",
    "Show me some artwork that can be described as 'cool'",
    "Give me all artworks, their names, and descriptions from author with name Leonardo Da Vinci",
    "Give me all artworks"
]

chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

jwt_token = os.environ['jwt_token']
node_provider = NodeHTTPProvider(os.environ['node_url'], jwt_token)
blockchain_provider = BlockchainProvider(
    "mainnet",
    "otp:2043",
)

dkg = DKG(node_provider, blockchain_provider)
try:
    print(dkg.node.info)
except:
    print("Error: couldn't connect to DKG node!")
    exit()

query_graph_result = dkg.graph.query(
    """
SELECT DISTINCT ?artwork ?name ?description ?image ?author ?ual WHERE {
  ?artwork rdf:type schema:VisualArtwork.
    GRAPH ?g {
    ?artwork schema:name ?name;
    schema:description ?description;
    schema:keywords ?keywords;
    schema:image ?image;
    (schema:author/schema:name) ?author.
    FILTER(CONTAINS(?keywords, "anime"))
  }
  ?ual schema:assertion ?g.
}
    """,
    repository="privateCurrent",
)

print(query_graph_result)
exit()


for prompt in human_prompts:
    print(f"{prompt}:\n")

    messages = [
        SystemMessage(content=SPARQL_GENERATION_SELECT_TEMPLATE),
        HumanMessage(content=prompt)
    ]
    response = chat(messages)
    cleaned_sparql = response.content.replace("```", "")

    print(cleaned_sparql, end='\n')
    print("------------------------")

    sleep(30)

    print(dkg.graph.query(cleaned_sparql, repository="publicCurrent"))
    print("------------------------------------------------------------------")

