"""
Project Face: Recommendations Engine
=====================================
Generates skincare product and procedure recommendations based on skin analysis.
Includes budget-aware product suggestions and routine building.

Author: Audrey Evans
"""

import json
from typing import List, Dict, Optional, Literal
from dataclasses import dataclass, field, asdict
from analysis_engine import SkinAnalysisResult, AcneAnalysis, SkinCondition


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

@dataclass
class ProductRecommendation:
    """A recommended skincare product."""
    category: str  # cleanser, moisturizer, treatment, sunscreen, etc.
    product_name: str
    brand: str
    price_tier: Literal["drugstore", "mid_range", "luxury"]
    price_usd: float
    key_ingredients: List[str]
    benefits: List[str]
    usage: str  # morning, evening, or both
    amazon_search_term: str  # For affiliate link generation
    notes: str = ""


@dataclass
class ProcedureRecommendation:
    """A recommended cosmetic or dermatological procedure."""
    procedure_name: str
    procedure_type: Literal["in_office", "at_home", "prescription"]
    description: str
    benefits: List[str]
    typical_cost_range: str
    frequency: str
    downtime: str
    requires_professional: bool
    notes: str = ""


@dataclass
class SkincareRoutine:
    """A complete skincare routine (morning or evening)."""
    routine_type: Literal["morning", "evening"]
    steps: List[Dict[str, str]]  # [{step: "1. Cleanser", product: "..."}]


@dataclass
class RecommendationSet:
    """Complete set of recommendations."""
    products: List[ProductRecommendation] = field(default_factory=list)
    procedures: List[ProcedureRecommendation] = field(default_factory=list)
    morning_routine: Optional[SkincareRoutine] = None
    evening_routine: Optional[SkincareRoutine] = None
    ingredient_guidance: Dict[str, List[str]] = field(default_factory=dict)  # to_look_for, to_avoid
    lifestyle_tips: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


# ---------------------------------------------------------------------------
# Recommendations Engine
# ---------------------------------------------------------------------------

