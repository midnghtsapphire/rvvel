"""Master Platform: AI Makeup Advisor - Streamlined Version
Face analysis, product recommendations with affiliate links, budget tiers.
Author: Audrey Evans
"""
import os, json
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

@dataclass
class MakeupProfile:
    face_shape: str  # oval, round, square, heart, oblong, diamond
    skin_tone: str   # fair, light, medium, tan, deep
    undertone: str   # warm, cool, neutral, olive
    skin_type: str   # oily, dry, combination, normal, sensitive
    budget: str      # drugstore, mid_range, luxury
    fragrance_pref: str  # fragrance_free, light, natural, sensory_friendly

class MakeupAdvisor:
    def __init__(self, amazon_tag="audreyevans-20"):
        self.amazon_tag = amazon_tag
        self.foundations = {
            "drugstore": [{"name": "Maybelline Fit Me", "price": "$8", "asin": "B00PFCTQPC"}],
            "mid_range": [{"name": "Fenty Pro Filt'r", "price": "$40", "asin": "B074WGWKJF"}],
            "luxury": [{"name": "Armani Luminous Silk", "price": "$69", "asin": "B001EYURQW"}],
        }
    
    def generate_affiliate_link(self, asin: str) -> str:
        return f"https://www.amazon.com/dp/{asin}?tag={self.amazon_tag}"
    
    def recommend_foundation(self, skin_type: str, budget: str) -> List[Dict]:
        products = self.foundations.get(budget, [])
        return [{**p, "affiliate_link": self.generate_affiliate_link(p["asin"])} for p in products]
    
    def get_contouring_guide(self, face_shape: str) -> Dict:
        guides = {
            "oval": {"technique": "Light contouring", "contour": ["Under cheekbones"], "highlight": ["Center forehead", "Nose bridge"]},
            "round": {"technique": "Create angles", "contour": ["Sides of forehead", "Jawline"], "highlight": ["Center forehead", "Chin"]},
            "square": {"technique": "Soften angles", "contour": ["Jawline corners"], "highlight": ["Center forehead", "Chin"]},
        }
        return guides.get(face_shape, guides["oval"])
    
    def build_full_routine(self, profile: MakeupProfile) -> Dict:
        return {
            "profile": asdict(profile),
            "foundation": self.recommend_foundation(profile.skin_type, profile.budget),
            "contour": self.get_contouring_guide(profile.face_shape),
            "disclaimer": "Product recommendations include affiliate links.",
        }

if __name__ == "__main__":
    advisor = MakeupAdvisor()
    profile = MakeupProfile("oval", "medium", "warm", "combination", "drugstore", "fragrance_free")
    routine = advisor.build_full_routine(profile)
    print(f"Foundation: {routine['foundation'][0]['name']}")
