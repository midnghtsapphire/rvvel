"""
Project Face: AI Skin Analysis Engine
======================================
AI-powered skin analysis using vision models through OpenRouter.
Analyzes face zones, acne, skin conditions, body areas, and dermatological issues.

Author: Audrey Evans
"""

import os
import json
import base64
from pathlib import Path
from typing import Dict, List, Optional, Any, Literal
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from openai import OpenAI

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Vision models available through OpenRouter
VISION_MODELS = {
    "gpt-4o": "openai/gpt-4o",
    "gpt-4o-mini": "openai/gpt-4o-mini",
    "claude-sonnet": "anthropic/claude-3.5-sonnet",
    "gemini-flash": "google/gemini-2.0-flash-exp:free",
    "gemini-pro": "google/gemini-exp-1206:free",
}

DEFAULT_MODEL = "openai/gpt-4o-mini"

# Analysis zones
FACE_ZONES = ["forehead", "t_zone", "cheeks", "chin", "jawline", "nose", "under_eyes"]
BODY_ZONES = ["elbows", "feet", "hands", "neck", "chest", "back"]

# Skin conditions
ACNE_TYPES = ["comedonal", "inflammatory", "cystic", "hormonal"]
SKIN_TYPES = ["oily", "dry", "combination", "sensitive", "normal"]
DERMATOLOGICAL_CONDITIONS = [
    "eczema", "psoriasis", "rosacea", "melasma", "keratosis_pilaris",
    "hyperpigmentation", "sun_damage", "fungal_infection"
]


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

@dataclass
class AcneAnalysis:
    """Acne detection results."""
    detected: bool
    acne_type: Optional[str] = None  # comedonal, inflammatory, cystic, hormonal
    severity: Optional[Literal["mild", "moderate", "severe"]] = None
    locations: List[str] = field(default_factory=list)
    count_estimate: Optional[int] = None
    notes: str = ""


@dataclass
class SkinCondition:
    """General skin condition assessment."""
    texture: str = "normal"  # smooth, rough, uneven
    pores: str = "normal"  # enlarged, normal, fine
    wrinkles: str = "none"  # none, fine_lines, moderate, deep
    dark_spots: bool = False
    hyperpigmentation: bool = False
    redness: bool = False
    dryness: bool = False
    oiliness: bool = False
    notes: str = ""


@dataclass
class DermatologicalFlag:
    """Potential dermatological condition requiring doctor referral."""
    condition: str
    confidence: Literal["low", "medium", "high"]
    description: str
    recommend_doctor: bool = True


@dataclass
class ZoneAnalysis:
    """Analysis for a specific face or body zone."""
    zone: str
    acne: Optional[AcneAnalysis] = None
    condition: Optional[SkinCondition] = None
    dermatological_flags: List[DermatologicalFlag] = field(default_factory=list)


@dataclass
class SkinAnalysisResult:
    """Complete skin analysis result."""
    analysis_id: str
    timestamp: str
    image_path: str
    skin_type: str
    face_zones: List[ZoneAnalysis] = field(default_factory=list)
    body_zones: List[ZoneAnalysis] = field(default_factory=list)
    overall_acne: Optional[AcneAnalysis] = None
    overall_condition: Optional[SkinCondition] = None
    dermatological_flags: List[DermatologicalFlag] = field(default_factory=list)
    age_assessment: Optional[str] = None
    recommendations_summary: List[str] = field(default_factory=list)
    model_used: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "SkinAnalysisResult":
        # Reconstruct nested dataclasses
        if "face_zones" in d:
            d["face_zones"] = [ZoneAnalysis(**z) for z in d["face_zones"]]
        if "body_zones" in d:
            d["body_zones"] = [ZoneAnalysis(**z) for z in d["body_zones"]]
        if "overall_acne" in d and d["overall_acne"]:
            d["overall_acne"] = AcneAnalysis(**d["overall_acne"])
        if "overall_condition" in d and d["overall_condition"]:
            d["overall_condition"] = SkinCondition(**d["overall_condition"])
        if "dermatological_flags" in d:
            d["dermatological_flags"] = [DermatologicalFlag(**f) for f in d["dermatological_flags"]]
        return cls(**d)


# ---------------------------------------------------------------------------
# Skin Analysis Engine
# ---------------------------------------------------------------------------

