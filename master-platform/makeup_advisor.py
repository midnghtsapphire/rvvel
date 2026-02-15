"""
Master Platform: AI Makeup Advisor
Analyze face shape, skin tone, features — recommend products with affiliate links.
Budget tiers: drugstore, mid-range, luxury. Tutorial recommendations.
Author: Audrey Evans
"""
import os
import json
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field, asdict
from enum import Enum

DATA_DIR = Path(__file__).parent / "data" / "makeup_advisor"
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_URL = "https://openrouter.ai/api/v1"

class FaceShape(str, Enum):
    OVAL = "oval"
    ROUND = "round"
    SQUARE = "square"
    HEART = "heart"
    OBLONG = "oblong"
    DIAMOND = "diamond"

class SkinTone(str, Enum):
    FAIR = "fair"
    LIGHT = "light"
    MEDIUM = "medium"
    TAN = "tan"
    DEEP = "deep"

class Undertone(str, Enum):
    WARM = "warm"
    COOL = "cool"
    NEUTRAL = "neutral"
    OLIVE = "olive"

class BudgetTier(str, Enum):
    DRUGSTORE = "drugstore"        # Under $15
    MID_RANGE = "mid_range"        # $15-$40
    LUXURY = "luxury"              # $40+
    ALL = "all"

# ---------------------------------------------------------------------------
# Product Database (with affiliate link placeholders)
# ---------------------------------------------------------------------------

FOUNDATION_DB = {
    "drugstore": [
        {"name": "Maybelline Fit Me Matte", "price": "$8", "shades": 40, "best_for": ["oily", "combination"], "asin": "B00PFCTQPC"},
        {"name": "L'Oreal True Match", "price": "$11", "shades": 45, "best_for": ["dry", "normal"], "asin": "B000GCPB0C"},
        {"name": "NYX Can't Stop Won't Stop", "price": "$15", "shades": 45, "best_for": ["oily"], "asin": "B07GZR5VGQ"},
        {"name": "e.l.f. Flawless Finish", "price": "$6", "shades": 40, "best_for": ["all"], "asin": "B07YDG5C5V"},
    ],
    "mid_range": [
        {"name": "NARS Sheer Glow", "price": "$49", "shades": 30, "best_for": ["dry", "normal"], "asin": "B001EYURQW"},
        {"name": "Fenty Beauty Pro Filt'r", "price": "$40", "shades": 50, "best_for": ["oily", "combination"], "asin": "B074WGWKJF"},
        {"name": "MAC Studio Fix", "price": "$38", "shades": 60, "best_for": ["all"], "asin": "B000BNHGXK"},
    ],
    "luxury": [
        {"name": "Giorgio Armani Luminous Silk", "price": "$69", "shades": 40, "best_for": ["all"], "asin": "B001EYURQW"},
        {"name": "Tom Ford Traceless", "price": "$88", "shades": 30, "best_for": ["normal", "dry"], "asin": "B00GXCFM3S"},
    ],
}

CONTOURING_BY_FACE_SHAPE = {
    FaceShape.OVAL: {
        "technique": "Light contouring — oval is the 'ideal' shape, just enhance",
        "contour_areas": ["Slightly under cheekbones", "Temples (subtle)"],
        "highlight_areas": ["Center of forehead", "Bridge of nose", "Cupid's bow"],
    },
    FaceShape.ROUND: {
        "technique": "Create angles to elongate face",
        "contour_areas": ["Sides of forehead", "Under cheekbones (blend down)", "Jawline"],
        "highlight_areas": ["Center of forehead", "Chin", "Under eyes"],
    },
    FaceShape.SQUARE: {
        "technique": "Soften angles and jawline",
        "contour_areas": ["Corners of forehead", "Jawline corners", "Under cheekbones"],
        "highlight_areas": ["Center of forehead", "Center of chin", "Under eyes"],
    },
    FaceShape.HEART: {
        "technique": "Balance wider forehead with narrower chin",
        "contour_areas": ["Sides of forehead", "Temples", "Under cheekbones"],
        "highlight_areas": ["Center of chin", "Under eyes", "Center of forehead"],
    },
    FaceShape.OBLONG: {
        "technique": "Create width and shorten appearance",
        "contour_areas": ["Top of forehead", "Under chin", "Under cheekbones"],
        "highlight_areas": ["Sides of face", "Under eyes", "Cheekbones"],
    },
    FaceShape.DIAMOND: {
        "technique": "Soften cheekbones, add width to forehead and chin",
        "contour_areas": ["Cheekbone tips", "Under cheekbones"],
        "highlight_areas": ["Forehead center", "Chin", "Under eyes"],
    },
}

