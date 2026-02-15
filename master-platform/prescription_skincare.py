"""
Master Platform: Prescription Skincare Awareness Database
==========================================================
Educates users about prescription-strength skincare options most people don't
know their doctor can prescribe. Empowers users to advocate for themselves.

Author: Audrey Evans

DISCLAIMER: This module is for informational purposes only. It is NOT a
substitute for professional medical advice. Always consult a dermatologist
or healthcare provider before starting any prescription medication.
"""

import json
from pathlib import Path
from typing import List, Dict, Optional, Any, Literal
from dataclasses import dataclass, field, asdict

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DATA_DIR = Path(__file__).parent / "data" / "prescription_skincare"

MEDICAL_DISCLAIMER = (
    "DISCLAIMER: This information is for educational purposes only. It is NOT a "
    "substitute for professional medical advice, diagnosis, or treatment. Always "
    "consult your dermatologist or healthcare provider before starting, stopping, "
    "or changing any medication. Product recommendations may include affiliate links."
)


# ---------------------------------------------------------------------------
# Prescription Skincare Database
# ---------------------------------------------------------------------------

PRESCRIPTION_DATABASE = {
    "tretinoin": {
        "generic_name": "Tretinoin",
        "brand_names": ["Retin-A", "Retin-A Micro", "Atralin", "Avita", "Altreno"],
        "drug_class": "Retinoid (Vitamin A derivative)",
        "what_it_treats": [
            "Acne (all types)",
            "Fine lines and wrinkles",
            "Hyperpigmentation / dark spots",
            "Sun damage",
            "Rough skin texture",
            "Enlarged pores (appearance)",
        ],
        "how_it_works": (
            "Increases skin cell turnover, stimulates collagen production, and "
            "unclogs pores. Prescription tretinoin is 10-20x more potent than "
            "over-the-counter retinol. It's the GOLD STANDARD for anti-aging."
        ),
        "strengths": ["0.025%", "0.05%", "0.1%"],
        "how_to_ask_doctor": (
            "Tell your doctor: 'I'm interested in tretinoin for [acne/anti-aging/texture]. "
            "I've tried OTC retinol but want something more effective. Can you prescribe it?' "
            "Most dermatologists will prescribe it readily. Even primary care doctors can prescribe it."
        ),
        "cost": {
            "with_insurance": "$10-$75 copay (often covered for acne)",
            "without_insurance": "$30-$150 (generic tretinoin cream)",
            "generic_available": True,
            "goodrx_price": "$15-$45 with GoodRx coupon",
            "prior_auth_needed": "Sometimes for anti-aging (easier for acne diagnosis)",
        },
        "otc_alternative": "Adapalene (Differin) 0.1% — available OTC at $13, but less potent",
        "pharmacist_tip": "Ask your pharmacist about generic tretinoin — much cheaper than brand Retin-A",
        "side_effects": ["Peeling", "Redness", "Dryness", "Sun sensitivity", "Initial purging (2-6 weeks)"],
        "tips": [
            "Start with 0.025% strength, use 2-3x/week, build up slowly",
            "Apply PEA-SIZED amount to dry skin at night",
            "ALWAYS use SPF 50 during the day — tretinoin makes skin sun-sensitive",
            "Expect 'purging' (temporary breakouts) for 2-6 weeks — this is normal",
            "Results visible in 3-6 months — be patient",
            "Can be used long-term (decades) safely",
        ],
        "did_you_know": "Tretinoin was originally developed for acne in the 1960s. Doctors noticed patients' skin looked younger — and the anti-aging revolution began.",
    },
    "urea_20": {
        "generic_name": "Urea 20-40% Cream",
        "brand_names": ["Carmol 20", "Carmol 40", "Keralac", "Uramaxin", "Umecta"],
        "drug_class": "Keratolytic / Humectant",
        "what_it_treats": [
            "Extreme dryness / xerosis",
            "Keratosis pilaris (chicken skin bumps on arms)",
            "Cracked heels and feet",
            "Eczema-related dryness",
            "Psoriasis scaling",
            "Calluses and rough patches",
        ],
        "how_it_works": (
            "Urea at high concentrations (20-40%) breaks down the protein bonds in dead skin, "
            "dissolving flakes and rough patches while simultaneously drawing moisture into the skin. "
            "It's both an exfoliant AND a moisturizer. At lower concentrations (5-10%), it's just "
            "a moisturizer. Prescription strength (20-40%) is dramatically more effective than OTC."
        ),
        "strengths": ["20%", "40%"],
        "how_to_ask_doctor": (
            "Tell your doctor: 'I have extremely dry skin / keratosis pilaris / cracked heels "
            "that OTC moisturizers aren't helping. Can you prescribe urea 20% or 40% cream?' "
            "This is an easy prescription — most doctors will write it without hesitation."
        ),
        "cost": {
            "with_insurance": "$10-$30 copay",
            "without_insurance": "$20-$60 (generic)",
            "generic_available": True,
            "goodrx_price": "$15-$35 with GoodRx coupon",
            "prior_auth_needed": "Rarely",
        },
        "otc_alternative": "Urea 10% creams (Eucerin, CeraVe SA) — available OTC but less effective",
        "pharmacist_tip": "Ask your pharmacist: 'Do you carry urea 20% cream?' Some pharmacies stock it OTC in the foot care section.",
        "side_effects": ["Mild stinging on broken skin", "Temporary redness"],
        "tips": [
            "Apply to damp skin for best absorption",
            "For KP: apply to arms and legs after shower",
            "For feet: apply at night, cover with socks",
            "Can be used daily long-term",
            "Avoid applying to open wounds or cracked/bleeding skin",
        ],
        "did_you_know": "Urea is naturally produced by your body and found in healthy skin. Prescription-strength urea just replenishes what dry environments strip away.",
    },
    "hydroquinone": {
        "generic_name": "Hydroquinone",
        "brand_names": ["Tri-Luma (combination)", "Obagi Clear", "Lustra", "Melquin"],
        "drug_class": "Skin-lightening agent / Tyrosinase inhibitor",
        "what_it_treats": [
            "Hyperpigmentation / dark spots",
            "Melasma",
            "Post-inflammatory hyperpigmentation (PIH)",
            "Sun spots / age spots",
            "Uneven skin tone",
        ],
        "how_it_works": (
            "Inhibits tyrosinase, the enzyme that produces melanin. Prescription strength (4%) "
            "is twice as strong as OTC (2%). Tri-Luma combines hydroquinone + tretinoin + "
            "fluocinolone for maximum effectiveness against melasma."
        ),
        "strengths": ["4% (prescription)", "2% (OTC — being phased out in some states)"],
        "how_to_ask_doctor": (
            "Tell your doctor: 'I have dark spots / melasma / uneven skin tone that OTC products "
            "haven't improved. Can you prescribe hydroquinone 4% or Tri-Luma?' "
            "Dermatologists prescribe this routinely."
        ),
        "cost": {
            "with_insurance": "$15-$50 copay",
            "without_insurance": "$30-$100 (generic 4%); Tri-Luma $200+ without insurance",
            "generic_available": True,
            "goodrx_price": "$25-$60 with GoodRx coupon",
            "prior_auth_needed": "Sometimes for Tri-Luma",
        },
        "otc_alternative": "Alpha arbutin, vitamin C, azelaic acid, kojic acid — slower but no prescription needed",
        "pharmacist_tip": "OTC hydroquinone 2% is being restricted in some states. Ask your pharmacist about availability or get the prescription 4%.",
        "side_effects": ["Dryness", "Redness", "Stinging", "Ochronosis (rare, from overuse)"],
        "tips": [
            "Use for 3-6 months max, then take a break",
            "ALWAYS use SPF 50 — sun exposure reverses all progress",
            "Apply only to dark spots, not entire face",
            "Combine with tretinoin for best results",
            "Results visible in 4-8 weeks",
        ],
        "did_you_know": "Hydroquinone has been used safely for over 50 years. The key is using it correctly: limited duration, with sunscreen, and under doctor supervision.",
    },
    "azelaic_acid_rx": {
        "generic_name": "Azelaic Acid (prescription strength)",
        "brand_names": ["Finacea (15% gel)", "Azelex (20% cream)"],
        "drug_class": "Dicarboxylic acid",
        "what_it_treats": [
            "Rosacea (FDA-approved)",
            "Acne",
            "Hyperpigmentation",
            "Post-inflammatory marks",
            "Melasma (off-label)",
        ],
        "how_it_works": (
            "Anti-inflammatory, antibacterial, and melanin-inhibiting. One of the few "
            "treatments that addresses redness, bumps, AND dark spots simultaneously. "
            "Prescription 15-20% is significantly more effective than OTC 10%."
        ),
        "strengths": ["15% (Finacea gel)", "20% (Azelex cream)"],
        "how_to_ask_doctor": (
            "Tell your doctor: 'I have rosacea / acne with dark marks. I've read that "
            "azelaic acid can help both. Can you prescribe Finacea or Azelex?' "
            "Very commonly prescribed — doctors know it well."
        ),
        "cost": {
            "with_insurance": "$15-$50 copay",
            "without_insurance": "$50-$200",
            "generic_available": True,
            "goodrx_price": "$30-$80 with GoodRx coupon",
            "prior_auth_needed": "Rarely",
        },
        "otc_alternative": "The Ordinary Azelaic Acid 10% ($8) — less potent but a good starting point",
        "pharmacist_tip": "Generic azelaic acid 15% gel is much cheaper than brand Finacea. Ask your pharmacist.",
        "side_effects": ["Mild stinging/burning initially", "Dryness", "Peeling"],
        "tips": [
            "Safe during pregnancy (unlike tretinoin)",
            "Can be used morning AND night",
            "Layer under moisturizer",
            "Takes 4-12 weeks for visible results",
            "Safe for long-term use",
        ],
        "did_you_know": "Azelaic acid is naturally produced by yeast on your skin. It's one of the safest prescription skincare ingredients — even safe during pregnancy.",
    },
    "metronidazole": {
        "generic_name": "Metronidazole (topical)",
        "brand_names": ["MetroGel", "MetroCream", "MetroLotion", "Noritate"],
        "drug_class": "Antibiotic / Anti-inflammatory",
        "what_it_treats": [
            "Rosacea (FDA-approved)",
            "Rosacea-related redness and bumps",
            "Perioral dermatitis",
        ],
        "how_it_works": (
            "Reduces inflammation and kills bacteria associated with rosacea. "
            "One of the first-line treatments for rosacea."
        ),
        "strengths": ["0.75%", "1%"],
        "how_to_ask_doctor": (
            "Tell your doctor: 'I have persistent facial redness and bumps that I think "
            "might be rosacea. Can you prescribe metronidazole gel?' "
            "This is a standard first-line rosacea treatment."
        ),
        "cost": {
            "with_insurance": "$10-$40 copay",
            "without_insurance": "$20-$80 (generic)",
            "generic_available": True,
            "goodrx_price": "$15-$40 with GoodRx coupon",
            "prior_auth_needed": "Rarely",
        },
        "otc_alternative": "No direct OTC equivalent. Azelaic acid 10% (The Ordinary) may help mild rosacea.",
        "pharmacist_tip": "Generic metronidazole gel is very affordable. Ask for the generic.",
        "side_effects": ["Mild dryness", "Stinging", "Metallic taste (rare with topical)"],
        "tips": [
            "Apply thin layer to affected areas 1-2x daily",
            "Can take 3-9 weeks to see improvement",
            "Avoid alcohol-based products on rosacea skin",
            "Can be combined with azelaic acid for better results",
        ],
        "did_you_know": "Rosacea affects 16 million Americans, but most don't seek treatment because they think it's just 'sensitive skin.' A simple prescription can dramatically improve it.",
    },
    "tacrolimus": {
        "generic_name": "Tacrolimus (topical)",
        "brand_names": ["Protopic"],
        "drug_class": "Calcineurin inhibitor / Immunomodulator",
        "what_it_treats": [
            "Eczema / atopic dermatitis (moderate to severe)",
            "Facial eczema (where steroids are risky)",
            "Eyelid eczema",
            "Perioral dermatitis",
        ],
        "how_it_works": (
            "Suppresses the immune response that causes eczema inflammation WITHOUT "
            "the skin-thinning side effects of steroids. Especially important for "
            "delicate areas like face and eyelids where steroids are dangerous."
        ),
        "strengths": ["0.03%", "0.1%"],
        "how_to_ask_doctor": (
            "Tell your doctor: 'I have eczema on my face/eyelids and I'm worried about "
            "using steroids there long-term. Can you prescribe tacrolimus (Protopic)?' "
            "Dermatologists prefer this over steroids for facial eczema."
        ),
        "cost": {
            "with_insurance": "$15-$75 copay",
            "without_insurance": "$100-$300",
            "generic_available": True,
            "goodrx_price": "$50-$120 with GoodRx coupon",
            "prior_auth_needed": "Often — insurance may require trying steroids first",
        },
        "otc_alternative": "Colloidal oatmeal creams (Aveeno), CeraVe Eczema Cream — for mild eczema only",
        "pharmacist_tip": "If insurance denies Protopic, ask about pimecrolimus (Elidel) — similar drug, sometimes easier to get approved.",
        "side_effects": ["Burning/stinging initially (improves after a few days)", "Warmth at application site"],
        "tips": [
            "Initial burning is NORMAL and goes away after 3-5 days",
            "Apply to damp skin after bathing",
            "Safe for long-term use on face (unlike steroids)",
            "Use sunscreen — may increase sun sensitivity",
            "Can be used as maintenance therapy to prevent flares",
        ],
        "did_you_know": "Many people suffer with facial eczema for years using only OTC creams. Tacrolimus can clear it up in weeks — and it's safe for the delicate face and eye area.",
    },
    "clobetasol": {
        "generic_name": "Clobetasol Propionate",
        "brand_names": ["Temovate", "Clobex", "Olux"],
        "drug_class": "Super-potent topical corticosteroid",
        "what_it_treats": [
            "Severe eczema / dermatitis",
            "Psoriasis (plaque type)",
            "Severe contact dermatitis",
            "Lichen planus",
            "Discoid lupus",
        ],
        "how_it_works": (
            "The most potent topical steroid available. Rapidly reduces inflammation, "
            "itching, and redness. Reserved for severe cases that don't respond to "
            "milder treatments."
        ),
        "strengths": ["0.05% (cream, ointment, foam, solution)"],
        "how_to_ask_doctor": (
            "Tell your doctor: 'My eczema/psoriasis is severe and OTC hydrocortisone "
            "isn't helping. Can you prescribe something stronger like clobetasol?' "
            "Doctors prescribe this for severe cases."
        ),
        "cost": {
            "with_insurance": "$10-$40 copay",
            "without_insurance": "$20-$60 (generic)",
            "generic_available": True,
            "goodrx_price": "$12-$30 with GoodRx coupon",
            "prior_auth_needed": "Rarely for generic",
        },
        "otc_alternative": "Hydrocortisone 1% (OTC) — much weaker but safe for mild cases",
        "pharmacist_tip": "Generic clobetasol is very affordable. Ask for generic cream or ointment.",
        "side_effects": ["Skin thinning (with overuse)", "Stretch marks", "Rebound flare if stopped abruptly"],
        "tips": [
            "Use for SHORT periods only (2 weeks max on most areas)",
            "NEVER use on face, groin, or armpits (too potent)",
            "Taper off gradually — don't stop suddenly",
            "Apply thin layer to affected areas only",
            "Follow up with moisturizer",
        ],
        "did_you_know": "Clobetasol is so potent that a small tube can clear a severe psoriasis flare in days. But it must be used carefully and briefly.",
    },
    "dapsone_gel": {
        "generic_name": "Dapsone (topical)",
        "brand_names": ["Aczone"],
        "drug_class": "Sulfone antibiotic / Anti-inflammatory",
        "what_it_treats": [
            "Acne (especially in adult women)",
            "Hormonal acne",
            "Inflammatory acne",
        ],
        "how_it_works": (
            "Anti-inflammatory and antibacterial. Particularly effective for adult "
            "female acne, which is often hormonal and inflammatory."
        ),
        "strengths": ["5%", "7.5%"],
        "how_to_ask_doctor": (
            "Tell your doctor: 'I'm an adult woman with acne that keeps coming back, "
            "especially around my chin and jawline. I've heard dapsone gel works well "
            "for hormonal acne. Can you prescribe it?'"
        ),
        "cost": {
            "with_insurance": "$25-$75 copay",
            "without_insurance": "$200-$500 (brand Aczone)",
            "generic_available": True,
            "goodrx_price": "$30-$80 with GoodRx coupon (generic)",
            "prior_auth_needed": "Sometimes",
        },
        "otc_alternative": "Benzoyl peroxide 2.5% + adapalene (Differin) — OTC combination",
        "pharmacist_tip": "Generic dapsone 7.5% is now available and much cheaper than brand Aczone.",
        "side_effects": ["Dryness", "Peeling", "Oiliness (paradoxically)"],
        "tips": [
            "Apply thin layer to entire face (not just spots)",
            "Can be used morning AND night",
            "Safe to use with other acne treatments",
            "Do NOT use with benzoyl peroxide — causes orange staining",
            "Results in 4-12 weeks",
        ],
        "did_you_know": "Adult female acne is incredibly common but undertreated. Many women think they should have 'outgrown' acne. Dapsone was specifically studied for this population.",
    },
    "ivermectin_cream": {
        "generic_name": "Ivermectin (topical)",
        "brand_names": ["Soolantra"],
        "drug_class": "Anti-parasitic / Anti-inflammatory",
        "what_it_treats": [
            "Rosacea (papulopustular type)",
            "Demodex mite-related skin issues",
            "Rosacea bumps and pustules",
        ],
        "how_it_works": (
            "Kills Demodex mites (microscopic mites that live in hair follicles and "
            "are found in higher numbers in rosacea patients) and reduces inflammation. "
            "Often more effective than metronidazole for rosacea bumps."
        ),
        "strengths": ["1% cream"],
        "how_to_ask_doctor": (
            "Tell your doctor: 'I have rosacea with bumps and pustules. I've read that "
            "ivermectin cream (Soolantra) is very effective. Can you prescribe it?'"
        ),
        "cost": {
            "with_insurance": "$25-$75 copay",
            "without_insurance": "$200-$400 (brand Soolantra)",
            "generic_available": True,
            "goodrx_price": "$40-$100 with GoodRx coupon (generic)",
            "prior_auth_needed": "Sometimes — may need to try metronidazole first",
        },
        "otc_alternative": "No direct OTC equivalent. Tea tree oil products may help mild Demodex issues.",
        "pharmacist_tip": "Generic ivermectin cream is now available. Ask for it — saves hundreds.",
        "side_effects": ["Mild burning initially", "Dryness", "Initial worsening (die-off reaction)"],
        "tips": [
            "Apply once daily to affected areas",
            "Initial worsening in first 2 weeks is normal (mite die-off)",
            "Full results in 8-12 weeks",
            "Can be combined with azelaic acid",
            "Long-term use is safe",
        ],
        "did_you_know": "Demodex mites live on everyone's face, but rosacea patients have 10-18x more. Ivermectin targets this root cause — not just the symptoms.",
    },
}

