"""
Master Platform: Medical Tourism Engine
========================================
International cutting-edge procedures + vacation packages.
Turn medical trips into recovery vacations.
Track procedures available worldwide that aren't yet in the US.

Author: Audrey Evans

DISCLAIMER: This module is for informational purposes only. Always consult
qualified medical professionals. Verify credentials and accreditation of
international clinics. Travel at your own risk.
"""

import json
from pathlib import Path
from typing import List, Dict, Optional, Any, Literal
from dataclasses import dataclass, field, asdict

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DATA_DIR = Path(__file__).parent / "data" / "medical_tourism"

MEDICAL_DISCLAIMER = (
    "DISCLAIMER: Medical tourism involves risks. Always verify clinic credentials, "
    "surgeon qualifications, and accreditation (JCI, ISO). This information is for "
    "research purposes only. Consult your doctor before traveling for medical procedures. "
    "Product and clinic recommendations may include affiliate/referral links."
)

# ---------------------------------------------------------------------------
# International Medical Tourism Destinations
# ---------------------------------------------------------------------------

DESTINATIONS = {
    "tijuana_mexico": {
        "location": "Tijuana, Mexico",
        "country": "Mexico",
        "distance_from_us": "15 minutes from San Diego border",
        "why_go_here": [
            "50-80% cheaper than US prices for same quality",
            "Same-day procedures — drive across border, procedure, drive home",
            "Many surgeons US-trained and board-certified",
            "Marble offices nicer than most US clinics (Audrey verified)",
            "No wait times — book within days",
            "Medical tourism infrastructure — English-speaking staff",
        ],
        "specialties": [
            "Cosmetic surgery (facelifts, rhinoplasty, liposuction)",
            "Dental work (implants, veneers, full mouth reconstruction)",
            "Bariatric surgery (gastric sleeve, bypass)",
            "PDO threads and non-surgical facelifts",
            "NAD+ IV therapy and wellness treatments",
            "Botox and fillers (fraction of US cost)",
            "Stem cell treatments",
            "Hair transplants",
        ],
        "cost_comparison": {
            "pdo_threads_full_face": {"us": "$15,000", "tijuana": "$2,000-$3,500"},
            "dental_implant": {"us": "$3,000-$6,000", "tijuana": "$800-$1,500"},
            "rhinoplasty": {"us": "$8,000-$15,000", "tijuana": "$3,500-$5,500"},
            "gastric_sleeve": {"us": "$15,000-$25,000", "tijuana": "$4,500-$6,500"},
            "botox_per_unit": {"us": "$12-$20", "tijuana": "$5-$8"},
            "nad_iv_therapy": {"us": "$500-$1,000", "tijuana": "$150-$300"},
        },
        "top_clinics": [
            {
                "name": "Audrey's Recommended Surgeon (TJ)",
                "specialty": "Cosmetic surgery, PDO threads",
                "note": "Marble office, world-class quality, nicer than US clinics",
                "accreditation": "Board-certified, US-trained",
                "contact": "[Contact info to be added]",
            },
            {
                "name": "BioCare Hospital",
                "specialty": "Bariatric surgery, medical tourism hub",
                "accreditation": "JCI accredited",
            },
            {
                "name": "Advanced Health Medical Center",
                "specialty": "Dental, cosmetic, wellness",
                "accreditation": "ISO certified",
            },
        ],
        "recovery_hotels": [
            "Hotel Pueblo Amigo (walking distance to clinics)",
            "Grand Hotel Tijuana (luxury recovery suites)",
            "Airbnb near Zona Rio (affordable, close to clinics)",
        ],
        "travel_logistics": {
            "how_to_get_there": "Fly to San Diego, Uber/taxi to border, walk across, taxi to clinic",
            "border_crossing": "Pedestrian crossing at San Ysidro — bring passport",
            "transportation": "Clinics often provide shuttle service from border",
            "insurance": "Most US insurance doesn't cover — pay out of pocket (still cheaper)",
            "emergency_contact": "US Consulate Tijuana: +52-664-977-2000",
        },
        "vacation_package_example": {
            "name": "PDO Thread Lift + Recovery Getaway",
            "includes": [
                "Full-face PDO thread lift procedure",
                "3 nights at recovery hotel (private room)",
                "Airport/border pickup and dropoff",
                "Post-procedure follow-up visit",
                "Recovery kit (ice packs, medications, skincare)",
            ],
            "total_cost": "$2,500-$3,500",
            "us_equivalent_cost": "$15,000+",
            "savings": "$11,500+",
        },
        "what_to_bring": [
            "Passport (required for border crossing)",
            "Cash (USD accepted, pesos preferred)",
            "Comfortable clothing for recovery",
            "Someone to drive you back if sedation involved",
            "Medical records if relevant",
        ],
        "safety_rating": "High — established medical tourism destination",
        "language": "English widely spoken in medical facilities",
    },
    "south_korea": {
        "location": "Seoul, South Korea",
        "country": "South Korea",
        "distance_from_us": "11-13 hour flight from US West Coast",
        "why_go_here": [
            "Global leader in cosmetic innovation — procedures available 3-5 years before US FDA approval",
            "Gangnam district: highest concentration of plastic surgeons in the world",
            "Advanced technology (lasers, threads, fillers not yet in US)",
            "Medical tourism packages with translators and coordinators",
            "High safety standards and skilled surgeons",
            "Combine with vacation — Seoul is a world-class city",
        ],
        "specialties": [
            "Double eyelid surgery (blepharoplasty)",
            "V-line jaw surgery (facial contouring)",
            "Rhinoplasty (Asian rhinoplasty specialty)",
            "Skin treatments (laser, LED, microneedling)",
            "Thread lifts (more advanced than US)",
            "Stem cell facials and PRP treatments",
            "Body contouring",
        ],
        "cost_comparison": {
            "double_eyelid_surgery": {"us": "$3,000-$5,000", "seoul": "$1,500-$2,500"},
            "rhinoplasty": {"us": "$8,000-$15,000", "seoul": "$4,000-$7,000"},
            "v_line_jaw_surgery": {"us": "$20,000-$40,000", "seoul": "$10,000-$15,000"},
            "laser_skin_resurfacing": {"us": "$2,000-$5,000", "seoul": "$800-$1,500"},
        },
        "top_clinics": [
            {"name": "ID Hospital", "specialty": "Facial contouring, rhinoplasty", "accreditation": "JCI accredited"},
            {"name": "Banobagi Plastic Surgery", "specialty": "Anti-aging, facial surgery", "accreditation": "JCI accredited"},
            {"name": "Dream Medical Group", "specialty": "Eyes, nose, facial contouring", "accreditation": "ISO certified"},
        ],
        "recovery_hotels": [
            "Medical tourism hotels in Gangnam (built for recovery)",
            "Airbnb with nursing care available",
            "Clinic-affiliated recovery houses",
        ],
        "travel_logistics": {
            "how_to_get_there": "Fly to Incheon Airport (ICN), metro to Gangnam",
            "visa": "US citizens: 90-day visa-free entry",
            "transportation": "Excellent public transit, taxis, clinic shuttles",
            "insurance": "Medical tourism insurance recommended",
            "language": "English-speaking coordinators at all major clinics",
        },
        "vacation_package_example": {
            "name": "Seoul Skin Transformation + City Tour",
            "includes": [
                "Laser skin resurfacing + PRP facial",
                "7 nights at medical tourism hotel",
                "Airport pickup/dropoff",
                "English-speaking medical coordinator",
                "3 follow-up visits",
                "Seoul city tour (post-recovery)",
                "K-beauty shopping tour",
            ],
            "total_cost": "$3,500-$5,000 (including flights)",
            "us_equivalent_cost": "$8,000-$12,000",
            "savings": "$4,500-$7,000",
        },
        "what_to_bring": [
            "Passport (6+ months validity)",
            "Medical records and photos",
            "Comfortable recovery clothing",
            "Sunscreen and skincare (or buy K-beauty there)",
        ],
        "safety_rating": "Very High — world-class medical standards",
        "language": "English coordinators at all major clinics",
    },
    "colombia": {
        "location": "Medellín & Cali, Colombia",
        "country": "Colombia",
        "distance_from_us": "5-6 hour flight from Miami",
        "why_go_here": [
            "Medellín is the 'plastic surgery capital of South America'",
            "Extremely affordable — 60-70% cheaper than US",
            "Surgeons trained in US and Europe",
            "Beautiful city for recovery (Medellín = 'City of Eternal Spring')",
            "Medical tourism infrastructure with English support",
            "Combine with vacation — coffee region, beaches, culture",
        ],
        "specialties": [
            "Brazilian Butt Lift (BBL) — Colombia is world-famous for this",
            "Liposuction and body contouring",
            "Breast augmentation/lift",
            "Tummy tuck (abdominoplasty)",
            "Facelifts and neck lifts",
            "Rhinoplasty",
        ],
        "cost_comparison": {
            "brazilian_butt_lift": {"us": "$8,000-$15,000", "colombia": "$3,500-$5,500"},
            "liposuction": {"us": "$5,000-$10,000", "colombia": "$2,000-$3,500"},
            "breast_augmentation": {"us": "$6,000-$12,000", "colombia": "$3,000-$4,500"},
            "facelift": {"us": "$12,000-$25,000", "colombia": "$4,000-$7,000"},
        },
        "top_clinics": [
            {"name": "CES Clinic (Medellín)", "specialty": "BBL, body contouring", "accreditation": "ISO certified"},
            {"name": "Clínica Las Vegas (Medellín)", "specialty": "Cosmetic surgery", "accreditation": "JCI accredited"},
            {"name": "Clínica de Marly (Bogotá)", "specialty": "Comprehensive cosmetic", "accreditation": "JCI accredited"},
        ],
        "recovery_hotels": [
            "Recovery houses in Medellín (with nursing staff)",
            "Hotel Dann Carlton (luxury recovery)",
            "Airbnb in El Poblado (safe, upscale neighborhood)",
        ],
        "travel_logistics": {
            "how_to_get_there": "Fly to Medellín (MDE) or Cali (CLO)",
            "visa": "US citizens: 90-day visa-free entry",
            "transportation": "Uber, taxis, clinic shuttles",
            "insurance": "Medical tourism insurance recommended",
            "language": "English-speaking coordinators at major clinics",
        },
        "vacation_package_example": {
            "name": "BBL + Medellín Recovery Retreat",
            "includes": [
                "Brazilian Butt Lift procedure",
                "10 nights at recovery house (nursing care included)",
                "Airport pickup/dropoff",
                "Post-op massages (lymphatic drainage)",
                "BBL pillow and compression garments",
                "Follow-up visits",
            ],
            "total_cost": "$5,000-$7,000 (including flights)",
            "us_equivalent_cost": "$12,000-$18,000",
            "savings": "$7,000-$11,000",
        },
        "what_to_bring": [
            "Passport",
            "Compression garments (or buy there)",
            "Loose clothing for recovery",
            "Someone to travel with you (recommended for BBL)",
        ],
        "safety_rating": "High — verify clinic accreditation",
        "language": "English coordinators available",
    },
    "turkey": {
        "location": "Istanbul, Turkey",
        "country": "Turkey",
        "distance_from_us": "11-13 hour flight from US East Coast",
        "why_go_here": [
            "World leader in hair transplants — best prices and quality",
            "Dental tourism hub (veneers, implants)",
            "Advanced cosmetic surgery at fraction of US cost",
            "Combine with vacation — Istanbul is incredible",
            "All-inclusive packages with hotels and tours",
        ],
        "specialties": [
            "Hair transplants (FUE, DHI methods)",
            "Dental work (veneers, implants, crowns)",
            "Rhinoplasty",
            "Breast augmentation",
            "Liposuction",
            "Eye surgery (LASIK)",
        ],
        "cost_comparison": {
            "hair_transplant_fue": {"us": "$10,000-$20,000", "turkey": "$2,000-$4,000"},
            "dental_veneers_full_set": {"us": "$15,000-$30,000", "turkey": "$3,000-$6,000"},
            "rhinoplasty": {"us": "$8,000-$15,000", "turkey": "$3,000-$5,000"},
        },
        "top_clinics": [
            {"name": "Vera Clinic", "specialty": "Hair transplants", "accreditation": "JCI accredited"},
            {"name": "Estethica", "specialty": "Cosmetic surgery", "accreditation": "JCI accredited"},
            {"name": "Dentakay", "specialty": "Dental tourism", "accreditation": "ISO certified"},
        ],
        "recovery_hotels": [
            "Clinic-affiliated hotels in Istanbul",
            "5-star hotels in Taksim/Sultanahmet",
            "All-inclusive packages with tours",
        ],
        "travel_logistics": {
            "how_to_get_there": "Fly to Istanbul Airport (IST)",
            "visa": "US citizens: e-Visa required ($50, online)",
            "transportation": "Clinic shuttles, metro, taxis",
            "insurance": "Medical tourism insurance recommended",
            "language": "English widely spoken in medical facilities",
        },
        "vacation_package_example": {
            "name": "Hair Transplant + Istanbul Experience",
            "includes": [
                "FUE hair transplant (3,000-4,000 grafts)",
                "7 nights at 4-star hotel",
                "Airport transfers",
                "Post-op care kit",
                "Follow-up visits",
                "Bosphorus cruise tour",
            ],
            "total_cost": "$3,000-$5,000 (including flights)",
            "us_equivalent_cost": "$15,000-$25,000",
            "savings": "$12,000-$20,000",
        },
        "what_to_bring": [
            "Passport (6+ months validity)",
            "e-Visa printout",
            "Hat for post-transplant sun protection",
            "Comfortable clothing",
        ],
        "safety_rating": "High — verify JCI accreditation",
        "language": "English coordinators at all major clinics",
    },
    "miami_usa": {
        "location": "Miami, Florida, USA",
        "country": "United States",
        "distance_from_us": "Domestic travel",
        "why_go_here": [
            "Cutting-edge procedures without leaving the US",
            "Top surgeons (many trained in South America and US)",
            "Medical tourism infrastructure for international patients",
            "Vacation-friendly recovery — beaches, nightlife, culture",
            "No language barrier, US medical standards",
            "Insurance may cover some procedures",
        ],
        "specialties": [
            "Brazilian Butt Lift (BBL)",
            "Body contouring and liposuction",
            "Breast augmentation/lift",
            "Mommy makeovers",
            "Facelifts and neck lifts",
            "Non-surgical treatments (threads, fillers, lasers)",
        ],
        "cost_comparison": {
            "brazilian_butt_lift": {"us_average": "$8,000-$15,000", "miami": "$7,000-$12,000"},
            "liposuction": {"us_average": "$5,000-$10,000", "miami": "$4,000-$8,000"},
            "breast_augmentation": {"us_average": "$6,000-$12,000", "miami": "$5,000-$10,000"},
            "note": "Miami is competitive with US prices but offers vacation recovery",
        },
        "top_clinics": [
            {"name": "Seduction Cosmetic Center", "specialty": "BBL, body contouring", "accreditation": "AAAASF accredited"},
            {"name": "Strax Rejuvenation", "specialty": "Mommy makeovers, body", "accreditation": "AAAASF accredited"},
            {"name": "Miami Plastic Surgery", "specialty": "Facial and body", "accreditation": "AAAASF accredited"},
        ],
        "recovery_hotels": [
            "Recovery houses in Miami (nursing care)",
            "Beachfront hotels in South Beach",
            "Airbnb in Brickell or Coral Gables",
        ],
        "travel_logistics": {
            "how_to_get_there": "Fly to Miami International Airport (MIA)",
            "visa": "Not required (domestic)",
            "transportation": "Uber, Lyft, rental car",
            "insurance": "Check if your US insurance covers elective procedures",
            "language": "English and Spanish",
        },
        "vacation_package_example": {
            "name": "Miami Mommy Makeover + Beach Recovery",
            "includes": [
                "Tummy tuck + breast lift",
                "7 nights at recovery house (nursing care)",
                "Airport transfers",
                "Post-op massages",
                "Compression garments",
                "Follow-up visits",
            ],
            "total_cost": "$12,000-$18,000",
            "note": "More expensive than international but no passport needed, US standards",
        },
        "what_to_bring": [
            "ID (driver's license or passport)",
            "Insurance card",
            "Comfortable recovery clothing",
            "Someone to help you during recovery",
        ],
        "safety_rating": "Very High — US medical standards",
        "language": "English",
    },
}