LIP_COLOR_BY_UNDERTONE = {
    Undertone.WARM: {
        "best_colors": ["Coral", "Peach", "Warm red", "Terracotta", "Warm nude"],
        "avoid": ["Blue-based pinks", "Cool berries"],
        "drugstore": "Maybelline SuperStay Matte Ink in Loyalist ($10)",
        "luxury": "Charlotte Tilbury Pillow Talk Warm ($34)",
    },
    Undertone.COOL: {
        "best_colors": ["Berry", "Mauve", "Blue-red", "Plum", "Cool pink"],
        "avoid": ["Orange-based colors", "Warm corals"],
        "drugstore": "Revlon Super Lustrous in Berry Haute ($9)",
        "luxury": "MAC Ruby Woo ($21)",
    },
    Undertone.NEUTRAL: {
        "best_colors": ["Rose", "Dusty pink", "True red", "Mauve", "Nude pink"],
        "avoid": ["Nothing — neutrals can wear almost anything!"],
        "drugstore": "NYX Lip Lingerie in Bedtime Flirt ($7)",
        "luxury": "NARS Velvet Matte in Dolce Vita ($28)",
    },
    Undertone.OLIVE: {
        "best_colors": ["Brick red", "Warm berry", "Terracotta", "Deep plum", "Warm nude"],
        "avoid": ["Pastel pinks", "Bright corals"],
        "drugstore": "L'Oreal Colour Riche in Spiced Cider ($10)",
        "luxury": "Tom Ford Lip Color in Casablanca ($58)",
    },
}

FRAGRANCE_PREFERENCES = {
    "fragrance_free": {
        "description": "No added fragrance — ideal for sensitive skin, migraines, autism/sensory issues",
        "brands": ["Clinique", "CeraVe", "Vanicream", "La Roche-Posay", "e.l.f."],
    },
    "light_subtle": {
        "description": "Barely-there scent that fades quickly",
        "brands": ["Glossier", "Milk Makeup", "Ilia", "Kosas"],
    },
    "natural_essential_oils": {
        "description": "Plant-derived scents only, no synthetic fragrance",
        "brands": ["Tata Harper", "Herbivore", "Youth to the People", "Drunk Elephant"],
    },
    "sensory_friendly": {
        "description": "For AuDHD/autism — no strong smells, no weird textures, no sticky/tacky feel",
        "brands": ["Clinique", "Bare Minerals", "e.l.f.", "CeraVe"],
        "texture_notes": "Avoid: sticky glosses, heavy creams, gritty scrubs. Prefer: lightweight, fast-absorbing, smooth",
    },
}

# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

@dataclass
class UserMakeupProfile:
    face_shape: Optional[FaceShape] = None
    skin_tone: Optional[SkinTone] = None
    undertone: Optional[Undertone] = None
    skin_type: Optional[str] = None  # oily, dry, combination, normal, sensitive
    budget_tier: BudgetTier = BudgetTier.ALL
    fragrance_preference: Optional[str] = None
    concerns: List[str] = field(default_factory=list)  # acne, aging, dark circles, etc.
    age_range: Optional[str] = None

    def to_dict(self): return asdict(self)

@dataclass
class MakeupRecommendation:
    category: str  # foundation, lips, contour, eyes, etc.
    products: List[Dict[str, Any]]
    technique: str
    tutorial_keywords: List[str]
    affiliate_links: List[str]
    disclaimer: str = "Product recommendations may include affiliate links."

    def to_dict(self): return asdict(self)


# ---------------------------------------------------------------------------
# Makeup Advisor Engine
# ---------------------------------------------------------------------------

