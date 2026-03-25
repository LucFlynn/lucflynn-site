---
title: "Northbeam + Multi-Channel Attribution Setup Guide (2026)"
slug: "northbeam-multi-channel-setup"
description: "Step-by-step Northbeam setup for Multi-Channel attribution. Covers pixel installation, integration configuration, and verification."
category: "attribution"
date: "2026-03-24"
hub_page: "/attribution"
page_type: "spoke"
---

# How to Set Up Northbeam for Multi-Channel

I see Northbeam setups attempted in about 30% of mid-size ecommerce accounts I audit, but maybe half of those are actually configured correctly for multi-channel attribution. Most teams install the pixel and think they're done — then wonder why their attribution windows are wonky or why Google Ads conversions don't match what Northbeam reports. The ML models only work when you feed them clean data from day one.

## What You'll Have Working By The End

- Northbeam pixel properly installed with purchase and engagement tracking
- Connected data streams from Google Ads, Facebook Ads, TikTok, and email platforms
- UTM parameter capture feeding attribution models correctly
- Custom attribution windows configured for your purchase cycle
- Validation process to spot attribution discrepancies before they compound

## Prerequisites

- [ ] Northbeam account with admin access
- [ ] Google Tag Manager container access (recommended) or developer for site implementation
- [ ] Admin access to all ad platforms you want to attribute (Google Ads, Facebook, TikTok, etc.)
- [ ] Access to email platform APIs (Klaviyo, Mailchimp, etc.)
- [ ] Google Analytics 4 already implemented (Northbeam uses this as a data source)

## Step 1: Install the Northbeam Tracking Pixel

The Northbeam pixel needs to fire on every page, not just conversion pages. I prefer GTM installation because it's easier to debug when things go wrong.

### In Google Tag Manager:

Create a new HTML Custom tag:

```html
<!-- Northbeam Base Pixel -->
<script>
  !function(n,o,r,t,h,b,e,a,m){
    n.NorthbeamObject=h,n[h]=n[h]||function(){
    (n[h].q=n[h].q||[]).push(arguments)},n[h].l=1*new Date();
    b=o.createElement(r),e=o.getElementsByTagName(r)[0];
    b.async=1,b.src=t,e.parentNode.insertBefore(b,e);
    a=o.createElement('script'),m=o.getElementsByTagName('script')[0];
    a.async=1,a.innerHTML='window.northbeam=window.northbeam||function(){(window.northbeam.q=window.northbeam.q||[]).push(arguments)};',
    m.parentNode.insertBefore(a,m)
  }(window,document,'script','https://cdn.northbeam.io/js/[YOUR_PIXEL_ID]/nb.js','northbeam');
  
  northbeam('init', '[YOUR_PIXEL_ID]');
  northbeam('track', 'PageView');
</script>
```

**Trigger:** All Pages

Replace `[YOUR_PIXEL_ID]` with your actual Northbeam pixel ID from your dashboard.

### Direct Implementation:
If you can't use GTM, add this to your site's `<head>` tag on every page.

## Step 2: Configure Purchase Tracking

Northbeam's ML models need clean purchase data. The purchase event should fire on your order confirmation page with complete transaction details.

### GTM Purchase Event:

Create another HTML Custom tag:

```html
<script>
  // Get order data from dataLayer or page variables
  var orderId = '{{Order ID}}'; // GTM variable
  var orderValue = parseFloat('{{Order Total}}'); // GTM variable
  var orderItems = {{Order Items}}; // GTM variable array
  
  northbeam('track', 'Purchase', {
    order_id: orderId,
    value: orderValue,
    currency: 'USD',
    items: orderItems.map(function(item) {
      return {
        product_id: item.item_id,
        product_name: item.item_name,
        category: item.item_category,
        quantity: item.quantity,
        price: item.price
      }
    })
  });
</script>
```

**Trigger:** Purchase page (URL contains `/thank-you` or similar)

If your ecommerce platform doesn't populate a dataLayer, you'll need to extract order data from the page HTML or have your developer pass it through.

## Step 3: Connect Your Ad Platform Data Sources

This is where most setups fall apart. Northbeam needs API access to your ad platforms to see spend and click data. Without this, the attribution models can't work.

