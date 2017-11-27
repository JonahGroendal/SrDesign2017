__author__ = "Jonah Groendal"

from bson.objectid import ObjectId
import copy

"""
Contains the dictionary that defines the schemas for each of the MongoDb
collections.

Each collection is defined as a list of dictionaries, because that is native
python's equivalent of a MongoDb collection. Due to this structure, an entire
list of dicts can be validated with db.DB.is_valid_data() using the definition
for a collection.

Representation of MongoDB terms/types in Python (python: mongo):
    "dictionary key": "document field",
    dict: document,
    list: array,
    str: string,
    bool: bool,
    etc.

Terminology:
    - "validation key" (or "validation keyword") is any key in collections_def
      that starts with a "_". It is used to define constraints.
    - "valid key" is a key of the dict (document) that's hypothetically being validated.
      Valid (or permitted) keys are defined in "_dict_def"

Each collection-defining dict (found within collections_def) contains validation
keywords used to define constraints. All validation keywords are used only to
define constraints on a key's value(s).

Core validation keywords:
    _data_type - REQUIRED IN EVERY VALUE DEFINITION.
                 The type of a key's value.
    _dict_def - CAN ONLY BE USED WHEN "_data_type": dict.
                Defines the form of a (possibly nested) dict. The value of this
                validation key is a dict containing a whitelist of permitted
                keys and their value definitions.
                E.g. "_data_type": dict,
                     "_dict_def": {"name": {"_data_type": str}, "type": {"_data_type": str}}
                     |-val. key-| |------- dict of permitted keys w/ their val. defs -------|
    _list_def - CAN ONLY BE USED WHEN "_data_type": list.
                The value of this validation key is a dict containing a data
                definition, which applies to every value in the list.

Supplementary validation keywords (these can easily be expanded to include more):
    _data_min - The minimum length or value of a key's data
    _data_max - The maximum length or value of a key's data

Special key-value pairs that are used when creating the database:
    "_indexed": {"_unique": False} - Makes field indexed but not unique
    "_indexed": {"_unique": True} - Makes field unique and indexed
    note: Indexed unique fields will be indexed together as a compound index and
          are together used to identify each peptide in peptides.db
"""


####################################
# DEFINING COLLECTIONS
####################################

def value_with_metadata(def_of_value):
    return {
        "_data_type": dict,
        # Validation for dict object itself:
        "_dict_def": {
            # Permitted keys ("fields" in mongo):
            "value": def_of_value,
            "references": {
                "_data_type": list,
                # Validation for list object itself:
                "_list_def": {
                    # Validation for all values in list:
                    "_data_type": ObjectId
                }
            }
        }
    }


