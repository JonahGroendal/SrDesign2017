# Dictionary of fields that define each collection
# Each dictionary represents a collection
peptide = {
    "sequence": {"type": str, "max": 50},
    "name": {"type": str},
    "source": {"type": str},
    "hydrophobicity": {"type": int, "min": 0, "max": 100},
    "toxic": {"type": bool},
    "allergen": {"type": bool},
    "antiviral": {"type": bool},
    "antimicrobial": {"type": bool},
    "antibacterial": {"type": bool},
    "antihyptertensive": {"type": bool},
    "anticancer": {"type": bool},
    "antiparasitic": {"type": bool}
}
source = {
    "url": {"type": str},
    "institution": {"type": str},
    "authors": {"type": str}
}
