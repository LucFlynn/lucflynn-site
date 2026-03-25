#!/usr/bin/env python3
"""
SEO Page Generator for lucflynn.com
Generates markdown files for all programmatic SEO pages by calling the Claude API.

Usage:
    # Generate all pages
    python generate.py

    # Generate specific cluster only
    python generate.py --cluster A

    # Generate specific page by slug
    python generate.py --slug gravity-forms-google-ads-conversion-tracking

    # Dry run (show what would be generated)
    python generate.py --dry-run

    # Set concurrency (default: 3)
    python generate.py --concurrency 5

Requirements:
    pip install anthropic
    export ANTHROPIC_API_KEY=your_key_here
"""

import json
import os
import sys
import time
import argparse
import asyncio
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("Install anthropic: pip install anthropic")
    sys.exit(1)

# Config
MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 4096
OUTPUT_DIR = Path(__file__).parent.parent / "src" / "content" / "pages"
PAGES_FILE = Path(__file__).parent / "pages.json"
SYSTEM_PROMPT_FILE = Path(__file__).parent / "system_prompt.txt"

def load_system_prompt():
    with open(SYSTEM_PROMPT_FILE) as f:
        return f.read()

def load_pages():
    with open(PAGES_FILE) as f:
        return json.load(f)

def build_user_prompt(page: dict) -> str:
    """Build the user prompt for a specific page based on its cluster."""
    cluster = page["cluster"]

    if cluster == "A":
        return build_cluster_a_prompt(page)
    elif cluster == "B":
        return build_cluster_b_prompt(page)
    elif cluster == "C":
        return build_cluster_c_prompt(page)
    elif cluster == "D":
        return build_cluster_d_prompt(page)
    elif cluster == "E":
        return build_cluster_e_prompt(page)
    else:
        raise ValueError(f"Unknown cluster: {cluster}")

def build_cluster_a_prompt(page: dict) -> str:
    ft = page["form_tool"]
    ap = page["ad_platform"]
    related = page.get("related_spokes", [])[:3]

    return f"""Generate a programmatic SEO page for this Form Tool + Ad Platform combination:

**Page Metadata:**
- Title: {page['title']}
- H1: {page['h1']}
- Slug: {page['slug']}
- Route: {page['route_prefix']}/{page['slug']}
- Meta Description: {page['meta_description']}

**Form Tool: {ft['name']}**
- Platform: {ft['platform']}
- Technical notes: {ft['notes']}

**Ad Platform: {ap['name']}**
- Tag type in GTM: {ap['tag_type']}
- Verification method: {ap['verification']}
- Technical notes: {ap['notes']}

**Primary tracking method to cover:** {page['tracking_method']}

**Internal links to include:**
- Hub page: {page['hub_page']}
- Related form/platform combos: {', '.join(related)}
- CTA: /contact (free tracking audit)
- Also link to the corresponding CRM integration page: /integrations/{ft['slug']}-to-hubspot

**Key requirements:**
- Include actual code for the data layer push / event listener specific to {ft['name']}
- Include GTM trigger and tag configuration steps specific to {ap['name']}
- Include {page['tracking_method']} setup for this combo
- Include testing steps using the platform-specific debug tools
- Include troubleshooting for 4-6 real issues specific to this combo
- Cross-reference numbers: {ft['name']} entries vs {ap['name']} conversion count"""

def build_cluster_b_prompt(page: dict) -> str:
    ft = page["form_tool"]
    crm = page["crm"]
    related = page.get("related_spokes", [])[:3]

    return f"""Generate a programmatic SEO page for this Form Tool → CRM integration:

**Page Metadata:**
- Title: {page['title']}
- H1: {page['h1']}
- Slug: {page['slug']}
- Route: {page['route_prefix']}/{page['slug']}
- Meta Description: {page['meta_description']}

**Form Tool: {ft['name']}**
- Platform: {ft['platform']}
- Technical notes: {ft['notes']}

**CRM: {crm['name']}**
- Technical notes: {crm['notes']}

**Internal links to include:**
- Hub page: {page['hub_page']}
- Related integrations: {', '.join(related)}
- CTA: /contact (free tracking audit)
- Also link to tracking page: /tracking/{ft['slug']}-google-ads-conversion-tracking

**Cover these integration methods (in order of preference):**
1. Native/direct integration (if one exists between {ft['name']} and {crm['name']})
2. Zapier / Make.com connection
3. Webhook + API approach
4. Manual/CSV export (mention as last resort only)

**Key requirements:**
- Include specific field mapping guidance ({ft['name']} fields → {crm['name']} fields)
- Include the actual configuration steps for each method
- Cover what happens when the integration breaks (error handling, missed leads)
- Include a testing step: submit test form → verify it appears in {crm['name']}
- Troubleshoot 4-6 real issues: duplicate contacts, missing fields, webhook failures, etc."""

