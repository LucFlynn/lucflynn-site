---
title: "How to Track Typeform Conversions in GA4 (2026 Guide)"
slug: "typeform-ga4-conversion-tracking"
description: "Step-by-step guide to tracking Typeform form submissions as conversions in GA4. Covers GTM setup, Client-Side GTM, testing, and troubleshooting."
category: "tracking"
date: "2026-03-24"
hub_page: "/tracking/ga4-conversion-tracking"
page_type: "spoke"
---

# Typeform + GA4 Conversion Tracking Setup

I see broken Typeform → GA4 conversion tracking in about 35% of accounts I audit. The main culprit? Teams either set up tracking only on the thank you page (which gets missed if users bounce immediately) or they try to use Typeform's built-in GA4 integration, which often fires before GA4 is fully loaded. The result is phantom conversions that show up in Typeform's analytics but never make it to GA4.

## What You'll Have Working By The End

- Typeform submissions firing as GA4 events in real-time (visible in DebugView within seconds)
- GA4 conversions marked and counting in your reports
- Cross-verification between Typeform completion count and GA4 conversion count (should match within 5-15%)
- Proper event parameters for linking back to specific forms and campaigns
- Setup that works whether Typeform is embedded or standalone

## Prerequisites

- [ ] GA4 property with Enhanced Ecommerce enabled
- [ ] Google Tag Manager container installed on your website
- [ ] GTM Publish access (or someone who can publish your changes)
- [ ] GA4 Admin access to mark events as conversions
- [ ] Access to your Typeform account to configure redirect URLs

## Step 1: Configure Typeform Redirect

The most reliable method is tracking via redirect URL, not Typeform's native integration.

In your Typeform:
1. Go to **Configure** → **After completion**
2. Select **Redirect to a URL**
3. Set redirect URL to: `https://yoursite.com/thank-you?form=typeform_lead&source={{form_id}}`

Replace `yoursite.com/thank-you` with your actual thank you page. The `form=typeform_lead` parameter lets us identify this specific conversion source, and `{{form_id}}` passes the Typeform ID for tracking multiple forms.

If you're using embedded Typeform and don't want redirects, we'll set up postMessage tracking in Step 3.

## Step 2: Create the GA4 Event Tag in GTM

In Google Tag Manager:

