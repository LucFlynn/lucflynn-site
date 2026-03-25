#!/usr/bin/env python3
"""
Hub Page Generator for lucflynn.com
Generates markdown hub/pillar pages from pages.json data (no API calls).
"""

import json
from pathlib import Path
from datetime import date

PAGES_FILE = Path(__file__).parent / "pages.json"
OUTPUT_DIR = Path(__file__).parent.parent / "src" / "content" / "pages"
TODAY = date.today().isoformat()

# Hub metadata: slug -> (title, h1, description, intro)
HUB_META = {
    "/tracking/google-ads-conversion-tracking": {
        "title": "Google Ads Conversion Tracking — Complete Setup Guide Hub",
        "h1": "Google Ads Conversion Tracking Setup Guides",
        "description": "Complete library of Google Ads conversion tracking guides. Form-specific setups, Enhanced Conversions, server-side GTM, and troubleshooting.",
        "intro": "Every guide you need to get Google Ads conversion tracking working properly. I've organized these by form tool so you can jump straight to your setup. Each guide includes the actual code, GTM configuration, and testing steps — not theory.",
    },
    "/tracking/meta-ads-conversion-tracking": {
        "title": "Meta Ads Conversion Tracking — Complete Setup Guide Hub",
        "h1": "Meta Ads Conversion Tracking Setup Guides",
        "description": "Complete library of Meta Ads (Facebook) conversion tracking guides. Form-specific setups, Meta CAPI, and pixel configuration.",
        "intro": "Every guide you need to track Meta Ads conversions from your forms. Whether you're running lead gen or e-commerce, these guides cover the Pixel, Conversions API, and form-specific event firing. Pick your form tool below.",
    },
    "/tracking/ga4-conversion-tracking": {
        "title": "GA4 Event Tracking — Complete Setup Guide Hub",
        "h1": "GA4 Event Tracking Setup Guides",
        "description": "Complete library of GA4 event tracking guides. Form submissions, custom events, and measurement protocol setup.",
        "intro": "GA4's event model is powerful but confusing. These guides show you exactly how to fire custom events from your forms, validate them in DebugView, and mark them as conversions. Pick your form tool to get started.",
    },
    "/tracking/linkedin-ads-conversion-tracking": {
        "title": "LinkedIn Ads Conversion Tracking — Complete Setup Guide Hub",
        "h1": "LinkedIn Ads Conversion Tracking Setup Guides",
        "description": "Complete library of LinkedIn Ads conversion tracking guides. Insight Tag setup, event-specific tracking, and form integrations.",
        "intro": "LinkedIn conversion tracking is notoriously finicky. These guides walk you through the Insight Tag, event-specific pixels, and form tool integrations. Each one includes the exact configuration that works — not LinkedIn's generic docs.",
    },
    "/tracking/server-side-gtm": {
        "title": "Server-Side GTM — Complete Setup Guide Hub",
        "h1": "Server-Side GTM Setup Guides",
        "description": "Complete library of server-side Google Tag Manager guides. Platform-specific setup, Cloud Run deployment, and data routing.",
        "intro": "Server-side GTM is the infrastructure play that fixes most tracking issues caused by ad blockers and ITP. These guides cover the full setup: Cloud Run deployment, transport URL configuration, and platform-specific tag routing.",
    },
    "/tracking/form-conversion-tracking": {
        "title": "Form Conversion Tracking — Complete Setup Guide Hub",
        "h1": "Form Conversion Tracking Setup Guides",
        "description": "Complete library of form conversion tracking guides across all major form tools and ad platforms.",
        "intro": "The intersection of form tools and ad platforms is where most tracking breaks. These guides cover every major combination — pick your form tool and the platform you need to send conversions to.",
    },
    "/tracking/enhanced-conversions": {
        "title": "Enhanced Conversions — Complete Setup Guide Hub",
        "h1": "Enhanced Conversions Setup Guides",
        "description": "Complete library of Enhanced Conversions guides for Google Ads and GA4. First-party data, hashed user info, and conversion accuracy.",
        "intro": "Enhanced Conversions use first-party data (hashed email, phone) to recover conversions that cookie-based tracking misses. These guides cover the implementation for Google Ads and GA4 — including the GTM tag configuration and data layer setup.",
    },
    "/tracking/meta-capi": {
        "title": "Meta Conversions API (CAPI) — Setup Guide Hub",
        "h1": "Meta Conversions API Setup Guides",
        "description": "Complete guide to implementing Meta's Conversions API for server-side event tracking.",
        "intro": "Meta CAPI sends conversion events server-side, bypassing browser limitations. These guides cover the full implementation — from token generation to event deduplication to quality score optimization.",
    },
    "/tracking/offline-conversions": {
        "title": "Offline Conversion Tracking — Setup Guide Hub",
        "h1": "Offline Conversion Tracking Setup Guides",
        "description": "Complete library of offline conversion import guides for Google Ads, Meta Ads, and LinkedIn Ads.",
        "intro": "Offline conversion imports close the loop between ad clicks and CRM outcomes. These guides cover the upload formats, API integrations, and click ID passthrough setup for each major platform.",
    },
    "/tracking/webhooks": {
        "title": "Webhook & Direct API Tracking — Setup Guide Hub",
        "h1": "Webhook & Direct API Tracking Guides",
        "description": "Complete library of webhook and direct API tracking guides for sending conversion data to ad platforms.",
        "intro": "When GTM and browser-based tracking aren't enough, webhooks and direct API calls give you full control. These guides cover the payload formats, authentication, and error handling for each platform.",
    },
    "/integrations/hubspot": {
        "title": "HubSpot Integrations — Complete Form-to-CRM Guide Hub",
        "h1": "HubSpot Integration Guides",
        "description": "Complete library of form tool to HubSpot integration guides. Native connections, Zapier, webhooks, and field mapping.",
        "intro": "Getting form submissions into HubSpot reliably is the foundation of any lead gen operation. These guides cover every major form tool — native integrations where they exist, plus Zapier and webhook fallbacks when they don't.",
    },
    "/integrations/salesforce": {
        "title": "Salesforce Integrations — Complete Form-to-CRM Guide Hub",
        "h1": "Salesforce Integration Guides",
        "description": "Complete library of form tool to Salesforce integration guides. Web-to-Lead, API connections, and field mapping.",
        "intro": "Salesforce integration is more complex than most CRMs, but the payoff is worth it. These guides cover Web-to-Lead, API-based sync, and field mapping for every major form tool.",
    },
    "/integrations/gohighlevel": {
        "title": "GoHighLevel Integrations — Complete Form-to-CRM Guide Hub",
        "h1": "GoHighLevel Integration Guides",
        "description": "Complete library of form tool to GoHighLevel integration guides. Webhooks, Zapier, and pipeline automation.",
        "intro": "GHL is the go-to CRM for agencies and service businesses. These guides show you how to pipe form submissions from any major form tool into GHL contacts and pipelines — using webhooks, Zapier, or native connections.",
    },
    "/integrations/activecampaign": {
        "title": "ActiveCampaign Integrations — Complete Form-to-CRM Guide Hub",
        "h1": "ActiveCampaign Integration Guides",
        "description": "Complete library of form tool to ActiveCampaign integration guides. API connections, automations, and contact syncing.",
        "intro": "ActiveCampaign's automation engine is powerful, but only if leads actually make it in. These guides cover form-to-ActiveCampaign integrations for every major form tool — native, Zapier, and API approaches.",
    },
    "/integrations/zoho": {
        "title": "Zoho CRM Integrations — Complete Form-to-CRM Guide Hub",
        "h1": "Zoho CRM Integration Guides",
        "description": "Complete library of form tool to Zoho CRM integration guides. Web forms, API connections, and lead routing.",
        "intro": "Zoho CRM handles lead routing well once leads are in the system. These guides cover the integration for every major form tool — Zoho's native web forms, API-based sync, and Zapier connections.",
    },
    "/integrations/mailchimp": {
        "title": "Mailchimp Integrations — Complete Form-to-CRM Guide Hub",
        "h1": "Mailchimp Integration Guides",
        "description": "Complete library of form tool to Mailchimp integration guides. List sync, tag assignment, and automation triggers.",
        "intro": "Mailchimp is often the first platform businesses connect forms to. These guides cover list sync, tag assignment, and automation triggers for every major form tool.",
    },
    "/attribution": {
        "title": "Attribution Tool Setup — Complete Guide Hub",
        "h1": "Attribution Tool Setup Guides",
        "description": "Complete library of attribution tool setup guides. Hyros, Triple Whale, Northbeam, Wicked Reports — platform connections and validation.",
        "intro": "Attribution tools fill the gap between what ad platforms report and what actually happened. These guides cover the full setup — pixel installation, platform connections, parameter passthrough, and data validation.",
    },
}

