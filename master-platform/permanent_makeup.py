"""
Master Platform: Permanent Makeup & Areola Tattooing
=====================================================
Microblading, permanent eyeliner, lip color, scalp micropigmentation,
and 3D areola tattooing for breast cancer survivors.

This module is dedicated to all breast cancer survivors.
Areola tattooing is deeply personal — it helps women feel whole again.

Author: Audrey Evans (mastectomy survivor)

DISCLAIMER: This module is for informational purposes only. Always consult
qualified permanent makeup artists and verify credentials. Areola tattooing
should be done by specialized artists trained in 3D nipple/areola reconstruction.
"""

import json
from pathlib import Path
from typing import List, Dict, Optional, Any, Literal
from dataclasses import dataclass, field, asdict

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DATA_DIR = Path(__file__).parent / "data" / "permanent_makeup"

MEDICAL_DISCLAIMER = (
    "DISCLAIMER: Permanent makeup and tattooing involve risks. Always verify artist "
    "credentials, licensing, and portfolio. For areola tattooing, seek artists "
    "specialized in 3D nipple/areola reconstruction. This information is for research "
    "purposes only. Artist recommendations may include affiliate/referral links."
)

# ---------------------------------------------------------------------------
# Permanent Makeup Services
# ---------------------------------------------------------------------------

