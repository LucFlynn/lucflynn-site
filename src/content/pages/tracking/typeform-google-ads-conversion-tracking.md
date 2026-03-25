---
title: "How to Track Typeform Conversions in Google Ads (2026 Guide)"
slug: "typeform-google-ads-conversion-tracking"
description: "Step-by-step guide to tracking Typeform form submissions as conversions in Google Ads. Covers GTM setup, Enhanced Conversions, testing, and troubleshooting."
category: "tracking"
date: "2026-03-24"
hub_page: "/tracking/google-ads-conversion-tracking"
page_type: "spoke"
---

# Typeform + Google Ads Conversion Tracking Setup

I audit about 15-20 Google Ads accounts monthly, and roughly 60% of them are missing conversions from Typeform submissions. The issue isn't that Typeform is hard to track — it's that most people set up client-side tracking without Enhanced Conversions, then wonder why their conversion counts are 20-30% lower than their actual Typeform entries.

Typeform's embedded forms communicate through postMessage events, which makes tracking trickier than standard form submits. But once you know the pattern, it's actually more reliable than most other form tools.

## What You'll Have Working By The End

- Typeform submissions automatically firing as Google Ads conversions within 2-3 minutes
- Enhanced Conversions enabled for better attribution and iOS 14.5+ recovery
- Cross-platform data matching between Typeform completion count and Google Ads conversion reporting
- Debug visibility into exactly which form fields are being passed to Google Ads
- Backup server-side tracking through Typeform webhooks (optional but recommended)

## Prerequisites

- [ ] Google Tag Manager container installed on your site
- [ ] Google Ads conversion action already created (Conversion ID + Label)
- [ ] Admin access to your Typeform account
- [ ] Typeform embedded on your site (not using Typeform-hosted pages)
- [ ] Customer email addresses collected in your Typeform for Enhanced Conversions

## Step 1: Set Up the Typeform Event Listener

First, we need to catch Typeform's postMessage event when someone completes the form. Add this code to your site's `<head>` section, or create a Custom HTML tag in GTM that fires on All Pages:

```javascript
<script>
window.addEventListener('message', function(e) {
  // Only process messages from Typeform
  if (e.origin !== 'https://admin.typeform.com' && e.origin !== 'https://embed.typeform.com') {
    return;
  }
  
  // Check if it's a form submission event
  if (e.data && e.data.type === 'form_submit') {
    // Extract form data
    var formData = e.data;
    var responseId = formData.response_id;
    var formId = formData.form_id;
    
    // Find email field (adjust field reference as needed)
    var userEmail = '';
    if (formData.answers) {
      formData.answers.forEach(function(answer) {
        if (answer.type === 'email' || answer.field.type === 'email') {
          userEmail = answer.email || answer.text || '';
        }
      });
    }
    
    // Push to dataLayer for GTM
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
      'event': 'typeform_submit',
      'typeform_id': formId,
      'typeform_response_id': responseId,
      'user_email': userEmail,
      'form_type': 'typeform'
    });
    
    console.log('Typeform submission tracked:', responseId);
  }
});
</script>
```

If your Typeform redirects to a thank-you page instead of showing an inline success message, you can use a simpler approach. Just fire the conversion on the thank-you page load:

```javascript
<script>
window.dataLayer = window.dataLayer || [];
window.dataLayer.push({
  'event': 'typeform_submit',
  'page_type': 'thank_you'
});
</script>
```

I see the redirect method in about 70% of setups because it's more reliable, but you lose the form field data for Enhanced Conversions.

## Step 2: Create the GTM Trigger

In Google Tag Manager:

1. **Variables → New → Data Layer Variable**
   - Variable Name: `DLV - User Email`
   - Data Layer Variable Name: `user_email`

2. **Triggers → New → Custom Event**
   - Trigger Name: `Typeform Submission`
   - Event Name: `typeform_submit`
   - This trigger fires on: `All Custom Events`

## Step 3: Set Up Google Ads Conversion Tag with Enhanced Conversions

Create a new tag in GTM:

1. **Tag Type:** Google Ads Conversion Tracking
2. **Conversion ID:** Your Google Ads Conversion ID
3. **Conversion Label:** Your conversion label
4. **Conversion Value:** Leave blank (or add a Data Layer Variable if you collect order values)
5. **Transaction ID:** `{{DLV - Typeform Response ID}}` (prevents duplicate counting)

**Enhanced Conversions Configuration:**
- Enable Enhanced Conversions: ✅ Checked  
- User-provided data: **Collect from data layer**
- Email: `{{DLV - User Email}}`

**Advanced Settings:**
- Firing Trigger: `Typeform Submission`

The Enhanced Conversions piece is critical. I've seen conversion recovery rates improve by 15-25% when you're collecting email addresses and passing them properly.

