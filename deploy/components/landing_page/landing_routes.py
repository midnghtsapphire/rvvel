"""Landing Page Routes — Dynamic content for marketing pages."""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict


class LandingPageConfig(BaseModel):
    app_name: str = "Project Face"
    tagline: str = "Your skin, decoded by AI"
    hero_title: str = "AI-Powered Skin Analysis"
    hero_subtitle: str = "Upload a photo. Get personalized skincare recommendations powered by AI, GPS, and real-time weather data."
    features: List[Dict] = []
    pricing_tiers: List[Dict] = []
    testimonials: List[Dict] = []
    cta_text: str = "Start Free Analysis"
    cta_url: str = "/register"


DEFAULT_FEATURES = [
    {"icon": "sparkles", "title": "AI Skin Analysis", "description": "Upload a photo and get instant AI-powered skin analysis with personalized recommendations."},
    {"icon": "map-pin", "title": "GPS Personalization", "description": "Recommendations adapt to your location — dry Colorado air vs. humid California coast."},
    {"icon": "cloud-sun", "title": "Weather Skincare", "description": "Daily skincare adjustments based on real-time weather conditions in your area."},
    {"icon": "search", "title": "Clinical Trials Finder", "description": "Search ClinicalTrials.gov for relevant dermatology trials near you."},
    {"icon": "shield", "title": "Procedure Education", "description": "Learn about hidden procedures like PDO threads, with BBB ratings and reviews."},
    {"icon": "globe", "title": "Medical Tourism", "description": "Explore safe, affordable skincare procedures worldwide with verified providers."},
]

DEFAULT_PRICING = [
    {"name": "Free", "price": 0, "features": ["10 AI tokens/month", "Basic skin analysis", "Weather tips"], "cta": "Get Started"},
    {"name": "Starter", "price": 9, "features": ["100 AI tokens/month", "Full skin analysis", "Makeup advisor", "DIY recipes"], "cta": "Start Free Trial", "popular": False},
    {"name": "Pro", "price": 29, "features": ["500 AI tokens/month", "All features", "Clinical trials", "Priority support"], "cta": "Go Pro", "popular": True},
    {"name": "Business", "price": 99, "features": ["2,000 AI tokens/month", "API access", "White label", "Analytics dashboard"], "cta": "Contact Sales", "popular": False},
    {"name": "Enterprise", "price": 299, "features": ["10,000 AI tokens/month", "Dedicated support", "Custom integration", "SLA guarantee"], "cta": "Contact Sales", "popular": False},
]


def create_landing_router() -> APIRouter:
    router = APIRouter(prefix="/api/landing", tags=["Landing Page"])

    @router.get("/config")
    async def get_landing_config():
        return {
            "features": DEFAULT_FEATURES,
            "pricing": DEFAULT_PRICING,
            "hero": {
                "title": "AI-Powered Skin Analysis",
                "subtitle": "Upload a photo. Get personalized skincare recommendations powered by AI, GPS, and real-time weather data.",
                "cta_text": "Start Free Analysis",
                "cta_url": "/register",
            },
            "medical_disclaimer": "This application is for informational purposes only and is not a substitute for professional medical advice. Always consult a qualified healthcare provider.",
        }

    @router.get("/features")
    async def get_features():
        return DEFAULT_FEATURES

    @router.get("/pricing")
    async def get_pricing():
        return DEFAULT_PRICING

    return router
