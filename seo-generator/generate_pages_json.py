"""Generate the pages.json data file with all page definitions."""
import json

form_tools = [
    {"name": "Gravity Forms", "slug": "gravity-forms", "platform": "WordPress", "notes": "AJAX submission via gform_confirmation_loaded event. Field IDs are numeric (input_1, input_3). Most common WordPress form plugin."},
    {"name": "WPForms", "slug": "wpforms", "platform": "WordPress", "notes": "Uses wpformsAjaxSubmitSuccess event. Lite version is free. Field mapping is more intuitive than Gravity Forms."},
    {"name": "Contact Form 7", "slug": "contact-form-7", "platform": "WordPress", "notes": "Fires wpcf7mailsent DOM event on submission. No built-in entry storage — submissions go to email only unless you add Flamingo plugin. Very lightweight."},
    {"name": "Unbounce", "slug": "unbounce", "platform": "Standalone Landing Page", "notes": "Has its own tag manager and form system. Can fire conversion events via Unbounce Scripts or redirect to thank-you URL. Often used with external GTM snippet."},
    {"name": "HubSpot Forms", "slug": "hubspot-forms", "platform": "HubSpot CMS or Embedded", "notes": "Fires hsFormCallback and window.addEventListener for onFormSubmitted. Native HubSpot tracking pixel handles most HubSpot-specific tracking. Embedded forms on non-HubSpot sites need GTM listener."},
    {"name": "Typeform", "slug": "typeform", "platform": "Standalone or Embedded", "notes": "Embedded Typeform uses postMessage events. Can use Typeform webhooks for server-side tracking. Redirect on completion is the simplest tracking method."},
    {"name": "Jotform", "slug": "jotform", "platform": "Standalone or Embedded", "notes": "Fires submission via iframe postMessage. Thank-you page redirect is most reliable tracking method. Has native integrations with most CRMs."},
    {"name": "Elementor Forms", "slug": "elementor-forms", "platform": "WordPress", "notes": "Fires submit event on .elementor-form. Can use Elementor's built-in Actions After Submit to redirect or trigger webhook. Works well with GTM form submission trigger."},
    {"name": "Formidable Forms", "slug": "formidable-forms", "platform": "WordPress", "notes": "Fires frmFormComplete event. Good for complex multi-page forms. Field IDs follow frm_field_X_container pattern."},
    {"name": "Calendly", "slug": "calendly", "platform": "Standalone or Embedded", "notes": "Fires calendly.event_scheduled postMessage event when embedded. Can also track via redirect URL after booking. Native webhooks available for server-side tracking."},
]

ad_platforms = [
    {"name": "Google Ads", "slug": "google-ads", "tag_type": "Google Ads Conversion Tracking tag", "verification": "Google Ads → Goals → Conversions status column", "notes": "Use Conversion ID + Label. Set counting to 'One' for leads. Enhanced Conversions strongly recommended. 30-day default attribution window."},
    {"name": "Meta Ads", "slug": "meta-ads", "tag_type": "Meta Pixel event tag", "verification": "Events Manager → Test Events tool", "notes": "Use standard event 'Lead' or custom conversion. Meta CAPI strongly recommended for server-side deduplication. Event deduplication via event_id required if using both pixel and CAPI."},
    {"name": "GA4", "slug": "ga4", "tag_type": "GA4 Event tag", "verification": "GA4 → DebugView and Realtime reports", "notes": "Send as 'generate_lead' recommended event or custom event. Mark as conversion in GA4 admin. Can link to Google Ads for import."},
    {"name": "LinkedIn Ads", "slug": "linkedin-ads", "tag_type": "LinkedIn Insight Tag conversion event", "verification": "LinkedIn Campaign Manager → Analyze → Conversions", "notes": "Uses LinkedIn Insight Tag base code + event-specific pixel. Online conversions tracked via image pixel or event-based tracking. Less mature than Google/Meta tracking."},
]

tracking_methods = [
    {"name": "Client-Side GTM", "slug": "gtm"},
    {"name": "Server-Side GTM", "slug": "server-side-gtm"},
    {"name": "Meta CAPI", "slug": "meta-capi"},
    {"name": "Enhanced Conversions", "slug": "enhanced-conversions"},
    {"name": "Offline Conversion Import", "slug": "offline-conversions"},
    {"name": "Webhooks / Direct API", "slug": "webhooks"},
]

