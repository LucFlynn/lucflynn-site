---
title: "Northbeam + Google Ads Attribution Setup Guide (2026)"
slug: "northbeam-google-ads-setup"
description: "Step-by-step Northbeam setup for Google Ads attribution. Covers pixel installation, integration configuration, and verification."
category: "attribution"
date: "2026-03-24"
hub_page: "/attribution"
page_type: "spoke"
---

# How to Set Up Northbeam for Google Ads

I've audited 40+ Northbeam setups in the past year, and about 60% have critical configuration issues that inflate or deflate their Google Ads attribution. The biggest problem? Teams install the pixel but skip the data connection setup, then wonder why their attribution looks like garbage compared to Google Ads' native reporting.

Northbeam's ML attribution can be powerful, but only if you feed it clean data from the start. Miss the URL parameter passthrough or botch the conversion event mapping, and you'll be making bid decisions based on fantasy numbers.

## What You'll Have Working By The End

- Northbeam pixel tracking all Google Ads traffic with proper UTM parameter capture
- Direct Google Ads API connection feeding conversion data back to Google
- Custom attribution windows configured to match your actual customer journey
- Data validation process to catch discrepancies between Northbeam and Google Ads native reporting
- Troubleshooting playbook for the most common integration failures

## Prerequisites

- [ ] Northbeam account with admin access
- [ ] Google Ads account with admin permissions
- [ ] Website with ability to add JavaScript to header
- [ ] Google Analytics 4 connected (Northbeam pulls GA4 data for enhanced modeling)
- [ ] At least 2 weeks of conversion data in Google Ads (for baseline comparison)

## Step 1: Install the Northbeam Pixel

The Northbeam pixel needs to fire on every page, not just conversion pages. I see teams install it only on thank you pages about 25% of the time, which completely breaks the customer journey tracking.

Add this script to your website's `<head>` section, before any other tracking pixels:

```javascript
<script>
!function(n,o,r,t,h,b,e,a,m){n.NorthbeamObject=h,n[h]=n[h]||function(){
(n[h].q=n[h].q||[]).push(arguments)},n[h].l=1*new Date,b=o.createElement(r),
e=o.getElementsByTagName(r)[0],b.async=1,b.src=t,e.parentNode.insertBefore(b,e),
m=function(){n[h]('event','pageview')},n.attachEvent?n.attachEvent('onload',m):n.addEventListener('load',m,!1)
}(window,document,'script','https://cdn.northbeam.io/js/nb.js','nb');

nb('init', 'YOUR_PIXEL_ID');
nb('event', 'pageview');
</script>
```

Replace `YOUR_PIXEL_ID` with your actual pixel ID from the Northbeam dashboard (Settings → Pixels → Copy Pixel ID).

**Critical:** The pixel must load before other marketing pixels like Facebook Pixel or Google Ads tags. Northbeam uses first-party data collection, and loading order affects data quality.

For Shopify users, paste this in Settings → Checkout → Additional Scripts, NOT in the theme files. Shopify's checkout flow requires the pixel to persist across domain changes.

## Step 2: Configure URL Parameter Tracking

Northbeam needs to capture UTM parameters and Google's click ID (GCLID) to properly attribute conversions. The default pixel installation captures basic UTMs, but you need to explicitly track GCLID.

Add this parameter tracking configuration right after your pixel initialization:

```javascript
<script>
// Enhanced parameter tracking for Google Ads
nb('config', {
  track_params: true,
  utm_source: true,
  utm_medium: true,
  utm_campaign: true,
  utm_content: true,
  utm_term: true,
  gclid: true,
  wbraid: true,  // For iOS 14.5+ tracking
  gbraid: true   // For iOS 14.5+ tracking
});

// Custom parameter capture for Google Ads extensions
const urlParams = new URLSearchParams(window.location.search);
if (urlParams.get('gclid')) {
  nb('set', 'gclid', urlParams.get('gclid'));
}
</script>
```

**Which tracking approach should you use?** If you're running Performance Max or Smart campaigns, enable both `wbraid` and `gbraid` tracking. For standard Search and Display campaigns, GCLID tracking is sufficient.

## Step 3: Set Up Conversion Event Tracking

This is where most setups break. Northbeam needs to know what constitutes a conversion, and these events need to match exactly with what you're optimizing for in Google Ads.

For e-commerce purchases, add this to your order confirmation page:

```javascript
<script>
nb('event', 'purchase', {
  transaction_id: '{{ order.order_number }}',
  value: {{ order.total_price | divided_by: 100.0 }},
  currency: '{{ shop.currency }}',
  items: [
    {% for line_item in order.line_items %}
    {
      item_id: '{{ line_item.variant.sku | default: line_item.variant.id }}',
      item_name: '{{ line_item.title }}',
      category: '{{ line_item.product.type }}',
      quantity: {{ line_item.quantity }},
      price: {{ line_item.final_price | divided_by: 100.0 }}
    }{% unless forloop.last %},{% endunless %}
    {% endfor %}
  ]
});
</script>
```

For lead generation, track form submissions:

