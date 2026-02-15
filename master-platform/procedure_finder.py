"""
Master Platform: Procedure Finder
==================================
Find cheapest AND best cosmetic/skin/medical wellness procedures.
Ranked by REAL reviews (not paid) AND BBB ratings.
Includes Tijuana medical tourism integration.

Author: Audrey Evans
"""

import json
from pathlib import Path
from typing import List, Dict, Optional, Any, Literal
from dataclasses import dataclass, field, asdict
from datetime import datetime

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DATA_DIR = Path(__file__).parent / "data" / "procedures"
PROVIDERS_DB = DATA_DIR / "providers.json"
REVIEWS_DB = DATA_DIR / "reviews.json"


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

@dataclass
class Provider:
    """A cosmetic/medical procedure provider."""
    provider_id: str
    name: str
    location: str  # City, State or City, Country
    country: str  # US, Mexico, etc.
    address: str
    phone: str
    website: str
    provider_type: Literal["clinic", "medspa", "hospital", "private_practice"]
    specialties: List[str]  # botox, NAD+, laser, etc.
    bbb_rating: Optional[str] = None  # A+, A, B, etc.
    bbb_complaints: int = 0
    profeco_rating: Optional[str] = None  # For Mexico (Profeco equivalent)
    jci_accredited: bool = False  # Joint Commission International
    average_rating: float = 0.0  # Aggregate from reviews
    total_reviews: int = 0
    price_tier: Literal["budget", "mid_range", "luxury"] = "mid_range"
    accepts_insurance: bool = False
    languages: List[str] = field(default_factory=lambda: ["English"])
    shuttle_service: bool = False  # For Tijuana clinics
    recovery_hotel_partner: bool = False
    sponsored: bool = False  # Paid advertising
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Provider":
        return cls(**d)


@dataclass
class Procedure:
    """A specific procedure offered by a provider."""
    procedure_id: str
    provider_id: str
    procedure_name: str
    procedure_category: str  # cosmetic, dermatological, wellness, dental
    description: str
    price_usd: Optional[float] = None
    price_range_usd: Optional[str] = None  # "$500-$1000"
    duration: str = ""  # "30 minutes", "1 hour", etc.
    downtime: str = ""  # "None", "1-3 days", etc.
    requires_consultation: bool = True
    available_in_tijuana: bool = False
    tijuana_savings_percent: Optional[int] = None  # % savings vs US
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Procedure":
        return cls(**d)


@dataclass
class Review:
    """A user review of a provider."""
    review_id: str
    provider_id: str
    rating: float  # 1.0 - 5.0
    review_text: str
    reviewer_name: str
    review_date: str
    verified: bool = False  # Verified purchase/visit
    source: str = "platform"  # platform, google, yelp, realself, etc.
    helpful_count: int = 0
    flagged_as_paid: bool = False  # Flagged as potentially paid review

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Review":
        return cls(**d)


@dataclass
class SearchResult:
    """A search result with provider and procedure info."""
    provider: Provider
    procedure: Procedure
    match_score: float  # 0.0 - 1.0
    distance_miles: Optional[float] = None
    us_comparison_price: Optional[float] = None  # For Tijuana clinics


# ---------------------------------------------------------------------------
# Procedure Finder
# ---------------------------------------------------------------------------