# "Hooded eyes" and other specific conditions with Rx options
CONDITION_RX_MAP = {
    "hooded_eyes": {
        "condition": "Hooded Eyes / Dermatochalasis",
        "description": "Excess skin on the upper eyelid that droops over the crease, making eyes look smaller or tired.",
        "prescription_options": [
            {
                "name": "Upneeq (oxymetazoline 0.1%)",
                "what_it_does": "Prescription eye drop that lifts the upper eyelid 1-2mm by stimulating the Mueller's muscle",
                "cost": "$75-$100/month (not usually covered by insurance)",
                "how_to_ask": "Tell your eye doctor: 'My droopy eyelids bother me. Can I try Upneeq drops?'",
                "duration": "Effects last 6-8 hours per drop",
                "note": "Not a permanent fix — works like 'makeup for your eyelid muscles'",
            },
        ],
        "non_rx_options": ["Eyelid tape", "Eye primer techniques", "Blepharoplasty (surgical)"],
        "did_you_know": "Most people with hooded eyes don't know there's a prescription eye drop that can temporarily lift their lids. It's like a non-surgical eye lift in a bottle.",
    },
    "dark_circles": {
        "condition": "Dark Under-Eye Circles (Periorbital Hyperpigmentation)",
        "description": "Dark discoloration under the eyes caused by genetics, thin skin, allergies, or aging.",
        "prescription_options": [
            {
                "name": "Hydroquinone 4% (for pigmentation-based circles)",
                "what_it_does": "Lightens melanin-based dark circles",
                "cost": "$25-$60 generic",
                "how_to_ask": "Tell your dermatologist: 'My dark circles are pigmentation-based. Can I use hydroquinone under my eyes?'",
                "duration": "4-8 weeks for results",
                "note": "Only works for pigmentation — not for vascular (blue/purple) circles",
            },
            {
                "name": "Tretinoin 0.025% (for thin-skin circles)",
                "what_it_does": "Thickens under-eye skin over time, reducing visibility of blood vessels",
                "cost": "$15-$45 generic",
                "how_to_ask": "Ask your dermatologist about using low-strength tretinoin under the eyes",
                "duration": "3-6 months for results",
                "note": "Must use very low strength and sparingly — under-eye skin is delicate",
            },
        ],
        "non_rx_options": ["Vitamin C serum", "Caffeine eye cream", "Dermal fillers (for hollow circles)", "Adequate sleep"],
        "did_you_know": "Dark circles have different causes requiring different treatments. Pigmentation (brown) needs lightening agents. Vascular (blue/purple) needs fillers or vitamin K. Hollow circles need volume.",
    },
}


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

