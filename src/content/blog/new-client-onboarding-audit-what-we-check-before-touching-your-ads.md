---
title: "New Client Onboarding Audit: What We Check Before Touching Your Ads"
description: "**I've audited 400+ ad accounts over the past eight years and I'd estimate 85% of them have at least 4 of these problems. Most business owners don't even..."
pubDate: 2026-04-16
topic: "Service Model"
seo_keywords: "client, onboarding, check, ads, touching, audit, before, new"
draft: false
---

# New Client Onboarding Audit: What We Check Before Touching Your Ads

**I've audited 400+ ad accounts over the past eight years and I'd estimate 85% of them have at least 4 of these problems. Most business owners don't even know they're bleeding 30-40% of their budget on fixable mistakes.**

The worst part? These aren't complex technical issues. They're basic setup errors that previous agencies either missed or ignored because fixing them doesn't generate billable hours like launching new campaigns does.

This is the exact checklist I run on every new client before I touch a single bid or write a single ad. It's the difference between optimizing a broken machine and building something that actually works.

**Who this is for:** Business owners currently running Google Ads or Meta Ads who suspect something's wrong but can't pinpoint what. If your cost per lead keeps climbing, your attribution numbers don't match your CRM, or you're getting clicks but not customers, keep reading.

## Conversion Tracking & Attribution

**1. Verify conversion actions are counting actual business events**
Open Google Ads > Tools & Settings > Conversions. Check what's being counted as a conversion. I regularly find accounts counting page views, PDF downloads, or "time on site" as leads. If your conversion action says "Page view" or "Session duration," you're not tracking business outcomes. Good tracking counts form submissions, phone calls, purchases — events that matter to your bottom line. Bad tracking inflates your numbers and kills your optimization.

**2. Check for duplicate conversion counting**
Look for multiple conversion actions tracking the same event. Common culprit: importing GA4 goals AND using Google Ads conversion tracking on the same form. Your attribution will be wrong and Google's algorithms will optimize for phantom conversions. Run a conversion report and cross-reference with your CRM data for the same period. If Google shows 40 conversions but your CRM only has 25 new leads, you've got duplicates.

**3. Audit conversion values and attribution windows**
Default attribution is 30-day click, 1-day view. That might work for e-commerce but kills B2B campaigns where sales cycles run 60-90 days. Check if your conversion values reflect actual revenue or profit — not just arbitrary placeholder numbers. I've seen accounts where every lead is valued at $1, making it impossible to run value-based bidding strategies.

**4. Verify Meta Conversions API is properly configured**
If you're running Meta ads, check Events Manager for your Conversions API setup. iOS 14.5+ killed pixel-only tracking. Without CAPI, you're flying blind on mobile conversions. Look for the green checkmark next to your domain in Events Manager. If it's red or yellow, your attribution is broken and you're under-reporting conversions by 20-40%.

**5. Test server-side tracking implementation**
Fire a test conversion and verify it appears in both your ad platform and your analytics within 24 hours. Use Google Tag Manager Preview mode to confirm tags are firing. Check that the data layer is passing correct values — user ID, transaction ID, revenue amount. Broken server-side tracking is why Performance Max campaigns optimize for the wrong audience signals.

## Account Structure & Campaign Setup

**6. Review campaign naming conventions and organization**
Inconsistent naming kills your ability to analyze performance across time periods. Check if campaigns clearly indicate traffic source, campaign type, and business objective. "Campaign 1" and "New Campaign - Copy" tell you nothing six months later. Good structure: "GGL_Search_Legal_Personal_Injury_Exact" tells you exactly what you're looking at.

**7. Audit audience signals in Performance Max campaigns**
PMax without audience signals is like driving blindfolded. Check Asset Groups for customer list uploads, website visitors, and similar audiences. Empty audience signals mean Google optimizes for whoever clicks, not who converts. Upload your CRM data as a customer list — even 1,000 emails gives the algorithm direction.

**8. Check for proper negative keyword coverage**
Review shared negative keyword lists and campaign-level negatives. I consistently find accounts showing for "jobs," "free," "DIY," and competitor variations. For B2B campaigns, exclude "resume," "salary," "career" terms. For local services, exclude "supply," "materials," "wholesale." Missing negatives waste 15-25% of search campaign budgets.

**9. Verify location targeting matches service areas**
Check both included and excluded locations. Accounts targeting "United States" when they only serve three states. Or worse — excluding their actual service area by mistake. For local businesses, audit radius targeting against actual travel zones. A 50-mile radius around Denver includes mountain towns you probably don't serve.

