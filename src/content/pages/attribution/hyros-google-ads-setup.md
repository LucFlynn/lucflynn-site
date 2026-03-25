---
title: "Hyros + Google Ads Attribution Setup Guide (2026)"
slug: "hyros-google-ads-setup"
description: "Step-by-step Hyros setup for Google Ads attribution. Covers pixel installation, integration configuration, and verification."
category: "attribution"
date: "2026-03-24"
hub_page: "/attribution"
page_type: "spoke"
---

# How to Set Up Hyros for Google Ads

I see about 30% of Hyros setups broken on the Google Ads side — usually because the URL parameters aren't passing through correctly or the integration is only capturing first-touch data. The most common issue? People install the Hyros script but forget to configure the Google Ads integration properly, so they're missing 40-60% of their attribution data.

Hyros is solid for long-funnel attribution, but the setup has some quirks that'll bite you if you don't know what you're doing.

## What You'll Have Working By The End

- Hyros tracking script installed and firing on all pages
- Google Ads integration configured to pass campaign data to Hyros
- URL parameter passthrough working for UTM and gclid parameters
- Call tracking integrated with Google Ads offline conversion import
- Attribution data flowing into Hyros with proper campaign mapping
- Conversion verification showing 85-95% match rate between Hyros and Google Ads

## Prerequisites

- [ ] Admin access to your Hyros account
- [ ] Google Ads account access with conversion tracking permissions
- [ ] Website access to install tracking scripts (or developer who can do it)
- [ ] Google Analytics connected to the same Google Ads account (recommended)
- [ ] Phone number if you want call tracking attribution

## Step 1: Install the Hyros Universal Script

Log into Hyros and grab your universal tracking script from Settings > Tracking Code. It'll look like this:

```javascript
<script>
!function(h,y,r,o,s){h.HyrosAnalyticsObject=s;h[s]=h[s]||function(){
(h[s].q=h[s].q||[]).push(arguments)},h[s].l=1*new Date();
r=y.createElement('script'),o=y.getElementsByTagName('script')[0];
r.async=1;r.src='https://api.hyros.com/pixel/'+YOUR_PIXEL_ID+'/pixel.js';
o.parentNode.insertBefore(r,o)}(window,document,0,0,'hyros');

hyros('init', 'YOUR_PIXEL_ID');
hyros('track', 'PageView');
</script>
```

Install this in the `<head>` of every page. If you're using GTM, create a Custom HTML tag that fires on All Pages. 

**Critical:** The script needs to fire before any conversion events, so put it high in the head, not at the bottom of the page.

## Step 2: Configure Google Ads Integration in Hyros

In Hyros, go to Integrations > Google Ads and click "Add Integration."

You'll need to:

1. Connect your Google account (this authorizes Hyros to access Google Ads data)
2. Select your Google Ads account from the dropdown
3. Enable "Import Conversion Data" — this lets Hyros see your Google Ads conversions
4. Enable "Export Attribution Data" — this sends Hyros attribution back to Google Ads

The tricky part: Hyros will create new conversion actions in your Google Ads account. Don't panic when you see these show up. They're labeled with `[HYROS]` prefix.

## Step 3: Set Up URL Parameter Passthrough

This is where most setups break. Hyros needs to capture UTM parameters and gclid from your URLs, but it won't work if your site redirects or strips parameters.

### Configure Parameter Mapping

In Hyros Settings > Attribution > URL Parameters, add these mappings:

```
utm_source → Source
utm_medium → Medium  
utm_campaign → Campaign
utm_content → Ad Content
utm_term → Keyword
gclid → Google Click ID
```

### Test Parameter Passthrough

Visit your site with this test URL:
```
yoursite.com?utm_source=google&utm_medium=cpc&utm_campaign=test&gclid=test123
```

Check in Hyros Live View (under Reports) — you should see the session with all parameters captured. If not, your site is stripping parameters and you need to fix that first.

### Common Redirect Issues

If you're using:
- **Shopify**: Add UTM parameters to your "Additional Google Analytics JavaScript" section to preserve them through checkout
- **WordPress**: Install a plugin like "UTM Parameter Tracker" or add parameter preservation code to functions.php
- **Custom redirects**: Make sure 301/302 redirects append query parameters to the destination URL

## Step 4: Set Up Conversion Tracking

### Web Conversions

For each conversion you want to track, add the Hyros conversion code to your thank you page:

