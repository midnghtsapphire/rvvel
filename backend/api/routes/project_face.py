"""
Project Face — AI-Powered Skin Analysis Routes
The flagship product of GlowStarLabs.

Features:
- Upload photo → AI analyzes skin → personalized recommendations
- GPS-based personalization (Colorado dry vs California humid)
- Daily weather skincare adjustments
- Clinical trials finder (ClinicalTrials.gov API)
- Prescription awareness
- Hidden procedures education (PDO threads, etc.)
- Medical tourism (TJ Mexico, international)
- Permanent makeup + areola tattooing for mastectomy survivors
"""
import os
import base64
import uuid
from typing import Optional, List
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from pydantic import BaseModel

router = APIRouter(prefix="/api/skin", tags=["Project Face — Skin Analysis"])

MEDICAL_DISCLAIMER = (
    "DISCLAIMER: This application is for informational purposes only and is not a substitute "
    "for professional medical advice, diagnosis, or treatment. Always seek the advice of your "
    "physician or other qualified health care provider with any questions you may have regarding "
    "a medical condition."
)


# --- Request/Response Models ---

class SkinAnalysisRequest(BaseModel):
    concerns: List[str] = ["general"]
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    city: Optional[str] = None
    include_weather: bool = True
    include_trials: bool = False
    include_procedures: bool = False


class ProcedureSearchRequest(BaseModel):
    procedure: str
    location: str = ""
    budget_range: str = ""


class MedicalTourismRequest(BaseModel):
    procedure: str
    origin_city: str = ""
    destinations: List[str] = ["Tijuana, Mexico", "Bangkok, Thailand", "Seoul, South Korea"]


# --- Helper: Get services from app state ---

async def get_openrouter():
    from backend.integrations.openrouter_client import OpenRouterClient
    return OpenRouterClient()

async def get_weather():
    from backend.integrations.weather_client import WeatherClient
    return WeatherClient()

async def get_trials():
    from backend.integrations.clinical_trials_client import ClinicalTrialsClient
    return ClinicalTrialsClient()

async def get_perplexity():
    from backend.integrations.perplexity_client import PerplexityClient
    return PerplexityClient()


# --- Endpoints ---

