"""
Kimi K2 Thought-Chain Reuse Engine
===================================
Captures, stores, and reuses chain-of-thought reasoning patterns from Kimi K2 (moonshotai/kimi-k2).
Saves tokens, time, and money by reusing reasoning frameworks for similar tasks.

Author: Audrey Evans
"""

import json
import hashlib
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any, Literal
from dataclasses import dataclass, field, asdict
from collections import defaultdict

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

CACHE_DIR = Path(__file__).parent / "data" / "thought_chains"
CHAIN_INDEX = CACHE_DIR / "chain_index.json"
GOLDEN_CHAINS_FILE = CACHE_DIR / "golden_chains.json"


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

@dataclass
class ThoughtChain:
    """A captured chain-of-thought reasoning pattern."""
    chain_id: str
    task_type: str
    domain: str
    complexity: Literal["simple", "medium", "complex"]
    keywords: List[str]
    reasoning_steps: List[str]
    template: str  # Reusable reasoning framework
    captured_at: str
    model: str
    original_prompt: str
    original_response: str
    status: Literal["experimental", "validated", "golden"] = "experimental"
    reuse_count: int = 0
    success_rate: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "ThoughtChain":
        return cls(**d)


@dataclass
class ChainMatch:
    """A matched thought-chain with similarity score."""
    chain: ThoughtChain
    similarity_score: float
    match_reason: str


# ---------------------------------------------------------------------------
# Thought-Chain Cache
# ---------------------------------------------------------------------------