SERVICES = {
    "microblading": {
        "name": "Microblading Eyebrows",
        "description": "Hair-stroke technique using manual blade to create natural-looking eyebrows",
        "also_known_as": ["Eyebrow embroidery", "Feather brows", "3D brows"],
        "cost_range": {
            "initial_session": "$300-$800",
            "touch_up_6_weeks": "$100-$200",
            "annual_touch_up": "$150-$300",
        },
        "longevity": "12-18 months (fades over time, requires touch-ups)",
        "pain_level": "3-4/10 (numbing cream used)",
        "recovery_time": "7-14 days (scabbing, no makeup on brows)",
        "ideal_for": [
            "Sparse or over-plucked eyebrows",
            "Alopecia or hair loss",
            "Asymmetrical brows",
            "Anyone who wants to skip daily brow makeup",
        ],
        "not_recommended_for": [
            "Very oily skin (fades faster)",
            "Pregnant or breastfeeding",
            "Active skin conditions (eczema, psoriasis on brows)",
            "Keloid scarring tendency",
        ],
        "what_to_expect": {
            "day_1": "Brows look darker and bolder than final result",
            "days_3_7": "Scabbing and flaking (DO NOT PICK)",
            "week_2": "Color looks faded (this is normal — pigment returns)",
            "week_6": "Touch-up session to perfect shape and color",
            "month_3": "Final healed result",
        },
        "maintenance": "Touch-up every 12-18 months to maintain color",
        "risks": ["Infection (if aftercare not followed)", "Allergic reaction to pigment (rare)", "Uneven fading", "Color change over time"],
        "questions_to_ask_artist": [
            "Are you licensed and certified in microblading?",
            "Can I see your portfolio and before/after photos?",
            "What pigments do you use? (Should be hypoallergenic)",
            "What's your sanitation process?",
            "What's included in the price? (Initial + touch-up?)",
            "What if I don't like the result? (Removal options)",
        ],
    },
    "permanent_eyeliner": {
        "name": "Permanent Eyeliner",
        "description": "Tattooed eyeliner along the lash line for defined eyes without daily makeup",
        "styles": [
            "Lash enhancement (subtle, between lashes)",
            "Classic liner (thin line along lash line)",
            "Winged liner (cat-eye effect)",
        ],
        "cost_range": {
            "upper_lash_line": "$300-$600",
            "lower_lash_line": "$200-$400",
            "both": "$500-$900",
            "touch_up": "$100-$200",
        },
        "longevity": "2-5 years (fades over time)",
        "pain_level": "4-5/10 (eyes are sensitive, numbing drops used)",
        "recovery_time": "5-7 days (swelling, redness, no eye makeup)",
        "ideal_for": [
            "Anyone who wears eyeliner daily",
            "Allergies to traditional makeup",
            "Watery eyes that smudge makeup",
            "Hooded eyes (liner disappears in crease)",
            "Active lifestyle (swimming, gym)",
        ],
        "not_recommended_for": [
            "Active eye infections or styes",
            "Recent eye surgery (wait 6 months)",
            "Extremely sensitive eyes",
            "Pregnant or breastfeeding",
        ],
        "what_to_expect": {
            "day_1": "Swelling, redness, liner looks very dark",
            "days_2_3": "More swelling (ice packs help)",
            "days_4_7": "Swelling subsides, color starts to fade",
            "week_2": "Healed, color settles",
            "week_6": "Touch-up if needed",
        },
        "maintenance": "Touch-up every 2-5 years",
        "risks": ["Swelling (common, temporary)", "Infection (rare)", "Allergic reaction to pigment", "Asymmetry", "Migration of pigment (rare)"],
        "questions_to_ask_artist": [
            "How many eyeliner procedures have you done?",
            "Can I see photos of healed results (not fresh)?",
            "What numbing agents do you use?",
            "What if my eyes swell a lot? (Aftercare plan)",
            "Can I bring sunglasses? (Eyes will be sensitive)",
        ],
    },
    "permanent_lip_color": {
        "name": "Permanent Lip Color / Lip Blushing",
        "description": "Tattooed lip color for fuller, more defined lips without daily lipstick",
        "styles": [
            "Lip blushing (natural tint, enhances natural color)",
            "Full lip color (bold, defined color)",
            "Lip liner only (defines shape)",
        ],
        "cost_range": {
            "lip_blushing": "$400-$800",
            "full_lip_color": "$500-$1,000",
            "lip_liner_only": "$300-$600",
            "touch_up": "$150-$300",
        },
        "longevity": "2-5 years (fades over time, sun exposure fades faster)",
        "pain_level": "5-6/10 (lips are very sensitive, numbing used)",
        "recovery_time": "7-10 days (swelling, chapped lips, no kissing)",
        "ideal_for": [
            "Pale or uneven lip color",
            "Thin lips (creates illusion of fullness)",
            "Asymmetrical lips",
            "Anyone who wears lipstick daily",
        ],
        "not_recommended_for": [
            "Active cold sores (must take antiviral before procedure)",
            "Very dark lips (harder to lighten)",
            "Pregnant or breastfeeding",
            "Lip fillers (wait 4 weeks after fillers)",
        ],
        "what_to_expect": {
            "day_1": "Swelling, color looks VERY dark (don't panic)",
            "days_2_5": "More swelling, lips feel chapped and tight",
            "days_6_10": "Peeling (DO NOT PICK), color fades 40-50%",
            "week_2": "Color looks too light (this is normal)",
            "week_6": "Touch-up to add more color",
            "month_3": "Final healed result",
        },
        "maintenance": "Touch-up every 2-5 years, sunscreen on lips to prevent fading",
        "risks": ["Cold sore outbreak (take antiviral preventatively)", "Swelling (very common)", "Uneven color", "Allergic reaction to pigment"],
        "questions_to_ask_artist": [
            "Do I need to take antiviral medication before? (YES if you've ever had cold sores)",
            "Can I see healed results, not fresh? (Color changes dramatically)",
            "What pigments do you use? (Should be lip-safe, hypoallergenic)",
            "What if the color is too dark/light? (Touch-up included?)",
        ],
    },
    "scalp_micropigmentation": {
        "name": "Scalp Micropigmentation (SMP)",
        "description": "Tattooed dots on scalp to mimic hair follicles, creating illusion of fuller hair or shaved head",
        "ideal_for": [
            "Male pattern baldness",
            "Thinning hair (adds density)",
            "Alopecia",
            "Scar camouflage (hair transplant scars, injury scars)",
            "Women with thinning hair or wide part",
        ],
        "cost_range": {
            "full_scalp": "$1,500-$4,000 (3-4 sessions)",
            "hairline_only": "$500-$1,500",
            "scar_camouflage": "$200-$800",
            "touch_up": "$200-$500",
        },
        "longevity": "4-6 years (fades over time, touch-ups needed)",
        "pain_level": "2-4/10 (scalp is less sensitive than face)",
        "recovery_time": "3-5 days (redness, no sweating or sun)",
        "sessions_needed": "3-4 sessions (spaced 7-14 days apart)",
        "what_to_expect": {
            "session_1": "Hairline and coverage pattern created",
            "session_2": "Density added",
            "session_3": "Final density and blending",
            "week_2": "Healed, looks natural",
        },
        "maintenance": "Touch-up every 4-6 years",
        "risks": ["Unnatural look if done poorly", "Fading to blue/green (use quality pigments)", "Infection (rare)"],
        "questions_to_ask_artist": [
            "Can I see before/after photos of clients with my hair color/skin tone?",
            "What pigments do you use? (Should match your hair color)",
            "How many sessions will I need?",
            "What's your experience with scar camouflage? (If applicable)",
        ],
    },
    "areola_tattooing": {
        "name": "3D Areola Tattooing (Nipple/Areola Reconstruction)",
        "description": (
            "Specialized tattooing to recreate the appearance of a nipple and areola "
            "after mastectomy or breast reconstruction. This is the FINAL step in the "
            "journey to feeling whole again. Many artists offer this service for FREE "
            "or at reduced cost to breast cancer survivors."
        ),
        "emotional_significance": (
            "For many breast cancer survivors, areola tattooing is the moment they "
            "feel like themselves again. It's not 'just' a tattoo — it's reclaiming "
            "your body after trauma. This procedure is deeply personal and can be "
            "profoundly healing."
        ),
        "ideal_for": [
            "Post-mastectomy (with or without reconstruction)",
            "Post-lumpectomy with significant scarring",
            "Congenital absence of nipple/areola",
            "Nipple/areola discoloration or asymmetry",
        ],
        "cost_range": {
            "both_breasts": "$0-$800 (many artists offer FREE or reduced cost to survivors)",
            "one_breast": "$0-$400",
            "insurance_coverage": "Often covered as reconstructive (check with insurance)",
            "note": "MANY artists do this for free or at cost for cancer survivors",
        },
        "longevity": "3-5 years (fades over time, touch-ups available)",
        "pain_level": "1-3/10 (reconstructed tissue has less sensation)",
        "recovery_time": "7-10 days (minimal, no bra for a few days)",
        "sessions_needed": "1-2 sessions (initial + touch-up if needed)",
        "what_to_expect": {
            "consultation": "Artist will match color to your natural areola (if you have one) or choose a natural shade",
            "procedure": "3D technique creates realistic texture and dimension",
            "day_1": "Color looks dark, some redness",
            "week_1": "Color fades 30-40% (this is normal)",
            "week_6": "Touch-up if needed to adjust color or shape",
            "month_3": "Final healed result",
        },
        "insurance_coverage": [
            "Many insurance plans cover areola tattooing as part of breast reconstruction",
            "Considered 'reconstructive' not 'cosmetic'",
            "Check with your insurance — may need pre-authorization",
            "If denied, appeal — this is medically necessary for psychological healing",
        ],
        "finding_an_artist": [
            "Look for artists who specialize in medical tattooing or paramedical tattooing",
            "Ask your plastic surgeon for referrals",
            "Check with local breast cancer support groups",
            "Many hospitals have in-house medical tattoo artists",
            "Some artists travel to clients' homes for this procedure",
        ],
        "questions_to_ask_artist": [
            "How many areola tattoos have you done?",
            "Can I see your portfolio? (Before/after photos)",
            "Do you offer reduced/free services to cancer survivors?",
            "Will you work with my insurance?",
            "Can you match my natural areola color? (If applicable)",
            "What if I don't have sensation in that area? (Common after mastectomy)",
        ],
        "support_resources": [
            "American Cancer Society: cancer.org",
            "Breastcancer.org: Support and resources",
            "P.ink (Personal Ink): Decorative tattoos over mastectomy scars",
            "Local breast cancer survivor groups",
        ],
        "audrey_note": (
            "I'm a mastectomy survivor. This feature is personal to me. Areola tattooing "
            "is the final step in feeling whole again after breast cancer. If this app "
            "helps even ONE woman find an artist who can help her feel like herself again, "
            "it's worth it. You are not alone. You are beautiful. You are a survivor."
        ),
    },
    "tattoo_removal": {
        "name": "Laser Tattoo Removal",
        "description": "Laser technology breaks down tattoo ink so the body can absorb and eliminate it",
        "laser_types": [
            "PicoSure (fastest, most effective, fewer sessions)",
            "Q-switched lasers (older technology, more sessions needed)",
            "Nd:YAG (best for darker skin tones)",
        ],
        "cost_range": {
            "per_session": "$100-$500 (depends on tattoo size)",
            "small_tattoo": "$200-$500 total (3-5 sessions)",
            "medium_tattoo": "$1,000-$3,000 total (6-10 sessions)",
            "large_tattoo": "$3,000-$10,000+ total (10-15+ sessions)",
            "note": "Pricing by size (per square inch) or flat rate per session",
        },
        "sessions_needed": "3-15+ sessions (depends on ink color, depth, age of tattoo)",
        "session_spacing": "6-8 weeks between sessions (body needs time to clear ink)",
        "pain_level": "6-8/10 (more painful than getting the tattoo)",
        "recovery_time": "1-2 weeks (blistering, scabbing, redness)",
        "easiest_to_remove": ["Black ink", "Dark blue", "Red"],
        "hardest_to_remove": ["Yellow", "Green", "Light blue", "White", "Fluorescent colors"],
        "factors_affecting_removal": [
            "Ink color (black easiest, pastels hardest)",
            "Tattoo age (older tattoos easier)",
            "Ink depth (professional tattoos deeper than stick-and-poke)",
            "Skin tone (darker skin = more risk of discoloration)",
            "Location on body (areas with good blood flow clear faster)",
            "Immune system health (body clears ink)",
        ],
        "what_to_expect": {
            "during_session": "Rubber band snapping sensation, numbing cream helps",
            "immediately_after": "Redness, swelling, possible blistering",
            "days_1_7": "Scabbing (DO NOT PICK), itching",
            "weeks_2_8": "Tattoo fades gradually as body clears ink",
            "after_multiple_sessions": "Tattoo becomes lighter and lighter",
        },
        "at_home_removal": {
            "warning": "At-home laser devices are MUCH less effective than professional lasers",
            "cost": "$200-$500 for at-home device",
            "effectiveness": "May lighten tattoos slightly, but won't fully remove",
            "risks": "Burns, scarring, uneven results",
            "verdict": "Not recommended — see a professional",
        },
        "business_opportunity": (
            "Audrey considered buying a laser for a tattoo removal business. "
            "Lasers cost $50,000-$150,000. High profit margin: $200-$500 per session, "
            "laser lasts 10+ years. Tattoo removal is a growing market — people want "
            "old tattoos gone for jobs, relationships, or just regret."
        ),
        "questions_to_ask_clinic": [
            "What type of laser do you use? (PicoSure is best)",
            "How many sessions will I need? (Estimate based on your tattoo)",
            "What's the total cost? (Per session or package deal?)",
            "What are the risks for my skin tone? (Darker skin = more risk)",
            "Can I see before/after photos of similar tattoos?",
            "What if I just want it lightened for a cover-up? (Fewer sessions needed)",
        ],
    },
}


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

