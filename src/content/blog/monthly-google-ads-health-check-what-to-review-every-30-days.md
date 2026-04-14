---
title: "Monthly Google Ads Health Check: What to Review Every 30 Days"
description: "**I've audited hundreds of Google Ads accounts and I'd estimate 80% of them have at least 3 critical issues bleeding money every month. Most business..."
pubDate: 2026-04-14
topic: "Google Ads"
seo_keywords: "ads, check, health, days, review, every, monthly, google"
draft: false
---

# Monthly Google Ads Health Check: What to Review Every 30 Days

**I've audited hundreds of Google Ads accounts and I'd estimate 80% of them have at least 3 critical issues bleeding money every month. Most business owners have no idea it's happening.**

The worst part? These aren't complex optimization problems that require years of experience to spot. They're basic maintenance issues that accumulate when nobody's watching. A conversion action stops firing. Broad match keywords start hemorrhaging budget on irrelevant searches. A high-performing campaign hits its daily spend limit at 10 AM every day.

This checklist is for business owners and marketers running their own Google Ads who want to catch problems before they crater your ROI. If you're spending more than $2,000 a month and don't have someone checking these items regularly, you're probably wasting 20-30% of your budget. Keep reading.

I've organized this into the exact sequence I follow when I audit accounts. Each check takes 2-5 minutes. The whole process should take you under an hour monthly. And it'll save you thousands in wasted spend.

## Conversion Tracking & Data Integrity

**1. Verify conversion actions are firing**
Click into Tools & Settings > Conversions. Look at the "Recent conversions" column for the last 30 days. If any conversion action shows zero conversions but you know you had sales/leads, your tracking is broken. Good looks like: conversion numbers that roughly match your actual business results. Bad looks like: zero conversions on actions that should be firing, or conversion numbers that are 10x higher than your actual leads.

**2. Check for duplicate conversion counting**
In the same Conversions section, look at the "Count" setting for each action. If multiple conversion actions are set to "Every" instead of "One," you might be double-counting. I see this constantly — form submission conversion, thank-you page view conversion, and email confirmation conversion all firing for the same lead. Fix: Set primary conversion action to "One," disable duplicates.

**3. Review Google Analytics 4 integration**
Go to Tools & Settings > Linked accounts > Google Analytics. Verify your GA4 property is connected and importing goals correctly. Then spot-check: do your Google Ads conversion numbers roughly align with GA4 conversions for the same date range? A 10-20% difference is normal. A 200% difference means something's broken.

**4. Audit conversion attribution windows**
Still in Conversions, check the "Attribution model" and "Click-through conversion window" for each action. If you're running a 30-day sales cycle with a 1-day attribution window, you're missing most of your conversions. Match your attribution window to your actual sales cycle length, not Google's default.

## Campaign Structure & Settings

**5. Scan for mixed network campaigns**
Go to Campaigns and check the "Networks" column. If any campaign shows "Search + Display" or includes YouTube/Discovery, split them immediately. Search and Display have completely different intent levels and optimization needs. I've seen accounts waste 40% of budget on accidental Display clicks.

**6. Review campaign types alignment**
Look at your "Campaign type" column. If you're running Standard Shopping and Performance Max for the same products, they're competing against each other. If you have both Search and Performance Max targeting the same keywords/audiences, same problem. Pick one approach per objective.

**7. Check budget allocation logic**
Click into each campaign and review daily budgets. Are your best-converting campaigns hitting budget limits while low-performers get full spend? Open the "Budget" report to see which campaigns hit their daily limit and how often. Reallocate budget from campaigns with high impression share loss due to budget to campaigns that aren't budget-limited.

## Keyword & Search Term Performance

**8. Audit search terms report**
Go to Keywords > Search terms. Set date range to last 30 days, sort by clicks (descending). Look for search terms that got clicks but have nothing to do with your business. Classic red flags: job-related searches ("hiring," "salary"), competitor brand names, DIY terms when you sell services. Add irrelevant terms as negative keywords immediately.

**9. Review broad match keyword performance**
In the Keywords section, filter by "Broad match" keywords only. Check cost per conversion vs. your account average. If broad match keywords are converting at 2x+ your account average cost, either add them as negative keywords or switch them to phrase match with tight negatives. Broad match should scale winners, not explore wildly.

**10. Check for keyword cannibalization**
Look for multiple keywords in the same ad group triggering for similar searches. Example: if you have both "plumber near me" (phrase) and "emergency plumber" (broad), they might both trigger for "emergency plumber near me." Use the auction insights report to see if you're competing against yourself.

## Ad Creative & Extensions

