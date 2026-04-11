---
title: "Conversion Tracking Audit: 20-Point Checklist"
description: "**I've audited hundreds of Google Ads accounts and tracking setups over eight years. I'd estimate 75% of them have at least 5 of these problems, and most..."
pubDate: 2026-04-11
topic: "Tracking"
seo_keywords: "conversion, checklist, tracking, 20-point, audit"
draft: false
---

**I've audited hundreds of Google Ads accounts and tracking setups over eight years. I'd estimate 75% of them have at least 5 of these problems, and most business owners have no idea they're hemorrhaging money through broken tracking.**

Last month I took over an account where the previous agency was reporting a 12% conversion rate and $45 cost per lead. The client was confused because the phone wasn't ringing. I found the problem in 90 seconds — they were counting page views of the thank-you page as conversions, but the form was also redirecting there on validation errors. Every failed form submission was being counted as a lead. The real conversion rate was under 3%. The real cost per lead was $180.

This checklist is for business owners running Google Ads, Meta ads, or any paid traffic who want to know if their tracking is actually working. If you're spending more than $2,000 a month on ads and you haven't audited your conversion tracking in the last six months, keep reading. If you inherited an ad account from an agency or previous employee, definitely keep reading.

## Pre-Flight Checks

### 1. **Verify What You're Actually Tracking**
Open Google Ads, go to Tools & Settings → Conversions. Look at your conversion actions. Are you tracking form submissions or thank-you page views? Form submissions are real conversions. Page views are not. If you see "pageview" in the conversion action name, that's a red flag.

**What good looks like:** Conversions tied to actual form submissions, phone calls, or completed purchases — events that require user action.

**Quick fix:** Set up conversion tracking on form submission events, not page loads. Use Google Tag Manager to track form submit events properly.

### 2. **Check for Duplicate Conversion Actions**
Still in Google Ads conversions, count how many conversion actions you have for the same outcome. I regularly find accounts with 3-4 different "contact form" conversions all tracking the same form.

**What bad looks like:** Multiple conversion actions for the same user behavior, or old conversion actions that haven't been paused.

**What good looks like:** One conversion action per unique business outcome. Clean, organized conversion action list.

**Quick fix:** Pause duplicate conversion actions. Keep the most recent, properly configured one.

### 3. **Test Your Tracking Right Now**
Go to your website. Fill out your contact form with fake info (use your own email). Submit it. Wait 10 minutes, then check Google Ads conversions to see if it recorded. Do the same for Meta if you're running Facebook ads.

**What bad looks like:** You submit the form and nothing shows up in your ad platforms.

**What good looks like:** Your test conversion appears in Google Ads within 10 minutes, attributed to the correct campaign if you clicked through an ad.

**Quick fix:** If this fails, your conversion tracking is completely broken and you need to fix it before spending another dollar on ads.

## Google Ads Conversion Tracking

### 4. **Enhanced Conversions Configuration**
In Google Ads, go to Tools & Settings → Conversions → click on your main conversion action. Look for "Enhanced conversions" in the settings. This should be turned on and configured to send first-party data like email addresses.

**What bad looks like:** Enhanced conversions turned off, or turned on but not actually sending any data.

**What good looks like:** Enhanced conversions enabled with email or phone data being captured and sent to Google.

**Quick fix:** Enable enhanced conversions through Google Tag Manager or global site tag. This can improve conversion attribution by 10-15%.

### 5. **Attribution Model Review**
In the same conversion action settings, check your attribution model. If you're using "Last click," you're missing the full picture of your customer journey.

**What good looks like:** Data-driven attribution if you have enough conversion volume (30+ conversions per month), or first-click for lead generation campaigns.

### 6. **Conversion Value Settings**
Check if you're tracking conversion values. For lead generation, assign a dollar value based on your average customer lifetime value. For e-commerce, make sure you're tracking actual purchase amounts.

**What bad looks like:** All conversions showing the same value, or no value at all.

**What good looks like:** Conversion values that reflect actual business impact, whether estimated lead value or real purchase amounts.

### 7. **Campaign-Level Conversion Goals**
Go to your campaigns, click on Settings, then Conversions. Check what conversions each campaign is optimizing for. I find campaigns accidentally optimizing for newsletter signups instead of sales leads.

**What bad looks like:** Campaigns optimizing for low-value conversions like newsletter signups or brochure downloads.

**Quick fix:** Set each campaign to optimize only for conversions that directly impact revenue.

## Google Analytics 4 Integration

### 8. **GA4 Conversion Events Setup**
In GA4, go to Configure → Conversions. Your main business outcomes should be marked as conversion events here. The event names should match what you're tracking in Google Ads.

**What bad looks like:** No conversion events marked in GA4, or conversions that don't match your Google Ads setup.

