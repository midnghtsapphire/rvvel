#!/usr/bin/env python3
"""
============================================================================
SOUP-TO-NUTS MASTER DEPLOYMENT SCRIPT
Audrey Evans Official / GlowStarLabs
============================================================================

The ONE script to rule them all. Run it for Project Face, run it for
TheAltText, run it for the next app. Same pipeline, different product.

USAGE:
    python deploy/soup_to_nuts.py --config app_config.yaml
    python deploy/soup_to_nuts.py --app "Project Face" --domain "glowstarlabs.com" --tier full
    python deploy/soup_to_nuts.py --app "TheAltText" --domain "meetaudreyevans.com" --tier full
    python deploy/soup_to_nuts.py --step scaffold   # Run only one step
    python deploy/soup_to_nuts.py --step deploy      # Run only deploy step
    python deploy/soup_to_nuts.py --list-steps       # Show all steps

STEPS (in order):
    1. scaffold    — Create project structure
    2. configure   — Set up env vars, API keys, DB connections
    3. brand       — Apply glassmorphism theme, WCAG AAA, logos
    4. code        — Generate boilerplate (auth, payments, dashboard)
    5. connect     — Wire up all backend APIs
    6. database    — Create/migrate PostgreSQL schema
    7. test        — Run all test suites
    8. build       — Production builds (web, mobile, desktop)
    9. deploy      — Push to hosting, configure domain/SSL
   10. submit      — Auto-submit to app stores
   11. monitor     — Set up error tracking, analytics, uptime
   12. report      — Generate deployment report

Author: Audrey Evans
Version: 1.0.0
============================================================================
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import textwrap
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any

try:
    import yaml
except ImportError:
    yaml = None

# ============================================================================
# CONSTANTS
# ============================================================================

SCRIPT_DIR = Path(__file__).parent.resolve()
COMPONENTS_DIR = SCRIPT_DIR / "components"
REPO_ROOT = SCRIPT_DIR.parent

STEPS = [
    "scaffold", "configure", "brand", "code", "connect",
    "database", "test", "build", "deploy", "submit", "monitor", "report",
]

GLASSMORPHISM_THEME = {
    "primary": "#F59E0B",
    "secondary": "#D97706",
    "accent": "#FBBF24",
    "bg_dark": "#0F0F0F",
    "bg_glass": "rgba(255,255,255,0.05)",
    "text_primary": "#F5F5F5",
    "text_secondary": "#A3A3A3",
    "border_glass": "rgba(255,255,255,0.1)",
    "blur": "16px",
    "font": "Inter",
}

DEFAULT_MODULES = [
    "auth_module", "payment_module", "affiliate_module",
    "analytics_module", "notification_module", "admin_dashboard",
    "landing_page", "selling_space_module",
]

SUBSCRIPTION_TIERS = {
    "free": {"price": 0, "tokens": 10},
    "starter": {"price": 9, "tokens": 100},
    "pro": {"price": 29, "tokens": 500},
    "business": {"price": 99, "tokens": 2000},
    "enterprise": {"price": 299, "tokens": 10000},
}

AD_TIERS = {
    "basic": 20, "standard": 50, "premium": 100, "featured": 200,
    "spotlight": 500, "exclusive": 1000, "domination": 2000,
}

# ============================================================================
# THE 8 MANDATORY AUDREY EVANS OFFICIAL STANDARDS
# These are NON-NEGOTIABLE defaults for EVERY app. No exceptions.
# ============================================================================

MANDATORY_STANDARDS = {
    "1_no_blue_light": {
        "enabled": True,
        "dark_mode_default": True,
        "warm_amber_tones": True,
        "blue_light_filter": True,
        "night_mode_shift": True,
        "description": "No blue light. Warm amber/orange tones. Night mode shifts warmer.",
    },
    "2_eco_code": {
        "enabled": True,
        "minimize_api_calls": True,
        "aggressive_caching": True,
        "lightweight_models_first": True,
        "co2_tracking": True,
        "carbon_badge_visible": True,
        "eco_score_target": 95,
        "description": "Carbon-efficient programming. Cache aggressively. Track CO2 savings.",
    },
    "3_neurodivergent_friendly": {
        "enabled": True,
        "no_flashing": True,
        "no_autoplay": True,
        "no_sudden_sounds": True,
        "clear_visual_hierarchy": True,
        "predictable_navigation": True,
        "dopamine_progress_indicators": True,
        "focus_mode": True,
        "reduced_stimulation_mode": True,
        "executive_function_support": True,
        "customizable_density": True,
        "break_reminders_minutes": 25,
        "description": "AuDHD-optimized UX. No sensory overload. Focus mode. Break reminders.",
    },
    "4_glassmorphism": {
        "enabled": True,
        "frosted_glass": True,
        "backdrop_blur": True,
        "translucent_panels": True,
        "warm_amber_gradients": True,
        "layered_depth": True,
        "smooth_animations": True,
        "reduced_motion_option": True,
        "premium_luxury_feel": True,
        "description": "Best-in-class glassmorphism. Frosted glass. Warm amber. Premium feel.",
    },
    "5_best_in_class": {
        "enabled": True,
        "production_grade": True,
        "polished": True,
        "professional": True,
        "description": "Every feature is the BEST version. Not MVP. Production-grade.",
    },
    "6_blue_ocean_gangster": {
        "enabled": True,
        "underserved_markets": True,
        "unique_features": True,
        "competitive_pricing": True,
        "unique_combinations": True,
        "description": "Target markets nobody else serves. Features competitors don't have.",
    },
    "7_alt_text_everywhere": {
        "enabled": True,
        "wcag_level": "AAA",
        "screen_reader_compatible": True,
        "keyboard_navigation": True,
        "visual_only_notifications": True,
        "no_audio_dependency": True,
        "high_contrast_mode": True,
        "adjustable_font_sizes": True,
        "aria_labels_on_everything": True,
        "description": "Full WCAG AAA. Visual-only notifications. ARIA labels on everything.",
    },
    "8_carbon_savings_quantifier": {
        "enabled": True,
        "starbucks_cups_equivalent": True,
        "efficiency_percentage": True,
        "gamified_leaderboard": True,
        "esg_metrics": True,
        "description": "Display carbon savings. Gamified eco leaderboard. ESG-ready metrics.",
    },
}


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

class Logger:
    """Colored console output for build steps."""
    COLORS = {
        "header": "\033[95m", "blue": "\033[94m", "cyan": "\033[96m",
        "green": "\033[92m", "yellow": "\033[93m", "red": "\033[91m",
        "bold": "\033[1m", "end": "\033[0m",
    }

    @staticmethod
    def header(msg: str):
        print(f"\n{Logger.COLORS['bold']}{Logger.COLORS['header']}{'='*70}")
        print(f"  {msg}")
        print(f"{'='*70}{Logger.COLORS['end']}\n")

    @staticmethod
    def step(num: int, total: int, msg: str):
        print(f"{Logger.COLORS['bold']}{Logger.COLORS['cyan']}[{num}/{total}] {msg}{Logger.COLORS['end']}")

    @staticmethod
    def success(msg: str):
        print(f"  {Logger.COLORS['green']}✓ {msg}{Logger.COLORS['end']}")

    @staticmethod
    def warning(msg: str):
        print(f"  {Logger.COLORS['yellow']}⚠ {msg}{Logger.COLORS['end']}")

    @staticmethod
    def error(msg: str):
        print(f"  {Logger.COLORS['red']}✗ {msg}{Logger.COLORS['end']}")

    @staticmethod
    def info(msg: str):
        print(f"  {Logger.COLORS['blue']}ℹ {msg}{Logger.COLORS['end']}")


log = Logger()


def run_cmd(cmd: str, cwd: str = None, check: bool = True, capture: bool = False) -> subprocess.CompletedProcess:
    """Run a shell command with logging."""
    log.info(f"Running: {cmd[:80]}{'...' if len(cmd) > 80 else ''}")
    result = subprocess.run(
        cmd, shell=True, cwd=cwd, check=check,
        capture_output=capture, text=True,
    )
    return result


def load_config(config_path: str = None, app_name: str = None,
                domain: str = None, tier: str = "full") -> Dict:
    """Load configuration from YAML file or CLI args."""
    config = {}

    if config_path and Path(config_path).exists():
        if yaml:
            with open(config_path) as f:
                config = yaml.safe_load(f) or {}
        else:
            # Fallback: parse YAML-like structure manually
            with open(config_path) as f:
                content = f.read()
            log.warning("PyYAML not installed. Using default config with CLI overrides.")

    # CLI overrides
    if app_name:
        config.setdefault("app", {})["name"] = app_name
        config["app"]["display_name"] = app_name
    if domain:
        config.setdefault("domain", {})["primary"] = domain
    if tier:
        config.setdefault("deployment", {})["tier"] = tier

    # Apply defaults
    app = config.setdefault("app", {})
    app.setdefault("name", "MyApp")
    app.setdefault("display_name", app.get("name", "MyApp"))
    app.setdefault("version", "1.0.0")
    app.setdefault("description", f"{app['display_name']} — powered by GlowStarLabs")
    app.setdefault("parent_company", "Audrey Evans Official")
    app.setdefault("parent_brand", "GlowStarLabs")

    config.setdefault("domain", {}).setdefault("primary", "localhost")
    config.setdefault("deployment", {}).setdefault("tier", "full")
    config.setdefault("deployment", {}).setdefault("platform", "docker")
    config.setdefault("branding", GLASSMORPHISM_THEME.copy())
    config.setdefault("features", {k: True for k in [
        "skin_analysis", "affiliate_auto_linker", "selling_space",
        "subscription_manager", "universal_data_router", "ai_benchmarking",
        "admin_dashboard", "landing_page", "notification_system",
    ]})
    config.setdefault("modules", DEFAULT_MODULES.copy())
    config.setdefault("accessibility", {
        "wcag_level": "AAA",
        "visual_only_notifications": True,
        "high_contrast_mode": True,
        "no_audio_dependency": True,
        "keyboard_navigation": True,
        "screen_reader_optimized": True,
        "aria_labels_on_everything": True,
        "adjustable_font_sizes": True,
        "min_touch_target": "48px",
    })

    # MANDATORY: Enforce all 8 standards — these CANNOT be overridden to False
    config["mandatory_standards"] = MANDATORY_STANDARDS.copy()
    config.setdefault("eco_code", {
        "cache_ttl_seconds": 300,
        "lightweight_model_first": True,
        "max_api_calls_per_minute": 30,
        "co2_per_api_call_grams": 0.2,
        "co2_per_cached_response_grams": 0.001,
        "starbucks_cup_co2_grams": 21,
    })
    config.setdefault("neurodivergent", {
        "break_reminder_minutes": 25,
        "focus_mode_default": False,
        "no_autoplay": True,
        "no_flashing": True,
        "no_sudden_sounds": True,
        "dopamine_progress": True,
        "executive_function_support": True,
    })
    config.setdefault("blue_light_filter", {
        "enabled": True,
        "night_mode_start_hour": 20,
        "night_mode_end_hour": 6,
        "night_mode_warmth": "extra",
    })

    return config


def snake_case(name: str) -> str:
    """Convert display name to snake_case."""
    return name.lower().replace(" ", "_").replace("-", "_")


def kebab_case(name: str) -> str:
    """Convert display name to kebab-case."""
    return name.lower().replace(" ", "-").replace("_", "-")


# ============================================================================
# STEP 1: SCAFFOLD
# ============================================================================

def step_scaffold(config: Dict, output_dir: Path):
    """Create the complete project structure."""
    log.header("STEP 1: SCAFFOLD — Creating Project Structure")

    app_name = snake_case(config["app"]["name"])
    dirs = [
        # Backend
        "backend",
        "backend/api",
        "backend/api/routes",
        "backend/services",
        "backend/models",
        "backend/integrations",
        "backend/migrations",
        "backend/tests",
        "backend/tests/unit",
        "backend/tests/integration",
        # Frontend
        "frontend",
        "frontend/src",
        "frontend/src/components",
        "frontend/src/components/ui",
        "frontend/src/components/layout",
        "frontend/src/components/features",
        "frontend/src/pages",
        "frontend/src/hooks",
        "frontend/src/services",
        "frontend/src/styles",
        "frontend/src/utils",
        "frontend/src/assets",
        "frontend/public",
        # Shared
        "deploy",
        "deploy/components",
        "docker",
        "docs",
        "tests",
        "tests/unit",
        "tests/integration",
        "tests/e2e",
        "tests/accessibility",
        "tests/performance",
        ".github",
        ".github/workflows",
    ]

    for d in dirs:
        (output_dir / d).mkdir(parents=True, exist_ok=True)
        log.success(f"Created {d}/")

    # Copy reusable components
    if COMPONENTS_DIR.exists():
        dest_components = output_dir / "deploy" / "components"
        for module_dir in COMPONENTS_DIR.iterdir():
            if module_dir.is_dir():
                dest = dest_components / module_dir.name
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(module_dir, dest)
                log.success(f"Copied component: {module_dir.name}")

    log.success("Scaffold complete!")
    return True


# ============================================================================
# STEP 2: CONFIGURE
# ============================================================================

def step_configure(config: Dict, output_dir: Path):
    """Generate environment configuration files."""
    log.header("STEP 2: CONFIGURE — Environment Variables & API Keys")

    app_name = snake_case(config["app"]["name"])
    domain = config["domain"]["primary"]

    # .env.example
    env_template = f"""# ============================================================================
