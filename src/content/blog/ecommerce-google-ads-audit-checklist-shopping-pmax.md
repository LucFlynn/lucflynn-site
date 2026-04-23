---
title: "Ecommerce Google Ads Audit Checklist (Shopping + PMax)"
description: "**I've audited hundreds of ecommerce Google Ads accounts over the last eight years, and I'd estimate 80% of them are bleeding money on at least five of..."
pubDate: 2026-04-23
topic: "Google Ads"
seo_keywords: "ads, shopping, checklist, ecommerce, pmax, google, audit"
draft: false
---

# Ecommerce Google Ads Audit Checklist (Shopping + PMax)

**I've audited hundreds of ecommerce Google Ads accounts over the last eight years, and I'd estimate 80% of them are bleeding money on at least five of these issues.** Most business owners don't even know it's happening because the platforms tell a pretty story while your actual ROI slowly dies.

This checklist is for ecommerce business owners running Google Ads with Shopping campaigns, Performance Max, or both. If you're spending more than $3,000 a month and your ROAS has been trending down over the last six months — or if you inherited an account and have no idea what's actually working — keep reading.

I built this from real problems I find in real accounts. Not theory. Not best practices. The stuff that's actually costing you money right now.

## Conversion Tracking & Attribution

**1. Check if Enhanced Conversions is actually working**
Open Google Ads → Tools → Conversions → Click your purchase conversion. Look for "Enhanced conversions" status. If it says "Not set up" or "No recent enhanced conversions data," your attribution is broken. You should see enhanced conversion data matching at least 80% of your regular conversions. If you don't, Google's AI is optimizing with one hand tied behind its back.

**2. Verify GA4 ecommerce tracking alignment**
Pull the last 30 days of conversion data from Google Ads and GA4. The numbers should match within 5-10%. If GA4 shows 200 purchases and Google Ads shows 350, you've got duplicate tracking or attribution window mismatches. This means your automated bidding is chasing ghosts.

**3. Check for duplicate conversion counting**
Go to Tools → Conversions and look for multiple purchase actions. I find accounts tracking the same conversion through Google Ads tags, GA4 imports, and third-party tools simultaneously. Each sale gets counted 3x, your CPA looks amazing, and you're actually losing money on every click.

**4. Test your conversion tracking with real purchases**
Place a test order on your site. Check if it appears in Google Ads within 24 hours. If it doesn't, your tracking is broken and everything else is just organized gambling. Use Google Tag Assistant during checkout to see what fires when.

## Performance Max Campaign Structure

**5. Audit your asset groups for product relevance**
Open your Performance Max campaign → Asset groups. Each group should focus on specific product categories or customer segments. If you've got one asset group covering your entire inventory from phone cases to camping gear, the AI can't optimize effectively. Good: "Wireless Earbuds," "Running Shoes," "Coffee Equipment." Bad: "All Products."

**6. Check asset coverage and quality**
Click into each asset group. You need text assets (headlines, descriptions), images (square and landscape), logos, and video. Missing video is especially costly in 2024 — accounts with comprehensive video assets perform 25-40% better than image-only campaigns. If any category shows warnings, you're limiting where your ads can appear.

**7. Review audience signals configuration**
Look at your audience signals in each asset group. Empty audience signals = slow learning. Bad audience signals = wrong customers. Upload your customer list as a signal. Add demographics and interests that match your highest-LTV buyers. Remove broad audiences like "People interested in shopping" — that tells Google nothing useful.

**8. Verify brand exclusions are active**
Check Insights and reports → Search terms → All. If you see your own brand terms generating impressions in Performance Max, you're paying for traffic you'd get for free. Add your brand terms as negative keywords at the campaign level unless you specifically want to compete against yourself.

## Shopping Campaign Health

**9. Check Merchant Center approval status**
Open Google Merchant Center → Products → Diagnostics. Any disapproved products can't show in Shopping ads. Common issues: missing sale prices, policy violations, website claim problems. Fix disapprovals before optimizing anything else — you can't sell what Google won't show.

**10. Audit product feed quality**
Look at your product titles in Merchant Center. They should lead with the most important keywords. Bad: "SKU-12345 Blue Widget." Good: "Wireless Bluetooth Earbuds - Noise Canceling - 24hr Battery." Check that images are high-quality and prices match your website exactly. Feed quality directly impacts impression share.

**11. Review priority settings for campaign conflicts**
If you're running both Shopping and Performance Max, check Shopping campaign priorities (Low/Medium/High). Performance Max automatically gets priority over Standard Shopping, but conflicting priorities between Shopping campaigns create bidding wars against yourself.

