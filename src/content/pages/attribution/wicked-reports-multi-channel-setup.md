---
title: "Wicked Reports + Multi-Channel Attribution Setup Guide (2026)"
slug: "wicked-reports-multi-channel-setup"
description: "Step-by-step Wicked Reports setup for Multi-Channel attribution. Covers pixel installation, integration configuration, and verification."
category: "attribution"
date: "2026-03-24"
hub_page: "/attribution"
page_type: "spoke"
---

# How to Set Up Wicked Reports for Multi-Channel

Wicked Reports is solid for B2B attribution, but I see about 60% of multi-channel setups missing the CRM integration piece or tracking the wrong customer journey touchpoints. The platform excels at long sales cycle attribution, but it requires proper data flow from your CRM to actually connect the dots between that Facebook ad click and the deal that closed 3 months later.

The most common mistake? People set up the pixel but never configure the CRM sync properly, so they're only seeing partial attribution data.

## What You'll Have Working By The End

- Wicked Reports pixel tracking all traffic sources and campaign parameters
- CRM integration syncing customer data and revenue attribution back to ad touches
- Cross-platform attribution reports showing the full customer journey
- Proper UTM and platform-specific parameter tracking for Facebook, Google, LinkedIn, and TikTok
- Revenue attribution flowing back to specific campaigns and ad sets

## Prerequisites

- [ ] Wicked Reports account with API access
- [ ] Admin access to your CRM (HubSpot, Salesforce, Pipedrive, or ActiveCampaign)
- [ ] Ad platform access for Facebook Ads Manager, Google Ads, LinkedIn Campaign Manager
- [ ] Website admin access or developer who can add JavaScript
- [ ] At least 30 days of historical CRM data for baseline comparison

## Step 1: Install the Wicked Reports Pixel

Get your pixel code from Settings > Tracking Code in your Wicked Reports dashboard. The tracking script needs to go on every page of your website.

```javascript
<script type="text/javascript">
var _wrs = _wrs || [];
_wrs.push(['setAccount', 'YOUR_ACCOUNT_ID']);
_wrs.push(['setDomain', 'your-domain.com']);
_wrs.push(['setTrackByDefault', true]);

(function() {
    var wrs = document.createElement('script'); 
    wrs.type = 'text/javascript'; 
    wrs.async = true;
    wrs.src = ('https:' == document.location.protocol ? 'https://' : 'http://') + 'www.wickedreports.com/analytics.js';
    var s = document.getElementsByTagName('script')[0]; 
    s.parentNode.insertBefore(wrs, s);
})();
</script>
```

Replace `YOUR_ACCOUNT_ID` with your actual account ID from the dashboard and `your-domain.com` with your website domain.

For conversion tracking, add this to your thank you pages:

```javascript
<script type="text/javascript">
_wrs.push(['setOrderId', 'ORDER_ID']);
_wrs.push(['setEmail', 'customer@email.com']);
_wrs.push(['setOrderValue', 'TOTAL_VALUE']);
_wrs.push(['trackPurchase']);
</script>
```

Replace the placeholder values with actual order data. If you're using a CRM form instead of direct purchases, track form submissions:

```javascript
<script type="text/javascript">
_wrs.push(['setEmail', 'lead@email.com']);
_wrs.push(['setLeadValue', 'ESTIMATED_VALUE']);
_wrs.push(['trackLead']);
</script>
```

## Step 2: Configure CRM Integration

This is where most setups break. Wicked Reports needs your CRM data to connect ad clicks to actual revenue. Go to Integrations in your dashboard and select your CRM.

**For HubSpot:**
1. Click "Connect HubSpot" and authorize the integration
2. Map your deal stages to Wicked Reports pipeline stages
3. Set your lead-to-customer conversion rules
4. Configure deal amount syncing (use "Amount" field)

**For Salesforce:**
1. Install the Wicked Reports package from the AppExchange
2. Configure the sync settings in Setup > Installed Packages
3. Map Opportunity fields to Wicked Reports fields
4. Set up the automated sync schedule (I recommend every 4 hours)

**For Pipedrive:**
1. Generate an API token in Settings > Personal > API
2. Enter the token in Wicked Reports integrations
3. Map your pipeline stages to attribution stages
4. Configure contact and deal syncing

The key is mapping your deal stages correctly. I map "Marketing Qualified Lead" to the lead stage and "Closed Won" to the customer stage. Everything in between gets tracked as progression.

## Step 3: Connect Ad Platforms

Go to Integrations > Advertising Platforms and connect each platform you're running ads on.

**Facebook/Meta:**
1. Connect your Facebook Ads Manager account
2. Select the ad accounts you want to track
3. Enable auto-tagging (adds fbclid parameter)
4. Set up offline conversion matching using email addresses

**Google Ads:**
1. Connect your Google Ads account via Google sign-in
2. Enable auto-tagging in Google Ads settings
3. Configure Enhanced Conversions for better matching
4. Link Google Analytics if you're using it

**LinkedIn:**
1. Connect via LinkedIn Campaign Manager
2. Enable auto-tagging (adds li_fat_id parameter)
3. Configure conversion tracking for lead forms and website visits

**TikTok:**
1. Connect TikTok Ads Manager
2. Enable auto-tagging (adds ttclid parameter)
3. Set up TikTok Pixel integration if you haven't already