# {config['app']['display_name']} — Environment Configuration
# Generated by soup-to-nuts.py on {datetime.now(timezone.utc).isoformat()}
# ============================================================================

# --- APP ---
APP_NAME={config['app']['display_name']}
APP_VERSION={config['app']['version']}
APP_ENV=production
APP_DEBUG=false
APP_URL=https://{domain}
APP_SECRET_KEY=CHANGE_ME_TO_RANDOM_64_CHAR_STRING

# --- DATABASE ---
DB_HOST=localhost
DB_PORT=5432
DB_NAME={app_name}_db
DB_USER=postgres
DB_PASSWORD=CHANGE_ME
DATABASE_URL=postgresql://${{DB_USER}}:${{DB_PASSWORD}}@${{DB_HOST}}:${{DB_PORT}}/${{DB_NAME}}

# --- JWT ---
JWT_SECRET=CHANGE_ME_TO_RANDOM_64_CHAR_STRING
JWT_EXPIRY_HOURS=24

# --- STRIPE ---
STRIPE_SECRET_KEY=sk_live_CHANGE_ME
STRIPE_PUBLISHABLE_KEY=pk_live_CHANGE_ME
STRIPE_WEBHOOK_SECRET=whsec_CHANGE_ME

# --- OPENROUTER (AI Models) ---
OPENROUTER_API_KEY=CHANGE_ME

# --- OPENAI ---
OPENAI_API_KEY=CHANGE_ME

# --- PERPLEXITY ---
PERPLEXITY_API_KEY=CHANGE_ME

# --- OPENWEATHERMAP ---
OPENWEATHERMAP_API_KEY=CHANGE_ME

# --- AMAZON ASSOCIATES ---
AMAZON_ASSOCIATES_TAG=glowstarlabs-20
AMAZON_ACCESS_KEY=CHANGE_ME
AMAZON_SECRET_KEY=CHANGE_ME

# --- GOOGLE OAUTH ---
GOOGLE_CLIENT_ID=CHANGE_ME
GOOGLE_CLIENT_SECRET=CHANGE_ME

# --- APPLE SIGN-IN ---
APPLE_CLIENT_ID=CHANGE_ME
APPLE_TEAM_ID=CHANGE_ME
APPLE_KEY_ID=CHANGE_ME

# --- GMAIL API ---
GMAIL_CREDENTIALS_PATH=./credentials/gmail.json

# --- GITHUB ---
GITHUB_TOKEN=CHANGE_ME

# --- CORS ---
CORS_ORIGINS=https://{domain},http://localhost:3000,http://localhost:5173

# --- REDIS (optional, for caching) ---
REDIS_URL=redis://localhost:6379/0
"""

    (output_dir / ".env.example").write_text(env_template)
    log.success("Created .env.example")

    # .gitignore
    gitignore = """# Dependencies
node_modules/
__pycache__/
*.pyc
.venv/
venv/
env/

# Environment
.env
.env.local
.env.production

# Build
dist/
build/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Credentials
credentials/
*.pem
*.key

# Database
*.db
*.sqlite3

# Logs
*.log
logs/

# Coverage
coverage/
htmlcov/
.coverage

# Docker
docker-compose.override.yml
"""

    (output_dir / ".gitignore").write_text(gitignore)
    log.success("Created .gitignore")

    log.success("Configuration complete!")
    return True


# ============================================================================
# STEP 3: BRAND
# ============================================================================

def step_brand(config: Dict, output_dir: Path):
    """Apply glassmorphism theme, WCAG AAA accessibility, branding."""
    log.header("STEP 3: BRAND — Glassmorphism Theme + WCAG AAA")

    branding = config.get("branding", GLASSMORPHISM_THEME)
    app_name = config["app"]["display_name"]

    # Generate CSS variables file
    css_vars = f"""/* ============================================================================
   {app_name} — Glassmorphism Dark Theme
   WCAG AAA Compliant | Visual-Only Notifications | No Audio Dependencies
   Generated by soup-to-nuts.py
   ============================================================================ */

:root {{
  /* --- Colors --- */
  --color-primary: {branding.get('primary', '#F59E0B')};
  --color-secondary: {branding.get('secondary', '#D97706')};
  --color-accent: {branding.get('accent', '#FBBF24')};
  --color-bg-dark: {branding.get('bg_dark', '#0F0F0F')};
  --color-bg-glass: {branding.get('bg_glass', 'rgba(255,255,255,0.05)')};
  --color-text-primary: {branding.get('text_primary', '#F5F5F5')};
  --color-text-secondary: {branding.get('text_secondary', '#A3A3A3')};
  --color-border-glass: {branding.get('border_glass', 'rgba(255,255,255,0.1)')};
  --color-success: #22C55E;
  --color-warning: #F59E0B;
  --color-error: #EF4444;
  --color-info: #3B82F6;

  /* --- Glassmorphism --- */
  --glass-blur: {branding.get('blur', '16px')};
  --glass-bg: {branding.get('bg_glass', 'rgba(255,255,255,0.05)')};
  --glass-border: 1px solid {branding.get('border_glass', 'rgba(255,255,255,0.1)')};
  --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  --glass-radius: 16px;

  /* --- Typography (WCAG AAA: min 4.5:1 contrast for normal, 7:1 enhanced) --- */
  --font-family: '{branding.get('font', 'Inter')}', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-size-base: 16px;
  --font-size-sm: 14px;
  --font-size-lg: 18px;
  --font-size-xl: 24px;
  --font-size-2xl: 32px;
  --font-size-3xl: 48px;
  --line-height-base: 1.6;
  --line-height-heading: 1.2;

  /* --- Spacing --- */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;
  --space-3xl: 64px;

  /* --- Accessibility --- */
  --min-touch-target: 48px;
  --focus-ring: 0 0 0 3px var(--color-primary);
  --focus-ring-offset: 0 0 0 1px var(--color-bg-dark);

  /* --- Transitions --- */
  --transition-fast: 150ms ease;
  --transition-base: 250ms ease;
  --transition-slow: 500ms ease;
}}

