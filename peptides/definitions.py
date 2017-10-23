# Dictionary of fields that defines each collection
# Each dictionary represents a collection
# Indexed but not unique fields contain an {"indexed": { "unique": False}} attribute
# Unique, indexed fields contain a {"unique": {"indexed": True}}
# Unique, indexed fields will be indexed together as a compound index and
# are together used to identify each peptide in peptides.db
collections = {}
collections["peptide"] = {
    "poop": {"type": str},
    "sequence": {"type": str, "indexed": {"unique": True}, "max": 50},
    "name": {"type": str},
    "type": {"type": str},
    "source": {"type": str},
    "hydrophobicity": {"type": float, "min": 0, "max": 1},
    "toxic": {"type": bool},
    "immunogenic": {"type": bool},
    "allergen": {"type": bool},
    "antiviral": {"type": bool},
    "antimicrobial": {"type": bool},
    "antibacterial": {"type": bool},
    "antihyptertensive": {"type": bool},
    "anticancer": {"type": bool},
    "antiparasitic": {"type": bool}
}
collections["source"] = {
    "url": {"type": str, "indexed": {"unique": True}},
    "institution": {"type": str},
    "authors": {"type": str}
}

# This returns all indexed fields including unique_indexed_fields
def indexed_fields(collection_name):
    for field in collections[collection_name]:
        if "indexed" in collections[collection_name][field]:
            yield field

def unique_indexed_fields(collection_name):
    for field in collections[collection_name]:
        if "indexed" in collections[collection_name][field]:
            if collections[collection_name][field]["indexed"]["unique"] is True:
                yield field
