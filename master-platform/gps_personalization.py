"""
Master Platform: GPS Personalization Engine
=============================================
Location-based personalization across ALL apps on the platform.
Climate-aware recommendations, local providers, location-specific affiliate links.

Author: Audrey Evans
"""

import json
import math
from pathlib import Path
from typing import List, Dict, Optional, Any, Literal, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DATA_DIR = Path(__file__).parent / "data" / "gps"

# US state climate profiles
STATE_CLIMATE_PROFILES = {
    "CO": {
        "name": "Colorado",
        "climate_type": "semi_arid_alpine",
        "avg_humidity_percent": 35,
        "avg_uv_index": 7,
        "altitude_ft": 5280,
        "winter": {"humidity": 20, "temp_f": 30, "uv": 3, "concerns": ["extreme_dryness", "wind_damage", "altitude_uv", "cracking", "chapping"]},
        "spring": {"humidity": 30, "temp_f": 55, "uv": 6, "concerns": ["dryness", "uv_exposure", "wind"]},
        "summer": {"humidity": 40, "temp_f": 80, "uv": 9, "concerns": ["sun_damage", "altitude_uv", "dehydration"]},
        "fall": {"humidity": 30, "temp_f": 50, "uv": 5, "concerns": ["dryness", "wind", "transition"]},
    },
    "CA": {
        "name": "California",
        "climate_type": "mediterranean",
        "avg_humidity_percent": 60,
        "avg_uv_index": 7,
        "altitude_ft": 200,
        "winter": {"humidity": 65, "temp_f": 55, "uv": 3, "concerns": ["mild_dryness"]},
        "spring": {"humidity": 55, "temp_f": 65, "uv": 7, "concerns": ["uv_exposure", "pollen"]},
        "summer": {"humidity": 50, "temp_f": 80, "uv": 10, "concerns": ["sun_damage", "oil_production", "sweat"]},
        "fall": {"humidity": 45, "temp_f": 70, "uv": 5, "concerns": ["wildfire_smoke", "dryness"]},
    },
    "FL": {
        "name": "Florida",
        "climate_type": "subtropical_humid",
        "avg_humidity_percent": 75,
        "avg_uv_index": 8,
        "altitude_ft": 50,
        "winter": {"humidity": 65, "temp_f": 65, "uv": 5, "concerns": ["mild_humidity"]},
        "spring": {"humidity": 70, "temp_f": 78, "uv": 8, "concerns": ["humidity", "uv_exposure"]},
        "summer": {"humidity": 85, "temp_f": 90, "uv": 11, "concerns": ["extreme_humidity", "sweat", "fungal_risk", "sun_damage"]},
        "fall": {"humidity": 75, "temp_f": 80, "uv": 7, "concerns": ["humidity", "hurricane_season_stress"]},
    },
    "AZ": {
        "name": "Arizona",
        "climate_type": "desert",
        "avg_humidity_percent": 20,
        "avg_uv_index": 9,
        "altitude_ft": 1100,
        "winter": {"humidity": 30, "temp_f": 55, "uv": 5, "concerns": ["dryness"]},
        "spring": {"humidity": 15, "temp_f": 80, "uv": 9, "concerns": ["extreme_dryness", "sun_damage"]},
        "summer": {"humidity": 25, "temp_f": 105, "uv": 12, "concerns": ["extreme_heat", "extreme_uv", "dehydration", "heat_rash"]},
        "fall": {"humidity": 20, "temp_f": 85, "uv": 7, "concerns": ["dryness", "sun_damage"]},
    },
    "NY": {
        "name": "New York",
        "climate_type": "humid_continental",
        "avg_humidity_percent": 60,
        "avg_uv_index": 5,
        "altitude_ft": 33,
        "winter": {"humidity": 55, "temp_f": 30, "uv": 2, "concerns": ["cold_damage", "wind", "indoor_heating_dryness"]},
        "spring": {"humidity": 55, "temp_f": 55, "uv": 5, "concerns": ["pollen", "transition"]},
        "summer": {"humidity": 70, "temp_f": 80, "uv": 8, "concerns": ["humidity", "pollution", "sweat"]},
        "fall": {"humidity": 60, "temp_f": 55, "uv": 4, "concerns": ["transition", "wind"]},
    },
    "TX": {
        "name": "Texas",
        "climate_type": "varied_subtropical",
        "avg_humidity_percent": 55,
        "avg_uv_index": 8,
        "altitude_ft": 500,
        "winter": {"humidity": 55, "temp_f": 45, "uv": 4, "concerns": ["mild_dryness"]},
        "spring": {"humidity": 60, "temp_f": 70, "uv": 7, "concerns": ["pollen", "uv_exposure"]},
        "summer": {"humidity": 65, "temp_f": 95, "uv": 10, "concerns": ["extreme_heat", "sun_damage", "sweat", "humidity"]},
        "fall": {"humidity": 55, "temp_f": 75, "uv": 6, "concerns": ["transition"]},
    },
    "WA": {
        "name": "Washington",
        "climate_type": "oceanic",
        "avg_humidity_percent": 70,
        "avg_uv_index": 4,
        "altitude_ft": 175,
        "winter": {"humidity": 80, "temp_f": 40, "uv": 1, "concerns": ["vitamin_d_deficiency", "moisture_barrier", "gray_sky_depression"]},
        "spring": {"humidity": 65, "temp_f": 55, "uv": 4, "concerns": ["pollen", "transition"]},
        "summer": {"humidity": 55, "temp_f": 75, "uv": 7, "concerns": ["uv_exposure", "wildfire_smoke"]},
        "fall": {"humidity": 75, "temp_f": 50, "uv": 3, "concerns": ["moisture", "rain"]},
    },
    "HI": {
        "name": "Hawaii",
        "climate_type": "tropical",
        "avg_humidity_percent": 75,
        "avg_uv_index": 10,
        "altitude_ft": 50,
        "winter": {"humidity": 75, "temp_f": 75, "uv": 8, "concerns": ["humidity", "uv_exposure"]},
        "spring": {"humidity": 70, "temp_f": 78, "uv": 10, "concerns": ["sun_damage", "humidity"]},
        "summer": {"humidity": 70, "temp_f": 85, "uv": 12, "concerns": ["extreme_uv", "sweat", "salt_water_damage"]},
        "fall": {"humidity": 75, "temp_f": 80, "uv": 9, "concerns": ["humidity", "uv_exposure"]},
    },
}

