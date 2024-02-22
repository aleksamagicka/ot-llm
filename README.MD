# SPARQL generation for DKG Artworks using GPT models

The main file is `main_system.py`, which uses GPT to generate SPARQL queries for the artwork data in the OriginTrail DKG.

Examples of outputs:

```
Give me all artworks whose name contains 'aleksa':

SELECT ?artwork ?name ?description ?image ?author
WHERE {
  ?artwork rdf:type schema:VisualArtwork;
           schema:name ?name;
           schema:description ?description;
           schema:image ?image;
           schema:author ?author.
  FILTER(CONTAINS(?name, "aleksa"))
}
------------------------
[]
------------------------------------------------------------------
Give me all artworks where author is 'aleksa':

SELECT ?artwork ?name ?author
WHERE {
  ?artwork rdf:type schema:VisualArtwork;
           schema:author ?author.
  FILTER(CONTAINS(?author, "aleksa"))
}
------------------------
[]
------------------------------------------------------------------
Give me all artworks related to fairies:

SELECT ?artwork ?name ?description ?image ?author
WHERE {
  ?artwork rdf:type schema:VisualArtwork;
           schema:keywords ?keywords;
           schema:name ?name;
           schema:description ?description;
           schema:image ?image;
           schema:author ?author.
  FILTER (CONTAINS(?keywords, "fairy"))
}
------------------------
[]
------------------------------------------------------------------
Give me all artworks related to fairies and elves, and their locations:

SELECT ?artwork ?name ?description ?image ?author ?location WHERE {
  ?artwork rdf:type schema:VisualArtwork;
           schema:keywords ?keyword;
           schema:name ?name;
           schema:description ?description;
           schema:image ?image;
           schema:author ?author.
  FILTER (CONTAINS(?keyword, "fairy") || CONTAINS(?keyword, "elf"))
  OPTIONAL { ?artwork schema:location ?location }
}
------------------------
[]
------------------------------------------------------------------
Show me artworks containing humans:

SELECT ?artwork ?name ?image ?author
WHERE {
  ?artwork rdf:type schema:VisualArtwork;
           schema:name ?name;
           schema:image ?image;
           schema:author ?author;
           schema:keywords ?keywords.
  FILTER (CONTAINS(?keywords, "human")).
}
------------------------
[]
------------------------------------------------------------------
Show me artworks containing humans with black hair:

SELECT ?artwork ?name ?image ?author
WHERE {
  ?artwork rdf:type schema:VisualArtwork;
           schema:additionalProperty/schema:name "hair";
           schema:additionalProperty/schema:value "black";
           schema:additionalProperty/schema:name "attires";
           schema:additionalProperty/schema:value ?attires;
           schema:image ?image;
           schema:author ?author;
  FILTER(CONTAINS(?attires, "human"))
}
------------------------
[]
------------------------------------------------------------------
Show me artworks that are related to anime:

SELECT ?artwork ?name ?description ?image ?author
WHERE {
  ?artwork rdf:type schema:VisualArtwork;
           schema:keywords ?keyword;
           schema:name ?name;
           schema:description ?description;
           schema:image ?image;
           schema:author ?author.
  FILTER (CONTAINS(?keyword, "anime"))
}
------------------------
[{'artwork': 'https://t.co/gCHdCKJl75', 'author': '_:t1977794', 'image': 'https://t.co/gCHdCKJl75', 'name': '"anime guy"', 'description': '"wow cool"'}]
------------------------------------------------------------------
Show me some artwork on DKG with a flower motive:

SELECT ?artwork ?name ?image
WHERE {
  ?artwork rdf:type schema:VisualArtwork;
           schema:keywords ?keywords.
  FILTER (CONTAINS(?keywords, "flower")).
  ?artwork schema:name ?name;
           schema:image ?image.
}
------------------------
[]
------------------------------------------------------------------
Show me some artwork that can be described as 'cool':

SELECT ?artwork ?name ?description ?image ?author
WHERE {
  ?artwork rdf:type schema:VisualArtwork;
           schema:keywords ?keywords;
           schema:name ?name;
           schema:description ?description;
           schema:image ?image;
           schema:author ?author.
  FILTER (CONTAINS(?keywords, "cool"))
}
------------------------
[]
------------------------------------------------------------------
Give me all artworks, their names, and descriptions from author with name Leonardo Da Vinci:

SELECT ?artwork ?name ?description
WHERE {
  ?artwork rdf:type schema:VisualArtwork;
           schema:author [
             rdf:type schema:Person;
             schema:name "Leonardo Da Vinci"
           ];
           schema:name ?name;
           schema:description ?description.
}
------------------------
[]
------------------------------------------------------------------
```