### Google Ads Connection:
1. In Northbeam dashboard → Integrations → Google Ads
2. OAuth connect your Google Ads account
3. Select all campaigns you want attributed
4. Enable "Import Offline Conversions" (this sends Northbeam's attributed conversions back to Google Ads)

### Facebook/Meta Connection:
1. Integrations → Facebook/Meta
2. Connect your Business Manager account
3. Grant access to ad accounts and the Conversions API
4. Map your Facebook pixel events to Northbeam events

### TikTok Ads Connection:
1. Integrations → TikTok Ads
2. Connect Business Center account
3. Enable Events API integration

Each platform takes 24-48 hours to start showing data in Northbeam after connection.

## Step 4: Set Up UTM Parameter Capture

Northbeam's attribution depends on clean UTM data. You need to capture and pass UTM parameters through your entire funnel.

### Enhanced UTM Tracking:

In GTM, create a new HTML tag that fires on all pages:

```html
<script>
  // Capture and store UTM parameters
  function captureUTMs() {
    var urlParams = new URLSearchParams(window.location.search);
    var utmData = {};
    
    ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'].forEach(function(param) {
      var value = urlParams.get(param);
      if (value) {
        utmData[param] = value;
        // Store in localStorage for session persistence
        localStorage.setItem(param, value);
      } else {
        // Get from storage if not in current URL
        var stored = localStorage.getItem(param);
        if (stored) utmData[param] = stored;
      }
    });
    
    // Also capture platform-specific parameters
    var fbclid = urlParams.get('fbclid');
    var gclid = urlParams.get('gclid');
    var ttclid = urlParams.get('ttclid');
    
    if (fbclid) {
      utmData.fbclid = fbclid;
      localStorage.setItem('fbclid', fbclid);
    }
    if (gclid) {
      utmData.gclid = gclid;
      localStorage.setItem('gclid', gclid);
    }
    if (ttclid) {
      utmData.ttclid = ttclid;
      localStorage.setItem('ttclid', ttclid);
    }
    
    // Send to Northbeam
    if (Object.keys(utmData).length > 0) {
      northbeam('track', 'UTMCapture', utmData);
    }
  }
  
  captureUTMs();
</script>
```

This ensures Northbeam sees the attribution data even if users don't convert on their first visit.

## Step 5: Configure Attribution Windows

Northbeam's default attribution windows are 7-day click, 1-day view. For most ecommerce businesses, that's too short.

### Recommended Windows by Industry:
- **Fashion/Apparel:** 14-day click, 2-day view
- **Home/Furniture:** 30-day click, 7-day view  
- **Beauty/Personal Care:** 14-day click, 3-day view
- **Electronics:** 21-day click, 3-day view

To configure:
1. Northbeam Dashboard → Settings → Attribution
2. Set click and view windows for each channel
3. Choose between "First-Touch," "Last-Touch," or "Multi-Touch" models
4. Enable "Cross-Device" tracking if you have enough volume (1000+ monthly conversions)

I typically recommend starting with multi-touch attribution and 14-day click windows, then adjusting based on your actual customer journey data.

## Testing & Verification

### Verify Pixel Installation:
1. Install the Northbeam Chrome extension
2. Navigate your site — you should see "Northbeam Detected" and "PageView" events firing
3. Complete a test purchase — verify the Purchase event fires with correct order data

### Check Data Integration:
1. In Northbeam Dashboard → Data Sources
2. Verify all connected platforms show "Connected" status with recent data timestamps
3. Go to Attribution → Touchpoints — you should see clicks and impressions from connected platforms within 48 hours

### Validate Attribution Numbers:
Compare Northbeam's attributed conversions to native platform reporting:
- **Google Ads:** Northbeam typically reports 10-20% fewer conversions (removes view-through that GA4 counts)
- **Facebook:** Northbeam reports 15-30% fewer (more conservative attribution windows)
- **Email:** Northbeam often reports 2x more email attribution than platforms like Klaviyo (credits email for influenced purchases)

Acceptable variance is 20-40% for individual channels. If you're seeing 50%+ discrepancies, something's misconfigured.

## Troubleshooting

**Problem:** Northbeam shows zero conversions after 48 hours
Double-check your purchase tracking implementation. Use the browser console to verify the Purchase event fires correctly. Most common issue is the pixel firing before the northbeam object is loaded — add a small delay or use GTM's built-in loading triggers.

**Problem:** Google Ads integration connected but shows no click data
Your Google Ads account needs "Enhanced Conversions" enabled and proper linking to your Google Analytics 4 property. Northbeam pulls click data through the GA4 integration, not directly from Google Ads.

**Problem:** Attribution windows not matching expected behavior  
Northbeam uses "conversion date" as the anchor point for attribution windows, not "click date." A purchase on March 10th will look back 14 days to February 24th, regardless of when you changed the attribution window setting.

**Problem:** Cross-device attribution showing inflated numbers
Cross-device only works well with 1000+ monthly conversions. Below that threshold, the ML models overshoot and you'll see inflated attribution. Disable cross-device tracking for lower-volume accounts.

**Problem:** Email attribution seems too high compared to Klaviyo
This is usually correct. Northbeam credits email for purchases that happen within the attribution window, even if the customer clicked an ad later. Email platforms like Klaviyo only credit direct email→purchase paths. The truth is usually somewhere in between.

**Problem:** TikTok conversions not showing up in Northbeam
TikTok's Events API integration is flaky. Verify your TikTok pixel is installed correctly first, then check that you've granted "Events API" permissions in TikTok Business Center. Sometimes you need to disconnect and reconnect the integration.

## What To Do Next

Once your Northbeam setup is running clean, you'll want to optimize your attribution modeling and explore advanced features:

- [Attribution Modeling Best Practices](/attribution) — covers choosing between first-touch, last-touch, and multi-touch models
- [Cross-Platform Attribution Setup](/attribution/cross-platform-setup) — expanding beyond just paid channels
- [Attribution Data Validation](/attribution/data-validation) — ongoing processes to catch attribution drift

Need help getting this configured correctly? I offer a [free tracking audit](/contact) to identify what's broken in your current setup. Or if you want this done right the first time, check out my [done-for-you attribution setup service](/services/attribution-setup).

*This guide is part of the [Attribution Setup Hub](/attribution) — comprehensive guides for implementing attribution tracking across all major tools and platforms.*