# Skincare recommendations by climate concern
CLIMATE_SKINCARE_MAP = {
    "extreme_dryness": {
        "ingredients": ["hyaluronic acid", "ceramides", "squalane", "shea butter", "glycerin"],
        "products": ["heavy moisturizer", "facial oil", "overnight mask", "humidifier"],
        "avoid": ["alcohol-based toners", "harsh cleansers", "retinol (reduce frequency)"],
        "tip": "Layer hydration: hydrating toner → serum → moisturizer → facial oil. Use a humidifier at night.",
    },
    "altitude_uv": {
        "ingredients": ["zinc oxide", "titanium dioxide", "vitamin C", "niacinamide"],
        "products": ["SPF 50+ mineral sunscreen", "antioxidant serum", "UV-protective lip balm"],
        "avoid": ["skipping sunscreen", "chemical-only sunscreens at altitude"],
        "tip": "UV increases 4% per 1,000ft elevation. At 5,280ft (Denver), you get 21% more UV than sea level.",
    },
    "sun_damage": {
        "ingredients": ["vitamin C", "niacinamide", "retinol", "alpha arbutin", "zinc oxide"],
        "products": ["broad-spectrum SPF 50+", "vitamin C serum", "after-sun repair cream"],
        "avoid": ["tanning", "midday sun exposure", "expired sunscreen"],
        "tip": "Reapply sunscreen every 2 hours, more if swimming or sweating.",
    },
    "extreme_humidity": {
        "ingredients": ["niacinamide", "salicylic acid", "tea tree oil", "hyaluronic acid (light)"],
        "products": ["gel moisturizer", "oil-free sunscreen", "blotting papers", "lightweight serum"],
        "avoid": ["heavy creams", "occlusive oils", "thick foundations"],
        "tip": "Switch to gel-based products. Double cleanse at night to remove sweat and buildup.",
    },
    "wind_damage": {
        "ingredients": ["ceramides", "petrolatum", "beeswax", "shea butter"],
        "products": ["barrier repair cream", "lip balm", "protective face balm"],
        "avoid": ["thin moisturizers", "alcohol-based products"],
        "tip": "Apply a wind-barrier balm before going outside. Protect lips and exposed skin.",
    },
    "cold_damage": {
        "ingredients": ["ceramides", "squalane", "panthenol", "allantoin"],
        "products": ["rich night cream", "barrier repair serum", "gentle cleanser"],
        "avoid": ["hot water on face", "harsh exfoliants", "fragrance"],
        "tip": "Lukewarm water only. Switch to cream cleanser in winter.",
    },
    "pollution": {
        "ingredients": ["vitamin C", "vitamin E", "niacinamide", "green tea extract"],
        "products": ["antioxidant serum", "double cleanse routine", "pollution shield primer"],
        "avoid": ["sleeping with makeup", "skipping cleansing"],
        "tip": "Double cleanse every evening. Use antioxidant serum under sunscreen.",
    },
    "wildfire_smoke": {
        "ingredients": ["niacinamide", "centella asiatica", "green tea", "vitamin E"],
        "products": ["air purifier", "barrier cream", "soothing mask", "gentle cleanser"],
        "avoid": ["exfoliants during smoke events", "outdoor exercise"],
        "tip": "Smoke particles are tiny and penetrate skin. Use barrier cream and stay indoors on bad air days.",
    },
    "dehydration": {
        "ingredients": ["hyaluronic acid", "glycerin", "aloe vera", "electrolytes (internal)"],
        "products": ["hydrating mist", "water-based serum", "electrolyte drinks"],
        "avoid": ["caffeine excess", "alcohol", "skipping water intake"],
        "tip": "Hydrate from inside AND outside. Drink half your body weight in ounces of water daily.",
    },
    "fungal_risk": {
        "ingredients": ["tea tree oil", "zinc pyrithione", "ketoconazole"],
        "products": ["antifungal wash", "lightweight moisturizer", "breathable fabrics"],
        "avoid": ["heavy oils", "occlusive products on body", "tight synthetic clothing"],
        "tip": "In humid climates, fungal acne is common. Use fungal-safe products.",
    },
}