class MakeupAdvisorEngine:
    """AI-powered makeup recommendations with affiliate link integration."""

    def __init__(self, amazon_associate_tag: str = "audreyevans-20"):
        self.data_dir = DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.amazon_tag = amazon_associate_tag
        self.foundations = FOUNDATION_DB
        self.contouring = CONTOURING_BY_FACE_SHAPE
        self.lip_colors = LIP_COLOR_BY_UNDERTONE
        self.fragrance = FRAGRANCE_PREFERENCES

    def generate_affiliate_link(self, asin: str) -> str:
        """Generate Amazon affiliate link from ASIN."""
        return f"https://www.amazon.com/dp/{asin}?tag={self.amazon_tag}"

    def recommend_foundation(
        self, skin_type: str, budget: BudgetTier = BudgetTier.ALL
    ) -> List[Dict[str, Any]]:
        """Recommend foundations by skin type and budget."""
        results = []
        tiers = [budget.value] if budget != BudgetTier.ALL else ["drugstore", "mid_range", "luxury"]

        for tier in tiers:
            for product in self.foundations.get(tier, []):
                if skin_type in product["best_for"] or "all" in product["best_for"]:
                    results.append({
                        **product,
                        "tier": tier,
                        "affiliate_link": self.generate_affiliate_link(product["asin"]),
                    })
        return results

    def get_contouring_guide(self, face_shape: FaceShape) -> Dict[str, Any]:
        """Get contouring guide for face shape."""
        guide = self.contouring.get(face_shape, {})
        return {
            "face_shape": face_shape.value,
            **guide,
            "tutorial_search": f"How to contour {face_shape.value} face shape",
            "youtube_search": f"https://www.youtube.com/results?search_query=contour+{face_shape.value}+face",
        }

    def recommend_lip_color(self, undertone: Undertone) -> Dict[str, Any]:
        """Recommend lip colors by undertone."""
        return self.lip_colors.get(undertone, {})

    def get_fragrance_filtered_products(self, preference: str) -> Dict[str, Any]:
        """Get products filtered by fragrance preference."""
        return self.fragrance.get(preference, {})

    def build_full_face_routine(self, profile: UserMakeupProfile) -> Dict[str, Any]:
        """Build a complete makeup routine based on user profile."""
        routine = {
            "profile": profile.to_dict(),
            "steps": [],
        }

        # Step 1: Primer
        routine["steps"].append({
            "step": 1,
            "category": "Primer",
            "recommendation": "Mattifying primer for oily skin, hydrating for dry" if profile.skin_type else "Universal primer",
            "drugstore": "e.l.f. Poreless Putty Primer ($10)",
            "luxury": "Tatcha Silk Canvas ($52)",
        })

        # Step 2: Foundation
        if profile.skin_type:
            foundations = self.recommend_foundation(profile.skin_type, profile.budget_tier)
            routine["steps"].append({
                "step": 2,
                "category": "Foundation",
                "recommendations": foundations[:3],
            })

        # Step 3: Concealer
        routine["steps"].append({
            "step": 3,
            "category": "Concealer",
            "drugstore": "Maybelline Instant Age Rewind ($10)",
            "luxury": "NARS Radiant Creamy ($32)",
        })

        # Step 4: Contour
        if profile.face_shape:
            contour = self.get_contouring_guide(profile.face_shape)
            routine["steps"].append({
                "step": 4,
                "category": "Contour & Highlight",
                **contour,
            })

        # Step 5: Eyes
        routine["steps"].append({
            "step": 5,
            "category": "Eyes",
            "drugstore": "NYX Ultimate Shadow Palette ($18)",
            "luxury": "Natasha Denona Mini Palette ($29)",
        })

        # Step 6: Lips
        if profile.undertone:
            lips = self.recommend_lip_color(profile.undertone)
            routine["steps"].append({
                "step": 6,
                "category": "Lips",
                **lips,
            })

        # Step 7: Setting
        routine["steps"].append({
            "step": 7,
            "category": "Setting Spray",
            "drugstore": "NYX Matte Finish Setting Spray ($9)",
            "luxury": "Charlotte Tilbury Airbrush Flawless ($35)",
        })

        return routine

    async def analyze_face_image(self, image_path: str) -> Dict[str, Any]:
        """Use AI vision to analyze face shape, skin tone, and features."""
        from openai import OpenAI

        client = OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url=OPENROUTER_URL,
        )

        import base64
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode()

        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-001",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": (
                        "Analyze this face for makeup recommendations. Determine:\n"
                        "1. Face shape (oval, round, square, heart, oblong, diamond)\n"
                        "2. Approximate skin tone (fair, light, medium, tan, deep)\n"
                        "3. Undertone (warm, cool, neutral, olive)\n"
                        "4. Notable features (eye shape, lip shape, brow shape)\n"
                        "Return as JSON with keys: face_shape, skin_tone, undertone, features"
                    )},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}},
                ],
            }],
        )

        # Parse AI response
        analysis_text = response.choices[0].message.content
        try:
            analysis = json.loads(analysis_text)
        except json.JSONDecodeError:
            analysis = {"raw_analysis": analysis_text, "note": "Manual parsing needed"}

        return {
            "analysis": analysis,
            "disclaimer": "AI analysis is approximate. Results may vary.",
        }


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    engine = MakeupAdvisorEngine()

    profile = UserMakeupProfile(
        face_shape=FaceShape.OVAL,
        skin_tone=SkinTone.MEDIUM,
        undertone=Undertone.WARM,
        skin_type="combination",
        budget_tier=BudgetTier.DRUGSTORE,
        fragrance_preference="fragrance_free",
    )

    routine = engine.build_full_face_routine(profile)
    print("Full Face Routine:")
    for step in routine["steps"]:
        print(f"  Step {step['step']}: {step['category']}")

    print("\nContouring for oval face:")
    contour = engine.get_contouring_guide(FaceShape.OVAL)
    print(f"  Technique: {contour['technique']}")

    print("\nLip colors for warm undertone:")
    lips = engine.recommend_lip_color(Undertone.WARM)
    print(f"  Best: {', '.join(lips['best_colors'])}")
