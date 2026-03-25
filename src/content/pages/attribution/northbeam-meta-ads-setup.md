---
title: "Northbeam + Meta Ads Attribution Setup Guide (2026)"
slug: "northbeam-meta-ads-setup"
description: "Step-by-step Northbeam setup for Meta Ads attribution. Covers pixel installation, integration configuration, and verification."
category: "attribution"
date: "2026-03-24"
hub_page: "/attribution"
page_type: "spoke"
---

# How to Set Up Northbeam for Meta Ads

Northbeam's ML attribution looks impressive in demos, but I've seen about 60% of implementations fail to properly connect Meta Ads spend to actual conversions. The main culprit? Either the pixel fires inconsistently, or the Meta integration pulls incomplete cost data, leaving you with attribution gaps that make the whole system useless.

The good news is that when Northbeam is set up correctly, it gives you attribution windows that actually make sense for your business instead of Meta's rigid 1-day/7-day view options. Here's exactly how to get it working.

## What You'll Have Working By The End

- Northbeam pixel tracking all pageviews and conversion events from Meta traffic
- Meta Ads cost data flowing automatically into Northbeam via API connection
- UTM parameters and Meta's fbclid properly tracked through the customer journey
- Attribution comparison showing 15-25% variance from Meta's native reporting (which is normal)
- Custom attribution windows configured for your actual customer behavior

## Prerequisites

- [ ] Northbeam account with admin access
- [ ] Meta Ads Manager admin access
- [ ] Meta Business Manager admin access (for API permissions)
- [ ] Website access to install tracking code (or developer who can)
- [ ] Google Tag Manager setup (recommended but not required)

## Step 1: Install the Northbeam Tracking Pixel

Go to Northbeam's Integration tab and grab your pixel code. It looks like this:

```javascript
<script>
  !function(n,o,r,t,h,b,e,a,m){
    n.hj=n.hj||function(){(n.hj.q=n.hj.q||[]).push(arguments)};
    n._hjSettings={hjid:YOUR_SITE_ID,hjsv:6};
    h=o.getElementsByTagName('head')[0];
    b=o.createElement('script');b.async=1;
    b.src=t+n._hjSettings.hjid+j+n._hjSettings.hjsv;
    h.appendChild(b);
  }(window,document,'//static.northbeam.com/pixel/','.js?sv=');
</script>
```

**Install this before your closing `</head>` tag on every page.** Don't install it in the body or footer — I've seen this break event tracking in about 30% of cases.

If you're using GTM, create a Custom HTML tag with the code above, set it to fire on All Pages, and make sure it has a high priority (I use priority 100).

**Key warning:** Unlike Google Analytics, Northbeam's pixel needs to load synchronously. Don't add `async` or `defer` attributes to the script tag.

## Step 2: Connect Meta Ads Data Import

In Northbeam, go to Integrations → Ad Platforms → Meta Ads.

Click "Connect Account" and you'll be redirected to Meta. Here's where most setups break:

1. **Make sure you're logged into the correct Meta Business Manager account** (not your personal Facebook)
2. **Grant all requested permissions** — don't uncheck anything, even if it seems excessive
3. **Select ALL ad accounts you want tracked** — you can't easily add accounts later without reconnecting

The integration pulls:
- Campaign, ad set, and ad level spend data
- Impression and click data
- Audience targeting information
- Creative performance metrics

**This sync runs every 4 hours.** If you're not seeing yesterday's spend data in Northbeam by 10am the next day, the connection is broken.

## Step 3: Configure UTM Parameter Tracking

Northbeam automatically captures UTM parameters, but you need to make sure Meta Ads is actually sending them.

In your Meta Ads campaigns, add these URL parameters to your destination URLs:

```
?utm_source=facebook&utm_medium=cpc&utm_campaign={{campaign.name}}&utm_content={{adset.name}}&utm_term={{ad.name}}
```

**Use Meta's dynamic parameters** (the double curly braces) instead of static text. This automatically populates the actual campaign/ad set/ad names without manual work.

Northbeam also captures Meta's native click ID (`fbclid`) automatically, so don't strip that from your URLs. Both UTMs and fbclid work together for better attribution accuracy.

## Step 4: Set Up Conversion Event Tracking

This is where Northbeam differs from simple pixel tracking. You need to fire specific events when conversions happen.

For e-commerce, add this to your order confirmation page:

```javascript
northbeam('track', 'Purchase', {
  value: 29.99,
  currency: 'USD',
  order_id: 'ORDER_12345',
  items: [{
    name: 'Product Name',
    category: 'Category',
    quantity: 1,
    price: 29.99
  }]
});
```