# Cutting-edge procedures available internationally
CUTTING_EDGE_PROCEDURES = {
    "stem_cell_facelift": {
        "name": "Stem Cell Facelift",
        "description": "Uses patient's own stem cells (from fat) to rejuvenate facial tissue",
        "available_in": ["Mexico", "South Korea", "Colombia", "Thailand"],
        "not_yet_in_us": "FDA approval pending for cosmetic use",
        "cost_range": "$5,000-$12,000",
        "recovery_time": "1-2 weeks",
        "results_last": "5-10 years",
        "why_not_in_us": "FDA classifies stem cells as biologics — requires extensive trials for cosmetic approval",
    },
    "vampire_facelift_advanced": {
        "name": "Advanced Vampire Facelift (PRP + Growth Factors)",
        "description": "PRP combined with lab-cultured growth factors for enhanced results",
        "available_in": ["South Korea", "Japan", "Switzerland"],
        "not_yet_in_us": "Growth factor formulations not FDA-approved",
        "cost_range": "$2,000-$5,000",
        "recovery_time": "1-3 days",
        "results_last": "12-18 months",
        "why_not_in_us": "Cultured growth factors require FDA approval",
    },
    "nano_fat_grafting": {
        "name": "Nano Fat Grafting",
        "description": "Ultra-refined fat cells injected for skin rejuvenation (not volume)",
        "available_in": ["South Korea", "Italy", "Brazil"],
        "not_yet_in_us": "Technique is new, not yet widely adopted in US",
        "cost_range": "$3,000-$8,000",
        "recovery_time": "3-7 days",
        "results_last": "2-5 years",
        "why_not_in_us": "Emerging technique — US surgeons just starting to adopt",
    },
    "thread_lift_cog_threads": {
        "name": "COG Thread Lift (Barbed Threads)",
        "description": "More aggressive threads with barbs for stronger lift",
        "available_in": ["South Korea", "Thailand", "Mexico"],
        "not_yet_in_us": "Some COG thread types not FDA-cleared",
        "cost_range": "$2,000-$6,000",
        "recovery_time": "1 week",
        "results_last": "18-24 months",
        "why_not_in_us": "Specific thread brands awaiting FDA clearance",
    },
    "hifu_advanced": {
        "name": "Advanced HIFU (High-Intensity Focused Ultrasound)",
        "description": "Newer HIFU devices with deeper penetration and faster treatment",
        "available_in": ["South Korea", "China", "Thailand"],
        "not_yet_in_us": "Latest devices not yet FDA-cleared",
        "cost_range": "$1,000-$3,000",
        "recovery_time": "None",
        "results_last": "12-18 months",
        "why_not_in_us": "New device models require FDA clearance",
    },
}


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

