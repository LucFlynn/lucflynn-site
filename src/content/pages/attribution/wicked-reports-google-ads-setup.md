---
title: "Wicked Reports + Google Ads Attribution Setup Guide (2026)"
slug: "wicked-reports-google-ads-setup"
description: "Step-by-step Wicked Reports setup for Google Ads attribution. Covers pixel installation, integration configuration, and verification."
category: "attribution"
date: "2026-03-24"
hub_page: "/attribution"
page_type: "spoke"
---

# How to Set Up Wicked Reports for Google Ads

I see about 60% of B2B companies running Google Ads without proper attribution beyond last-click. They're flying blind on which keywords actually drive revenue 30-90 days later. Wicked Reports solves this by connecting your CRM sales data back to the original Google Ads click, but the setup is more involved than most attribution tools — and when it's wrong, you're making budget decisions on phantom data.

## What You'll Have Working By The End

- Wicked Reports tracking script installed and firing on all pages
- Google Ads conversion imports flowing automatically to your account
- UTM parameter capture feeding customer acquisition data into your CRM
- Revenue attribution showing which Google Ads campaigns/keywords drove closed deals
- Cross-platform view of your customer journey from Google Ads through to final sale

## Prerequisites

- [ ] Admin access to your website (to install tracking script)
- [ ] Wicked Reports account with active subscription
- [ ] Google Ads account with conversion tracking permissions
- [ ] CRM integration already set up in Wicked Reports (HubSpot, Salesforce, etc.)
- [ ] UTM parameter strategy defined for your campaigns

## Step 1: Install the Wicked Reports Universal Tracking Script

First, get your tracking script from Wicked Reports. In your dashboard, go to Settings > Tracking Code. You'll see something like this:

```html
<!-- Wicked Reports Universal Tracking -->
<script type="text/javascript">
  var _wrq = _wrq || [];
  _wrq.push(['_setAccount', 'ABC123']);
  _wrq.push(['_setDomain', 'yourdomain.com']);
  _wrq.push(['_setTimeZone', 'US/Eastern']);
  _wrq.push(['_trackPageView']);
  
  (function() {
    var wr = document.createElement('script');
    wr.type = 'text/javascript';
    wr.async = true;
    wr.src = 'https://www.wickedreports.com/analytics.js';
    var s = document.getElementsByTagName('script')[0];
    s.parentNode.insertBefore(wr, s);
  })();
</script>
```

Install this in your website's `<head>` section on every page. If you're using GTM, create a Custom HTML tag that fires on All Pages. Don't put it in the footer — Wicked Reports needs to fire early to catch the session data properly.

**Critical:** Make sure the `_setDomain` matches your actual domain. I've seen setups broken for months because someone used 'www.domain.com' when their site redirects to 'domain.com', causing session attribution to fail.

## Step 2: Configure Enhanced Ecommerce Tracking (If Applicable)

If you're running ecommerce, you need to push transaction data to Wicked Reports immediately after purchase. Add this code to your thank you page:

```javascript
_wrq.push(['_trackPurchase', {
  'order_id': '{{ORDER_ID}}',
  'total': {{ORDER_TOTAL}},
  'currency': 'USD',
  'products': [
    {
      'sku': '{{PRODUCT_SKU}}',
      'name': '{{PRODUCT_NAME}}',
      'price': {{PRODUCT_PRICE}},
      'quantity': {{QUANTITY}}
    }
  ]
}]);
```

Replace the template variables with your actual order data. If you're using Shopify, WooCommerce, or another platform, Wicked Reports has specific plugins that handle this automatically — use those instead of manual implementation.

## Step 3: Connect Google Ads to Wicked Reports

In your Wicked Reports dashboard, go to Integrations > Google Ads. Click "Add Google Ads Account" and authorize the connection. You'll need admin access to your Google Ads account for this to work.

Once connected, configure these settings:

- **Conversion Action Name:** Use something descriptive like "WR - Sales" or "WR - Qualified Leads"
- **Conversion Window:** Set this to match your typical sales cycle (30-90 days for most B2B)
- **Attribution Model:** I recommend "First Click" if you want to see which campaigns start the customer journey
- **Conversion Value:** Set to "Use actual conversion values" to pass revenue data

**Important:** Wicked Reports will create new conversion actions in your Google Ads account. Don't delete these or try to merge them with existing conversion tracking — you'll break the attribution flow.

## Step 4: Set Up UTM Parameter Capture

Wicked Reports relies heavily on UTM parameters to connect Google Ads clicks to later conversions. Your Google Ads campaigns need consistent UTM tagging. I recommend this structure:

- `utm_source=google`
- `utm_medium=cpc`
- `utm_campaign={{campaign}}`
- `utm_term={{keyword}}`
- `utm_content={{adgroup}}`

In Google Ads, go to Account Settings > Account-level automated tagging and enable "Auto-tagging." Then add your UTM template at the campaign level in the URL options:

```
?utm_source=google&utm_medium=cpc&utm_campaign={campaignid}&utm_term={keyword}&utm_content={adgroupid}
```

