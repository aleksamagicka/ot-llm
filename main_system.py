# import schema for chat messages and ChatOpenAI in order to query chatmodels GPT-3.5-turbo or GPT-4
import os
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

SPARQL_GENERATION_SELECT_TEMPLATE = """Task: Generate a SPARQL SELECT statement for querying a graph database.
The schema in JSON-LD format that outlines the structure and relationships of the data you have to generate a query
follows, enclosed in backticks:
```
{
  "public": {
    "@context": "http://schema.org",
    "@type": "VisualArtwork",
    "@id": "https://origintrail.io/images/otworld/b0645ab1219ee33.jpg",
    "name": "Lyxen Demons #1108",
    "description": "Lyxifer in OriginTrail suit",
    "artform": "LSP8 PFP",
    "author": {
      "@type": "Person",
      "name": "CanvasLand &amp; Jhue"
    },
    "image": "https://origintrail.io/images/otworld/b0645ab1219ee33.jpg",
    "keywords": [
      "anime style",
      "character",
      "blue hair",
      "elf ears",
      "digital art"
    ],
    "publisher": {
      "@type": "Person",
      "name": "CanvasLandWeb3"
    },
    "additionalProperty": [
      {
        "@type": "PropertyValue",
        "name": "background",
        "value": "OnyxShadow"
      },
      {
        "@type": "PropertyValue",
        "name": "skin",
        "value": "Lyxifer"
      },
      {
        "@type": "PropertyValue",
        "name": "eyes",
        "value": "Intense"
      },
      {
        "@type": "PropertyValue",
        "name": "attires",
        "value": "OriginTrail"
      },
      {
        "@type": "PropertyValue",
        "name": "hair",
        "value": "Trunk"
      }
    ]
  }
}
```
This schema is focused on artworks and includes various properties such as the artist, description, art form and author, among others.
There are other instances of this schema which you'll need to account for, as this isn't the only one, so don't use its values literally
and try to match parts of the prompt to additionalValues if possible.
If the prompt asks for a name, try to match the appropriate name (of author or artwork). If the prompt contains keywords, try to match
them also to additional properties.

Instructions:
Use only the node types and properties provided in the schema.
Do not use any node types and properties that are not explicitly provided. Use only the provided VisualArtwork schema.
Include all necessary prefixes.
Note: Be as concise as possible.
Do not include any explanations or apologies in your responses.
Do not respond to any questions that ask for anything else than for you to construct a SPARQL query.
Do not include any text except the SPARQL query generated.

The question is:
{prompt}"""

chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

human_prompts = [
    "Give me all artworks whose name contains 'aleksa'",
    "Give me all artworks where author is 'aleksa'",
    "Give me all artworks related to anime",
]

for prompt in human_prompts:
    print(f"{prompt}:\n")
    print("```")

    messages = [
        SystemMessage(content=SPARQL_GENERATION_SELECT_TEMPLATE),
        HumanMessage(content=prompt)
    ]
    response = chat(messages)

    print(response.content, end='\n')
    print("```")
    print("------------------------")
