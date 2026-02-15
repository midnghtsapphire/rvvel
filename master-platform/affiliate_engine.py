"""
Master Platform: Affiliate Auto-Linker Engine
==============================================
Automatically generates affiliate links for ANY product mentioned across the platform.
Tracks clicks, conversions, and revenue per link.

Author: Audrey Evans
"""

import os
import re
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Optional, Any, Literal
from dataclasses import dataclass, field, asdict
from urllib.parse import quote_plus

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Amazon Associates tracking ID
AMAZON_ASSOCIATE_TAG = os.environ.get("AMAZON_ASSOCIATE_TAG", "audreyevans-20")

# Affiliate networks
AFFILIATE_NETWORKS = {
    "amazon": {
        "base_url": "https://www.amazon.com/s?k={query}&tag={tag}",
        "product_url": "https://www.amazon.com/dp/{asin}?tag={tag}",
    },
    "target": {
        "base_url": "https://www.target.com/s?searchTerm={query}",
    },
    "ulta": {
        "base_url": "https://www.ulta.com/search?query={query}",
    },
    "sephora": {
        "base_url": "https://www.sephora.com/search?keyword={query}",
    },
}

DATA_DIR = Path(__file__).parent / "data" / "affiliate_links"
LINK_INDEX = DATA_DIR / "link_index.json"
ANALYTICS_FILE = DATA_DIR / "analytics.json"


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

@dataclass
class AffiliateLink:
    """A generated affiliate link."""
    link_id: str
    product_name: str
    product_category: str
    network: str  # amazon, target, ulta, sephora, etc.
    affiliate_url: str
    created_at: str
    source_context: str  # Where the product was mentioned
    clicks: int = 0
    conversions: int = 0
    revenue_usd: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "AffiliateLink":
        return cls(**d)


@dataclass
class ProductMention:
    """A detected product mention in text."""
    product_name: str
    product_category: str
    confidence: float  # 0.0 - 1.0
    context: str
    suggested_network: str = "amazon"


# ---------------------------------------------------------------------------
# Affiliate Engine
# ---------------------------------------------------------------------------