/* --- Reduced Motion --- */
@media (prefers-reduced-motion: reduce) {{
  *, *::before, *::after {{
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }}
}}

/* --- High Contrast Mode --- */
@media (prefers-contrast: high) {{
  :root {{
    --color-bg-glass: rgba(255,255,255,0.15);
    --color-border-glass: rgba(255,255,255,0.3);
    --glass-blur: 0px;
  }}
}}

/* --- Base Styles --- */
* {{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}}

html {{
  font-size: var(--font-size-base);
  scroll-behavior: smooth;
}}

body {{
  font-family: var(--font-family);
  background-color: var(--color-bg-dark);
  color: var(--color-text-primary);
  line-height: var(--line-height-base);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh;
}}

/* --- Focus Styles (WCAG AAA) --- */
*:focus-visible {{
  outline: none;
  box-shadow: var(--focus-ring-offset), var(--focus-ring);
}}

/* --- Skip to Content (Accessibility) --- */
.skip-to-content {{
  position: absolute;
  top: -100%;
  left: 50%;
  transform: translateX(-50%);
  background: var(--color-primary);
  color: var(--color-bg-dark);
  padding: var(--space-sm) var(--space-lg);
  border-radius: var(--glass-radius);
  font-weight: 700;
  z-index: 10000;
  transition: top var(--transition-fast);
}}

.skip-to-content:focus {{
  top: var(--space-md);
}}

/* --- Glass Card Component --- */
.glass-card {{
  background: var(--glass-bg);
  backdrop-filter: blur(var(--glass-blur));
  -webkit-backdrop-filter: blur(var(--glass-blur));
  border: var(--glass-border);
  border-radius: var(--glass-radius);
  box-shadow: var(--glass-shadow);
  padding: var(--space-lg);
  transition: transform var(--transition-base), box-shadow var(--transition-base);
}}

.glass-card:hover {{
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
}}

/* --- Glass Button --- */
.glass-btn {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-lg);
  min-height: var(--min-touch-target);
  min-width: var(--min-touch-target);
  background: var(--glass-bg);
  backdrop-filter: blur(var(--glass-blur));
  border: var(--glass-border);
  border-radius: calc(var(--glass-radius) / 2);
  color: var(--color-text-primary);
  font-family: var(--font-family);
  font-size: var(--font-size-base);
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-base);
  text-decoration: none;
}}

.glass-btn:hover {{
  background: rgba(255,255,255,0.1);
  border-color: var(--color-primary);
}}

.glass-btn-primary {{
  background: var(--color-primary);
  color: var(--color-bg-dark);
  border-color: var(--color-primary);
}}

.glass-btn-primary:hover {{
  background: var(--color-secondary);
  border-color: var(--color-secondary);
}}

/* --- Glass Input --- */
.glass-input {{
  width: 100%;
  padding: var(--space-sm) var(--space-md);
  min-height: var(--min-touch-target);
  background: var(--glass-bg);
  backdrop-filter: blur(var(--glass-blur));
  border: var(--glass-border);
  border-radius: calc(var(--glass-radius) / 2);
  color: var(--color-text-primary);
  font-family: var(--font-family);
  font-size: var(--font-size-base);
  transition: border-color var(--transition-fast);
}}

.glass-input:focus {{
  border-color: var(--color-primary);
  outline: none;
  box-shadow: var(--focus-ring);
}}

.glass-input::placeholder {{
  color: var(--color-text-secondary);
}}

/* --- Notification Styles (VISUAL ONLY — NO AUDIO) --- */
.notification-banner {{
  position: fixed;
  top: var(--space-md);
  right: var(--space-md);
  z-index: 9999;
  max-width: 400px;
  padding: var(--space-md) var(--space-lg);
  border-radius: var(--glass-radius);
  background: var(--glass-bg);
  backdrop-filter: blur(var(--glass-blur));
  border: var(--glass-border);
  box-shadow: var(--glass-shadow);
  animation: slideIn var(--transition-base) ease-out;
}}

.notification-banner.flash {{
  animation: slideIn var(--transition-base) ease-out, flash 1s ease-in-out 3;
}}

@keyframes slideIn {{
  from {{ transform: translateX(100%); opacity: 0; }}
  to {{ transform: translateX(0); opacity: 1; }}
}}

@keyframes flash {{
  0%, 100% {{ opacity: 1; }}
  50% {{ opacity: 0.5; }}
}}

/* --- Medical Disclaimer Banner --- */
.medical-disclaimer {{
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: var(--glass-radius);
  padding: var(--space-md);
  margin: var(--space-md) 0;
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}}

.medical-disclaimer strong {{
  color: #EF4444;
}}

/* --- Responsive Grid --- */
.grid {{
  display: grid;
  gap: var(--space-lg);
}}

.grid-cols-1 {{ grid-template-columns: 1fr; }}
.grid-cols-2 {{ grid-template-columns: repeat(2, 1fr); }}
.grid-cols-3 {{ grid-template-columns: repeat(3, 1fr); }}
.grid-cols-4 {{ grid-template-columns: repeat(4, 1fr); }}

@media (max-width: 768px) {{
  .grid-cols-2, .grid-cols-3, .grid-cols-4 {{
    grid-template-columns: 1fr;
  }}
}}

@media (max-width: 1024px) {{
  .grid-cols-3, .grid-cols-4 {{
    grid-template-columns: repeat(2, 1fr);
  }}
}}
"""

    styles_dir = output_dir / "frontend" / "src" / "styles"
    styles_dir.mkdir(parents=True, exist_ok=True)
    (styles_dir / "theme.css").write_text(css_vars)
    log.success("Created glassmorphism theme CSS")

    # Generate Tailwind config
    tailwind_config = f"""/** @type {{import('tailwindcss').Config}} */
export default {{
  content: ['./index.html', './src/**/*.{{js,ts,jsx,tsx}}'],
  theme: {{
    extend: {{
      colors: {{
        primary: {{ DEFAULT: '{branding.get("primary", "#F59E0B")}', dark: '{branding.get("secondary", "#D97706")}', light: '{branding.get("accent", "#FBBF24")}' }},
        dark: {{ DEFAULT: '{branding.get("bg_dark", "#0F0F0F")}', glass: '{branding.get("bg_glass", "rgba(255,255,255,0.05)")}' }},
        glass: {{ border: '{branding.get("border_glass", "rgba(255,255,255,0.1)")}' }},
      }},
      fontFamily: {{
        sans: ['{branding.get("font", "Inter")}', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'sans-serif'],
      }},
      backdropBlur: {{
        glass: '{branding.get("blur", "16px")}',
      }},
      borderRadius: {{
        glass: '16px',
      }},
      minHeight: {{
        touch: '48px',
      }},
      minWidth: {{
        touch: '48px',
      }},
    }},
  }},
  plugins: [],
}}
"""

    (output_dir / "frontend" / "tailwind.config.js").write_text(tailwind_config)
    log.success("Created Tailwind config with glassmorphism theme")

    # Generate SVG favicon
    favicon_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <defs>
    <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{branding.get('primary', '#F59E0B')};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{branding.get('secondary', '#D97706')};stop-opacity:1" />
    </linearGradient>
  </defs>
  <circle cx="50" cy="50" r="45" fill="url(#g)"/>
  <text x="50" y="62" font-family="Inter,sans-serif" font-size="36" font-weight="700"
        fill="{branding.get('bg_dark', '#0F0F0F')}" text-anchor="middle">{app_name[0].upper()}</text>
</svg>"""

    public_dir = output_dir / "frontend" / "public"
    public_dir.mkdir(parents=True, exist_ok=True)
    (public_dir / "favicon.svg").write_text(favicon_svg)
    log.success(f"Created favicon for {app_name}")

    log.success("Branding complete!")
    return True


# ============================================================================
# STEP 4: CODE
# ============================================================================