Each platform connection allows Wicked Reports to import cost data and match it with conversion data from your CRM.

## Step 4: Configure URL Parameter Tracking

Wicked Reports automatically captures UTM parameters, but you need to configure platform-specific parameters for better attribution accuracy.

In Settings > Tracking Configuration, set up these parameter mappings:

```
UTM Source Mapping:
- utm_source → Source
- utm_medium → Medium  
- utm_campaign → Campaign
- utm_content → Ad Content
- utm_term → Keyword

Platform Parameters:
- fbclid → Facebook Click ID
- gclid → Google Click ID
- li_fat_id → LinkedIn Click ID
- ttclid → TikTok Click ID
- msclkid → Microsoft Click ID
```

For campaigns without auto-tagging, use this UTM structure:

```
https://yoursite.com/landing-page?utm_source=facebook&utm_medium=cpc&utm_campaign=q1-lead-gen&utm_content=video-ad-v2&utm_term=marketing-software
```

I recommend using consistent naming conventions across all platforms. Use lowercase, hyphens instead of spaces, and descriptive campaign names.

## Step 5: Set Up Attribution Models

In Attribution Settings, configure your attribution model. For B2B multi-channel attribution, I typically use these settings:

- **Attribution Window:** 90 days (B2B sales cycles are longer)
- **Model:** Time Decay (gives more credit to recent touchpoints)
- **Cross-device matching:** Email-based
- **Conversion lag reporting:** 30-day lookback

If you have shorter sales cycles (under 30 days), use a 30-day attribution window with Last-Click or Linear attribution.

Configure your funnel stages to match your sales process:

1. **Visitor:** Anyone who hits your website
2. **Lead:** Form submission or email capture
3. **Marketing Qualified Lead:** Meets scoring criteria
4. **Sales Qualified Lead:** Sales team accepts
5. **Opportunity:** Deal created in CRM
6. **Customer:** Closed won deal

## Testing & Verification

Test the pixel installation by visiting your website and checking the Wicked Reports Live Visitor Stream. You should see your visit appear within 30 seconds.

Verify CRM integration by creating a test deal in your CRM with a known email address. The deal should appear in Wicked Reports within 4 hours (or whatever sync frequency you set).

Check attribution accuracy by comparing a recent campaign's performance:
- Wicked Reports attributed conversions vs. ad platform reported conversions
- Revenue attribution vs. CRM deal amounts
- Lead attribution vs. form submission counts

Acceptable variances:
- **Lead count variance:** 5-15% (due to bot traffic and attribution windows)
- **Revenue variance:** 10-25% (due to attribution model differences)
- **Click variance:** 15-30% (Wicked Reports focuses on unique visitors, not total clicks)

Red flags that indicate broken attribution:
- Zero attributed conversions despite active campaigns
- Massive spikes in "Direct" traffic (usually indicates broken UTM tagging)
- Revenue attribution not matching CRM deal amounts
- No cross-platform attribution showing (indicates parameter tracking issues)

## Troubleshooting

**Problem:** CRM deals aren't showing up in attribution reports
The sync is probably broken. Check Integrations > CRM Status for error messages. Most common issue is expired API tokens or changed field permissions. Re-authenticate the integration and verify the mapped fields still exist in your CRM.

**Problem:** Facebook attribution shows zero conversions despite pixel firing
Offline conversion matching is failing. Go to Facebook integration settings and verify your customer match rate. If it's below 50%, you need better email hygiene or additional matching parameters like phone numbers.

**Problem:** Attribution reports show everything as "Direct" traffic
Your UTM parameters aren't being captured properly. Check that auto-tagging is enabled on all ad platforms and verify the pixel is firing on all landing pages. Use the Live Visitor Stream to see what parameters are being captured in real-time.

**Problem:** Revenue attribution is drastically different from CRM reports
Your deal stage mapping is wrong. Check that "Closed Won" deals in your CRM are mapping to the "Customer" stage in Wicked Reports. Also verify that deal amounts are syncing correctly - some CRMs use different currency fields.

**Problem:** Cross-device attribution isn't working
Email matching is the weak link. Wicked Reports relies on email addresses to connect devices. If your forms don't capture emails or if people use different emails on different devices, attribution breaks down. Consider implementing a customer ID system or phone number matching.

**Problem:** LinkedIn attribution shows zero despite confirmed clicks
LinkedIn's li_fat_id parameter expires quickly and doesn't always append. Enable LinkedIn Insight Tag alongside Wicked Reports tracking and verify that LinkedIn Campaign Manager is properly connected. Also check that your LinkedIn ads are driving traffic to UTM-tagged URLs as a backup.

## What To Do Next

Now that you have multi-channel attribution set up, you need to optimize based on the data. Check out our [Attribution Strategy Guide](/attribution) for advanced techniques and model optimization.

For enterprise setups or if you're dealing with complex B2B sales cycles, our [Attribution Setup Service](/services/attribution-setup) handles the entire configuration including custom CRM field mapping and advanced attribution modeling.

Ready to see what's actually driving your revenue? [Get a free tracking audit](/contact) where I'll analyze your current attribution setup and identify gaps in your multi-channel reporting.

*This guide is part of the [Attribution Tracking Hub](/attribution) — comprehensive guides for setting up attribution across all major platforms and tools.*