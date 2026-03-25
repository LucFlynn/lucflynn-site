---
title: "How to Track Elementor Forms Conversions in GA4 (2026 Guide)"
slug: "elementor-forms-ga4-conversion-tracking"
description: "Step-by-step guide to tracking Elementor Forms form submissions as conversions in GA4. Covers GTM setup, Client-Side GTM, testing, and troubleshooting."
category: "tracking"
date: "2026-03-24"
hub_page: "/tracking/ga4-conversion-tracking"
page_type: "spoke"
---

# Elementor Forms + GA4 Conversion Tracking Setup

I audit about 30-40 Elementor sites per year, and roughly 60% of them have broken GA4 conversion tracking for their forms. The most common issue? They're relying on Elementor's built-in Google Analytics integration, which doesn't fire the events GA4 actually needs for conversion tracking. You end up with form submissions in your WordPress dashboard but zero conversions in GA4.

The second most common mistake is setting up the GTM trigger to fire on *any* form submission instead of specifically targeting Elementor forms. This creates false positives when users submit search forms or newsletter signups.

## What You'll Have Working By The End

- Elementor Forms submissions automatically tracked as `generate_lead` events in GA4
- Those events marked as conversions in GA4 (ready for Google Ads import)
- Clean event data with form name and page path in GA4
- Accurate cross-referencing between Elementor's submission count and GA4's conversion count
- Debug process to catch issues before they mess up your data

## Prerequisites

- [ ] Elementor Pro installed and active (free version doesn't include Forms widget)
- [ ] Google Tag Manager container installed on your WordPress site
- [ ] GA4 property connected to your GTM container
- [ ] Admin access to both GTM and GA4
- [ ] At least one Elementor form published and receiving submissions

## Step 1: Set Up the Data Layer Push in GTM

Elementor Forms fires a JavaScript event when forms are submitted, but it doesn't automatically push to the data layer. We need to create a Custom HTML tag that listens for Elementor's form submission event and pushes the data GTM needs.

In GTM, create a new **Custom HTML** tag with this code:

```javascript
<script>
jQuery(document).on('submit_success', '.elementor-form', function(e, response) {
  // Get form details
  var formElement = jQuery(this);
  var formName = formElement.find('input[name="form_name"]').val() || 'Unknown Form';
  var formId = formElement.closest('.elementor-element').data('id') || 'unknown';
  
  // Push to data layer
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({
    'event': 'elementor_form_submit',
    'form_name': formName,
    'form_id': formId,
    'form_source': 'elementor'
  });
});
</script>
```

Set this tag to fire on **All Pages** and name it "Elementor Forms - Data Layer Push".

## Step 2: Create the GTM Trigger

Create a **Custom Event** trigger in GTM:
- **Event name**: `elementor_form_submit`
- **This trigger fires on**: All Custom Events

Name it "Elementor Form Submission".

## Step 3: Set Up Data Layer Variables

Create these **Data Layer Variable** in GTM:
- **Variable Name**: "DLV - Form Name"
- **Data Layer Variable Name**: `form_name`

Create another:
- **Variable Name**: "DLV - Form ID"  
- **Data Layer Variable Name**: `form_id`

## Step 4: Create the GA4 Event Tag

Create a new **GA4 Event** tag:
- **Configuration Tag**: Select your GA4 Configuration tag
- **Event Name**: `generate_lead`
- **Event Parameters**:
  - `form_name`: `{{DLV - Form Name}}`
  - `form_id`: `{{DLV - Form ID}}`
  - `form_source`: `elementor`

**Triggering**: Select your "Elementor Form Submission" trigger.

Name this tag "GA4 - Elementor Form Conversion".

## Step 5: Mark the Event as a Conversion in GA4

In your GA4 property:
1. Go to **Configure** → **Events**
2. Find the `generate_lead` event (you may need to wait 24-48 hours for it to appear after your first test submission)
3. Toggle the **Mark as conversion** switch to ON

If you want to use a custom event name instead of `generate_lead`, that works too — just make sure to mark whatever event name you choose as a conversion.

## Step 6: Configure Elementor Form Actions (Optional but Recommended)

In your Elementor form settings, under **Actions After Submit**:
- Keep **Email** and **Email 2** if you're using them
- **Don't** add the built-in "Google Analytics" action — it conflicts with our GTM setup
- If you need a thank you page redirect, use the **Redirect** action

## Testing & Verification

### Test in GTM Preview Mode
1. Enable **Preview** mode in GTM
2. Submit your Elementor form
3. In the GTM preview panel, look for the `elementor_form_submit` event
4. Verify that your "GA4 - Elementor Form Conversion" tag fired
5. Check that the form_name and form_id variables populated correctly

### Test in GA4 DebugView
1. In GA4, go to **Configure** → **DebugView**
2. Submit your form again
3. Look for the `generate_lead` event
4. Verify the event parameters (form_name, form_id, form_source) are coming through

### Test in GA4 Realtime
1. Go to **Reports** → **Realtime**  
2. Submit your form
3. You should see the conversion event appear within 30-60 seconds

### Cross-Reference Numbers
After 24-48 hours, compare:
- Elementor Forms submissions (WordPress Admin → Elementor → Submissions)
- GA4 conversions (GA4 → Reports → Engagement → Conversions)

Acceptable variance is 5-15%. Higher variance usually indicates duplicate firing or missed submissions.

## Troubleshooting

**Problem**: GTM preview shows the trigger fired but the GA4 tag didn't fire
→ Check that your GA4 Configuration tag is firing on the same pages. Most commonly, the GA4 config tag is set to fire on "All Pages" but excludes admin pages, while your form might be on a page that's being excluded.

**Problem**: GA4 DebugView shows the event but with empty form_name parameter
→ Elementor doesn't always set a form_name field. Edit your form in Elementor, go to **Content** → **Form Fields**, and make sure you've set a **Form Name** in the form settings (not individual field settings).

**Problem**: Multiple events firing for a single form submission
→ Your Custom HTML tag might be firing on multiple triggers. Check that it's only set to fire on "All Pages" and not on additional triggers. Also verify you don't have Elementor's built-in GA integration running simultaneously.

**Problem**: Events firing on other forms (contact forms, newsletter signups) on the same page
→ The `.elementor-form` selector should prevent this, but if you have other plugins that add this class, add a more specific selector: `.elementor-widget-form .elementor-form`

**Problem**: Form submissions showing in Elementor but zero GA4 conversions after 48 hours
→ Check that you marked `generate_lead` as a conversion in GA4. Events appear in DebugView and Realtime immediately, but only show up in the Conversions report after being marked as conversions.

**Problem**: jQuery is not defined error in browser console
→ Some WordPress themes don't load jQuery on all pages. Add this to the top of your Custom HTML tag:
```javascript
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
```

## What To Do Next

Once your Elementor Forms are tracking properly in GA4, you'll probably want to:
- [Set up Google Ads conversion tracking](/tracking/elementor-forms-google-ads-conversion-tracking) to import these conversions for bidding
- [Track Meta Ads conversions](/tracking/elementor-forms-meta-ads-conversion-tracking) if you're running Facebook/Instagram campaigns  
- [Connect Elementor Forms to HubSpot](/integrations/elementor-forms-to-hubspot) to get the leads into your CRM automatically

Not seeing the data you expected? I do free 15-minute tracking audits to diagnose what's broken. [Book one here](/contact) and I'll spot-check your setup.

*This guide is part of the [GA4 Conversion Tracking](/tracking/ga4-conversion-tracking) hub — complete setups for tracking any form or event as a GA4 conversion.*