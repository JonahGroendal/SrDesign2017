__author__ = "Jonah Groendal"

from bson.objectid import ObjectId

# Dictionary of fields that defines each collection
# Each dictionary represents a collection
# Indexed but not unique fields contain an {"_indexed": { "_unique": False}} attribute
# Indexed unique fields contain a {"_unique": {"_indexed": True}}
# Indexed unique fields will be indexed together as a compound index and
# are together used to identify each peptide in peptides.db

def value_with_metadata(def_of_value):
    return {
        "_data_type": dict,
        "_dict_def": {
            "value": def_of_value,
            "references": {
                "_data_type": list,
                "_list_def": {
                    "_data_type": ObjectId
                }
            }
        }
    }


collection_peptide = {
    "_name": "peptide",
    "_data_type": dict,
    "_dict_def": {
        "sequence": {
            "_indexed": {"_unique": True},
            "_data_type": str,
            "_data_max": 50
        },
        "name": value_with_metadata({
            "_data_type": str
        }),
        "type": value_with_metadata({
            "_data_type": str
        }),
        "source": {
            "_data_type": list,
            "_list_def": value_with_metadata({
                "_data_type": str
            })
        },
        "hydrophobicity": value_with_metadata({
            "_data_type": float,
            "_data_min": 0,
            "_data_max": 1
        }),
        "toxic": value_with_metadata({
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
        }),
    }
}
collection_source = {
    "_name": "source",
    "_dict_def": {
        "url": {
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