def build_cluster_c_prompt(page: dict) -> str:
    return f"""Generate a programmatic SEO page for this Tracking Method + Ad Platform combination:

**Page Metadata:**
- Title: {page['title']}
- H1: {page['h1']}
- Slug: {page['slug']}
- Route: {page['route_prefix']}/{page['slug']}
- Meta Description: {page['meta_description']}

**Tracking Method: {page['tracking_method_name']}**
**Ad Platform: {page['ad_platform_name']}**

**Internal links to include:**
- Hub page: {page['hub_page']}
- CTA: /contact (free tracking audit)
- Link to related form-specific tracking pages where natural

**Key requirements:**
- This is a TECHNICAL SETUP GUIDE — more depth on the infrastructure than the form-specific pages
- Include architecture overview (how data flows from browser → server → ad platform)
- Include actual configuration: container setup, tag configs, transport URLs, API endpoints
- Include code snippets where applicable
- Cover data quality: what fields are required, what's optional, format requirements
- Testing and verification with platform-specific debug tools
- Troubleshooting 4-6 real implementation issues
- If this involves server-side tracking, cover hosting/deployment (Cloud Run, AWS, etc.)"""

def build_cluster_d_prompt(page: dict) -> str:
    tool = page["attribution_tool"]

    return f"""Generate a programmatic SEO page for this Attribution Tool + Platform combination:

**Page Metadata:**
- Title: {page['title']}
- H1: {page['h1']}
- Slug: {page['slug']}
- Route: {page['route_prefix']}/{page['slug']}
- Meta Description: {page['meta_description']}

**Attribution Tool: {tool['name']}**
- Notes: {tool['notes']}

**Ad Platform: {page['ad_platform_name']}**

**Internal links to include:**
- Hub page: {page['hub_page']}
- CTA: /contact (free tracking audit)
- Link to /services/attribution-setup for done-for-you option

**Key requirements:**
- Cover the full setup: pixel/script installation, platform connection, parameter configuration
- Include URL parameter passthrough setup (UTM + platform-specific params)
- Cover data validation: how to verify attribution is matching correctly
- Compare the tool's attribution to the ad platform's native reporting — explain expected discrepancies
- Troubleshoot 4-6 real issues specific to {tool['name']} + {page['ad_platform_name']}
- Be honest about limitations of {tool['name']}"""

def build_cluster_e_prompt(page: dict) -> str:
    if page["page_type"] == "service_vertical":
        v = page["vertical"]
        return f"""Generate a service landing page for this industry vertical:

**Page Metadata:**
- Title: {page['title']}
- H1: {page['h1']}
- Slug: {page['slug']}
- Route: {page['route_prefix']}/{page['slug']}
- Meta Description: {page['meta_description']}

**Vertical: {v['name']}**
- Industry notes: {v['notes']}

**This is a SERVICE PAGE, not a how-to guide. Different structure:**

1. **Hook** — The specific pain point for {v['name']} running Google Ads (2-3 sentences)
2. **"What's Actually Going Wrong"** — 3-4 specific problems {v['name']} face with their ad accounts (broken tracking, wasted spend, wrong attribution, bad targeting)
3. **"What I Do Differently"** — How Luc's approach is different from typical agencies. Emphasize: tracking-first methodology, infrastructure before campaigns, software-powered monitoring.
4. **"What's Included"** — Bullet list of deliverables:
   - Complete tracking infrastructure (GTM, Enhanced Conversions, Meta CAPI if applicable)
   - Campaign build and optimization
   - Automated monitoring and alerting
   - Monthly performance reports
   - Ongoing bid and budget optimization
5. **Pricing** — $800 setup + $200/month. Be direct. No "contact us for pricing."
6. **"How It Works"** — 3-step process: Audit → Build → Monitor
7. **CTA** — Link to /contact for free audit

**Do NOT make this a generic agency landing page. Make it specific to {v['name']}.**
Include specific metrics, KPIs, and challenges that are unique to this vertical."""

    else:
        s = page["service"]
        return f"""Generate a technical service page:

**Page Metadata:**
- Title: {page['title']}
- H1: {page['h1']}
- Slug: {page['slug']}
- Route: {page['route_prefix']}/{page['slug']}
- Meta Description: {page['meta_description']}

**Service: {s['name']}**
- Notes: {s['notes']}

**Structure:**
1. **Hook** — Why this service matters (tracking is the foundation, everything downstream depends on it)
2. **"What You Get"** — Specific deliverables
3. **"How It Works"** — Process overview (audit → implement → verify → document)
4. **"What It Costs"** — Be direct with pricing or ranges
5. **CTA** — Link to /contact

**Link to related tracking/integration guide pages where natural.**
Keep it under 1,000 words — service pages should be concise and action-oriented."""


def get_output_path(page: dict) -> Path:
    """Get the output file path for a page."""
    category = page["route_prefix"].strip("/")
    return OUTPUT_DIR / category / f"{page['slug']}.md"


