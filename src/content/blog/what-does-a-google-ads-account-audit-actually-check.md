---
title: "What Does a Google Ads Account Audit Actually Check?"
description: "A real Google Ads audit starts with data integrity, not performance metrics. Here's the full process — in order — and why the sequence matters."
pubDate: 2026-03-28
topic: "Google Ads Audit"
seo_keywords: "google ads audit, google ads account audit checklist, google ads audit what to look for, google ads audit process"
draft: false
---

**Most Google Ads audits start in the wrong place. They look at performance before verifying the data behind it. Here's the right order.**

I've done hundreds of Google Ads audits. The accounts that look like they're performing well on the surface often have structural problems that make the numbers misleading. The first job of an audit isn't to analyze performance — it's to establish whether you can trust the data at all.

Here's the process I use, in the order I use it.

## Step 1: Conversion Tracking Audit

### What conversion actions are set up?
List every conversion action in the account. For each one, verify:
- Is it tracking the right thing? (Form submission vs. page view — many accounts track 'thank you page views' and call them conversions, which is correct, but verify)
- Is it the primary action you're optimizing toward?
- What's the conversion window? Does it match your sales cycle?

### Is anything double-counting?
This is the most common issue I find. A thank-you page fires a Google Ads conversion tag AND a Google Analytics goal, both imported into Google Ads. Every conversion gets counted twice. CPL looks half as expensive as it actually is.

Check: are any conversion actions being counted that come from the same action through different tracking paths?

### Is the tracking actually firing correctly?
Use Tag Assistant or the Google Ads conversion test tool. Watch a test conversion happen and verify it registers exactly once.

## Step 2: Campaign Settings Review

### Are Search campaigns opted into the Display Network?
Go to every Search campaign → Settings → Networks. If 'Display Network' is checked, uncheck it. This is the most common budget leak I find in audited accounts.

### Are Search Partners enabled?
Search Partners (third-party sites that show Google ads) vary significantly in quality. Check your Search Partners performance segmented by network. If cost per lead is materially higher than Google Search alone, turn them off.

### What bidding strategy is each campaign using?
Are automated bidding strategies using enough conversion data to work properly? Target CPA bidding needs at least 30-50 conversions in the last 30 days to function well. Accounts using Target CPA with 5 monthly conversions are giving the algorithm too little to work with.

## Step 3: Search Terms Report

### Where is the budget actually going?
Sort search terms by cost, descending. Look at the top 20 terms eating budget. Are they relevant? Are they what you'd have chosen as keywords?

### What irrelevant queries are triggering ads?
Filter for search terms with spend but zero conversions. How many are clearly irrelevant? This shows you the waste — and tells you how aggressive your match types are.

### What negative keywords are missing?
Based on irrelevant queries found, what negatives should be added immediately? Build a list during the audit.

## Step 4: Ad and Landing Page Review

### Do ads match what the landing page delivers?
If someone searches 'emergency plumber' and your ad says '24/7 Emergency Plumbing,' does the landing page immediately confirm that's what they're getting? Message match between ad and landing page is one of the highest-leverage conversion rate factors.

### Are ads testing variations?
Every ad group should have at least 2-3 active ad variations. If every ad group has one ad, you're not learning anything about what resonates.

## Step 5: Quality Score and Ad Rank Review

Quality Score (1-10) reflects expected CTR, ad relevance, and landing page experience. Keywords with Quality Scores below 5 are expensive — you're paying more per click than competitors with better scores for the same position.

Low Quality Scores usually point to: ad copy that doesn't match the keyword, landing pages that don't match the ad, or keywords that are too broadly defined.

## What to Fix First

Not everything an audit reveals needs to be fixed immediately. Prioritize in this order:

1. Fix tracking issues — everything downstream depends on clean data
2. Remove Display Network from Search campaigns — immediate budget recovery
3. Add critical negative keywords — stop the bleeding
4. Address major Quality Score issues — reduces costs per click
5. Test ad variations — medium-term improvement
