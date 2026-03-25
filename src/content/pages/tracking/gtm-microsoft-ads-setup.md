---
title: "Client-Side GTM for Microsoft Ads: Complete Setup Guide (2026)"
slug: "gtm-microsoft-ads-setup"
description: "Complete guide to setting up Client-Side GTM for Microsoft Ads. Step-by-step configuration, testing, and troubleshooting."
category: "tracking"
date: "2026-03-24"
hub_page: "/tracking/form-conversion-tracking"
page_type: "spoke"
---

# Client-Side GTM + Microsoft Ads Setup Guide

I see broken Microsoft Ads tracking in about 60% of the accounts I audit — usually because someone tried to paste the UET tag directly into their site instead of properly configuring it through GTM. Microsoft's tracking gets especially messy when you're running forms or multi-step funnels, and their documentation assumes you're only tracking basic page views.

This guide walks through the complete client-side GTM setup for Microsoft Ads UET tracking that actually works in production.

## What You'll Have Working By The End

- **Clean UET base code** firing on all pages without duplicate events
- **Form conversion tracking** with proper goal configuration in Microsoft Ads
- **Custom event tracking** for multi-step funnels or lead qualification
- **Revenue tracking** with actual purchase values (if applicable)
- **Debug verification** showing events hitting Microsoft's servers in real-time

## Prerequisites

- [ ] Google Tag Manager container access (Publish permissions)
- [ ] Microsoft Ads account access with conversion tracking permissions
- [ ] UET Tag ID from Microsoft Ads (format: 12345678)
- [ ] Website with GTM container already installed
- [ ] Form IDs or conversion trigger elements identified

## Step 1: Configure the Microsoft UET Base Tag

The UET base tag needs to load on every page before any conversion events fire. I set this up as a single tag that handles both the base tracking and batches conversion events.

In GTM, create a new tag:

**Tag Type:** Custom HTML  
**Tag Name:** Microsoft UET Base  
**Firing Triggers:** All Pages

```html
<script>
(function(w,d,t,r,u){
var f,n,i;
w[u]=w[u]||[],f=function(){
var o={ti:"{UET_TAG_ID}"};
o.q=w[u],w[u]=new UetTag(o),w[u].push("pageLoad")
},n=d.createElement(t),n.src=r,n.async=1,n.onload=n.onreadystatechange=function(){
var s=n.readyState;s&&s!=="loaded"&&s!=="complete"||(f(),n.onload=n.onreadystatechange=null)
},i=d.getElementsByTagName(t)[0],i.parentNode.insertBefore(n,i)
})(window,document,"script","//bat.bing.com/bat.js","uetq");
</script>
```

Replace `{UET_TAG_ID}` with your actual UET Tag ID from Microsoft Ads.

**Advanced Configuration:** Add this custom JavaScript variable if you need to pass additional page data:

**Variable Name:** UET Page Data  
**Variable Type:** Custom JavaScript

```javascript
function() {
  return {
    event_category: 'page_view',
    page_title: document.title,
    page_location: window.location.href,
    custom_data: {
      user_type: {{User Type}}, // reference other GTM variables
      page_category: {{Page Category}}
    }
  };
}
```

## Step 2: Set Up Form Conversion Tracking

Microsoft Ads conversion tracking requires both the tag configuration in GTM and the corresponding goal setup in the Microsoft Ads interface.

Create a new tag in GTM:

**Tag Type:** Custom HTML  
**Tag Name:** Microsoft UET - Form Conversion  
**Firing Triggers:** Form Submit (configure based on your form setup)

```html
<script>
window.uetq = window.uetq || [];
window.uetq.push('event', 'form_submit', {
  'event_category': 'conversion',
  'event_label': 'contact_form',
  'revenue_value': {{Conversion Value}}, // optional, use GTM variable
  'currency': 'USD' // or dynamic currency variable
});
</script>
```

