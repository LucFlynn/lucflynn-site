---
title: "How to Track Gravity Forms Conversions in LinkedIn Ads (2026 Guide)"
slug: "gravity-forms-linkedin-ads-conversion-tracking"
description: "Step-by-step guide to tracking Gravity Forms form submissions as conversions in LinkedIn Ads. Covers GTM setup, Client-Side GTM, testing, and troubleshooting."
category: "tracking"
date: "2026-03-24"
hub_page: "/tracking/linkedin-ads-conversion-tracking"
page_type: "spoke"
---

# Gravity Forms + LinkedIn Ads Conversion Tracking Setup

I audit probably 20 WordPress sites every quarter, and about 60% of them run Gravity Forms. Most of those are trying to track form submissions in LinkedIn Ads, and I'd say 70% have it set up wrong. Either they're missing the conversion events entirely, or they're firing duplicates, or the data just doesn't match what's showing in their CRM.

The main issue I see is that people try to use LinkedIn's auto-conversion tracking or rely on UTM parameters instead of properly firing the LinkedIn Insight Tag conversion events. LinkedIn's tracking is less mature than Google or Meta, so you need to be more precise about when and how you fire those conversion pixels.

## What You'll Have Working By The End

- Gravity Forms submissions automatically firing LinkedIn Ads conversion events in real-time
- Clean conversion tracking that matches your actual form submission count (within 5-15% variance)
- Proper attribution back to your LinkedIn campaigns and ads
- Debug visibility so you can verify conversions are firing before they hit LinkedIn
- Conversion data flowing into LinkedIn Campaign Manager within 2-4 hours

## Prerequisites

- [ ] WordPress site with Gravity Forms plugin activated
- [ ] Google Tag Manager container installed on your site
- [ ] LinkedIn Ads account with conversion tracking enabled
- [ ] LinkedIn Insight Tag base code already installed (either via GTM or hardcoded)
- [ ] Admin access to your WordPress dashboard to view form entries
- [ ] At least Editor access to your GTM container

## Step 1: Set Up the Gravity Forms Data Layer Push

First, you need to push form submission data to the data layer when someone completes a Gravity Forms form. Add this code to your active theme's `functions.php` file or create a custom plugin:

```php
// Gravity Forms submission tracking for GTM
add_action('gform_after_submission', 'push_gf_conversion_to_datalayer', 10, 2);

function push_gf_conversion_to_datalayer($entry, $form) {
    // Only track specific forms - adjust form IDs as needed
    $tracked_forms = array(1, 2, 3); // Replace with your form IDs
    
    if (!in_array($form['id'], $tracked_forms)) {
        return;
    }
    
    ?>
    <script type="text/javascript">
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
        'event': 'gravity_form_submission',
        'form_id': '<?php echo esc_js($form['id']); ?>',
        'form_title': '<?php echo esc_js($form['title']); ?>',
        'conversion_value': <?php echo !empty($entry['payment_amount']) ? floatval($entry['payment_amount']) : 0; ?>,
        'user_email': '<?php echo esc_js(rgar($entry, '1')); ?>', // Adjust field ID
        'timestamp': '<?php echo date('Y-m-d H:i:s'); ?>'
    });
    </script>
    <?php
}
```

**Important:** Update the `$tracked_forms` array with your actual form IDs. You can find these in your WordPress admin under Forms → All Forms. Also adjust the email field ID (`'1'`) to match your actual email field number.

If you're using AJAX form submissions (which most Gravity Forms setups do), you might need this alternative approach that listens for the confirmation event:

```javascript
// Alternative for AJAX submissions - add to GTM custom HTML tag
document.addEventListener('DOMContentLoaded', function() {
    jQuery(document).on('gform_confirmation_loaded', function(event, formId) {
        // Only track specific forms
        var trackedForms = [1, 2, 3]; // Update with your form IDs
        
        if (trackedForms.indexOf(parseInt(formId)) === -1) {
            return;
        }
        
        window.dataLayer = window.dataLayer || [];
        window.dataLayer.push({
            'event': 'gravity_form_submission',
            'form_id': formId,
            'form_title': 'Contact Form', // Update as needed
            'conversion_value': 0,
            'timestamp': new Date().toISOString()
        });
    });
});
```

## Step 2: Create the GTM Trigger

In Google Tag Manager, create a new trigger for the form submissions:

1. **Trigger Type**: Custom Event
2. **Event Name**: `gravity_form_submission`
3. **This trigger fires on**: All Custom Events
4. **Trigger Name**: "GF - Form Submission"

If you want to track only specific forms, add a condition:
- **Fire On**: Some Custom Events
- **Condition**: `form_id` equals `1` (or whatever your target form ID is)

## Step 3: Set Up LinkedIn Insight Tag Conversion Event

Create a new tag in GTM for the LinkedIn conversion:

1. **Tag Type**: Custom HTML
2. **Tag Name**: "LinkedIn - Gravity Forms Conversion"
3. **HTML Code**:

```html
<script type="text/javascript">
window.lintrk = window.lintrk || function(a,b){window.lintrk.q.push([a,b])};
window.lintrk.q = window.lintrk.q || [];
window.lintrk('track', { conversion_id: YOUR_CONVERSION_ID });
</script>
```

Replace `YOUR_CONVERSION_ID` with the actual conversion ID from your LinkedIn Ads account. Find this under Campaign Manager → Analyze → Conversions → [Your Conversion] → Install Conversion Tracking.

For more advanced tracking with conversion values, use this version instead:

```html
<script type="text/javascript">
window.lintrk = window.lintrk || function(a,b){window.lintrk.q.push([a,b])};
window.lintrk.q = window.lintrk.q || [];

var conversionValue = {{conversion_value}} || 0; // GTM variable
window.lintrk('track', { 
    conversion_id: YOUR_CONVERSION_ID,
    conversion_value: conversionValue
});
</script>
```

4. **Triggering**: Select your "GF - Form Submission" trigger
5. **Advanced Settings → Tag Sequencing**: If you have the base LinkedIn Insight Tag, set this to fire after it

## Step 4: Create GTM Variables (Optional but Recommended)

Create these Data Layer Variables in GTM to make your setup more flexible:

- **Variable Name**: "DL - Form ID"
  - **Type**: Data Layer Variable
  - **Data Layer Variable Name**: `form_id`

- **Variable Name**: "DL - Form Title" 
  - **Type**: Data Layer Variable
  - **Data Layer Variable Name**: `form_title`

- **Variable Name**: "DL - Conversion Value"
  - **Type**: Data Layer Variable  
  - **Data Layer Variable Name**: `conversion_value`

You can then use these variables in your LinkedIn tag or create separate tags for different forms.

## Step 5: Configure Client-Side GTM Setup

Since LinkedIn's tracking relies on client-side pixels, you need to ensure your GTM container is firing client-side. Here's what to verify:

1. **Container Loading**: Your GTM container should load in the `<head>` of your site
2. **LinkedIn Base Tag**: Make sure the LinkedIn Insight Tag base code is installed. Add this to GTM as a Custom HTML tag if it's not already installed:

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
b.src = "https://snap.licdn.com/li.lms-analytics/insight.min.js";
s.parentNode.insertBefore(b, s);})(window.lintrk);
</script>
```

**Fire this tag on**: All Pages, with a trigger condition that it only fires once per session.

## Testing & Verification

### Test in GTM Preview Mode

1. Enable GTM Preview mode
2. Submit a test form on your site  
3. In the GTM debugger, verify you see:
   - The `gravity_form_submission` event firing
   - Your LinkedIn conversion tag firing after the event
   - The correct form_id and other data layer values

### Verify in LinkedIn Campaign Manager

1. Go to Campaign Manager → Analyze → Conversions
2. Select your conversion action
3. Check the "Recent Conversions" section (can take 2-4 hours to appear)
4. Look for test conversions with timestamps matching your tests

### Cross-Check the Numbers

Compare your conversion counts after 24-48 hours:
- **WordPress Admin**: Forms → Entries → [Your Form] (count total entries)
- **LinkedIn Ads**: Campaign Manager → Conversions (check total conversion count)

Acceptable variance is 5-15%. LinkedIn tends to de-duplicate some conversions and may miss some due to ad blockers (I see about 10-15% fewer LinkedIn conversions vs. actual form submissions).

## Troubleshooting

**Problem:** GTM shows the trigger firing but LinkedIn conversion tag doesn't fire
**Solution:** Check if you have the LinkedIn Insight Tag base code installed. The conversion events won't work without it. Also verify your conversion ID is correct and active.

**Problem:** LinkedIn shows conversions but they don't match form submission timing
**Solution:** You might have duplicate tracking. Check if LinkedIn auto-conversion tracking is enabled and disable it. Also check for hardcoded LinkedIn pixels on your thank you pages.

**Problem:** Conversions fire for AJAX forms but not regular submissions  
**Solution:** You're probably missing the `gform_after_submission` hook version of the code. AJAX and regular submissions need different JavaScript listeners. Use both the PHP hook and the `gform_confirmation_loaded` event listener.

**Problem:** Getting 0 conversion values even with payment forms
**Solution:** The `payment_amount` field might not exist in your form entry. Check your Gravity Forms field mapping and use the correct field ID for your price field, usually something like `rgar($entry, 'payment_amount')`.

**Problem:** Some forms track but others don't
**Solution:** Check your `$tracked_forms` array in the PHP code. Make sure all the form IDs you want to track are included, and verify the form IDs are correct (Forms → All Forms in WordPress admin).

**Problem:** LinkedIn reports much lower conversion count than WordPress entries
**Solution:** This is normal. LinkedIn deduplicates conversions within 30 days by default, and some users block LinkedIn tracking. If you're seeing more than 20% variance, check for JavaScript errors preventing the tag from firing.

## What To Do Next

Once your Gravity Forms → LinkedIn Ads tracking is working, consider these related setups:

- [Gravity Forms + Google Ads Conversion Tracking](/tracking/gravity-forms-google-ads-conversion-tracking) — Track the same forms in Google Ads for comparison
- [Gravity Forms + Meta Ads Conversion Tracking](/tracking/gravity-forms-meta-ads-conversion-tracking) — Add Facebook/Instagram tracking
- [Gravity Forms + GA4 Conversion Tracking](/tracking/gravity-forms-ga4-conversion-tracking) — Set up Google Analytics conversion tracking
- [Gravity Forms to HubSpot Integration](/integrations/gravity-forms-to-hubspot) — Automatically send form data to your CRM

Need help auditing your current tracking setup? [Get a free tracking audit](/contact) and I'll review your forms, ad platforms, and attribution setup.

*This guide is part of the [LinkedIn Ads Conversion Tracking Hub](/tracking/linkedin-ads-conversion-tracking) — complete setups for tracking LinkedIn Ads conversions from any form, CRM, or ecommerce platform.*