@router.post("/analyze")
async def analyze_skin(
    file: UploadFile = File(...),
    concerns: str = Query("general", description="Comma-separated skin concerns"),
    latitude: Optional[float] = Query(None),
    longitude: Optional[float] = Query(None),
    city: Optional[str] = Query(None),
):
    """Upload a photo for AI skin analysis with GPS-based personalization."""
    # Read and encode image
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:  # 10MB limit
        raise HTTPException(status_code=413, detail="Image too large. Max 10MB.")

    image_b64 = base64.b64encode(contents).decode("utf-8")
    concern_list = [c.strip() for c in concerns.split(",")]

    # Get AI analysis
    ai_client = await get_openrouter()
    analysis = await ai_client.analyze_skin(image_b64, concern_list)

    # Get weather data if location provided
    weather_data = None
    if latitude and longitude:
        try:
            weather_client = await get_weather()
            weather_data = await weather_client.get_weather(latitude, longitude)
        except Exception:
            weather_data = None
    elif city:
        try:
            weather_client = await get_weather()
            weather_data = await weather_client.get_by_city(city)
        except Exception:
            weather_data = None

    # Build response
    ai_content = ""
    if analysis.get("choices"):
        ai_content = analysis["choices"][0].get("message", {}).get("content", "")

    return {
        "analysis_id": str(uuid.uuid4()),
        "skin_analysis": ai_content,
        "weather_personalization": weather_data,
        "concerns_addressed": concern_list,
        "model_used": analysis.get("model", "openai/gpt-4o"),
        "tokens_used": analysis.get("usage", {}).get("total_tokens", 0),
        "medical_disclaimer": MEDICAL_DISCLAIMER,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/weather-tips")
async def get_weather_skincare_tips(
    latitude: Optional[float] = Query(None),
    longitude: Optional[float] = Query(None),
    city: Optional[str] = Query(None),
):
    """Get daily weather-based skincare adjustments."""
    weather_client = await get_weather()

    if latitude and longitude:
        data = await weather_client.get_weather(latitude, longitude)
    elif city:
        data = await weather_client.get_by_city(city)
    else:
        raise HTTPException(status_code=400, detail="Provide latitude/longitude or city")

    return {
        "weather": data,
        "medical_disclaimer": MEDICAL_DISCLAIMER,
    }


@router.get("/clinical-trials")
async def search_clinical_trials(
    condition: str = Query("dermatology", description="Skin condition to search"),
    location: str = Query("", description="City or state"),
    max_results: int = Query(10, ge=1, le=50),
):
    """Search ClinicalTrials.gov for relevant dermatology trials."""
    trials_client = await get_trials()
    results = await trials_client.search_trials(condition, location, max_results=max_results)

    return {
        "trials": results,
        "total": len(results),
        "search_condition": condition,
        "search_location": location,
        "source": "ClinicalTrials.gov",
        "medical_disclaimer": MEDICAL_DISCLAIMER,
    }


@router.get("/clinical-trials/skin")
async def search_skin_trials(location: str = Query("", description="City or state")):
    """Search for all dermatology-related clinical trials."""
    trials_client = await get_trials()
    results = await trials_client.search_skin_trials(location)

    return {
        "trials": results,
        "total": len(results),
        "source": "ClinicalTrials.gov",
        "medical_disclaimer": MEDICAL_DISCLAIMER,
    }


@router.post("/procedures/research")
async def research_procedure(data: ProcedureSearchRequest):
    """Research a cosmetic/medical procedure with BBB ratings and reviews."""
    perplexity = await get_perplexity()
    result = await perplexity.search_procedures(data.procedure, data.location)

    content = ""
    if result.get("choices"):
        content = result["choices"][0].get("message", {}).get("content", "")

    return {
        "procedure": data.procedure,
        "research": content,
        "location": data.location,
        "medical_disclaimer": MEDICAL_DISCLAIMER,
    }


@router.get("/procedures/hidden")
async def hidden_procedures_education():
    """Educational content about lesser-known cosmetic procedures."""
    procedures = [
        {
            "name": "PDO Thread Lift",
            "description": "Minimally invasive procedure using dissolvable threads to lift and tighten skin.",
            "avg_cost": "$1,500 - $4,500",
            "recovery": "3-5 days",
            "duration": "1-3 years",
            "risks": ["Infection", "Thread migration", "Asymmetry", "Dimpling"],
            "what_they_dont_tell_you": "Results vary significantly. Some providers use inferior threads. Always verify provider credentials and ask about thread brand/origin.",
        },
        {
            "name": "Platelet-Rich Plasma (PRP) Facial",
            "description": "Uses your own blood platelets to stimulate collagen production.",
            "avg_cost": "$500 - $2,000 per session",
            "recovery": "1-3 days",
            "duration": "6-12 months",
            "risks": ["Bruising", "Infection", "Uneven results"],
            "what_they_dont_tell_you": "Multiple sessions needed. Results take weeks to appear. Not all PRP preparations are equal — ask about centrifuge type and platelet concentration.",
        },
        {
            "name": "Microneedling with RF",
            "description": "Combines microneedling with radiofrequency energy for deeper skin remodeling.",
            "avg_cost": "$1,000 - $3,500 per session",
            "recovery": "2-5 days",
            "duration": "1-2 years",
            "risks": ["Burns", "Scarring", "Hyperpigmentation"],
            "what_they_dont_tell_you": "Depth settings matter enormously. Improper settings can cause permanent scarring. Verify provider has specific RF microneedling training.",
        },
        {
            "name": "Permanent Makeup / Microblading",
            "description": "Semi-permanent tattooing for eyebrows, eyeliner, and lips.",
            "avg_cost": "$400 - $1,500",
            "recovery": "7-14 days",
            "duration": "1-3 years",
            "risks": ["Allergic reaction", "Infection", "Color migration", "Scarring"],
            "what_they_dont_tell_you": "Colors can shift over time (especially to orange/blue). MRI interactions possible with some pigments. Always ask about pigment ingredients.",
        },
        {
            "name": "Areola Tattooing (Post-Mastectomy)",
            "description": "3D areola tattooing to restore natural appearance after breast reconstruction.",
            "avg_cost": "$200 - $800 (often covered by insurance or offered free by nonprofits)",
            "recovery": "5-10 days",
            "duration": "3-5 years before touch-up",
            "risks": ["Infection", "Color fading", "Allergic reaction"],
            "what_they_dont_tell_you": "Many artists offer this service free or at reduced cost for survivors. Organizations like P.ink connect survivors with tattoo artists. This is a deeply personal and healing experience for many survivors.",
            "resources": ["P.ink (personalink.org)", "The Breast Cancer Recovery Foundation"],
        },
    ]

    return {
        "procedures": procedures,
        "total": len(procedures),
        "note": "This information is for educational purposes. Always consult a board-certified provider.",
        "medical_disclaimer": MEDICAL_DISCLAIMER,
    }


@router.post("/medical-tourism")
async def medical_tourism_research(data: MedicalTourismRequest):
    """Research medical tourism options for cosmetic procedures."""
    perplexity = await get_perplexity()

    query = (
        f"Research medical tourism for {data.procedure} procedure. "
        f"Compare costs, quality, and safety in: {', '.join(data.destinations)}. "
        f"Include: accredited facilities, surgeon credentials, patient reviews, "
        f"travel logistics, aftercare requirements, and risks of medical tourism."
    )

    result = await perplexity.research(query)
    content = ""
    if result.get("choices"):
        content = result["choices"][0].get("message", {}).get("content", "")

    return {
        "procedure": data.procedure,
        "destinations": data.destinations,
        "research": content,
        "safety_warning": (
            "Medical tourism carries additional risks including: limited legal recourse, "
            "communication barriers, different medical standards, and complications during travel. "
            "Always verify facility accreditation (JCI) and surgeon credentials."
        ),
        "medical_disclaimer": MEDICAL_DISCLAIMER,
    }


@router.get("/prescription-awareness")
async def prescription_awareness():
    """Information about prescription skincare and what to discuss with your doctor."""
    return {
        "categories": [
            {
                "name": "Retinoids",
                "examples": ["Tretinoin (Retin-A)", "Adapalene (Differin)", "Tazarotene"],
                "what_to_ask": "Ask about starting concentration, purging period, and sun sensitivity.",
            },
            {
                "name": "Antibiotics",
                "examples": ["Clindamycin", "Doxycycline", "Minocycline"],
                "what_to_ask": "Ask about antibiotic resistance, duration limits, and probiotic support.",
            },
            {
                "name": "Hormonal Treatments",
                "examples": ["Spironolactone", "Birth control pills", "Finasteride"],
                "what_to_ask": "Ask about hormonal side effects, blood work monitoring, and timeline.",
            },
            {
                "name": "Immunosuppressants",
                "examples": ["Tacrolimus", "Pimecrolimus", "Cyclosporine"],
                "what_to_ask": "Ask about long-term safety, sun exposure risks, and monitoring schedule.",
            },
        ],
        "general_tips": [
            "Always tell your dermatologist about ALL products you use, including OTC",
            "Ask about generic alternatives — often identical formulations at lower cost",
            "Request samples before committing to expensive prescriptions",
            "Ask about patient assistance programs if cost is a concern",
        ],
        "medical_disclaimer": MEDICAL_DISCLAIMER,
    }