collections_def = {
    # Definition for collection "peptide"
    "peptide": {
        "_data_type": list,
        # Validation for list object ("collection" in mongo) itself:
        # (E.g. if _data_max was used, it would limit len of list (collection))
        "_list_def": {
            # Validation for all values in list:
            # (E.g. if _data_max was used, it would limit len of dict (collection))
            "_data_type": dict,
            "_dict_def": {
                # Permitted keys ("fields" in mongo):
                "sequence": {
                    # Mark this field as unique and indexed
                    "_indexed": {"_unique": True},
                    # Validation for this key's (field's) value:
                    "_data_type": str,
                    "_data_max": 50
                },
                "name": value_with_metadata({
                    # Validation for this key's (field's) value:
                    "_data_type": str
                }),
                "type": value_with_metadata({
                    # Validation for this key's (field's) value:
                    "_data_type": str
                }),
                "source": {
                    # Validation for this key's (field's) value:
                    "_data_type": list,
                    # Validation for list (array) object itself:
                    # (E.g. _data_max would limit len of list (array))
                    "_list_def": value_with_metadata({
                        # Validation for all values in list (array):
                        # (E.g. _data_max would limit len of each string in list (array))
                        "_data_type": str
                    })
                },
                "hydrophobicity": value_with_metadata({
                    # Validation for this key's (field's) value:
                    "_data_type": float,
                    "_data_min": 0,
                    "_data_max": 1
                }),
                "toxic": value_with_metadata({
                    # Validation for this key's (field's) value:
                    "_data_type": bool
                }),
                "immunogenic": value_with_metadata({
                    "_data_type": bool
                }),
                "insecticidal": value_with_metadata({
                    "_data_type": bool
                }),
                "allergen": value_with_metadata({
                    "_data_type": bool
                }),
                "antibacterial": value_with_metadata({
                    "_data_type": bool
                }),
                "anticancer": value_with_metadata({
                    "_data_type": bool
                }),
                "antifungal": value_with_metadata({
                    "_data_type": bool
                }),
                "antihyptertensive": value_with_metadata({
                    "_data_type": bool
                }),
                "antimicrobial": value_with_metadata({
                    "_data_type": bool
                }),
                "antiparasitic": value_with_metadata({
                    "_data_type": bool
                }),
                "antiviral": value_with_metadata({
                    "_data_type": bool
                })
            }
        }
    },
    # Definition for collection "source"
    "source": {
        "_data_type": list,
        "_list_def": {
            "_data_type": dict,
            "_dict_def": {
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


####################################
# DEFINING VALID DEFINITIONS
####################################

valid_data_def = {}         # Data definition of a valid data definition.

valid_data_def_dict = {}    # Data definition of a valid data definition where
                            # data_type is dict.
valid_data_def_list = {}    # Data definition of a valid data definition where
                            # data_type is list.
valid_data_def_other = {}   # Data definition of a valid data definition where
                            # data_type is neither dict nor list.

valid_data_def = {
    # A valid data definition can be one of three forms:
    "_or": [
        valid_data_def_other,
        valid_data_def_list,
        valid_data_def_dict
    ]
}

# Validation keys common to all three forms
universal_validation_keys = {
    # Allowed validation keys and thier values' data definitions:
    '_not': valid_data_def,
    '_or': {
        "_data_type": list,
        "_list_def": valid_data_def
    },
    '_and': {
        "_data_type": list,
        "_list_def": valid_data_def
    },
    '_data_min': {
        "_or": [
            {"_data_type": int},
            {"_data_type": float}
        ]
    },
    '_data_max': {
        "_or": [
            {"_data_type": int},
            {"_data_type": float}
        ]
    },
    '_data_equals': {
        "_data_type": type
    }
}

# Data definition of a valid dict data definition:
valid_data_def_dict["_data_type"] = dict   # A data definition is always a dict
valid_data_def_dict["_dict_def"] = {
    # Allowed validation keys and thier values' data definitions:
    '_data_type': {
        "_data_type": type,
        "_data_equals": dict
    },
    '_dict_def': {
        "_data_type": dict,
        "_dict_def": {
            '*': valid_data_def
        }
    }
}
valid_data_def_dict["_dict_def"].update(universal_validation_keys)

# Data definition of a valid list data definition:
valid_data_def_list["_data_type"] = dict   # A data definition is always a dict
valid_data_def_list["_dict_def"] = {
    # Allowed validation keys and thier values' data definitions:
    '_data_type': {
        "_data_type": type,
        "_data_equals": list
    },
    '_list_def': valid_data_def
}
valid_data_def_list["_dict_def"].update(universal_validation_keys)

# Data definition of a valid data definition where the data being defined is
# neither a list nor a dict:
valid_data_def_other["_data_type"] = dict   # A data definition is always a dict
valid_data_def_other["_dict_def"] = {
    # Allowed validation keys and thier values' data definitions:
    '_data_type': {
        "_and": [
            {"_data_type": type},
            {"_not": {"_data_type": type, "_data_equals": dict}},
            {"_not": {"_data_type": type, "_data_equals": list}}
        ]
    },
    '_indexed': {
        "_data_type": dict,
        "_dict_def": {
            '_unique': {
                "_data_type": bool
            }
        }
    }
}
valid_data_def_other["_dict_def"].update(universal_validation_keys)


# Data definition of a valid collections_def dict
# Used to validate syntax of collections_def
def_of_collections_def = {
    "_data_type": dict,
    "_dict_def": {
        '*': {
            "_data_type": dict,
            "_dict_def": {
                '_data_type': {
                    "_data_type": type,
                    "_data_equals": list
                },
                '_list_def': {
                    "_data_type": dict,
                    "_dict_def": {
                        '_data_type': {
                            "_data_type": type,
                            "_data_equals": dict
                        },
                        '_dict_def': {
                            "_data_type": dict,
                            "_dict_def": {
                                # '*' matches every string
                                '*': valid_data_def
                            }
                        }
                    }
                }
            }
        }
    }
}