### 9. **Data Stream Configuration**
Go to Admin → Data Streams in GA4. Click on your web data stream. Enhanced measurement should be turned on, and you should see events like page_view, scroll, and file_download being tracked automatically.

**What good looks like:** Enhanced measurement enabled, custom events properly configured, and real-time data showing up in the DebugView.

### 10. **Cross-Domain Tracking**
If your website and checkout/contact form are on different domains (like yoursite.com and checkout.yoursite.com), check if cross-domain tracking is properly configured.

**What bad looks like:** GA4 treating each domain as a separate session, artificially inflating session counts and breaking attribution.

## Meta Ads Conversion Tracking

### 11. **Meta Pixel Health Check**
Go to Events Manager in Meta Business Manager. Look at your pixel. It should show "Active" status with recent events. Check the diagnostics tab for any error messages.

**What bad looks like:** Pixel showing errors like "Event sent from incorrect domain" or "Duplicate pixel installation."

### 12. **Conversion API Implementation**
In Events Manager, check if you have Conversions API configured alongside your pixel. This is critical in 2026 due to iOS privacy restrictions and ad blockers.

**What bad looks like:** Only Meta pixel implemented, no server-side tracking through Conversions API.

**What good looks like:** Both pixel and Conversions API sending data, with event match quality scores above 7.0.

### 13. **Custom Conversion Setup**
Go to Events Manager → Custom Conversions. Your main business outcomes should be set up as custom conversions here, not just standard events.

**What bad looks like:** Optimizing campaigns for "Lead" events instead of custom conversions that represent actual form submissions.

## Technical Infrastructure

### 14. **Google Tag Manager Container Audit**
Open Google Tag Manager. Go to your workspace and check how many tags you have. I regularly find 20+ duplicate tracking tags from different agencies and employees adding their own versions.

**What bad looks like:** Multiple Google Ads conversion tags, duplicate GA4 tags, or tags that haven't been fired in months.

**Quick fix:** Audit and remove duplicate tags. Use built-in tag templates when possible.

### 15. **Consent Management Implementation**
Check if you have a consent management platform (CMP) properly configured. In Europe, this is legally required. In the US, it affects data quality.

**What good looks like:** CMP integrated with Google Tag Manager, with tags only firing after proper consent is given.

### 16. **Server-Side Tagging Setup**
Advanced check: If you're running significant ad spend (>$10K/month), verify if you have server-side Google Tag Manager configured to bypass browser restrictions.

**What good looks like:** First-party data collection through your own domain, reducing data loss from ad blockers and privacy restrictions.

## Audience and Attribution

### 17. **Retargeting Audience Health**
In Google Ads, go to Tools & Settings → Audience Manager. Check your retargeting audiences. They should be actively collecting users and have reasonable sizes.

**What bad looks like:** Retargeting audiences with 0 users, or audiences that haven't been updated in weeks.

### 18. **Attribution Windows Alignment**
Check that your attribution windows are consistent across platforms. Google Ads default is 30-day click, 1-day view. Meta recently restricted attribution windows in 2026.

**What good looks like:** Attribution windows aligned with your actual sales cycle length, not platform defaults.

### 19. **UTM Parameter Consistency**
Check a few of your ads to see if UTM parameters are properly configured and consistent. Your naming convention should be standardized across all campaigns.

**What bad looks like:** Missing UTM parameters, inconsistent naming (sometimes "google-ads" and sometimes "googleads"), or generic campaign names.

## Data Quality Verification

### 20. **Revenue Attribution Verification**
The ultimate test: Can you trace a specific Google Ads click to an actual sale in your CRM or payment processor? If you can't connect ad clicks to revenue, you're optimizing in the dark.

**What good looks like:** Clear path from ad click to conversion to customer record to revenue, with click IDs tracked through your entire funnel.

**What bad looks like:** No way to verify which ad campaigns actually generate paying customers versus just leads that never close.

## Scoring Your Audit

**0-4 issues:** Your tracking is in decent shape, just needs minor tune-ups.

**5-9 issues:** You're probably wasting 20-30% of your ad spend on bad data. Fix these before scaling.

**10+ issues:** Stop running ads until you fix this. You're throwing money at campaigns optimized for fake conversions.

---

This checklist catches the obvious stuff — the tracking gaps you can see with basic platform access. But the stuff that really kills ROI is invisible in a self-audit. Attribution drift where your tracking slowly degrades over time. Audience decay where your retargeting pools fill with unqualified traffic. Server-side infrastructure that looks fine but is missing 40% of mobile conversions.

That's what a professional audit covers. I've built tracking infrastructure for 200+ ad accounts over eight years. If you found more than 5 issues in this checklist, your tracking problems go deeper than what you can fix with platform settings.

Want the 47-point professional audit checklist I use for client accounts? It's available as a PDF download along with the Google Tag Manager templates I use to fix the most common tracking issues. [Get the complete audit toolkit here](https://electroraven.com/audit).
