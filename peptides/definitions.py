# Dictionary of fields that define each collection
# Each dictionary represents a collection
collection_fields = {}
collection_fields["peptide"] = {
    "sequence": {"type": str, "max": 50},
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
collection_fields["source"] = {
    "url": {"type": str},
    "institution": {"type": str},
    "authors": {"type": str}
}