@dataclass
class MedicalTourismPackage:
    """A complete medical tourism vacation package."""
    destination: str
    procedure: str
    total_cost: str
    us_equivalent_cost: str
    savings: str
    includes: List[str]
    duration: str
    clinic_name: str
    recovery_hotel: str
    what_to_bring: List[str]
    travel_logistics: Dict[str, str]
    safety_rating: str
    disclaimer: str = MEDICAL_DISCLAIMER

    def to_dict(self) -> dict:
        return asdict(self)


# ---------------------------------------------------------------------------
# Medical Tourism Engine
# ---------------------------------------------------------------------------

class MedicalTourismEngine:
    """
    International medical tourism packages and cutting-edge procedures.
    Turn medical trips into recovery vacations.
    """

    def __init__(self):
        self.data_dir = DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.destinations = DESTINATIONS
        self.cutting_edge = CUTTING_EDGE_PROCEDURES

    def get_all_destinations(self) -> Dict[str, Any]:
        """Get all medical tourism destinations."""
        return self.destinations

    def get_destination_info(self, destination_key: str) -> Optional[Dict[str, Any]]:
        """Get detailed info about a specific destination."""
        return self.destinations.get(destination_key)

    def find_destinations_for_procedure(self, procedure: str) -> List[Dict[str, Any]]:
        """Find destinations that offer a specific procedure."""
        procedure_lower = procedure.lower()
        matches = []
        
        for key, dest in self.destinations.items():
            for specialty in dest["specialties"]:
                if procedure_lower in specialty.lower():
                    matches.append({
                        "destination": dest["location"],
                        "country": dest["country"],
                        "specialty": specialty,
                        "cost_comparison": dest.get("cost_comparison", {}),
                        "why_go_here": dest["why_go_here"],
                        "safety_rating": dest["safety_rating"],
                        "key": key,
                    })
                    break
        
        return matches

    def compare_costs(self, procedure: str) -> Dict[str, Any]:
        """Compare costs for a procedure across all destinations."""
        comparison = {
            "procedure": procedure,
            "destinations": [],
            "disclaimer": MEDICAL_DISCLAIMER,
        }
        
        for key, dest in self.destinations.items():
            costs = dest.get("cost_comparison", {})
            for proc_key, cost_data in costs.items():
                if procedure.lower() in proc_key.lower():
                    comparison["destinations"].append({
                        "location": dest["location"],
                        "cost": cost_data.get(key.split("_")[0], cost_data),
                        "savings_vs_us": self._calculate_savings(cost_data),
                    })
        
        return comparison

    def _calculate_savings(self, cost_data: dict) -> str:
        """Calculate savings vs US cost."""
        if "us" in cost_data:
            us_cost = cost_data["us"]
            destination_cost = [v for k, v in cost_data.items() if k != "us"][0]
            # Simple string extraction (would need proper parsing in production)
            return f"Save ~50-70% vs US"
        return "Varies"

    def get_cutting_edge_procedures(self) -> Dict[str, Any]:
        """Get procedures available internationally but not yet in US."""
        return self.cutting_edge

    def find_cutting_edge_by_destination(self, destination: str) -> List[Dict[str, Any]]:
        """Find cutting-edge procedures available in a specific destination."""
        destination_lower = destination.lower()
        matches = []
        
        for key, proc in self.cutting_edge.items():
            for location in proc["available_in"]:
                if destination_lower in location.lower():
                    matches.append({
                        "procedure": proc["name"],
                        "description": proc["description"],
                        "cost_range": proc["cost_range"],
                        "recovery_time": proc["recovery_time"],
                        "why_not_in_us": proc["why_not_in_us"],
                        "key": key,
                    })
                    break
        
        return matches

    def generate_vacation_package(
        self,
        destination_key: str,
        procedure: str,
        duration_nights: int = 7,
    ) -> Optional[MedicalTourismPackage]:
        """Generate a complete medical tourism vacation package."""
        dest = self.destinations.get(destination_key)
        if not dest:
            return None
        
        # Use example package if available
        if "vacation_package_example" in dest:
            example = dest["vacation_package_example"]
            return MedicalTourismPackage(
                destination=dest["location"],
                procedure=example.get("name", procedure),
                total_cost=example["total_cost"],
                us_equivalent_cost=example.get("us_equivalent_cost", "N/A"),
                savings=example.get("savings", "Varies"),
                includes=example["includes"],
                duration=f"{duration_nights} nights",
                clinic_name=dest["top_clinics"][0]["name"] if dest["top_clinics"] else "TBD",
                recovery_hotel=dest["recovery_hotels"][0] if dest["recovery_hotels"] else "TBD",
                what_to_bring=dest["what_to_bring"],
                travel_logistics=dest["travel_logistics"],
                safety_rating=dest["safety_rating"],
            )
        
        return None

    def get_travel_tips(self, destination_key: str) -> Dict[str, Any]:
        """Get travel tips and logistics for a destination."""
        dest = self.destinations.get(destination_key)
        if not dest:
            return {}
        
        return {
            "destination": dest["location"],
            "how_to_get_there": dest["travel_logistics"]["how_to_get_there"],
            "what_to_bring": dest["what_to_bring"],
            "language": dest["language"],
            "safety_rating": dest["safety_rating"],
            "emergency_contact": dest["travel_logistics"].get("emergency_contact", "Contact US Embassy"),
            "insurance_note": dest["travel_logistics"].get("insurance", "Check insurance coverage"),
            "disclaimer": MEDICAL_DISCLAIMER,
        }

    def get_tijuana_recommendation(self) -> Dict[str, Any]:
        """Get Audrey's personal Tijuana surgeon recommendation."""
        tj = self.destinations.get("tijuana_mexico")
        if not tj:
            return {}
        
        return {
            "destination": "Tijuana, Mexico",
            "audrey_says": (
                "I've been to this surgeon's office in TJ. It's MARBLE. Nicer than "
                "most US clinics I've seen. World-class quality at a fraction of the price. "
                "You can literally drive across the border, get the procedure, and drive home "
                "the same day. It's 15 minutes from San Diego."
            ),
            "top_clinic": tj["top_clinics"][0],
            "cost_savings": "50-80% cheaper than US for same quality",
            "procedures": tj["specialties"],
            "travel_tip": "Walk across the border at San Ysidro, take a taxi to the clinic. Easy.",
            "disclaimer": MEDICAL_DISCLAIMER,
        }


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Master Platform: Medical Tourism Engine — Demo")
    print("=" * 55)
    
    engine = MedicalTourismEngine()
    
    # Find destinations for PDO threads
    print("\nWhere can I get PDO threads internationally?")
    matches = engine.find_destinations_for_procedure("PDO threads")
    for match in matches:
        print(f"  - {match['destination']}: {match['cost_comparison']}")
    
    # Audrey's TJ recommendation
    print("\nAudrey's Tijuana Recommendation:")
    tj_rec = engine.get_tijuana_recommendation()
    print(f"  {tj_rec['audrey_says']}")
    
    # Cutting-edge procedures
    print("\nCutting-edge procedures not yet in the US:")
    for key, proc in engine.get_cutting_edge_procedures().items():
        print(f"  - {proc['name']}: Available in {', '.join(proc['available_in'][:3])}")
        print(f"    Why not in US: {proc['why_not_in_us']}")
    
    print(f"\n{MEDICAL_DISCLAIMER}")