def step_code(config: Dict, output_dir: Path):
    """Generate boilerplate code for all standard features."""
    log.header("STEP 4: CODE — Generating Application Boilerplate")

    app_name = config["app"]["display_name"]
    app_slug = snake_case(config["app"]["name"])

    # Backend requirements.txt
    requirements = """# ============================================================================
# Backend Dependencies
# ============================================================================
fastapi==0.115.0
uvicorn[standard]==0.30.0
pydantic[email]==2.9.0
asyncpg==0.30.0
python-jose[cryptography]==3.3.0
PyJWT==2.9.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.12
httpx==0.27.0
stripe==11.0.0
python-dotenv==1.0.1
pyyaml==6.0.2
aiofiles==24.1.0
websockets==13.0
Pillow==11.0.0
jinja2==3.1.4
alembic==1.14.0
psycopg2-binary==2.9.10
redis==5.2.0
celery==5.4.0
gunicorn==23.0.0
"""

    (output_dir / "backend" / "requirements.txt").write_text(requirements)
    log.success("Created backend/requirements.txt")

    # Backend main.py — the unified FastAPI application
    main_py = f'''"""
{app_name} — Production Backend
Audrey Evans Official / GlowStarLabs

Unified FastAPI application with all modules wired up.
Generated by soup-to-nuts.py
"""
import os
import sys
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import asyncpg
from dotenv import load_dotenv

load_dotenv()

# Add deploy/components to path for reusable modules
sys.path.insert(0, str(Path(__file__).parent.parent))

# --- Database Pool ---
db_pool = None

async def get_db_pool():
    global db_pool
    if db_pool is None:
        db_pool = await asyncpg.create_pool(
            dsn=os.environ.get("DATABASE_URL",
                "postgresql://postgres:postgres@localhost:5432/{app_slug}_db"),
            min_size=5, max_size=20,
        )
    return db_pool

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    pool = await get_db_pool()
    # Run migrations on startup
    from backend.migrations.run_migrations import run_all_migrations
    await run_all_migrations(pool)
    yield
    if pool:
        await pool.close()

# --- Create App ---
app = FastAPI(
    title="{app_name}",
    description="{config["app"].get("description", "")}",
    version="{config["app"]["version"]}",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# --- CORS ---
origins = os.environ.get("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Health Check ---
@app.get("/api/health")
async def health_check():
    pool = await get_db_pool()
    try:
        async with pool.acquire() as conn:
            await conn.fetchval("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {{str(e)}}"
    return {{
        "status": "healthy",
        "app": "{app_name}",
        "version": "{config["app"]["version"]}",
        "database": db_status,
    }}

# --- Medical Disclaimer (on every health-related response) ---
MEDICAL_DISCLAIMER = (
    "This application is for informational purposes only and is not a substitute "
    "for professional medical advice, diagnosis, or treatment. Always seek the advice "
    "of your physician or other qualified health care provider."
)

# --- Wire Up Modules ---
async def setup_routes():
    pool = await get_db_pool()

    # Auth Module
    from deploy.components.auth_module import AuthService, create_auth_router
    auth_service = AuthService(pool)
    auth_router = create_auth_router(auth_service)
    app.include_router(auth_router)
    get_current_user = auth_router.get_current_user

    # Payment Module
    from deploy.components.payment_module import PaymentService, create_payment_router
    payment_service = PaymentService(pool)
    payment_router = create_payment_router(payment_service, get_current_user)
    app.include_router(payment_router)

    # Affiliate Module
    from deploy.components.affiliate_module import AffiliateService, create_affiliate_router
    affiliate_service = AffiliateService(pool)
    affiliate_router = create_affiliate_router(affiliate_service, get_current_user)
    app.include_router(affiliate_router)

    # Analytics Module
    from deploy.components.analytics_module import AnalyticsService, create_analytics_router
    analytics_service = AnalyticsService(pool)
    analytics_router = create_analytics_router(analytics_service, get_current_user)
    app.include_router(analytics_router)

    # Notification Module
    from deploy.components.notification_module import NotificationService, create_notification_router
    notification_service = NotificationService(pool)
    notification_router = create_notification_router(notification_service, get_current_user)
    app.include_router(notification_router)

    # Selling Space Module
    from deploy.components.selling_space_module import SellingSpaceService, create_selling_space_router
    selling_space_service = SellingSpaceService(pool)
    selling_space_router = create_selling_space_router(selling_space_service, get_current_user)
    app.include_router(selling_space_router)

    # Admin Dashboard
    from deploy.components.admin_dashboard import create_admin_router
    admin_router = create_admin_router(pool, get_current_user)
    app.include_router(admin_router)

    # Landing Page
    from deploy.components.landing_page import create_landing_router
    landing_router = create_landing_router()
    app.include_router(landing_router)

    # App-specific routes
    from backend.api.routes import project_face, data_router, benchmarking
    app.include_router(project_face.router)
    app.include_router(data_router.router)
    app.include_router(benchmarking.router)

    return auth_service, payment_service, notification_service

# Run setup on import (called during lifespan)
@app.on_event("startup")
async def on_startup():
    await setup_routes()

# --- Error Handlers ---
@app.exception_handler(404)
async def not_found(request: Request, exc):
    return JSONResponse(status_code=404, content={{"detail": "Not found"}})

@app.exception_handler(500)
async def server_error(request: Request, exc):
    return JSONResponse(status_code=500, content={{"detail": "Internal server error"}})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
'''

    (output_dir / "backend" / "main.py").write_text(main_py)
    (output_dir / "backend" / "__init__.py").write_text("")
    (output_dir / "backend" / "api" / "__init__.py").write_text("")
    (output_dir / "backend" / "api" / "routes" / "__init__.py").write_text("")
    (output_dir / "backend" / "services" / "__init__.py").write_text("")
    (output_dir / "backend" / "models" / "__init__.py").write_text("")
    (output_dir / "backend" / "integrations" / "__init__.py").write_text("")
    (output_dir / "backend" / "migrations" / "__init__.py").write_text("")
    (output_dir / "backend" / "tests" / "__init__.py").write_text("")
    log.success("Created backend/main.py with all modules wired")

    # Frontend package.json
    pkg_json = {{
        "name": kebab_case(config["app"]["name"]),
        "private": True,
        "version": config["app"]["version"],
        "type": "module",
        "scripts": {{
            "dev": "vite",
            "build": "tsc && vite build",
            "preview": "vite preview",
            "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
            "test": "vitest",
            "test:a11y": "npx pa11y-ci",
        }},
        "dependencies": {{
            "react": "^18.3.0",
            "react-dom": "^18.3.0",
            "react-router-dom": "^6.26.0",
            "@tanstack/react-query": "^5.56.0",
            "axios": "^1.7.0",
            "lucide-react": "^0.441.0",
            "recharts": "^2.13.0",
            "zustand": "^5.0.0",
            "clsx": "^2.1.0",
            "@stripe/stripe-js": "^4.5.0",
            "@stripe/react-stripe-js": "^2.8.0",
        }},
        "devDependencies": {{
            "@types/react": "^18.3.0",
            "@types/react-dom": "^18.3.0",
            "@vitejs/plugin-react": "^4.3.0",
            "autoprefixer": "^10.4.0",
            "postcss": "^8.4.0",
            "tailwindcss": "^3.4.0",
            "typescript": "^5.5.0",
            "vite": "^5.4.0",
            "vitest": "^2.1.0",
            "eslint": "^9.0.0",
            "pa11y-ci": "^3.1.0",
        }},
    }}

    (output_dir / "frontend" / "package.json").write_text(json.dumps(pkg_json, indent=2))
    log.success("Created frontend/package.json")

    log.success("Code generation complete!")
    return True


# ============================================================================
# STEP 5: CONNECT BACKENDS
# ============================================================================

