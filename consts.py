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
    "@id": "",
    "name": "",
    "description": "",
    "artform": "",
    "author": {
      "@type": "",
      "name": ""
    },
    "image": "",
    "keywords": [
      "",
    ],
    "publisher": {
      "@type": "",
      "name": ""
    },
    "isBasedOn": {
      "@id": "",
      "isPartOf": ""
    }
  }
}

An example SPARQL query that retrieves the artwork name, author, image, ual, description and other attributes
looks like this in markdown format:

```
SELECT DISTINCT ?artwork ?artworkName ?description ?artform ?imageURL ?authorName ?ual WHERE {
  GRAPH ?g {
      ?artwork a schema:VisualArtwork;
      schema:name ?artworkName;
      schema:description ?description;
      schema:keywords ?keywords;
      schema:image ?imageURL;
      schema:artform ?artform;
      (schema:author/schema:name) ?authorName;
  }
  ?ual schema:assertion ?g.
  filter(!regex(str(?ual), "^did:dkg:otp/") )
}
```

Use that SPARQL query as inspiration for new queries. If you need to use CONTAINS in FILTER, do not convert to string 
using str. Always include the GRAPH block as shown. Always include ?ual in the SELECT query. Always include the filter
with the regex as in the example.

This schema is focused on artworks and includes various properties such as the artist, description, art form, 
keywords and author, among others. There are other instances of this schema which you'll need to account for, 
as this isn't the only one, so don't use its values literally. If a specific term is requested, match it to keywords, 
description and name using CONTAINS. When matching to description or name, match in lowercase using LCASE. All terms 
describing artworks should be considered. If a specific term is in plural form, match it to keywords and description 
by using CONTAINS with the singular form. For example, if asked for the presence of animals, search both keywords, 
description and name for 'animal'. Do the same for all such terms in the query. ALWAYS check presence of specific 
term in keywords. Include keywords in every SELECT query where keywords are present in a FILTER clause.

When searching for a specific author, use a FILTER clause and do not include the author name in the list of parameters.
Always put FILTER clause after the parameters you're requesting in WHERE.

An example query for searching artworks by a specific author name looks like this:

SELECT DISTINCT ?artwork ?name ?description ?image ?authorName ?ual WHERE {
GRAPH ?g {
  ?artwork a schema:VisualArtwork;
  schema:name ?name;
  schema:description ?description;
  schema:keywords ?keywords;
  schema:image ?image;
  (schema:author/schema:name) ?authorName.
  
  FILTER(?authorName, "<author_query>")
 }
 ?ual schema:assertion ?g.
 filter(!regex(str(?ual), "^did:dkg:otp/") )
}

You will need to replace <author_query> in the FILTER clause with the given author name, with double quotes around it.

If you list parameters after a FILTER, end the FILTER line with a dot instead of a semicolon. Always put FILTER 
statements last. In case of multiple CONTAINS in a FILTER statement, put parenthesis around them. In filter 
statements, use '!' instead of NOT for negation. In FILTER statements, search both keywords and description unless 
otherwise instructed. In filter statements, group negated CONTAINS together and put parenthesis around them.

Instructions: Use only the node types and properties provided in the schema. Do not use any node types and properties 
that are not explicitly provided. Use only the provided VisualArtwork schema. Do not use schema.org definitions. 
Include all necessary prefixes. Note: Be as concise as possible. Do not include any explanations or apologies in your 
responses. Do not respond to any questions that ask for anything else than for you to construct a SPARQL query. Do 
not include any text except the SPARQL query generated. Do not include a markdown specification for the generated code.
Always put FILTER clauses at the end of WHERE section.

The question is:
{prompt}"""

"""
Seems to work better without these:

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
"""

IS_ARTWORK_RELATED_PROMPT="""
Task: determine whether the given prompt mentions art, artworks, or is requesting information about artworks, or
contains word artwork or a synonym, or it's general motive is related to artworks.
Sample queries that are related to artworks are as follows and should be answered YES, enclosed in quotes are as follows:

"Give me all artworks related to fairies",
"Give me all artworks related to fairies and elves, and their locations",
"Show me artworks containing humans",
"Show me artworks containing humans with black hair",
"Show me artworks that are related to anime",
"Show me some artwork on DKG with a flower motive",
"Show me some artwork that can be described as 'cool'",
"Give me all artworks, their names, and descriptions from author with name Leonardo Da Vinci",
"Give me all artworks"

Instructions:
Output YES or NO whether the given prompt matches the rules.
Do not include any explanations or apologies in your responses. Do not respond to any questions that ask for anything
else than for you to output a percentage. Do not include a markdown specification. Only include YES or NO in your answer.

The prompt is:
{prompt}
"""