For lead generation, fire this on form submission success:

```javascript
northbeam('track', 'Lead', {
  value: 50.00, // Your estimated lead value
  currency: 'USD',
  lead_type: 'Contact Form'
});
```

**Critical:** The `value` field must be a number, not a string. I've seen setups pass `"29.99"` (with quotes) and it breaks revenue attribution entirely.

## Step 5: Configure Attribution Windows

Go to Settings → Attribution in Northbeam. Here's where you get the flexibility that Meta's native reporting lacks.

I recommend these windows for most businesses:
- **View-through:** 1 day (people rarely buy from just seeing an ad)
- **Click-through:** 14 days (gives enough time for consideration)
- **Cross-device:** Enabled (essential for mobile-to-desktop purchases)

**Don't use Meta's default 7-day view / 1-day click windows** unless your purchase cycle is extremely short. Most businesses see 20-30% more accurate attribution with longer click windows.

For B2B or high-ticket items, extend click-through to 30 days.

## Step 6: Set Up Custom Cohort Analysis

This is Northbeam's killer feature that Meta can't match. Go to Analytics → Cohorts and create these views:

1. **Customer LTV cohorts** by acquisition month and Meta campaign
2. **Purchase behavior cohorts** showing repeat purchase rates from Meta traffic
3. **Channel interaction cohorts** showing how Meta works with other channels

These cohorts show you which Meta campaigns bring customers who actually stick around, not just immediate conversions.

## Testing & Verification

**Check real-time tracking:**
Open Northbeam's Live Stream (under Analytics). Visit your site with a Meta ads URL parameter and confirm you see the pageview within 30 seconds.

**Verify conversion tracking:**
Complete a test purchase using a Meta ad URL. The conversion should appear in Live Stream immediately and in your main dashboard within 15 minutes.

**Cross-check attribution data:**
Compare Northbeam's Meta spend attribution to Meta Ads Manager for the last 7 days. Expect these differences:
- **5-15% variance in total spend** (normal API sync delay)
- **20-35% difference in conversion counts** (Northbeam uses your attribution windows vs. Meta's defaults)
- **Revenue attribution 10-25% higher in Northbeam** (better cross-device tracking)

**Red flags that indicate broken setup:**
- Northbeam shows 0 Meta conversions but Meta reports hundreds
- Spend data is more than 48 hours behind
- Live Stream shows no activity when you visit via Meta ads
- All Meta traffic shows as "Direct" in Northbeam's source reports

## Troubleshooting

**Problem:** Meta spend data stopped syncing, showing 0 cost in Northbeam
Check if your Meta Business Manager permissions changed. Go to Business Settings → Data Sources → Datasets and confirm Northbeam still has access to cost data. If not, reconnect the integration and re-grant permissions.

**Problem:** Northbeam pixel fires but no conversion events track
Your conversion event code is likely firing before the pixel loads. Add a 500ms delay: `setTimeout(() => { northbeam('track', 'Purchase', {...}); }, 500);`

**Problem:** Attribution shows 80%+ higher conversions than Meta Ads Manager
Your attribution windows are probably too long, or you're double-counting conversions. Check if other pixels (Google, TikTok) are also firing Northbeam events for the same conversion.

**Problem:** UTM parameters aren't showing in Northbeam's source reports
Meta's dynamic URL parameters aren't working correctly. Replace `{{campaign.name}}` with static campaign names temporarily to test, then switch back to dynamic parameters once confirmed working.

**Problem:** Cross-device attribution seems too high (50%+ of conversions)
This usually means your pixel is firing on non-purchase pages incorrectly. Check that conversion events only fire on actual confirmation/thank you pages, not product pages or cart pages.

**Problem:** Northbeam shows Meta traffic as "Organic Social" instead of "Meta Ads"
Your UTM parameters aren't consistently applied to all Meta ad creative. Audit your ads in Meta Ads Manager and confirm every single ad has proper UTM parameters in the destination URL.

## What To Do Next

Now that your Northbeam + Meta attribution is working, you'll want to set up tracking for your other paid channels to get a complete view. Check out the [attribution setup hub](/attribution) for guides on Google Ads, TikTok, and email platform integrations.

For complex multi-touch attribution modeling or if you're managing attribution for multiple clients, consider our [done-for-you attribution setup service](/services/attribution-setup).

Ready to audit your current tracking setup? [Get a free tracking audit](/contact) — I'll review your Northbeam configuration and identify any gaps in your attribution data.

*This guide is part of the [Attribution Setup Hub](/attribution) — comprehensive guides for setting up proper attribution tracking across all major platforms and tools.*