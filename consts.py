"""
TODO:
isBasedOn? It doesn't know if it's empty or not
additionalValues? They can be named whatever, it can't make up proper attribute names
"""

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
Try to match parts of the prompt to additionalValues if possible by using OPTIONAL, since they may not exist. If a specific term is requested, try to match it to a field by using CONTAINS.
If a specific term is in plural, match it to a field by using CONTAINS for singular form.

If isBasedOn is not empty, use it to retrieve the referenced artwork.

If a specific term is requested, try to match it to the keywords array. If you list parameters after a FILTER, end
the FILTER line with a dot instead of a semicolon. Always put FILTER statements last.

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