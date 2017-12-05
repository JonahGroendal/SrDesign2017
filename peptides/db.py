__author__ = "Jonah Groendal"

import types
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import errors
import csv_tools
import db_schema

class PymongoDB:
    """
    Used to connect to a MongoDB database through the pymongo driver.
    If a database of the name db_name doesn't exist, one is created from the
    specifications in db_schema.

    self.db is a MongoClient object, so any database operation can be
    performed through it.

    A key component of this class is self.is_valid_data(). It's used to
    validate data (in the form of Python types) against a "data schema" before
    the data is added to the database. A data schema is a dict used to definine
    the structure and/or validation rules of instances of (nested) Python data
    types. The argument db_schema is a data schema of a MongoDB database, which,
    in this project, is represented by a list of dicts.
    """
    def __init__(self, db_name, db_schema=None):
        # Name of database
        self.db_name = db_name
        # Database schema
        self.db_schema = db_schema
        # Schema of valid data schema
        # (defines what's a valid argument for self.is_valid_data())
        self.data_meta_schema = self._data_meta_schema()
        # Schema of valid db_schema
        self.db_meta_schema = self._db_meta_schema()
        # Validate db_schema
        if not self.is_valid_data(self.db_meta_schema, self.db_schema):
            raise ValueError("argument 'db_schema' is not a valid schema")
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
        """
        Creates and indexes collections based on their schemas (provided in
        self.db_schema).
        """
        for collection_name in self.db_schema:
            self.db.create_collection(collection_name)
            collection_keys = []
            for field in self.indexed_fields(self.db_schema[collection_name]):
                if field in self.unique_indexed_fields(self.db_schema[collection_name]):
                    collection_keys.append((field, 1))
                else:
                    self.db[collection_name].create_index(field, unique=False)
            if len(collection_keys) > 0:
                self.db[collection_name].create_index(collection_keys, unique=True)

    def indexed_fields(self, collection_schema):
        """ Returns fields with attribute "_indexed" (unique or otherwise) """
        for field in collection_schema["_for_each"]["_schema"]:
            if "_indexed" in collection_schema["_for_each"]["_schema"][field]:
                yield field

    def unique_indexed_fields(self, collection_schema):
        """ Returns fields with attribute "_indexed":{"_unique":True} """
        for field in collection_schema["_for_each"]["_schema"]:
            if "_indexed" in collection_schema["_for_each"]["_schema"][field]:
                if collection_schema["_for_each"]["_schema"][field]["_indexed"]["_unique"] is True:
                    yield field

    # Can recursively convert data from within nested lists
    def convert_data_type(self, data_schema, data):
        """
        params:
            data_schema - a data schema specifying the target data type

            data - either a string to be converted or a composite data type
            containing the string to be converted

        Used to convert string data from csv into and instance of the data type
        specified in data_schema. If the specified target is nested instances of
        data types (E.g. list of ints, dict of int values, list of lists of
        strings, etc.), this function will recursively traverse "data_schema"
        and "data" to convert the string(s) within "data".
        """
        # Ensure that data_schema is a valid data schema
        if not self.is_valid_data(self.data_meta_schema, data_schema):
            raise ValueError("argument 'db_schema' is not a valid schema")

        # Recursion cases (if data type is list or dict):
        if data_schema["_data_type"] is list:
            if type(data) is not list:
                data = list((data,))
            for value in data:
                value = self.convert_data_type(data_schema["_for_each"], value)
            return data
        elif data_schema["_data_type"] is dict:
            for key in data:
                data[key] = self.convert_data_type(data_schema["_schema"][key], data[key])
            return data

        # Base cases:
        # If this field's data type is bool, convert by hand
        elif data_schema["_data_type"] is bool:
            if data == "1" or data == "True" or data == "true":
                return True
            elif data == "0" or data == "False" or data == "false":
                return False
            else:
                return bool(data)
        # Otherwise use this data type's function for conversion
        else:
            return data_schema["_data_type"](data)

    def is_valid_data(self, data_schema, data):
        """
        Returns true if data is valid with respect to data_schema,
        otherwise returns false.

        args:
            data_schema - Attribute 'data' is validated against this schema. A
                data_schema may contain nested data schemas
            data - The data that is being validated. Can be any data type that
                satisfies: type( data type ) == type
        """

        def _or(data):
            """
            Recursively validate data against each data schema.
            data must be valid with respect to at least one data schema.
            """
            for data_schema in data_schema["_or"]:
                if self.is_valid_data(data_schema, data):
                    return True

            return False

        def _for_each(data):
            """ Recursively validate items in lists """
            # Validate every item in list
            for value in data:
                if not self.is_valid_data(data_schema["_for_each"], value):
                    return False
            return True

        def _schema(data):
            """ Recursively validate items in dicts """
            if id(data) not in schemas_validated:
                # Keep track of schemas validated to avoid infinite recursion
                # when validating self-referential data schemas
                schemas_validated.append(id(data))
                for key in data:
                    valid = False
                    # '*' matches all strings
                    if "*" in data_schema["_schema"]:
                        if self.is_valid_data(data_schema["_schema"]["*"], data[key]):
                            valid = True
                    if key in data_schema["_schema"]:
                        if self.is_valid_data(data_schema["_schema"][key], data[key]):
                            valid = True
                    if not valid:
                        return False

            return True

        ###################
        # BASE CASES
        ###################
        def _data_type(data):
            """ Verify data is of it's defined type """
            return type(data) is data_schema["_data_type"]

        def _rules(data):
            """
            Ensure that every validation function (or "validation rule") returns
            true with 'data' as an argument.
            """
            for constraint_func in data_schema["_rules"]:
                if not constraint_func(data):
                    return False
            return True

        # For keeping track of schemas that were validated, so self-referential
        # schemas don't cause infinite recursion.
        schemas_validated = []

        for validation_key in data_schema:
            try:
                if not eval('{}(data)'.format(validation_key)):
                    return False
            except NameError:
                # This will happen with the '_indexed' validation key
                pass

        return True

    def _data_meta_schema(self):
        """
        Returns valid_data_schema, which is a data schema of a valid data
        schema. It can be used as an argument in self.is_valid_data() to
        validate the syntax of a data schema to be used in self.is_valid_data().

        Called in __init__() to initialize self.data_meta_schema

        If you would like to understand the syntax of a data schemas such as
        this, please refer to the documentation in db_schema.py for further
        details.

        Note: This data schema is a valid data schema of itself 😎
        """

        valid_data_schema = {}          # Data schema of a valid data schema.

        valid_data_schema_dict = {}     # Data schema of a valid data schema
                                        # where data_type is dict.
        valid_data_schema_list = {}     # Data schema of a valid data schema
                                        # where data_type is list.
        valid_data_schema_primitive = {}# Data schema of a valid data schema
                                        # where data_type is is a primitive type.

        valid_data_schema = {
            # A valid data schema can be one of three forms:
            "_or": [
                valid_data_schema_list,
                valid_data_schema_dict,
                valid_data_schema_primitive
            ]
        }

        # Validation keys common to all three forms
        universal_validation_keyvalues = {
            # Allowed validation keys and thier values' data schemas:
            '_or': {
                "_data_type": list,
                "_for_each": valid_data_schema
            },
            '_rules': {
                "_data_type": list,
                "_for_each": {
                    "_data_type": types.FunctionType
                }
            }
        }
        # Data schema of a valid dict data schema:
        valid_data_schema_dict["_data_type"] = dict   # A data schema is always a dict
        valid_data_schema_dict["_schema"] = {
            # Allowed validation keys and thier values' data schemas:
            '_data_type': {
                "_data_type": type,
                "_rules": [
                    lambda data: data is dict
                ]
            },
            '_schema': {
                "_data_type": dict,
                "_schema": {
                    '*': valid_data_schema
                }
            }
        }
        valid_data_schema_dict["_schema"].update(universal_validation_keyvalues)

        # Data schema of a valid list data schema:
        valid_data_schema_list["_data_type"] = dict   # A data schema is always a dict
        valid_data_schema_list["_schema"] = {
            # Allowed validation keys and thier values' data schemas:
            '_data_type': {
                "_data_type": type,
                "_rules": [
                    lambda data: data is list
                ]
            },
            '_for_each': valid_data_schema
        }
        valid_data_schema_list["_schema"].update(universal_validation_keyvalues)

        # Data schema of a valid data schema where the data being defined is
        # neither a list nor a dict:
        valid_data_schema_primitive["_data_type"] = dict   # A data schema is always a dict
        valid_data_schema_primitive["_schema"] = {
            # Allowed validation keys and thier values' data schemas:
            '_data_type': {
                "_data_type": type,
                "_rules": [
                    lambda data: data is not dict,
                    lambda data: data is not list
                ]
            },
            '_indexed': {
                "_data_type": dict,
                "_schema": {
                    '_unique': {
                        "_data_type": bool
                    }
                }
            }
        }
        valid_data_schema_primitive["_schema"].update(universal_validation_keyvalues)

        return valid_data_schema

    def _db_meta_schema(self):
        """
        Returns a data schema of a valid database schema. Using
        self.is_valid_data(), this data schema defines what values of the
        parameter 'db_schema' are valid in __init__().

        Called in __init__() to initialize self.db_meta_schema.

        Please refer to the documentation in db_schema.py for further details.
        """
        # A valid database schema is a data schema that describes a list of
        # dicts, each of which is a valid data schema.
        return {
            "_data_type": dict,
            "_schema": {
                '*': {
                    "_data_type": dict,
                    "_schema": {
                        '_data_type': {
                            "_data_type": type,
                            "_rules": [lambda data: data is list]
                        },
                        '_for_each': {
                            "_data_type": dict,
                            "_schema": {
                                '_data_type': {
                                    "_data_type": type,
                                    "_rules": [lambda data: data is dict]
                                },
                                '_schema': {
                                    "_data_type": dict,
                                    "_schema": {
                                        # '*' matches every string
                                        '*': self._data_meta_schema()
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }


class PeptideDB(PymongoDB):
    """
    Extends PymongoDB to provide specialized functionality for the peptide
    database. Included is the database schema as well as methods for importing
    and exporting to and from a csv file.

    In this project, all connections to the database are facilitaed through
    instances of this class. self.sources and self.peptides are MongoDB
    Collection objects, which should be used to perform operations on their
    respective collections. Please refer to the MongoDB API reference for
    documentation on their methods for querying, inserting, updating, etc.
    """
    def __init__(self, db_name="peptide"):
        # Schema of database
        self.db_schema = db_schema.peptide_db_schema
        # Schema of collection for references
        self.source_coll_schema = self.db_schema["source"]
        # Schema of collection for peptides and thier activities
        self.peptide_coll_schema = self.db_schema["peptide"]
        # Create database and collections, index fields, and connect
        super().__init__(db_name, db_schema=self.db_schema)
        # Mongo Collection objects for querying, inserting, updating, etc.
        self.sources = self.db["source"]
        self.peptides = self.db["peptide"]

    def import_dataset(self, filepath, source_doc):
        """
        Used for importing data into the "peptide" and "source" collections
        from a specially formatted csv file.

        Converts data from string to whatever is specified in the "peptide"
        collection schema, then validates the data against the collection schema.
        If valid, it will attempt to insert the data into the "peptide"
        collection. If the sequence already exists, it will update the existing
        peptide document using self.augment_peptide_doc(). If documet validation
        fails or if the update conflicts with data in the database, an error is
        thrown and no more documents are inserted/updated (the update is
        aborted).

        Sadly, MongoDB doesn't support transactions. If you would like to
        reverse an insert, you must perform an update operation and $unset all
        references to source_doc as well as any fields that refer only to
        source_doc. Alternatively, you could delete the database and start over.

        Format of csv file:
            - First row contains the names of the columns (or "fields" in Mongo)
            - The rest of the rows contain values corresponding to thier
              columns.
            - Use "None" to indicate no value (equivalent to null in SQL).
            - Use "1" and "0" to indicate True and False

        params:
            filepath - The filepath to the csv file.
            source_doc - A document contaning reference info for citing the
                source of the peptide data. It must be a dict that's valid with
                respect to the "source" collection schema.
        """
        # Import cleaned .csv back into a Dataset object
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
                    self.peptide_coll_schema["_for_each"]["_schema"][field_name],
                    peptide_doc[field_name])
            # Validate
            if not (
                self.is_valid_data(
                    self.peptide_coll_schema["_for_each"],
                    peptide_doc)
            ):
                raise errors.ViolationOfDefinedConstraintError(
                    {field_name: self.peptide_coll_schema["_for_each"]["_schema"][field_name]},
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
                uif = list(self.unique_indexed_fields(self.peptide_coll_schema))
                peptide_doc_uif = {k: v for k, v in peptide_doc.items() if k in uif}
                print("{0} already exists. Merging data...".format(peptide_doc_uif))
                # Augment existing document
                self.augment_peptide_doc(peptide_doc)

    def insert_peptide_doc(self, peptide_doc):
        self.peptides.insert_one(peptide_doc)

    def augment_peptide_doc(self, fields_to_add):
        """
        For updating an existing peptide doc without removing any existing data.

        If there are any conflicting values between what's in the database and
        what's being added, an error is thrown and the update is aborted.

        params:
            fields_to_add - The fields and thier values to be added to the
                existing document. The fields required to identify the existing
                document must be included as well.
        """
        # Check what fields are used to identify peptide documents
        uif = list(self.unique_indexed_fields(self.peptide_coll_schema))
        # Save fields and thier values to identify peptide doc
        fields_to_add_uif = {k: v for k, v in fields_to_add.items() if k in uif}
        # Save other fields and their values
        fields_to_add = {k: v for k, v in fields_to_add.items() if k not in uif}
        # Get existing peptide doc
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
                # If field exists and values are different, throw error
                elif fields_to_add[field]["value"] != peptide_doc[field]["value"]:
                    peptide_doc.pop("_id")
                    fields_to_add.update(fields_to_add_uif)
                    raise errors.ConflictingUpdateError(peptide_doc, fields_to_add)
                elif fields_to_add[field]["references"][0] not in peptide_doc[field]["references"]:
                    fields_to_add[field]["references"].extend(peptide_doc[field]["references"])
            # Update database with changes
            fields_to_add_update = {"$set": fields_to_add}
            self.peptides.update(fields_to_add_uif, fields_to_add_update)

    def insert_source_doc(self, source_doc, replace_existing=False):
        """
        Insert doc containing info for referencing sources. If document exists,
        replace existing document if replace_existing is True, otherwise throw
        error.

        params:
            source_doc - a dict containing fields to be inserted.
            replace_exiting - a boolean

        returns the ObjectId of the inserted source_doc
        """
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
        """
        Replaces all values in peptide_doc with a dict of the form:
        {"value": *the value*, "references": *source_id*}, then returns the
        altered peptide_doc.

        params:
            peptide_doc - dict with values to be replaced
            source_id - ObjectId of the peptide data's source document
        """
        doc = {}
        for field in peptide_doc:
            if field in self.unique_indexed_fields(self.peptide_coll_schema):
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
        """
        An undo button for self.embed_source_id(). Returns the altered
        peptide_doc

        params:
            peptide_doc - a dict whose values are a dict embedded with source_id
                references.
        """
        doc = {}
        doc = dict(peptide_doc)
        for field in doc:
            if type(doc[field]) is dict and "value" in doc[field]:
                doc[field] = doc[field]["value"]
        return doc

    def export_peptides_to_csv(self, filepath, field_names, pretty=False):
        """
        Exports peptide data to a csv file. If pretty==True, values are padded
        with spaces such that every value in a column is the same width.
        If pretty==True, the csv data cannot be imported back into a Dataset
        object.

        params:
            filepath - path to csv file
            field_names - names of fields to be exported
            pretty - whether or not values will be padded with spaces
        """
        cursor = self.peptides.find({}, {v: True for v in field_names})
        documents = []
        peptides = csv_tools.Dataset()
        peptides.column_names = field_names
        for document in cursor:
            document.pop("_id")
            peptides.append_row(self.remove_source_id(document))
        peptides.export_csv(filepath, pretty=pretty)
