"""
Master Platform: Clinical Trials Finder
=========================================
Pulls from ClinicalTrials.gov API to match users with eligible clinical trials.
Covers skincare, anti-aging, cancer, glaucoma, rare diseases, cosmetic, wellness.
Includes breakthrough notifications and cutting-edge procedure tracking.

Author: Audrey Evans
"""

import json
import hashlib
import requests
from pathlib import Path
from typing import List, Dict, Optional, Any, Literal
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from urllib.parse import urlencode

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# ClinicalTrials.gov v2 API (free, public, no key required)
CTGOV_BASE_URL = "https://clinicaltrials.gov/api/v2"
CTGOV_STUDIES_ENDPOINT = f"{CTGOV_BASE_URL}/studies"

DATA_DIR = Path(__file__).parent / "data" / "clinical_trials"
USER_PROFILES_DIR = DATA_DIR / "user_profiles"
NOTIFICATIONS_DIR = DATA_DIR / "notifications"
CUTTING_EDGE_DB = DATA_DIR / "cutting_edge_procedures.json"
BREAKTHROUGHS_DB = DATA_DIR / "breakthroughs.json"

# Categories of interest
TRIAL_CATEGORIES = {
    "skincare": ["dermatitis", "acne", "eczema", "psoriasis", "rosacea", "skin aging", "hyperpigmentation"],
    "anti_aging": ["aging", "longevity", "telomere", "senescence", "NAD+", "rapamycin", "metformin aging"],
    "cancer": ["oncology", "immunotherapy", "CAR-T", "checkpoint inhibitor", "tumor"],
    "glaucoma": ["glaucoma", "intraocular pressure", "optic nerve", "eye aging"],
    "rare_diseases": ["orphan drug", "rare disease", "gene therapy"],
    "cosmetic": ["cosmetic", "botulinum toxin", "dermal filler", "laser skin", "microneedling"],
    "wellness": ["vitamin D", "IV therapy", "NAD+ infusion", "stem cell", "peptide therapy"],
}


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

@dataclass
class UserProfile:
    """User profile for trial matching."""
    user_id: str
    age: Optional[int] = None
    sex: Optional[Literal["male", "female", "other"]] = None
    location: Optional[str] = None  # City, State
    state: Optional[str] = None
    conditions: List[str] = field(default_factory=list)
    interests: List[str] = field(default_factory=list)  # skincare, anti_aging, etc.
    max_travel_miles: int = 100
    willing_to_travel_internationally: bool = False
    notification_preferences: Dict[str, bool] = field(default_factory=lambda: {
        "new_trials": True,
        "breakthroughs": True,
        "fda_approvals": True,
        "price_drops": True,
        "new_clinics": True,
    })

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "UserProfile":
        return cls(**d)


@dataclass
class ClinicalTrial:
    """A clinical trial from ClinicalTrials.gov."""
    nct_id: str
    title: str
    brief_summary: str
    status: str  # Recruiting, Active, Completed, etc.
    phase: Optional[str] = None  # Phase 1, Phase 2, Phase 3, Phase 4
    conditions: List[str] = field(default_factory=list)
    interventions: List[str] = field(default_factory=list)
    sponsor: str = ""
    locations: List[Dict[str, str]] = field(default_factory=list)
    enrollment: Optional[int] = None
    start_date: Optional[str] = None
    completion_date: Optional[str] = None
    eligibility_criteria: str = ""
    min_age: Optional[str] = None
    max_age: Optional[str] = None
    sex: Optional[str] = None  # All, Female, Male
    compensation: Optional[str] = None
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    url: str = ""
    category: str = ""  # Our internal category
    match_score: float = 0.0

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "ClinicalTrial":
        return cls(**d)


