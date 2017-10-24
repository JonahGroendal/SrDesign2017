# Dictionary of fields that defines each collection
# Each dictionary represents a collection
# Indexed but not unique fields contain an {"indexed": { "unique": False}} attribute
# Unique, indexed fields contain a {"unique": {"indexed": True}}
# Unique, indexed fields will be indexed together as a compound index and
# are together used to identify each peptide in peptides.db
collection_peptide = {
    "name": "peptide",
    "fields": {
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
}
collection_source = {
    "name": "source",
    "fields": {
        "url": {"type": str, "indexed": {"unique": True}},
        "institution": {"type": str},
        "authors": {"type": str}
    }
}
