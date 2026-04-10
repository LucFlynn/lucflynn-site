---
title: "The Complete Google Ads Audit Checklist (2026)"
description: "**I've audited over 200 Google Ads accounts and I'd estimate 85% of them are bleeding money on at least five fixable problems.** Most business owners..."
pubDate: 2026-04-10
topic: "Google Ads"
seo_keywords: "ads, complete, 2026, checklist, google, audit"
draft: false
---

# The Complete Google Ads Audit Checklist (2026)

**I've audited over 200 Google Ads accounts and I'd estimate 85% of them are bleeding money on at least five fixable problems.** Most business owners running ads have no idea they're optimizing campaigns based on broken data, missing obvious waste, or letting Google's automation work against their actual business goals.

This checklist is for business owners and marketers who want to know if their Google Ads account is actually working — or just burning budget while the dashboard shows green arrows. If you're spending more than $2,000 a month on ads and can't confidently explain where every dollar is going, keep reading.

## Foundation & Conversion Tracking (The Make-Or-Break Stuff)

### 1. **Conversion tracking isn't counting the same action twice**
Open Google Ads → Tools & Settings → Conversions. Look for duplicate actions like "Purchase" from GA4 and "Purchase" from Google Ads tag. If you see both tracking the same event, you're double-counting every sale.

**Bad:** Two conversion actions for the same purchase, inflating your conversion numbers by 50-100%.
**Good:** One primary conversion per actual business outcome.
**Fix:** Keep the more reliable tracking source, usually GA4 Enhanced Ecommerce. Set the other to "Secondary" for reporting only.

### 2. **Primary conversions actually matter to your business**
Check which conversions are marked "Primary" in your conversions list. Google's Smart Bidding optimizes toward these actions. If "Newsletter signup" is primary but "Purchase" is secondary, you're telling Google to find newsletter subscribers instead of buyers.

**Bad:** Phone number clicks, brochure downloads, or page views set as primary conversions.
**Good:** Purchases, qualified lead forms, booked appointments, demo requests — actions that correlate with revenue.
**Fix:** Set revenue-driving actions as Primary. Everything else goes to Secondary.

### 3. **GA4 is actually linked and working**
Google Ads → Tools & Settings → Linked Accounts → Google Analytics. Verify the connection is active. Then spot-check: does a recent conversion in GA4 show up in Google Ads within 24 hours?

**Bad:** No GA4 link, or conversions showing in GA4 but not importing to Google Ads.
**Good:** Real-time conversion data flowing both directions, with attribution models matching.
**Fix:** Relink the accounts. Verify GA4 Enhanced Ecommerce is configured correctly.

### 4. **Phone call tracking makes sense**
If you're a local business, check Tools & Settings → Conversions for call conversions. Are you counting 15-second calls as leads? Most hang-ups happen in the first 30 seconds.

**Bad:** Every call over 10 seconds counts as a conversion, including wrong numbers and hang-ups.
**Good:** Calls over 60 seconds, or better yet, only calls that reach a human.
**Fix:** Increase minimum call duration to 60+ seconds. Set up call recording if legally allowed in your state.

## Campaign Structure & Targeting

### 5. **Brand and non-brand campaigns are separated**
Search Campaigns → check if you have separate campaigns for branded terms (your company name) versus generic terms (your service/product). Brand campaigns should have exact match keywords and exclude non-brand campaigns.

**Bad:** Everything mixed together, or brand terms competing against generic terms in the same campaign.
**Good:** Branded campaign with 10-20% of total budget, non-brand campaigns with the rest.
**Fix:** Create separate brand campaign. Add negative keywords to exclude your brand from non-brand campaigns.

### 6. **Location targeting isn't bleeding budget**
Campaigns → Settings → Locations. Check if you're targeting "People in, or who show interest in" your locations. This wastes money on people researching your area who live somewhere else.

