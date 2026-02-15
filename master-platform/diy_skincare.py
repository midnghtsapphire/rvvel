"""
Master Platform: DIY Skincare & Homemade Alternatives
Recipes for making your own skincare products at home.
Author: Audrey Evans
"""
import json
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

DATA_DIR = Path(__file__).parent / "data" / "diy_skincare"
SAFETY_DISCLAIMER = "DISCLAIMER: DIY skincare is for educational purposes. Patch test all recipes. Consult dermatologist for skin concerns."

DIY_RECIPES = {
    "moisturizer": {
        "name": "DIY Rich Moisturizer",
        "commercial_equivalent": "CeraVe Moisturizing Cream ($15)",
        "diy_cost": "$3 per batch",
        "savings": "$12 per batch (80% savings)",
        "ingredients": [
            "1/4 cup shea butter ($2)",
            "2 tbsp coconut oil ($0.50)",
            "1 tbsp jojoba oil ($0.50)",
            "5 drops vitamin E oil (optional)",
        ],
        "instructions": [
            "Melt shea butter and coconut oil in double boiler",
            "Remove from heat, add jojoba oil and vitamin E",
            "Let cool slightly, then whip with hand mixer until fluffy",
            "Store in airtight jar, use within 3 months",
        ],
        "shelf_life": "3 months (refrigerate to extend)",
        "good_for": ["Dry skin", "Winter hydration", "Body butter"],
    },
    "face_mask": {
        "name": "DIY Brightening Face Mask",
        "commercial_equivalent": "Glamglow Supermud ($60)",
        "diy_cost": "$1 per use",
        "savings": "$59 per use",
        "ingredients": [
            "1 tbsp honey (antibacterial, hydrating)",
            "1 tsp turmeric (brightening)",
            "1 tbsp yogurt (lactic acid exfoliation)",
        ],
        "instructions": [
            "Mix all ingredients in bowl",
            "Apply to clean face, avoid eyes",
            "Leave on 10-15 minutes",
            "Rinse with warm water",
        ],
        "frequency": "1-2x per week",
        "good_for": ["Dull skin", "Hyperpigmentation", "Acne"],
        "warning": "Turmeric may temporarily stain skin yellow (fades in hours)",
    },
    "lip_scrub": {
        "name": "DIY Lip Scrub",
        "commercial_equivalent": "Lush Lip Scrub ($10)",
        "diy_cost": "$0.50 per batch",
        "savings": "$9.50 per batch",
        "ingredients": [
            "1 tbsp sugar",
            "1 tsp honey",
            "1 tsp coconut oil",
        ],
        "instructions": [
            "Mix all ingredients",
            "Gently scrub lips in circular motions",
            "Rinse and apply lip balm",
        ],
        "shelf_life": "Use immediately or store 1 week",
        "good_for": ["Chapped lips", "Flaky lips", "Before lipstick"],
    },
}

INGREDIENT_SOURCING = {
    "shea_butter": {"where": "Amazon, iHerb, Whole Foods", "cost": "$8-$12 per 8oz"},
    "coconut_oil": {"where": "Grocery store, Amazon", "cost": "$5-$10 per jar"},
    "jojoba_oil": {"where": "Amazon, health food stores", "cost": "$10-$15 per 4oz"},
    "honey": {"where": "Grocery store", "cost": "$5-$10 per jar"},
    "turmeric": {"where": "Grocery store spice aisle", "cost": "$3-$5"},
}

SAFETY_WARNINGS = {
    "what_not_to_mix": [
        "Lemon juice + sun exposure = burns (phototoxic)",
        "Baking soda on face = too harsh, disrupts pH",
        "Essential oils undiluted = irritation, burns",
        "Cinnamon on skin = can burn",
    ],
    "patch_test": "Always patch test on inner arm before applying to face. Wait 24 hours.",
    "sterile_containers": "Use clean, sterilized jars. Bacteria = infections.",
    "expiration": "DIY products don't have preservatives. Use within weeks, refrigerate if possible.",
}

@dataclass
class DIYRecipe:
    name: str
    commercial_equivalent: str
    diy_cost: str
    savings: str
    ingredients: List[str]
    instructions: List[str]
    good_for: List[str]
    disclaimer: str = SAFETY_DISCLAIMER
    def to_dict(self): return asdict(self)

class DIYSkincareEngine:
    def __init__(self):
        self.data_dir = DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.recipes = DIY_RECIPES
        self.sourcing = INGREDIENT_SOURCING
        self.safety = SAFETY_WARNINGS
    
    def get_all_recipes(self): return self.recipes
    def get_recipe(self, key: str): return self.recipes.get(key)
    def get_ingredient_sourcing(self): return self.sourcing
    def get_safety_warnings(self): return self.safety
    
    def compare_cost(self, recipe_key: str) -> Dict:
        recipe = self.recipes.get(recipe_key)
        if not recipe: return {}
        return {
            "recipe": recipe["name"],
            "commercial_product": recipe["commercial_equivalent"],
            "diy_cost": recipe["diy_cost"],
            "savings": recipe["savings"],
            "verdict": f"Make it yourself and save {recipe['savings']}!",
            "disclaimer": SAFETY_DISCLAIMER,
        }

if __name__ == "__main__":
    engine = DIYSkincareEngine()
    print("DIY Moisturizer saves:", engine.compare_cost("moisturizer")["savings"])