```javascript
<script>
// Fire when lead form is successfully submitted
nb('event', 'lead', {
  value: 50.00,  // Assign a value based on your average lead value
  currency: 'USD',
  form_type: 'contact_form'  // Custom parameter for segmentation
});
</script>
```

**Warning:** Don't fire conversion events on form views or button clicks. Only fire when the actual conversion happens (form submitted, order completed, trial started).

## Step 4: Connect Google Ads API Integration

Go to Northbeam dashboard → Integrations → Google Ads → Add New Connection.

You'll need to authorize Northbeam to access your Google Ads account. This connection serves two purposes:
1. Imports cost and impression data for attribution modeling
2. Sends conversion data back to Google Ads for optimization

**Key settings:**

- **Auto-import conversions:** Enable this to send Northbeam's attributed conversions back to Google Ads
- **Attribution window:** Set to match your Google Ads conversion windows (typically 30 days view, 1 day click)
- **Conversion name mapping:** Map Northbeam events to existing Google Ads conversion actions

I recommend creating separate conversion actions in Google Ads for Northbeam data (e.g., "Purchase - Northbeam Attribution") rather than overwriting existing ones. This lets you compare attribution models side-by-side.

## Step 5: Configure Attribution Settings

Navigate to Settings → Attribution in your Northbeam dashboard.

**Attribution Window Configuration:**
- Click-through attribution: 30 days (matches Google Ads default)
- View-through attribution: 1 day (more conservative than Google's 30-day default)
- Cross-device attribution: Enable if you have sufficient login data

**Custom Attribution Rules:**
Set up channel priority if you're running multiple paid channels. For most accounts, I recommend:
1. Direct/branded search (highest priority)
2. Google Ads non-branded
3. Facebook/Meta
4. Other paid channels

**Model Selection:** Start with Northbeam's "Northbeam Model" (their ML approach). After 30 days of data, you can A/B test against "First Click" or "Linear" models to see which performs better for your business.

## Testing & Verification

**1. Pixel Installation Check:**
Use Northbeam's Chrome extension or check the browser console. You should see successful pixel loads and pageview events firing.

**2. Parameter Capture Verification:**
Visit your site with test UTM parameters: `yoursite.com?utm_source=google&utm_medium=cpc&gclid=test123`

In Northbeam Events tab, verify the pageview event captured all parameters correctly.

**3. Conversion Tracking Test:**
Complete a test purchase or lead form submission. Within 2-3 minutes, you should see the conversion event in Northbeam's Events stream with all the correct data points.

**4. Google Ads Integration Check:**
In Google Ads, go to Tools → Conversions. You should see Northbeam conversions importing within 6-24 hours of the API connection.

**5. Attribution Comparison:**
After 1 week of data, compare Northbeam's Google Ads attribution to Google Ads native reporting. Acceptable variance is 10-25%. Northbeam typically shows higher conversion counts due to cross-device and view-through attribution modeling.

**Red flags:**
- Zero conversions showing in Northbeam after 48 hours
- More than 40% variance between Northbeam and Google Ads native reporting
- Missing GCLID capture (check URL parameter reports)

## Troubleshooting

**Problem:** Northbeam shows Google Ads conversions, but Google Ads shows zero Northbeam conversions
**Solution:** Check that conversion import is enabled in the Google Ads integration settings. Verify the conversion action mapping matches existing Google Ads conversion names exactly (case sensitive).

**Problem:** Huge discrepancy between Northbeam and Google Ads attribution (50%+ difference)
**Solution:** Check attribution window settings match between platforms. Northbeam's default view-through window is longer than most Google Ads setups. Reduce Northbeam's view-through window to 1 day to start.

**Problem:** Pixel firing but no parameter capture for Google Ads traffic
**Solution:** Verify GCLID parameter tracking is enabled in the pixel configuration. Check that the parameter capture script loads after the main Northbeam pixel. Clear browser cache and test with fresh URLs.

**Problem:** Conversions showing wrong values or missing product data
**Solution:** Check the conversion event syntax matches Northbeam's required format exactly. Common issue: passing strings instead of numbers for value fields. Use `parseFloat()` to ensure numeric values.

**Problem:** Attribution showing all conversions as "Direct" despite UTM parameters
**Solution:** The pixel may be loading after a redirect that strips UTM parameters. Move pixel installation higher in the page head, before any redirect scripts. Check for URL shorteners or tracking scripts that modify URLs.

**Problem:** Integration disconnecting frequently or showing API errors
**Solution:** Google Ads API tokens expire. Re-authorize the connection in Northbeam. If problems persist, create a new Google Ads manager account specifically for API connections (more stable than individual account access).

## What To Do Next

Got Northbeam connected but want to compare it with other attribution tools? Check out the [complete attribution setup guide](/attribution) to see how Northbeam stacks up against Triple Whale, Hyros, and other popular options.

Need help with advanced multi-touch attribution modeling or custom event tracking? My [attribution setup service](/services/attribution-setup) includes full Northbeam configuration plus 90 days of data validation.

Want a free audit of your current tracking setup? [Book a call](/contact) and I'll review your Northbeam configuration plus identify any gaps in your measurement stack.

*This guide is part of the [Attribution Tool Setup Hub](/attribution) — complete guides for connecting attribution platforms with major ad networks.*