# API Services Inventory

This document provides a comprehensive inventory of all API keys and services used in projects for Audrey Evans (MIDNGHTSAPPHIRE). It is intended as a template and should **NEVER** contain actual API keys.

## Services Inventory

| Service | Description | Environment Variable | Key Format (if known) | Notes |
| :--- | :--- | :--- | :--- | :--- |
| OpenRouter | API key for 300+ AI models | `OPENROUTER_API_KEY` | `sk-or-v1-...` | |
| Perplexity | Search API and agent | `PERPLEXITY_API_KEY` | `pplx-xxxxx` | |
| OpenAI | GPT models | `OPENAI_API_KEY` | `sk-...` | |
| GitHub | MIDNGHTSAPPHIRE account | N/A | N/A | Authenticated via `gh` CLI |
| Google Drive | Connected storage | N/A | N/A | Connected via rclone |
| Gmail | Email accounts | N/A | N/A | angelreporters@gmail.com, aevans_ocda@yahoo.com |
| Amazon | Vine reviewer account | N/A | N/A | 80K views, 500 upvotes |
| SoundCloud | Music (Revvel/Hailstorm) | N/A | N/A | |
| TikTok | Social media account | N/A | N/A | #MeetAudreyEvans |
| SSRN | Published author | N/A | N/A | Audrey Walter-Evans |
| Grants.gov | Registered account | N/A | N/A | |
| DUNS Numbers | Multiple | N/A | N/A | Need recovery from emails |
| Stripe | Payment processing | `STRIPE_SECRET_KEY` | `sk_live_...` or `sk_test_...` | To be set up |
| Domains | Various domains | N/A | N/A | meetaudreyevans.com, yumyumcode.com, growlingeyes.com, truthslayer.com, glowstarlabs.com, reesereviews.com |
| Freedom Angel Corps | Nonprofit EIN | N/A | N/A | |

## Setting Up Environment Variables

### Windows

**Using Command Prompt (cmd):**

```bash
setx VARIABLE_NAME "your_value"
```

**Using PowerShell:**

```powershell
[System.Environment]::SetEnvironmentVariable("VARIABLE_NAME", "your_value", "User")
```

### macOS and Linux

```bash
export VARIABLE_NAME="your_value"
```

To make this permanent, add the line to your shell's configuration file (e.g., `~/.bashrc`, `~/.zshrc`).

## Using .env Files Safely

A `.env` file is a simple text file that contains key-value pairs of your environment variables. It allows you to load sensitive information into your application without hardcoding it.

1.  **Create a `.env` file** in the root of your project.
2.  **Add your environment variables** in the format `VARIABLE_NAME=your_value`.
3.  **Add `.env` to your `.gitignore` file.** This is the most important step to prevent accidentally committing your secret keys to a public repository.

## Key Rotation

Key rotation is the process of periodically changing your API keys. This is a critical security practice to limit the damage if a key is compromised.

1.  **Generate a new key** from the service provider's dashboard.
2.  **Update your application** to use the new key. It's best to have a brief period where both the old and new keys work to ensure a smooth transition.
3.  **Deactivate the old key** once you have confirmed the new key is working correctly.

## Template .env.example File

This file should be committed to your repository. It serves as a template for other developers to know which environment variables are needed for the project.

```
# OpenRouter API Key
OPENROUTER_API_KEY=

# Perplexity API Key
PERPLEXITY_API_KEY=

# OpenAI API Key
OPENAI_API_KEY=

# Stripe Secret Key
STRIPE_SECRET_KEY=
```

## Security Best Practices

- **Never commit actual keys to version control.** Use environment variables or a secret management service.
- **Do not share keys in plain text** over email or messaging apps.
- **Rotate keys regularly**, especially if you suspect a key has been compromised.
- **Use different keys for different environments** (development, testing, production).
- **Grant the least privilege necessary.** If a key only needs read access, do not give it write access.