class AffiliateEngine:
    """
    Automatically detects product mentions and generates affiliate links.
    Works across ALL apps and ALL websites.
    """

    def __init__(self, amazon_tag: Optional[str] = None):
        self.amazon_tag = amazon_tag or AMAZON_ASSOCIATE_TAG
        self.data_dir = DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.link_index_path = self.data_dir / "link_index.json"
        self.analytics_path = self.data_dir / "analytics.json"
        self._link_index: Dict[str, AffiliateLink] = {}
        self._load_index()

    # ---- Index management ----

    def _load_index(self):
        """Load the link index from disk."""
        if self.link_index_path.exists():
            with open(self.link_index_path) as f:
                data = json.load(f)
                self._link_index = {k: AffiliateLink.from_dict(v) for k, v in data.items()}

    def _save_index(self):
        """Persist the link index to disk."""
        with open(self.link_index_path, "w") as f:
            json.dump({k: v.to_dict() for k, v in self._link_index.items()}, f, indent=2)

    # ---- Product detection ----

    def detect_products(self, text: str, context: str = "") -> List[ProductMention]:
        """
        Detect product mentions in text using pattern matching and heuristics.
        
        Args:
            text: The text to analyze
            context: Context about where this text came from
        
        Returns:
            List of detected product mentions
        """
        mentions = []
        
        # Pattern 1: Brand + Product Name (e.g., "CeraVe Hydrating Cleanser")
        brand_product_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3})\b'
        matches = re.findall(brand_product_pattern, text)
        
        for brand, product in matches:
            full_name = f"{brand} {product}"
            category = self._infer_category(full_name, text)
            
            mentions.append(ProductMention(
                product_name=full_name,
                product_category=category,
                confidence=0.8,
                context=context,
                suggested_network="amazon",
            ))
        
        # Pattern 2: Quoted product names (e.g., "Salicylic Acid 2% Solution")
        quoted_pattern = r'"([^"]+)"'
        quoted_matches = re.findall(quoted_pattern, text)
        
        for quoted in quoted_matches:
            if len(quoted.split()) >= 2 and len(quoted) < 100:
                category = self._infer_category(quoted, text)
                mentions.append(ProductMention(
                    product_name=quoted,
                    product_category=category,
                    confidence=0.7,
                    context=context,
                    suggested_network="amazon",
                ))
        
        # Pattern 3: Skincare/makeup keywords
        skincare_keywords = [
            "cleanser", "moisturizer", "serum", "sunscreen", "toner", "exfoliant",
            "retinol", "vitamin c", "hyaluronic acid", "niacinamide", "salicylic acid",
            "foundation", "concealer", "mascara", "lipstick", "blush", "eyeshadow",
            "primer", "setting spray", "highlighter", "bronzer", "eyeliner",
        ]
        
        for keyword in skincare_keywords:
            if keyword.lower() in text.lower():
                # Find surrounding context
                pattern = rf'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+{re.escape(keyword)}\b'
                keyword_matches = re.findall(pattern, text, re.IGNORECASE)
                
                for brand in keyword_matches:
                    full_name = f"{brand} {keyword.title()}"
                    category = self._infer_category(full_name, text)
                    
                    mentions.append(ProductMention(
                        product_name=full_name,
                        product_category=category,
                        confidence=0.75,
                        context=context,
                        suggested_network="amazon",
                    ))
        
        # Deduplicate
        seen = set()
        unique_mentions = []
        for mention in mentions:
            key = mention.product_name.lower()
            if key not in seen:
                seen.add(key)
                unique_mentions.append(mention)
        
        return unique_mentions

    def _infer_category(self, product_name: str, context: str) -> str:
        """Infer product category from name and context."""
        product_lower = product_name.lower()
        context_lower = context.lower()
        
        # Skincare
        skincare_terms = ["cleanser", "moisturizer", "serum", "sunscreen", "toner", "cream", "lotion", "oil", "balm"]
        if any(term in product_lower for term in skincare_terms):
            return "skincare"
        
        # Makeup
        makeup_terms = ["foundation", "concealer", "mascara", "lipstick", "blush", "eyeshadow", "primer", "highlighter", "bronzer", "eyeliner"]
        if any(term in product_lower for term in makeup_terms):
            return "makeup"
        
        # Haircare
        haircare_terms = ["shampoo", "conditioner", "hair", "scalp"]
        if any(term in product_lower for term in haircare_terms):
            return "haircare"
        
        # Wellness
        wellness_terms = ["vitamin", "supplement", "nad+", "iv", "therapy"]
        if any(term in product_lower for term in wellness_terms):
            return "wellness"
        
        # From context
        if "skin" in context_lower or "face" in context_lower:
            return "skincare"
        if "makeup" in context_lower or "cosmetic" in context_lower:
            return "makeup"
        
        return "general"

    # ---- Link generation ----

    def generate_link(
        self,
        product_name: str,
        product_category: str = "general",
        network: str = "amazon",
        source_context: str = "",
        asin: Optional[str] = None,
    ) -> AffiliateLink:
        """
        Generate an affiliate link for a product.
        
        Args:
            product_name: Name of the product
            product_category: Category (skincare, makeup, etc.)
            network: Affiliate network (amazon, target, etc.)
            source_context: Where the product was mentioned
            asin: Amazon ASIN (if known)
        
        Returns:
            AffiliateLink object
        """
        # Generate link ID
        link_id = hashlib.sha256(
            f"{product_name}:{network}:{datetime.now(timezone.utc).isoformat()}".encode()
        ).hexdigest()[:16]
        
        # Generate affiliate URL
        if network == "amazon":
            if asin:
                url = AFFILIATE_NETWORKS["amazon"]["product_url"].format(
                    asin=asin,
                    tag=self.amazon_tag,
                )
            else:
                query = quote_plus(product_name)
                url = AFFILIATE_NETWORKS["amazon"]["base_url"].format(
                    query=query,
                    tag=self.amazon_tag,
                )
        else:
            network_config = AFFILIATE_NETWORKS.get(network, AFFILIATE_NETWORKS["amazon"])
            query = quote_plus(product_name)
            url = network_config["base_url"].format(query=query)
        
        # Create link object
        link = AffiliateLink(
            link_id=link_id,
            product_name=product_name,
            product_category=product_category,
            network=network,
            affiliate_url=url,
            created_at=datetime.now(timezone.utc).isoformat(),
            source_context=source_context,
        )
        
        # Store in index
        self._link_index[link_id] = link
        self._save_index()
        
        return link

    def auto_link_text(self, text: str, context: str = "") -> tuple[str, List[AffiliateLink]]:
        """
        Automatically detect products in text and replace with affiliate links.
        
        Args:
            text: The text to process
            context: Context about where this text came from
        
        Returns:
            Tuple of (modified_text, list_of_generated_links)
        """
        mentions = self.detect_products(text, context)
        generated_links = []
        modified_text = text
        
        for mention in mentions:
            # Generate link
            link = self.generate_link(
                product_name=mention.product_name,
                product_category=mention.product_category,
                network=mention.suggested_network,
                source_context=context,
            )
            generated_links.append(link)
            
            # Replace in text (first occurrence only)
            # Wrap in markdown link: [Product Name](affiliate_url)
            markdown_link = f"[{mention.product_name}]({link.affiliate_url})"
            modified_text = modified_text.replace(mention.product_name, markdown_link, 1)
        
        return modified_text, generated_links

    # ---- Analytics ----

    def record_click(self, link_id: str):
        """Record a click on an affiliate link."""
        if link_id in self._link_index:
            self._link_index[link_id].clicks += 1
            self._save_index()
            self._update_analytics()

    def record_conversion(self, link_id: str, revenue_usd: float):
        """Record a conversion (purchase) from an affiliate link."""
        if link_id in self._link_index:
            self._link_index[link_id].conversions += 1
            self._link_index[link_id].revenue_usd += revenue_usd
            self._save_index()
            self._update_analytics()

    def _update_analytics(self):
        """Update aggregate analytics."""
        total_clicks = sum(link.clicks for link in self._link_index.values())
        total_conversions = sum(link.conversions for link in self._link_index.values())
        total_revenue = sum(link.revenue_usd for link in self._link_index.values())
        
        analytics = {
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "total_links": len(self._link_index),
            "total_clicks": total_clicks,
            "total_conversions": total_conversions,
            "total_revenue_usd": round(total_revenue, 2),
            "conversion_rate": round(total_conversions / total_clicks, 4) if total_clicks > 0 else 0.0,
            "avg_revenue_per_click": round(total_revenue / total_clicks, 2) if total_clicks > 0 else 0.0,
        }
        
        with open(self.analytics_path, "w") as f:
            json.dump(analytics, f, indent=2)

    def get_analytics(self) -> Dict[str, Any]:
        """Get aggregate analytics."""
        if self.analytics_path.exists():
            with open(self.analytics_path) as f:
                return json.load(f)
        return {}

    def get_top_performers(self, limit: int = 10) -> List[AffiliateLink]:
        """Get top-performing affiliate links by revenue."""
        links = list(self._link_index.values())
        return sorted(links, key=lambda l: l.revenue_usd, reverse=True)[:limit]

    def get_links_by_category(self, category: str) -> List[AffiliateLink]:
        """Get all links for a specific product category."""
        return [link for link in self._link_index.values() if link.product_category == category]

    def get_links_by_network(self, network: str) -> List[AffiliateLink]:
        """Get all links for a specific affiliate network."""
        return [link for link in self._link_index.values() if link.network == network]

    # ---- Bulk processing ----

    def process_content_batch(self, content_items: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Process a batch of content items and generate affiliate links.
        
        Args:
            content_items: List of dicts with 'text' and 'context' keys
        
        Returns:
            Summary of processing results
        """
        results = {
            "total_items": len(content_items),
            "total_mentions": 0,
            "total_links": 0,
            "items": [],
        }
        
        for item in content_items:
            text = item.get("text", "")
            context = item.get("context", "")
            
            modified_text, links = self.auto_link_text(text, context)
            
            results["total_mentions"] += len(links)
            results["total_links"] += len(links)
            results["items"].append({
                "original_text": text,
                "modified_text": modified_text,
                "links_generated": len(links),
                "links": [link.to_dict() for link in links],
            })
        
        return results


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Master Platform: Affiliate Auto-Linker Engine — Demo")
    print("=" * 50)

    engine = AffiliateEngine()

    # Demo text with product mentions
    demo_text = """
    For oily skin, I recommend the CeraVe Foaming Facial Cleanser. 
    Follow up with The Ordinary Niacinamide 10% + Zinc 1% to minimize pores.
    Don't forget sunscreen — try EltaMD UV Clear SPF 46.
    """

    print("\nOriginal text:")
    print(demo_text)

    # Auto-link
    modified_text, links = engine.auto_link_text(demo_text, context="skincare_recommendation")

    print("\nModified text with affiliate links:")
    print(modified_text)

    print(f"\nGenerated {len(links)} affiliate links:")
    for link in links:
        print(f"  - {link.product_name} ({link.network})")
        print(f"    URL: {link.affiliate_url}")

    # Analytics
    analytics = engine.get_analytics()
    print(f"\nAnalytics:")
    print(f"  Total links: {analytics.get('total_links', 0)}")
    print(f"  Total clicks: {analytics.get('total_clicks', 0)}")
    print(f"  Total revenue: ${analytics.get('total_revenue_usd', 0)}")
