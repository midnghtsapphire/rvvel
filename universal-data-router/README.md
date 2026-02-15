# Universal Data Router (Revvel)

**Route data from ANY source to ANY destination with multi-select**

## Overview

The Universal Data Router (Revvel) is an intelligent data routing platform that provides a centralized staging area for all incoming data—from emails and LLM exports to manual uploads and API responses. From this staging area, users can categorize, tag, search, and route data to multiple destinations simultaneously with a single click.

## Features

- **Universal Ingress:** Connect to any data source (Email, LLM exports, uploads, APIs)
- **Intelligent Staging:** AI-powered auto-categorization and tagging
- **Multi-Destination Routing:** Send to GitHub, Google Drive, Email, and more
- **Flexible Processing:** Real-time, bulk, and date-range processing modes
- **Rules Engine:** Automate sorting and routing with user-defined rules
- **WCAG AAA Accessibility:** Fully accessible interface for all users
- **Carbon Tracking:** Measure environmental impact of efficient data management

## Architecture

```
Sources → Ingress Gateway → InReview Staging → Rules Engine → Routing Orchestrator → Destinations
```

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set up database
export DATABASE_URL="postgresql://user:pass@localhost:5432/revvel_db"
alembic upgrade head

# Run the application
python -m src.main
```

## API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.

## Key Endpoints

- `GET /items` - List items in InReview staging area
- `POST /routing/jobs` - Create multi-destination routing job
- `POST /processing/run` - Trigger processing (bulk/real-time/date-range)
- `POST /rules/auto-sort` - Create auto-sort rule
- `POST /webhooks/email/gmail` - Receive Gmail notifications

## Development

```bash
# Run in development mode
uvicorn src.main:app --reload

# Run tests
pytest tests/
```

## License

Private - Audrey Evans (MIDNGHTSAPPHIRE)