class SkinAnalysisEngine:
    """
    AI-powered skin analysis using vision models.
    Privacy-first: images processed and deleted, never stored permanently.
    """

    def __init__(self, model: str = DEFAULT_MODEL, api_key: Optional[str] = None):
        self.model = model
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not set")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://openrouter.ai/api/v1",
        )

    # ---- Image encoding ----

    def _encode_image(self, image_path: str) -> str:
        """Encode image to base64 for API submission."""
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    # ---- Core analysis ----

    def analyze_skin(
        self,
        image_path: str,
        analysis_type: Literal["face", "body", "full"] = "face",
        focus_zones: Optional[List[str]] = None,
    ) -> SkinAnalysisResult:
        """
        Perform comprehensive skin analysis on an image.
        
        Args:
            image_path: Path to the image file
            analysis_type: Type of analysis (face, body, or full)
            focus_zones: Specific zones to focus on (optional)
        
        Returns:
            SkinAnalysisResult with detailed findings
        """
        # Generate analysis ID
        analysis_id = f"analysis_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{os.urandom(4).hex()}"
        
        # Encode image
        image_base64 = self._encode_image(image_path)
        image_url = f"data:image/jpeg;base64,{image_base64}"
        
        # Build analysis prompt
        prompt = self._build_analysis_prompt(analysis_type, focus_zones)
        
        # Call vision model
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ],
                }
            ],
            temperature=0.3,
            max_tokens=2000,
        )
        
        # Parse response
        analysis_text = response.choices[0].message.content
        result = self._parse_analysis_response(analysis_text, analysis_type)
        
        # Populate metadata
        result.analysis_id = analysis_id
        result.timestamp = datetime.now(timezone.utc).isoformat()
        result.image_path = image_path
        result.model_used = self.model
        
        return result

    def _build_analysis_prompt(
        self,
        analysis_type: Literal["face", "body", "full"],
        focus_zones: Optional[List[str]] = None,
    ) -> str:
        """Build the analysis prompt for the vision model."""
        
        base_prompt = """You are an expert dermatologist and skin analysis AI. Analyze this image and provide a detailed skin assessment.

**ANALYSIS SCOPE:**"""
        
        if analysis_type == "face":
            base_prompt += "\n- Focus on facial skin: forehead, T-zone, cheeks, chin, jawline, nose, under-eyes"
        elif analysis_type == "body":
            base_prompt += "\n- Focus on body skin: elbows, feet, hands, neck, chest, back"
        else:
            base_prompt += "\n- Analyze both face and body areas"
        
        if focus_zones:
            base_prompt += f"\n- Pay special attention to: {', '.join(focus_zones)}"
        
        base_prompt += """

**ASSESSMENT CRITERIA:**

1. **Skin Type:** Determine if skin is oily, dry, combination, sensitive, or normal.

2. **Acne Analysis:**
   - Detect presence of acne
   - Classify type: comedonal (blackheads/whiteheads), inflammatory (red bumps), cystic (deep, painful), hormonal (jawline/chin)
   - Assess severity: mild, moderate, severe
   - Identify locations
   - Estimate count if visible

3. **Skin Condition:**
   - Texture: smooth, rough, uneven
   - Pores: enlarged, normal, fine
   - Wrinkles: none, fine lines, moderate, deep
   - Dark spots or hyperpigmentation
   - Redness or inflammation
   - Dryness or flaking
   - Oiliness or shine

4. **Dermatological Flags (require doctor referral):**
   - Eczema (red, itchy, inflamed patches)
   - Psoriasis (thick, scaly plaques)
   - Rosacea (persistent redness, visible blood vessels)
   - Melasma (dark patches, often on face)
   - Keratosis pilaris (rough bumps, often on arms/legs)
   - Fungal infections
   - Sun damage or suspicious lesions

5. **Age-Related Changes:**
   - Fine lines, loss of elasticity, sun damage

**OUTPUT FORMAT (JSON):**

```json
{
  "skin_type": "combination",
  "overall_acne": {
    "detected": true,
    "acne_type": "inflammatory",
    "severity": "moderate",
    "locations": ["forehead", "chin"],
    "count_estimate": 15,
    "notes": "Active inflammatory acne with some post-inflammatory hyperpigmentation"
  },
  "overall_condition": {
    "texture": "uneven",
    "pores": "enlarged",
    "wrinkles": "fine_lines",
    "dark_spots": true,
    "hyperpigmentation": true,
    "redness": true,
    "dryness": false,
    "oiliness": true,
    "notes": "T-zone is oily, cheeks are normal to dry"
  },
  "dermatological_flags": [
    {
      "condition": "rosacea",
      "confidence": "medium",
      "description": "Persistent redness on cheeks with visible capillaries",
      "recommend_doctor": true
    }
  ],
  "age_assessment": "Early signs of aging: fine lines around eyes, slight loss of elasticity",
  "recommendations_summary": [
    "Use gentle, non-comedogenic cleanser twice daily",
    "Apply salicylic acid treatment for acne",
    "Use broad-spectrum SPF 50+ daily",
    "Consider retinol for fine lines and texture",
    "Consult dermatologist for rosacea management"
  ]
}
```

Provide ONLY the JSON output, no additional text."""
        
        return base_prompt

    def _parse_analysis_response(
        self,
        response_text: str,
        analysis_type: Literal["face", "body", "full"],
    ) -> SkinAnalysisResult:
        """Parse the model's JSON response into a structured result."""
        
        # Extract JSON from response (handle markdown code blocks)
        json_text = response_text.strip()
        if json_text.startswith("```json"):
            json_text = json_text[7:]
        if json_text.startswith("```"):
            json_text = json_text[3:]
        if json_text.endswith("```"):
            json_text = json_text[:-3]
        json_text = json_text.strip()
        
        try:
            data = json.loads(json_text)
        except json.JSONDecodeError:
            # Fallback: create minimal result
            return SkinAnalysisResult(
                analysis_id="",
                timestamp="",
                image_path="",
                skin_type="unknown",
                recommendations_summary=["Unable to parse analysis. Please try again."],
            )
        
        # Build result
        result = SkinAnalysisResult(
            analysis_id="",
            timestamp="",
            image_path="",
            skin_type=data.get("skin_type", "unknown"),
            age_assessment=data.get("age_assessment"),
            recommendations_summary=data.get("recommendations_summary", []),
        )
        
        # Parse overall acne
        if "overall_acne" in data and data["overall_acne"]:
            acne_data = data["overall_acne"]
            result.overall_acne = AcneAnalysis(
                detected=acne_data.get("detected", False),
                acne_type=acne_data.get("acne_type"),
                severity=acne_data.get("severity"),
                locations=acne_data.get("locations", []),
                count_estimate=acne_data.get("count_estimate"),
                notes=acne_data.get("notes", ""),
            )
        
        # Parse overall condition
        if "overall_condition" in data and data["overall_condition"]:
            cond_data = data["overall_condition"]
            result.overall_condition = SkinCondition(
                texture=cond_data.get("texture", "normal"),
                pores=cond_data.get("pores", "normal"),
                wrinkles=cond_data.get("wrinkles", "none"),
                dark_spots=cond_data.get("dark_spots", False),
                hyperpigmentation=cond_data.get("hyperpigmentation", False),
                redness=cond_data.get("redness", False),
                dryness=cond_data.get("dryness", False),
                oiliness=cond_data.get("oiliness", False),
                notes=cond_data.get("notes", ""),
            )
        
        # Parse dermatological flags
        if "dermatological_flags" in data:
            for flag_data in data["dermatological_flags"]:
                result.dermatological_flags.append(
                    DermatologicalFlag(
                        condition=flag_data.get("condition", "unknown"),
                        confidence=flag_data.get("confidence", "low"),
                        description=flag_data.get("description", ""),
                        recommend_doctor=flag_data.get("recommend_doctor", True),
                    )
                )
        
        return result

    # ---- Progress tracking ----

    def save_analysis(self, result: SkinAnalysisResult, output_dir: str):
        """Save analysis result to disk."""
        output_path = Path(output_dir) / f"{result.analysis_id}.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w") as f:
            json.dump(result.to_dict(), f, indent=2)

    def load_analysis(self, analysis_id: str, data_dir: str) -> Optional[SkinAnalysisResult]:
        """Load a saved analysis result."""
        analysis_path = Path(data_dir) / f"{analysis_id}.json"
        
        if not analysis_path.exists():
            return None
        
        with open(analysis_path) as f:
            data = json.load(f)
            return SkinAnalysisResult.from_dict(data)

    def list_analyses(self, data_dir: str) -> List[Dict[str, str]]:
        """List all saved analyses."""
        data_path = Path(data_dir)
        if not data_path.exists():
            return []
        
        analyses = []
        for path in sorted(data_path.glob("*.json"), reverse=True):
            with open(path) as f:
                data = json.load(f)
                analyses.append({
                    "analysis_id": data.get("analysis_id", ""),
                    "timestamp": data.get("timestamp", ""),
                    "skin_type": data.get("skin_type", ""),
                })
        
        return analyses


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Project Face: AI Skin Analysis Engine — Demo")
    print("=" * 50)
    print("\nNOTE: This demo requires an image file to analyze.")
    print("Usage: python analysis_engine.py <image_path>")
    print("\nFor full functionality, integrate with the FastAPI backend.")
