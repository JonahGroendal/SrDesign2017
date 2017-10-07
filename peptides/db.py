import pymongo
from pymongo import MongoClient
import csv
import definitions  # for field names

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
        # Create dictionary of fields for each collection
        self.collection_fields = {}
        self.collection_fields["peptide"] = definitions.peptide
        self.collection_fields["source"] = definitions.source

    def create_collections(self, source_coll_name="source", peptide_coll_name="peptide"):
        self.db.create_collection(peptide_coll_name)
        self.db.create_collection(source_coll_name)
        self.db[peptide_coll_name].create_index("sequence", unique=True)
        self.db[source_coll_name].create_index("url", unique=True)

    def import_csv(self, filepath, db_name="peptide", delimiter="|"):
        # Read csv
        with open(filepath, 'r') as f:
            reader = csv.reader(f, delimiter=delimiter)
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
        try:
            print(document_data)
            self.sources.insert_one(document_data)
        except pymongo.errors.DuplicateKeyError:
            print("Source already exists. Updating...")
            # Remove _id field that was automatically added by insert_one()
            document_data.pop("_id")
            self.sources.update({"url": document_data["url"]}, document_data)

        # Convert 2D array to array of dictionaries, starting from second row
        # Second row of 2D array is names of fields, rest are peptide data
        # URL of source is also added to each field as a reference to the source
        # Only fields in collection_data["peptide"] will be added, others will be skipped
        collection_data = []
        for row in csv_list[2:]:
            document_data = {}
            for count, value in enumerate(row):
                if csv_list[1][count] in collection_fields["peptide"]:
                    document_data[csv_list[1][count]] = self.convert_data_type("peptide", csv_list[1][count], value)
            document_data["url"] = source_url
            collection_data.append(document_data)

        # Insert into database
        # If there's a DuplicateKeyError (1100), update document instead
        try:
            self.peptides.insert_many(collection_data, ordered=False)
        except pymongo.errors.BulkWriteError as e:
            for count, write_error in enumerate(e.details['writeErrors']):
                if write_error["code"] == 11000:
                    fields = write_error["op"]
                    fields.pop("_id")
                    self.peptides.update({"sequence": write_error["op"]["sequence"]}, fields)
                    print("Updated peptide", write_error["op"]["sequence"])
                else:
                    print("something went wrong")

    def validate_document(self, doc, source_or_peptide):
        pass

    def convert_data_type(self, coll_name, field_name, data):
        # If this field's data type is bool, convert by hand
        if self.collection_fields[coll_name][field_name]["type"] is bool:
            if data == "1" or data == "True" or data == "true":
                return True
            elif data == "0" or data == "False" or data == "false":
                return False
            else:
                return bool(data)
        # Otherwise use this data type's function for conversion
        else:
            return self.collection_fields[coll_name][field_name]["type"](data)
