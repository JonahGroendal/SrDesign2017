import pymongo
from pymongo import MongoClient
import definitions
import errors
import csv_tools

class DB:
    def __init__(self, db_name, collection_definitions):
        self.db_name = db_name
        self.collections = collection_definitions
        # Connect to server
        self.client = MongoClient()
        # Use desired database
        self.db = self.client[db_name]
        # Create and index collections
        existing_dbs = self.client.database_names()
        if self.db_name not in existing_dbs:
            print("Creating collections...")
            self.create_collections()

    # Creates collections. Names of collections are specified with *args
    # Names of all collections must exist in definitions.collections
    # Automatically indexes collections
    def create_collections(self):
        for collection in self.collections:
            self.db.create_collection(collection["name"])
            collection_keys = []
            for field in self.indexed_fields(collection):
                if field in self.unique_indexed_fields(collection):
                    collection_keys.append((field, 1))
                else:
                    self.db[collection["name"]].create_index(field, unique=False)
            if len(collection_keys) > 0:
                self.db[collection["name"]].create_index(collection_keys, unique=True)

    # Returns fields with attribute "indexed"
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
    def __init__(self, db_name, source_coll_def, peptide_coll_def):
        super().__init__(db_name, (source_coll_def, peptide_coll_def))
        self.source_coll_def = source_coll_def
        self.peptide_coll_def = peptide_coll_def
        self.sources = self.db[source_coll_def["name"]]
        self.peptides = self.db[peptide_coll_def["name"]]

    def import_dataset(self, filepath, source_doc):
        # Import cleaned csv back into a Dataset object
        dataset = csv_tools.Dataset(csv_filepath=filepath)

        # Insert source document and save its ID
        source_id = self.insert_source_doc(source_doc, replace_existing=True)

        for peptide_doc in dataset:
            # Convert strings to correct data types
            for field in peptide_doc:
                peptide_doc[field] = self.convert_data_type(self.peptide_coll_def, field, peptide_doc[field])

            # Insert into database
            try:
                self.insert_peptide_doc(peptide_doc, source_id)
            # If already in database, augment existing document instead
            except pymongo.errors.WriteError:
                uif = list(self.unique_indexed_fields(self.peptide_coll_def))
                peptide_doc_uif = {k:v for k,v in peptide_doc.items() if k in uif}
                print("{0} already exists. Merging data...".format(peptide_doc_uif))
                self.augment_peptide_doc(peptide_doc, source_id)


    def insert_peptide_doc(self, peptide_doc, source_id):
        peptide_doc = self.embed_source_id(peptide_doc, source_id)
        self.peptides.insert_one(peptide_doc)

    def augment_peptide_doc(self, fields_to_add, source_id):
        fields_to_add = self.embed_source_id(fields_to_add, source_id)
        uif = list(self.unique_indexed_fields(self.peptide_coll_def))
        fields_to_add_uif = {k:v for k,v in fields_to_add.items() if k in uif}
        fields_to_add = {k:v for k,v in fields_to_add.items() if k not in uif}
        peptide_doc = self.peptides.find_one(fields_to_add_uif)

        for field in fields_to_add:
            if field in peptide_doc:
                if fields_to_add[field]["value"] != peptide_doc[field]["value"]:
                    peptide_doc.pop("_id")
                    fields_to_add.update(fields_to_add_uif)
                    peptide_doc = self.remove_source_id(peptide_doc)
                    fields_to_add = self.remove_source_id(fields_to_add)
                    raise errors.ConflictingUpdateError(peptide_doc, fields_to_add)
                elif fields_to_add[field]["sources"][0] not in peptide_doc[field]["sources"]:
                    fields_to_add[field]["sources"].extend(peptide_doc[field]["sources"])
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
                doc[field] = {"value": peptide_doc[field], "sources": [source_id]}
        return doc

    def remove_source_id(self, peptide_doc):
        doc = {}
        doc = dict(peptide_doc)
        for field in doc:
            if type(doc[field]) is dict and "value" in doc[field]:
                doc[field] = doc[field]["value"]
        return doc

    def validate_document(self, doc, source_or_peptide):
        pass

    def convert_data_type(self, collection, field_name, data):
        # Ensure field is defined
        if field_name not in collection["fields"]:
            raise errors.UndefinedFieldError(field_name)

        # If this field's data type is bool, convert by hand
        if collection["fields"][field_name]["type"] is bool:
            if data == "1" or data == "True" or data == "true":
                return True
            elif data == "0" or data == "False" or data == "false":
                return False
            else:
                return bool(data)
        # Otherwise use this data type's function for conversion
        else:
            return collection["fields"][field_name]["type"](data)
