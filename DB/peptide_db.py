import pymongo
from pymongo import MongoClient
import csv

class PeptideDB:
    def __init__(self, db_name="peptide", source_coll_name="source", peptide_coll_name="peptide"):
        # Connect to server
        self.client = MongoClient()
        # Use desired database
        self.db = self.client[db_name]
        # Define schemas for collections
        existing_dbs = self.client.database_names()
        if db_name not in existing_dbs:
            self.create_collections()
        # Create attributes for collections
        self.peptides = self.db[peptide_coll_name]
        self.sources = self.db[source_coll_name]

    def create_collections(self, source_coll_name="source", peptide_coll_name="peptide"):
        self.db.create_collection(peptide_coll_name, validator={
        "$and":
            [
                { "sequence": { "$type": "string" } },
                { "url": { "$type": "string" } }
            ],
        "$or":
            [
                { "anticancer": { "$type": "bool" } },
                { "antifungal": { "$type": "bool" } }
            ]
        })
        self.db.create_collection(source_coll_name, validator={ "$and":
            [
                { "url": { "$type": "string" } },
                { "institution": { "$type": "string" } },
                { "authors": { "$type": "string" } }
            ]
        })
        self.db[peptide_coll_name].create_index("sequence", unique=True)

    def import_csv(self, filepath, db_name):
        # Read csv
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            csv_list = list(reader)

        # Get source data from first row of 2D array
        database_authors = []
        for author in csv_list[0][2:]:
            database_authors.append(author)
        document_data = {}
        document_data["url"] = csv_list[0][0]
        document_data["institution"] = csv_list[0][1]
        document_data["authors"] = database_authors

        #save source url
        source_url = document_data["url"]

        # Insert source data
        result = {}
        result["source_insert"] = self.sources.insert_one(document_data)

        # Convert 2D array to array of dictionaries, starting from second row
        # Second row of 2D array is names of columns, rest are peptide data
        # URL of source is also added to each field as a reference to the source
        collection_data = []
        for row in csv_list[2:]:
            document_data = {}
            for count, value in enumerate(row):
                document_data[csv_list[1][count]] = self.convert_data_type(value)
            document_data["url"] = source_url
            collection_data.append(document_data)

        # insert into database
        result["peptide_insert"] = self.peptides.insert_many(collection_data)

        return result

    def convert_data_type(self, data):
        if data == "True":
            return True
        elif data == "False":
            return False
        return data