**10. Review ad scheduling against business hours**
Running ads when no one answers the phone kills conversion rates. Check if ad scheduling aligns with sales team availability, not just business hours. B2B campaigns performing better during business hours but running 24/7. Home services getting calls at 2 AM because someone forgot to pause overnight hours.

## Bidding & Budget Configuration

**11. Assess bidding strategy alignment with campaign maturity**
New campaigns using Target ROAS without conversion history. Manual CPC on campaigns with 500+ monthly conversions that should be on Smart Bidding. Check conversion volume against bidding strategy requirements. Target CPA needs 30+ conversions in 30 days to work properly. Switch to Maximize Conversions until you hit that threshold.

**12. Check budget allocation across campaigns**
High-performing campaigns limited by budget while low performers get full allocation. Review impression share lost to budget — anything over 20% means you need more budget or better targeting. Compare daily budget to actual daily spend. If you're consistently under budget, your targeting is too narrow or your bids are too low.

**13. Audit shared budgets and campaign priorities**
Shared budgets let Google decide where to spend your money. Sometimes that's smart. Usually it's not. Check if your brand campaign is competing with generic terms for the same budget. Verify Shopping campaign priorities align with margin strategy — high-margin products should get priority over volume plays.

## Creative & Landing Page Analysis

**14. Review responsive search ad asset combinations**
Check for pinned headlines that limit Google's testing ability. Verify you have 15 headlines and 4 descriptions — incomplete assets hurt performance. Look for duplicate messaging across assets. Use the combinations report to identify winning patterns and pause low-performing asset combinations.

**15. Test landing page load speed and mobile experience**
Run PageSpeed Insights on your primary landing pages. Anything under 70 mobile score costs you conversions. Check mobile responsiveness — form fields that don't work on phone, buttons too small to tap, text too small to read. Mobile accounts for 60%+ of traffic but most landing pages are built for desktop.

**16. Verify landing page message match**
Ad copy promising "free consultation" landing on a page about "premium services." Discount ads pointing to full-price pages. Message mismatch kills Quality Score and conversion rates. The headline on your landing page should echo your ad copy — not contradict it.

## Technical Infrastructure

**17. Check Google Analytics 4 integration and configuration**
Verify GA4 is properly linked to your ad accounts and importing conversions correctly. Check that Enhanced Conversions is enabled if you have first-party data. Missing GA4 integration means Google's algorithms optimize without website behavior data — like trying to drive with your eyes closed.

**18. Audit Google Tag Manager container health**
Open GTM and check for broken tags, missing triggers, or version conflicts. Use Preview mode to verify tags fire on target pages. I regularly find containers with 47 versions and tags that haven't fired in months but are still slowing down page load.

**19. Review automated rules and scripts**
Check for outdated automated rules pausing campaigns or adjusting bids based on old performance thresholds. Scripts that made sense in 2022 might be fighting against current algorithm improvements. Pause any automation you can't explain in one sentence.

**20. Verify account access and user permissions**
Check who has admin access to your ad accounts. Previous agency employees with full access. Contractors with more permissions than your internal team. Clean up user access — only current team members should have edit permissions. Everyone else gets read-only.

## Scoring Your Account Health

**1-4 issues found:** Minor tune-up needed. You're probably losing 10-15% efficiency but nothing catastrophic.

**5-8 issues found:** Moderate problems. You're likely wasting 25-35% of your ad spend on fixable issues.

**9-12 issues found:** Major structural problems. Stop increasing budget until you fix the foundation.

**13+ issues found:** Your ad account is hemorrhaging money. Pause everything except your highest-performing branded campaigns and rebuild from scratch.

This checklist catches the obvious stuff — the errors that show up in any systematic account review. But the stuff that really kills your ROI is invisible in a self-audit. Attribution gaps where conversions happen but don't get tracked back to the source. Audience decay where your targeting gets stale but performance stays flat. Competitive pressure that shifts optimal bidding without triggering any alerts.

That's what a professional audit covers. Not just what's broken, but what's missing. What opportunities you can't see because you're too close to the day-to-day management.

If you found more than 5 issues on this checklist, your account needs more than a tune-up. It needs someone who's audited hundreds of accounts to spot the patterns you can't see yet.

**Want the PDF version of this checklist plus our advanced technical audit criteria?** [Download the complete audit framework here.] Because fixing the obvious problems is just the beginning.
