---
title: "Hyros + Meta Ads Attribution Setup Guide (2026)"
slug: "hyros-meta-ads-setup"
description: "Step-by-step Hyros setup for Meta Ads attribution. Covers pixel installation, integration configuration, and verification."
category: "attribution"
date: "2026-03-24"
hub_page: "/attribution"
page_type: "spoke"
---

# How to Set Up Hyros for Meta Ads

I see broken Hyros + Meta setups in about 35% of the accounts I audit. The most common issue? URL parameter passthrough isn't configured properly, so Hyros can't tie phone calls and delayed conversions back to specific Meta campaigns. The second most common? The integration pulls data but the attribution windows don't match, creating massive reporting discrepancies.

Here's exactly how to set this up so your long-funnel attribution actually works.

## What You'll Have Working By The End

- Hyros Universal Script tracking all Meta Ads traffic with proper campaign attribution
- Phone call tracking that connects calls to specific Meta campaigns and ad sets
- CAPI integration sending server-side conversion data back to Meta
- URL parameter passthrough preserving fbclid and UTM data through your entire funnel
- Attribution reporting that matches Meta's native data within 10-15%

## Prerequisites

- [ ] Hyros account with Universal Script access (not just the basic pixel)
- [ ] Meta Ads Manager admin access
- [ ] Meta Business Manager admin access for CAPI setup
- [ ] Google Tag Manager container (recommended) or direct website access
- [ ] Access to your phone system for call tracking integration

## Step 1: Install Hyros Universal Script

The Universal Script is different from Hyros' basic tracking pixel — it handles both web events and offline conversions in one script.

In GTM, create a new Custom HTML tag:

```html
<script>
!function(e,r,a,n,t,o,i){e.hyrax||(t=e.hyrax=function(){t.callMethod?t.callMethod.apply(t,arguments):t.queue.push(arguments)},t.push=t,t.loaded=!0,t.version="1.0",t.queue=[],o=r.createElement(a),o.async=!0,o.src=n,i=r.getElementsByTagName(a)[0],i.parentNode.insertBefore(o,i))}(window,document,"script","https://track.hyros.com/v1/hyrax.js");

hyrax('init', 'YOUR_SCRIPT_ID');
hyrax('track', 'PageView');
</script>
```

Replace `YOUR_SCRIPT_ID` with your actual Hyros script ID from your dashboard.

Set the trigger to "All Pages" and configure these built-in variables:
- Page URL
- Referrer 
- Click URL (for link tracking)

**Common mistake**: Don't use both the Universal Script AND the basic Hyros pixel. Pick one. The Universal Script handles everything the basic pixel does, plus call tracking and offline attribution.

## Step 2: Configure URL Parameter Passthrough

This is where most setups break. Hyros needs to capture and preserve specific URL parameters throughout your entire funnel.

### Required Parameters for Meta Ads:
- `fbclid` (Facebook Click ID)
- `utm_source`
- `utm_medium` 
- `utm_campaign`
- `utm_content`
- `utm_term`

In your Hyros dashboard, go to Settings → URL Parameters and ensure these are set to "Preserve":

```
fbclid=preserve_throughout_session
utm_source=preserve_throughout_session  
utm_medium=preserve_throughout_session
utm_campaign=preserve_throughout_session
utm_content=preserve_throughout_session
utm_term=preserve_throughout_session
```

**Critical**: If you use landing page builders like ClickFunnels or Leadpages, you need to manually pass these parameters through every redirect and form submission. Check that your "Thank You" page URLs include the original fbclid parameter.

## Step 3: Set Up Meta CAPI Integration

In Hyros, navigate to Integrations → Facebook → Conversions API.