**12. Analyze product performance segmentation**
Pull a product performance report for the last 90 days. Sort by ROAS. Your top performers should get more budget and aggressive bidding. Your bottom performers need negative keywords, bid adjustments, or removal. Most accounts spread budget equally across winners and losers.

## Search Terms & Negative Keywords

**13. Audit search term relevance**
Download 90 days of search terms from both Shopping and Performance Max. Tag each term: Relevant/Irrelevant/Branded. Add negatives for irrelevant themes immediately. Common ecommerce negatives: "free," "diy," "how to," "jobs," "walmart," "amazon," competitor names.

**14. Check for broad match bleeding**
If you see search terms that are tangentially related but not conversion-worthy, your match types are too loose. Example: selling coffee makers and showing for "coffee shop equipment" or "commercial espresso machines." Tighten with negatives or switch to phrase/exact match.

**15. Review negative keyword conflicts**
Sometimes negative keywords block legitimate traffic. If performance dropped after adding negatives, check the overlap. Adding "free" as a negative might also block "free shipping" searches that actually convert.

## Budget & Bidding Strategy

**16. Check for limited by budget campaigns**
Look at campaign status. "Limited by budget" means you're missing profitable traffic. Either increase budget or improve efficiency first. But if a campaign is limited by budget and has terrible ROAS, throwing more money at it just loses money faster.

**17. Audit bidding strategy performance**
Compare CPA and ROAS across different bidding strategies. If Target CPA campaigns consistently miss targets by more than 30%, switch to Target ROAS or manual bidding. If Target ROAS campaigns hit ROAS but generate low volume, the targets might be too aggressive.

**18. Review ad schedule performance**
Check when your ads run vs. when they perform best. If your highest ROAS hours are 2-6pm but you're spending equally across all hours, shift budget to peak performance windows. Most accounts burn money during low-intent hours out of habit.

## Network & Placement Analysis

**19. Check Search Partners performance**
Go to Networks tab in your campaigns. If Search Partners shows 20%+ lower ROAS than Google Search, disable it. Search Partners traffic is often lower quality but gets lumped into overall "Search" performance, making campaigns look better than they are.

**20. Review YouTube placement performance in Performance Max**
Performance Max runs across Search, Display, YouTube, and Gmail. Pull placement reports. If YouTube placements show terrible ROAS compared to Search, consider excluding YouTube or creating separate campaigns with different targets for different networks.

## Technical & Landing Page Issues

**21. Test mobile page speed**
Use Google PageSpeed Insights on your top-selling product pages. Scores below 50 on mobile kill conversions. I've seen 2-second speed improvements double conversion rates. Technical performance is marketing performance.

**22. Verify SSL and website claim**
Your site needs HTTPS and you need to claim it in Merchant Center. Unclaimed websites get lower impression share and potential policy violations. This takes five minutes to fix but kills performance until you do.

**23. Check for message match**
Click your own ads and verify the landing page matches the product advertised. Mismatches (wrong size, color, price, or completely different product) violate Google policies and tank Quality Scores. This happens more than you think with dynamic feeds.

## Performance Trends & Benchmarks

**24. Compare month-over-month ROAS trends**
Pull 6 months of campaign performance. Declining ROAS could mean audience fatigue, increased competition, seasonal changes, or tracking degradation. Identify if it's systematic (all campaigns) or specific (one campaign/product line).

**25. Benchmark against your email/organic revenue**
If Google Ads shows 4x ROAS but your overall business profitability is flat, you might be cannibalizing other channels or attracting deal-seekers who don't repeat purchase. True incrementality is the only metric that matters for growth.

## Scoring Your Account

**If you found 1-4 issues:** Minor optimization needed. You're probably losing 10-15% to inefficiency.

**If you found 5-9 issues:** You're likely wasting 25-35% of your ad spend. Focus on tracking and structure first.

**If you found 10+ issues:** Stop running ads until you fix the foundation. You're burning money and feeding bad data to Google's algorithms.

---

This checklist catches the obvious stuff — the problems hiding in plain sight that anyone can spot with the right list. But the things that really kill ecommerce ROAS are the problems you can't see in a self-audit. Attribution gaps between platforms. Audience overlap creating bidding wars. Feed optimization opportunities that require competitive analysis. Landing page friction that shows up in user behavior data, not campaign metrics.

That's what a professional audit uncovers. I charge $1,500 for a comprehensive ecommerce audit because it typically identifies $3,000-$8,000 in monthly waste within the first 90 days. If this checklist found problems in your account, imagine what a proper deep dive would find.