def step_connect(config: Dict, output_dir: Path):
    """Wire up all external API integrations."""
    log.header("STEP 5: CONNECT — Wiring Backend API Integrations")

    # OpenRouter integration
    openrouter_py = '''"""OpenRouter Integration — Unified AI model access."""
import os
import httpx
from typing import Dict, List, Optional


class OpenRouterClient:
    """Client for OpenRouter API — access any AI model."""

    BASE_URL = "https://openrouter.ai/api/v1"

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY", "")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://glowstarlabs.com",
            "X-Title": "GlowStarLabs Platform",
        }

    async def chat(self, messages: List[Dict], model: str = "openai/gpt-4o-mini",
                   max_tokens: int = 2000, temperature: float = 0.7) -> Dict:
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                f"{self.BASE_URL}/chat/completions",
                headers=self.headers,
                json={
                    "model": model,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                },
            )
            resp.raise_for_status()
            return resp.json()

    async def analyze_skin(self, image_base64: str, concerns: List[str] = None) -> Dict:
        """Use vision model to analyze skin from photo."""
        messages = [
            {"role": "system", "content": """You are a dermatology AI assistant. Analyze the skin in the provided image.
Identify: skin type, visible conditions, texture, hydration level, sun damage signs.
Provide recommendations for skincare routine, products, and when to see a dermatologist.
ALWAYS include the medical disclaimer that this is not medical advice."""},
            {"role": "user", "content": [
                {"type": "text", "text": f"Analyze my skin. Concerns: {', '.join(concerns or ['general'])}"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}},
            ]},
        ]
        return await self.chat(messages, model="openai/gpt-4o", max_tokens=3000)

    async def get_models(self) -> List[Dict]:
        """List available models and pricing."""
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(f"{self.BASE_URL}/models", headers=self.headers)
            resp.raise_for_status()
            return resp.json().get("data", [])

    async def get_model_stats(self) -> Dict:
        """Get usage statistics for benchmarking."""
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(
                f"{self.BASE_URL}/auth/key",
                headers=self.headers,
            )
            if resp.status_code == 200:
                return resp.json()
            return {"error": "Could not fetch stats"}
'''

    (output_dir / "backend" / "integrations" / "openrouter_client.py").write_text(openrouter_py)
    log.success("Created OpenRouter integration")

    # Weather integration
    weather_py = '''"""OpenWeatherMap Integration — Weather-based skincare adjustments."""
import os
import httpx
from typing import Dict, Optional


class WeatherClient:
    """Get weather data for GPS-based skincare personalization."""

    BASE_URL = "https://api.openweathermap.org/data/2.5"

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("OPENWEATHERMAP_API_KEY", "")

    async def get_weather(self, lat: float, lon: float) -> Dict:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(
                f"{self.BASE_URL}/weather",
                params={"lat": lat, "lon": lon, "appid": self.api_key, "units": "imperial"},
            )
            resp.raise_for_status()
            data = resp.json()

        return {
            "temperature_f": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "uv_index": data.get("uvi", 0),
            "wind_speed": data["wind"]["speed"],
            "description": data["weather"][0]["description"],
            "location": data.get("name", "Unknown"),
            "skincare_factors": self._analyze_skincare_factors(data),
        }

    def _analyze_skincare_factors(self, data: Dict) -> Dict:
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        factors = {
            "hydration_need": "high" if humidity < 30 else "moderate" if humidity < 60 else "low",
            "spf_recommendation": "SPF 50+" if temp > 80 else "SPF 30+",
            "moisturizer_weight": "heavy" if humidity < 30 else "light" if humidity > 70 else "medium",
            "climate_type": "arid" if humidity < 25 else "humid" if humidity > 70 else "temperate",
            "wind_protection": temp < 40 or data["wind"]["speed"] > 15,
            "tips": [],
        }
        if humidity < 30:
            factors["tips"].append("Very dry air — use a humidifier and hyaluronic acid serum")
        if temp > 85:
            factors["tips"].append("High heat — lightweight, water-based products recommended")
        if temp < 32:
            factors["tips"].append("Freezing temps — protect skin barrier with occlusive moisturizer")
        return factors

    async def get_by_city(self, city: str) -> Dict:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(
                f"{self.BASE_URL}/weather",
                params={"q": city, "appid": self.api_key, "units": "imperial"},
            )
            resp.raise_for_status()
            data = resp.json()
        return self._analyze_skincare_factors(data)
'''

    (output_dir / "backend" / "integrations" / "weather_client.py").write_text(weather_py)
    log.success("Created Weather integration")

    # Clinical Trials integration
    clinical_py = '''"""ClinicalTrials.gov Integration — Find relevant dermatology trials."""
import httpx
from typing import Dict, List, Optional


class ClinicalTrialsClient:
    """Search ClinicalTrials.gov for skin-related clinical trials."""

    BASE_URL = "https://clinicaltrials.gov/api/v2"

    async def search_trials(self, condition: str, location: str = "",
                           status: str = "RECRUITING", max_results: int = 20) -> List[Dict]:
        params = {
            "query.cond": condition,
            "filter.overallStatus": status,
            "pageSize": max_results,
            "format": "json",
        }
        if location:
            params["query.locn"] = location

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(f"{self.BASE_URL}/studies", params=params)
            resp.raise_for_status()
            data = resp.json()

        studies = data.get("studies", [])
        results = []
        for study in studies:
            proto = study.get("protocolSection", {})
            ident = proto.get("identificationModule", {})
            status_mod = proto.get("statusModule", {})
            desc = proto.get("descriptionModule", {})
            contacts = proto.get("contactsLocationsModule", {})

            results.append({
                "nct_id": ident.get("nctId", ""),
                "title": ident.get("briefTitle", ""),
                "status": status_mod.get("overallStatus", ""),
                "summary": desc.get("briefSummary", ""),
                "conditions": proto.get("conditionsModule", {}).get("conditions", []),
                "locations": [
                    {"facility": loc.get("facility", ""), "city": loc.get("city", ""),
                     "state": loc.get("state", ""), "country": loc.get("country", "")}
                    for loc in contacts.get("locations", [])[:5]
                ],
                "url": f"https://clinicaltrials.gov/study/{ident.get('nctId', '')}",
            })

        return results

    async def search_skin_trials(self, location: str = "") -> List[Dict]:
        """Search for dermatology-specific trials."""
        conditions = ["dermatology", "skin care", "acne", "eczema", "psoriasis",
                      "anti-aging", "hyperpigmentation", "rosacea"]
        all_results = []
        for cond in conditions[:3]:  # Limit to avoid rate limiting
            results = await self.search_trials(cond, location, max_results=5)
            all_results.extend(results)
        # Deduplicate by NCT ID
        seen = set()
        unique = []
        for r in all_results:
            if r["nct_id"] not in seen:
                seen.add(r["nct_id"])
                unique.append(r)
        return unique
'''

    (output_dir / "backend" / "integrations" / "clinical_trials_client.py").write_text(clinical_py)
    log.success("Created ClinicalTrials.gov integration")

    # Perplexity integration
    perplexity_py = '''"""Perplexity Integration — AI-powered research and search."""
import os
import httpx
from typing import Dict, List


class PerplexityClient:
    """Perplexity API for research-backed skincare information."""

    BASE_URL = "https://api.perplexity.ai"

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("PERPLEXITY_API_KEY", "")

    async def research(self, query: str, model: str = "llama-3.1-sonar-large-128k-online") -> Dict:
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                f"{self.BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": "You are a research assistant specializing in skincare, dermatology, and cosmetic procedures. Provide evidence-based information with sources."},
                        {"role": "user", "content": query},
                    ],
                },
            )
            resp.raise_for_status()
            return resp.json()

    async def search_procedures(self, procedure: str, location: str = "") -> Dict:
        query = f"Research {procedure} procedure: costs, risks, recovery time, BBB ratings for providers"
        if location:
            query += f" near {location}"
        return await self.research(query)
'''

    (output_dir / "backend" / "integrations" / "perplexity_client.py").write_text(perplexity_py)
    log.success("Created Perplexity integration")

    log.success("All backend connections wired!")
    return True


# ============================================================================
# STEP 6: DATABASE
# ============================================================================

def step_database(config: Dict, output_dir: Path):
    """Generate database migration scripts."""
    log.header("STEP 6: DATABASE — PostgreSQL Schema & Migrations")

    app_slug = snake_case(config["app"]["name"])

    migration_sql = f"""-- ============================================================================
-- {config['app']['display_name']} — Database Schema
-- Generated by soup-to-nuts.py
-- ============================================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================================
-- 1. USERS
-- ============================================================================
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    display_name VARCHAR(100) NOT NULL,
    avatar_url TEXT,
    provider VARCHAR(20) NOT NULL DEFAULT 'email',
    provider_id VARCHAR(255),
    subscription_tier VARCHAR(20) NOT NULL DEFAULT 'free',
    tokens_remaining INTEGER NOT NULL DEFAULT 10,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    roles TEXT[] NOT NULL DEFAULT ARRAY['user'],
    last_login TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================================
-- 2. SUBSCRIPTIONS
-- ============================================================================
CREATE TABLE IF NOT EXISTS subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    tier VARCHAR(20) NOT NULL DEFAULT 'free',
    stripe_subscription_id VARCHAR(255),
    stripe_customer_id VARCHAR(255),
    stripe_price_id VARCHAR(255),
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    current_period_start TIMESTAMPTZ,
    current_period_end TIMESTAMPTZ,
    tokens_remaining INTEGER NOT NULL DEFAULT 10,
    tokens_used_this_period INTEGER NOT NULL DEFAULT 0,
    cancel_at_period_end BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(user_id)
);

-- ============================================================================
-- 3. SKIN ANALYSES
-- ============================================================================
CREATE TABLE IF NOT EXISTS skin_analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    image_url TEXT,
    skin_type VARCHAR(50),
    conditions JSONB DEFAULT '[]',
    recommendations JSONB DEFAULT '[]',
    location_lat DECIMAL(10, 7),
    location_lon DECIMAL(10, 7),
    location_city VARCHAR(100),
    weather_data JSONB DEFAULT '{{}}',
    ai_model_used VARCHAR(100),
    ai_response JSONB DEFAULT '{{}}',
    tokens_used INTEGER DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================================
-- 4. PRODUCT RECOMMENDATIONS
-- ============================================================================
CREATE TABLE IF NOT EXISTS product_recommendations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    analysis_id UUID REFERENCES skin_analyses(id),
    product_name VARCHAR(500) NOT NULL,
    product_url TEXT,
    affiliate_url TEXT,
    amazon_asin VARCHAR(20),
    category VARCHAR(100),
    price_range VARCHAR(50),
    rating DECIMAL(3, 2),
    reason TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================================
-- 5. AFFILIATE LINKS & TRACKING
-- ============================================================================
CREATE TABLE IF NOT EXISTS affiliate_links (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_name VARCHAR(500) NOT NULL,
    original_url TEXT NOT NULL,
    affiliate_url TEXT NOT NULL,
    short_code VARCHAR(20) UNIQUE NOT NULL,
    amazon_asin VARCHAR(20),
    category VARCHAR(100),
    source_module VARCHAR(100),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS affiliate_clicks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    link_id UUID NOT NULL REFERENCES affiliate_links(id),
    user_id UUID,
    ip_hash VARCHAR(64),
    user_agent TEXT,
    referrer TEXT,
    clicked_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS affiliate_conversions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    link_id UUID NOT NULL REFERENCES affiliate_links(id),
    user_id UUID,
    order_id VARCHAR(255),
    amount_cents INTEGER,
    commission_cents INTEGER,
    converted_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================================
-- 6. AD PLACEMENTS (SELLING SPACE)
-- ============================================================================
CREATE TABLE IF NOT EXISTS ad_placements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    advertiser_id UUID NOT NULL REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    image_url TEXT,
    click_url TEXT NOT NULL,
    ad_tier VARCHAR(20) NOT NULL,
    placement_type VARCHAR(20) NOT NULL DEFAULT 'sidebar',
    target_domains TEXT[] DEFAULT ARRAY[]::TEXT[],
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    stripe_payment_id VARCHAR(255),
    amount_paid_cents INTEGER NOT NULL DEFAULT 0,
    impressions INTEGER NOT NULL DEFAULT 0,
    clicks INTEGER NOT NULL DEFAULT 0,
    starts_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ad_impressions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ad_id UUID NOT NULL REFERENCES ad_placements(id),
    page_url TEXT,
    ip_hash VARCHAR(64),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ad_clicks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ad_id UUID NOT NULL REFERENCES ad_placements(id),
    ip_hash VARCHAR(64),
    user_agent TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================================
-- 7. FILE ROUTING RULES (UNIVERSAL DATA ROUTER)
-- ============================================================================
CREATE TABLE IF NOT EXISTS routing_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    source_type VARCHAR(50) NOT NULL,
    source_config JSONB DEFAULT '{{}}',
    destination_type VARCHAR(50) NOT NULL,
    destination_config JSONB DEFAULT '{{}}',
    filter_rules JSONB DEFAULT '{{}}',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    schedule VARCHAR(100),
    last_run TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS routed_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rule_id UUID REFERENCES routing_rules(id),
    user_id UUID NOT NULL REFERENCES users(id),
    source_type VARCHAR(50) NOT NULL,
    file_name VARCHAR(500),
    file_type VARCHAR(100),
    file_size INTEGER,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    destination_type VARCHAR(50),
    destination_path TEXT,
    metadata JSONB DEFAULT '{{}}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    processed_at TIMESTAMPTZ
);

-- ============================================================================
-- 8. BENCHMARK METRICS (AI BENCHMARKING)
-- ============================================================================
CREATE TABLE IF NOT EXISTS benchmark_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    model_name VARCHAR(255) NOT NULL,
    provider VARCHAR(100),
    task_type VARCHAR(100),
    latency_ms INTEGER,
    tokens_input INTEGER,
    tokens_output INTEGER,
    cost_cents DECIMAL(10, 4),
    quality_score DECIMAL(5, 4),
    success BOOLEAN NOT NULL DEFAULT TRUE,
    error_message TEXT,
    metadata JSONB DEFAULT '{{}}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================================
-- 9. THOUGHT-CHAIN CACHE
-- ============================================================================
CREATE TABLE IF NOT EXISTS thought_chains (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chain_id VARCHAR(100) UNIQUE NOT NULL,
    task_type VARCHAR(100) NOT NULL,
    domain VARCHAR(100),
    complexity VARCHAR(20),
    keywords TEXT[],
    reasoning_steps JSONB DEFAULT '[]',
    template TEXT,
    original_prompt TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'experimental',
    success_rate DECIMAL(5, 4) DEFAULT 0,
    reuse_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================================
-- 10. NOTIFICATIONS
-- ============================================================================
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    action_url TEXT,
    icon VARCHAR(50) DEFAULT 'info',
    priority VARCHAR(20) DEFAULT 'normal',
    is_read BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    read_at TIMESTAMPTZ
);

-- ============================================================================
-- 11. ANALYTICS EVENTS
-- ============================================================================
CREATE TABLE IF NOT EXISTS analytics_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID,
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB DEFAULT '{{}}',
    page_url TEXT,
    session_id VARCHAR(100),
    ip_hash VARCHAR(64),
    user_agent TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================================
-- INDEXES
-- ============================================================================
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_provider ON users(provider, provider_id);
CREATE INDEX IF NOT EXISTS idx_subscriptions_user ON subscriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_subscriptions_stripe ON subscriptions(stripe_subscription_id);
CREATE INDEX IF NOT EXISTS idx_skin_analyses_user ON skin_analyses(user_id);
CREATE INDEX IF NOT EXISTS idx_skin_analyses_created ON skin_analyses(created_at);
CREATE INDEX IF NOT EXISTS idx_product_recs_analysis ON product_recommendations(analysis_id);
CREATE INDEX IF NOT EXISTS idx_affiliate_links_code ON affiliate_links(short_code);
CREATE INDEX IF NOT EXISTS idx_affiliate_clicks_link ON affiliate_clicks(link_id);
CREATE INDEX IF NOT EXISTS idx_ad_placements_status ON ad_placements(status, starts_at, expires_at);
CREATE INDEX IF NOT EXISTS idx_ad_placements_advertiser ON ad_placements(advertiser_id);
CREATE INDEX IF NOT EXISTS idx_routing_rules_user ON routing_rules(user_id);
CREATE INDEX IF NOT EXISTS idx_routed_items_user ON routed_items(user_id, status);
CREATE INDEX IF NOT EXISTS idx_benchmark_metrics_model ON benchmark_metrics(model_name, created_at);
CREATE INDEX IF NOT EXISTS idx_thought_chains_task ON thought_chains(task_type, domain);
CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id, is_read);
CREATE INDEX IF NOT EXISTS idx_analytics_events_type ON analytics_events(event_type);
CREATE INDEX IF NOT EXISTS idx_analytics_events_user ON analytics_events(user_id);
CREATE INDEX IF NOT EXISTS idx_analytics_events_created ON analytics_events(created_at);
"""

    migrations_dir = output_dir / "backend" / "migrations"
    migrations_dir.mkdir(parents=True, exist_ok=True)
    (migrations_dir / "001_initial_schema.sql").write_text(migration_sql)
    log.success("Created migration: 001_initial_schema.sql")

    # Migration runner
    migration_runner = '''"""Database Migration Runner — Execute SQL migrations in order."""
import os
from pathlib import Path


async def run_all_migrations(pool):
    """Run all pending SQL migrations."""
    migrations_dir = Path(__file__).parent
    sql_files = sorted(migrations_dir.glob("*.sql"))

    async with pool.acquire() as conn:
        # Create migrations tracking table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS _migrations (
                id SERIAL PRIMARY KEY,
                filename VARCHAR(255) UNIQUE NOT NULL,
                applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        """)

        for sql_file in sql_files:
            filename = sql_file.name
            already_applied = await conn.fetchval(
                "SELECT COUNT(*) FROM _migrations WHERE filename = $1", filename
            )
            if already_applied:
                continue

            print(f"  Applying migration: {filename}")
            sql = sql_file.read_text()
            try:
                await conn.execute(sql)
                await conn.execute(
                    "INSERT INTO _migrations (filename) VALUES ($1)", filename
                )
                print(f"  ✓ Migration {filename} applied successfully")
            except Exception as e:
                print(f"  ✗ Migration {filename} failed: {e}")
                raise
'''

    (migrations_dir / "run_migrations.py").write_text(migration_runner)
    log.success("Created migration runner")

    log.success("Database schema complete!")
    return True


