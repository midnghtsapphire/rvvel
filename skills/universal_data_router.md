# Universal Data Router (Revvel) Skill

## Overview

The Universal Data Router (Revvel) is a comprehensive data routing platform that enables users to route data from ANY source to ANY destination with multi-select capabilities. This skill provides guidance on using, maintaining, and extending the system.

## Core Capabilities

1. **Universal Ingress**: Accept data from multiple sources (Email, LLM exports, uploads, APIs)
2. **Intelligent Staging**: AI-powered categorization and tagging in the InReview area
3. **Multi-Destination Routing**: Send data to multiple destinations simultaneously
4. **Flexible Processing**: Support for real-time, bulk, and date-range processing modes
5. **Rules Engine**: Automated sorting and routing based on user-defined rules
6. **Accessibility**: WCAG AAA compliant with glassmorphism UI design

## Architecture

### System Components

| Component | Purpose | Technology |
|-----------|---------|------------|
| Ingress Gateway | Receive data from all sources | FastAPI, OAuth |
| InReview Engine | Staging area with AI categorization | OpenRouter, PostgreSQL |
| Rules Engine | Automated sorting and routing | Custom Logic, JSONB |
| Routing Orchestrator | Multi-destination dispatch | Celery, Tenacity |
| Control Plane | User interface and API | FastAPI, WebSocket |

### Data Flow

```
Sources → Ingress → InReview Staging → Rules Engine → Routing Orchestrator → Destinations
```

## Key Features

### Processing Modes

1. **Bulk Mode**: Process all emails/items at once or by date range
2. **Real-Time Mode**: Auto-process items as they arrive via webhooks
3. **Date Range Mode**: Process items within a specific date window

### Date Range Organization

- Filter and view items by: today, this week, this month, custom range
- Export items by date range to any destination
- Organize ALL files (not just emails) by date ranges

### Attachment Auto-Processing

- Auto-categorize emails when notifications arrive
- Auto-extract and categorize attachments
- Multiple export methods for attachments (download, drive, github, etc.)

### Auto-Sort on Notification

- Real-time email webhook/push notification listener
- Auto-categorize, auto-extract attachments, auto-tag on arrival
- "Auto-sort" button processes everything in InReview automatically
- "Auto-download" button downloads all attachments to configured location
- User-defined rules: "emails from X always go to Y folder"

### Multiple Export Methods

- Individual item export
- Bulk export (select multiple)
- Date range export
- Category export (all code files, all legal docs, etc.)
- Source export (all from Gmail, all from Claude, etc.)
- One-click "export everything" with multi-destination

## API Endpoints

### Items (InReview Staging Area)

```
GET  /items                    # List items with filtering
GET  /items/{item_id}          # Get single item
PATCH /items/{item_id}         # Update item
DELETE /items                  # Bulk delete
GET  /items/date-range/{range} # Filter by date range
```

### Routing and Export

```
POST /routing/jobs             # Create multi-destination routing job
GET  /routing/jobs/{job_id}    # Get job status
POST /routing/export           # Flexible export endpoint
```

### Processing Modes

```
POST /processing/run           # Trigger processing (bulk/real-time/date-range)
POST /processing/auto-sort/run # Trigger auto-sort
POST /processing/auto-download/run # Trigger auto-download
```

### Rules

```
GET  /rules/auto-sort          # List auto-sort rules
POST /rules/auto-sort          # Create auto-sort rule
PUT  /rules/auto-sort/{id}     # Update auto-sort rule
DELETE /rules/auto-sort/{id}   # Delete auto-sort rule
GET  /rules/routing            # List routing rules
POST /rules/routing            # Create routing rule
```

### Webhooks

```
POST /webhooks/email/gmail     # Gmail push notifications
POST /webhooks/generic         # Generic webhook
```

## Database Schema

### Core Tables

