---
title: "How to Track WPForms Conversions in LinkedIn Ads (2026 Guide)"
slug: "wpforms-linkedin-ads-conversion-tracking"
description: "Step-by-step guide to tracking WPForms form submissions as conversions in LinkedIn Ads. Covers GTM setup, Client-Side GTM, testing, and troubleshooting."
category: "tracking"
date: "2026-03-24"
hub_page: "/tracking/linkedin-ads-conversion-tracking"
page_type: "spoke"
---

# WPForms + LinkedIn Ads Conversion Tracking Setup

I see this combo in about 25% of B2B accounts I audit, and here's the thing — most setups are capturing maybe 60-70% of actual conversions. The `wpformsAjaxSubmitSuccess` event fires perfectly, but people either miss it entirely or set up the LinkedIn Insight Tag conversion wrong. LinkedIn's tracking is less forgiving than Google or Meta, so small mistakes kill your data.

The most common issue? The conversion action gets created in LinkedIn Campaign Manager, but the GTM tag is firing the wrong event name or missing the conversion ID entirely. LinkedIn just silently drops those conversions.

## What You'll Have Working By The End

- WPForms submissions automatically tracked as LinkedIn Ads conversions
- Proper conversion attribution showing in LinkedIn Campaign Manager
- Cross-verification between WPForms entries and LinkedIn conversion counts
- Debug process to catch tracking failures before they cost you money
- Backup tracking method in case the primary setup breaks

## Prerequisites