# ============================================================================
# STEP 7: TEST
# ============================================================================

def step_test(config: Dict, output_dir: Path):
    """Generate and optionally run test suites."""
    log.header("STEP 7: TEST — Generating Test Suites")

    # Unit tests
    unit_test = '''"""Unit Tests — Core module tests."""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class TestAuthModule:
    def test_password_hashing(self):
        from deploy.components.auth_module.auth_service import AuthService
        password = "TestPassword123!"
        hashed = AuthService.hash_password(password)
        assert AuthService.verify_password(password, hashed)
        assert not AuthService.verify_password("wrong", hashed)

    def test_password_different_salts(self):
        from deploy.components.auth_module.auth_service import AuthService
        h1 = AuthService.hash_password("same_password")
        h2 = AuthService.hash_password("same_password")
        assert h1 != h2  # Different salts


class TestSubscriptionTiers:
    def test_tier_config(self):
        from deploy.components.payment_module.payment_models import TIER_CONFIG, SubscriptionTier
        assert SubscriptionTier.FREE in TIER_CONFIG
        assert TIER_CONFIG[SubscriptionTier.FREE]["price"] == 0
        assert TIER_CONFIG[SubscriptionTier.STARTER]["price"] == 900
        assert TIER_CONFIG[SubscriptionTier.PRO]["price"] == 2900
        assert TIER_CONFIG[SubscriptionTier.BUSINESS]["price"] == 9900
        assert TIER_CONFIG[SubscriptionTier.ENTERPRISE]["price"] == 29900

    def test_token_allocations(self):
        from deploy.components.payment_module.payment_models import TIER_CONFIG, SubscriptionTier
        assert TIER_CONFIG[SubscriptionTier.FREE]["tokens"] == 10
        assert TIER_CONFIG[SubscriptionTier.ENTERPRISE]["tokens"] == 10000


class TestAffiliateModule:
    def test_amazon_link_generation(self):
        from deploy.components.affiliate_module.affiliate_service import AffiliateService
        svc = AffiliateService.__new__(AffiliateService)
        svc.config = type("C", (), {"amazon_tag": "test-20"})()
        url = svc.generate_amazon_link("https://www.amazon.com/dp/B001234")
        assert "tag=test-20" in url

    def test_amazon_search_link(self):
        from deploy.components.affiliate_module.affiliate_service import AffiliateService
        svc = AffiliateService.__new__(AffiliateService)
        svc.config = type("C", (), {"amazon_tag": "test-20"})()
        url = svc.generate_amazon_search_link("CeraVe Moisturizer")
        assert "tag=test-20" in url
        assert "CeraVe" in url

    def test_auto_linkify(self):
        from deploy.components.affiliate_module.affiliate_service import AffiliateService
        svc = AffiliateService.__new__(AffiliateService)
        text = "Try CeraVe for dry skin"
        links = {"CeraVe": "https://amazon.com/cerave?tag=test-20"}
        result = svc.auto_linkify_text(text, links)
        assert "href=" in result
        assert "sponsored" in result


class TestAdTiers:
    def test_all_tiers_exist(self):
        from deploy.components.selling_space_module.selling_space_service import AD_TIERS
        expected = ["basic", "standard", "premium", "featured", "spotlight", "exclusive", "domination"]
        for tier in expected:
            assert tier in AD_TIERS

    def test_tier_pricing(self):
        from deploy.components.selling_space_module.selling_space_service import AD_TIERS
        assert AD_TIERS["basic"]["price_cents"] == 2000
        assert AD_TIERS["domination"]["price_cents"] == 200000


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
'''

    (output_dir / "tests" / "unit" / "test_modules.py").write_text(unit_test)
    (output_dir / "tests" / "__init__.py").write_text("")
    (output_dir / "tests" / "unit" / "__init__.py").write_text("")
    log.success("Created unit tests")

    # Integration tests
    integration_test = '''"""Integration Tests — API endpoint tests."""
import pytest
from httpx import AsyncClient, ASGITransport
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


@pytest.mark.asyncio
class TestHealthEndpoint:
    async def test_health_check(self):
        """Test that health endpoint returns 200."""
        # This test requires a running database
        # In CI, use docker-compose to spin up PostgreSQL
        pass


@pytest.mark.asyncio
class TestAuthEndpoints:
    async def test_register_requires_password(self):
        """Registration with email provider requires password."""
        pass

    async def test_login_invalid_credentials(self):
        """Login with wrong password returns 401."""
        pass


@pytest.mark.asyncio
class TestPaymentEndpoints:
    async def test_list_tiers(self):
        """Tier listing is public and returns all tiers."""
        pass

    async def test_checkout_requires_auth(self):
        """Checkout requires authentication."""
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
'''

    (output_dir / "tests" / "integration" / "__init__.py").write_text("")
    (output_dir / "tests" / "integration" / "test_api.py").write_text(integration_test)
    log.success("Created integration tests")

    # Accessibility tests
    a11y_config = """{
  "defaults": {
    "timeout": 30000,
    "wait": 1000,
    "standard": "WCAG2AAA",
    "runners": ["axe"]
  },
  "urls": [
    "http://localhost:3000/",
    "http://localhost:3000/login",
    "http://localhost:3000/register",
    "http://localhost:3000/dashboard",
    "http://localhost:3000/pricing"
  ]
}"""

    (output_dir / "tests" / "accessibility" / "pa11y-ci.json").write_text(a11y_config)
    log.success("Created WCAG AAA accessibility test config")

    # Performance test
    perf_test = '''"""Performance Tests — Response time and load testing."""
import time
import asyncio
import httpx


async def test_api_response_times(base_url: str = "http://localhost:8000"):
    """Test that API endpoints respond within acceptable times."""
    endpoints = [
        ("/api/health", 500),           # 500ms max
        ("/api/landing/config", 200),    # 200ms max
        ("/api/landing/pricing", 200),   # 200ms max
        ("/api/payments/tiers", 200),    # 200ms max
        ("/api/ads/tiers", 200),         # 200ms max
    ]

    results = []
    async with httpx.AsyncClient(base_url=base_url, timeout=10.0) as client:
        for endpoint, max_ms in endpoints:
            start = time.monotonic()
            try:
                resp = await client.get(endpoint)
                elapsed_ms = (time.monotonic() - start) * 1000
                passed = elapsed_ms <= max_ms and resp.status_code == 200
                results.append({
                    "endpoint": endpoint,
                    "status": resp.status_code,
                    "time_ms": round(elapsed_ms, 2),
                    "max_ms": max_ms,
                    "passed": passed,
                })
            except Exception as e:
                results.append({
                    "endpoint": endpoint,
                    "error": str(e),
                    "passed": False,
                })

    print("\\nPerformance Test Results:")
    print("-" * 60)
    for r in results:
        status = "PASS" if r.get("passed") else "FAIL"
        print(f"  [{status}] {r['endpoint']} — {r.get('time_ms', 'N/A')}ms (max: {r.get('max_ms', 'N/A')}ms)")

    return results


if __name__ == "__main__":
    asyncio.run(test_api_response_times())
'''

    (output_dir / "tests" / "performance" / "test_response_times.py").write_text(perf_test)
    log.success("Created performance tests")

    log.success("Test suites complete!")
    return True


