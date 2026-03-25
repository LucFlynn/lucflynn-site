---
title: "How to Track WPForms Conversions in GA4 (2026 Guide)"
slug: "wpforms-ga4-conversion-tracking"
description: "Step-by-step guide to tracking WPForms form submissions as conversions in GA4. Covers GTM setup, Client-Side GTM, testing, and troubleshooting."
category: "tracking"
date: "2026-03-24"
hub_page: "/tracking/ga4-conversion-tracking"
page_type: "spoke"
---

# WPForms + GA4 Conversion Tracking Setup

I audit about 30-40 WordPress sites with WPForms every month, and roughly 60% of them have broken or missing GA4 conversion tracking. The most common issue? They're relying on basic GA4 auto-tracking that misses AJAX form submissions, or they set up a custom event but never marked it as a conversion in GA4.

WPForms fires a clean `wpformsAjaxSubmitSuccess` event that makes tracking straightforward once you know what to listen for.

## What You'll Have Working By The End

- WPForms submissions automatically sending conversion events to GA4
- Clean event data with form ID and entry ID for proper attribution
- Conversion events properly marked in GA4 for reporting and Google Ads import
- Cross-verification system between WPForms entries and GA4 conversion counts
- Debug setup to catch tracking failures in real-time

## Prerequisites

- [ ] WPForms installed and active on your WordPress site (Lite version works fine)
- [ ] Google Tag Manager container installed on your site
- [ ] GA4 property set up and connected to GTM
- [ ] Admin access to your GA4 property (needed to mark events as conversions)
- [ ] At least one published form to test with

## Step 1: Set Up the WPForms Event Listener

WPForms fires `wpformsAjaxSubmitSuccess` after successful form submissions. You need to catch this event and push clean data to the data layer.

Add this code to your theme's functions.php file or in a custom plugin:

```php
function wpforms_ga4_tracking() {
    ?>
    <script>
    jQuery(document).ready(function($) {
        // Listen for WPForms AJAX success event
        $(document).on('wpformsAjaxSubmitSuccess', function(event, formData, response) {
            // Extract form information
            var formId = response.data.form_id || 'unknown';
            var entryId = response.data.entry_id || 'unknown';
            var formTitle = $('#wpforms-' + formId + ' .wpforms-head-title').text() || 'WPForms Submission';
            
            // Push to data layer for GTM
            window.dataLayer = window.dataLayer || [];
            window.dataLayer.push({
                'event': 'wpforms_submission',
                'form_id': formId,
                'entry_id': entryId,
                'form_title': formTitle,
                'conversion_value': 1
            });
            
            // Debug log (remove in production)
            console.log('WPForms submission tracked:', {
                form_id: formId,
                entry_id: entryId,
                form_title: formTitle
            });
        });
    });
    </script>
    <?php
}
add_action('wp_footer', 'wpforms_ga4_tracking');
```

This code fires after every successful WPForms submission and sends clean data to GTM.

## Step 2: Create the GTM Trigger

In Google Tag Manager:

1. Go to **Triggers** → **New**
2. Name it "WPForms Submission"
3. Choose **Custom Event** as trigger type
4. Event name: `wpforms_submission`
5. Leave "This trigger fires on" set to "All Custom Events"
6. **Save**

The trigger will fire every time someone submits any WPForms form on your site.

## Step 3: Set Up Data Layer Variables

Create these variables in GTM to capture the form data:

**Form ID Variable:**
1. **Variables** → **New** → **Data Layer Variable**
2. Name: "WPForms - Form ID"
3. Data Layer Variable Name: `form_id`
4. **Save**

**Entry ID Variable:**
1. **Variables** → **New** → **Data Layer Variable**
2. Name: "WPForms - Entry ID"
3. Data Layer Variable Name: `entry_id`
4. **Save**

**Form Title Variable:**
1. **Variables** → **New** → **Data Layer Variable**
2. Name: "WPForms - Form Title"
3. Data Layer Variable Name: `form_title`
4. **Save**

## Step 4: Create the GA4 Event Tag

1. Go to **Tags** → **New**
2. Name it "GA4 - WPForms Conversion"
3. Choose **Google Analytics: GA4 Event** as tag type
4. Configuration Tag: Select your GA4 Configuration tag
5. Event Name: `generate_lead` (recommended event) or `wpforms_submission` (custom)
6. Add these Event Parameters:
   - `form_id`: `{{WPForms - Form ID}}`
   - `entry_id`: `{{WPForms - Entry ID}}`
   - `form_title`: `{{WPForms - Form Title}}`
   - `value`: `1`