crms = [
    {"name": "HubSpot", "slug": "hubspot", "notes": "Native integrations with most form tools. REST API for custom integrations. Contact properties map to form fields. Workflows can trigger on form submission."},
    {"name": "Salesforce", "slug": "salesforce", "notes": "Web-to-Lead for simple setups. REST API for custom. Lead vs Contact object matters. Field mapping requires matching API names. Pardot adds marketing automation layer."},
    {"name": "GoHighLevel", "slug": "gohighlevel", "notes": "Webhook-based integration is most reliable. Native Zapier connection available. Contact and Opportunity objects. Pipeline automation on inbound leads. Popular with agencies."},
    {"name": "ActiveCampaign", "slug": "activecampaign", "notes": "Form tool integrations via native or Zapier. Contact + Deal objects. Automation triggers on contact creation. Custom fields map to form fields."},
    {"name": "Zoho CRM", "slug": "zoho", "notes": "Web forms generate leads directly. REST API for custom. Lead and Contact modules. Blueprint automation available. Zoho Forms has native integration."},
    {"name": "Mailchimp", "slug": "mailchimp", "notes": "Audience/List based. Tags and segments for organization. Limited CRM functionality — better as email destination than true CRM. API and Zapier integrations."},
]

attribution_tools = [
    {"name": "Hyros", "slug": "hyros", "notes": "Call tracking + web tracking. Universal script + CAPI integration. Requires proper URL parameter passthrough. Known for accurate long-funnel attribution."},
    {"name": "Triple Whale", "slug": "triple-whale", "notes": "E-commerce focused but expanding. Pixel-based tracking + data warehouse integrations. Shopify-native with expanding platform support."},
    {"name": "Northbeam", "slug": "northbeam", "notes": "ML-based attribution modeling. Requires pixel installation + data connections to ad platforms. Custom attribution windows."},
    {"name": "Wicked Reports", "slug": "wicked-reports", "notes": "CRM-based attribution. Requires CRM integration + ad platform connections. Strong for B2B and longer sales cycles."},
]

attr_platforms = [
    {"name": "Google Ads", "slug": "google-ads"},
    {"name": "Meta Ads", "slug": "meta-ads"},
    {"name": "Multi-Channel", "slug": "multi-channel"},
]

service_verticals = [
    {"name": "Law Firms", "slug": "law-firm", "notes": "High CPC ($50-200+). Competitive local search. Call tracking critical. Case value justifies high ad spend. Compliance restrictions on ad copy."},
    {"name": "Home Services", "slug": "home-services", "notes": "Local service ads + search. Seasonal demand patterns. Lead quality varies wildly. Phone calls are primary conversion. Service area targeting."},
    {"name": "Healthcare / Medical", "slug": "healthcare", "notes": "HIPAA considerations for tracking. Limited remarketing. High patient lifetime value. Location-based targeting. Appointment booking as conversion."},
    {"name": "Higher Education", "slug": "higher-education", "notes": "Long enrollment cycles. Multiple touch attribution matters. Program-level campaigns. Lead nurture is critical. Seasonal enrollment windows."},
    {"name": "SaaS / B2B", "slug": "saas", "notes": "Demo/trial as primary conversion. Long sales cycles. Account-based targeting. LinkedIn often outperforms for enterprise. Free trial → paid conversion tracking."},
    {"name": "E-commerce", "slug": "ecommerce", "notes": "ROAS-focused. Shopping campaigns. Dynamic remarketing. Cart abandonment tracking. Revenue tracking with transaction data."},
    {"name": "Real Estate", "slug": "real-estate", "notes": "High-value leads. Local targeting critical. Listing-specific landing pages. Lead registration forms. IDX integration tracking."},
    {"name": "Dental / Orthodontics", "slug": "dental", "notes": "Local search dominant. New patient value $3K-10K+. Call tracking essential. Insurance vs cash-pay targeting. Before/after content."},
    {"name": "Roofing", "slug": "roofing", "notes": "Storm-chasing seasonal spikes. Local service ads. High ticket ($8K-25K+). Lead quality filtering critical. Emergency vs planned replacement."},
    {"name": "HVAC", "slug": "hvac", "notes": "Seasonal demand (summer cooling, winter heating). Emergency service calls. Maintenance agreement upsells. Local targeting. Call tracking."},
]