You'll need:
- Your Meta Business Manager ID
- Facebook App ID (create one in Meta Business if you don't have it)
- Facebook App Secret
- Your Pixel ID from Meta Ads Manager

```javascript
// Test CAPI connection with this verification call
hyrax('track', 'Purchase', {
  value: 97.00,
  currency: 'USD',
  content_ids: ['test-product-123'],
  content_type: 'product'
});
```

The integration should show "Connected" status within 5 minutes. If it shows "Needs Attention," check your App Secret — that's wrong 70% of the time.

### CAPI Attribution Window Settings:
- View-through: 1 day (match Meta's default)
- Click-through: 7 days (match Meta's default)

**Which attribution model should you use?** Stick with Meta's default settings initially. You can adjust later, but mismatched attribution windows create impossible-to-reconcile reporting differences.

## Step 4: Configure Call Tracking Attribution

This is Hyros' main strength over other attribution tools. Set up dynamic number insertion on pages that get Meta traffic.

In Hyros, go to Call Tracking → Number Pools and create a pool with at least 20 numbers for Meta campaigns.

Add this script after your Universal Script:

```javascript
<script>
hyrax('track', 'CallTrackingInit', {
  pool_id: 'meta_ads_pool',
  fallback_number: '+1-555-xxx-xxxx',
  preserve_params: ['fbclid', 'utm_campaign', 'utm_content']
});
</script>
```

**Important**: The fallback number should be your main business line. If dynamic insertion fails (happens about 5% of the time), visitors still see a working number.

## Step 5: Set Up Conversion Events

Map your conversion events to Meta's standard event names for proper CAPI sync:

```javascript
// Purchase event
hyrax('track', 'Purchase', {
  value: revenue_amount,
  currency: 'USD',
  transaction_id: order_id,
  content_ids: [product_sku],
  fbclid: get_url_parameter('fbclid')
});

// Lead event  
hyrax('track', 'Lead', {
  content_name: form_name,
  fbclid: get_url_parameter('fbclid'),
  source: 'meta_ads'
});
```

Set these up in GTM using Custom HTML tags triggered on your conversion confirmation pages.

## Testing & Verification

### 1. Hyros Debug Mode
In your Hyros dashboard, enable Debug Mode. Visit your site with Meta campaign parameters:
`yoursite.com?utm_source=facebook&utm_campaign=test&fbclid=test123`

You should see:
- PageView event registered
- Campaign attribution showing "facebook/test"
- Parameters preserved on subsequent page loads

### 2. Meta Events Manager
Check Events Manager for your pixel. You should see:
- PageView events from both browser pixel and CAPI
- Custom conversions with matching event names
- CAPI events showing "Server" source

### 3. Attribution Cross-Check
Run a small test campaign ($50 spend) and compare:
- Meta Ads Manager: Purchases attributed to your campaign
- Hyros Dashboard: Sales attributed to same campaign
- Your actual sales records

**Acceptable variance**: 5-15% difference is normal. Hyros typically shows higher attribution than Meta due to longer attribution windows and call tracking.

**Red flags**:
- 0 conversions showing in Hyros but sales in Meta (broken parameter passthrough)
- Hyros showing 3x+ more conversions than Meta (attribution window mismatch)
- No call tracking attribution despite phone leads (DNI not working)

## Troubleshooting

**Problem**: Hyros shows "Unknown" traffic source for obvious Meta Ads traffic
**Solution**: Check that fbclid parameters aren't being stripped by redirects or form processors. Use a URL parameter testing tool to verify preservation through your entire funnel.

**Problem**: CAPI integration shows "Connected" but no server events in Events Manager
**Solution**: Your Facebook App Secret is likely incorrect, or your App doesn't have proper permissions. Regenerate the App Secret and reconnect.

**Problem**: Call tracking numbers not displaying on landing pages
**Solution**: JavaScript errors are preventing DNI script execution. Check browser console. Most common issue: Universal Script not loading before call tracking script.

**Problem**: Conversion values in Hyros don't match actual order values
**Solution**: Your conversion tracking script is firing multiple times or capturing the wrong value field. Check for duplicate pixels and verify the revenue variable name.

**Problem**: Hyros attribution shows sales from campaigns that weren't running
**Solution**: Attribution window is too long, or you have cross-campaign parameter contamination. Reduce attribution window to 3 days and check for URL parameter persistence issues.

**Problem**: Phone calls showing in Hyros but not attributing to specific campaigns
**Solution**: Dynamic number insertion isn't preserving campaign parameters. Verify that your DNI script includes the `preserve_params` configuration.

## What To Do Next

Now that your Hyros + Meta setup is tracking properly, consider these next steps:

- **[Attribution Tool Comparison](/attribution)** — See how Hyros stacks up against other attribution solutions
- **[Server-Side Tracking Setup](/attribution/server-side-tracking)** — Add first-party data collection to reduce iOS 14+ attribution loss  
- **[Multi-Platform Attribution](/attribution/multi-platform-setup)** — Connect Google Ads and other platforms to Hyros for unified reporting
- **[Free Tracking Audit](/contact)** — I'll review your setup and identify any gaps (usually find 2-3 issues even in "working" setups)

*This guide is part of the [Attribution Tools Guide](/attribution) — complete setups for tracking your marketing across platforms with proper attribution.*