**11. Review ad strength scores**
Go to Ads & Extensions > Ads. Look at the "Ad strength" column for your Responsive Search Ads. Anything below "Good" needs more headlines and descriptions. Poor ad strength usually means you have 3-5 headlines when you should have 15, or your headlines are too similar to each other.

**12. Audit ad extension coverage**
Check Ads & Extensions > Extensions. Verify you have sitelinks, callouts, and structured snippets running on all campaigns. Missing extensions = lower ad rank = higher costs. Good coverage means 4+ sitelinks, 4+ callouts, and relevant structured snippets for each campaign theme.

**13. Check for disapproved ads**
In the Ads section, filter Status to "Disapproved" or "Under review." Disapproved ads mean you're running with reduced coverage, hurting performance. Common issues: trademark violations, misleading claims, destination mismatch between ad and landing page. Fix immediately.

## Bidding & Budget Performance

**14. Review Smart Bidding performance**
For campaigns using Target CPA or Target ROAS, check if Google is hitting your targets. Go to Campaigns > Bid strategies (if using portfolio strategies) or check individual campaign performance. If actual CPA is 50%+ higher than target consistently, either your target is too aggressive or the campaign needs more conversion data.

**15. Identify impression share losses**
Add columns for "Search impression share," "IS lost due to budget," and "IS lost due to rank." Campaigns losing 20%+ impression share due to budget need budget increases. Campaigns losing impression share due to rank need bid increases or ad quality improvements.

**16. Monitor automated bid adjustments**
Check Tools & Settings > Bid adjustments. If you're using automated adjustments for device, location, or demographics, verify they make sense. I've seen automated mobile bid adjustments set to -90% because the algorithm misread poor mobile landing page performance as low mobile intent.

## Performance Max & AI Campaigns

**17. Audit Performance Max asset groups**
For Performance Max campaigns, review asset group performance individually. Look for asset groups with high spend but low conversions. Check if you've provided audience signals — campaigns without signals often waste spend on irrelevant placements. Add negative keywords at the campaign level to prevent showing for obviously wrong searches.

**18. Review automated assets**
Check if Google is automatically creating headlines or sitelinks for your ads. Go to Ads & Extensions > Automated extensions. Sometimes these auto-generated assets are terrible and hurt performance. Disable automatic creation and provide your own assets.

## Account-Level Health

**19. Check for policy violations**
Go to Tools & Settings > Account settings > Account status. Any policy violations, even warnings, can throttle your account's delivery. Common issues: misleading landing pages, prohibited content, billing problems. Resolve immediately.

**20. Review change history for unauthorized edits**
Tools & Settings > Change history. Look for changes you didn't make — sometimes other users with account access make "helpful" adjustments that break things. Filter by last 30 days and verify all major changes align with your strategy.

## Landing Page & User Experience

**21. Spot-check landing page speed**
Open 3-5 of your highest-traffic landing pages and test load speed. Anything over 3 seconds hurts Quality Score and conversion rates. Use Google PageSpeed Insights for specific recommendations.

**22. Verify tracking codes are live**
Check that your Google Ads conversion tracking code and Google Analytics code are firing on conversion pages. Use Google Tag Assistant Chrome extension for a quick check. Missing codes = missing conversion data = bad optimization decisions.

## Scoring Your Account Health

**Count up your issues:**
- **1-3 problems:** Minor tune-up needed. You're probably running efficiently but leaving some money on the table.
- **4-7 problems:** You're likely wasting 20-30% of your spend. These fixes should improve performance noticeably.
- **8+ problems:** Stop running ads until you fix this. You're bleeding money on preventable issues.

Most accounts I audit score 6-8 issues on their first check. Don't panic. The goal isn't perfection — it's catching problems before they compound.

## What This Checklist Doesn't Cover

This monthly review catches the obvious stuff — the leaks you can spot in 60 minutes. But the stuff that really kills ROI lives deeper. Attribution gaps where your best campaigns look terrible because the tracking is 14 days behind. Audience decay where your remarketing lists haven't been updated in eight months. Conversion value optimization where you're optimizing for lead quantity when you should optimize for lead quality.

That's what a professional audit covers. The invisible problems you can't see in a self-review because you need external tools, cross-platform analysis, and frankly, experience seeing the same patterns across hundreds of accounts.

I run these deep audits for $297 and usually find 15-20 additional issues that this checklist misses. If you scored 4+ problems on this monthly check, you probably need the full analysis. [Book here](mailto:luc@electroraven.com) and I'll show you exactly where your budget is going.

**Want the PDF version of this checklist?** Email me at luc@electroraven.com and I'll send you the downloadable version you can save and reuse every month.

The accounts that make Google Ads work aren't the ones with perfect campaigns. They're the ones that catch problems early and fix them fast. Start checking these 22 items monthly and you'll be surprised how much better your numbers look in 90 days.