service_technical = [
    {"name": "Conversion Tracking Audit", "slug": "tracking-audit", "notes": "Full audit of all tracking tags, pixels, and conversion events. Identifies gaps, double-counting, and misattribution. Deliverable: audit report + fix list."},
    {"name": "Server-Side GTM Implementation", "slug": "server-side-gtm-setup", "notes": "Full sGTM deployment on custom subdomain. Includes Google Ads, Meta CAPI, GA4 server-side configs. First-party data collection setup."},
    {"name": "Meta CAPI Implementation", "slug": "meta-capi-setup", "notes": "Meta Conversions API setup via sGTM or direct integration. Event deduplication. Data quality verification in Events Manager."},
    {"name": "GA4 Setup & Configuration", "slug": "ga4-setup", "notes": "Full GA4 property setup. Event tracking configuration. Conversion marking. Google Ads linking. Custom dimensions and audiences."},
    {"name": "Attribution Platform Setup", "slug": "attribution-setup", "notes": "Setup and configuration of third-party attribution tools (Hyros, Triple Whale, etc). URL parameter configuration. Platform integration verification."},
]

pages = []

# CLUSTER A: Form × Ad Platform
for ft in form_tools:
    for ap in ad_platforms:
        priority = "P0" if ft["slug"] in ["gravity-forms", "unbounce", "hubspot-forms", "contact-form-7", "wpforms"] and ap["slug"] in ["google-ads", "meta-ads"] else "P1"
        primary_method = "Meta CAPI" if ap["slug"] == "meta-ads" else "Enhanced Conversions" if ap["slug"] == "google-ads" else "Client-Side GTM"
        pages.append({
            "cluster": "A",
            "route_prefix": "/tracking",
            "slug": f"{ft['slug']}-{ap['slug']}-conversion-tracking",
            "form_tool": ft,
            "ad_platform": ap,
            "tracking_method": primary_method,
            "title": f"How to Track {ft['name']} Conversions in {ap['name']} (2026 Guide)",
            "h1": f"{ft['name']} + {ap['name']} Conversion Tracking Setup",
            "meta_description": f"Step-by-step guide to tracking {ft['name']} form submissions as conversions in {ap['name']}. Covers GTM setup, {primary_method}, testing, and troubleshooting.",
            "search_intent": "Transactional / How-to",
            "priority": priority,
            "hub_page": f"/tracking/{ap['slug']}-conversion-tracking",
            "related_spokes": [
                f"/tracking/{ft['slug']}-{other_ap['slug']}-conversion-tracking" 
                for other_ap in ad_platforms if other_ap['slug'] != ap['slug']
            ],
            "cta_link": "/contact",
            "page_type": "spoke",
        })

# CLUSTER B: Form × CRM
for ft in form_tools:
    for crm in crms:
        priority = "P0" if ft["slug"] in ["gravity-forms", "unbounce", "hubspot-forms", "wpforms", "contact-form-7"] and crm["slug"] in ["hubspot", "salesforce", "gohighlevel"] else "P1"
        pages.append({
            "cluster": "B",
            "route_prefix": "/integrations",
            "slug": f"{ft['slug']}-to-{crm['slug']}",
            "form_tool": ft,
            "crm": crm,
            "title": f"How to Send {ft['name']} Leads to {crm['name']} (Setup Guide)",
            "h1": f"{ft['name']} → {crm['name']} Integration Guide",
            "meta_description": f"Connect {ft['name']} to {crm['name']} so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping.",
            "search_intent": "Transactional / Integration",
            "priority": priority,
            "hub_page": f"/integrations/{crm['slug']}",
            "related_spokes": [
                f"/integrations/{ft['slug']}-to-{other_crm['slug']}" 
                for other_crm in crms if other_crm['slug'] != crm['slug']
            ][:3],
            "cta_link": "/contact",
            "page_type": "spoke",
        })

# CLUSTER C: Tracking Method × Platform (curated combos)
method_combos = [
    ("Server-Side GTM", "server-side-gtm", "Google Ads", "google-ads"),
    ("Server-Side GTM", "server-side-gtm", "Meta Ads", "meta-ads"),
    ("Server-Side GTM", "server-side-gtm", "GA4", "ga4"),
    ("Server-Side GTM", "server-side-gtm", "LinkedIn Ads", "linkedin-ads"),
    ("Server-Side GTM", "server-side-gtm", "TikTok Ads", "tiktok-ads"),
    ("Meta CAPI", "meta-capi", "Meta Ads", "meta-ads"),
    ("Enhanced Conversions", "enhanced-conversions", "Google Ads", "google-ads"),
    ("Enhanced Conversions", "enhanced-conversions", "GA4", "ga4"),
    ("Offline Conversion Import", "offline-conversions", "Google Ads", "google-ads"),
    ("Offline Conversion Import", "offline-conversions", "Meta Ads", "meta-ads"),
    ("Offline Conversion Import", "offline-conversions", "LinkedIn Ads", "linkedin-ads"),
    ("Client-Side GTM", "gtm", "Google Ads", "google-ads"),
    ("Client-Side GTM", "gtm", "Meta Ads", "meta-ads"),
    ("Client-Side GTM", "gtm", "GA4", "ga4"),
    ("Client-Side GTM", "gtm", "LinkedIn Ads", "linkedin-ads"),
    ("Client-Side GTM", "gtm", "TikTok Ads", "tiktok-ads"),
    ("Client-Side GTM", "gtm", "Microsoft Ads", "microsoft-ads"),
    ("Webhooks / Direct API", "webhooks", "Google Ads", "google-ads"),
    ("Webhooks / Direct API", "webhooks", "Meta Ads", "meta-ads"),
    ("Webhooks / Direct API", "webhooks", "LinkedIn Ads", "linkedin-ads"),
]

