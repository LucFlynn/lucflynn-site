# SPEC: Programmatic SEO Page Generation & Site Integration

## Context

lucflynn.com is a Next.js site deployed on Vercel from the `LucFlynn/lucflynn-site` repo. It currently serves:
- `/` — homepage
- `/blog/[slug]` — editorial posts (markdown-based)
- `/sop/[slug]` — SOP library
- `/templates/[slug]` — interactive tools
- `/contact` — contact/audit request form

We are adding 147 programmatic SEO pages across 4 new route groups plus 13 hub/pillar pages. Total: 160 new pages.

## Deliverables

### Phase 1: Generator Setup

1. Copy the `seo-generator/` directory into the repo root (or wherever makes sense as a scripts directory)
2. Install dependency: `pip install anthropic`
3. Run generation, P0 pages first, then all:
   ```
   cd seo-generator
   python generate.py --priority P0
   python generate.py
   ```
4. Output lands in `content/pages/{category}/{slug}.md`
5. Verify: should be 147 markdown files across `content/pages/tracking/`, `content/pages/integrations/`, `content/pages/attribution/`, `content/pages/services/`

### Phase 2: Next.js Route Integration

Create dynamic routes that render the generated markdown pages. Match the existing blog rendering pattern (study how `/blog/[slug]` works in the codebase and replicate the same approach for the new routes).

**New routes to create:**
- `app/tracking/[slug]/page.tsx` — reads from `content/pages/tracking/`
- `app/integrations/[slug]/page.tsx` — reads from `content/pages/integrations/`
- `app/attribution/[slug]/page.tsx` — reads from `content/pages/attribution/`
- `app/services/[slug]/page.tsx` — reads from `content/pages/services/`

**Each route must:**
- Parse frontmatter (title, description, date, slug, category) using the same markdown/frontmatter parser the blog uses (likely gray-matter + remark/rehype or similar — check the existing codebase)
- Render markdown to HTML with syntax highlighting for code blocks (the pages contain JavaScript, HTML, and GTM config snippets)
- Use the same layout/wrapper component as blog posts (nav, footer, consistent styling)
- Generate proper `<head>` metadata from frontmatter (title, description, og tags)
- Generate `generateStaticParams()` that reads all .md files in the content directory to pre-render at build time
- Return 404 for unknown slugs

**Important: don't reinvent the wheel.** The blog already does markdown → page rendering. Reuse that infrastructure. If the blog uses a shared `<MarkdownRenderer>` or `<PostLayout>` component, use it. If it parses markdown with a specific library, use the same one.

### Phase 3: Hub Pages

After spoke pages are generated and routes are working, generate 13 hub/pillar pages. These are special because they aggregate links to their spoke pages.

**Hub pages to create** (save to `content/pages/{category}/` alongside the spokes):

| Slug | Route | Purpose |
|------|-------|---------|
| `google-ads-conversion-tracking` | `/tracking/google-ads-conversion-tracking` | Links all Google Ads tracking guides |
| `meta-ads-conversion-tracking` | `/tracking/meta-ads-conversion-tracking` | Links all Meta Ads tracking guides |
| `ga4-event-tracking` | `/tracking/ga4-event-tracking` | Links all GA4 implementation guides |
| `server-side-gtm` | `/tracking/server-side-gtm` | Master sGTM guide |
| `form-conversion-tracking` | `/tracking/form-conversion-tracking` | Links all form × platform combos |
| `enhanced-conversions` | `/tracking/enhanced-conversions` | Enhanced Conversions master guide |
| `linkedin-ads-conversion-tracking` | `/tracking/linkedin-ads-conversion-tracking` | LinkedIn tracking guides |
| `form-to-crm` | `/integrations/form-to-crm` | Master form → CRM guide |
| `hubspot` | `/integrations/hubspot` | All HubSpot integrations |
| `salesforce` | `/integrations/salesforce` | All Salesforce integrations |
| `gohighlevel` | `/integrations/gohighlevel` | All GHL integrations |
| `attribution` | `/attribution/attribution` (or index) | Attribution tools overview |
| `services` | `/services/services` (or index) | All services overview |