@dataclass
class PermanentMakeupService:
    """Formatted permanent makeup service information."""
    name: str
    description: str
    cost_range: Dict[str, str]
    longevity: str
    pain_level: str
    recovery_time: str
    ideal_for: List[str]
    what_to_expect: Dict[str, str]
    questions_to_ask_artist: List[str]
    disclaimer: str = MEDICAL_DISCLAIMER

    def to_dict(self) -> dict:
        return asdict(self)


# ---------------------------------------------------------------------------
# Permanent Makeup Engine
# ---------------------------------------------------------------------------

class PermanentMakeupEngine:
    """
    Permanent makeup services including areola tattooing for breast cancer survivors.
    """

    def __init__(self):
        self.data_dir = DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.services = SERVICES

    def get_all_services(self) -> Dict[str, Any]:
        """Get all permanent makeup services."""
        return self.services

    def get_service_info(self, service_key: str) -> Optional[Dict[str, Any]]:
        """Get detailed info about a specific service."""
        return self.services.get(service_key)

    def get_areola_tattooing_info(self) -> Dict[str, Any]:
        """Get comprehensive info about areola tattooing for breast cancer survivors."""
        areola = self.services.get("areola_tattooing")
        if not areola:
            return {}
        
        return {
            **areola,
            "survivor_support": {
                "message": (
                    "You are not alone. Millions of women have walked this path. "
                    "Areola tattooing is the final step in reclaiming your body. "
                    "Many artists offer this service for FREE or reduced cost to survivors. "
                    "Your insurance may cover it. You deserve to feel whole again."
                ),
                "resources": areola["support_resources"],
                "audrey_note": areola["audrey_note"],
            },
            "disclaimer": MEDICAL_DISCLAIMER,
        }

    def find_services_by_goal(self, goal: str) -> List[Dict[str, Any]]:
        """Find services based on user's goal."""
        goal_lower = goal.lower()
        matches = []
        
        goal_map = {
            "eyebrows": ["microblading"],
            "eyes": ["permanent_eyeliner"],
            "lips": ["permanent_lip_color"],
            "hair loss": ["scalp_micropigmentation"],
            "baldness": ["scalp_micropigmentation"],
            "breast cancer": ["areola_tattooing"],
            "mastectomy": ["areola_tattooing"],
            "tattoo removal": ["tattoo_removal"],
            "remove tattoo": ["tattoo_removal"],
        }
        
        for keyword, service_keys in goal_map.items():
            if keyword in goal_lower:
                for key in service_keys:
                    service = self.services.get(key)
                    if service:
                        matches.append({
                            "service": service["name"],
                            "description": service["description"],
                            "cost_range": service["cost_range"],
                            "key": key,
                        })
        
        return matches

    def get_cost_estimate(self, service_key: str, detail: Optional[str] = None) -> Dict[str, Any]:
        """Get cost estimate for a service."""
        service = self.services.get(service_key)
        if not service:
            return {}
        
        return {
            "service": service["name"],
            "cost_range": service["cost_range"],
            "longevity": service.get("longevity", "Varies"),
            "maintenance": service.get("maintenance", "Varies"),
            "note": "Prices vary by location, artist experience, and complexity",
            "disclaimer": MEDICAL_DISCLAIMER,
        }

    def get_recovery_timeline(self, service_key: str) -> Dict[str, Any]:
        """Get detailed recovery timeline for a service."""
        service = self.services.get(service_key)
        if not service:
            return {}
        
        return {
            "service": service["name"],
            "recovery_time": service.get("recovery_time", "Varies"),
            "what_to_expect": service.get("what_to_expect", {}),
            "pain_level": service.get("pain_level", "Varies"),
            "aftercare_tips": self._get_aftercare_tips(service_key),
            "disclaimer": MEDICAL_DISCLAIMER,
        }

    def _get_aftercare_tips(self, service_key: str) -> List[str]:
        """Get aftercare tips for a service."""
        general_tips = [
            "Keep area clean and dry",
            "Apply aftercare ointment as directed",
            "No picking or scratching",
            "Avoid sun exposure",
            "No swimming or soaking",
            "Sleep on clean pillowcase",
        ]
        
        specific_tips = {
            "microblading": [
                "No makeup on brows for 10 days",
                "No sweating (gym, sauna) for 10 days",
                "Brows will look too dark at first — this is normal",
            ],
            "permanent_eyeliner": [
                "Ice packs for swelling",
                "No eye makeup for 7 days",
                "Wear sunglasses outdoors",
            ],
            "permanent_lip_color": [
                "Take antiviral if you've ever had cold sores",
                "No kissing for 7 days",
                "Drink through a straw",
                "Lips will peel — DO NOT PICK",
            ],
            "areola_tattooing": [
                "No bra for 3-5 days",
                "Minimal pain (reconstructed tissue has less sensation)",
                "Moisturize gently",
            ],
        }
        
        return general_tips + specific_tips.get(service_key, [])

    def get_breast_cancer_survivor_resources(self) -> Dict[str, Any]:
        """Get resources specifically for breast cancer survivors."""
        areola = self.services.get("areola_tattooing")
        if not areola:
            return {}
        
        return {
            "title": "Resources for Breast Cancer Survivors",
            "areola_tattooing": {
                "what_it_is": areola["description"],
                "emotional_significance": areola["emotional_significance"],
                "cost": areola["cost_range"],
                "insurance_coverage": areola["insurance_coverage"],
                "finding_an_artist": areola["finding_an_artist"],
            },
            "support_organizations": [
                {"name": "American Cancer Society", "website": "cancer.org", "services": "Support groups, resources, financial assistance"},
                {"name": "Breastcancer.org", "website": "breastcancer.org", "services": "Information, community forums, expert advice"},
                {"name": "P.ink (Personal Ink)", "website": "p-ink.org", "services": "Decorative mastectomy tattoos (alternative to reconstruction)"},
                {"name": "Living Beyond Breast Cancer", "website": "lbbc.org", "services": "Education, support, survivorship resources"},
            ],
            "audrey_message": areola["audrey_note"],
            "disclaimer": MEDICAL_DISCLAIMER,
        }


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Master Platform: Permanent Makeup & Areola Tattooing — Demo")
    print("=" * 60)
    
    engine = PermanentMakeupEngine()
    
    # Areola tattooing for breast cancer survivors
    print("\n3D Areola Tattooing for Breast Cancer Survivors:")
    areola_info = engine.get_areola_tattooing_info()
    print(f"  {areola_info['description']}")
    print(f"\n  Emotional significance:")
    print(f"  {areola_info['emotional_significance']}")
    print(f"\n  Cost: {areola_info['cost_range']['both_breasts']}")
    print(f"  Note: {areola_info['cost_range']['note']}")
    print(f"\n  Audrey's note:")
    print(f"  {areola_info['audrey_note']}")
    
    # Microblading
    print("\n\nMicroblading Eyebrows:")
    microblading = engine.get_service_info("microblading")
    print(f"  Cost: {microblading['cost_range']['initial_session']}")
    print(f"  Longevity: {microblading['longevity']}")
    print(f"  Pain level: {microblading['pain_level']}")
    
    # Tattoo removal business opportunity
    print("\n\nTattoo Removal Business Opportunity:")
    removal = engine.get_service_info("tattoo_removal")
    print(f"  {removal['business_opportunity']}")
    
    print(f"\n{MEDICAL_DISCLAIMER}")