class RecommendationsEngine:
    """
    Generates personalized skincare recommendations based on analysis results.
    Budget-aware, ingredient-focused, and routine-building.
    """

    def __init__(self):
        pass

    def generate_recommendations(
        self,
        analysis: SkinAnalysisResult,
        budget: Literal["drugstore", "mid_range", "luxury", "mixed"] = "mixed",
        concerns: Optional[List[str]] = None,
    ) -> RecommendationSet:
        """
        Generate comprehensive recommendations based on skin analysis.
        
        Args:
            analysis: SkinAnalysisResult from the analysis engine
            budget: Budget tier preference
            concerns: Additional user-specified concerns
        
        Returns:
            RecommendationSet with products, procedures, and routines
        """
        recommendations = RecommendationSet()
        
        # Determine primary concerns from analysis
        primary_concerns = self._extract_concerns(analysis, concerns)
        
        # Generate product recommendations
        recommendations.products = self._recommend_products(
            analysis.skin_type,
            primary_concerns,
            budget,
        )
        
        # Generate procedure recommendations
        recommendations.procedures = self._recommend_procedures(primary_concerns)
        
        # Build routines
        recommendations.morning_routine = self._build_routine("morning", recommendations.products)
        recommendations.evening_routine = self._build_routine("evening", recommendations.products)
        
        # Ingredient guidance
        recommendations.ingredient_guidance = self._generate_ingredient_guidance(primary_concerns)
        
        # Lifestyle tips
        recommendations.lifestyle_tips = self._generate_lifestyle_tips(analysis.skin_type, primary_concerns)
        
        return recommendations

    def _extract_concerns(
        self,
        analysis: SkinAnalysisResult,
        user_concerns: Optional[List[str]] = None,
    ) -> List[str]:
        """Extract primary skin concerns from analysis."""
        concerns = set(user_concerns or [])
        
        # From acne analysis
        if analysis.overall_acne and analysis.overall_acne.detected:
            concerns.add("acne")
            if analysis.overall_acne.acne_type:
                concerns.add(f"acne_{analysis.overall_acne.acne_type}")
        
        # From skin condition
        if analysis.overall_condition:
            cond = analysis.overall_condition
            if cond.dark_spots or cond.hyperpigmentation:
                concerns.add("hyperpigmentation")
            if cond.redness:
                concerns.add("redness")
            if cond.dryness:
                concerns.add("dryness")
            if cond.oiliness:
                concerns.add("oiliness")
            if cond.wrinkles in ["moderate", "deep"]:
                concerns.add("aging")
            elif cond.wrinkles == "fine_lines":
                concerns.add("fine_lines")
            if cond.pores == "enlarged":
                concerns.add("enlarged_pores")
        
        # From dermatological flags
        for flag in analysis.dermatological_flags:
            concerns.add(flag.condition)
        
        return list(concerns)

    def _recommend_products(
        self,
        skin_type: str,
        concerns: List[str],
        budget: Literal["drugstore", "mid_range", "luxury", "mixed"],
    ) -> List[ProductRecommendation]:
        """Generate product recommendations based on skin type and concerns."""
        products = []
        
        # Core products (everyone needs these)
        products.extend(self._recommend_cleanser(skin_type, budget))
        products.extend(self._recommend_moisturizer(skin_type, budget))
        products.extend(self._recommend_sunscreen(budget))
        
        # Concern-specific treatments
        if "acne" in concerns or any("acne_" in c for c in concerns):
            products.extend(self._recommend_acne_treatment(concerns, budget))
        
        if "hyperpigmentation" in concerns:
            products.extend(self._recommend_brightening(budget))
        
        if "aging" in concerns or "fine_lines" in concerns:
            products.extend(self._recommend_anti_aging(budget))
        
        if "redness" in concerns or "rosacea" in concerns:
            products.extend(self._recommend_calming(budget))
        
        if "dryness" in concerns:
            products.extend(self._recommend_hydrating(budget))
        
        if "enlarged_pores" in concerns:
            products.extend(self._recommend_pore_refining(budget))
        
        return products

    def _recommend_cleanser(self, skin_type: str, budget: str) -> List[ProductRecommendation]:
        """Recommend cleansers based on skin type."""
        if budget in ["drugstore", "mixed"]:
            if skin_type in ["oily", "combination"]:
                return [ProductRecommendation(
                    category="cleanser",
                    product_name="Foaming Facial Cleanser",
                    brand="CeraVe",
                    price_tier="drugstore",
                    price_usd=14.99,
                    key_ingredients=["ceramides", "hyaluronic acid", "niacinamide"],
                    benefits=["removes excess oil", "maintains skin barrier", "non-stripping"],
                    usage="both",
                    amazon_search_term="CeraVe Foaming Facial Cleanser",
                    notes="Gentle yet effective for oily/combination skin",
                )]
            else:
                return [ProductRecommendation(
                    category="cleanser",
                    product_name="Hydrating Facial Cleanser",
                    brand="CeraVe",
                    price_tier="drugstore",
                    price_usd=14.99,
                    key_ingredients=["ceramides", "hyaluronic acid"],
                    benefits=["hydrates while cleansing", "non-foaming", "gentle"],
                    usage="both",
                    amazon_search_term="CeraVe Hydrating Facial Cleanser",
                    notes="Perfect for dry and sensitive skin",
                )]
        
        # Add more budget tiers as needed
        return []

    def _recommend_moisturizer(self, skin_type: str, budget: str) -> List[ProductRecommendation]:
        """Recommend moisturizers based on skin type."""
        if budget in ["drugstore", "mixed"]:
            if skin_type in ["oily", "combination"]:
                return [ProductRecommendation(
                    category="moisturizer",
                    product_name="Ultra Facial Oil-Free Gel Cream",
                    brand="Kiehl's",
                    price_tier="mid_range",
                    price_usd=32.00,
                    key_ingredients=["glacial glycoprotein", "desert plant extract"],
                    benefits=["lightweight hydration", "oil-free", "non-comedogenic"],
                    usage="both",
                    amazon_search_term="Kiehls Ultra Facial Oil Free Gel Cream",
                    notes="Hydrates without adding shine",
                )]
            else:
                return [ProductRecommendation(
                    category="moisturizer",
                    product_name="Moisturizing Cream",
                    brand="CeraVe",
                    price_tier="drugstore",
                    price_usd=18.99,
                    key_ingredients=["ceramides", "hyaluronic acid", "petrolatum"],
                    benefits=["intense hydration", "restores skin barrier", "long-lasting"],
                    usage="both",
                    amazon_search_term="CeraVe Moisturizing Cream",
                    notes="Rich, non-greasy formula for dry skin",
                )]
        
        return []

    def _recommend_sunscreen(self, budget: str) -> List[ProductRecommendation]:
        """Recommend sunscreen (essential for everyone)."""
        if budget in ["drugstore", "mixed"]:
            return [ProductRecommendation(
                category="sunscreen",
                product_name="UV Clear Broad-Spectrum SPF 46",
                brand="EltaMD",
                price_tier="mid_range",
                price_usd=39.00,
                key_ingredients=["zinc oxide", "niacinamide", "hyaluronic acid"],
                benefits=["broad-spectrum protection", "oil-free", "calms redness"],
                usage="morning",
                amazon_search_term="EltaMD UV Clear SPF 46",
                notes="Ideal for acne-prone and sensitive skin",
            )]
        
        return []

    def _recommend_acne_treatment(self, concerns: List[str], budget: str) -> List[ProductRecommendation]:
        """Recommend acne treatments."""
        products = []
        
        if budget in ["drugstore", "mixed"]:
            products.append(ProductRecommendation(
                category="treatment",
                product_name="Salicylic Acid 2% Solution",
                brand="The Ordinary",
                price_tier="drugstore",
                price_usd=5.80,
                key_ingredients=["salicylic acid 2%"],
                benefits=["exfoliates inside pores", "reduces blackheads", "prevents breakouts"],
                usage="evening",
                amazon_search_term="The Ordinary Salicylic Acid 2%",
                notes="Start 2-3x per week, increase as tolerated",
            ))
        
        return products

    def _recommend_brightening(self, budget: str) -> List[ProductRecommendation]:
        """Recommend products for hyperpigmentation."""
        if budget in ["drugstore", "mid_range", "mixed"]:
            return [ProductRecommendation(
                category="treatment",
                product_name="Vitamin C Suspension 23% + HA Spheres 2%",
                brand="The Ordinary",
                price_tier="drugstore",
                price_usd=5.80,
                key_ingredients=["vitamin C 23%", "hyaluronic acid"],
                benefits=["brightens dark spots", "evens skin tone", "antioxidant protection"],
                usage="evening",
                amazon_search_term="The Ordinary Vitamin C 23%",
                notes="May tingle; use PM only",
            )]
        
        return []

    def _recommend_anti_aging(self, budget: str) -> List[ProductRecommendation]:
        """Recommend anti-aging products."""
        if budget in ["drugstore", "mid_range", "mixed"]:
            return [ProductRecommendation(
                category="treatment",
                product_name="Retinol 0.5% in Squalane",
                brand="The Ordinary",
                price_tier="drugstore",
                price_usd=5.80,
                key_ingredients=["retinol 0.5%", "squalane"],
                benefits=["reduces fine lines", "improves texture", "boosts collagen"],
                usage="evening",
                amazon_search_term="The Ordinary Retinol 0.5%",
                notes="Start 2x per week, use sunscreen daily",
            )]
        
        return []

    def _recommend_calming(self, budget: str) -> List[ProductRecommendation]:
        """Recommend calming products for redness/rosacea."""
        if budget in ["mid_range", "mixed"]:
            return [ProductRecommendation(
                category="treatment",
                product_name="Cicaplast Baume B5",
                brand="La Roche-Posay",
                price_tier="mid_range",
                price_usd=15.99,
                key_ingredients=["panthenol", "madecassoside", "copper-zinc-manganese"],
                benefits=["soothes irritation", "repairs skin barrier", "reduces redness"],
                usage="both",
                amazon_search_term="La Roche Posay Cicaplast Baume B5",
                notes="Use as needed on irritated areas",
            )]
        
        return []

    def _recommend_hydrating(self, budget: str) -> List[ProductRecommendation]:
        """Recommend hydrating products for dryness."""
        if budget in ["drugstore", "mixed"]:
            return [ProductRecommendation(
                category="serum",
                product_name="Hyaluronic Acid 2% + B5",
                brand="The Ordinary",
                price_tier="drugstore",
                price_usd=6.80,
                key_ingredients=["hyaluronic acid", "vitamin B5"],
                benefits=["intense hydration", "plumps skin", "improves moisture retention"],
                usage="both",
                amazon_search_term="The Ordinary Hyaluronic Acid 2%",
                notes="Apply to damp skin, follow with moisturizer",
            )]
        
        return []

    def _recommend_pore_refining(self, budget: str) -> List[ProductRecommendation]:
        """Recommend products for enlarged pores."""
        if budget in ["drugstore", "mixed"]:
            return [ProductRecommendation(
                category="treatment",
                product_name="Niacinamide 10% + Zinc 1%",
                brand="The Ordinary",
                price_tier="drugstore",
                price_usd=5.90,
                key_ingredients=["niacinamide 10%", "zinc 1%"],
                benefits=["minimizes pores", "regulates oil", "brightens"],
                usage="both",
                amazon_search_term="The Ordinary Niacinamide 10% Zinc 1%",
                notes="Can be used AM and PM",
            )]
        
        return []

    def _recommend_procedures(self, concerns: List[str]) -> List[ProcedureRecommendation]:
        """Recommend cosmetic/dermatological procedures."""
        procedures = []
        
        if "acne" in concerns or any("acne_" in c for c in concerns):
            procedures.append(ProcedureRecommendation(
                procedure_name="Chemical Peel (Salicylic Acid)",
                procedure_type="in_office",
                description="Professional-strength salicylic acid peel to deeply exfoliate and clear pores",
                benefits=["reduces active acne", "unclogs pores", "improves texture"],
                typical_cost_range="$100-$300 per session",
                frequency="Every 4-6 weeks",
                downtime="1-3 days of mild peeling",
                requires_professional=True,
                notes="Series of 3-6 treatments recommended",
            ))
        
        if "hyperpigmentation" in concerns:
            procedures.append(ProcedureRecommendation(
                procedure_name="Laser Treatment (IPL or Fraxel)",
                procedure_type="in_office",
                description="Laser therapy to target and break up pigmentation",
                benefits=["fades dark spots", "evens skin tone", "long-lasting results"],
                typical_cost_range="$300-$1,500 per session",
                frequency="3-5 sessions, 4 weeks apart",
                downtime="3-7 days of redness and peeling",
                requires_professional=True,
                notes="Requires strict sun protection",
            ))
        
        if "aging" in concerns or "fine_lines" in concerns:
            procedures.append(ProcedureRecommendation(
                procedure_name="Microneedling with PRP",
                procedure_type="in_office",
                description="Collagen-induction therapy with platelet-rich plasma",
                benefits=["reduces fine lines", "improves texture", "boosts collagen"],
                typical_cost_range="$300-$700 per session",
                frequency="3-6 sessions, 4-6 weeks apart",
                downtime="2-3 days of redness",
                requires_professional=True,
                notes="Results improve over 3-6 months",
            ))
        
        if "wrinkles" in concerns or "aging" in concerns:
            procedures.append(ProcedureRecommendation(
                procedure_name="Botox (Botulinum Toxin)",
                procedure_type="in_office",
                description="Injectable neurotoxin to relax facial muscles and smooth wrinkles",
                benefits=["reduces forehead lines", "softens crow's feet", "prevents new wrinkles"],
                typical_cost_range="$300-$600 per area",
                frequency="Every 3-4 months",
                downtime="None (may have minor bruising)",
                requires_professional=True,
                notes="Results last 3-4 months",
            ))
        
        return procedures

    def _build_routine(self, routine_type: Literal["morning", "evening"], products: List[ProductRecommendation]) -> SkincareRoutine:
        """Build a step-by-step skincare routine."""
        routine_products = [p for p in products if p.usage in [routine_type, "both"]]
        
        # Order by category
        category_order = ["cleanser", "toner", "serum", "treatment", "moisturizer", "sunscreen", "spot_treatment"]
        sorted_products = sorted(routine_products, key=lambda p: category_order.index(p.category) if p.category in category_order else 99)
        
        steps = []
        for i, product in enumerate(sorted_products, 1):
            steps.append({
                "step": f"{i}. {product.category.title()}",
                "product": f"{product.brand} {product.product_name}",
                "usage": product.usage,
            })
        
        return SkincareRoutine(routine_type=routine_type, steps=steps)

    def _generate_ingredient_guidance(self, concerns: List[str]) -> Dict[str, List[str]]:
        """Generate ingredient guidance (what to look for and avoid)."""
        to_look_for = []
        to_avoid = []
        
        if "acne" in concerns or any("acne_" in c for c in concerns):
            to_look_for.extend(["salicylic acid", "benzoyl peroxide", "niacinamide", "retinoids"])
            to_avoid.extend(["coconut oil", "heavy oils", "comedogenic ingredients"])
        
        if "hyperpigmentation" in concerns:
            to_look_for.extend(["vitamin C", "niacinamide", "alpha arbutin", "kojic acid", "tranexamic acid"])
        
        if "aging" in concerns or "fine_lines" in concerns:
            to_look_for.extend(["retinol", "peptides", "vitamin C", "hyaluronic acid", "ceramides"])
        
        if "redness" in concerns or "rosacea" in concerns:
            to_look_for.extend(["centella asiatica", "niacinamide", "azelaic acid", "green tea extract"])
            to_avoid.extend(["fragrance", "alcohol", "harsh exfoliants", "hot water"])
        
        if "dryness" in concerns:
            to_look_for.extend(["hyaluronic acid", "ceramides", "glycerin", "squalane", "urea"])
            to_avoid.extend(["alcohol", "harsh sulfates", "over-exfoliation"])
        
        return {
            "to_look_for": list(set(to_look_for)),
            "to_avoid": list(set(to_avoid)),
        }

    def _generate_lifestyle_tips(self, skin_type: str, concerns: List[str]) -> List[str]:
        """Generate lifestyle tips based on skin type and concerns."""
        tips = [
            "Drink at least 8 glasses of water daily",
            "Get 7-9 hours of sleep per night",
            "Change pillowcases weekly",
            "Avoid touching your face throughout the day",
        ]
        
        if "acne" in concerns:
            tips.extend([
                "Cleanse face after sweating",
                "Avoid picking or squeezing blemishes",
                "Use non-comedogenic makeup and skincare",
            ])
        
        if "aging" in concerns or "hyperpigmentation" in concerns:
            tips.extend([
                "Wear broad-spectrum SPF 50+ daily, even indoors",
                "Reapply sunscreen every 2 hours when outdoors",
                "Wear a wide-brimmed hat in direct sun",
            ])
        
        if skin_type in ["dry", "sensitive"]:
            tips.extend([
                "Use a humidifier in dry environments",
                "Avoid hot showers (use lukewarm water)",
                "Pat skin dry instead of rubbing",
            ])
        
        return tips


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Project Face: Recommendations Engine — Demo")
    print("=" * 50)
    print("\nThis module generates skincare recommendations based on analysis results.")
    print("For full functionality, integrate with the analysis engine and FastAPI backend.")
