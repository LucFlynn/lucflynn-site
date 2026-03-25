# SEO Page Generator — lucflynn.com

Generates 147 programmatic SEO pages across 5 clusters by calling the Claude API.

## Quick Start

```bash
# Install dependency
pip install anthropic

# Set your API key
export ANTHROPIC_API_KEY=sk-ant-...

# See what will be generated
python generate.py --dry-run

# Generate P0 pages first (highest priority, ~50 pages)
python generate.py --priority P0

# Generate a specific cluster
python generate.py --cluster A

# Generate everything
python generate.py

# Generate a single page (useful for testing)
python generate.py --slug gravity-forms-google-ads-conversion-tracking
```

## Output

Pages are written to `content/pages/{category}/{slug}.md`:

```
content/pages/
├── tracking/
│   ├── gravity-forms-google-ads-conversion-tracking.md
│   ├── gravity-forms-meta-ads-conversion-tracking.md
│   ├── server-side-gtm-google-ads-setup.md
│   └── ...
├── integrations/
│   ├── gravity-forms-to-hubspot.md
│   ├── unbounce-to-salesforce.md
│   └── ...
├── attribution/
│   ├── hyros-google-ads-setup.md
│   └── ...
└── services/
    ├── law-firm-google-ads.md
    ├── tracking-audit.md
    └── ...
```

## Cost Estimate

Using Claude Sonnet at $3/M input, $15/M output:
- Per page: ~2K input tokens, ~3K output tokens ≈ $0.05
- All 147 pages: ~$7-8 total
- P0 only (~50 pages): ~$2-3

## Files

- `pages.json` — All 147 page definitions with metadata
- `system_prompt.txt` — System prompt defining voice, tone, and structure
- `generate.py` — Generation script with CLI options
- `generate_pages_json.py` — Script that built pages.json (run once, already done)

## Flags

| Flag | Description |
|------|------------|
| `--cluster A` | Generate only cluster A (B, C, D, E) |
| `--priority P0` | Generate only P0 priority pages |
| `--slug <slug>` | Generate a single specific page |
| `--dry-run` | Show what would be generated without calling API |
| `--concurrency 5` | Max parallel API calls (default: 3) |
| `--skip-existing` | Skip pages that already have a file (default: true) |

## After Generation

1. Copy `content/pages/` into your lucflynn-site repo
2. Add Next.js dynamic routes for `/tracking/[slug]`, `/integrations/[slug]`, `/attribution/[slug]`, `/services/[slug]`
3. Build hub pages that aggregate links to spoke pages
4. Deploy via Vercel

## Clusters

| Cluster | Type | Pages | Example |
|---------|------|-------|---------|
| A | Form × Ad Platform | 40 | Gravity Forms + Google Ads tracking |
| B | Form × CRM | 60 | Unbounce → HubSpot integration |
| C | Method × Platform | 20 | Server-Side GTM for Meta Ads |
| D | Attribution | 12 | Hyros + Google Ads setup |
| E | Service Pages | 15 | Google Ads for Law Firms |
