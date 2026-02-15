"""
Project Face: FastAPI Backend
AI-powered skin analysis and product recommendations.
Author: Audrey Evans
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from analysis_engine import SkinAnalysisEngine
from recommendations import RecommendationEngine

app = FastAPI(title="Project Face API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engines
skin_analyzer = SkinAnalysisEngine()
recommender = RecommendationEngine()


class AnalysisRequest(BaseModel):
    image_url: Optional[str] = None
    location: Optional[str] = None
    concerns: List[str] = []


class AnalysisResponse(BaseModel):
    skin_type: str
    conditions: List[Dict]
    recommendations: List[Dict]
    disclaimer: str


@app.get("/")
async def root():
    return {
        "message": "Project Face API",
        "version": "1.0.0",
        "endpoints": ["/analyze", "/recommend", "/weather-routine"]
    }


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_skin(file: UploadFile = File(...)):
    """Analyze uploaded skin image."""
    try:
        # Save uploaded file temporarily
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(await file.read())
        
        # Analyze image
        analysis = await skin_analyzer.analyze_image(temp_path)
        
        # Get recommendations
        recommendations = recommender.get_recommendations(
            skin_type=analysis.get("skin_type"),
            conditions=analysis.get("conditions", [])
        )
        
        return AnalysisResponse(
            skin_type=analysis.get("skin_type", "unknown"),
            conditions=analysis.get("conditions", []),
            recommendations=recommendations,
            disclaimer="This is an AI-powered analysis. Consult a dermatologist for medical advice."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/recommend/{skin_type}")
async def get_recommendations(skin_type: str, budget: str = "all"):
    """Get product recommendations for a skin type."""
    recommendations = recommender.get_recommendations(
        skin_type=skin_type,
        budget=budget
    )
    return {"recommendations": recommendations}


@app.get("/weather-routine")
async def get_weather_routine(location: str):
    """Get daily skincare routine based on weather."""
    # This would integrate with daily_weather_skincare.py
    return {
        "location": location,
        "routine": "Weather-based routine (to be implemented)",
        "note": "Integrate with daily_weather_skincare module"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