@dataclass
class CuttingEdgeProcedure:
    """A rare/cutting-edge procedure tracked globally."""
    procedure_id: str
    name: str
    description: str
    category: str  # cosmetic, ophthalmology, anti-aging, etc.
    num_specialists_worldwide: int  # "Only X doctors do this"
    specialists: List[Dict[str, str]] = field(default_factory=list)  # [{name, location, clinic}]
    locations_available: List[str] = field(default_factory=list)
    estimated_cost_usd: Optional[str] = None
    waitlist_months: Optional[int] = None
    fda_approved: bool = False
    clinical_trial_phase: Optional[str] = None
    success_rate: Optional[str] = None
    risks: List[str] = field(default_factory=list)
    reviews_summary: str = ""
    last_updated: str = ""
    related_trials: List[str] = field(default_factory=list)  # NCT IDs
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "CuttingEdgeProcedure":
        return cls(**d)


@dataclass
class Breakthrough:
    """A medical/cosmetic breakthrough notification."""
    breakthrough_id: str
    title: str
    description: str
    category: str  # fda_approval, new_ingredient, new_procedure, price_drop, new_clinic
    source_url: str
    published_date: str
    relevance_tags: List[str] = field(default_factory=list)
    impact_level: Literal["low", "medium", "high", "critical"] = "medium"
    notified_users: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Breakthrough":
        return cls(**d)


# ---------------------------------------------------------------------------
# Clinical Trials Finder
# ---------------------------------------------------------------------------