@dataclass
class PrescriptionInfo:
    """Formatted prescription information for a user."""
    medication_name: str
    brand_names: List[str]
    what_it_treats: List[str]
    how_to_ask_doctor: str
    cost_summary: Dict[str, str]
    otc_alternative: str
    pharmacist_tip: str
    tips: List[str]
    did_you_know: str
    disclaimer: str = MEDICAL_DISCLAIMER

    def to_dict(self) -> dict:
        return asdict(self)


# ---------------------------------------------------------------------------
# Prescription Skincare Engine
# ---------------------------------------------------------------------------

class PrescriptionSkincareEngine:
    """
    Educates users about prescription skincare options.
    Empowers users to advocate for themselves with their doctors.
    """

    def __init__(self):
        self.data_dir = DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.database = PRESCRIPTION_DATABASE
        self.condition_map = CONDITION_RX_MAP

    def get_all_prescriptions(self) -> Dict[str, Any]:
        """Get the complete prescription database."""
        return self.database

    def get_prescription_info(self, medication_key: str) -> Optional[PrescriptionInfo]:
        """Get detailed info about a specific prescription medication."""
        med = self.database.get(medication_key)
        if not med:
            return None
        
        return PrescriptionInfo(
            medication_name=med["generic_name"],
            brand_names=med["brand_names"],
            what_it_treats=med["what_it_treats"],
            how_to_ask_doctor=med["how_to_ask_doctor"],
            cost_summary=med["cost"],
            otc_alternative=med["otc_alternative"],
            pharmacist_tip=med["pharmacist_tip"],
            tips=med["tips"],
            did_you_know=med["did_you_know"],
        )

    def find_rx_for_condition(self, condition: str) -> List[Dict[str, Any]]:
        """
        Find prescription options for a skin condition.
        
        Args:
            condition: Skin condition (acne, rosacea, eczema, etc.)
        
        Returns:
            List of matching prescription medications with details
        """
        condition_lower = condition.lower()
        matches = []
        
        for key, med in self.database.items():
            for treats in med["what_it_treats"]:
                if condition_lower in treats.lower():
                    matches.append({
                        "medication": med["generic_name"],
                        "brand_names": med["brand_names"],
                        "treats": treats,
                        "how_to_ask": med["how_to_ask_doctor"],
                        "cost": med["cost"],
                        "otc_alternative": med["otc_alternative"],
                        "key": key,
                    })
                    break
        
        return matches

    def find_rx_for_symptom(self, symptom: str) -> List[Dict[str, Any]]:
        """Find prescriptions based on symptoms."""
        symptom_condition_map = {
            "dry": ["extreme dryness", "eczema", "keratosis pilaris"],
            "oily": ["acne"],
            "red": ["rosacea"],
            "bumpy": ["acne", "rosacea", "keratosis pilaris"],
            "dark spots": ["hyperpigmentation", "melasma"],
            "wrinkles": ["fine lines", "anti-aging"],
            "flaky": ["psoriasis", "eczema", "extreme dryness"],
            "itchy": ["eczema", "dermatitis"],
            "burning": ["rosacea", "dermatitis"],
        }
        
        conditions = symptom_condition_map.get(symptom.lower(), [])
        all_matches = []
        
        for condition in conditions:
            matches = self.find_rx_for_condition(condition)
            all_matches.extend(matches)
        
        # Deduplicate
        seen = set()
        unique = []
        for match in all_matches:
            if match["medication"] not in seen:
                seen.add(match["medication"])
                unique.append(match)
        
        return unique

    def get_condition_rx_info(self, condition_key: str) -> Optional[Dict[str, Any]]:
        """Get Rx info for specific conditions like hooded eyes."""
        return self.condition_map.get(condition_key)

    def get_insurance_guide(self) -> Dict[str, Any]:
        """Get guide on insurance coverage for prescription skincare."""
        return {
            "title": "Insurance Coverage Guide for Prescription Skincare",
            "general_tips": [
                "Acne medications are MORE LIKELY to be covered than anti-aging",
                "Ask your doctor to code the prescription for a medical condition (acne, rosacea, eczema) rather than cosmetic",
                "Generic versions are almost always covered and much cheaper",
                "GoodRx coupons can beat insurance copays — always check both",
                "Prior authorization: if insurance denies, your doctor can appeal",
                "Mail-order pharmacies (Costco, Amazon Pharmacy) often have lowest prices",
            ],
            "commonly_covered": [
                "Tretinoin (for acne diagnosis)",
                "Metronidazole (for rosacea)",
                "Azelaic acid (for rosacea)",
                "Clobetasol (for eczema/psoriasis)",
                "Tacrolimus (for eczema — may need prior auth)",
            ],
            "often_denied": [
                "Tretinoin (when coded as anti-aging/cosmetic)",
                "Hydroquinone (often considered cosmetic)",
                "Upneeq (usually not covered)",
            ],
            "money_saving_tips": [
                "Always ask for generic",
                "Check GoodRx, RxSaver, and Amazon Pharmacy prices",
                "Costco pharmacy doesn't require membership for Rx",
                "Manufacturer coupons available for many brand-name drugs",
                "Some dermatology offices have samples — ask!",
                "Telehealth dermatology (Curology, Apostrophe) can be cheaper than office visits",
            ],
            "disclaimer": MEDICAL_DISCLAIMER,
        }

    def generate_did_you_know(self, category: Optional[str] = None) -> List[Dict[str, str]]:
        """Generate 'Did you know?' notifications about prescription skincare."""
        notifications = []
        
        for key, med in self.database.items():
            notifications.append({
                "medication": med["generic_name"],
                "fact": med["did_you_know"],
                "category": key,
            })
        
        for key, condition in self.condition_map.items():
            notifications.append({
                "medication": condition["condition"],
                "fact": condition["did_you_know"],
                "category": key,
            })
        
        if category:
            notifications = [n for n in notifications if n["category"] == category]
        
        return notifications


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Master Platform: Prescription Skincare Awareness — Demo")
    print("=" * 55)
    
    engine = PrescriptionSkincareEngine()
    
    # Find Rx for acne
    print("\nPrescription options for ACNE:")
    matches = engine.find_rx_for_condition("acne")
    for match in matches:
        print(f"  - {match['medication']} ({', '.join(match['brand_names'][:2])})")
        print(f"    Cost: {match['cost']['goodrx_price']}")
        print(f"    OTC alternative: {match['otc_alternative']}")
    
    # Hooded eyes
    print("\nPrescription options for HOODED EYES:")
    hooded = engine.get_condition_rx_info("hooded_eyes")
    if hooded:
        for rx in hooded["prescription_options"]:
            print(f"  - {rx['name']}: {rx['what_it_does']}")
            print(f"    Cost: {rx['cost']}")
            print(f"    How to ask: {rx['how_to_ask']}")
    
    # Did you know?
    print("\nDid You Know?")
    facts = engine.generate_did_you_know()
    for fact in facts[:3]:
        print(f"  - {fact['medication']}: {fact['fact']}")
    
    print(f"\n{MEDICAL_DISCLAIMER}")
