"""
Master Platform: Daily Weather-Based Skincare Engine
=====================================================
Real-time weather integration for daily skincare routine adjustments.
Pulls live weather data (temp, humidity, wind, UV, precipitation).
Handles rapid Colorado-style weather swings within the same day.
Cross-references user symptom input with weather data.

Author: Audrey Evans

DISCLAIMER: This module is for informational purposes only. It is not a
substitute for professional medical advice, diagnosis, or treatment. Always
consult a dermatologist or healthcare provider for skin concerns.
"""

import json
import os
import requests
from pathlib import Path
from typing import List, Dict, Optional, Any, Literal, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone, timedelta

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# OpenWeatherMap API (free tier: 1,000 calls/day)
OWM_API_KEY = os.environ.get("OPENWEATHERMAP_API_KEY", "")
OWM_CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
OWM_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
OWM_UV_URL = "https://api.openweathermap.org/data/2.5/uvi"

# Open-Meteo API (free, no key required, unlimited)
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

DATA_DIR = Path(__file__).parent / "data" / "daily_weather"

# Skin symptom mappings
SYMPTOM_WEATHER_CORRELATIONS = {
    "dry": {
        "weather_triggers": ["low_humidity", "wind", "cold", "indoor_heating"],
        "immediate_actions": [
            "Apply hyaluronic acid serum to DAMP skin (mist face first)",
            "Layer a heavy occlusive moisturizer (CeraVe Moisturizing Cream, Aquaphor)",
            "Skip any exfoliants today",
            "Use a humidifier if indoors",
            "Drink extra water — dehydration shows on skin first",
        ],
        "products": {
            "drugstore": ["CeraVe Moisturizing Cream ($16)", "Aquaphor Healing Ointment ($12)", "Neutrogena Hydro Boost ($20)"],
            "mid_range": ["La Roche-Posay Cicaplast Baume B5 ($17)", "First Aid Beauty Ultra Repair Cream ($38)"],
            "luxury": ["Dr. Jart+ Ceramidin Cream ($48)", "Tatcha Dewy Skin Cream ($69)"],
        },
        "prescription_option": "Ask your doctor about Urea 20% cream — prescription-strength for extreme dryness",
    },
    "oily": {
        "weather_triggers": ["high_humidity", "heat", "sweat"],
        "immediate_actions": [
            "Switch to gel or water-based moisturizer",
            "Use niacinamide serum to control oil production",
            "Blotting papers throughout the day",
            "Double cleanse tonight to prevent clogged pores",
            "Use oil-free SPF — reapply with powder sunscreen",
        ],
        "products": {
            "drugstore": ["Neutrogena Oil-Free Moisturizer ($12)", "Clean & Clear Blotting Sheets ($5)", "CeraVe Foaming Cleanser ($15)"],
            "mid_range": ["Paula's Choice Niacinamide Booster ($24)", "Tatcha Blotting Papers ($12)"],
            "luxury": ["SkinCeuticals Silymarin CF ($166)", "Drunk Elephant B-Hydra Serum ($48)"],
        },
        "prescription_option": "For persistent oiliness, ask about spironolactone (hormonal) or tretinoin (pore-minimizing)",
    },
    "irritated": {
        "weather_triggers": ["wind", "extreme_cold", "extreme_heat", "dry_air", "pollution"],
        "immediate_actions": [
            "STOP all actives (retinol, AHA/BHA, vitamin C) until irritation subsides",
            "Use only gentle cleanser and barrier repair cream",
            "Apply centella asiatica (cica) or colloidal oatmeal products",
            "Avoid hot water on face — lukewarm only",
            "If redness persists 3+ days, see a dermatologist",
        ],
        "products": {
            "drugstore": ["Aveeno Calm + Restore Oat Gel ($18)", "Vanicream Gentle Cleanser ($9)", "CeraVe Healing Ointment ($12)"],
            "mid_range": ["La Roche-Posay Cicaplast Baume B5 ($17)", "Dr. Jart+ Cicapair ($52)"],
            "luxury": ["Avene Cicalfate+ Restorative Cream ($28)", "Biossance Squalane + Omega Repair Cream ($58)"],
        },
        "prescription_option": "If irritation is severe, ask about tacrolimus ointment or azelaic acid gel",
    },
    "flaky": {
        "weather_triggers": ["low_humidity", "wind", "cold", "altitude"],
        "immediate_actions": [
            "Gentle chemical exfoliant ONCE (lactic acid, not scrubs)",
            "Apply thick moisturizer immediately after cleansing on damp skin",
            "Seal with facial oil or occlusive",
            "Avoid makeup over flaky areas — it makes it worse",
            "Consider a hydrating overnight mask tonight",
        ],
        "products": {
            "drugstore": ["The Ordinary Lactic Acid 5% ($7)", "CeraVe SA Smoothing Cream ($18)", "Aquaphor ($12)"],
            "mid_range": ["Paula's Choice 8% AHA Gel ($30)", "Farmacy Honey Potion Mask ($38)"],
            "luxury": ["Drunk Elephant T.L.C. Sukari Babyfacial ($80)", "SK-II Facial Treatment Mask ($95)"],
        },
        "prescription_option": "Urea 20-40% cream (prescription) dissolves flakes without irritation. Ask your doctor.",
    },
    "tight": {
        "weather_triggers": ["low_humidity", "wind", "over_cleansing", "hot_water"],
        "immediate_actions": [
            "Your moisture barrier is compromised — focus on repair",
            "Switch to cream/milk cleanser (no foaming)",
            "Apply ceramide-rich moisturizer within 60 seconds of washing",
            "Add facial oil as final step to lock in moisture",
            "Avoid retinol and exfoliants until tightness resolves",
        ],
        "products": {
            "drugstore": ["CeraVe Hydrating Cleanser ($15)", "Vanicream Moisturizing Cream ($13)", "The Ordinary Natural Moisturizing Factors ($8)"],
            "mid_range": ["Krave Beauty Great Barrier Relief ($28)", "Stratia Liquid Gold ($27)"],
            "luxury": ["Dr. Jart+ Ceramidin Liquid ($39)", "Laneige Water Sleeping Mask ($29)"],
        },
        "prescription_option": "If tightness is chronic, ask about prescription ceramide creams or hyaluronic acid injections",
    },
    "burning": {
        "weather_triggers": ["sun_exposure", "wind_burn", "allergic_reaction", "product_reaction"],
        "immediate_actions": [
            "STOP all products except gentle cleanser and plain moisturizer",
            "Apply cold compress (not ice directly)",
            "Aloe vera gel (pure, no fragrance) can soothe",
            "If burning is severe or spreading, see a doctor TODAY",
            "Take an antihistamine if allergic reaction suspected",
        ],
        "products": {
            "drugstore": ["Pure Aloe Vera Gel ($8)", "Aveeno Eczema Therapy ($12)", "Hydrocortisone 1% (short-term only) ($6)"],
            "mid_range": ["La Roche-Posay Toleriane Ultra ($30)", "Avene Thermal Spring Water Spray ($14)"],
            "luxury": ["Avene Cicalfate+ ($28)", "Biossance Squalane + Vitamin C Rose Oil ($72)"],
        },
        "prescription_option": "Burning skin may indicate contact dermatitis or rosacea. See a dermatologist for proper diagnosis.",
    },
    "breakout": {
        "weather_triggers": ["humidity", "sweat", "mask_wearing", "stress", "hormonal"],
        "immediate_actions": [
            "Don't pick or squeeze — causes scarring and spreads bacteria",
            "Spot treat with benzoyl peroxide 2.5% or salicylic acid",
            "Change pillowcase tonight",
            "Double cleanse if wearing sunscreen or makeup",
            "Check if new products introduced in last 2 weeks — could be purging or reaction",
        ],
        "products": {
            "drugstore": ["Differin Gel (adapalene 0.1%) ($13)", "La Roche-Posay Effaclar Duo ($30)", "CeraVe Acne Foaming Cleanser ($15)"],
            "mid_range": ["Paula's Choice 2% BHA Liquid ($30)", "The Ordinary Niacinamide 10% ($6)"],
            "luxury": ["SkinCeuticals Blemish + Age Defense ($92)", "Sunday Riley Good Genes ($85)"],
        },
        "prescription_option": "Tretinoin (Retin-A) is the gold standard for acne. Ask your doctor — it's often covered by insurance.",
    },
}


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

