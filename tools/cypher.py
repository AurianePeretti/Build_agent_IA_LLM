import streamlit as st
from llm import llm
from graph import graph

from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
# allows us to create a QA Chain that generates Cypher: Gra^hCypherQAChain

from langchain.prompts.prompt import PromptTemplate

# Create the Cypher QA chain


# CYPHER_GENERATION_TEMPLATE = """
# You are an expert Neo4j Developer translating user questions into Cypher to answer questions about movies and provide recommendations.
# Convert the user's question based on the schema.

# Use only the provided relationship types and properties in the schema.
# Do not use any other relationship types or properties that are not provided.

# Do not return entire nodes or embedding properties.

# Fine Tuning:

# For movie titles that begin with "The", move "the" to the end. For example "The 39 Steps" becomes "39 Steps, The" or "the matrix" becomes "Matrix, The".


# Schema:
# {schema}

# Question:
# {question}

# Cypher Query:
# """

CYPHER_GENERATION_TEMPLATE = """
You are an expert Neo4j Developer translating user questions into Cypher to answer questions about movies and provide recommendations.
Convert the user's question based on the schema.

Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.

Do not return entire nodes or embedding properties.

Fine Tuning:

For movie titles that begin with "The", move "the" to the end. For example "The 39 Steps" becomes "39 Steps, The" or "the matrix" becomes "Matrix, The".

Example Cypher Statements:

1. To find who acted in a movie:
```
MATCH (p:Person)-[r:ACTED_IN]->(m:Movie {{title: "Movie Title"}})
RETURN p.name, r.role
```

2. To find who directed a movie:
```
MATCH (p:Person)-[r:DIRECTED]->(m:Movie {{title: "Movie Title"}})
RETURN p.name
```

3. How to find how many degrees of separation there are between two people:
```
// Ajouter Viola Davis
CREATE (p:Person {name: "Viola Davis", born: 1965, tmdbId: "11883"});

// Ajouter Kevin Bacon
CREATE (p:Person {name: "Kevin Bacon", born: 1958, tmdbId: "4724"});

MATCH path = shortestPath(
  (p1:Person {name: "Viola Davis"})-[:ACTED_IN|DIRECTED*]-(p2:Person {name: "Kevin Bacon"})
)
WITH path, p1, p2, relationships(path) AS rels
RETURN
  p1 { .name, .born, link:'https://www.themoviedb.org/person/'+ p1.tmdbId } AS start,
  p2 { .name, .born, link:'https://www.themoviedb.org/person/'+ p2.tmdbId } AS end,
  reduce(output = '', i IN range(0, length(path)-1) |
    output + CASE
      WHEN i = 0 THEN
        startNode(rels[i]).name + CASE WHEN type(rels[i]) = 'ACTED_IN' THEN ' played '+ rels[i].role +' in ' ELSE ' directed ' END + endNode(rels[i]).title
      ELSE
        ' with '+ startNode(rels[i]).name + ', who '+ CASE WHEN type(rels[i]) = 'ACTED_IN' THEN 'played '+ rels[i].role +' in ' ELSE 'directed ' END + endNode(rels[i]).title
    END
  ) AS pathBetweenPeople;

```

Schema:
{schema}

Question:
{question}
"""




cypher_prompt = PromptTemplate.from_template(CYPHER_GENERATION_TEMPLATE)



cypher_qa = GraphCypherQAChain.from_llm(

    llm,
    graph = graph,
    verbose = True,
    cypher_prompt = cypher_prompt
)

# The GraphCypherQAChain provides a static .fom_llm() method for creating a new instance
# La chaîne utilisera la classe Neo4j pour pouvoir écrire un Cyher et l'éxecuter dans la databse du graph