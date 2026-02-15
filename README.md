# Audrey Evans Official / GlowStarLabs Platform

**Production-ready, deployable application suite** built with the 8 Mandatory Audrey Evans Official Standards.

---

## The 8 Mandatory Standards

Every app that rolls off this assembly line has ALL of these built in automatically. No exceptions.

| # | Standard | Description |
|---|---------|-------------|
| 1 | **No Blue Light** | Dark mode default, warm amber/orange tones, night mode shift |
| 2 | **Eco Code** | Cache aggressively, lightweight models first, CO2 tracking |
| 3 | **Neurodivergent-Friendly** | No flashing, no autoplay, focus mode, break reminders (25min) |
| 4 | **Glassmorphism** | Frosted glass, backdrop-blur, warm amber gradients, premium feel |
| 5 | **Best in Class** | Production-grade, polished, professional — not MVP |
| 6 | **Blue Ocean Gangster** | Underserved markets, unique features, competitive pricing |
| 7 | **Alt Text Everywhere** | WCAG AAA, visual-only notifications, ARIA labels on everything |
| 8 | **Carbon Savings Quantifier** | Starbucks cups equivalent, gamified leaderboard, ESG metrics |

---

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 22+
- Python 3.11+
- PostgreSQL 16+

### Development

```bash
# Clone
git clone https://github.com/MIDNGHTSAPPHIRE/audrey-evans-official.git
cd audrey-evans-official

# Copy environment config
cp .env.example .env
# Edit .env with your API keys

# Start with Docker
docker-compose up -d

# Or run separately:
# Backend
cd backend && pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000

# Frontend
cd frontend && npm install && npm run dev
```

### Production Deployment

```bash
docker-compose up -d --build
```

---

## Soup-to-Nuts Master Script

**The crown jewel.** One script to deploy ANY app.

```bash
# Deploy Project Face
python deploy/soup_to_nuts.py --app "Project Face" --domain "glowstarlabs.com" --tier "full"

# Deploy TheAltText
python deploy/soup_to_nuts.py --app "TheAltText" --domain "meetaudreyevans.com" --tier "full"

# Deploy any future app
python deploy/soup_to_nuts.py --app "My New App" --domain "example.com" --tier "full"
```

The script handles all 12 steps: Scaffold, Configure, Brand, Code, Connect, Database, Test, Build, Deploy, Submit, Monitor, Report.

---

## Architecture

```
Frontend:  React + TypeScript + Vite + TailwindCSS
Backend:   FastAPI + Python 3.11
Database:  PostgreSQL 16
Cache:     Redis 7
Payments:  Stripe (subscriptions + one-time)
AI:        OpenRouter (multi-model)
Auth:      Google OAuth + Apple Sign-In + Email/Password
Realtime:  WebSocket (visual-only notifications)
```

---

## Project Structure

```
audrey-evans-official/
├── backend/                    # FastAPI backend
│   ├── main.py                 # Application entry point
│   ├── api/routes/             # API route handlers
│   │   ├── project_face.py     # Skin analysis (flagship)
│   │   ├── data_router.py      # Universal data router
│   │   └── benchmarking.py     # AI model benchmarking
│   ├── migrations/             # Database migrations
│   │   └── init.sql            # Full schema (17 tables)
│   └── requirements.txt
├── frontend/                   # React + TypeScript frontend
│   ├── src/
│   │   ├── App.tsx             # Main app with routing
│   │   ├── pages/              # All page components
│   │   ├── components/         # Reusable UI components
│   │   │   ├── layout/         # Navbar, Footer, Layout
│   │   │   ├── eco/            # CarbonBadge
│   │   │   ├── neurodivergent/ # FocusMode
│   │   │   └── notifications/  # VisualNotification
│   │   └── styles/             # Global CSS + glassmorphism
│   ├── package.json
│   └── vite.config.ts
├── deploy/                     # Deployment infrastructure
│   ├── soup_to_nuts.py         # MASTER DEPLOYMENT SCRIPT
│   ├── app_config_template.yaml
│   └── components/             # Reusable drop-in modules
│       ├── auth_module/        # OAuth + email/password
│       ├── payment_module/     # Stripe subscriptions
│       ├── affiliate_module/   # Amazon Associates
│       ├── analytics_module/   # Usage tracking
│       ├── notification_module/# Visual-only notifications
│       ├── admin_dashboard/    # Admin panel
│       ├── landing_page/       # Marketing page
│       └── selling_space_module/ # Ad platform
├── docker/                     # Docker configuration
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   ├── nginx.conf
│   └── nginx-frontend.conf
├── tests/                      # Comprehensive test suite
│   ├── unit/                   # Unit tests
│   ├── integration/            # API connection tests
│   ├── e2e/                    # Critical flow tests
│   └── accessibility/          # WCAG AAA tests
├── .github/workflows/          # CI/CD pipeline
│   └── ci-cd.yml
├── .coderabbit.yaml            # CodeRabbit review config
├── docker-compose.yml          # Full stack orchestration
├── .env.example                # Environment template
└── README.md
```