@dataclass
class WeatherData:
    """Real-time weather data for a location."""
    location: str
    timestamp: str
    temperature_f: float
    feels_like_f: float
    humidity_percent: int
    wind_speed_mph: float
    wind_gust_mph: Optional[float] = None
    uv_index: float = 0.0
    precipitation_type: Optional[str] = None  # rain, snow, sleet, none
    precipitation_inches: float = 0.0
    cloud_cover_percent: int = 0
    air_quality_index: Optional[int] = None
    dew_point_f: Optional[float] = None
    visibility_miles: Optional[float] = None
    weather_description: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class DailyRoutine:
    """A personalized daily skincare routine based on weather and symptoms."""
    date: str
    location: str
    weather: WeatherData
    user_symptoms: List[str]
    morning_routine: List[Dict[str, str]]
    evening_routine: List[Dict[str, str]]
    midday_adjustments: List[str]
    weather_alerts: List[str]
    product_recommendations: Dict[str, List[str]]
    prescription_tips: List[str]
    disclaimer: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class WeatherForecastEntry:
    """A single forecast entry (3-hour or daily)."""
    timestamp: str
    temperature_f: float
    humidity_percent: int
    wind_speed_mph: float
    uv_index: float
    precipitation_type: Optional[str]
    weather_description: str

    def to_dict(self) -> dict:
        return asdict(self)