- [ ] WPForms installed and active on your WordPress site (Lite version works fine)
- [ ] Google Tag Manager container installed on your site
- [ ] LinkedIn Ads account with Campaign Manager access
- [ ] LinkedIn Insight Tag base code already installed (if not, we'll add it)
- [ ] Admin access to create conversion actions in LinkedIn Campaign Manager

## Step 1: Create the LinkedIn Conversion Action

First, set up the conversion action in LinkedIn Campaign Manager. This gives you the conversion ID and event name you'll need for GTM.

1. Go to LinkedIn Campaign Manager → Analyze → Conversions
2. Click "Create Conversion"
3. Choose "Online Conversion"
4. Select "Event-based attribution" (not "Image pixel" — that's the old method)
5. Fill in your conversion details:
   - **Name**: "WPForms Lead" (or whatever makes sense for your business)
   - **Campaign Attribution**: 30-day view, 90-day click (LinkedIn default)
   - **Value**: Set if you assign lead values, otherwise leave at $1
6. Click "Create Conversion"

LinkedIn will generate a conversion ID (looks like `12345678`) and event name. Copy both — you'll need them for GTM.

The event name will be something like `lead` or `signup`. Don't change it unless you have a specific reason. LinkedIn's tracking is pickier than Google's about event name matching.

## Step 2: Install LinkedIn Insight Tag Base Code (If Needed)

If you don't already have LinkedIn Insight Tag on your site, add it through GTM first. Skip this if it's already installed.

1. In LinkedIn Campaign Manager, go to Account Assets → Insight Tag
2. Copy your Partner ID (8-digit number)
3. In GTM, create a new tag:
   - **Tag Type**: Custom HTML
   - **HTML**: 
   ```html
   <script type="text/javascript">
   _linkedin_partner_id = "YOUR_PARTNER_ID";
   window._linkedin_data_partner_ids = window._linkedin_data_partner_ids || [];
   window._linkedin_data_partner_ids.push(_linkedin_partner_id);
   </script>
   <script type="text/javascript">
   (function(l) {
   if (!l){window.lintrk = function(a,b){window.lintrk.q.push([a,b])};
   window.lintrk.q=[]}
   var s = document.getElementsByTagName("script")[0];
   var b = document.createElement("script");
   b.type = "text/javascript";b.async = true;
   b.src = "https://snap.licdn.com/li.js";
   s.parentNode.insertBefore(b, s);})(window.lintrk);
   </script>
   ```
4. Replace `YOUR_PARTNER_ID` with your actual Partner ID
5. **Trigger**: All Pages
6. Save and publish

## Step 3: Set Up WPForms Data Layer Event

WPForms fires `wpformsAjaxSubmitSuccess` when a form submits successfully. We need to catch this and push it to the data layer for GTM.

Add this code to your theme's `functions.php` file or in a custom plugin:

```javascript
<script>
jQuery(document).ready(function($) {
    $(document).on('wpformsAjaxSubmitSuccess', function(e, data) {
        // Push to data layer for GTM
        window.dataLayer = window.dataLayer || [];
        window.dataLayer.push({
            'event': 'wpforms_conversion',
            'form_id': data.form_id,
            'form_name': data.form_name || 'WPForms Lead',
            'entry_id': data.entry_id
        });
        
        // Also fire LinkedIn conversion directly (backup method)
        if (typeof window.lintrk !== 'undefined') {
            window.lintrk('track', { conversion_id: YOUR_CONVERSION_ID });
        }
    });
});
</script>
```

Replace `YOUR_CONVERSION_ID` with the actual conversion ID from Step 1.

**Alternative method**: If you can't edit your theme files, add this through GTM as a Custom HTML tag that fires on All Pages. Wrap it in `<script>` tags and it'll work the same way.

## Step 4: Create GTM Trigger for WPForms Submissions

1. In GTM, go to Triggers → New
2. **Trigger Type**: Custom Event
3. **Event Name**: `wpforms_conversion`
4. **This trigger fires on**: All Custom Events
5. Name it "WPForms - Conversion"
6. Save

The trigger will fire every time someone submits any WPForms form. If you only want to track specific forms, add a condition:
- **Some Custom Events**
- **form_id** equals **123** (replace with your form ID)

## Step 5: Create LinkedIn Conversion Tag in GTM

1. Go to Tags → New
2. **Tag Type**: Custom HTML
3. **HTML**:
   ```html
   <script>
   window.lintrk('track', { 
       conversion_id: {{LinkedIn Conversion ID}}
   });
   </script>
   ```
4. **Firing Triggers**: Select your "WPForms - Conversion" trigger
5. Name it "LinkedIn Ads - WPForms Conversion"

**Create the Conversion ID variable**: Go to Variables → New → Constant → Value: `12345678` (your actual conversion ID). Name it "LinkedIn Conversion ID".

This approach lets you reuse the conversion ID across multiple tags if needed.

## Step 6: Testing & Verification

### Test in GTM Preview Mode

1. Enable Preview Mode in GTM
2. Go to a page with your WPForms form
3. Fill out and submit the form
4. In GTM Preview, check:
   - "WPForms - Conversion" trigger fired
   - "LinkedIn Ads - WPForms Conversion" tag fired
   - Data layer shows the `wpforms_conversion` event with correct form_id

### Verify in LinkedIn Campaign Manager

1. Go to LinkedIn Campaign Manager → Analyze → Conversions
2. Click on your conversion action
3. Check "Recent Activity" tab — conversions should appear within 30 minutes
4. Click "Test Conversion" to see if your pixel is firing

**Note**: LinkedIn's real-time reporting is slower than Google or Meta. Give it 2-4 hours for conversions to show up in campaign reporting.

### Cross-Check the Numbers

After 24-48 hours, compare:
- **WPForms entries**: WordPress Admin → WPForms → Entries
- **LinkedIn conversions**: Campaign Manager → Campaigns → Conversions column

Expect 5-15% variance. LinkedIn tracks users who came from LinkedIn ads and later converted, while WPForms counts all submissions. If you're seeing 30%+ difference, something's broken.

## Troubleshooting

**Problem**: GTM trigger fires but no conversions in LinkedIn Campaign Manager
The LinkedIn Insight Tag base code isn't installed or the `lintrk` function isn't available when your conversion tag fires. Check browser console for `lintrk is not defined` errors. Make sure your base code tag has a higher priority (lower number) than your conversion tag.

**Problem**: Conversions show in "Recent Activity" but not in campaign reporting
LinkedIn's attribution window hasn't matched the conversions to ad clicks yet. Wait 48 hours. If they still don't appear, check that your campaigns are targeting the same audience that's converting. LinkedIn only attributes conversions to users who saw/clicked your ads.

**Problem**: Multiple conversions firing for the same form submission
WPForms can fire `wpformsAjaxSubmitSuccess` multiple times if users click submit repeatedly. Add a conversion flag to prevent duplicate tracking:

```javascript
$(document).on('wpformsAjaxSubmitSuccess', function(e, data) {
    if (data.entry_id && window.wpforms_tracked_entries) {
        if (window.wpforms_tracked_entries.includes(data.entry_id)) {
            return; // Already tracked
        }
        window.wpforms_tracked_entries.push(data.entry_id);
    }
    // Continue with tracking code...
});
```

**Problem**: Form submissions work but LinkedIn Insight Tag shows "No recent conversions"
Your conversion ID in the GTM tag doesn't match the ID from LinkedIn Campaign Manager. Double-check both numbers. LinkedIn conversion IDs are 8-10 digits, not the shorter campaign IDs.

**Problem**: WPForms AJAX isn't working, form redirects instead of showing success message
Your theme or another plugin is interfering with WPForms AJAX. The `wpformsAjaxSubmitSuccess` event won't fire. Switch to tracking the form's redirect page instead, or use the direct jQuery form submit handler:

```javascript
$('form[id^="wpforms-form-"]').on('submit', function() {
    var formId = $(this).attr('id').split('-').pop();
    // Add small delay to ensure form validates
    setTimeout(function() {
        window.dataLayer.push({
            'event': 'wpforms_conversion',
            'form_id': formId
        });
    }, 500);
});
```

**Problem**: Tracking works in test but stops working after GTM publish
You're in a different GTM workspace or container. Make sure you're publishing from the same workspace where you created the tags. Check that your live site is using the correct GTM container ID.

## What To Do Next

Once your WPForms → LinkedIn tracking is solid, consider these related setups:

- Set up [WPForms to Google Ads conversion tracking](/tracking/wpforms-google-ads-conversion-tracking) for cross-platform attribution
- Add [WPForms to GA4 conversion tracking](/tracking/wpforms-ga4-conversion-tracking) for better funnel analysis
- Connect [WPForms to HubSpot](/integrations/wpforms-to-hubspot) to get your leads into your CRM automatically
- Get a [free tracking audit](/contact) to catch issues you might be missing across all your platforms

*This guide is part of the [LinkedIn Ads Conversion Tracking hub](/tracking/linkedin-ads-conversion-tracking) — covering every major form tool, CRM, and ecommerce platform for LinkedIn attribution.*