---

## Database Schema (17 Tables)

| Table | Purpose |
|-------|---------|
| users | User accounts with accessibility preferences |
| subscriptions | Stripe subscription management |
| skin_analyses | Skin analysis results with weather data |
| product_recommendations | AI-generated product suggestions |
| affiliate_links | Auto-generated affiliate URLs |
| affiliate_clicks | Click tracking |
| affiliate_conversions | Conversion tracking |
| ad_placements | Selling space ad management |
| ad_impressions | Ad view tracking |
| ad_clicks | Ad click tracking |
| routing_rules | Data router rule definitions |
| routed_items | Routed item history |
| benchmark_metrics | AI model performance data |
| thought_chains | Kimi thought-chain cache |
| notifications | Visual-only notification queue |
| analytics_events | Usage analytics |
| carbon_ledger | CO2 savings tracking |

---

## Subscription Tiers

| Tier | Price | Tokens | Features |
|------|-------|--------|----------|
| Free | $0 | 10 | Basic skin analysis |
| Starter | $9 | 100 | Full analysis + recommendations |
| Pro | $29 | 500 | GPS personalization + procedures |
| Business | $99 | 2,000 | Data router + benchmarking + API |
| Enterprise | $299 | 10,000 | White-label + custom integrations |

---

## Domains

| Domain | Purpose |
|--------|---------|
| meetaudreyevans.com | Central hub |
| glowstarlabs.com | Parent brand |
| growlingeyes.com | Creative projects |
| truthslayer.com | Research tools |
| yumyumcode.com | Developer tools |
| reesereviews.com | Daughter's review site |

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check + eco metrics |
| `/api/carbon` | GET | Carbon savings dashboard |
| `/api/auth/*` | POST | Authentication (register, login, OAuth) |
| `/api/payments/*` | POST | Stripe payments + webhooks |
| `/api/skin-analysis/*` | POST | Skin analysis + recommendations |
| `/api/clinical-trials/*` | GET | ClinicalTrials.gov search |
| `/api/data-router/*` | CRUD | Routing rule management |
| `/api/benchmarking/*` | GET/POST | AI model benchmarking |
| `/api/affiliate/*` | GET | Affiliate link management |
| `/api/selling-space/*` | CRUD | Ad placement management |
| `/api/notifications/ws` | WS | Real-time visual notifications |
| `/api/admin/*` | GET | Admin dashboard data |

---

## Accessibility (WCAG AAA)

- **Visual-only notifications** — Audrey's daughter is legally deaf
- No audio-dependent features anywhere
- ARIA labels on every interactive element
- Keyboard navigation throughout
- High contrast mode
- Adjustable font sizes (14px–24px)
- Minimum 48px touch targets
- Skip-to-content link
- Reduced motion respected
- Focus indicators on all interactive elements

---

## License

Copyright 2024-2026 Audrey Evans Official / GlowStarLabs. All rights reserved.
