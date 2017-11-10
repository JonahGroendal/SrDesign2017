import pymongo
from pymongo import MongoClient
import definitions
import errors
import csv_tools

class DB:
    def __init__(self, db_name, collection_definitions):
        self.db_name = db_name
        self.collection_defs = collection_definitions
        # Connect to server
        self.client = MongoClient()
        # Use desired database
        self.db = self.client[db_name]
        # Create and index collections
        existing_dbs = self.client.database_names()
        if self.db_name not in existing_dbs:
            print("Creating collections...")
            self.create_collections()

    # Creates and indexes collections based on their definitions
    def create_collections(self):
        for collection in self.collection_defs:
            self.db.create_collection(collection["name"])
            collection_keys = []
            for field in self.indexed_fields(collection):
                if field in self.unique_indexed_fields(collection):
                    collection_keys.append((field, 1))
                else:
                    self.db[collection["name"]].create_index(field, unique=False)
            if len(collection_keys) > 0:
                self.db[collection["name"]].create_index(collection_keys, unique=True)

    # Can recursively convert data from within nested lists
    def convert_data_type(self, field_definition, data):
        if type(field_definition["data_type"]) is dict and \
           list in field_definition["data_type"]:
            if type(data) is not list:
                data = list((data,))
            for value in data:
                value = self.convert_data_type(field_definition["data_type"][list], value)
            return data
        # If this field's data type is bool, convert by hand
        elif field_definition["data_type"] is bool:
            if data == "1" or data == "True" or data == "true":
                return True
            elif data == "0" or data == "False" or data == "false":
                return False
            else:
                return bool(data)
        # Otherwise use this data type's function for conversion
        else:
            return field_definition["data_type"](data)

    # Returns fields with attribute "indexed" (unique or otherwise)
    def indexed_fields(self, collection):
        for field in collection["fields"]:
            if "indexed" in collection["fields"][field]:
                yield field
    # Returns fields with attribute "indexed":{"unique":True}
    def unique_indexed_fields(self, collection):
        for field in collection["fields"]:
            if "indexed" in collection["fields"][field]:
                if collection["fields"][field]["indexed"]["unique"] is True:
                    yield field

class PeptideDB(DB):
    def __init__(self, db_name="peptide"):
        self.source_coll_def = definitions.collection_source
        self.peptide_coll_def = definitions.collection_peptide
        super().__init__(db_name, (self.source_coll_def, self.peptide_coll_def))
        self.sources = self.db[self.source_coll_def["name"]]
        self.peptides = self.db[self.peptide_coll_def["name"]]

    def import_dataset(self, filepath, source_doc):
        # Import cleaned csv back into a Dataset object
        dataset = csv_tools.Dataset(csv_filepath=filepath)

        # Insert source document and save its ID
        source_id = self.insert_source_doc(source_doc, replace_existing=True)

        for peptide_doc in dataset:
            # Convert strings to correct data types
            for field_name in peptide_doc:
                peptide_doc[field_name] = self.convert_data_type(
                        self.peptide_coll_def["fields"][field_name],
                        peptide_doc[field_name])
            # Insert into database
            try:
                self.insert_peptide_doc(peptide_doc, source_id)
            # If already in database, augment existing document instead
            except pymongo.errors.WriteError:
                uif = list(self.unique_indexed_fields(self.peptide_coll_def))
                peptide_doc_uif = {k: v for k, v in peptide_doc.items() if k in uif}
                print("{0} already exists. Merging data...".format(peptide_doc_uif))
                self.augment_peptide_doc(peptide_doc, source_id)

    def insert_peptide_doc(self, peptide_doc, source_id):
        peptide_doc = self.embed_source_id(peptide_doc, source_id)
        self.peptides.insert_one(peptide_doc)

    def augment_peptide_doc(self, fields_to_add, source_id):
        fields_to_add = self.embed_source_id(fields_to_add, source_id)
        uif = list(self.unique_indexed_fields(self.peptide_coll_def))
        fields_to_add_uif = {k: v for k, v in fields_to_add.items() if k in uif}
        fields_to_add = {k: v for k, v in fields_to_add.items() if k not in uif}
        peptide_doc = self.peptides.find_one(fields_to_add_uif)

        for field in fields_to_add:
            if field in peptide_doc:
                if type(fields_to_add[field]) is list:
                    for v1 in fields_to_add[field]:
                        for v2 in peptide_doc[field]:
                            if v1["value"] == v2["value"]:
                                for s in v2["references"]:
                                    if s not in v1["references"]:
                                        v1["references"].append(s)
                elif fields_to_add[field]["value"] != peptide_doc[field]["value"]:
                    peptide_doc.pop("_id")
                    fields_to_add.update(fields_to_add_uif)
                    #peptide_doc = self.remove_source_id(peptide_doc)
                    #fields_to_add = self.remove_source_id(fields_to_add)
                    raise errors.ConflictingUpdateError(peptide_doc, fields_to_add)
                elif fields_to_add[field]["references"][0] not in peptide_doc[field]["references"]:
                    fields_to_add[field]["references"].extend(peptide_doc[field]["references"])
            fields_to_add_update = {"$set": fields_to_add}
            self.peptides.update(fields_to_add_uif, fields_to_add_update)

    def insert_source_doc(self, source_doc, replace_existing=False):
        source_id = None
        try:
            self.sources.insert_one(source_doc)
        except pymongo.errors.DuplicateKeyError:
            if replace_existing:
                print("Source already exists. Updating...")
                # Remove _id field that was automatically added by insert_one()
                source_doc.pop("_id")
                self.sources.update({"url": source_doc["url"]}, source_doc)
                source_id = self.sources.find_one({"url": source_doc["url"]})["_id"]
            else:
                raise
        else:
            source_id = source_doc["_id"]
        return source_id

    def embed_source_id(self, peptide_doc, source_id):
        doc = {}
        for field in peptide_doc:
            if field in self.unique_indexed_fields(self.peptide_coll_def):
                # Don't embed source_id
                doc[field] = peptide_doc[field]
            else:
                # Embed source_id
                if type(peptide_doc[field]) is list:
                    doc[field] = []
                    for value in peptide_doc[field]:
                        doc[field].append({"value": value, "references": [source_id]})
                else:
                    doc[field] = {"value": peptide_doc[field], "references": [source_id]}
        return doc

    def remove_source_id(self, peptide_doc):
        doc = {}
        doc = dict(peptide_doc)
        for field in doc:
            if type(doc[field]) is dict and "value" in doc[field]:
                doc[field] = doc[field]["value"]
        return doc