**Bad:** "Interest in" targeting enabled, serving ads to people researching your city from 500 miles away.
**Good:** "Presence" targeting only — people physically in your service area.
**Fix:** Change to "People in your targeted locations" unless you specifically serve tourists.

### 7. **Search Partners are turned off**
Campaign Settings → Networks. If "Include Google search partners" is checked, you're showing ads on random websites and apps where search intent is weaker.

**Bad:** Search Partners enabled, driving up costs with lower-quality traffic.
**Good:** Google Search only, unless Search Partners specifically convert better (rare).
**Fix:** Uncheck Search Partners. Monitor performance for two weeks, then decide if you want to test them again.

### 8. **Ad scheduling matches your business hours**
Campaign Settings → Ad Schedule. If you're a local business that doesn't answer phones after 6 PM, why are your ads running at 11 PM?

**Bad:** Ads running 24/7 when you can only handle leads during business hours.
**Good:** Ad schedule aligned with when you can actually serve customers.
**Fix:** Set ad schedule to run during business hours plus 1-2 hours buffer. Bid down 30-50% outside core hours.

## Keywords & Search Terms

### 9. **Search terms report reveals actual queries**
Campaigns → Keywords → Search Terms. Pull 30-90 days of data. Look for queries that triggered your ads but have nothing to do with your business.

**Bad:** Broad match keywords triggering on job searches, DIY tutorials, or competitor research.
**Good:** Most triggering queries are relevant to your actual service/product.
**Fix:** Add negative keywords for irrelevant themes: -jobs, -careers, -free, -DIY, -how to, -salary.

### 10. **Negative keyword lists are comprehensive**
Tools & Settings → Shared Library → Negative Keywords Lists. You should have lists for common irrelevant terms applied across campaigns.

**Bad:** No negative keyword lists, or basic lists with 5-10 obvious terms.
**Good:** 100+ negatives covering jobs, free seekers, DIY, competitors, and irrelevant product categories.
**Fix:** Build negative lists from search terms report. Apply shared negative lists to all relevant campaigns.

### 11. **Match types make sense for your goals**
Keywords tab → check the match type distribution. Exact match keywords typically convert best, but broad match can work for scaling if managed correctly.

**Bad:** Everything on broad match without negative keyword management, or everything on exact match limiting scale.
**Good:** Mix of exact match for proven winners, phrase match for expansion, broad match only on well-managed campaigns.
**Fix:** Start new campaigns with exact and phrase match. Add broad match only after building strong negative keyword lists.

## Ad Copy & Extensions

### 12. **Ad copy matches the keywords and landing page**
Review your ads versus the keywords they serve for and the landing pages they send to. The message should flow: keyword → ad → landing page headline.

**Bad:** Generic ads that don't mention the specific service someone searched for.
**Good:** Ad copy includes the main keyword and promises what the landing page delivers.
**Fix:** Write ads that speak directly to the search intent. Include the primary keyword in headlines when possible.

### 13. **All ad extensions are enabled and relevant**
Campaigns → Ads & Extensions → Extensions. You should be running sitelinks, callouts, structured snippets, and call extensions at minimum.

**Bad:** No extensions, or extensions that haven't been updated in years.
**Good:** Fresh, relevant extensions that give users more reasons to click and more real estate on the search results.
**Fix:** Add 4-6 sitelinks, 4+ callouts, structured snippets for your service categories, and call extensions with your business number.

### 14. **Responsive Search Ads have enough variety**
Check your Responsive Search Ads for "Ad Strength." Counterintuitively, "Good" ad strength often converts better than "Excellent" because you maintain more control over messaging.

**Bad:** Only 1-2 headlines and descriptions, or headlines that are too similar to each other.
**Good:** 8-10 unique headlines and 3-4 descriptions that can combine in multiple ways.
**Fix:** Add more headline variety. Include emotional appeals, feature callouts, and urgency in different headlines.

## Performance Max & Automation