# Services hub (not in pages.json hub_page references, but SPEC asks for one)
SERVICES_HUB = {
    "title": "Tracking & Analytics Services — Luc Flynn",
    "h1": "Tracking & Analytics Services",
    "description": "Professional tracking infrastructure, analytics setup, and attribution services. Done-for-you implementation by Luc Flynn.",
    "intro": "If you'd rather have someone who's done this 200+ times handle the implementation, these are the services I offer. Each one includes audit, implementation, testing, and documentation.",
}


def load_pages():
    with open(PAGES_FILE) as f:
        return json.load(f)


def generate_hub(hub_path: str, meta: dict, spokes: list):
    """Generate a hub markdown file."""
    # Parse category and slug from hub path
    parts = hub_path.strip("/").split("/")
    if len(parts) == 1:
        category = parts[0]
        slug = parts[0]
    else:
        category = parts[0]
        slug = parts[1]

    # Group spokes by cluster for better organization
    clusters = {}
    for s in spokes:
        c = s.get("cluster", "?")
        if c not in clusters:
            clusters[c] = []
        clusters[c].append(s)

    # Build markdown
    lines = [
        "---",
        f'title: "{meta["title"]}"',
        f'slug: "{slug}"',
        f'description: "{meta["description"]}"',
        f'category: "{category}"',
        f'date: "{TODAY}"',
        f'hub_page: "{hub_path}"',
        'page_type: "hub"',
        "---",
        "",
        f"# {meta['h1']}",
        "",
        meta["intro"],
        "",
    ]

    # List all spoke pages
    lines.append("## Guides")
    lines.append("")

    for spoke in sorted(spokes, key=lambda s: s["title"]):
        lines.append(f"- [{spoke['title']}]({spoke['route']})")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Need Help With Your Setup?")
    lines.append("")
    lines.append("If you'd rather not DIY this, I set up tracking infrastructure for a living. [Get a free tracking audit](/contact) and I'll tell you exactly what's broken and how to fix it.")
    lines.append("")
    lines.append(f"*This is the {meta['h1']} hub page — your starting point for all related guides.*")

    # Write file
    output_path = OUTPUT_DIR / category / f"{slug}.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines))
    print(f"  OK {category}/{slug}.md ({len(spokes)} spokes)")
    return output_path