# Procedure legality by state (simplified — some procedures have varying regulations)
PROCEDURE_LEGALITY = {
    "botox": {"legal_everywhere": True, "notes": "Must be administered by licensed provider"},
    "NAD+_IV": {"legal_everywhere": False, "restricted_states": ["NY"], "notes": "Regulations vary; some states require physician oversight"},
    "stem_cell_therapy": {"legal_everywhere": False, "restricted_states": ["CA", "NY"], "notes": "FDA regulates; many clinics operate in gray area"},
    "ketamine_therapy": {"legal_everywhere": False, "restricted_states": [], "notes": "Legal but heavily regulated; requires licensed clinic"},
    "permanent_eye_color": {"legal_everywhere": False, "restricted_states": [], "notes": "Very few providers; not FDA-approved"},
}


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

@dataclass
class UserLocation:
    """User's location data."""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    city: Optional[str] = None
    state: Optional[str] = None
    state_code: Optional[str] = None
    country: str = "US"
    zip_code: Optional[str] = None
    altitude_ft: Optional[int] = None
    auto_detected: bool = False

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "UserLocation":
        return cls(**d)


@dataclass
class ClimateContext:
    """Current climate context for a location."""
    location: UserLocation
    season: str  # winter, spring, summer, fall
    humidity_percent: int
    uv_index: int
    temperature_f: int
    altitude_ft: int
    concerns: List[str]
    skincare_recommendations: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class LocalizedRecommendation:
    """A recommendation personalized to user's location."""
    recommendation_type: str  # product, procedure, clinic, routine
    title: str
    description: str
    location_relevance: str  # Why this is relevant to their location
    affiliate_link: Optional[str] = None
    local_provider: Optional[str] = None
    climate_factor: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


# ---------------------------------------------------------------------------
# GPS Personalization Engine
# ---------------------------------------------------------------------------