class ClinicalTrialsFinder:
    """
    Search ClinicalTrials.gov and match users with eligible trials.
    Track cutting-edge procedures and send breakthrough notifications.
    """

    def __init__(self):
        self.data_dir = DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)
        USER_PROFILES_DIR.mkdir(parents=True, exist_ok=True)
        NOTIFICATIONS_DIR.mkdir(parents=True, exist_ok=True)
        
        self._cutting_edge: Dict[str, CuttingEdgeProcedure] = {}
        self._breakthroughs: List[Breakthrough] = []
        self._load_data()

    def _load_data(self):
        """Load cutting-edge procedures and breakthroughs from disk."""
        if CUTTING_EDGE_DB.exists():
            with open(CUTTING_EDGE_DB) as f:
                data = json.load(f)
                self._cutting_edge = {k: CuttingEdgeProcedure.from_dict(v) for k, v in data.items()}
        
        if BREAKTHROUGHS_DB.exists():
            with open(BREAKTHROUGHS_DB) as f:
                data = json.load(f)
                self._breakthroughs = [Breakthrough.from_dict(b) for b in data]

    def _save_data(self):
        """Persist data to disk."""
        with open(CUTTING_EDGE_DB, "w") as f:
            json.dump({k: v.to_dict() for k, v in self._cutting_edge.items()}, f, indent=2)
        
        with open(BREAKTHROUGHS_DB, "w") as f:
            json.dump([b.to_dict() for b in self._breakthroughs], f, indent=2)

    # ---- ClinicalTrials.gov API ----

    def search_trials(
        self,
        query: str,
        status: Optional[str] = "RECRUITING",
        phase: Optional[str] = None,
        location: Optional[str] = None,
        max_results: int = 20,
    ) -> List[ClinicalTrial]:
        """
        Search ClinicalTrials.gov for matching trials.
        
        Args:
            query: Search query (condition, intervention, keyword)
            status: Trial status filter (RECRUITING, ACTIVE_NOT_RECRUITING, COMPLETED, etc.)
            phase: Trial phase filter (PHASE1, PHASE2, PHASE3, PHASE4)
            location: Location filter (state or city)
            max_results: Maximum number of results
        
        Returns:
            List of ClinicalTrial objects
        """
        params = {
            "query.term": query,
            "pageSize": min(max_results, 100),
            "format": "json",
        }
        
        # Build filter
        filters = []
        if status:
            filters.append(f"overallStatus:{status}")
        if phase:
            filters.append(f"phase:{phase}")
        
        if filters:
            params["filter.advanced"] = " AND ".join(filters)
        
        if location:
            params["query.locn"] = location
        
        try:
            response = requests.get(
                CTGOV_STUDIES_ENDPOINT,
                params=params,
                timeout=30,
                headers={"Accept": "application/json"},
            )
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"ClinicalTrials.gov API error: {e}")
            return []
        
        trials = []
        studies = data.get("studies", [])
        
        for study in studies:
            protocol = study.get("protocolSection", {})
            id_module = protocol.get("identificationModule", {})
            status_module = protocol.get("statusModule", {})
            desc_module = protocol.get("descriptionModule", {})
            design_module = protocol.get("designModule", {})
            eligibility_module = protocol.get("eligibilityModule", {})
            contacts_module = protocol.get("contactsLocationsModule", {})
            sponsor_module = protocol.get("sponsorCollaboratorsModule", {})
            arms_module = protocol.get("armsInterventionsModule", {})
            conditions_module = protocol.get("conditionsModule", {})
            
            nct_id = id_module.get("nctId", "")
            
            # Extract locations
            locations = []
            for loc in contacts_module.get("locations", []):
                locations.append({
                    "facility": loc.get("facility", ""),
                    "city": loc.get("city", ""),
                    "state": loc.get("state", ""),
                    "country": loc.get("country", ""),
                })
            
            # Extract interventions
            interventions = []
            for arm in arms_module.get("interventions", []):
                interventions.append(arm.get("name", ""))
            
            # Extract conditions
            conditions = conditions_module.get("conditions", [])
            
            # Extract contact info
            central_contacts = contacts_module.get("centralContacts", [])
            contact_name = central_contacts[0].get("name", "") if central_contacts else ""
            contact_email = central_contacts[0].get("email", "") if central_contacts else ""
            contact_phone = central_contacts[0].get("phone", "") if central_contacts else ""
            
            # Extract phases
            phases = design_module.get("phases", [])
            phase_str = ", ".join(phases) if phases else None
            
            # Extract enrollment
            enrollment_info = design_module.get("enrollmentInfo", {})
            enrollment = enrollment_info.get("count")
            
            # Extract sponsor
            lead_sponsor = sponsor_module.get("leadSponsor", {})
            sponsor = lead_sponsor.get("name", "")
            
            trial = ClinicalTrial(
                nct_id=nct_id,
                title=id_module.get("officialTitle", id_module.get("briefTitle", "")),
                brief_summary=desc_module.get("briefSummary", ""),
                status=status_module.get("overallStatus", ""),
                phase=phase_str,
                conditions=conditions,
                interventions=interventions,
                sponsor=sponsor,
                locations=locations,
                enrollment=enrollment,
                start_date=status_module.get("startDateStruct", {}).get("date", ""),
                completion_date=status_module.get("completionDateStruct", {}).get("date", ""),
                eligibility_criteria=eligibility_module.get("eligibilityCriteria", ""),
                min_age=eligibility_module.get("minimumAge", ""),
                max_age=eligibility_module.get("maximumAge", ""),
                sex=eligibility_module.get("sex", ""),
                contact_name=contact_name,
                contact_email=contact_email,
                contact_phone=contact_phone,
                url=f"https://clinicaltrials.gov/study/{nct_id}",
            )
            
            trials.append(trial)
        
        return trials

    def search_by_category(
        self,
        category: str,
        location: Optional[str] = None,
        max_results: int = 20,
    ) -> List[ClinicalTrial]:
        """Search trials by predefined category."""
        keywords = TRIAL_CATEGORIES.get(category, [])
        all_trials = []
        
        for keyword in keywords:
            trials = self.search_trials(
                query=keyword,
                location=location,
                max_results=max_results // len(keywords) + 1,
            )
            for trial in trials:
                trial.category = category
            all_trials.extend(trials)
        
        # Deduplicate by NCT ID
        seen = set()
        unique_trials = []
        for trial in all_trials:
            if trial.nct_id not in seen:
                seen.add(trial.nct_id)
                unique_trials.append(trial)
        
        return unique_trials[:max_results]

    # ---- User profile matching ----

    def match_trials_to_user(
        self,
        user_profile: UserProfile,
        max_results: int = 20,
    ) -> List[ClinicalTrial]:
        """
        Match clinical trials to a user's profile.
        
        Args:
            user_profile: User's profile with conditions, interests, location
            max_results: Maximum number of results
        
        Returns:
            List of matched ClinicalTrial objects sorted by relevance
        """
        all_matched = []
        
        # Search by user's conditions
        for condition in user_profile.conditions:
            trials = self.search_trials(
                query=condition,
                location=user_profile.state,
                max_results=10,
            )
            for trial in trials:
                trial.match_score = self._calculate_match_score(trial, user_profile)
            all_matched.extend(trials)
        
        # Search by user's interests
        for interest in user_profile.interests:
            if interest in TRIAL_CATEGORIES:
                trials = self.search_by_category(
                    category=interest,
                    location=user_profile.state,
                    max_results=10,
                )
                for trial in trials:
                    trial.match_score = self._calculate_match_score(trial, user_profile)
                all_matched.extend(trials)
        
        # Deduplicate and sort by match score
        seen = set()
        unique_matched = []
        for trial in all_matched:
            if trial.nct_id not in seen:
                seen.add(trial.nct_id)
                unique_matched.append(trial)
        
        unique_matched.sort(key=lambda t: t.match_score, reverse=True)
        return unique_matched[:max_results]

    def _calculate_match_score(self, trial: ClinicalTrial, profile: UserProfile) -> float:
        """Calculate how well a trial matches a user profile."""
        score = 0.0
        
        # Condition match
        for condition in profile.conditions:
            if condition.lower() in trial.title.lower() or condition.lower() in trial.brief_summary.lower():
                score += 30.0
            for trial_cond in trial.conditions:
                if condition.lower() in trial_cond.lower():
                    score += 20.0
        
        # Location match
        if profile.state:
            for loc in trial.locations:
                if profile.state.lower() in loc.get("state", "").lower():
                    score += 25.0
                    break
        
        # Age eligibility
        if profile.age:
            age_eligible = True
            if trial.min_age:
                try:
                    min_age_num = int(trial.min_age.split()[0])
                    if profile.age < min_age_num:
                        age_eligible = False
                except (ValueError, IndexError):
                    pass
            if trial.max_age:
                try:
                    max_age_num = int(trial.max_age.split()[0])
                    if profile.age > max_age_num:
                        age_eligible = False
                except (ValueError, IndexError):
                    pass
            if age_eligible:
                score += 15.0
        
        # Sex eligibility
        if profile.sex and trial.sex:
            if trial.sex == "ALL" or trial.sex.lower() == profile.sex.lower():
                score += 5.0
        
        # Recruiting bonus
        if trial.status == "RECRUITING":
            score += 10.0
        
        # Compensation bonus
        if trial.compensation:
            score += 5.0
        
        return round(score, 2)

    # ---- Cutting-edge procedures ----

    def add_cutting_edge_procedure(self, procedure: CuttingEdgeProcedure):
        """Add a cutting-edge procedure to the tracking database."""
        self._cutting_edge[procedure.procedure_id] = procedure
        self._save_data()

    def get_cutting_edge_procedures(
        self,
        category: Optional[str] = None,
    ) -> List[CuttingEdgeProcedure]:
        """Get all tracked cutting-edge procedures."""
        procedures = list(self._cutting_edge.values())
        if category:
            procedures = [p for p in procedures if p.category == category]
        return sorted(procedures, key=lambda p: p.num_specialists_worldwide)

    def search_cutting_edge(self, query: str) -> List[CuttingEdgeProcedure]:
        """Search cutting-edge procedures by keyword."""
        query_lower = query.lower()
        return [
            p for p in self._cutting_edge.values()
            if query_lower in p.name.lower() or query_lower in p.description.lower()
        ]

    def seed_cutting_edge_procedures(self):
        """Seed the database with known cutting-edge procedures."""
        procedures = [
            CuttingEdgeProcedure(
                procedure_id="ce_eye_color_change",
                name="Permanent Eye Color Change (Keratopigmentation)",
                description=(
                    "Permanent iris color change using a corneal tattoo technique called "
                    "keratopigmentation. Creates a femtosecond laser tunnel in the cornea "
                    "and fills it with biocompatible pigment. Currently available from very "
                    "few specialists in the US (primarily New York) and select clinics in "
                    "Europe and Latin America."
                ),
                category="cosmetic_ophthalmology",
                num_specialists_worldwide=12,
                specialists=[
                    {"name": "Dr. Alexander Movshovich", "location": "New York, NY", "clinic": "Kerato NYC"},
                ],
                locations_available=["New York, NY", "Paris, France", "Barcelona, Spain", "Bogota, Colombia"],
                estimated_cost_usd="$8,000-$15,000",
                waitlist_months=3,
                fda_approved=False,
                clinical_trial_phase="Not in formal trials — performed as elective procedure",
                success_rate="High cosmetic success; long-term safety data still emerging",
                risks=["Corneal damage", "Infection", "Pigment migration", "Glare/halos", "Irreversibility"],
                reviews_summary="Mixed: high satisfaction for cosmetic result, concerns about long-term safety",
                last_updated=datetime.now(timezone.utc).isoformat(),
            ),
            CuttingEdgeProcedure(
                procedure_id="ce_glaucoma_aging_reversal",
                name="Glaucoma Gene Therapy with Age-Reversal Effect",
                description=(
                    "Experimental gene therapy using Yamanaka factors (OSK — Oct4, Sox2, Klf4) "
                    "delivered via AAV vector to retinal ganglion cells. Originally developed to "
                    "restore vision in glaucoma by reprogramming aged cells. Landmark Harvard/Sinclair "
                    "lab research showed it reversed age-related epigenetic changes in mouse retinas, "
                    "effectively making cells 'younger' by up to 20 years equivalent. Now being "
                    "explored for broader anti-aging applications."
                ),
                category="ophthalmology_anti_aging",
                num_specialists_worldwide=5,
                specialists=[
                    {"name": "Dr. David Sinclair Lab", "location": "Boston, MA", "clinic": "Harvard Medical School"},
                    {"name": "Life Biosciences / Turn Biotechnologies", "location": "San Diego, CA", "clinic": "Research"},
                ],
                locations_available=["Boston, MA (research only)", "San Diego, CA (research only)"],
                estimated_cost_usd="Not yet commercially available",
                waitlist_months=None,
                fda_approved=False,
                clinical_trial_phase="Phase 1 (for vision restoration)",
                success_rate="Preclinical: restored vision in mice with glaucoma; reversed epigenetic age",
                risks=["Gene therapy risks", "Tumor formation (if Oct4 overexpressed)", "Unknown long-term effects"],
                reviews_summary="Groundbreaking research; not yet available to patients. Clinical trials expected.",
                last_updated=datetime.now(timezone.utc).isoformat(),
                related_trials=["NCT04808596"],
            ),
            CuttingEdgeProcedure(
                procedure_id="ce_stem_cell_face",
                name="Autologous Stem Cell Facelift",
                description=(
                    "Uses patient's own adipose-derived stem cells combined with fat transfer "
                    "to rejuvenate facial tissue. Stem cells promote new blood vessel growth, "
                    "collagen production, and tissue regeneration. Results are more natural "
                    "and longer-lasting than traditional facelifts."
                ),
                category="cosmetic",
                num_specialists_worldwide=50,
                specialists=[
                    {"name": "Dr. Nathan Newman", "location": "Beverly Hills, CA", "clinic": "Newman Plastic Surgery"},
                ],
                locations_available=["Beverly Hills, CA", "Miami, FL", "Seoul, South Korea", "Tijuana, Mexico"],
                estimated_cost_usd="$15,000-$50,000",
                waitlist_months=2,
                fda_approved=False,
                clinical_trial_phase="Various trials ongoing",
                success_rate="Promising results in published studies",
                risks=["Infection", "Fat necrosis", "Asymmetry", "Stem cell unpredictability"],
                reviews_summary="High satisfaction among patients; natural-looking results",
                last_updated=datetime.now(timezone.utc).isoformat(),
            ),
            CuttingEdgeProcedure(
                procedure_id="ce_exosome_therapy",
                name="Exosome Therapy for Skin Rejuvenation",
                description=(
                    "Uses exosomes (nano-sized vesicles derived from stem cells) applied topically "
                    "or injected to stimulate cellular repair, collagen production, and tissue "
                    "regeneration. Emerging as a next-generation alternative to PRP."
                ),
                category="cosmetic_anti_aging",
                num_specialists_worldwide=100,
                specialists=[],
                locations_available=["Multiple US cities", "Seoul, South Korea", "Dubai, UAE"],
                estimated_cost_usd="$500-$3,000 per session",
                waitlist_months=0,
                fda_approved=False,
                clinical_trial_phase="Phase 2 trials ongoing",
                success_rate="Early results promising for skin texture and wound healing",
                risks=["Unregulated products", "Variable quality", "Limited long-term data"],
                reviews_summary="Growing popularity; quality varies significantly between providers",
                last_updated=datetime.now(timezone.utc).isoformat(),
            ),
            CuttingEdgeProcedure(
                procedure_id="ce_nad_iv",
                name="NAD+ IV Infusion Therapy",
                description=(
                    "Intravenous infusion of nicotinamide adenine dinucleotide (NAD+) for "
                    "cellular repair, anti-aging, energy restoration, and addiction recovery. "
                    "Especially relevant for cancer recovery patients. NAD+ levels decline "
                    "with age; replenishing via IV may reverse some age-related cellular damage."
                ),
                category="wellness_anti_aging",
                num_specialists_worldwide=500,
                specialists=[],
                locations_available=[
                    "Nationwide US (wellness clinics)", "Tijuana, Mexico (50-70% cheaper)",
                    "Dubai, UAE", "London, UK", "Bangkok, Thailand",
                ],
                estimated_cost_usd="$250-$1,000 per session (US); $100-$400 (Tijuana)",
                waitlist_months=0,
                fda_approved=False,
                clinical_trial_phase="Multiple Phase 1/2 trials",
                success_rate="Anecdotal: high patient satisfaction for energy and recovery",
                risks=["Nausea during infusion", "Chest tightness", "Unregulated dosing"],
                reviews_summary="Very popular in wellness community; limited clinical evidence for anti-aging claims",
                last_updated=datetime.now(timezone.utc).isoformat(),
            ),
        ]
        
        for proc in procedures:
            self._cutting_edge[proc.procedure_id] = proc
        
        self._save_data()

    # ---- Breakthrough notifications ----

    def add_breakthrough(self, breakthrough: Breakthrough):
        """Add a new breakthrough notification."""
        self._breakthroughs.append(breakthrough)
        self._save_data()

    def get_breakthroughs(
        self,
        category: Optional[str] = None,
        impact_level: Optional[str] = None,
        limit: int = 20,
    ) -> List[Breakthrough]:
        """Get recent breakthroughs, optionally filtered."""
        breakthroughs = self._breakthroughs.copy()
        
        if category:
            breakthroughs = [b for b in breakthroughs if b.category == category]
        if impact_level:
            breakthroughs = [b for b in breakthroughs if b.impact_level == impact_level]
        
        return sorted(breakthroughs, key=lambda b: b.published_date, reverse=True)[:limit]

    def match_breakthroughs_to_user(self, user_profile: UserProfile) -> List[Breakthrough]:
        """Find breakthroughs relevant to a user's profile."""
        matched = []
        
        for breakthrough in self._breakthroughs:
            relevance = 0
            
            # Check condition match
            for condition in user_profile.conditions:
                if condition.lower() in " ".join(breakthrough.relevance_tags).lower():
                    relevance += 1
            
            # Check interest match
            for interest in user_profile.interests:
                if interest.lower() in " ".join(breakthrough.relevance_tags).lower():
                    relevance += 1
            
            if relevance > 0:
                matched.append(breakthrough)
        
        return sorted(matched, key=lambda b: b.published_date, reverse=True)

    # ---- User profile management ----

    def save_user_profile(self, profile: UserProfile):
        """Save a user profile for trial matching."""
        profile_path = USER_PROFILES_DIR / f"{profile.user_id}.json"
        with open(profile_path, "w") as f:
            json.dump(profile.to_dict(), f, indent=2)

    def load_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """Load a user profile."""
        profile_path = USER_PROFILES_DIR / f"{user_id}.json"
        if profile_path.exists():
            with open(profile_path) as f:
                return UserProfile.from_dict(json.load(f))
        return None

    # ---- Specific searches ----

    def find_glaucoma_aging_trials(self) -> List[ClinicalTrial]:
        """Find the specific glaucoma treatment that reverses aging."""
        queries = [
            "Yamanaka factors glaucoma",
            "epigenetic reprogramming retina",
            "OSK gene therapy vision",
            "age reversal glaucoma",
            "NAD+ glaucoma",
        ]
        
        all_trials = []
        for query in queries:
            trials = self.search_trials(query=query, status=None, max_results=10)
            all_trials.extend(trials)
        
        # Deduplicate
        seen = set()
        unique = []
        for trial in all_trials:
            if trial.nct_id not in seen:
                seen.add(trial.nct_id)
                unique.append(trial)
        
        return unique

    def find_compensated_trials(
        self,
        location: Optional[str] = None,
        category: Optional[str] = None,
    ) -> List[ClinicalTrial]:
        """Find trials that compensate participants."""
        # ClinicalTrials.gov doesn't have a direct compensation filter,
        # so we search broadly and check eligibility text
        if category:
            trials = self.search_by_category(category, location=location, max_results=50)
        else:
            trials = self.search_trials(
                query="healthy volunteer compensation",
                location=location,
                max_results=50,
            )
        
        # Filter for mentions of compensation
        compensated = []
        compensation_keywords = ["compensat", "reimburse", "stipend", "payment", "paid"]
        
        for trial in trials:
            text = (trial.eligibility_criteria + " " + trial.brief_summary).lower()
            if any(kw in text for kw in compensation_keywords):
                trial.compensation = "Compensation mentioned in trial description"
                compensated.append(trial)
        
        return compensated


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Master Platform: Clinical Trials Finder — Demo")
    print("=" * 50)
    
    finder = ClinicalTrialsFinder()
    
    # Seed cutting-edge procedures
    finder.seed_cutting_edge_procedures()
    print(f"\nSeeded {len(finder._cutting_edge)} cutting-edge procedures:")
    for proc in finder.get_cutting_edge_procedures():
        print(f"  - {proc.name} ({proc.num_specialists_worldwide} specialists worldwide)")
    
    # Search for skincare trials
    print("\nSearching ClinicalTrials.gov for skincare trials...")
    trials = finder.search_by_category("skincare", max_results=5)
    print(f"Found {len(trials)} trials:")
    for trial in trials:
        print(f"  - [{trial.nct_id}] {trial.title[:80]}...")
        print(f"    Status: {trial.status} | Phase: {trial.phase}")
        print(f"    URL: {trial.url}")
    
    # Search for glaucoma aging reversal
    print("\nSearching for glaucoma + aging reversal trials...")
    glaucoma_trials = finder.find_glaucoma_aging_trials()
    print(f"Found {len(glaucoma_trials)} related trials")