- `user`: User accounts and preferences
- `in_review_item`: Central staging table for all incoming data
- `attachment`: Extracted attachments from emails/sources
- `routing_rule`: User-defined routing rules
- `auto_sort_rule`: User-defined auto-sort rules
- `routing_job`: Tracks routing operations
- `audit_log`: Complete audit trail
- `source_config`: Source credentials and settings
- `destination_config`: Destination credentials and settings
- `carbon_tracking`: Environmental impact tracking

## Plugin Architecture

### Creating a New Plugin

All source and destination plugins inherit from `BasePlugin`:

```python
from abc import ABC, abstractmethod

class BasePlugin(ABC):
    def __init__(self, config: dict):
        self.config = config
    
    @abstractmethod
    async def connect(self):
        """Establish connection to service"""
        pass
    
    @abstractmethod
    async def send(self, data_packet: dict) -> dict:
        """Send data to destination"""
        pass
    
    @abstractmethod
    async def fetch(self) -> list[dict]:
        """Fetch data from source"""
        pass
```

### Supported Integrations

**Sources**: Gmail, Outlook, Yahoo, LLM exports, Manual uploads, Web scraping, APIs

**Destinations**: GitHub, GitLab, Bitbucket, Google Drive, Email, LLMs (Claude, GPT, Grok), AI Agents, SSRN, SoundCloud, TikTok

## Development Workflow

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set up database
export DATABASE_URL="postgresql://user:pass@localhost:5432/revvel_db"

# Run application
python -m src.main
```

### Testing

```bash
# Run test suite
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src
```

### Deployment

The project follows a **dev → test → live** deployment process:

1. **Dev**: Local development with SQLite
2. **Test**: Staging environment with test database
3. **Live**: Production with PostgreSQL, Redis, Celery

Code review is mandatory using **Coderabbit** before merging to production.

## Best Practices

### Auto-Sort Rules

Create rules that match specific conditions and apply actions:

```json
{
  "name": "Legal Documents from Law Firm",
  "conditions": {
    "from": "*@lawfirm.com",
    "subject_contains": "Contract"
  },
  "actions": {
    "set_category": "legal",
    "add_tags": ["contract", "review"]
  },
  "priority": 10
}
```

### Routing Rules

Define automatic routing based on conditions:

```json
{
  "name": "Code to GitHub",
  "conditions": {
    "category": "code"
  },
  "destination_ids": [1, 2]
}
```

### Processing Modes

- Use **real-time mode** for immediate processing of incoming data
- Use **bulk mode** for processing large backlogs
- Use **date-range mode** for selective processing of historical data

## Accessibility

The UI is designed to meet **WCAG AAA** standards:

- High contrast (7:1 ratio minimum)
- Keyboard navigation throughout
- Screen reader support with proper ARIA attributes
- Visual-only notifications (no audio cues)
- Reduced motion support
- Glassmorphism design with warm amber accents

## Carbon Tracking

The system tracks environmental impact:

- CO2 savings from efficient data routing
- Reduced email storage
- Optimized file compression
- Dashboard shows cumulative impact

## Troubleshooting

### Common Issues

1. **Database connection errors**: Check `DATABASE_URL` environment variable
2. **OAuth failures**: Verify credentials in `source_config` table
3. **Routing job failures**: Check destination plugin configuration
4. **WebSocket disconnects**: Ensure proper CORS and WebSocket support

### Logs

All operations are logged with structured logging:

```python
logger.info(f"Processed item {item_id}")
logger.error(f"Failed to route to {destination}: {error}")
```

## Future Enhancements

- Stripe integration for payment processing
- Plaid integration for financial data routing
- Slack notifications for enterprise features
- Advanced analytics dashboard
- Machine learning for improved categorization
- Mobile app (iOS/Android)

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://www.sqlalchemy.org/)
- [OpenRouter API](https://openrouter.ai/docs)
- [WCAG AAA Guidelines](https://www.w3.org/TR/WCAG22/)

---

**Author**: Audrey Evans (MIDNGHTSAPPHIRE)
**Date**: 2026-02-15
**Description**: Comprehensive skill for Universal Data Router (Revvel) development and maintenance