def generate_services_hub(service_pages: list):
    """Generate the services overview hub."""
    meta = SERVICES_HUB
    lines = [
        "---",
        f'title: "{meta["title"]}"',
        'slug: "services-overview"',
        f'description: "{meta["description"]}"',
        'category: "services"',
        f'date: "{TODAY}"',
        'page_type: "hub"',
        "---",
        "",
        f"# {meta['h1']}",
        "",
        meta["intro"],
        "",
        "## Technical Services",
        "",
    ]

    technical = [p for p in service_pages if p.get("page_type") == "service_technical"]
    verticals = [p for p in service_pages if p.get("page_type") == "service_vertical"]

    for p in sorted(technical, key=lambda s: s["title"]):
        lines.append(f"- [{p['title']}]({p['route']})")

    lines.append("")
    lines.append("## Industry-Specific Google Ads Management")
    lines.append("")

    for p in sorted(verticals, key=lambda s: s["title"]):
        lines.append(f"- [{p['title']}]({p['route']})")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Ready to Get Started?")
    lines.append("")
    lines.append("[Get a free tracking audit](/contact) — I'll review your current setup and tell you exactly what needs fixing.")
    lines.append("")
    lines.append("*This is the services hub — your starting point for all tracking and analytics services.*")

    output_path = OUTPUT_DIR / "services" / "services-overview.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines))
    print(f"  OK services/services-overview.md ({len(service_pages)} pages)")


def main():
    pages = load_pages()

    # Build hub -> spokes mapping
    hubs = {}
    for p in pages:
        hp = p.get("hub_page", "")
        if hp:
            if hp not in hubs:
                hubs[hp] = []
            hubs[hp].append({
                "slug": p["slug"],
                "title": p["title"],
                "route": p["route_prefix"] + "/" + p["slug"],
                "cluster": p["cluster"],
                "page_type": p.get("page_type", "spoke"),
            })

    print(f"\nHub Page Generator — lucflynn.com")
    print(f"{'='*50}")
    print(f"Hubs to generate: {len(HUB_META) + 1}")  # +1 for services
    print(f"Output directory: {OUTPUT_DIR}\n")

    generated = 0
    for hub_path, meta in HUB_META.items():
        spokes = hubs.get(hub_path, [])
        if not spokes:
            print(f"  WARN {hub_path} has no spokes — generating anyway")
        generate_hub(hub_path, meta, spokes)
        generated += 1

    # Services hub
    service_pages = [
        {
            "slug": p["slug"],
            "title": p["title"],
            "route": p["route_prefix"] + "/" + p["slug"],
            "page_type": p.get("page_type", "spoke"),
        }
        for p in pages if p["cluster"] == "E"
    ]
    generate_services_hub(service_pages)
    generated += 1

    print(f"\n{'='*50}")
    print(f"Generated {generated} hub pages")


if __name__ == "__main__":
    main()