for method_name, method_slug, ap_name, ap_slug in method_combos:
    priority = "P0" if "Server-Side" in method_name or "Enhanced" in method_name or "CAPI" in method_name else "P1"
    pages.append({
        "cluster": "C",
        "route_prefix": "/tracking",
        "slug": f"{method_slug}-{ap_slug}-setup",
        "tracking_method_name": method_name,
        "tracking_method_slug": method_slug,
        "ad_platform_name": ap_name,
        "ad_platform_slug": ap_slug,
        "title": f"{method_name} for {ap_name}: Complete Setup Guide (2026)",
        "h1": f"{method_name} + {ap_name} Setup Guide",
        "meta_description": f"Complete guide to setting up {method_name} for {ap_name}. Step-by-step configuration, testing, and troubleshooting.",
        "search_intent": "Transactional / Technical",
        "priority": priority,
        "hub_page": f"/tracking/{method_slug}" if method_slug != "gtm" else "/tracking/form-conversion-tracking",
        "page_type": "spoke",
    })

# CLUSTER D: Attribution
for tool in attribution_tools:
    for ap in attr_platforms:
        priority = "P0" if tool["slug"] == "hyros" else "P1"
        pages.append({
            "cluster": "D",
            "route_prefix": "/attribution",
            "slug": f"{tool['slug']}-{ap['slug']}-setup",
            "attribution_tool": tool,
            "ad_platform_name": ap["name"],
            "ad_platform_slug": ap["slug"],
            "title": f"{tool['name']} + {ap['name']} Attribution Setup Guide (2026)",
            "h1": f"How to Set Up {tool['name']} for {ap['name']}",
            "meta_description": f"Step-by-step {tool['name']} setup for {ap['name']} attribution. Covers pixel installation, integration configuration, and verification.",
            "search_intent": "Transactional / Setup",
            "priority": priority,
            "hub_page": "/attribution",
            "page_type": "spoke",
        })

# CLUSTER E: Service Pages — Verticals
for v in service_verticals:
    pages.append({
        "cluster": "E",
        "route_prefix": "/services",
        "slug": f"{v['slug']}-google-ads",
        "vertical": v,
        "title": f"Google Ads Management for {v['name']}",
        "h1": f"Google Ads for {v['name']}",
        "meta_description": f"Managed Google Ads for {v['name']}. Tracking setup, campaign management, and conversion optimization. $800 setup + $200/month.",
        "search_intent": "Commercial / Service",
        "priority": "P0" if v["slug"] in ["law-firm", "home-services", "healthcare", "higher-education"] else "P1",
        "page_type": "service_vertical",
    })

# CLUSTER E: Service Pages — Technical
for s in service_technical:
    pages.append({
        "cluster": "E",
        "route_prefix": "/services",
        "slug": s["slug"],
        "service": s,
        "title": s["name"],
        "h1": s["name"],
        "meta_description": f"{s['notes'][:150]}",
        "search_intent": "Commercial / Service",
        "priority": "P0" if s["slug"] in ["tracking-audit", "server-side-gtm-setup", "meta-capi-setup"] else "P1",
        "page_type": "service_technical",
    })

# Summary
cluster_counts = {}
for p in pages:
    c = p["cluster"]
    cluster_counts[c] = cluster_counts.get(c, 0) + 1

print(f"Total pages: {len(pages)}")
for c, count in sorted(cluster_counts.items()):
    print(f"  Cluster {c}: {count} pages")

with open('/home/claude/seo-generator/pages.json', 'w') as f:
    json.dump(pages, f, indent=2)
print("\nSaved to pages.json")
