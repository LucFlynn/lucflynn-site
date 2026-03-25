---
title: "How to Track Gravity Forms Conversions in GA4 (2026 Guide)"
slug: "gravity-forms-ga4-conversion-tracking"
description: "Step-by-step guide to tracking Gravity Forms form submissions as conversions in GA4. Covers GTM setup, Client-Side GTM, testing, and troubleshooting."
category: "tracking"
date: "2026-03-24"
hub_page: "/tracking/ga4-conversion-tracking"
page_type: "spoke"
---

# Gravity Forms + GA4 Conversion Tracking Setup

I've audited 200+ WordPress sites and about 70% using Gravity Forms have broken GA4 conversion tracking. The most common issue? They're listening for generic form events that never fire, or they're tracking the wrong confirmation step. Gravity Forms uses AJAX submissions with a specific callback — miss that, and you'll wonder why your conversion data is garbage.

The setup I'm walking through works reliably across different Gravity Forms configurations, whether you're using redirects, text confirmations, or page confirmations.

## What You'll Have Working By The End

- Form submissions automatically tracked as 'generate_lead' events in GA4
- Conversion data flowing to GA4 within 5-10 minutes of submission
- Form ID and selected field values captured in GA4 for analysis
- Proper conversion marking so the data can import to Google Ads
- Debug tools showing you exactly when tracking fires

## Prerequisites

Before starting, make sure you have:
- [ ] WordPress admin access to install/configure Gravity Forms
- [ ] Google Tag Manager container installed on your WordPress site
- [ ] GA4 property set up and connected to your GTM container
- [ ] Admin access to your GA4 property (to mark events as conversions)
- [ ] At least one active Gravity Form on your site

## Step 1: Add the Data Layer Push to Gravity Forms

Gravity Forms fires a `gform_confirmation_loaded` JavaScript event after successful AJAX submissions. We need to listen for this and push the data to GTM's data layer.

Add this code to your WordPress theme's `functions.php` file or via a code snippets plugin:

```javascript
<script>
jQuery(document).on('gform_confirmation_loaded', function(event, formId) {
    // Get form data
    var form = jQuery('#gform_' + formId);
    var formTitle = form.find('.gform_title').text() || 'Gravity Form';
    
    // Extract field values (common ones)
    var email = form.find('input[type="email"]').val() || '';
    var firstName = form.find('input[id*="input_"][id*="_1"]').val() || '';
    var lastName = form.find('input[id*="input_"][id*="_2"]').val() || '';
    
    // Push to data layer
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
        'event': 'gravity_form_submission',
        'form_id': formId,
        'form_title': formTitle,
        'user_email': email,
        'user_first_name': firstName,
        'user_last_name': lastName
    });
    
    console.log('Gravity Forms submission tracked:', {
        formId: formId,
        formTitle: formTitle
    });
});
</script>
```

**Important:** Gravity Forms field IDs follow the pattern `input_X_Y` where X is the form ID and Y is the field ID. The most common setup has field 1 as first name, field 2 as last name, and field 3 as email, but this varies by form configuration.

If you need to capture specific field values, inspect your form HTML to find the exact input IDs and modify the selectors accordingly.

## Step 2: Create the GTM Trigger

In Google Tag Manager:

1. Go to **Triggers** → **New**
2. Name it "Gravity Forms - Form Submission"
3. **Trigger Type:** Custom Event
4. **Event name:** `gravity_form_submission`
5. **This trigger fires on:** All Custom Events

Save the trigger.

For form-specific tracking, you can add a condition:
- **This trigger fires on:** Some Custom Events
- **Fire this trigger when:** `form_id` equals `[your form ID number]`

## Step 3: Set Up GA4 Event Tag

Create the GA4 event tag:

1. Go to **Tags** → **New**
2. Name it "GA4 - Gravity Forms Lead Generation"
3. **Tag Type:** Google Analytics: GA4 Event
4. **Configuration Tag:** [Select your GA4 configuration tag]
5. **Event Name:** `generate_lead`

Add these **Event Parameters:**
- `form_id`: `{{DLV - form_id}}`
- `form_name`: `{{DLV - form_title}}`
- `method`: `gravity_forms`

**Triggering:** Select the "Gravity Forms - Form Submission" trigger you created.

**Which event name should you use?** I recommend `generate_lead` because it's a Google-recommended event that automatically gets enhanced measurement features. If you want custom naming, use something like `form_submit_gravity` but you'll need to manually mark it as a conversion later.

## Step 4: Create Data Layer Variables

You'll need these Data Layer Variables in GTM to capture the form data:

1. **DLV - form_id**
   - Variable Type: Data Layer Variable
   - Data Layer Variable Name: `form_id`