# ---------------------------------------------------------------------------
# Daily Weather Skincare Engine
# ---------------------------------------------------------------------------

MEDICAL_DISCLAIMER = (
    "DISCLAIMER: This is for informational purposes only. It is NOT a substitute "
    "for professional medical advice, diagnosis, or treatment. Always consult a "
    "dermatologist or healthcare provider for skin concerns. Product recommendations "
    "may include affiliate links."
)


class DailyWeatherSkincareEngine:
    """
    Real-time weather-based skincare recommendations.
    Pulls live weather data and cross-references with user symptoms.
    Handles rapid weather changes (Colorado-style same-day swings).
    """

    def __init__(self):
        self.data_dir = DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)

    # ---- Weather data fetching ----

    def fetch_weather_open_meteo(self, latitude: float, longitude: float) -> Optional[WeatherData]:
        """
        Fetch current weather from Open-Meteo API (free, no key required).
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
        
        Returns:
            WeatherData object or None on error
        """
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,snowfall,cloud_cover,wind_speed_10m,wind_gusts_10m,uv_index",
            "temperature_unit": "fahrenheit",
            "wind_speed_unit": "mph",
            "precipitation_unit": "inch",
            "timezone": "auto",
        }
        
        try:
            response = requests.get(OPEN_METEO_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"Open-Meteo API error: {e}")
            return None
        
        current = data.get("current", {})
        
        # Determine precipitation type
        precip_type = None
        if current.get("snowfall", 0) > 0:
            precip_type = "snow"
        elif current.get("rain", 0) > 0:
            precip_type = "rain"
        elif current.get("precipitation", 0) > 0:
            precip_type = "mixed"
        
        return WeatherData(
            location=f"{latitude}, {longitude}",
            timestamp=current.get("time", datetime.now(timezone.utc).isoformat()),
            temperature_f=current.get("temperature_2m", 70),
            feels_like_f=current.get("apparent_temperature", 70),
            humidity_percent=current.get("relative_humidity_2m", 50),
            wind_speed_mph=current.get("wind_speed_10m", 0),
            wind_gust_mph=current.get("wind_gusts_10m"),
            uv_index=current.get("uv_index", 0),
            precipitation_type=precip_type,
            precipitation_inches=current.get("precipitation", 0),
            cloud_cover_percent=current.get("cloud_cover", 0),
            weather_description=self._describe_weather(current),
        )

    def fetch_forecast_open_meteo(self, latitude: float, longitude: float, hours: int = 24) -> List[WeatherForecastEntry]:
        """Fetch hourly forecast from Open-Meteo."""
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m,uv_index,precipitation,snowfall",
            "temperature_unit": "fahrenheit",
            "wind_speed_unit": "mph",
            "precipitation_unit": "inch",
            "timezone": "auto",
            "forecast_hours": hours,
        }
        
        try:
            response = requests.get(OPEN_METEO_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"Open-Meteo forecast error: {e}")
            return []
        
        hourly = data.get("hourly", {})
        times = hourly.get("time", [])
        entries = []
        
        for i, time_str in enumerate(times[:hours]):
            precip_type = None
            if hourly.get("snowfall", [0])[i] > 0:
                precip_type = "snow"
            elif hourly.get("precipitation", [0])[i] > 0:
                precip_type = "rain"
            
            entries.append(WeatherForecastEntry(
                timestamp=time_str,
                temperature_f=hourly.get("temperature_2m", [70])[i],
                humidity_percent=hourly.get("relative_humidity_2m", [50])[i],
                wind_speed_mph=hourly.get("wind_speed_10m", [0])[i],
                uv_index=hourly.get("uv_index", [0])[i],
                precipitation_type=precip_type,
                weather_description="",
            ))
        
        return entries

    def _describe_weather(self, current: dict) -> str:
        """Generate a human-readable weather description."""
        parts = []
        temp = current.get("temperature_2m", 70)
        humidity = current.get("relative_humidity_2m", 50)
        wind = current.get("wind_speed_10m", 0)
        
        if temp < 20:
            parts.append("Extremely cold")
        elif temp < 40:
            parts.append("Cold")
        elif temp < 60:
            parts.append("Cool")
        elif temp < 80:
            parts.append("Warm")
        elif temp < 95:
            parts.append("Hot")
        else:
            parts.append("Extremely hot")
        
        if humidity < 20:
            parts.append("very dry air")
        elif humidity < 40:
            parts.append("dry")
        elif humidity > 80:
            parts.append("very humid")
        elif humidity > 60:
            parts.append("humid")
        
        if wind > 30:
            parts.append("strong winds")
        elif wind > 15:
            parts.append("windy")
        
        if current.get("snowfall", 0) > 0:
            parts.append("snowing")
        elif current.get("rain", 0) > 0:
            parts.append("raining")
        
        return ", ".join(parts)

    # ---- Symptom analysis ----

    def analyze_symptoms(
        self,
        symptoms: List[str],
        weather: WeatherData,
    ) -> Dict[str, Any]:
        """
        Cross-reference user symptoms with current weather to generate recommendations.
        
        Args:
            symptoms: User-reported symptoms (dry, oily, irritated, flaky, tight, burning, breakout)
            weather: Current weather data
        
        Returns:
            Analysis with weather correlation and recommendations
        """
        analysis = {
            "symptoms": symptoms,
            "weather_summary": weather.weather_description,
            "correlations": [],
            "immediate_actions": [],
            "product_recommendations": {"drugstore": [], "mid_range": [], "luxury": []},
            "prescription_tips": [],
            "weather_factors": [],
            "disclaimer": MEDICAL_DISCLAIMER,
        }
        
        # Identify weather factors
        if weather.humidity_percent < 25:
            analysis["weather_factors"].append("Very low humidity — skin loses moisture rapidly")
        if weather.wind_speed_mph > 15:
            analysis["weather_factors"].append(f"Wind at {weather.wind_speed_mph}mph — damages moisture barrier")
        if weather.temperature_f < 32:
            analysis["weather_factors"].append("Below freezing — cold damages skin barrier")
        if weather.temperature_f > 90:
            analysis["weather_factors"].append("Extreme heat — increased oil production and sweat")
        if weather.uv_index > 6:
            analysis["weather_factors"].append(f"High UV index ({weather.uv_index}) — sun damage risk")
        if weather.precipitation_type == "snow":
            analysis["weather_factors"].append("Snow reflects UV — double sun exposure risk")
        
        # Process each symptom
        for symptom in symptoms:
            symptom_lower = symptom.lower().strip()
            if symptom_lower in SYMPTOM_WEATHER_CORRELATIONS:
                symptom_data = SYMPTOM_WEATHER_CORRELATIONS[symptom_lower]
                
                # Check weather correlation
                correlation_found = False
                for trigger in symptom_data["weather_triggers"]:
                    if self._check_weather_trigger(trigger, weather):
                        analysis["correlations"].append({
                            "symptom": symptom_lower,
                            "weather_trigger": trigger,
                            "explanation": f"Your '{symptom_lower}' skin is likely caused by {trigger.replace('_', ' ')} (current conditions: {weather.weather_description})",
                        })
                        correlation_found = True
                
                if not correlation_found:
                    analysis["correlations"].append({
                        "symptom": symptom_lower,
                        "weather_trigger": "none_detected",
                        "explanation": f"Your '{symptom_lower}' skin may not be weather-related. Consider diet, stress, hormones, or product reactions.",
                    })
                
                # Add actions and products
                analysis["immediate_actions"].extend(symptom_data["immediate_actions"])
                for tier, products in symptom_data["products"].items():
                    analysis["product_recommendations"][tier].extend(products)
                
                if symptom_data.get("prescription_option"):
                    analysis["prescription_tips"].append(symptom_data["prescription_option"])
        
        # Deduplicate
        analysis["immediate_actions"] = list(dict.fromkeys(analysis["immediate_actions"]))
        for tier in analysis["product_recommendations"]:
            analysis["product_recommendations"][tier] = list(dict.fromkeys(analysis["product_recommendations"][tier]))
        analysis["prescription_tips"] = list(dict.fromkeys(analysis["prescription_tips"]))
        
        return analysis

    def _check_weather_trigger(self, trigger: str, weather: WeatherData) -> bool:
        """Check if a weather trigger matches current conditions."""
        trigger_checks = {
            "low_humidity": weather.humidity_percent < 30,
            "high_humidity": weather.humidity_percent > 70,
            "wind": weather.wind_speed_mph > 15,
            "cold": weather.temperature_f < 40,
            "extreme_cold": weather.temperature_f < 20,
            "heat": weather.temperature_f > 85,
            "extreme_heat": weather.temperature_f > 95,
            "indoor_heating": weather.temperature_f < 40,  # Proxy: if cold outside, heating is on
            "sun_exposure": weather.uv_index > 6,
            "humidity": weather.humidity_percent > 60,
            "sweat": weather.temperature_f > 80 and weather.humidity_percent > 60,
            "dry_air": weather.humidity_percent < 25,
            "pollution": (weather.air_quality_index or 0) > 100,
            "wind_burn": weather.wind_speed_mph > 20 and weather.temperature_f < 40,
            "altitude": True,  # Would check actual altitude
        }
        return trigger_checks.get(trigger, False)

    # ---- Daily routine generation ----

    def generate_daily_routine(
        self,
        weather: WeatherData,
        forecast: List[WeatherForecastEntry],
        skin_type: str = "normal",
        symptoms: Optional[List[str]] = None,
    ) -> DailyRoutine:
        """
        Generate a complete daily skincare routine based on weather and symptoms.
        
        Args:
            weather: Current weather data
            forecast: Hourly forecast for the day
            skin_type: User's skin type
            symptoms: User-reported symptoms (optional)
        
        Returns:
            Complete DailyRoutine object
        """
        symptoms = symptoms or []
        
        # Analyze symptoms against weather
        symptom_analysis = self.analyze_symptoms(symptoms, weather) if symptoms else None
        
        # Detect rapid weather changes (Colorado-style)
        weather_swing = self._detect_weather_swing(forecast)
        
        # Build morning routine
        morning = self._build_morning_routine(weather, skin_type, symptoms)
        
        # Build evening routine (based on forecast for end of day)
        evening_weather = forecast[-1] if forecast else None
        evening = self._build_evening_routine(weather, evening_weather, skin_type, symptoms)
        
        # Midday adjustments
        midday = self._build_midday_adjustments(weather, forecast, skin_type)
        
        # Weather alerts
        alerts = self._generate_weather_alerts(weather, forecast, weather_swing)
        
        # Product recommendations
        products = {"drugstore": [], "mid_range": [], "luxury": []}
        if symptom_analysis:
            products = symptom_analysis["product_recommendations"]
        
        # Prescription tips
        rx_tips = symptom_analysis["prescription_tips"] if symptom_analysis else []
        
        return DailyRoutine(
            date=datetime.now().strftime("%Y-%m-%d"),
            location=weather.location,
            weather=weather,
            user_symptoms=symptoms,
            morning_routine=morning,
            evening_routine=evening,
            midday_adjustments=midday,
            weather_alerts=alerts,
            product_recommendations=products,
            prescription_tips=rx_tips,
            disclaimer=MEDICAL_DISCLAIMER,
        )

    def _build_morning_routine(
        self,
        weather: WeatherData,
        skin_type: str,
        symptoms: List[str],
    ) -> List[Dict[str, str]]:
        """Build morning routine based on current weather."""
        routine = []
        
        # Step 1: Cleanser
        if weather.humidity_percent < 30 or "dry" in symptoms or "tight" in symptoms:
            routine.append({"step": "1", "product": "Cream/Milk Cleanser", "reason": f"Gentle for dry conditions ({weather.humidity_percent}% humidity)"})
        elif weather.humidity_percent > 70 or "oily" in symptoms:
            routine.append({"step": "1", "product": "Gel Cleanser", "reason": f"Controls oil in humid conditions ({weather.humidity_percent}% humidity)"})
        else:
            routine.append({"step": "1", "product": "Gentle Gel Cleanser", "reason": "Balanced cleansing"})
        
        # Step 2: Toner
        if weather.humidity_percent < 30:
            routine.append({"step": "2", "product": "Hydrating Toner (alcohol-free)", "reason": "Prep skin for moisture in dry air"})
        else:
            routine.append({"step": "2", "product": "Balancing Toner", "reason": "Prep and balance skin pH"})
        
        # Step 3: Treatment
        if "irritated" in symptoms or "burning" in symptoms:
            routine.append({"step": "3", "product": "Centella/Cica Serum", "reason": "Soothe irritation — skip actives today"})
        elif weather.uv_index > 5:
            routine.append({"step": "3", "product": "Vitamin C Serum", "reason": f"Antioxidant protection (UV index: {weather.uv_index})"})
        else:
            routine.append({"step": "3", "product": "Niacinamide Serum", "reason": "Brightening and barrier support"})
        
        # Step 4: Hydration (if dry conditions)
        if weather.humidity_percent < 35:
            routine.append({"step": "4", "product": "Hyaluronic Acid (on DAMP skin)", "reason": f"Critical — {weather.humidity_percent}% humidity pulls moisture FROM skin if applied dry"})
        
        # Step 5: Moisturizer
        step_num = str(len(routine) + 1)
        if weather.humidity_percent < 25 or weather.temperature_f < 30:
            routine.append({"step": step_num, "product": "Heavy Occlusive Moisturizer", "reason": f"Seal in moisture — {weather.temperature_f}°F, {weather.humidity_percent}% humidity"})
        elif weather.humidity_percent > 70:
            routine.append({"step": step_num, "product": "Lightweight Gel Moisturizer", "reason": f"Won't clog pores in {weather.humidity_percent}% humidity"})
        else:
            routine.append({"step": step_num, "product": "Lotion Moisturizer", "reason": "Balanced hydration"})
        
        # Step 6: Sunscreen (ALWAYS)
        step_num = str(len(routine) + 1)
        if weather.uv_index > 7:
            routine.append({"step": step_num, "product": "SPF 50+ Mineral Sunscreen", "reason": f"HIGH UV ({weather.uv_index}) — reapply every 90 min outdoors"})
        elif weather.uv_index > 3:
            routine.append({"step": step_num, "product": "SPF 50 Sunscreen", "reason": f"UV index {weather.uv_index} — reapply every 2 hours"})
        elif weather.precipitation_type == "snow":
            routine.append({"step": step_num, "product": "SPF 50 Sunscreen", "reason": "Snow reflects 80% of UV rays — sunscreen essential even on cloudy days"})
        else:
            routine.append({"step": step_num, "product": "SPF 30+ Sunscreen", "reason": "Daily protection — UV penetrates clouds"})
        
        # Wind protection
        if weather.wind_speed_mph > 20:
            step_num = str(len(routine) + 1)
            routine.append({"step": step_num, "product": "Wind Barrier Balm (lips + exposed skin)", "reason": f"Wind at {weather.wind_speed_mph}mph — protect exposed skin"})
        
        return routine

    def _build_evening_routine(
        self,
        morning_weather: WeatherData,
        evening_forecast: Optional[WeatherForecastEntry],
        skin_type: str,
        symptoms: List[str],
    ) -> List[Dict[str, str]]:
        """Build evening routine."""
        routine = [
            {"step": "1", "product": "Oil Cleanser / Micellar Water", "reason": "Remove sunscreen, makeup, pollution, and sweat"},
            {"step": "2", "product": "Gentle Water-Based Cleanser", "reason": "Second cleanse for truly clean skin"},
        ]
        
        # Treatment based on symptoms
        if "irritated" in symptoms or "burning" in symptoms:
            routine.append({"step": "3", "product": "Barrier Repair Serum (ceramides)", "reason": "Repair damaged moisture barrier overnight"})
        elif "breakout" in symptoms:
            routine.append({"step": "3", "product": "Salicylic Acid or Benzoyl Peroxide (spot treat)", "reason": "Target active breakouts"})
        elif "flaky" in symptoms:
            routine.append({"step": "3", "product": "Gentle AHA (lactic acid 5%)", "reason": "Dissolve flakes without irritation"})
        else:
            routine.append({"step": "3", "product": "Retinol (2-3x/week) or Niacinamide", "reason": "Anti-aging and skin renewal"})
        
        # Hydration
        if morning_weather.humidity_percent < 35:
            routine.append({"step": "4", "product": "Hyaluronic Acid Serum", "reason": "Extra hydration for dry climate"})
            routine.append({"step": "5", "product": "Facial Oil (squalane or rosehip)", "reason": "Seal in all moisture overnight"})
        
        step_num = str(len(routine) + 1)
        routine.append({"step": step_num, "product": "Night Cream / Sleeping Mask", "reason": "Deep repair and restoration while sleeping"})
        
        return routine

    def _build_midday_adjustments(
        self,
        weather: WeatherData,
        forecast: List[WeatherForecastEntry],
        skin_type: str,
    ) -> List[str]:
        """Build midday adjustment recommendations."""
        adjustments = []
        
        if weather.uv_index > 5:
            adjustments.append(f"Reapply sunscreen now (UV index: {weather.uv_index})")
        
        if weather.humidity_percent < 25:
            adjustments.append("Mist face with hydrating spray — dry air is pulling moisture from your skin")
        
        if weather.temperature_f > 85:
            adjustments.append("Blot excess oil — heat increases sebum production")
        
        # Check for weather swing
        swing = self._detect_weather_swing(forecast)
        if swing:
            adjustments.append(f"WEATHER CHANGE ALERT: {swing}")
        
        return adjustments

    def _detect_weather_swing(self, forecast: List[WeatherForecastEntry]) -> Optional[str]:
        """Detect rapid weather changes within the day (Colorado-style)."""
        if len(forecast) < 6:
            return None
        
        # Check for temperature swings > 30°F within 12 hours
        temps = [f.temperature_f for f in forecast[:12]]
        if temps:
            temp_range = max(temps) - min(temps)
            if temp_range > 30:
                return (
                    f"Temperature swinging {temp_range:.0f}°F today "
                    f"(from {min(temps):.0f}°F to {max(temps):.0f}°F). "
                    "Carry both lightweight and heavy moisturizer. "
                    "Adjust routine based on conditions when you step outside."
                )
        
        # Check for precipitation changes
        precip_types = set(f.precipitation_type for f in forecast[:12] if f.precipitation_type)
        if "snow" in precip_types and any(f.temperature_f > 60 for f in forecast[:12]):
            return (
                "Classic Colorado weather: warm temps AND snow in the same day. "
                "Morning may need heavy protection, afternoon may need lighter products. "
                "Keep both options in your bag."
            )
        
        return None

    def _generate_weather_alerts(
        self,
        weather: WeatherData,
        forecast: List[WeatherForecastEntry],
        swing: Optional[str],
    ) -> List[str]:
        """Generate weather-related skin alerts."""
        alerts = []
        
        if weather.uv_index >= 8:
            alerts.append(f"VERY HIGH UV ({weather.uv_index}): Limit sun exposure 10am-4pm. Wear hat + sunscreen.")
        
        if weather.humidity_percent < 15:
            alerts.append(f"EXTREME DRY AIR ({weather.humidity_percent}%): Your skin is losing moisture rapidly. Use humidifier indoors.")
        
        if weather.wind_speed_mph > 30:
            alerts.append(f"HIGH WIND ({weather.wind_speed_mph}mph): Wind strips moisture barrier. Apply barrier balm before going out.")
        
        if weather.temperature_f < 10:
            alerts.append(f"EXTREME COLD ({weather.temperature_f}°F): Risk of frostbite on exposed skin. Cover face.")
        
        if weather.temperature_f > 100:
            alerts.append(f"EXTREME HEAT ({weather.temperature_f}°F): Stay hydrated. Heat rash risk. Use lightweight products only.")
        
        if weather.precipitation_type == "snow":
            alerts.append("SNOW: UV reflection from snow increases sun exposure by up to 80%. Wear sunscreen even on cloudy days.")
        
        if swing:
            alerts.append(f"RAPID WEATHER CHANGE: {swing}")
        
        return alerts

    # ---- Convenience methods ----

    def get_today_routine(
        self,
        latitude: float,
        longitude: float,
        skin_type: str = "normal",
        symptoms: Optional[List[str]] = None,
        location_name: str = "",
    ) -> Dict[str, Any]:
        """
        One-call method: fetch weather + generate complete daily routine.
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
            skin_type: User's skin type
            symptoms: How the user's skin feels today
            location_name: Human-readable location name
        
        Returns:
            Complete daily routine as dict
        """
        # Fetch weather
        weather = self.fetch_weather_open_meteo(latitude, longitude)
        if not weather:
            return {"error": "Could not fetch weather data"}
        
        if location_name:
            weather.location = location_name
        
        # Fetch forecast
        forecast = self.fetch_forecast_open_meteo(latitude, longitude, hours=24)
        
        # Generate routine
        routine = self.generate_daily_routine(weather, forecast, skin_type, symptoms)
        
        result = routine.to_dict()
        
        # Add tomorrow preview
        if len(forecast) > 12:
            tomorrow_weather = forecast[12]  # ~12 hours from now
            result["tomorrow_preview"] = {
                "temperature_f": tomorrow_weather.temperature_f,
                "humidity_percent": tomorrow_weather.humidity_percent,
                "uv_index": tomorrow_weather.uv_index,
                "note": self._tomorrow_note(weather, tomorrow_weather),
            }
        
        return result

    def _tomorrow_note(self, today: WeatherData, tomorrow: WeatherForecastEntry) -> str:
        """Generate a note about tomorrow's conditions vs today."""
        notes = []
        temp_diff = tomorrow.temperature_f - today.temperature_f
        humidity_diff = tomorrow.humidity_percent - today.humidity_percent
        
        if abs(temp_diff) > 15:
            direction = "warmer" if temp_diff > 0 else "colder"
            notes.append(f"Tomorrow will be {abs(temp_diff):.0f}°F {direction}")
        
        if abs(humidity_diff) > 15:
            direction = "more humid" if humidity_diff > 0 else "drier"
            notes.append(f"and {abs(humidity_diff)}% {direction}")
        
        if notes:
            return " ".join(notes) + ". Adjust routine accordingly."
        return "Similar conditions expected tomorrow."


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Master Platform: Daily Weather Skincare Engine — Demo")
    print("=" * 55)
    
    engine = DailyWeatherSkincareEngine()
    
    # Wellington, CO coordinates
    lat, lon = 40.7036, -105.0086
    
    print(f"\nFetching weather for Wellington, CO ({lat}, {lon})...")
    weather = engine.fetch_weather_open_meteo(lat, lon)
    
    if weather:
        weather.location = "Wellington, CO"
        print(f"  Temperature: {weather.temperature_f}°F (feels like {weather.feels_like_f}°F)")
        print(f"  Humidity: {weather.humidity_percent}%")
        print(f"  Wind: {weather.wind_speed_mph}mph")
        print(f"  UV Index: {weather.uv_index}")
        print(f"  Conditions: {weather.weather_description}")
        
        # User says "I'm so dry today"
        print("\nUser input: 'I'm so dry and tight today'")
        analysis = engine.analyze_symptoms(["dry", "tight"], weather)
        
        print(f"\nWeather factors:")
        for factor in analysis["weather_factors"]:
            print(f"  - {factor}")
        
        print(f"\nCorrelations:")
        for corr in analysis["correlations"]:
            print(f"  - {corr['explanation']}")
        
        print(f"\nImmediate actions:")
        for action in analysis["immediate_actions"][:5]:
            print(f"  - {action}")
        
        print(f"\nPrescription tips:")
        for tip in analysis["prescription_tips"]:
            print(f"  - {tip}")
    
    print(f"\n{MEDICAL_DISCLAIMER}")