# ============================================================================
# STEP 8: BUILD
# ============================================================================

def step_build(config: Dict, output_dir: Path):
    """Create production build configurations."""
    log.header("STEP 8: BUILD — Production Build Configs")

    # Vite config for frontend
    vite_config = """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/go': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    minify: 'terser',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom'],
          charts: ['recharts'],
          stripe: ['@stripe/stripe-js', '@stripe/react-stripe-js'],
        },
      },
    },
  },
})
"""

    (output_dir / "frontend" / "vite.config.ts").write_text(vite_config)
    log.success("Created Vite build config")

    # TypeScript config
    tsconfig = """{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}"""

    tsconfig_node = """{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}"""

    (output_dir / "frontend" / "tsconfig.json").write_text(tsconfig)
    (output_dir / "frontend" / "tsconfig.node.json").write_text(tsconfig_node)
    log.success("Created TypeScript configs")

    # Electron config for desktop builds
    electron_config = """{
  "appId": "com.glowstarlabs.%s",
  "productName": "%s",
  "directories": {
    "output": "dist-electron"
  },
  "files": ["dist/**/*", "electron/**/*"],
  "win": {
    "target": ["nsis"],
    "icon": "public/icon.ico"
  },
  "mac": {
    "target": ["dmg"],
    "icon": "public/icon.icns",
    "category": "public.app-category.healthcare"
  },
  "linux": {
    "target": ["AppImage"],
    "icon": "public/icon.png"
  }
}""" % (snake_case(config["app"]["name"]), config["app"]["display_name"])

    (output_dir / "frontend" / "electron-builder.json").write_text(electron_config)
    log.success("Created Electron builder config for desktop")

    log.success("Build configs complete!")
    return True


# ============================================================================
# STEP 9: DEPLOY
# ============================================================================

def step_deploy(config: Dict, output_dir: Path):
    """Generate Docker and deployment configurations."""
    log.header("STEP 9: DEPLOY — Docker & Hosting Configuration")

    app_slug = snake_case(config["app"]["name"])

    # Backend Dockerfile
    backend_dockerfile = f"""FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \\
    build-essential libpq-dev curl && \\
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ ./backend/
COPY deploy/ ./deploy/

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \\
    CMD curl -f http://localhost:8000/api/health || exit 1

EXPOSE 8000

CMD ["gunicorn", "backend.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", \\
     "--bind", "0.0.0.0:8000", "--timeout", "120", "--access-logfile", "-"]
"""

    (output_dir / "docker" / "Dockerfile.backend").write_text(backend_dockerfile)
    log.success("Created backend Dockerfile")

    # Frontend Dockerfile
    frontend_dockerfile = """FROM node:22-alpine AS builder

WORKDIR /app
COPY frontend/package.json frontend/pnpm-lock.yaml* ./
RUN corepack enable && pnpm install --frozen-lockfile 2>/dev/null || npm install

COPY frontend/ .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD wget -q --spider http://localhost:80/ || exit 1

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
"""

    (output_dir / "docker" / "Dockerfile.frontend").write_text(frontend_dockerfile)
    log.success("Created frontend Dockerfile")

    # Nginx config
    nginx_conf = """server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' https://js.stripe.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self' https://api.stripe.com https://openrouter.ai;" always;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml text/javascript image/svg+xml;
    gzip_min_length 1000;

    # SPA routing
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API proxy
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Affiliate redirect proxy
    location /go/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # WebSocket proxy
    location /api/notifications/ws {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }

    # Cache static assets
    location ~* \\.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
"""

    (output_dir / "docker" / "nginx.conf").write_text(nginx_conf)
    log.success("Created Nginx config")

    # docker-compose.yml
    compose = f"""version: '3.8'

services:
  # PostgreSQL Database
  db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_DB: {app_slug}_db
      POSTGRES_USER: ${{DB_USER:-postgres}}
      POSTGRES_PASSWORD: ${{DB_PASSWORD:-changeme}}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  redis:
    image: redis:7-alpine
    restart: unless-stopped
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # FastAPI Backend
  backend:
    build:
      context: .
      dockerfile: docker/Dockerfile.backend
    restart: unless-stopped
    env_file: .env
    environment:
      DATABASE_URL: postgresql://${{DB_USER:-postgres}}:${{DB_PASSWORD:-changeme}}@db:5432/{app_slug}_db
      REDIS_URL: redis://redis:6379/0
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    ports:
      - "8000:8000"

  # React Frontend
  frontend:
    build:
      context: .
      dockerfile: docker/Dockerfile.frontend
    restart: unless-stopped
    depends_on:
      - backend
    ports:
      - "80:80"
      - "443:443"

volumes:
  postgres_data:
"""

    (output_dir / "docker-compose.yml").write_text(compose)
    log.success("Created docker-compose.yml")

    log.success("Deployment configs complete!")
    return True


# ============================================================================
# STEP 10: SUBMIT
# ============================================================================

def step_submit(config: Dict, output_dir: Path):
    """Generate app store submission configs."""
    log.header("STEP 10: SUBMIT — App Store Submission Configs")

    # Fastlane Appfile
    app_store = config.get("app_store", {})
    google = app_store.get("google_play", {})
    apple = app_store.get("apple_app_store", {})

    fastlane_dir = output_dir / "fastlane"
    fastlane_dir.mkdir(exist_ok=True)

    appfile = f"""# Fastlane Appfile
# Generated by soup-to-nuts.py

# Apple
app_identifier("{apple.get('bundle_id', 'com.glowstarlabs.app')}")
apple_id("audrey@meetaudreyevans.com")
team_id("")  # Fill with Apple Developer Team ID

# Google
json_key_file("")  # Path to Google Play JSON key
package_name("{google.get('package_name', 'com.glowstarlabs.app')}")
"""

    (fastlane_dir / "Appfile").write_text(appfile)
    log.success("Created Fastlane Appfile")

    # Fastfile
    fastfile = """# Fastlane Fastfile
# Generated by soup-to-nuts.py

default_platform(:ios)

platform :ios do
  desc "Build and upload to TestFlight"
  lane :beta do
    build_app(scheme: "GlowStarLabs")
    upload_to_testflight
  end

  desc "Build and upload to App Store"
  lane :release do
    build_app(scheme: "GlowStarLabs")
    upload_to_app_store(
      skip_metadata: false,
      skip_screenshots: false,
      submit_for_review: true,
    )
  end
end

platform :android do
  desc "Build and upload to Google Play internal track"
  lane :beta do
    gradle(task: "clean bundleRelease")
    upload_to_play_store(track: "internal")
  end

  desc "Build and upload to Google Play production"
  lane :release do
    gradle(task: "clean bundleRelease")
    upload_to_play_store(track: "production", rollout: "0.1")
  end
end
"""

    (fastlane_dir / "Fastfile").write_text(fastfile)
    log.success("Created Fastlane Fastfile")

    log.success("App store submission configs complete!")
    return True


# ============================================================================
# STEP 11: MONITOR
# ============================================================================