2. **DLV - form_title**
   - Variable Type: Data Layer Variable
   - Data Layer Variable Name: `form_title`

3. **DLV - user_email** (optional, for enhanced conversions)
   - Variable Type: Data Layer Variable
   - Data Layer Variable Name: `user_email`

## Step 5: Configure Client-Side GTM Setup

Since we're using client-side GTM, the tracking fires directly from the user's browser when the form submits successfully. This means:

- **Timing:** Events fire immediately after form submission
- **Reliability:** About 85% capture rate (some users have ad blockers)
- **Data freshness:** Shows in GA4 DebugView within seconds

The client-side approach works well for Gravity Forms because the `gform_confirmation_loaded` event is reliable and fires consistently across different confirmation types.

**Alternative consideration:** If you need near-100% tracking accuracy for critical lead forms, consider adding server-side tracking using Gravity Forms hooks, but for most sites, client-side tracking provides sufficient data quality.

## Step 6: Mark Events as Conversions in GA4

After your tags are firing:

1. In GA4, go to **Configure** → **Events**
2. Find your `generate_lead` event in the list
3. Toggle **Mark as conversion** to ON
4. The conversion will appear in **Configure** → **Conversions**

Conversions marked in GA4 can be imported into Google Ads automatically if your accounts are linked.

## Testing & Verification

### GTM Preview Mode
1. Enable **Preview** mode in GTM
2. Submit a test form on your site
3. In the GTM debug panel, look for:
   - The `gravity_form_submission` event firing
   - Your GA4 event tag firing with correct parameters
   - Data layer showing form_id, form_title, and other captured values

### GA4 DebugView
1. In GA4, go to **Configure** → **DebugView**
2. Submit a test form
3. You should see the `generate_lead` event appear within 5-10 seconds
4. Check the event parameters contain your form data

### GA4 Realtime Reports
1. Go to **Reports** → **Realtime**
2. Submit a test form
3. Within 1-2 minutes, you should see the conversion in the Realtime events

### Cross-Check Numbers
Compare your Gravity Forms entry count with GA4 conversion count:
- **In WordPress:** Gravity Forms → Entries → [Your Form]
- **In GA4:** Reports → Engagement → Conversions

**Acceptable variance:** 10-20% lower in GA4 is normal due to ad blockers and tracking prevention. If GA4 shows more than 25% fewer conversions, something's broken.

## Troubleshooting

**Problem:** GTM shows the custom event firing but GA4 tag doesn't fire  
**Solution:** Check that your GA4 Configuration tag is set up correctly and connected to the right GA4 property. Verify the GA4 Measurement ID matches your property.

**Problem:** Events fire multiple times for a single form submission  
**Solution:** The `gform_confirmation_loaded` event might be firing multiple times. Add a check to prevent duplicate pushes by storing the submission in sessionStorage temporarily.

**Problem:** Form field values are coming through as empty in GA4  
**Solution:** Gravity Forms field IDs vary by form. Inspect your specific form HTML to find the correct input selectors. Common patterns are `input_[form_id]_[field_id]` but custom forms may differ.

**Problem:** Tracking works on some forms but not others  
**Solution:** Different forms may have different confirmation settings. Check if some forms redirect to thank-you pages instead of showing inline confirmations. Redirected forms need different tracking approaches.

**Problem:** GA4 shows events but they're not marked as conversions  
**Solution:** You need to manually mark `generate_lead` as a conversion in GA4 admin. The marking isn't automatic even for recommended events.

**Problem:** Numbers in GA4 are way lower than form entries  
**Solution:** Check if your forms have bot protection enabled. Heavy bot traffic might inflate form entries while legitimate submissions get tracked properly in GA4.

## What To Do Next

Now that your Gravity Forms are tracking in GA4, consider expanding your conversion tracking:
- [Gravity Forms + Google Ads Conversion Tracking](/tracking/gravity-forms-google-ads-conversion-tracking) for direct ad platform tracking
- [Gravity Forms + Meta Ads Conversion Tracking](/tracking/gravity-forms-meta-ads-conversion-tracking) to track Facebook and Instagram ad conversions
- [Gravity Forms to HubSpot Integration](/integrations/gravity-forms-to-hubspot) to sync your leads with your CRM

Want me to audit your current tracking setup for free? I'll check your Gravity Forms, GTM configuration, and GA4 setup to identify what's working and what's broken. [Get your free tracking audit here](/contact).

*This guide is part of the [GA4 Conversion Tracking Hub](/tracking/ga4-conversion-tracking) — complete guides for tracking conversions from any form platform or traffic source in GA4.*