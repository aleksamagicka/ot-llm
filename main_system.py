# import schema for chat messages and ChatOpenAI in order to query chatmodels GPT-3.5-turbo or GPT-4
import os
from time import sleep

from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain_openai import ChatOpenAI

from dkg import DKG
from dkg.providers import BlockchainProvider, NodeHTTPProvider

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

SPARQL_GENERATION_SELECT_TEMPLATE = """Task: Generate a SPARQL SELECT statement for querying a graph database.
The schema in JSON-LD format that outlines the structure and relationships of the data you have to generate a query
follows:

{
  "public": {
    "@context": "http://schema.org",
    "@type": "VisualArtwork",
    "@id": "https://origintrail.io/images/otworld/b0645ab1219ee33.jpg",
    "name": "",
    "description": "",
    "artform": "",
    "author": {
      "@type": "Person",
      "name": ""
    },
    "image": "https://origintrail.io/images/otworld/b0645ab1219ee33.jpg",
    "keywords": [
      "",
    ],
    "publisher": {
      "@type": "Person",
      "name": ""
    },
    "isBasedOn": {
      "@id": "",
      "isPartOf": ""
    }
    "additionalProperty": [
      {
        "@type": "PropertyValue",
        "name": "background",
        "value": ""
      },
      {
        "@type": "PropertyValue",
        "name": "skin",
        "value": ""
      },
      {
        "@type": "PropertyValue",
        "name": "eyes",
        "value": ""
      },
      {
        "@type": "PropertyValue",
        "name": "attires",
        "value": ""
      },
      {
        "@type": "PropertyValue",
        "name": "hair",
        "value": ""
      },
      {
        "@type": "PropertyValue",
        "name": "TrackTitle",
        "value": ""
      },
      {
        "@type": "PropertyValue",
        "name": "Artist",
        "value": ""
      },
      {
        "@type": "PropertyValue",
        "name": "ReleaseDate",
        "value": ""
      },
      {
        "@type": "PropertyValue",
        "name": "YearOfRecording",
        "value": ""
      },
      {
        "@type": "PropertyValue",
        "name": "imageSet",
        "value": ""
      },
      {
        "@type": "PropertyValue",
        "name": "imageNumber",
        "value": ""
      },
    ]
  }
}

An example SPARQL query that retrieves the artwork name, author, image and description looks like this:

SELECT ?artwork ?name ?description ?image ?author WHERE {
  ?artwork rdf:type schema:VisualArtwork;

  schema:name ?name;
  schema:description ?description;
  schema:image ?image;
  schema:author ?author;
}


Use that SPARQL query as inspiration for new queries. If you need to use CONTAINS in FILTER, do not convert to string using str.

This schema is focused on artworks and includes various properties such as the artist, description, art form and author, among others.
There are other instances of this schema which you'll need to account for, as this isn't the only one, so don't use its values literally.
Try to match parts of the prompt to additionalValues if possible. If a specific term is requested, try to match it to a field by using CONTAINS.
If a specific term is in plural, try to match it to a field by using contains for singular form and contains for plural form. 

If a specific term is requested, try to match it to the keywords array. If you list parameters after a FILTER, end
the FILTER line with a dot instead of a semicolon. Do not mark parameters as OPTIONAL.

Instructions:
Use only the node types and properties provided in the schema.
Do not use any node types and properties that are not explicitly provided. Use only the provided VisualArtwork schema. Do not use schema.org definitions.
Include all necessary prefixes.
Note: Be as concise as possible.
Do not include any explanations or apologies in your responses.
Do not respond to any questions that ask for anything else than for you to construct a SPARQL query.
Do not include any text except the SPARQL query generated.
Do not include a markdown specification for the generated code.

The question is:
{prompt}"""

chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

human_prompts = [
    "Give me all artworks whose name contains 'aleksa'",
    "Give me all artworks where author is 'aleksa'",
    "Give me all artworks related to fairies",
    "Give me all artworks related to fairies and elves, and their locations",
    "Show me artworks containing humans",
    "Show me artworks containing humans with black hair",
    "Show me artworks that are related to anime",
    "Show me some artwork on DKG with a flower motive",
    "Show me some artwork that can be described as 'cool'",
    "Give me all artworks, their names, and descriptions from author with name Leonardo Da Vinci"
]

jwt_token = os.environ['jwt_token']
node_provider = NodeHTTPProvider("https://proxima-node-38.origin-trail.network:8900", jwt_token)
blockchain_provider = BlockchainProvider(
    "mainnet",
    "otp:2043",
)

dkg = DKG(node_provider, blockchain_provider)

print(dkg.node.info)

# query_graph_result = dkg.graph.query(
#     """
# SELECT ?artwork ?name ?description ?image ?author
# WHERE {
#   ?artwork rdf:type schema:VisualArtwork;
#            schema:additionalProperty/schema:name ?property_name;
#            FILTER(CONTAINS(?property_name, "skin") || CONTAINS(?property_name, "eyes") || CONTAINS(?property_name, "attire") || CONTAINS(?property_name, "hair")).
#
#   ?artwork schema:name ?name;
#            schema:description ?description;
#            schema:image ?image;
#            schema:author ?author.
# }
#     """,
#     repository="publicCurrent",
# )

#print(query_graph_result)
#exit()


for prompt in human_prompts:
    print(f"{prompt}:\n")

    messages = [
        SystemMessage(content=SPARQL_GENERATION_SELECT_TEMPLATE),
        HumanMessage(content=prompt)
    ]
    response = chat(messages)

    print(response.content, end='\n')
    print("------------------------")

    sleep(30)

    cleaned_sparql = response.content.replace("```", "")
    print(dkg.graph.query(cleaned_sparql, repository="publicCurrent"))
    print("------------------------------------------------------------------")

