__author__ = "Jonah Groendal"

import types
from bson.objectid import ObjectId

"""
Contained is the peptide_db_schema, which provides a schema for each of
the MongoDB collections. These schemas contain preferences for collection
creation, define validation rules for adding to a collection, and keep track of
data types for data conversion from csv files.

Database schemas describe data in terms of python
types because pymongo automatically converts to and from MongoDB data types. Each
collection is defined as a list of dictionaries, because that is native python's
type-equivalent of a MongoDb collection. Due to this structure, an entire list
of dicts (representing a MongoDB collection of documents) can be validated with
db.PymongoDB.is_valid_data() before adding them to the database.

Representation of MongoDB terms/types in Python (python: mongo):
    "dictionary key": "document field",
    dict: document,
    list: array,
    str: string,
    bool: bool,
    etc.

Terminology:
    - "key" and "value" refer to a key and value in a python dict

    - "data schemas" are python dicts that are used to definine the
      structure and/or validation rules concerning Python data structures. These
      strucures may be constructed from any combination of dicts, lists, and
      primitive types in a nested fashon. Data schemas that define data
      structures contain nested data schemas, which are also considered a part
      of the larger schema. To simplify terms, all dicts within a data schema
      are considered data schemas, even if they only define constraints for
      primitive types.

    - "validation keys" (or "validation keywords") are the special keys in a
      data schema that define validation rules ("_data_type" and "_rules"),
      data schemas ("_schema" and " _for_each"), or logical operators ("_or").
      All validation keys are prefixed with a "_". Any key in a data schema
      that is not a "valid key" is a validation key and vice versa.

    - "valid keys" are the keys within a data schema that is the value of a
      _schema valiation key. They define what string values are permitted as
      keys in a Python dict. The "*" valid key is special and matches all
      strings.

    - "constraints" is synonymous with "validation rules".


Available validation keys:
    For validation and type conversion:
    _data_type - REQUIRED IN EVERY DATA-DEFINITION.
                 The type of the data being defined. It's Required because it's
                 used in converting data from csv to the appropriate type using
                 db.PymongoDB.convert_data_type().

    For validation only:
    _rules  -   OPTIONAL
                Defines constraints for data. The value of this validation
                key is a list of functions. Each function must take one
                argument: the data being validated. Data is valid with
                respect to its defined _rules only if every function
                in _rules returns True

    For validation and nesting schemas:
    _schema  -  CAN ONLY BE USED WHEN "_data_type": dict.
                If omitted, any dict is valid reguardless of it's contents. If
                included, this validation key's value is a dict that specifies
                the form of the dict being defined. The keys of this
                dict-defining dict are the valid keys, togather forming a
                whitelist of keys that are permitted in the dict being defined.
                The keys of a dict being defined by a data schema must all
                be strings. The "*" valid key is special and matches all keys.
                The value of each of these valid keys is a data schema
                defining the value of the key that's defined by the valid key.
                E.g. "_data_type": dict,
                     "_schema": {"name": {"_data_type": str}, "type": {"_data_type": str}}
                    |-val. key-||------ dict of valid keys w/ their data schemas --------|
    _for_each - CAN ONLY BE USED WHEN "_data_type": list.
                If omitted, a list defined by this data schema is always
                valid reguardless of it's contents. If included, the value of
                this validation key is a dict containing a data schema,
                which applies to every value in the list.

Key-value pairs for collection creation preferences:
    "_indexed": {"_unique": False} - Instructs db.PymongoDB.create_collections()
                                     to make this field unique but not indexed
    "_indexed": {"_unique": True} - Instructs db.PymongoDB.create_collections()
                                    to make this field unique and indexed
    note: Indexed unique fields will be indexed together as a compound index and
          are together used to identify each peptide in peptides.db
"""

def value_with_references(schema_of_value):
    return {
        "_data_type": dict,
        "_schema": {
            # Permitted keys ("fields" in Mongo):
            "value": schema_of_value,
            "references": {
                "_data_type": list,
                "_for_each": {
                    # Validation for all values in list:
                    "_data_type": ObjectId
                }
            }
        }
    }


peptide_db_schema = {
    # Schema for collection "peptide"
    "peptide": {
        # Constraints on list object ("collection" in Mongo) itself:
        "_data_type": list,
        "_for_each": {
            # Constraints on all values in list:
            "_data_type": dict,
            "_schema": {
                # Permitted keys ("fields" in mongo):
                "sequence": {
                    # Mark this field as unique and indexed
                    "_indexed": {"_unique": True},
                    # Constraints on this key's value:
                    "_data_type": str,
                    "_rules": [
                        lambda data: len(data) <= 50
                    ]
                },
                "name": value_with_references({
                    # Constraints on this key's value:
                    "_data_type": str
                }),
                "type": value_with_references({
                    # Constraints on this key's value:
                    "_data_type": str
                }),
                "source": {
                    # Constraints on this key's value:
                    "_data_type": list,
                    "_for_each": value_with_references({
                        # Constraints on all values in list (array):
                        "_data_type": str
                    })
                },
                "hydrophobicity": value_with_references({
                    # Constraints on this key's value:
                    "_data_type": float,
                    "_rules": [
                        lambda data: data >= 0,
                        lambda data: data <= 1
                    ]
                }),
                "toxic": value_with_references({
                    # Constraints on this key's value:
                    "_data_type": bool
                }),
                "immunogenic": value_with_references({
                    "_data_type": bool
                }),
                "insecticidal": value_with_references({
                    "_data_type": bool
                }),
                "allergen": value_with_references({
                    "_data_type": bool
                }),
                "antibacterial": value_with_references({
                    "_data_type": bool
                }),
                "anticancer": value_with_references({
                    "_data_type": bool
                }),
                "antifungal": value_with_references({
                    "_data_type": bool
                }),
                "antihypertensive": value_with_references({
                    "_data_type": bool
                }),
                "antimicrobial": value_with_references({
                    "_data_type": bool
                }),
                "antiparasitic": value_with_references({
                    "_data_type": bool
                }),
                "antiviral": value_with_references({
                    "_data_type": bool
                })
            }
        }
    },
    # Schema for collection "source"
    "source": {
        "_data_type": list,
        "_for_each": {
            "_data_type": dict,
            "_schema": {
                "url": {
                    # Mark this field as unique and indexed
                    "_indexed": {"_unique": True},
                    "_data_type": str
                },
                "institution": {
                    "_data_type": str
                },
                "authors": {
                    "_data_type": str
                }
            }
        }
    }
}
