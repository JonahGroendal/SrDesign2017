# Dictionary of fields that defines each collection
# Each dictionary represents a collection
# Indexed but not unique fields contain an {"indexed": { "unique": False}} attribute
# Indexed unique fields contain a {"unique": {"indexed": True}}
# Indexed unique fields will be indexed together as a compound index and
# are together used to identify each peptide in peptides.db
collection_peptide = {
    "name": "peptide",
    "fields": {
        "sequence": {"data_type": str, "indexed": {"unique": True}, "max": 50},
        "name": {"data_type": str},
        "type": {"data_type": str},
        "source": {"data_type": {list: {"data_type": str}}},
        "hydrophobicity": {"data_type": float, "min": 0, "max": 1},
        "toxic": {"data_type": bool},
        "immunogenic": {"data_type": bool},
        "insecticidal": {"data_type": bool},
        "allergen": {"data_type": bool},
        "antibacterial": {"data_type": bool},
        "anticancer": {"data_type": bool},
        "antifungal": {"data_type": bool},
        "antihyptertensive": {"data_type": bool},
        "antimicrobial": {"data_type": bool},
        "antiparasitic": {"data_type": bool},
        "antiviral": {"data_type": bool}
    }
}
collection_source = {
    "name": "source",
    "fields": {
        "url": {"data_type": str, "indexed": {"unique": True}},
        "institution": {"data_type": str},
        "authors": {"data_type": str}
    }
}