async def generate_page(client, system_prompt: str, page: dict, semaphore: asyncio.Semaphore) -> dict:
    """Generate a single page."""
    async with semaphore:
        output_path = get_output_path(page)

        if output_path.exists():
            return {"slug": page["slug"], "status": "skipped", "reason": "already exists"}

        user_prompt = build_user_prompt(page)

        try:
            message = client.messages.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
            )

            content = message.content[0].text

            # Write file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(content)

            tokens_in = message.usage.input_tokens
            tokens_out = message.usage.output_tokens

            return {
                "slug": page["slug"],
                "status": "generated",
                "tokens_in": tokens_in,
                "tokens_out": tokens_out,
                "path": str(output_path),
            }

        except Exception as e:
            return {"slug": page["slug"], "status": "error", "error": str(e)}


async def main():
    parser = argparse.ArgumentParser(description="Generate SEO pages for lucflynn.com")
    parser.add_argument("--cluster", type=str, help="Generate only this cluster (A, B, C, D, E)")
    parser.add_argument("--slug", type=str, help="Generate only this specific slug")
    parser.add_argument("--priority", type=str, help="Generate only this priority (P0, P1, P2)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be generated")
    parser.add_argument("--concurrency", type=int, default=3, help="Max concurrent API calls")
    parser.add_argument("--skip-existing", action="store_true", default=True, help="Skip pages that already exist")
    args = parser.parse_args()

    # Load data
    system_prompt = load_system_prompt()
    pages = load_pages()

    # Filter
    if args.cluster:
        pages = [p for p in pages if p["cluster"] == args.cluster.upper()]
    if args.slug:
        pages = [p for p in pages if p["slug"] == args.slug]
    if args.priority:
        pages = [p for p in pages if p.get("priority") == args.priority]

    if not pages:
        print("No pages match the filters.")
        return

    print(f"\n{'='*60}")
    print(f"SEO Page Generator — lucflynn.com")
    print(f"{'='*60}")
    print(f"Pages to generate: {len(pages)}")
    print(f"Model: {MODEL}")
    print(f"Concurrency: {args.concurrency}")
    print(f"Output directory: {OUTPUT_DIR}")

    # Cluster breakdown
    cluster_counts = {}
    for p in pages:
        c = p["cluster"]
        cluster_counts[c] = cluster_counts.get(c, 0) + 1
    for c, count in sorted(cluster_counts.items()):
        print(f"  Cluster {c}: {count} pages")

    if args.dry_run:
        print(f"\n--- DRY RUN ---")
        for p in pages:
            path = get_output_path(p)
            exists = "EXISTS" if path.exists() else "NEW"
            print(f"  [{exists}] {p['cluster']}/{p['slug']}")
        return

    # Check API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("\nERROR: Set ANTHROPIC_API_KEY environment variable")
        print("  export ANTHROPIC_API_KEY=your_key_here")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    semaphore = asyncio.Semaphore(args.concurrency)

    print(f"\nStarting generation...\n")
    start_time = time.time()

    # Run all tasks (using sync client in async wrapper for simplicity)
    results = []
    total_tokens_in = 0
    total_tokens_out = 0
    generated = 0
    skipped = 0
    errors = 0

    for i, page in enumerate(pages):
        output_path = get_output_path(page)
        if args.skip_existing and output_path.exists():
            skipped += 1
            print(f"  [{i+1}/{len(pages)}] SKIP {page['slug']} (exists)")
            continue

        user_prompt = build_user_prompt(page)

        try:
            message = client.messages.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
            )

            content = message.content[0].text
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(content)

            tokens_in = message.usage.input_tokens
            tokens_out = message.usage.output_tokens
            total_tokens_in += tokens_in
            total_tokens_out += tokens_out
            generated += 1

            print(f"  [{i+1}/{len(pages)}] OK {page['slug']} ({tokens_out} tokens)")

        except Exception as e:
            errors += 1
            print(f"  [{i+1}/{len(pages)}] ERROR {page['slug']}: {e}")

            # Back off on rate limits
            if "rate" in str(e).lower():
                print("    Rate limited — waiting 60s...")
                time.sleep(60)

    elapsed = time.time() - start_time

    # Cost estimate (Sonnet pricing)
    cost_in = total_tokens_in * 3.0 / 1_000_000   # $3/M input tokens
    cost_out = total_tokens_out * 15.0 / 1_000_000  # $15/M output tokens
    total_cost = cost_in + cost_out

    print(f"\n{'='*60}")
    print(f"DONE in {elapsed:.0f}s")
    print(f"  Generated: {generated}")
    print(f"  Skipped:   {skipped}")
    print(f"  Errors:    {errors}")
    print(f"  Tokens:    {total_tokens_in:,} in / {total_tokens_out:,} out")
    print(f"  Est. cost: ${total_cost:.2f}")
    print(f"{'='*60}")


if __name__ == "__main__":
    asyncio.run(main())