### 15. **Performance Max campaigns have proper asset groups**
If running Performance Max, check Asset Groups for coverage. Do you have assets for all your main products/services, or is everything lumped together?

**Bad:** One asset group trying to cover multiple unrelated products/services.
**Good:** Separate asset groups for distinct offerings, with specific audiences and assets for each.
**Fix:** Split broad Performance Max campaigns into focused asset groups. Add audience signals for each group.

### 16. **Smart Bidding has enough conversion data**
Campaign Settings → Bidding. If you're using Target CPA or Target ROAS but getting fewer than 15 conversions per month, Smart Bidding is flying blind.

**Bad:** Smart Bidding strategies on campaigns with 3-5 conversions per month.
**Good:** Manual CPC or Enhanced CPC until you hit 15+ conversions monthly, then graduate to Smart Bidding.
**Fix:** Switch low-conversion campaigns back to manual bidding. Use Target CPA/ROAS only on campaigns with sufficient data.

## Budget & Account Management

### 17. **Budget allocation matches performance**
Compare budget distribution to actual performance. Are high-performing campaigns limited by budget while poor performers get full spend?

**Bad:** Best-converting campaign gets 20% of budget while worst-performing campaign has unlimited budget.
**Good:** Budget flows to campaigns and keywords that actually drive business results.
**Fix:** Reallocate budget toward profitable campaigns. Pause or severely limit budget on poor performers.

### 18. **Shared budgets aren't causing issues**
Campaign Settings → Budget. Shared budgets sound efficient but often cause unpredictable spending patterns where one campaign dominates.

**Bad:** Multiple campaigns sharing one budget, with unclear spending distribution.
**Good:** Individual campaign budgets so you control exactly what gets how much spend.
**Fix:** Split shared budgets into individual campaign budgets. Set each based on that campaign's performance.

## Tracking & Attribution

### 19. **Attribution models match your sales cycle**
Google Ads → Tools & Settings → Conversions → Attribution Models. If you have a long sales cycle, last-click attribution might miss most of your touchpoints.

**Bad:** Last-click attribution on 60+ day sales cycles, missing most of the customer journey.
**Good:** Data-driven attribution (if you have enough volume) or first-click for longer cycles.
**Fix:** Test different attribution models. Compare results to your actual sales data to see what matches reality.

### 20. **Landing pages load fast and work on mobile**
Test your landing pages on mobile. Use Google PageSpeed Insights to check load times. Anything over 3 seconds kills mobile conversions.

**Bad:** Landing pages that take 5+ seconds to load, or forms that don't work properly on phones.
**Good:** Sub-3-second load times, mobile-optimized forms, clear call-to-action above the fold.
**Fix:** Optimize images, improve hosting, simplify mobile forms. Test the conversion process on your phone.

## Your Audit Score

Count how many issues you found:

**1-3 issues:** Minor tune-up needed. You're probably doing better than most.
**4-7 issues:** You're likely wasting 20-30% of your ad spend on fixable problems.
**8-12 issues:** Stop running ads until you fix the foundation. You're burning money.
**13+ issues:** Your account needs a complete rebuild. Start over with proper setup.

## What This Audit Doesn't Catch

This checklist covers the obvious stuff — the problems you can spot in a few hours of clicking around. The expensive problems are usually invisible in a self-audit. Attribution gaps where your best campaigns look terrible because the tracking is broken. Audience decay where your retargeting lists haven't been refreshed in months. Bid strategy conflicts where different campaigns compete against each other and drive up your own costs.

The difference between an account that works and one that burns budget usually isn't the obvious checklist items. It's the systematic issues that compound over months — the stuff that requires deep account analysis and custom tracking infrastructure to actually fix.

If you want the full audit that catches the expensive problems, not just the obvious ones, [get a professional account audit here](https://www.electroraven.com/audit). I'll show you exactly where your budget is going and what's actually driving results versus what just looks good in the dashboard.