7. Triggering: Select "WPForms Submission" trigger
8. **Save**

I recommend using `generate_lead` since it's a Google-recommended event that works well for form submissions and automatically imports to Google Ads.

## Step 5: Mark Events as Conversions in GA4

After publishing your GTM changes:

1. Go to your GA4 property
2. Navigate to **Configure** → **Events**
3. Wait for your event to appear (submit a test form first)
4. Find your event (`generate_lead` or `wpforms_submission`)
5. Toggle on "Mark as conversion"

The conversion will now show up in GA4 reports and be available for Google Ads import.

## Step 6: Test Client-Side Tracking

**Test the Data Layer Push:**
1. Open your site in Chrome
2. Open Developer Tools → Console
3. Submit a form
4. Look for the console.log output showing form data
5. Check `dataLayer` in console - you should see the wpforms_submission event

**Test GTM Firing:**
1. Enable GTM Preview mode
2. Submit a test form
3. Check that "WPForms Submission" trigger fires
4. Verify the GA4 tag fires with correct parameters

**Test GA4 Reception:**
1. Go to GA4 → **Configure** → **DebugView**
2. Submit a test form
3. Look for `generate_lead` event with your form parameters
4. Check **Reports** → **Realtime** → **Events** for the conversion

## Testing & Verification

**Source of Truth Check:**
Compare WPForms entries to GA4 conversions weekly. Go to **WPForms** → **Entries** and count submissions, then check GA4 **Reports** → **Events** for the same date range.

**Acceptable Variance:**
- 5-10% variance is normal (users with JavaScript disabled, ad blockers)
- 15-20% variance suggests tracking issues
- 30%+ variance means something is broken

**Red Flags:**
- No events showing in GA4 DebugView after form submission
- Events firing but no form_id parameter captured
- Multiple events firing for single form submission
- Zero conversions in GA4 but confirmed form submissions

## Troubleshooting

**Problem:** Events not firing in GA4 DebugView
Check that jQuery is loaded before your tracking code. WPForms requires jQuery for the AJAX success event. Add this check to your functions.php:

```php
function check_jquery_for_wpforms() {
    if (!wp_script_is('jquery', 'enqueued')) {
        wp_enqueue_script('jquery');
    }
}
add_action('wp_enqueue_scripts', 'check_jquery_for_wpforms');
```

**Problem:** form_id showing as "unknown" in GA4
The WPForms response object structure changed. Update the form ID extraction:

```javascript
var formId = response.data.form_id || response.form_id || event.target.getAttribute('id').replace('wpforms-form-', '') || 'unknown';
```

**Problem:** Multiple events firing for one submission
WPForms triggers multiple success events in some configurations. Add a debounce mechanism:

```javascript
var submittedForms = [];
$(document).on('wpformsAjaxSubmitSuccess', function(event, formData, response) {
    var formId = response.data.form_id;
    var entryId = response.data.entry_id;
    var uniqueId = formId + '-' + entryId;
    
    if (submittedForms.includes(uniqueId)) {
        return; // Already tracked this submission
    }
    submittedForms.push(uniqueId);
    
    // Your tracking code here...
});
```

**Problem:** Conversions not showing in GA4 reports
Events fire but don't show as conversions. Check that you marked the event as a conversion in GA4 **Configure** → **Events**. It can take 24-48 hours to appear in standard reports after marking.

**Problem:** Tracking breaks after WPForms plugin update
Plugin updates sometimes change the AJAX response structure. Check the browser console for JavaScript errors and verify the response object structure:

```javascript
$(document).on('wpformsAjaxSubmitSuccess', function(event, formData, response) {
    console.log('Full response object:', response);
    // Then update your form_id extraction based on the actual structure
});
```

**Problem:** Contact Form 7 events firing instead of WPForms
If you have both plugins installed, make sure you're listening for the correct event. Contact Form 7 uses different events that can interfere with tracking.

## What To Do Next

- Set up [WPForms Google Ads conversion tracking](/tracking/wpforms-google-ads-conversion-tracking) to capture paid search conversions
- Configure [WPForms Meta Ads tracking](/tracking/wpforms-meta-ads-conversion-tracking) for Facebook campaign attribution  
- Connect [WPForms to HubSpot](/integrations/wpforms-to-hubspot) to automatically create contacts from form submissions
- Book a [free tracking audit](/contact) to verify your setup and identify other conversion tracking gaps

*This guide is part of the [GA4 Conversion Tracking Hub](/tracking/ga4-conversion-tracking) — complete setup guides for tracking form submissions, purchases, and custom events as GA4 conversions.*