class GPSPersonalizationEngine:
    """
    Location-based personalization engine for all platform apps.
    Provides climate-aware recommendations, local providers, and location-specific content.
    """

    def __init__(self):
        self.data_dir = DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)

    # ---- Location detection ----

    def set_location_manual(self, city: str, state_code: str, zip_code: Optional[str] = None) -> UserLocation:
        """Set user location manually."""
        climate = STATE_CLIMATE_PROFILES.get(state_code, {})
        return UserLocation(
            city=city,
            state=climate.get("name", state_code),
            state_code=state_code,
            country="US",
            zip_code=zip_code,
            altitude_ft=climate.get("altitude_ft", 0),
            auto_detected=False,
        )

    def set_location_gps(self, latitude: float, longitude: float) -> UserLocation:
        """Set user location from GPS coordinates (would use reverse geocoding in production)."""
        return UserLocation(
            latitude=latitude,
            longitude=longitude,
            auto_detected=True,
        )

    # ---- Climate context ----

    def get_current_season(self) -> str:
        """Get current season based on date."""
        month = datetime.now().month
        if month in (12, 1, 2):
            return "winter"
        elif month in (3, 4, 5):
            return "spring"
        elif month in (6, 7, 8):
            return "summer"
        else:
            return "fall"

    def get_climate_context(self, location: UserLocation, season: Optional[str] = None) -> ClimateContext:
        """
        Get the climate context for a user's location.
        
        Args:
            location: User's location
            season: Override season (default: auto-detect)
        
        Returns:
            ClimateContext with climate data and skincare concerns
        """
        if season is None:
            season = self.get_current_season()
        
        state_code = location.state_code or "CO"  # Default to Colorado
        climate = STATE_CLIMATE_PROFILES.get(state_code, STATE_CLIMATE_PROFILES["CO"])
        season_data = climate.get(season, climate.get("winter", {}))
        
        concerns = season_data.get("concerns", [])
        
        # Build skincare recommendations from concerns
        skincare_recs = {}
        for concern in concerns:
            if concern in CLIMATE_SKINCARE_MAP:
                skincare_recs[concern] = CLIMATE_SKINCARE_MAP[concern]
        
        return ClimateContext(
            location=location,
            season=season,
            humidity_percent=season_data.get("humidity", climate.get("avg_humidity_percent", 50)),
            uv_index=season_data.get("uv", climate.get("avg_uv_index", 5)),
            temperature_f=season_data.get("temp_f", 70),
            altitude_ft=climate.get("altitude_ft", 0),
            concerns=concerns,
            skincare_recommendations=skincare_recs,
        )

    # ---- Skincare recommendations ----

    def get_skincare_routine(
        self,
        location: UserLocation,
        skin_type: str = "normal",
        season: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate a climate-aware skincare routine.
        
        Args:
            location: User's location
            skin_type: User's skin type (oily, dry, combination, sensitive, normal)
            season: Override season
        
        Returns:
            Morning and evening routines with climate-specific products
        """
        climate = self.get_climate_context(location, season)
        
        # Base routine
        routine = {
            "location": f"{location.city}, {location.state_code}",
            "season": climate.season,
            "climate_summary": f"Humidity: {climate.humidity_percent}%, UV: {climate.uv_index}, Temp: {climate.temperature_f}°F, Alt: {climate.altitude_ft}ft",
            "key_concerns": climate.concerns,
            "morning": [],
            "evening": [],
            "weekly": [],
            "climate_tips": [],
        }
        
        # Morning routine
        routine["morning"] = [
            {"step": 1, "product": "Gentle Cleanser", "note": self._cleanser_note(climate, skin_type)},
            {"step": 2, "product": "Toner/Essence", "note": self._toner_note(climate, skin_type)},
            {"step": 3, "product": "Vitamin C Serum", "note": "Antioxidant protection — essential for UV defense"},
        ]
        
        # Add hydration step based on climate
        if climate.humidity_percent < 40:
            routine["morning"].append({"step": 4, "product": "Hyaluronic Acid Serum", "note": "Critical in dry climates — apply to damp skin"})
        
        # Moisturizer based on humidity
        if climate.humidity_percent > 70:
            routine["morning"].append({"step": 5, "product": "Gel Moisturizer", "note": "Lightweight for humid climate"})
        elif climate.humidity_percent < 35:
            routine["morning"].append({"step": 5, "product": "Rich Cream Moisturizer", "note": "Heavy moisture for dry climate"})
        else:
            routine["morning"].append({"step": 5, "product": "Lotion Moisturizer", "note": "Balanced for moderate humidity"})
        
        # Sunscreen — always, but SPF varies
        spf_note = "SPF 30+" if climate.uv_index < 6 else "SPF 50+ mineral sunscreen — high UV area"
        if climate.altitude_ft > 3000:
            spf_note += f" (altitude: +{int((climate.altitude_ft / 1000) * 4)}% UV increase)"
        routine["morning"].append({"step": 6, "product": "Sunscreen", "note": spf_note})
        
        # Evening routine
        routine["evening"] = [
            {"step": 1, "product": "Oil Cleanser / Micellar Water", "note": "First cleanse to remove sunscreen and makeup"},
            {"step": 2, "product": "Gentle Cleanser", "note": "Second cleanse for clean skin"},
            {"step": 3, "product": "Treatment Serum", "note": self._treatment_note(climate, skin_type)},
        ]
        
        if climate.humidity_percent < 40:
            routine["evening"].append({"step": 4, "product": "Facial Oil", "note": "Seal in moisture overnight in dry climate"})
        
        routine["evening"].append({"step": 5, "product": "Night Cream", "note": "Repair and restore while sleeping"})
        
        # Weekly treatments
        routine["weekly"] = [
            {"product": "Exfoliant", "frequency": "1-2x/week", "note": "Chemical exfoliant preferred over physical"},
            {"product": "Hydrating Mask", "frequency": "1-2x/week", "note": "Extra hydration boost"},
        ]
        
        if "sun_damage" in climate.concerns:
            routine["weekly"].append({"product": "Brightening Mask", "frequency": "1x/week", "note": "Address sun damage and hyperpigmentation"})
        
        # Climate-specific tips
        for concern in climate.concerns:
            if concern in CLIMATE_SKINCARE_MAP:
                routine["climate_tips"].append({
                    "concern": concern,
                    "tip": CLIMATE_SKINCARE_MAP[concern]["tip"],
                    "key_ingredients": CLIMATE_SKINCARE_MAP[concern]["ingredients"][:3],
                    "avoid": CLIMATE_SKINCARE_MAP[concern]["avoid"][:2],
                })
        
        return routine

    def _cleanser_note(self, climate: ClimateContext, skin_type: str) -> str:
        if climate.humidity_percent < 35 or skin_type == "dry":
            return "Cream or milk cleanser — avoid foaming in dry climate"
        elif climate.humidity_percent > 70 or skin_type == "oily":
            return "Gel or foaming cleanser — control oil in humid climate"
        return "Gentle gel cleanser"

    def _toner_note(self, climate: ClimateContext, skin_type: str) -> str:
        if climate.humidity_percent < 35:
            return "Hydrating toner (no alcohol) — prep skin for moisture"
        elif climate.humidity_percent > 70:
            return "Pore-minimizing toner with niacinamide"
        return "Balancing toner"

    def _treatment_note(self, climate: ClimateContext, skin_type: str) -> str:
        if "sun_damage" in climate.concerns:
            return "Retinol or vitamin A derivative — repair sun damage (evening only)"
        elif "extreme_dryness" in climate.concerns:
            return "Ceramide serum — rebuild moisture barrier"
        elif "extreme_humidity" in climate.concerns:
            return "Niacinamide serum — control oil and minimize pores"
        return "Retinol 2-3x/week, niacinamide on other nights"

    # ---- Travel mode ----

    def get_travel_skincare_kit(
        self,
        home_location: UserLocation,
        travel_destination: str,  # State code
        skin_type: str = "normal",
    ) -> Dict[str, Any]:
        """
        Generate travel skincare recommendations when visiting a different climate.
        
        Args:
            home_location: User's home location
            travel_destination: Destination state code
            skin_type: User's skin type
        
        Returns:
            Travel skincare kit with transition products
        """
        home_climate = self.get_climate_context(home_location)
        
        dest_location = UserLocation(state_code=travel_destination)
        dest_climate = self.get_climate_context(dest_location)
        
        home_profile = STATE_CLIMATE_PROFILES.get(home_location.state_code, {})
        dest_profile = STATE_CLIMATE_PROFILES.get(travel_destination, {})
        
        humidity_change = dest_climate.humidity_percent - home_climate.humidity_percent
        uv_change = dest_climate.uv_index - home_climate.uv_index
        temp_change = dest_climate.temperature_f - home_climate.temperature_f
        
        kit = {
            "from": f"{home_location.city}, {home_location.state_code} ({home_profile.get('climate_type', 'unknown')})",
            "to": f"{dest_profile.get('name', travel_destination)} ({dest_profile.get('climate_type', 'unknown')})",
            "climate_shift": {
                "humidity_change": f"{'+' if humidity_change > 0 else ''}{humidity_change}%",
                "uv_change": f"{'+' if uv_change > 0 else ''}{uv_change}",
                "temp_change": f"{'+' if temp_change > 0 else ''}{temp_change}°F",
            },
            "must_pack": [],
            "leave_behind": [],
            "buy_there": [],
            "transition_tips": [],
        }
        
        # Humidity shift recommendations
        if humidity_change > 20:
            kit["must_pack"].append("Lightweight gel moisturizer")
            kit["must_pack"].append("Oil-free sunscreen")
            kit["leave_behind"].append("Heavy cream moisturizer")
            kit["transition_tips"].append(f"Going from dry to humid (+{humidity_change}% humidity). Switch to lighter products.")
        elif humidity_change < -20:
            kit["must_pack"].append("Rich cream moisturizer")
            kit["must_pack"].append("Facial oil")
            kit["must_pack"].append("Hydrating mist")
            kit["leave_behind"].append("Mattifying products")
            kit["transition_tips"].append(f"Going from humid to dry ({humidity_change}% humidity). Layer extra hydration.")
        
        # UV shift recommendations
        if uv_change > 3:
            kit["must_pack"].append("SPF 50+ mineral sunscreen")
            kit["must_pack"].append("Wide-brim hat")
            kit["must_pack"].append("After-sun repair cream")
            kit["transition_tips"].append(f"UV index much higher at destination (+{uv_change}). Reapply sunscreen every 90 minutes.")
        
        # Temperature shift
        if temp_change > 20:
            kit["must_pack"].append("Blotting papers")
            kit["transition_tips"].append("Higher temperatures mean more sweat and oil. Cleanse more frequently.")
        elif temp_change < -20:
            kit["must_pack"].append("Barrier repair cream")
            kit["transition_tips"].append("Cold weather damages moisture barrier. Apply barrier cream before going outside.")
        
        # Always pack
        kit["must_pack"].extend(["Travel-size gentle cleanser", "Lip balm with SPF"])
        
        return kit

    # ---- Procedure availability ----

    def check_procedure_legality(self, procedure_name: str, state_code: str) -> Dict[str, Any]:
        """Check if a procedure is legal/available in a specific state."""
        proc_info = PROCEDURE_LEGALITY.get(procedure_name, {})
        
        if not proc_info:
            return {
                "procedure": procedure_name,
                "state": state_code,
                "status": "unknown",
                "note": "Procedure not in our database. Check with local providers.",
            }
        
        if proc_info.get("legal_everywhere"):
            return {
                "procedure": procedure_name,
                "state": state_code,
                "status": "legal",
                "note": proc_info.get("notes", ""),
            }
        
        restricted = proc_info.get("restricted_states", [])
        if state_code in restricted:
            return {
                "procedure": procedure_name,
                "state": state_code,
                "status": "restricted",
                "note": f"This procedure has restrictions in {state_code}. {proc_info.get('notes', '')}",
            }
        
        return {
            "procedure": procedure_name,
            "state": state_code,
            "status": "available",
            "note": proc_info.get("notes", ""),
        }

    # ---- Seasonal routine adjustments ----

    def get_seasonal_transition_guide(
        self,
        location: UserLocation,
        from_season: str,
        to_season: str,
    ) -> Dict[str, Any]:
        """
        Get guidance for transitioning skincare between seasons.
        
        Args:
            location: User's location
            from_season: Current season
            to_season: Upcoming season
        
        Returns:
            Transition guide with product swaps and timing
        """
        from_climate = self.get_climate_context(location, from_season)
        to_climate = self.get_climate_context(location, to_season)
        
        guide = {
            "location": f"{location.city}, {location.state_code}",
            "transition": f"{from_season.title()} → {to_season.title()}",
            "humidity_shift": f"{from_climate.humidity_percent}% → {to_climate.humidity_percent}%",
            "uv_shift": f"{from_climate.uv_index} → {to_climate.uv_index}",
            "temp_shift": f"{from_climate.temperature_f}°F → {to_climate.temperature_f}°F",
            "product_swaps": [],
            "new_concerns": [],
            "resolved_concerns": [],
            "timing": "Start transitioning 2 weeks before season change",
        }
        
        # Identify new and resolved concerns
        new_concerns = set(to_climate.concerns) - set(from_climate.concerns)
        resolved = set(from_climate.concerns) - set(to_climate.concerns)
        
        guide["new_concerns"] = list(new_concerns)
        guide["resolved_concerns"] = list(resolved)
        
        # Product swap recommendations
        humidity_change = to_climate.humidity_percent - from_climate.humidity_percent
        if humidity_change > 15:
            guide["product_swaps"].append({
                "swap": "Moisturizer",
                "from": "Rich cream",
                "to": "Lightweight gel or lotion",
                "reason": f"Humidity increasing by {humidity_change}%",
            })
        elif humidity_change < -15:
            guide["product_swaps"].append({
                "swap": "Moisturizer",
                "from": "Lightweight gel",
                "to": "Rich cream with ceramides",
                "reason": f"Humidity decreasing by {abs(humidity_change)}%",
            })
        
        uv_change = to_climate.uv_index - from_climate.uv_index
        if uv_change > 2:
            guide["product_swaps"].append({
                "swap": "Sunscreen",
                "from": "SPF 30",
                "to": "SPF 50+ with reapplication",
                "reason": f"UV index increasing by {uv_change}",
            })
        
        return guide

    # ---- Location-based affiliate links ----

    def get_localized_affiliate_products(
        self,
        location: UserLocation,
        product_category: str = "skincare",
    ) -> List[Dict[str, Any]]:
        """
        Get affiliate product recommendations based on location and climate.
        
        Args:
            location: User's location
            product_category: Product category
        
        Returns:
            List of location-relevant products with affiliate potential
        """
        climate = self.get_climate_context(location)
        products = []
        
        for concern in climate.concerns:
            if concern in CLIMATE_SKINCARE_MAP:
                concern_data = CLIMATE_SKINCARE_MAP[concern]
                for ingredient in concern_data["ingredients"][:2]:
                    products.append({
                        "product_type": ingredient,
                        "reason": f"Recommended for {concern.replace('_', ' ')} in {location.state_code}",
                        "climate_relevance": concern,
                        "search_query": f"best {ingredient} {product_category}",
                        "affiliate_network": "amazon",
                    })
        
        return products


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Master Platform: GPS Personalization Engine — Demo")
    print("=" * 50)
    
    engine = GPSPersonalizationEngine()
    
    # Set location to Denver, Colorado
    location = engine.set_location_manual("Denver", "CO", "80202")
    print(f"\nLocation: {location.city}, {location.state_code}")
    
    # Get climate context
    climate = engine.get_climate_context(location)
    print(f"\nClimate Context:")
    print(f"  Season: {climate.season}")
    print(f"  Humidity: {climate.humidity_percent}%")
    print(f"  UV Index: {climate.uv_index}")
    print(f"  Temperature: {climate.temperature_f}°F")
    print(f"  Altitude: {climate.altitude_ft}ft")
    print(f"  Concerns: {', '.join(climate.concerns)}")
    
    # Get skincare routine
    routine = engine.get_skincare_routine(location, skin_type="dry")
    print(f"\nMorning Routine ({len(routine['morning'])} steps):")
    for step in routine["morning"]:
        print(f"  {step['step']}. {step['product']} — {step['note']}")
    
    # Travel mode
    print("\nTravel Mode: Denver → Miami")
    travel_kit = engine.get_travel_skincare_kit(location, "FL", "dry")
    print(f"  Climate shift: {travel_kit['climate_shift']}")
    print(f"  Must pack: {', '.join(travel_kit['must_pack'][:3])}")
    print(f"  Tips: {travel_kit['transition_tips'][0] if travel_kit['transition_tips'] else 'N/A'}")
