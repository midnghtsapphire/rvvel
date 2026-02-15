"""
Master Platform: Hidden Procedures Education
PDO threads, plasma fibroblast, non-surgical alternatives most people don't know about.
Author: Audrey Evans
"""
import json
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

DATA_DIR = Path(__file__).parent / "data" / "hidden_procedures"
MEDICAL_DISCLAIMER = "DISCLAIMER: For informational purposes only. Consult qualified medical professionals."

HIDDEN_PROCEDURES = {
    "pdo_threads": {
        "name": "PDO Thread Lift",
        "description": "Dissolvable threads inserted under skin to lift and tighten",
        "cost": {"us": "$1,500-$3,000", "tijuana": "$800-$1,500"},
        "vs_surgery": "PDO threads: $2K, no downtime. Surgical facelift: $15K+, weeks recovery.",
        "how_long_lasts": "12-18 months (threads dissolve in 6 months, collagen lasts longer)",
        "recovery": "3-7 days mild swelling",
        "ideal_for": ["Jowls", "Neck sagging", "Brow lift", "Nasolabial folds"],
    },
    "plasma_fibroblast": {
        "name": "Plasma Fibroblast (Skin Tightening)",
        "description": "Plasma pen creates micro-injuries to tighten skin without surgery",
        "cost": "$500-$2,000 per area",
        "how_long_lasts": "2-3 years",
        "recovery": "7-14 days (scabbing, redness)",
        "ideal_for": ["Hooded eyes", "Neck lines", "Crow's feet", "Loose skin"],
    },
    "morpheus8": {
        "name": "Morpheus8 (Microneedling + RF)",
        "description": "Combines microneedling with radiofrequency for deep skin remodeling",
        "cost": "$1,000-$1,500 per session (3-4 sessions typical)",
        "how_long_lasts": "12-24 months",
        "recovery": "3-5 days redness",
        "ideal_for": ["Acne scars", "Skin laxity", "Wrinkles", "Texture"],
    },
    "kybella": {
        "name": "Kybella (Double Chin Dissolving)",
        "description": "Injectable that dissolves fat cells under chin",
        "cost": "$1,200-$2,400 (2-4 sessions)",
        "how_long_lasts": "Permanent (fat cells destroyed)",
        "recovery": "1-2 weeks swelling",
        "ideal_for": ["Double chin", "Submental fat"],
    },
    "sculptra": {
        "name": "Sculptra (Collagen Stimulator)",
        "description": "Injectable that stimulates your own collagen production",
        "cost": "$800-$1,500 per vial (2-3 vials typical)",
        "how_long_lasts": "2+ years",
        "recovery": "None (massage required)",
        "ideal_for": ["Volume loss", "Hollow cheeks", "Aging hands"],
    },
}

@dataclass
class HiddenProcedure:
    name: str
    description: str
    cost: Dict[str, str]
    how_long_lasts: str
    recovery: str
    ideal_for: List[str]
    disclaimer: str = MEDICAL_DISCLAIMER
    def to_dict(self): return asdict(self)

class HiddenProceduresEngine:
    def __init__(self):
        self.data_dir = DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.procedures = HIDDEN_PROCEDURES
    
    def get_all_procedures(self): return self.procedures
    def get_procedure_info(self, key: str): return self.procedures.get(key)
    
    def compare_to_surgery(self, procedure_key: str) -> Dict:
        proc = self.procedures.get(procedure_key)
        if not proc: return {}
        return {
            "procedure": proc["name"],
            "cost": proc["cost"],
            "recovery": proc["recovery"],
            "comparison": proc.get("vs_surgery", "Non-surgical alternative"),
            "disclaimer": MEDICAL_DISCLAIMER,
        }

if __name__ == "__main__":
    engine = HiddenProceduresEngine()
    print("Hidden Procedures: PDO threads cost:", engine.get_procedure_info("pdo_threads")["cost"])