**Which should you use — campaign names or IDs?** I prefer IDs because campaign names change, but IDs are permanent. Makes reporting more stable over time.

## Step 5: Configure CRM Integration Mapping

This is where most setups break. In Wicked Reports, go to Integrations > [Your CRM] > Field Mapping. You need to map:

- **Lead Source:** Should capture "Google Ads"
- **Campaign:** Maps to utm_campaign
- **Keyword:** Maps to utm_term
- **Ad Group:** Maps to utm_content
- **Landing Page:** First page the user visited

The critical part is ensuring your CRM is actually capturing these UTM parameters when leads convert. Most CRMs don't do this by default. You'll need to:

1. Add hidden fields to your forms for utm_source, utm_medium, utm_campaign, utm_term, utm_content
2. Use JavaScript to populate these fields from the URL parameters
3. Map these form fields to custom properties in your CRM

Here's the JavaScript for hidden field population:

```javascript
function getURLParameter(name) {
  return new URLSearchParams(window.location.search).get(name) || 
         sessionStorage.getItem(name) || '';
}

// Populate hidden fields
document.getElementById('utm_source').value = getURLParameter('utm_source');
document.getElementById('utm_medium').value = getURLParameter('utm_medium');
document.getElementById('utm_campaign').value = getURLParameter('utm_campaign');
document.getElementById('utm_term').value = getURLParameter('utm_term');
document.getElementById('utm_content').value = getURLParameter('utm_content');

// Store in session storage for multi-page forms
sessionStorage.setItem('utm_source', getURLParameter('utm_source'));
sessionStorage.setItem('utm_medium', getURLParameter('utm_medium'));
// etc...
```

## Step 6: Test the Google Ads Conversion Import

Go to Google Ads > Tools & Settings > Conversions. You should see the conversion actions that Wicked Reports created. Click on one and check the "Recent conversions" section.

If everything is working, you'll see conversions appearing here with attribution back to specific campaigns and keywords. The data flow typically takes 2-4 hours for test conversions to appear.

## Testing & Verification

**In Wicked Reports:**
- Go to Dashboard > Data Quality Check
- Verify your tracking script is firing on all pages (should show 100% coverage)
- Check that form submissions are being captured with UTM data
- Look for Google Ads attribution in the Customer Journey reports

**In Google Ads:**
- Check Tools & Settings > Conversions for imported conversion actions
- Verify conversions are appearing with proper attribution
- Cross-check conversion values match what you see in Wicked Reports

**Cross-Platform Verification:**
Compare Google Ads conversion counts to Wicked Reports data. Expect 10-20% discrepancy due to:
- Attribution window differences
- Users blocking tracking scripts
- CRM data quality issues (duplicate leads, missing UTM capture)

**Red flags that indicate broken setup:**
- 0 conversions showing in Google Ads after 48+ hours
- All conversions attributed to "(not set)" campaigns
- Massive discrepancy (>40%) between platforms
- UTM data showing as blank in your CRM

## Troubleshooting

**Problem:** Google Ads shows 0 conversions but Wicked Reports shows sales
**Solution:** Check your CRM field mapping. Wicked Reports can only attribute sales that have proper UTM data in your CRM. If leads are coming in without utm_source="google", they won't be attributed to Google Ads.

**Problem:** All conversions show as "(not set)" campaign in Google Ads
**Solution:** Your UTM parameters aren't being captured properly. Verify that your landing pages are actually appending the UTM parameters and that your forms are capturing them in hidden fields.

**Problem:** Conversion values in Google Ads don't match actual sale amounts
**Solution:** Check your currency settings in both platforms. Also verify that Wicked Reports is pulling the correct revenue field from your CRM (many CRMs have multiple revenue fields).

**Problem:** Massive lag between sale and attribution showing in Google Ads
**Solution:** This is normal for Wicked Reports since it waits for CRM data to sync. Typical delay is 4-24 hours depending on your CRM sync frequency. Check Integrations > [Your CRM] > Sync Status for issues.

**Problem:** Some campaigns show attribution but others don't
**Solution:** Check your campaign-level UTM templates. Each campaign needs proper UTM tagging. Also verify that your ad groups and keywords aren't using conflicting destination URLs.

**Problem:** Wicked Reports dashboard shows "Low data quality" warnings
**Solution:** Usually means your UTM capture is incomplete. Check that all traffic sources (not just Google Ads) are properly tagged, and that your website isn't stripping UTM parameters on form submissions.

## What To Do Next

Now that you have Google Ads attribution working, consider expanding your attribution setup:

- [Full Attribution Tool Comparison](/attribution) — See how Wicked Reports stacks up against other attribution solutions
- [Multi-Touch Attribution Setup](/attribution/multi-touch-setup) — Configure Wicked Reports for more sophisticated attribution models
- [Attribution Reporting Best Practices](/attribution/reporting-guide) — Get the most value from your attribution data

Want this setup done right the first time? [Get a free tracking audit](/contact) and I'll review your current setup and show you exactly what's broken (and how much revenue you're missing because of it).

*This guide is part of the [Attribution Setup Hub](/attribution) — comprehensive guides for connecting your ad spend to actual revenue.*