from app.db.neo4j.database_config import driver


def insert_bulk_data(data):
    with driver.session() as session:
        session.write_transaction(insert_bulk_records, data)


def insert_bulk_records(tx, data):
    cypher_query = """
       UNWIND $data AS record

       WITH record
       WHERE record.Region IS NOT NULL
       MERGE (region:Region {name: record.Region})

       WITH record, region
       WHERE record.Country IS NOT NULL
       MERGE (country:Country {name: record.Country})

       WITH record, region, country
       WHERE record.State IS NOT NULL
       MERGE (state:State {name: record.State})

       WITH record, region, country, state
       WHERE record.City IS NOT NULL
       MERGE (city:City {name: record.City, lat: coalesce(record.lat, 0.0), lon: coalesce(record.lon, 0.0)})

       WITH record, region, country, state, city
       WHERE record.Attack_type IS NOT NULL
       MERGE (attackType:Attack_Type {name: record.Attack_type})
        
       WITH record, region, country, state, city, attackType
       WHERE record.Target_type IS NOT NULL
       MERGE (targetType:Target_Type {name: record.Target_type})

       MERGE (event:Event {date: record.date})
       MERGE (region)-[:CONTAINS]->(country)
       MERGE (country)-[:CONTAINS]->(state)
       MERGE (state)-[:CONTAINS]->(city)
       MERGE (event)-[:HAPPENED_IN]->(city)
       MERGE (event)-[:HAS_ATTACK_TYPE]->(attackType)
       MERGE (event)-[:TARGETED]->(targetType)
       
       WITH record, event
       UNWIND record.Group_name AS groupName
       MERGE (group:Group_Name {name: groupName})
       MERGE (event)-[:COMMITTED_BY]->(group)
       """

    tx.run(cypher_query, data=data)