**Hub page generation approach:**
- Read `pages.json` to find all spokes that reference each hub via `hub_page` field
- Generate a markdown file for each hub that includes:
  - An intro paragraph (2-3 sentences explaining what this hub covers)
  - A linked list of all spoke pages with their titles
  - Grouped by subcategory where it makes sense (e.g., form tool or ad platform)
  - CTA to /contact at the bottom
- Use the same Claude API call pattern as the spoke generator, but with a hub-specific prompt
- OR generate these statically from the JSON data without an API call (simpler, and hub pages are mostly structured links anyway)

### Phase 4: Index Pages

Create listing/index pages for each route group so `/tracking`, `/integrations`, `/attribution`, `/services` aren't 404s.

**Options (pick whichever matches the site's existing patterns):**
- If the site uses `app/blog/page.tsx` as a blog listing page, create equivalent listing pages for each new route group
- Each listing page should show all pages in that category, sorted by priority (P0 first), with title and description
- Include the hub pages at the top as featured/pillar content

### Phase 5: Internal Linking from Existing Content

Update existing blog posts and SOPs to link into the new cluster pages where relevant:

- `/sop/conversion-tracking` should link to `/tracking/form-conversion-tracking` hub and relevant method guides
- `/sop/lead-scoring` should link to `/attribution` hub
- Blog posts about tracking should link to relevant tracking spoke pages
- Homepage `/` "Conversion Tracking Setup" section should link to `/tracking/form-conversion-tracking`

**Approach:** Read existing content files, find natural insertion points for links, add them. Don't force links where they don't fit. 2-3 new internal links per existing page max.

### Phase 6: Sitemap & SEO

1. Ensure all new pages are included in the sitemap (if the site generates sitemap.xml automatically via Next.js, this should happen for free with `generateStaticParams`)
2. Add a `robots.txt` entry if one doesn't exist
3. Verify the site builds successfully with all new pages: `npm run build` should complete without errors

## File Structure (Expected End State)

```
lucflynn-site/
├── app/
│   ├── tracking/
│   │   └── [slug]/
│   │       └── page.tsx
│   ├── integrations/
│   │   └── [slug]/
│   │       └── page.tsx
│   ├── attribution/
│   │   └── [slug]/
│   │       └── page.tsx
│   ├── services/
│   │   └── [slug]/
│   │       └── page.tsx
│   ├── blog/
│   │   └── [slug]/
│   │       └── page.tsx          ← existing
│   └── sop/
│       └── [slug]/
│           └── page.tsx          ← existing
├── content/
│   ├── pages/
│   │   ├── tracking/             ← 47 markdown files (40 spokes + 7 hubs)
│   │   ├── integrations/         ← 63 markdown files (60 spokes + 3 hubs)
│   │   ├── attribution/          ← 13 markdown files (12 spokes + 1 hub)
│   │   └── services/             ← 16 markdown files (15 spokes + 1 hub)
│   └── blog/                     ← existing blog posts
├── seo-generator/
│   ├── pages.json
│   ├── system_prompt.txt
│   ├── generate.py
│   ├── generate_pages_json.py
│   └── README.md
└── ...
```

## Important Notes

- **Match existing patterns.** Before creating anything new, read the existing codebase. See how blog posts are rendered, what libraries are used, what components exist. Replicate that pattern.
- **The generator writes markdown files. The site renders them.** These are two separate concerns. The generator is a one-time script. The site routes are permanent.
- **Don't touch the ECF pipeline.** Blog posts at `/blog/[slug]` are managed by the ECF content factory (Cloud Scheduler → GitHub commits → Vercel). The new programmatic pages are separate — they live in `content/pages/` not wherever ECF puts blog posts.
- **Feature branch.** Do all work on a feature branch. PR into main. Don't push directly to main.
- **Build must pass.** Run `npm run build` before committing. All 160 pages must render without errors.
- **No placeholder content.** Every page must have real, generated content before merging. Don't merge with empty markdown files or "TODO" placeholders.

## Execution Order

1. Study existing codebase (blog rendering, markdown parsing, layout components)
2. Run the page generator (Phase 1)
3. Create routes that render the generated pages (Phase 2)
4. Verify build passes and pages render correctly
5. Generate hub pages (Phase 3)
6. Create index/listing pages (Phase 4)
7. Add internal links to existing content (Phase 5)
8. Final build verification and sitemap check (Phase 6)
9. Open PR