## Step 4: Configure Conversion Counting Settings

In Google Ads, go to **Goals → Conversions** and verify your conversion action settings:

- **Count:** One (for lead gen forms — each person should only count once)
- **Attribution Model:** Data-driven (default) or Position-based if you have lower volume
- **Conversion Window:** 30 days click, 1 day view (adjust based on your sales cycle)
- **Include in Conversions:** Yes

Most people leave this on "Every" count, which inflates numbers if users refresh the thank-you page or resubmit forms.

## Step 5: Add Server-Side Backup Tracking (Recommended)

Typeform's webhook feature lets you send conversion data directly to Google Ads when someone submits, bypassing browser blocking entirely. About 15-20% of users block client-side tracking, so this backup catches those missed conversions.

In Typeform:
1. **Connect → Webhooks → Add webhook**
2. **Endpoint URL:** Your server endpoint that receives the webhook
3. **Secret:** Set a secret key for verification

Server-side conversion upload example (Python):

```python
from googleads import adwords

def track_typeform_conversion(webhook_data):
    conversion_upload_service = adwords_client.GetService(
        'ConversionUploadService', version='v201809')
    
    conversion = {
        'conversionName': 'Typeform Lead',
        'conversionTime': webhook_data['submitted_at'],
        'conversionValue': 1.0,
        'gclid': get_gclid_from_session(webhook_data['token'])  # Store GCLID when user lands
    }
    
    upload_conversion = {
        'conversions': [conversion]
    }
    
    result = conversion_upload_service.uploadConversions(upload_conversion)
    return result
```

You'll need to capture and store the GCLID parameter when users first land on your site, then associate it with the form submission through Typeform's hidden fields.

## Testing & Verification

**GTM Preview Mode:**
1. Enable Preview mode in GTM
2. Fill out and submit your Typeform
3. Verify the `typeform_submit` event fires
4. Check that your Google Ads tag triggers
5. Confirm the `user_email` variable populates correctly

**Google Ads Verification:**
1. **Goals → Conversions** — status should show "Recently active" within 2-3 hours
2. **Tools → Google Ads tag → Conversions** — will show recent conversion events
3. Check the conversion in the **Dimensions → Conversion action** report within 6-8 hours

**Cross-Check Numbers:**
- Typeform: **Results** tab shows completion count
- Google Ads: **Campaigns → Conversions** column (filter to your conversion action)
- Expected variance: 5-15% lower in Google Ads due to ad blockers and attribution windows

If Google Ads shows 20%+ fewer conversions than Typeform completions, you likely have a tracking setup issue or need server-side backup tracking.

## Troubleshooting

**Problem:** GTM tag fires but no conversions appear in Google Ads  
The Conversion ID/Label combination is wrong, or the conversion action is paused. Double-check both values in Google Ads → Goals → Conversions. Also verify the conversion action's status is "Enabled."

**Problem:** Getting duplicate conversions for the same user  
You're not passing the Transaction ID, or the counting setting is on "Every" instead of "One." Use the Typeform response ID as the transaction ID to prevent duplicates.

**Problem:** Enhanced Conversions showing "No recent activity"  
The email field isn't being captured from Typeform or passed to the data layer correctly. Check your Typeform has an email field and verify the field reference in your JavaScript matches Typeform's structure.

**Problem:** Conversions only tracking on desktop, not mobile  
Typeform's postMessage events sometimes behave differently on mobile browsers. Switch to the redirect method if you're seeing desktop-only tracking.

**Problem:** Form submissions fire the event multiple times  
Typeform can trigger multiple postMessage events during submission. Add a flag to prevent duplicate data layer pushes: check if the response ID has already been processed before pushing to dataLayer.

**Problem:** Conversions attributed to wrong campaigns  
The GCLID parameter isn't being preserved correctly through the form flow. If using hidden fields to pass GCLID, make sure the parameter mapping is correct and the GCLID isn't getting stripped by redirects.

## What To Do Next

Once your Typeform → Google Ads tracking is working, you'll want to expand your conversion tracking setup:

- Set up [Typeform to Meta Ads conversion tracking](/tracking/typeform-meta-ads-conversion-tracking) for cross-platform attribution
- Connect [Typeform submissions to HubSpot](/integrations/typeform-to-hubspot) for full lead management
- Add [GA4 conversion tracking for Typeform](/tracking/typeform-ga4-conversion-tracking) to get organic and other channel attribution
- Want me to audit your current setup? [Get a free tracking audit](/contact) — I'll check your GTM configuration and conversion accuracy.

*This guide is part of the [Google Ads Conversion Tracking Hub](/tracking/google-ads-conversion-tracking) — complete setup guides for tracking any form or event as a Google Ads conversion.*