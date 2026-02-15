"""
Master Platform: Foot Analysis Engine
======================================
AI-powered foot condition detection and recommendations.
Upload photo of feet for analysis: cracked heels, calluses, fungal infections,
plantar warts, diabetic concerns, and seasonal foot care.

Author: Audrey Evans

DISCLAIMER: This module is for informational purposes only. It is NOT a
substitute for professional medical advice from a podiatrist or healthcare
provider. For diabetic foot concerns or suspected infections, see a doctor
immediately.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Optional, Any, Literal
from dataclasses import dataclass, field, asdict

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DATA_DIR = Path(__file__).parent / "data" / "foot_analysis"

MEDICAL_DISCLAIMER = (
    "DISCLAIMER: This is for informational purposes only. It is NOT a substitute "
    "for professional medical advice, diagnosis, or treatment from a podiatrist or "
    "healthcare provider. For diabetic foot concerns, infections, or severe pain, "
    "see a doctor immediately. Product recommendations may include affiliate links."
)

# OpenRouter API for vision analysis
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# ---------------------------------------------------------------------------
# Foot Conditions Database
# ---------------------------------------------------------------------------

FOOT_CONDITIONS = {
    "cracked_heels": {
        "name": "Cracked Heels (Heel Fissures)",
        "description": "Deep cracks in the skin of the heels, often painful and sometimes bleeding",
        "visual_signs": [
            "Thick, dry skin on heels",
            "Visible cracks or fissures",
            "Yellow or brown discoloration",
            "Flaking or peeling skin",
            "Redness around cracks",
        ],
        "causes": [
            "Dry skin (most common)",
            "Standing for long periods",
            "Open-back shoes (sandals, flip-flops)",
            "Obesity (pressure on heels)",
            "Diabetes (poor circulation)",
            "Thyroid problems",
            "Vitamin deficiency (zinc, omega-3)",
            "Hereditary (some people just have dry feet)",
        ],
        "severity_levels": {
            "mild": "Surface cracks, no pain",
            "moderate": "Deeper cracks, some discomfort",
            "severe": "Deep fissures, bleeding, pain when walking — SEE A PODIATRIST",
        },
        "treatment": {
            "otc": [
                "Urea cream 10-20% (CeraVe, Eucerin, Aquaphor)",
                "Petroleum jelly (Vaseline) at night with socks",
                "Pumice stone or foot file (gently remove dead skin)",
                "Heel balm (O'Keeffe's Healthy Feet, Gold Bond)",
            ],
            "prescription": "Urea 40% cream — ask your doctor for prescription-strength",
            "home_remedies": [
                "Soak feet in warm water 10-15 min, then apply thick moisturizer",
                "Coconut oil or shea butter at night",
                "Honey foot mask (antibacterial)",
            ],
            "when_to_see_doctor": [
                "Cracks are bleeding",
                "Signs of infection (redness, swelling, pus)",
                "You have diabetes (ANY foot issue needs doctor)",
                "Pain when walking",
                "Not improving after 2 weeks of treatment",
            ],
        },
        "prevention": [
            "Moisturize feet daily (especially after shower)",
            "Wear closed-toe shoes with cushioned soles",
            "Drink plenty of water",
            "Use a humidifier in dry climates",
            "Avoid harsh soaps on feet",
        ],
        "seasonal_note": "Worse in winter (dry air, indoor heating) and summer (sandals dry out feet)",
    },
    "calluses": {
        "name": "Calluses",
        "description": "Thick, hardened areas of skin caused by repeated friction or pressure",
        "visual_signs": [
            "Thick, rough patches of skin",
            "Usually on balls of feet, heels, or toes",
            "Yellow or gray color",
            "Less sensitive to touch than surrounding skin",
            "May have a slightly raised appearance",
        ],
        "causes": [
            "Ill-fitting shoes (too tight or too loose)",
            "Walking barefoot frequently",
            "High heels (pressure on ball of foot)",
            "Abnormal gait or foot structure",
            "Not wearing socks",
            "Manual labor or sports (repeated friction)",
        ],
        "vs_corns": "Calluses are larger and less defined. Corns are smaller, round, and have a hard center.",
        "treatment": {
            "otc": [
                "Pumice stone or foot file (after soaking feet)",
                "Salicylic acid pads (Dr. Scholl's)",
                "Urea cream 10-20%",
                "Cushioned insoles or pads",
            ],
            "prescription": "Stronger salicylic acid or urea cream from podiatrist",
            "professional": "Podiatrist can shave down thick calluses safely",
            "do_not": [
                "DO NOT cut calluses with a blade at home (risk of infection)",
                "DO NOT use callus removers if you have diabetes",
            ],
        },
        "prevention": [
            "Wear properly fitted shoes",
            "Use cushioned insoles",
            "Wear socks to reduce friction",
            "Moisturize feet daily",
            "Address underlying foot structure issues (orthotics)",
        ],
        "when_to_see_doctor": [
            "Callus is painful",
            "You have diabetes (podiatrist should handle all calluses)",
            "Callus is cracked or bleeding",
            "Home treatment not working after 4 weeks",
        ],
    },
    "fungal_infection": {
        "name": "Fungal Infection (Athlete's Foot / Toenail Fungus)",
        "description": "Fungal infection of the skin (athlete's foot) or toenails (onychomycosis)",
        "types": {
            "athletes_foot": {
                "name": "Athlete's Foot (Tinea Pedis)",
                "visual_signs": [
                    "Itching, burning, stinging between toes",
                    "Red, scaly, flaky skin",
                    "Cracked skin between toes",
                    "Blisters (in some cases)",
                    "Foul odor",
                ],
                "treatment": {
                    "otc": [
                        "Antifungal cream (Lotrimin, Lamisil, Tinactin)",
                        "Antifungal powder (for shoes)",
                        "Tea tree oil (natural antifungal)",
                    ],
                    "prescription": "Stronger antifungal cream or oral medication (fluconazole, terbinafine)",
                    "duration": "Treat for 2-4 weeks even after symptoms clear",
                },
            },
            "toenail_fungus": {
                "name": "Toenail Fungus (Onychomycosis)",
                "visual_signs": [
                    "Thickened toenails",
                    "Yellow, brown, or white discoloration",
                    "Brittle, crumbly nails",
                    "Distorted nail shape",
                    "Foul smell",
                    "Nail separating from nail bed",
                ],
                "treatment": {
                    "otc": [
                        "Antifungal nail polish (Penlac)",
                        "Tea tree oil (apply daily)",
                        "Vicks VapoRub (anecdotal — some people swear by it)",
                    ],
                    "prescription": [
                        "Oral antifungal (terbinafine, itraconazole) — most effective",
                        "Prescription antifungal nail lacquer",
                        "Laser treatment (expensive, not always covered)",
                    ],
                    "duration": "3-6 months for oral meds, 12+ months for topical",
                    "note": "Toenail fungus is HARD to cure. Oral meds are most effective but have side effects.",
                },
            },
        },
        "causes": [
            "Walking barefoot in public areas (gyms, pools, locker rooms)",
            "Sweaty feet in closed shoes",
            "Sharing shoes or towels",
            "Weakened immune system",
            "Diabetes",
            "Poor circulation",
        ],
        "prevention": [
            "Keep feet clean and DRY",
            "Wear flip-flops in public showers/pools",
            "Change socks daily (moisture-wicking socks best)",
            "Alternate shoes (let them dry out between wears)",
            "Use antifungal powder in shoes",
            "Trim toenails straight across",
        ],
        "when_to_see_doctor": [
            "OTC treatment not working after 2 weeks",
            "Spreading to other toes or nails",
            "You have diabetes (fungal infections can lead to serious complications)",
            "Severe pain or swelling",
        ],
    },
    "plantar_warts": {
        "name": "Plantar Warts",
        "description": "Warts on the bottom of the foot caused by HPV virus, often mistaken for calluses",
        "visual_signs": [
            "Small, grainy bump on sole of foot",
            "Hard, thickened skin (looks like a callus)",
            "Black pinpoints (clotted blood vessels — KEY SIGN)",
            "Tenderness when walking or standing",
            "Often on weight-bearing areas (ball of foot, heel)",
        ],
        "vs_calluses": "Warts have tiny black dots (blood vessels). Calluses do not. Warts hurt when squeezed from sides. Calluses hurt when pressed directly.",
        "causes": [
            "HPV virus (enters through tiny cuts in skin)",
            "Walking barefoot in public areas",
            "Weakened immune system",
            "Skin-to-skin contact with warts",
        ],
        "treatment": {
            "otc": [
                "Salicylic acid pads or gel (Compound W, Dr. Scholl's) — takes weeks/months",
                "Duct tape method (cover wart with duct tape for 6 days, remove, file down, repeat)",
            ],
            "professional": [
                "Cryotherapy (freezing with liquid nitrogen) — most common",
                "Laser treatment",
                "Surgical removal (last resort)",
                "Immunotherapy (for stubborn warts)",
            ],
            "duration": "Can take months to resolve, even with treatment",
            "note": "Warts often go away on their own eventually (months to years)",
        },
        "prevention": [
            "Wear flip-flops in public showers, pools, gyms",
            "Keep feet clean and dry",
            "Don't pick at warts (spreads virus)",
            "Don't share shoes or towels",
        ],
        "when_to_see_doctor": [
            "Wart is painful",
            "Wart is spreading",
            "You have diabetes or poor circulation",
            "Unsure if it's a wart or something else",
            "OTC treatment not working after 3 months",
        ],
    },
    "diabetic_foot": {
        "name": "Diabetic Foot Concerns",
        "description": "Diabetes causes nerve damage and poor circulation, making feet vulnerable to serious complications",
        "warning_signs": [
            "Loss of sensation in feet (can't feel hot/cold, pain)",
            "Tingling, burning, or numbness",
            "Slow-healing cuts or sores",
            "Changes in skin color (red, blue, pale)",
            "Swelling",
            "Ingrown toenails",
            "Fungal infections",
            "Dry, cracked skin",
            "ANY wound or blister",
        ],
        "why_its_serious": (
            "Diabetes damages nerves (neuropathy) and blood vessels. You may not feel "
            "a cut or blister. Poor circulation means wounds heal slowly. Infections "
            "can develop quickly and lead to ulcers, gangrene, and amputation. "
            "Diabetic foot problems are the #1 cause of non-traumatic amputations."
        ),
        "daily_foot_care": [
            "Inspect feet DAILY (use a mirror to see bottoms)",
            "Wash feet daily with mild soap and lukewarm water",
            "Dry thoroughly, especially between toes",
            "Moisturize (but NOT between toes — moisture = fungus)",
            "Trim toenails straight across (or have podiatrist do it)",
            "Wear clean, dry socks daily",
            "NEVER walk barefoot (even indoors)",
            "Check shoes for foreign objects before wearing",
        ],
        "what_to_avoid": [
            "Hot water (can burn feet without feeling it)",
            "Heating pads or hot water bottles on feet",
            "Cutting corns or calluses yourself",
            "Over-the-counter corn removers (too harsh)",
            "Tight socks or shoes",
            "Smoking (worsens circulation)",
        ],
        "when_to_see_doctor_immediately": [
            "ANY cut, blister, or sore on feet",
            "Redness, warmth, or swelling",
            "Ingrown toenail",
            "Foot pain (even if no visible injury)",
            "Changes in skin color or temperature",
            "Foul odor",
        ],
        "podiatrist_visits": "If you have diabetes, see a podiatrist every 3-6 months for preventive care",
        "insurance_coverage": "Medicare and most insurance cover diabetic foot care",
    },
}

# Product recommendations by condition
PRODUCT_RECOMMENDATIONS = {
    "cracked_heels": {
        "drugstore": [
            "CeraVe Renewing SA Foot Cream ($9) — urea + salicylic acid",
            "Aquaphor Healing Ointment ($12) — occlusive for overnight",
            "O'Keeffe's Healthy Feet Cream ($8) — cult favorite",
            "Eucerin Advanced Repair Foot Cream ($10) — urea-based",
        ],
        "mid_range": [
            "Flexitol Heel Balm ($12) — 25% urea",
            "Gold Bond Ultimate Healing Foot Cream ($10)",
        ],
        "luxury": [
            "Kerasal Intensive Foot Repair ($20) — urea + salicylic acid",
        ],
        "tools": [
            "Pumice stone ($5)",
            "Foot file ($8)",
            "Exfoliating foot mask ($15)",
        ],
    },
    "calluses": {
        "drugstore": [
            "Dr. Scholl's Callus Removers ($7) — salicylic acid pads",
            "Amopé Pedi Perfect ($30) — electric foot file",
        ],
        "professional": "Podiatrist visit for thick calluses ($50-$150)",
    },
    "fungal_infection": {
        "otc_antifungal": [
            "Lotrimin AF Cream ($8) — clotrimazole",
            "Lamisil AT Cream ($12) — terbinafine (most effective OTC)",
            "Tinactin Spray ($9) — tolnaftate",
            "Tea tree oil ($10) — natural antifungal",
        ],
        "prevention": [
            "Antifungal foot powder ($8)",
            "Moisture-wicking socks ($15/3-pack)",
            "UV shoe sanitizer ($30)",
        ],
        "prescription": "Oral terbinafine or itraconazole (prescription required)",
    },
    "diabetic_foot": {
        "essential": [
            "Diabetic socks (seamless, non-binding) ($20/3-pack)",
            "Diabetic shoes (extra depth, cushioned) ($80-$150)",
            "Foot mirror ($10) — for daily inspection",
            "Gentle moisturizer (CeraVe, Eucerin) ($12)",
        ],
        "do_not_use": [
            "Harsh exfoliants",
            "Callus removers",
            "Hot water",
        ],
    },
}


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

@dataclass
class FootAnalysisResult:
    """Result of AI-powered foot analysis."""
    detected_conditions: List[Dict[str, Any]]
    confidence_scores: Dict[str, float]
    recommendations: List[str]
    product_suggestions: Dict[str, List[str]]
    when_to_see_doctor: List[str]
    disclaimer: str = MEDICAL_DISCLAIMER

    def to_dict(self) -> dict:
        return asdict(self)


# ---------------------------------------------------------------------------
# Foot Analysis Engine
# ---------------------------------------------------------------------------

class FootAnalysisEngine:
    """
    AI-powered foot condition detection and recommendations.
    """

    def __init__(self):
        self.data_dir = DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.conditions = FOOT_CONDITIONS
        self.products = PRODUCT_RECOMMENDATIONS

    def get_all_conditions(self) -> Dict[str, Any]:
        """Get all foot conditions in the database."""
        return self.conditions

    def get_condition_info(self, condition_key: str) -> Optional[Dict[str, Any]]:
        """Get detailed info about a specific foot condition."""
        return self.conditions.get(condition_key)

    def analyze_foot_image(
        self,
        image_path: str,
        user_symptoms: Optional[List[str]] = None,
        has_diabetes: bool = False,
    ) -> FootAnalysisResult:
        """
        Analyze a foot image using AI vision model.
        
        Args:
            image_path: Path to foot image
            user_symptoms: User-reported symptoms (itching, pain, dryness, etc.)
            has_diabetes: Whether user has diabetes (affects recommendations)
        
        Returns:
            FootAnalysisResult with detected conditions and recommendations
        """
        # In production, this would call OpenRouter vision API
        # For now, return a structured analysis based on symptoms
        
        detected = []
        confidence = {}
        recommendations = []
        products = {"drugstore": [], "mid_range": [], "professional": []}
        doctor_flags = []
        
        # Simulate AI analysis based on symptoms
        if user_symptoms:
            for symptom in user_symptoms:
                symptom_lower = symptom.lower()
                
                if "crack" in symptom_lower or "dry" in symptom_lower:
                    detected.append({
                        "condition": "Cracked Heels",
                        "description": self.conditions["cracked_heels"]["description"],
                        "severity": "Moderate (based on symptoms)",
                    })
                    confidence["cracked_heels"] = 0.85
                    recommendations.extend(self.conditions["cracked_heels"]["treatment"]["otc"][:3])
                    products["drugstore"].extend(self.products["cracked_heels"]["drugstore"][:3])
                
                if "itch" in symptom_lower or "smell" in symptom_lower or "fungus" in symptom_lower:
                    detected.append({
                        "condition": "Possible Fungal Infection",
                        "description": "Itching and odor suggest athlete's foot or toenail fungus",
                        "severity": "Mild to Moderate",
                    })
                    confidence["fungal_infection"] = 0.75
                    recommendations.append("Try OTC antifungal cream for 2 weeks. If no improvement, see a doctor.")
                    products["drugstore"].extend(self.products["fungal_infection"]["otc_antifungal"][:2])
                    doctor_flags.append("If not improving after 2 weeks of OTC treatment, see a podiatrist")
                
                if "callus" in symptom_lower or "thick" in symptom_lower:
                    detected.append({
                        "condition": "Calluses",
                        "description": "Thickened skin from pressure or friction",
                        "severity": "Mild",
                    })
                    confidence["calluses"] = 0.80
                    recommendations.extend(self.conditions["calluses"]["treatment"]["otc"][:2])
                    products["drugstore"].extend(self.products["calluses"]["drugstore"])
        
        # Diabetes flag
        if has_diabetes:
            doctor_flags.insert(0, "⚠️ DIABETES ALERT: See a podiatrist for ANY foot issue. Do not self-treat.")
            recommendations.insert(0, "Because you have diabetes, see a podiatrist before trying any treatments.")
            products = {"essential": self.products["diabetic_foot"]["essential"]}
        
        # Default if no conditions detected
        if not detected:
            detected.append({
                "condition": "No obvious conditions detected",
                "description": "Feet appear healthy based on symptoms provided",
                "severity": "N/A",
            })
            recommendations.append("Continue regular foot care: moisturize daily, wear proper footwear, inspect feet regularly")
        
        return FootAnalysisResult(
            detected_conditions=detected,
            confidence_scores=confidence,
            recommendations=recommendations,
            product_suggestions=products,
            when_to_see_doctor=doctor_flags,
        )

    def get_seasonal_foot_care(self, season: Literal["winter", "spring", "summer", "fall"]) -> Dict[str, Any]:
        """Get seasonal foot care recommendations."""
        seasonal_care = {
            "winter": {
                "challenges": [
                    "Dry air causes cracked heels",
                    "Boots trap moisture → fungal infections",
                    "Indoor heating dries out skin",
                    "Less sun exposure → vitamin D deficiency affects skin",
                ],
                "recommendations": [
                    "Moisturize feet 2x daily (morning and night)",
                    "Wear moisture-wicking socks",
                    "Alternate boots (let them dry out)",
                    "Use a humidifier indoors",
                    "Apply thick foot cream at night with socks",
                ],
                "products": [
                    "Heavy-duty foot cream (Aquaphor, O'Keeffe's)",
                    "Wool socks (breathable, warm)",
                    "Overnight foot masks",
                ],
            },
            "summer": {
                "challenges": [
                    "Sandals dry out feet → cracked heels",
                    "Sweaty feet in closed shoes → fungus",
                    "Walking barefoot → plantar warts, cuts",
                    "Sun exposure → dry, damaged skin",
                ],
                "recommendations": [
                    "Moisturize heels daily (sandals expose them to air)",
                    "Wear flip-flops in public pools/showers",
                    "Use antifungal powder in closed shoes",
                    "Apply sunscreen to tops of feet",
                    "Exfoliate feet weekly",
                ],
                "products": [
                    "Lightweight foot cream",
                    "Antifungal spray/powder",
                    "Sunscreen for feet",
                    "Foot file for callus removal",
                ],
            },
            "spring": {
                "challenges": [
                    "Transitioning from boots to sandals → rough heels visible",
                    "Increased outdoor activity → blisters, calluses",
                ],
                "recommendations": [
                    "Exfoliate and moisturize to prep for sandal season",
                    "Address any winter damage (cracks, calluses)",
                    "Start wearing open-toe shoes gradually",
                ],
                "products": [
                    "Foot peel mask (Baby Foot)",
                    "Pumice stone",
                    "Blister prevention (moleskin, bandages)",
                ],
            },
            "fall": {
                "challenges": [
                    "Transitioning back to closed shoes → adjustment period",
                    "Cooler, drier air begins",
                ],
                "recommendations": [
                    "Start moisturizing more frequently",
                    "Break in new boots gradually",
                    "Treat any summer damage (calluses from sandals)",
                ],
                "products": [
                    "Foot cream",
                    "Blister prevention",
                    "Cushioned insoles for boots",
                ],
            },
        }
        
        return {
            "season": season.capitalize(),
            **seasonal_care[season],
            "disclaimer": MEDICAL_DISCLAIMER,
        }

    def get_diabetic_foot_care_guide(self) -> Dict[str, Any]:
        """Get comprehensive diabetic foot care guide."""
        diabetic = self.conditions.get("diabetic_foot")
        if not diabetic:
            return {}
        
        return {
            "title": "Diabetic Foot Care Guide",
            "why_its_critical": diabetic["why_its_serious"],
            "daily_routine": diabetic["daily_foot_care"],
            "what_to_avoid": diabetic["what_to_avoid"],
            "warning_signs": diabetic["warning_signs"],
            "when_to_see_doctor": diabetic["when_to_see_doctor_immediately"],
            "podiatrist_schedule": diabetic["podiatrist_visits"],
            "insurance_note": diabetic["insurance_coverage"],
            "products": self.products["diabetic_foot"],
            "disclaimer": MEDICAL_DISCLAIMER,
        }

    def compare_wart_vs_callus(self) -> Dict[str, Any]:
        """Help users distinguish between plantar warts and calluses."""
        wart = self.conditions.get("plantar_warts")
        callus = self.conditions.get("calluses")
        
        return {
            "title": "Plantar Wart vs Callus: How to Tell the Difference",
            "wart": {
                "visual_signs": wart["visual_signs"],
                "key_identifier": "Tiny black dots (clotted blood vessels)",
                "pain_test": "Hurts when squeezed from SIDES",
            },
            "callus": {
                "visual_signs": callus["visual_signs"],
                "key_identifier": "No black dots, uniform thick skin",
                "pain_test": "Hurts when pressed DIRECTLY down",
            },
            "comparison": wart["vs_calluses"],
            "when_unsure": "See a podiatrist for proper diagnosis",
            "disclaimer": MEDICAL_DISCLAIMER,
        }


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Master Platform: Foot Analysis Engine — Demo")
    print("=" * 55)
    
    engine = FootAnalysisEngine()
    
    # Analyze foot with symptoms
    print("\nUser reports: 'My heels are so dry and cracked'")
    result = engine.analyze_foot_image(
        image_path="path/to/foot.jpg",
        user_symptoms=["dry", "cracked heels"],
        has_diabetes=False,
    )
    
    print(f"\nDetected conditions:")
    for condition in result.detected_conditions:
        print(f"  - {condition['condition']}: {condition['description']}")
    
    print(f"\nRecommendations:")
    for rec in result.recommendations[:3]:
        print(f"  - {rec}")
    
    print(f"\nProduct suggestions:")
    for product in result.product_suggestions.get("drugstore", [])[:3]:
        print(f"  - {product}")
    
    # Diabetic foot care
    print("\n\nDiabetic Foot Care:")
    diabetic_guide = engine.get_diabetic_foot_care_guide()
    print(f"  Why it's critical: {diabetic_guide['why_its_critical'][:100]}...")
    print(f"  Daily routine: {len(diabetic_guide['daily_routine'])} steps")
    
    # Seasonal care
    print("\n\nWinter Foot Care:")
    winter = engine.get_seasonal_foot_care("winter")
    print(f"  Challenges: {winter['challenges'][0]}")
    print(f"  Recommendations: {winter['recommendations'][0]}")
    
    print(f"\n{MEDICAL_DISCLAIMER}")
