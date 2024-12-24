import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv(verbose=True)
NEO4J_URI = os.environ['NEO4J_URI']
NEO4J_USER = os.environ['NEO4J_USER']
NEO4J_PASSWORD = os.environ['NEO4J_PASSWORD']

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)


def init_neo4j():
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")