class ThoughtChainCache:
    """
    Storage and retrieval system for chain-of-thought reasoning patterns.
    Indexes chains by task type, domain, complexity, and keywords.
    """

    def __init__(self, cache_dir: Optional[str] = None):
        self.cache_dir = Path(cache_dir) if cache_dir else CACHE_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.cache_dir / "chain_index.json"
        self.golden_path = self.cache_dir / "golden_chains.json"
        self._index: Dict[str, ThoughtChain] = {}
        self._golden_chains: List[str] = []
        self._load_index()

    # ---- Index management ----

    def _load_index(self):
        """Load the chain index from disk."""
        if self.index_path.exists():
            with open(self.index_path) as f:
                data = json.load(f)
                self._index = {k: ThoughtChain.from_dict(v) for k, v in data.items()}
        
        if self.golden_path.exists():
            with open(self.golden_path) as f:
                self._golden_chains = json.load(f)

    def _save_index(self):
        """Persist the chain index to disk."""
        with open(self.index_path, "w") as f:
            json.dump({k: v.to_dict() for k, v in self._index.items()}, f, indent=2)
        
        with open(self.golden_path, "w") as f:
            json.dump(self._golden_chains, f, indent=2)

    # ---- Capture and store ----

    def capture_chain(
        self,
        task_type: str,
        domain: str,
        complexity: Literal["simple", "medium", "complex"],
        keywords: List[str],
        original_prompt: str,
        original_response: str,
        model: str = "moonshotai/kimi-k2",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ThoughtChain:
        """
        Capture a new thought-chain from a model response.
        Automatically extracts reasoning steps and creates a reusable template.
        """
        reasoning_steps = self._extract_reasoning_steps(original_response)
        template = self._create_template(reasoning_steps, original_prompt)
        
        chain_id = hashlib.sha256(
            f"{task_type}:{domain}:{template}:{datetime.now(timezone.utc).isoformat()}".encode()
        ).hexdigest()[:16]

        chain = ThoughtChain(
            chain_id=chain_id,
            task_type=task_type,
            domain=domain,
            complexity=complexity,
            keywords=[kw.lower().strip() for kw in keywords],
            reasoning_steps=reasoning_steps,
            template=template,
            captured_at=datetime.now(timezone.utc).isoformat(),
            model=model,
            original_prompt=original_prompt,
            original_response=original_response,
            status="experimental",
            metadata=metadata or {},
        )

        self._index[chain_id] = chain
        self._save_index()
        return chain

    def _extract_reasoning_steps(self, response: str) -> List[str]:
        """
        Extract reasoning steps from a model response.
        Looks for numbered lists, bullet points, or paragraph breaks.
        """
        steps = []
        
        # Try numbered lists first (1., 2., etc.)
        numbered = re.findall(r'(?:^|\n)\s*(\d+\.?\s+.+?)(?=\n\s*\d+\.|\n\n|$)', response, re.MULTILINE | re.DOTALL)
        if numbered:
            steps = [s.strip() for s in numbered]
            return steps
        
        # Try bullet points
        bullets = re.findall(r'(?:^|\n)\s*[-*•]\s+(.+?)(?=\n\s*[-*•]|\n\n|$)', response, re.MULTILINE | re.DOTALL)
        if bullets:
            steps = [s.strip() for s in bullets]
            return steps
        
        # Fallback: split by double newlines
        paragraphs = [p.strip() for p in response.split('\n\n') if p.strip()]
        if len(paragraphs) > 1:
            steps = paragraphs[:10]  # Cap at 10 steps
            return steps
        
        # Last resort: treat entire response as one step
        return [response.strip()]

    def _create_template(self, reasoning_steps: List[str], original_prompt: str) -> str:
        """
        Create a reusable template from reasoning steps.
        Replaces specific details with placeholders.
        """
        template_steps = []
        for step in reasoning_steps:
            # Replace specific numbers, names, dates with placeholders
            templated = re.sub(r'\b\d{4}\b', '[YEAR]', step)
            templated = re.sub(r'\b\d+\.\d+\b', '[NUMBER]', templated)
            templated = re.sub(r'\b\d+\b', '[N]', templated)
            templated = re.sub(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', '[NAME]', templated)
            template_steps.append(templated)
        
        return "\n".join(f"{i+1}. {step}" for i, step in enumerate(template_steps))

    # ---- Search and retrieve ----

    def find_matching_chain(
        self,
        task_type: str,
        domain: Optional[str] = None,
        keywords: Optional[List[str]] = None,
        complexity: Optional[Literal["simple", "medium", "complex"]] = None,
        prefer_golden: bool = True,
    ) -> Optional[ChainMatch]:
        """
        Find the best matching thought-chain for a given task.
        Returns None if no suitable match is found.
        """
        candidates = list(self._index.values())
        
        if not candidates:
            return None
        
        # Filter by task type (required)
        candidates = [c for c in candidates if c.task_type == task_type]
        
        if not candidates:
            return None
        
        # Prefer golden chains if requested
        if prefer_golden:
            golden_candidates = [c for c in candidates if c.chain_id in self._golden_chains]
            if golden_candidates:
                candidates = golden_candidates
        
        # Score each candidate
        scored = []
        for chain in candidates:
            score = 0.0
            reasons = []
            
            # Domain match (high weight)
            if domain and chain.domain.lower() == domain.lower():
                score += 50.0
                reasons.append("domain_match")
            
            # Complexity match (medium weight)
            if complexity and chain.complexity == complexity:
                score += 20.0
                reasons.append("complexity_match")
            
            # Keyword overlap (variable weight)
            if keywords:
                query_kw = set(kw.lower().strip() for kw in keywords)
                chain_kw = set(chain.keywords)
                overlap = query_kw & chain_kw
                if overlap:
                    overlap_ratio = len(overlap) / len(query_kw)
                    score += overlap_ratio * 30.0
                    reasons.append(f"keyword_overlap_{len(overlap)}")
            
            # Status bonus
            if chain.status == "golden":
                score += 15.0
                reasons.append("golden_status")
            elif chain.status == "validated":
                score += 5.0
                reasons.append("validated_status")
            
            # Success rate bonus
            if chain.reuse_count > 0:
                score += chain.success_rate * 10.0
                reasons.append(f"success_rate_{chain.success_rate:.2f}")
            
            scored.append((chain, score, reasons))
        
        # Sort by score descending
        scored.sort(key=lambda x: x[1], reverse=True)
        
        # Return best match if score is above threshold
        best_chain, best_score, best_reasons = scored[0]
        if best_score >= 30.0:  # Minimum threshold
            return ChainMatch(
                chain=best_chain,
                similarity_score=round(best_score, 2),
                match_reason=", ".join(best_reasons),
            )
        
        return None

    def get_chain(self, chain_id: str) -> Optional[ThoughtChain]:
        """Retrieve a specific chain by ID."""
        return self._index.get(chain_id)

    def list_chains(
        self,
        task_type: Optional[str] = None,
        domain: Optional[str] = None,
        status: Optional[Literal["experimental", "validated", "golden"]] = None,
    ) -> List[ThoughtChain]:
        """List all chains, optionally filtered."""
        chains = list(self._index.values())
        
        if task_type:
            chains = [c for c in chains if c.task_type == task_type]
        if domain:
            chains = [c for c in chains if c.domain.lower() == domain.lower()]
        if status:
            chains = [c for c in chains if c.status == status]
        
        return sorted(chains, key=lambda c: c.captured_at, reverse=True)

    # ---- Chain management ----

    def mark_as_golden(self, chain_id: str):
        """Mark a chain as 'golden' (always reuse)."""
        if chain_id in self._index:
            self._index[chain_id].status = "golden"
            if chain_id not in self._golden_chains:
                self._golden_chains.append(chain_id)
            self._save_index()

    def mark_as_validated(self, chain_id: str):
        """Mark a chain as 'validated' (proven useful)."""
        if chain_id in self._index:
            self._index[chain_id].status = "validated"
            self._save_index()

    def record_reuse(self, chain_id: str, success: bool):
        """Record that a chain was reused and whether it was successful."""
        if chain_id in self._index:
            chain = self._index[chain_id]
            chain.reuse_count += 1
            # Update success rate using exponential moving average
            alpha = 0.2  # Weight for new observation
            new_success = 1.0 if success else 0.0
            chain.success_rate = (1 - alpha) * chain.success_rate + alpha * new_success
            self._save_index()

    def delete_chain(self, chain_id: str):
        """Remove a chain from the cache."""
        if chain_id in self._index:
            del self._index[chain_id]
            if chain_id in self._golden_chains:
                self._golden_chains.remove(chain_id)
            self._save_index()

    # ---- Statistics ----

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        chains = list(self._index.values())
        
        if not chains:
            return {
                "total_chains": 0,
                "golden_chains": 0,
                "validated_chains": 0,
                "experimental_chains": 0,
                "total_reuses": 0,
                "avg_success_rate": 0.0,
                "task_types": {},
                "domains": {},
            }
        
        task_type_counts = defaultdict(int)
        domain_counts = defaultdict(int)
        
        for chain in chains:
            task_type_counts[chain.task_type] += 1
            domain_counts[chain.domain] += 1
        
        reused_chains = [c for c in chains if c.reuse_count > 0]
        
        return {
            "total_chains": len(chains),
            "golden_chains": len([c for c in chains if c.status == "golden"]),
            "validated_chains": len([c for c in chains if c.status == "validated"]),
            "experimental_chains": len([c for c in chains if c.status == "experimental"]),
            "total_reuses": sum(c.reuse_count for c in chains),
            "avg_success_rate": round(
                sum(c.success_rate for c in reused_chains) / len(reused_chains), 4
            ) if reused_chains else 0.0,
            "task_types": dict(task_type_counts),
            "domains": dict(domain_counts),
        }

    # ---- Export/Import ----

    def export_chain(self, chain_id: str, output_path: str):
        """Export a single chain to a JSON file."""
        chain = self.get_chain(chain_id)
        if chain:
            with open(output_path, "w") as f:
                json.dump(chain.to_dict(), f, indent=2)

    def import_chain(self, input_path: str) -> ThoughtChain:
        """Import a chain from a JSON file."""
        with open(input_path) as f:
            data = json.load(f)
            chain = ThoughtChain.from_dict(data)
            self._index[chain.chain_id] = chain
            self._save_index()
            return chain


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Kimi K2 Thought-Chain Cache — Demo")
    print("=" * 50)

    cache = ThoughtChainCache()

    # Demo: capture a chain
    demo_response = """
    To solve this problem, I'll follow these steps:
    
    1. First, analyze the input data structure and identify key patterns.
    2. Next, apply a filtering algorithm to remove noise and outliers.
    3. Then, use a clustering approach to group similar items.
    4. Finally, rank the clusters by relevance and return the top results.
    
    This approach ensures both accuracy and efficiency.
    """

    chain = cache.capture_chain(
        task_type="data_analysis",
        domain="clustering",
        complexity="medium",
        keywords=["clustering", "filtering", "ranking"],
        original_prompt="How do I cluster and rank similar items from noisy data?",
        original_response=demo_response,
    )

    print(f"Captured chain: {chain.chain_id}")
    print(f"  Task: {chain.task_type}")
    print(f"  Domain: {chain.domain}")
    print(f"  Steps: {len(chain.reasoning_steps)}")
    print(f"\nTemplate:\n{chain.template}")

    # Demo: find matching chain
    match = cache.find_matching_chain(
        task_type="data_analysis",
        domain="clustering",
        keywords=["clustering", "grouping"],
    )

    if match:
        print(f"\nFound matching chain!")
        print(f"  Chain ID: {match.chain.chain_id}")
        print(f"  Similarity: {match.similarity_score}")
        print(f"  Reason: {match.match_reason}")
    else:
        print("\nNo matching chain found.")

    # Demo: stats
    stats = cache.get_stats()
    print(f"\nCache Stats:")
    print(f"  Total chains: {stats['total_chains']}")
    print(f"  Golden chains: {stats['golden_chains']}")
    print(f"  Task types: {stats['task_types']}")