```javascript
hyros('track', 'Purchase', {
  transaction_id: 'ORDER_123', 
  value: 99.95,
  currency: 'USD'
});
```

Replace 'Purchase' with your conversion name. Hyros supports these standard events:
- Purchase
- Lead  
- Subscribe
- ViewContent
- AddToCart

### Call Tracking Setup

If you're using Hyros call tracking:

1. In Hyros, go to Call Tracking > Phone Numbers
2. Click "Add Tracking Number" 
3. Forward calls to your main business line
4. Add the dynamic number insertion script to your site:

```javascript
hyros('track', 'CallTracking', {
  display_number: 'YOUR_TRACKING_NUMBER'
});
```

The script will swap your phone number for the tracking number and pass attribution data when calls come in.

## Step 5: Configure Google Ads Offline Conversions

This step lets Hyros send phone conversions and delayed conversions back to Google Ads.

In Google Ads:
1. Go to Tools > Conversions > Create Conversion Action
2. Choose "Import" as the source
3. Select "Track conversions from clicks" 
4. Choose "Use Google Click IDs"
5. Name it "Hyros Phone Conversions" or similar

Copy the conversion action ID (it's in the URL after `/conversions/` when you view the conversion).

In Hyros:
1. Go to Integrations > Google Ads > Offline Conversions
2. Paste the conversion action ID
3. Map your Hyros conversion events to Google Ads conversion actions
4. Enable "Send Phone Conversions" and "Send Delayed Conversions"

## Testing & Verification

### Check Hyros Data Collection

1. Go to Hyros Reports > Live View
2. Browse your site with UTM parameters in the URL
3. Trigger a test conversion
4. Verify the session shows up with correct attribution data

### Verify Google Ads Integration

1. In Google Ads, check Tools > Conversions
2. Look for conversions with `[HYROS]` prefix — these should start showing data within 24 hours
3. Check the Google Ads integration status in Hyros (should show "Connected" with a green dot)

### Cross-Check Attribution

Compare conversion counts between:
- **Hyros dashboard** (Reports > Attribution)
- **Google Ads** (Campaigns tab, Conversions column)  
- **Google Analytics** (if connected)

**Acceptable variance:** 5-15% difference is normal. Hyros typically reports 10-20% more conversions than Google Ads because it captures view-through conversions and has longer attribution windows.

**Red flags:**
- Hyros shows 50%+ more conversions (script probably firing multiple times)
- Zero conversions in Hyros but Google Ads shows conversions (integration broken)
- Hyros shows conversions but zero attribution to Google Ads (parameter passthrough broken)

## Troubleshooting

**Problem:** Hyros shows sessions but no Google Ads attribution
→ Check URL parameter passthrough. Visit your site with `?utm_source=google&gclid=test123` and verify parameters appear in Hyros Live View. If not, your site is stripping parameters.

**Problem:** Google Ads integration shows "Disconnected" status
→ Re-authorize the Google connection in Hyros Integrations. Google tokens expire every 7 days and need refresh. Also check that your Google account has admin access to the Google Ads account.

**Problem:** Call tracking numbers not showing on the site
→ Verify the dynamic insertion script is installed correctly. Check browser console for JavaScript errors. The script needs to load after the Hyros pixel but before page content renders.

**Problem:** Conversions showing in Hyros but not importing to Google Ads offline conversions
→ Check that gclid parameters are being captured. Without valid gclids, Google Ads can't match conversions to clicks. Also verify the conversion action ID is correct in Hyros settings.

**Problem:** Hyros attribution window seems too long/short
→ Adjust attribution settings in Hyros Settings > Attribution. Default is 30-day click, 1-day view. For Google Ads, I recommend 30-day click, 1-day view to match Google's default attribution.

**Problem:** Duplicate conversions between Hyros and native Google Ads tracking
→ You're probably running both Hyros conversion tracking AND Google Ads conversion tags. Pick one. I recommend turning off Google Ads native tracking and using Hyros exclusively for cleaner data.

## What To Do Next

Once your Hyros + Google Ads setup is running, consider these next steps:

- [Attribution tracking comparison](/attribution) — see how Hyros stacks up against other attribution tools
- [Done-for-you attribution setup](/services/attribution-setup) — if you want me to handle the technical setup
- [Free tracking audit](/contact) — I'll review your setup and find what's broken

*This guide is part of the [Attribution Tracking Hub](/attribution) — compare attribution tools, see setup guides for different platforms, and understand which solution fits your needs.*