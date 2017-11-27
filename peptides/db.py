__author__ = "Jonah Groendal"

import pymongo
from pymongo import MongoClient
import definitions
import errors
import csv_tools

class PymongoDB:
    def __init__(self, db_name, collections_def):
        self.db_name = db_name
        self.collections_def = collections_def
        self.valid_data_def = definitions.valid_data_def
        self.def_of_collections_def = definitions.def_of_collections_def
        # Validate syntax of collections_def
        if not self.is_valid_data(self.def_of_collections_def, self.collections_def):
            raise ValueError("argument 'collections_def' is invalid")
        # Connect to server
        self.client = MongoClient()
        # Use desired database
        self.db = self.client[db_name]
        # Create and index collections
        existing_dbs = self.client.database_names()
        if self.db_name not in existing_dbs:
            print("Creating collections...")
            self.create_collections()

    def create_collections(self):
        """ Creates and indexes collections based on their definitions """
        for collection_name in self.collections_def:
            self.db.create_collection(collection_name)
            collection_keys = []
            for field in self.indexed_fields(self.collections_def[collection_name]):
                if field in self.unique_indexed_fields(self.collections_def[collection_name]):
                    collection_keys.append((field, 1))
                else:
                    self.db[collection_name].create_index(field, unique=False)
            if len(collection_keys) > 0:
                self.db[collection_name].create_index(collection_keys, unique=True)

    # Can recursively convert data from within nested lists
    def convert_data_type(self, data_definition, data):
        if data_definition["_data_type"] is list:
            if type(data) is not list:
                data = list((data,))
            for value in data:
                value = self.convert_data_type(data_definition["_list_def"], value)
            return data
        elif data_definition["_data_type"] is dict:
            for key in data:
                data[key] = self.convert_data_type(data_definition["_dict_def"][key], data[key])
            return data
        # If this field's data type is bool, convert by hand
        elif data_definition["_data_type"] is bool:
            if data == "1" or data == "True" or data == "true":
                return True
            elif data == "0" or data == "False" or data == "false":
                return False
            else:
                return bool(data)
        # Otherwise use this data type's function for conversion
        else:
            return data_definition["_data_type"](data)

    def is_valid_data(self, data_definition, data):
        """
        Returns true if data is valid with respect to data_definition,
        otherwise returns false.

        More info can be found in definitions.py.

        args:
            data_definition - Attribute 'data' is validated against this definition.
            data - The data that is being validated. Can be any data type that
                   satisfies: type( data type ) == type
        """

        def _or(data):
            """
            Recursively validate data against each data definition.
            data must be valid with respect to at least one data definition.
            """
            for data_def in data_definition["_or"]:
                if self.is_valid_data(data_def, data):
                    return True

            return False

        def _and(data):
            """
            Recursively validate data against each data definition.
            data must be valid with respect to all data definitions.
            """
            for data_def in data_definition["_and"]:
                if not self.is_valid_data(data_def, data):
                    return False

            return True

        def _not(data):
            """ Recursively validate falsity of data """
            return not self.is_valid_data(data_definition["_not"], data)

        def _data_type(data):
            """ Verify data is of it's defined type """
            return type(data) is data_definition["_data_type"]

        def _list_def(data):
            """ Recursively validate items in (nested) lists """
            # Ignore this constraint if data_type is not list
            if data_definition["_data_type"] is not list:
                return True
            # Validate every item in list
            for value in data:
                if not self.is_valid_data(data_definition["_list_def"], value):
                    return False
            return True

        def _dict_def(data):
            """ Recursively validate items in nested dicts """
            # Ignore this constraint if data_type is not dict
            if data_definition["_data_type"] is not dict:
                return True
            # Validate every item in list
            for key in data:
                valid = False
                # '*' matches every string
                if "*" in data_definition["_dict_def"]:
                    if self.is_valid_data(data_definition["_dict_def"]["*"], data[key]):
                        valid = True
                if key in data_definition["_dict_def"]:
                    if self.is_valid_data(data_definition["_dict_def"][key], data[key]):
                        valid = True
                if not valid:
                    return False

            return True

        def _data_equals(data):
            return data == data_definition["_data_equals"]

        def _data_min(data):
            """
            If data is a collection, verify len(data) >= _data_min.
            If data is not a collection, verify data >= _data_min.
            """
            try:
                magnitude = len(data)
            except TypeError:
                magnitude = data
            return magnitude >= data_definition["_data_min"]

        def _data_max(data):
            """
            If data is a collection, verify len(data) <= _data_max.
            If data is not a collection, verify data <= _data_max.
            """
            try:
                magnitude = len(data)
            except TypeError:
                magnitude = data
            return magnitude <= data_definition["_data_max"]

        validators = {
            "_or": _or,
            "_and": _and,
            "_not": _not,
            "_data_type": _data_type,
            "_list_def": _list_def,
            "_dict_def": _dict_def,
            "_data_min": _data_min,
            "_data_max": _data_max,
            "_data_equals": _data_equals
        }
        for validation_key in data_definition:
            if validation_key in validators:
                is_valid = validators[validation_key](data)
                if not is_valid:
                    return False
        return True

    # Returns fields with attribute "_indexed" (unique or otherwise)
    def indexed_fields(self, collection_def):
        for field in collection_def["_list_def"]["_dict_def"]:
            if "_indexed" in collection_def["_list_def"]["_dict_def"][field]:
                yield field
    # Returns fields with attribute "_indexed":{"_unique":True}
    def unique_indexed_fields(self, collection_def):
        for field in collection_def["_list_def"]["_dict_def"]:
            if "_indexed" in collection_def["_list_def"]["_dict_def"][field]:
                if collection_def["_list_def"]["_dict_def"][field]["_indexed"]["_unique"] is True:
                    yield field