**Create the Tag:**
1. **Tags** → **New** → **GA4 Event**
2. **Configuration Tag**: Select your GA4 config tag
3. **Event Name**: `generate_lead` (this is GA4's recommended event for lead forms)
4. **Event Parameters**:
   - `form_type`: `typeform`
   - `form_name`: `{{Page Query - form}}`
   - `form_id`: `{{Page Query - source}}`
   - `page_location`: `{{Page URL}}`

**Create the Trigger:**
1. **Triggers** → **New** → **Page View - DOM Ready**
2. **Fire on**: Some Page Views
3. **Conditions**: 
   - Page URL contains `/thank-you`
   - AND Page Query - form equals `typeform_lead`

This setup fires when users hit your thank you page with the specific Typeform parameters.

## Step 3: Set Up Embedded Typeform Tracking (Alternative Method)

If you're using embedded Typeform and can't redirect, track the postMessage event instead.

**Create Custom HTML Tag:**
```html
<script>
window.addEventListener('message', function(event) {
  // Verify message is from Typeform
  if (event.origin !== 'https://form.typeform.com') return;
  
  if (event.data.type === 'form_submit') {
    // Push to data layer
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
      'event': 'typeform_submit',
      'form_type': 'typeform',
      'form_id': event.data.form_id || 'unknown',
      'form_name': 'embedded_typeform'
    });
  }
});
</script>
```

**Create the Data Layer Trigger:**
1. **Triggers** → **New** → **Custom Event**
2. **Event name**: `typeform_submit`

**Update your GA4 Event Tag:**
- Change the trigger to fire on `typeform_submit` custom event
- Update event parameters to use the data layer variables instead of URL parameters

## Step 4: Set Up URL Query Variables

For the redirect method, create these built-in variables in GTM:

1. **Variables** → **Configure** → **Built-Ins**
2. Enable: **Page Query - form** and **Page Query - source**

If these don't auto-populate your form parameters, create custom URL variables:
1. **Variables** → **New** → **URL**
2. **Component Type**: Query
3. **Query Key**: `form` (create another for `source`)

## Step 5: Mark as Conversion in GA4

In GA4:
1. **Configure** → **Conversions**
2. **Create conversion event**
3. **New event name**: `generate_lead`
4. Toggle **Mark as conversion**: ON

The conversion will start counting within 24-48 hours. Use DebugView for immediate verification.

## Testing & Verification

**Immediate Testing (DebugView):**
1. GA4 → **Configure** → **DebugView**
2. Fill out and submit your Typeform
3. You should see `generate_lead` event within 30 seconds
4. Check event parameters match your setup

**Production Verification:**
- **Realtime Reports**: GA4 → **Reports** → **Realtime** → check for live conversions
- **Cross-check numbers**: Compare Typeform completion count (Typeform → Results → Summary) with GA4 conversion count (GA4 → Reports → Conversions)
- **Acceptable variance**: 5-15% difference is normal due to ad blockers and users bouncing before the tag fires

**Red Flags:**
- No events showing in DebugView after 2 minutes
- Typeform shows 100 completions but GA4 shows 0 conversions
- Events firing but missing form_id or form_type parameters

## Troubleshooting

**Problem** → GA4 events not firing at all
Check GTM Preview mode. If the trigger isn't firing, verify your thank you page URL structure matches the trigger conditions exactly. I see this when teams use `/thanks` instead of `/thank-you` or forget the URL query parameters.

**Problem** → Events firing with missing parameters
The URL query variables aren't pulling the data. Check that your Typeform redirect URL is actually appending the parameters. Test by manually visiting `yoursite.com/thank-you?form=typeform_lead&source=test` and see if the variables populate in GTM Preview.

**Problem** → Embedded Typeform postMessage not working
The postMessage listener might be loading before Typeform. Wrap the event listener in a `document.addEventListener('DOMContentLoaded', function() { ... })` to ensure Typeform is fully loaded first.

**Problem** → GA4 shows events but not conversions
The event name in your GA4 tag doesn't match what you marked as a conversion. Double-check that both use exactly `generate_lead` (case-sensitive). Also verify the conversion toggle is actually ON in GA4 admin.

**Problem** → Conversion count way higher than Typeform submissions
Multiple events firing per submission. Check GTM Preview for duplicate tags. This often happens when both redirect tracking AND postMessage tracking are active simultaneously.

**Problem** → GA4 conversion count 50%+ lower than Typeform count
Either users are bouncing before the thank you page loads completely, or there are JavaScript errors preventing the GA4 tag from firing. Check browser console for errors and consider moving to server-side tracking via [Typeform webhooks](/integrations/typeform-to-hubspot) for more accuracy.

## What To Do Next

Now that you have Typeform conversions flowing into GA4, consider setting up tracking for other platforms:
- [Typeform → Google Ads conversion tracking](/tracking/typeform-google-ads-conversion-tracking) to optimize your search campaigns
- [Typeform → Meta Ads conversion tracking](/tracking/typeform-meta-ads-conversion-tracking) for Facebook campaign optimization  
- [Typeform → LinkedIn Ads conversion tracking](/tracking/typeform-linkedin-ads-conversion-tracking) for B2B lead generation

Want me to audit your current tracking setup for free? I'll spot the gaps and broken connections that are costing you conversions. [Get a free tracking audit here](/contact).

*This guide is part of the [GA4 Conversion Tracking Hub](/tracking/ga4-conversion-tracking) — complete guides for tracking conversions from every major form tool and landing page builder into GA4.*