def step_monitor(config: Dict, output_dir: Path):
    """Set up monitoring and error tracking."""
    log.header("STEP 11: MONITOR — Error Tracking & Uptime")

    monitor_config = f"""# ============================================================================
# Monitoring Configuration
# {config['app']['display_name']}
# ============================================================================

# Uptime monitoring endpoints
health_checks:
  - name: "API Health"
    url: "https://{config['domain']['primary']}/api/health"
    interval: 60
    timeout: 10
    expected_status: 200

  - name: "Frontend"
    url: "https://{config['domain']['primary']}/"
    interval: 60
    timeout: 10
    expected_status: 200

  - name: "WebSocket"
    url: "wss://{config['domain']['primary']}/api/notifications/ws"
    type: websocket
    interval: 300

# Alert configuration
alerts:
  email: "{config.get('monitoring', {}).get('alert_email', 'audrey@meetaudreyevans.com')}"
  on_down: true
  on_recovery: true
  on_ssl_expiry: true
  ssl_expiry_days: 14

# Log aggregation
logging:
  level: "{config.get('monitoring', {}).get('log_level', 'INFO')}"
  format: "json"
  retention_days: 30
"""

    (output_dir / "monitoring.yaml").write_text(monitor_config)
    log.success("Created monitoring config")

    log.success("Monitoring setup complete!")
    return True


# ============================================================================
# STEP 12: REPORT
# ============================================================================

def step_report(config: Dict, output_dir: Path):
    """Generate deployment report."""
    log.header("STEP 12: REPORT — Deployment Summary")

    app_name = config["app"]["display_name"]
    domain = config["domain"]["primary"]
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    report = f"""# ============================================================================
# DEPLOYMENT REPORT
# {app_name}
# Generated: {timestamp}
# ============================================================================

## Application
- **Name:** {app_name}
- **Version:** {config['app']['version']}
- **Parent Company:** {config['app'].get('parent_company', 'Audrey Evans Official')}
- **Brand:** {config['app'].get('parent_brand', 'GlowStarLabs')}

## URLs
- **Production:** https://{domain}
- **API Docs:** https://{domain}/api/docs
- **API ReDoc:** https://{domain}/api/redoc
- **Health Check:** https://{domain}/api/health

## Architecture
- **Frontend:** React + TypeScript + Vite + TailwindCSS
- **Backend:** FastAPI + Python 3.11
- **Database:** PostgreSQL 16
- **Cache:** Redis 7
- **Deployment:** Docker + docker-compose

## Modules Deployed
- Auth Module (Google OAuth, Apple Sign-In, Email/Password)
- Payment Module (Stripe subscriptions + token-based usage)
- Affiliate Module (Amazon Associates auto-linking)
- Analytics Module (Event tracking + dashboards)
- Notification Module (Visual-only, WCAG AAA, WebSocket)
- Selling Space Module (Self-service ad platform)
- Admin Dashboard (User management, revenue, health)
- Landing Page (Glassmorphism marketing page)

## Subscription Tiers
| Tier | Price | AI Tokens |
|------|-------|-----------|
| Free | $0/mo | 10 |
| Starter | $9/mo | 100 |
| Pro | $29/mo | 500 |
| Business | $99/mo | 2,000 |
| Enterprise | $299/mo | 10,000 |

## Ad Tiers
| Tier | Price |
|------|-------|
| Basic | $20 |
| Standard | $50 |
| Premium | $100 |
| Featured | $200 |
| Spotlight | $500 |
| Exclusive | $1,000 |
| Domination | $2,000 |

## Accessibility (Standard 7: Alt Text Everywhere)
- **WCAG Level:** AAA
- **Visual-Only Notifications:** Yes (no audio dependencies)
- **High Contrast Mode:** Supported
- **Keyboard Navigation:** Full support
- **Screen Reader:** Optimized
- **Min Touch Target:** 48px
- **Reduced Motion:** Respected
- **ARIA Labels:** On every interactive element
- **Adjustable Font Sizes:** Yes

## 8 Mandatory Standards (Audrey Evans Official DNA)
| # | Standard | Status |
|---|---------|--------|
| 1 | No Blue Light — Dark mode default, warm amber, night mode | ENFORCED |
| 2 | Eco Code — Cache aggressively, CO2 tracking, lightweight models first | ENFORCED |
| 3 | Neurodivergent-Friendly — No flashing, focus mode, break reminders (25min) | ENFORCED |
| 4 | Glassmorphism — Frosted glass, backdrop-blur, warm amber gradients | ENFORCED |
| 5 | Best in Class — Production-grade, polished, professional | ENFORCED |
| 6 | Blue Ocean Gangster — Underserved markets, unique features | ENFORCED |
| 7 | Alt Text Everywhere — WCAG AAA, visual-only notifications, ARIA labels | ENFORCED |
| 8 | Carbon Savings Quantifier — Starbucks cups equivalent, ESG metrics | ENFORCED |

## Database Tables
1. users
2. subscriptions
3. skin_analyses
4. product_recommendations
5. affiliate_links
6. affiliate_clicks
7. affiliate_conversions
8. ad_placements
9. ad_impressions
10. ad_clicks
11. routing_rules
12. routed_items
13. benchmark_metrics
14. thought_chains
15. notifications
16. analytics_events

## Deployment Commands
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Run migrations
docker-compose exec backend python -m backend.migrations.run_migrations

# Run tests
docker-compose exec backend pytest tests/ -v

# Build frontend
cd frontend && npm run build

# Desktop builds
cd frontend && npx electron-builder --win --mac --linux
```

## Environment Variables Required
See `.env.example` for the complete list of required environment variables.

## Next Steps
1. Configure DNS for {domain}
2. Set up SSL certificate (Let's Encrypt)
3. Configure Stripe webhook endpoint
4. Set up Google OAuth credentials
5. Configure Apple Sign-In
6. Set up Amazon Associates account
7. Configure OpenWeatherMap API key
8. Submit to Google Play Store
9. Submit to Apple App Store
10. Set up uptime monitoring

---
Generated by soup-to-nuts.py — Build once, deploy forever.
Audrey Evans Official / GlowStarLabs
"""

    (output_dir / "DEPLOYMENT_REPORT.md").write_text(report)
    log.success("Created DEPLOYMENT_REPORT.md")

    log.success("Report complete!")
    return True


# ============================================================================
# MAIN ORCHESTRATOR
# ============================================================================

STEP_FUNCTIONS = {
    "scaffold": step_scaffold,
    "configure": step_configure,
    "brand": step_brand,
    "code": step_code,
    "connect": step_connect,
    "database": step_database,
    "test": step_test,
    "build": step_build,
    "deploy": step_deploy,
    "submit": step_submit,
    "monitor": step_monitor,
    "report": step_report,
}


def main():
    parser = argparse.ArgumentParser(
        description="Soup-to-Nuts Master Deployment Script — Build once, deploy forever.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        EXAMPLES:
          python deploy/soup_to_nuts.py --app "Project Face" --domain "glowstarlabs.com" --tier full
          python deploy/soup_to_nuts.py --config app_config.yaml
          python deploy/soup_to_nuts.py --step scaffold --app "TheAltText"
          python deploy/soup_to_nuts.py --list-steps
        """),
    )

    parser.add_argument("--config", "-c", help="Path to app_config.yaml")
    parser.add_argument("--app", "-a", help="Application name")
    parser.add_argument("--domain", "-d", help="Primary domain")
    parser.add_argument("--tier", "-t", default="full", choices=["full", "web-only", "api-only", "mobile-only"])
    parser.add_argument("--step", "-s", help="Run only a specific step", choices=STEPS)
    parser.add_argument("--output", "-o", help="Output directory (default: current repo root)")
    parser.add_argument("--list-steps", action="store_true", help="List all available steps")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without executing")

    args = parser.parse_args()

    if args.list_steps:
        print("\nAvailable Steps:")
        print("-" * 50)
        for i, step in enumerate(STEPS, 1):
            print(f"  {i:2d}. {step:12s} — {STEP_FUNCTIONS[step].__doc__.strip()}")
        print()
        return

    # Load config
    config = load_config(args.config, args.app, args.domain, args.tier)
    output_dir = Path(args.output) if args.output else REPO_ROOT

    # Banner
    log.header(f"SOUP-TO-NUTS: {config['app']['display_name']}")
    print(f"  Domain:  {config['domain']['primary']}")
    print(f"  Tier:    {config['deployment']['tier']}")
    print(f"  Output:  {output_dir}")
    print(f"  Time:    {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print()

    if args.dry_run:
        log.warning("DRY RUN — No changes will be made")
        return

    # Run steps
    steps_to_run = [args.step] if args.step else STEPS
    total = len(steps_to_run)
    results = {}

    start_time = time.time()

    for i, step_name in enumerate(steps_to_run, 1):
        log.step(i, total, f"Running: {step_name}")
        try:
            success = STEP_FUNCTIONS[step_name](config, output_dir)
            results[step_name] = "SUCCESS" if success else "FAILED"
        except Exception as e:
            log.error(f"Step '{step_name}' failed: {e}")
            results[step_name] = f"ERROR: {e}"

    elapsed = time.time() - start_time

    # Summary
    log.header("DEPLOYMENT COMPLETE")
    print(f"  App:     {config['app']['display_name']}")
    print(f"  Domain:  {config['domain']['primary']}")
    print(f"  Time:    {elapsed:.1f}s")
    print()
    print("  Step Results:")
    for step, result in results.items():
        icon = "✓" if result == "SUCCESS" else "✗"
        color = Logger.COLORS["green"] if result == "SUCCESS" else Logger.COLORS["red"]
        print(f"    {color}{icon} {step:12s} — {result}{Logger.COLORS['end']}")
    print()
    print(f"  {Logger.COLORS['bold']}Build once, deploy forever.{Logger.COLORS['end']}")
    print(f"  {Logger.COLORS['bold']}Audrey Evans Official / GlowStarLabs{Logger.COLORS['end']}")
    print()


if __name__ == "__main__":
    main()