class PeptideDB(PymongoDB):
    def __init__(self, db_name="peptide"):
        self.source_coll_def = definitions.collections_def["source"]
        self.peptide_coll_def = definitions.collections_def["peptide"]
        super().__init__(db_name, definitions.collections_def)
        self.sources = self.db["source"]
        self.peptides = self.db["peptide"]

    def import_dataset(self, filepath, source_doc):
        # Import cleaned csv back into a Dataset object
        dataset = csv_tools.Dataset(csv_filepath=filepath)

        # Insert source document and save its ID
        source_id = self.insert_source_doc(source_doc, replace_existing=True)

        docs_to_insert = []
        for peptide_doc in dataset:
            # Remove None fields
            for field_name in list(peptide_doc):
                if peptide_doc[field_name] == "None":
                    peptide_doc.pop(field_name)

            # Add source metadata to peptide doc
            peptide_doc = self.embed_source_id(peptide_doc, source_id)

            # Convert strings to correct data types and validate
            for field_name in peptide_doc:
                # Convert strings to correct data types
                peptide_doc[field_name] = self.convert_data_type(
                    self.peptide_coll_def["_list_def"]["_dict_def"][field_name],
                    peptide_doc[field_name])
            # Validate
            if not (
                self.is_valid_data(
                    self.peptide_coll_def["_list_def"],
                    peptide_doc)
            ):
                raise errors.ViolationOfDefinedConstraintError(
                    {field_name: self.peptide_coll_def["_list_def"]["_dict_def"][field_name]},
                    peptide_doc)

            docs_to_insert.append(peptide_doc)

        for peptide_doc in docs_to_insert:
            # Insert into database
            try:
                self.insert_peptide_doc(peptide_doc)
            # If already in database, augment existing document instead
            except pymongo.errors.WriteError:
                # Remove _id generated by insert statement
                peptide_doc.pop("_id")
                # Print updating info
                uif = list(self.unique_indexed_fields(self.peptide_coll_def))
                peptide_doc_uif = {k: v for k, v in peptide_doc.items() if k in uif}
                print("{0} already exists. Merging data...".format(peptide_doc_uif))
                # Augment existing document
                self.augment_peptide_doc(peptide_doc)

    def insert_peptide_doc(self, peptide_doc):
        self.peptides.insert_one(peptide_doc)

    def augment_peptide_doc(self, fields_to_add):
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
                # Don't embed unique_indexed_fields
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

    def export_peptides_to_csv(self, filepath, field_names):
        cursor = self.peptides.find({}, {v: True for v in field_names})
        documents = []
        peptides = csv_tools.Dataset()
        peptides.column_names = field_names
        for document in cursor:
            document.pop("_id")
            peptides.append_row(self.remove_source_id(document))
        peptides.export_csv(filepath, pretty=True)