**Trigger Configuration:**  
**Trigger Type:** Form Submission  
**Wait for Tags:** 2000ms (crucial for Microsoft's slower event processing)  
**Enable when:** Form matches your specific form selector

For lead forms, I typically set up the trigger to fire on:
- **Some Forms** where Form ID contains `contact` OR Form Classes contains `lead-form`
- OR specific CSS selectors: `form[data-conversion="true"]`

## Step 3: Configure Microsoft Ads Conversion Goals

In your Microsoft Ads account, you need to create the corresponding conversion goals that match your GTM events.

Navigate to **Tools > Conversion Tracking > Conversion Goals**

**Goal Details:**
- **Goal Name:** Contact Form Submission (match your GTM event label)
- **Goal Category:** Lead or Sale
- **Revenue:** Same value setup as your GTM configuration
- **Count:** One per customer (prevents duplicate conversions)

**UET Tag Association:**
- Select your UET tag created in Step 1
- **Goal Type:** Event goal
- **Event Action:** form_submit
- **Event Category:** conversion

The event parameters must match exactly between GTM and Microsoft Ads or the conversions won't attribute properly.

## Step 4: Add Enhanced Conversion Tracking

For better attribution and to combat iOS 14.5+ tracking limitations, set up Microsoft's enhanced conversions.

Create an additional GTM tag:

**Tag Type:** Custom HTML  
**Tag Name:** Microsoft UET - Enhanced Data  
**Firing Triggers:** Form Submit (same as Step 2)

```html
<script>
window.uetq = window.uetq || [];
window.uetq.push('event', '', {
  'ec': 'enhanced_conversion',
  'ea': 'form_submit',
  'el': {{Form ID}},
  'customer_data': {
    'em': {{Hashed Email}}, // SHA-256 hashed email
    'ph': {{Hashed Phone}}, // SHA-256 hashed phone
    'fn': {{Hashed First Name}}, // optional
    'ln': {{Hashed Last Name}}, // optional
    'ct': {{City}}, // optional
    'st': {{State}}, // optional
    'zp': {{Zip Code}}, // optional
    'cn': 'US' // country code
  }
});
</script>
```

**Important:** Hash the personally identifiable information (PII) using SHA-256 before sending. Create GTM variables that hash the form data client-side:

```javascript
function() {
  var email = {{Email Form Field}};
  if (email) {
    // Basic SHA-256 implementation or use crypto.subtle.digest
    return CryptoJS.SHA256(email.toLowerCase().trim()).toString();
  }
  return undefined;
}
```

## Step 5: Set Up E-commerce Revenue Tracking

If you're tracking purchases or lead values, configure revenue tracking with proper currency handling.

**Tag Type:** Custom HTML  
**Tag Name:** Microsoft UET - Purchase  
**Firing Triggers:** Purchase Complete

```html
<script>
window.uetq = window.uetq || [];
window.uetq.push('event', 'purchase', {
  'event_category': 'ecommerce',
  'revenue_value': {{Purchase Value}},
  'currency': {{Currency Code}},
  'transaction_id': {{Transaction ID}},
  'items': [
    {
      'id': {{Product ID}},
      'quantity': {{Quantity}},
      'price': {{Product Price}}
    }
  ]
});
</script>
```

**Revenue Value Variable Setup:**  
**Variable Type:** Data Layer Variable  
**Data Layer Variable Name:** `purchase.value` or `ecommerce.purchase.actionField.revenue`

Make sure your e-commerce platform is pushing the purchase data to the GTM data layer in the correct format.

## Testing & Verification

**GTM Preview Mode:**
1. Enable Preview mode in GTM
2. Navigate through your conversion funnel
3. Verify the UET base tag fires on all pages
4. Check that conversion events fire only when expected
5. Confirm no duplicate events (common issue with Microsoft tracking)

**Microsoft UET Helper:**
Install the Microsoft UET Helper browser extension. After triggering a conversion:
- Base UET tag should show "Success" status
- Conversion events should appear with correct parameters
- Revenue values should match your expected amounts

**Microsoft Ads Validation:**
In Microsoft Ads, go to **Tools > UET Tag Helper**:
- Verify tag installation shows "Tag Active"
- Check conversion goals show "Recording conversions"
- Look for validation errors in the diagnostics section

**Cross-Platform Verification:**
Compare conversion counts between:
- GTM debug console (events fired)
- Microsoft UET Helper (events received)
- Microsoft Ads reporting (conversions attributed)

Acceptable variance is 10-20% due to ad blockers and attribution windows. If you're seeing 30%+ variance, something's broken.

## Troubleshooting

**Problem:** UET tag fires multiple times on single page load  
Check for duplicate GTM containers or manual UET installations. Remove any hardcoded UET tags from your site template. Ensure the GTM tag only fires once per page.

**Problem:** Conversions firing but not showing in Microsoft Ads  
Verify the event parameters match exactly between GTM and your Microsoft Ads conversion goal setup. Event action, category, and label are case-sensitive. Check the conversion attribution window — Microsoft defaults to 7 days view-through.

**Problem:** Enhanced conversion data rejected  
Microsoft requires properly hashed PII data. Verify your email/phone hashing is using SHA-256 and includes proper normalization (lowercase, trim whitespace). Test with the Microsoft UET Helper to see validation errors.

**Problem:** Revenue tracking shows $0.00 values  
Check that your GTM revenue variables are pulling actual numeric values, not strings. Remove currency symbols and ensure proper data layer formatting. Microsoft expects revenue as a number, not formatted currency.

**Problem:** Form submissions not triggering conversion tags  
Increase the "Wait for Tags" timing in your form trigger to 3000ms. Microsoft's tracking is slower than Google's. Also verify your form trigger is actually firing by checking GTM Preview mode.

**Problem:** Tags working in preview but not in production  
Clear your GTM container cache and republish. Microsoft's CDN can take 15-20 minutes to propagate changes. Also check for JavaScript errors on your live site that might prevent tag execution.

## What To Do Next

- Set up [Server-Side GTM for Microsoft Ads](/tracking/server-gtm-microsoft-ads-setup) for better data quality and iOS 14.5+ resilience
- Configure [Lead Form Conversion Tracking](/tracking/lead-form-conversion-tracking) for specific form types
- Implement [Multi-Step Funnel Tracking](/tracking/multi-step-funnel-tracking) to optimize your conversion paths
- Get a [free tracking audit](/contact) to verify your Microsoft Ads setup is capturing all available conversions

*This guide is part of the [Form Conversion Tracking Hub](/tracking/form-conversion-tracking) — comprehensive guides for tracking form conversions across all major ad platforms.*