class ProcedureFinder:
    """
    Search and compare cosmetic/medical procedures across providers.
    Includes BBB ratings, real reviews, and Tijuana medical tourism.
    """

    def __init__(self):
        self.data_dir = DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.providers_path = self.data_dir / "providers.json"
        self.reviews_path = self.data_dir / "reviews.json"
        self.procedures_path = self.data_dir / "procedures.json"
        
        self._providers: Dict[str, Provider] = {}
        self._procedures: Dict[str, Procedure] = {}
        self._reviews: Dict[str, List[Review]] = {}  # provider_id -> reviews
        
        self._load_data()

    # ---- Data management ----

    def _load_data(self):
        """Load providers, procedures, and reviews from disk."""
        if self.providers_path.exists():
            with open(self.providers_path) as f:
                data = json.load(f)
                self._providers = {k: Provider.from_dict(v) for k, v in data.items()}
        
        if self.procedures_path.exists():
            with open(self.procedures_path) as f:
                data = json.load(f)
                self._procedures = {k: Procedure.from_dict(v) for k, v in data.items()}
        
        if self.reviews_path.exists():
            with open(self.reviews_path) as f:
                data = json.load(f)
                self._reviews = {k: [Review.from_dict(r) for r in v] for k, v in data.items()}

    def _save_data(self):
        """Persist providers, procedures, and reviews to disk."""
        with open(self.providers_path, "w") as f:
            json.dump({k: v.to_dict() for k, v in self._providers.items()}, f, indent=2)
        
        with open(self.procedures_path, "w") as f:
            json.dump({k: v.to_dict() for k, v in self._procedures.items()}, f, indent=2)
        
        with open(self.reviews_path, "w") as f:
            json.dump({k: [r.to_dict() for r in v] for k, v in self._reviews.items()}, f, indent=2)

    # ---- Provider management ----

    def add_provider(self, provider: Provider):
        """Add a new provider to the database."""
        self._providers[provider.provider_id] = provider
        self._save_data()

    def add_procedure(self, procedure: Procedure):
        """Add a new procedure to the database."""
        self._procedures[procedure.procedure_id] = procedure
        self._save_data()

    def add_review(self, review: Review):
        """Add a review for a provider."""
        if review.provider_id not in self._reviews:
            self._reviews[review.provider_id] = []
        self._reviews[review.provider_id].append(review)
        
        # Update provider's aggregate rating
        if review.provider_id in self._providers:
            provider = self._providers[review.provider_id]
            reviews = self._reviews[review.provider_id]
            # Only count non-paid reviews
            real_reviews = [r for r in reviews if not r.flagged_as_paid]
            if real_reviews:
                provider.average_rating = sum(r.rating for r in real_reviews) / len(real_reviews)
                provider.total_reviews = len(real_reviews)
        
        self._save_data()

    # ---- Search ----

    def search_procedures(
        self,
        procedure_name: str,
        location: Optional[str] = None,
        max_distance_miles: Optional[float] = None,
        include_tijuana: bool = True,
        price_tier: Optional[Literal["budget", "mid_range", "luxury"]] = None,
        min_rating: float = 3.0,
        sort_by: Literal["price", "rating", "distance"] = "rating",
    ) -> List[SearchResult]:
        """
        Search for procedures matching criteria.
        
        Args:
            procedure_name: Name or keyword for the procedure
            location: User's location (City, State)
            max_distance_miles: Maximum distance from user
            include_tijuana: Include Tijuana medical tourism options
            price_tier: Filter by price tier
            min_rating: Minimum average rating
            sort_by: Sort results by price, rating, or distance
        
        Returns:
            List of SearchResult objects
        """
        results = []
        
        # Find matching procedures
        matching_procedures = [
            p for p in self._procedures.values()
            if procedure_name.lower() in p.procedure_name.lower()
        ]
        
        for procedure in matching_procedures:
            provider = self._providers.get(procedure.provider_id)
            if not provider:
                continue
            
            # Filter by rating
            if provider.average_rating < min_rating:
                continue
            
            # Filter by price tier
            if price_tier and provider.price_tier != price_tier:
                continue
            
            # Filter by location
            if not include_tijuana and provider.country == "Mexico":
                continue
            
            # Calculate match score
            match_score = self._calculate_match_score(provider, procedure, procedure_name)
            
            # Calculate distance (placeholder - would use geocoding in production)
            distance = None
            if location and provider.country == "US":
                distance = self._estimate_distance(location, provider.location)
                if max_distance_miles and distance > max_distance_miles:
                    continue
            
            # US comparison price for Tijuana
            us_comparison = None
            if provider.country == "Mexico" and procedure.tijuana_savings_percent:
                if procedure.price_usd:
                    us_comparison = procedure.price_usd / (1 - procedure.tijuana_savings_percent / 100)
            
            results.append(SearchResult(
                provider=provider,
                procedure=procedure,
                match_score=match_score,
                distance_miles=distance,
                us_comparison_price=us_comparison,
            ))
        
        # Sort results
        if sort_by == "price":
            results.sort(key=lambda r: r.procedure.price_usd or 999999)
        elif sort_by == "rating":
            results.sort(key=lambda r: r.provider.average_rating, reverse=True)
        elif sort_by == "distance":
            results.sort(key=lambda r: r.distance_miles or 999999)
        
        return results

    def _calculate_match_score(self, provider: Provider, procedure: Procedure, query: str) -> float:
        """Calculate relevance score for a search result."""
        score = 0.0
        
        # Exact match bonus
        if query.lower() == procedure.procedure_name.lower():
            score += 50.0
        elif query.lower() in procedure.procedure_name.lower():
            score += 30.0
        
        # Rating bonus
        score += provider.average_rating * 10.0
        
        # Review count bonus
        score += min(provider.total_reviews / 10, 10.0)
        
        # BBB rating bonus
        if provider.bbb_rating:
            bbb_scores = {"A+": 10, "A": 8, "B": 6, "C": 4, "D": 2, "F": 0}
            score += bbb_scores.get(provider.bbb_rating, 0)
        
        # JCI accreditation bonus
        if provider.jci_accredited:
            score += 15.0
        
        # Penalty for BBB complaints
        score -= min(provider.bbb_complaints * 2, 20)
        
        # Sponsored boost (but not too much)
        if provider.sponsored:
            score += 5.0
        
        return round(score, 2)

    def _estimate_distance(self, location1: str, location2: str) -> float:
        """Estimate distance between two locations (placeholder)."""
        # In production, use geocoding API (Google Maps, Mapbox, etc.)
        # For now, return a placeholder
        return 50.0

    # ---- Medical wellness procedures ----

    def get_wellness_procedures(self, location: Optional[str] = None) -> List[SearchResult]:
        """Get medical wellness procedures (NAD+, Botox, IV therapy)."""
        wellness_keywords = ["NAD+", "Botox", "IV therapy", "vitamin drip", "Myers cocktail", "glutathione"]
        
        results = []
        for keyword in wellness_keywords:
            results.extend(self.search_procedures(keyword, location=location))
        
        # Deduplicate by provider
        seen_providers = set()
        unique_results = []
        for result in results:
            if result.provider.provider_id not in seen_providers:
                seen_providers.add(result.provider.provider_id)
                unique_results.append(result)
        
        return unique_results

    # ---- Tijuana medical tourism ----

    def get_tijuana_clinics(
        self,
        procedure_name: Optional[str] = None,
        jci_only: bool = False,
    ) -> List[SearchResult]:
        """Get Tijuana medical tourism clinics."""
        tijuana_providers = [
            p for p in self._providers.values()
            if p.country == "Mexico" and "Tijuana" in p.location
        ]
        
        if jci_only:
            tijuana_providers = [p for p in tijuana_providers if p.jci_accredited]
        
        results = []
        for provider in tijuana_providers:
            # Get all procedures for this provider
            provider_procedures = [
                proc for proc in self._procedures.values()
                if proc.provider_id == provider.provider_id
            ]
            
            # Filter by procedure name if specified
            if procedure_name:
                provider_procedures = [
                    proc for proc in provider_procedures
                    if procedure_name.lower() in proc.procedure_name.lower()
                ]
            
            for procedure in provider_procedures:
                match_score = self._calculate_match_score(provider, procedure, procedure_name or "")
                
                us_comparison = None
                if procedure.tijuana_savings_percent and procedure.price_usd:
                    us_comparison = procedure.price_usd / (1 - procedure.tijuana_savings_percent / 100)
                
                results.append(SearchResult(
                    provider=provider,
                    procedure=procedure,
                    match_score=match_score,
                    us_comparison_price=us_comparison,
                ))
        
        results.sort(key=lambda r: r.match_score, reverse=True)
        return results

    def get_tijuana_travel_info(self) -> Dict[str, Any]:
        """Get travel logistics for Tijuana medical tourism."""
        return {
            "border_crossing": {
                "ports_of_entry": [
                    "San Ysidro (pedestrian and vehicle)",
                    "Otay Mesa (vehicle only)",
                    "Cross Border Xpress (CBX) - pedestrian bridge from Tijuana airport",
                ],
                "wait_times_url": "https://bwt.cbp.gov/",
                "tips": [
                    "Cross early morning or late evening to avoid peak wait times",
                    "Bring passport or passport card",
                    "Declare all medications when returning to US",
                    "CBX bridge is fastest option if flying into Tijuana airport",
                ],
            },
            "transportation": {
                "shuttle_services": [
                    "Many clinics offer free shuttle from border",
                    "Uber and taxi available",
                    "Private medical transport services available",
                ],
                "parking": "Secure parking available on US side near border",
            },
            "recovery_hotels": [
                "Hotel Lucerna Tijuana",
                "Grand Hotel Tijuana",
                "Marriott Tijuana",
                "City Express Tijuana",
            ],
            "safety": [
                "Stay in Zona Rio or tourist areas",
                "Use clinic-recommended transportation",
                "Keep valuables secure",
                "Have emergency contacts saved",
            ],
            "insurance": "Most US insurance does not cover procedures in Mexico. Check with your provider.",
            "language": "Most medical staff speak English. Spanish helpful but not required.",
        }

    # ---- Analytics ----

    def get_provider_reviews(self, provider_id: str, exclude_paid: bool = True) -> List[Review]:
        """Get reviews for a specific provider."""
        reviews = self._reviews.get(provider_id, [])
        if exclude_paid:
            reviews = [r for r in reviews if not r.flagged_as_paid]
        return sorted(reviews, key=lambda r: r.review_date, reverse=True)

    def compare_providers(self, provider_ids: List[str]) -> Dict[str, Any]:
        """Compare multiple providers side-by-side."""
        comparison = {
            "providers": [],
        }
        
        for provider_id in provider_ids:
            provider = self._providers.get(provider_id)
            if not provider:
                continue
            
            reviews = self.get_provider_reviews(provider_id, exclude_paid=True)
            procedures = [p for p in self._procedures.values() if p.provider_id == provider_id]
            
            comparison["providers"].append({
                "name": provider.name,
                "location": provider.location,
                "average_rating": provider.average_rating,
                "total_reviews": len(reviews),
                "bbb_rating": provider.bbb_rating,
                "bbb_complaints": provider.bbb_complaints,
                "jci_accredited": provider.jci_accredited,
                "price_tier": provider.price_tier,
                "total_procedures": len(procedures),
                "sponsored": provider.sponsored,
            })
        
        return comparison


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Master Platform: Procedure Finder — Demo")
    print("=" * 50)
    
    finder = ProcedureFinder()
    
    print("\nThis module finds and compares cosmetic/medical procedures.")
    print("Includes BBB ratings, real reviews, and Tijuana medical tourism.")
    print("\nFeatures:")
    print("  - Medical wellness: NAD+, Botox, IV therapy")
    print("  - Tijuana clinics with US price comparison")
    print("  - BBB and Profeco ratings")
    print("  - JCI accreditation filtering")
    print("  - Real review aggregation")
    print("  - Sponsored listings (clearly marked)")
