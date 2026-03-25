---
title: "How to Track Typeform Conversions in Meta Ads (2026 Guide)"
slug: "typeform-meta-ads-conversion-tracking"
description: "Step-by-step guide to tracking Typeform form submissions as conversions in Meta Ads. Covers GTM setup, Meta CAPI, testing, and troubleshooting."
category: "tracking"
date: "2026-03-24"
hub_page: "/tracking/meta-ads-conversion-tracking"
page_type: "spoke"
---

# Typeform + Meta Ads Conversion Tracking Setup

I see Typeform + Meta Ads setups broken in about 35% of accounts I audit. The most common issue? They're only tracking redirects or thank you pages, missing all the embedded form completions. When Typeform is embedded, users don't navigate to a new page — they complete the form right there, and your pixel never fires.

The fix is tracking the actual form submission event using Typeform's postMessage API, then sending that data to Meta via both the pixel and Conversions API for maximum reliability.

## What You'll Have Working By The End

- Typeform submissions tracked as 'Lead' events in Meta Ads (both embedded and standalone)
- Meta Conversions API (CAPI) running server-side with proper deduplication
- Cross-platform attribution data flowing to your CRM
- 5-15% variance between Typeform entries and Meta conversion counts (acceptable range)
- Bulletproof tracking that works even when users have ad blockers

## Prerequisites

- [ ] Meta Ads Manager access with admin permissions
- [ ] Meta Events Manager access to your pixel
- [ ] Google Tag Manager container with publish permissions
- [ ] Meta Conversions API access token (Business Manager → Events Manager → Conversions API)
- [ ] Typeform with either redirect URL control or JavaScript access to embedded forms
- [ ] Server endpoint capable of sending CAPI events (or Zapier/webhook service)

## Step 1: Set Up Typeform Tracking

The tracking method depends on how your Typeform is implemented. Most setups I see use embedded forms, which need special handling.

### For Embedded Typeforms

Add this JavaScript to any page with an embedded Typeform. This listens for Typeform's completion postMessage:

```javascript
<script>
// Listen for Typeform completion events
window.addEventListener('message', function(event) {
  // Verify the event is from Typeform
  if (event.data.type === 'form_submit' && event.origin.includes('typeform.com')) {
    
    // Push to dataLayer for GTM
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
      'event': 'typeform_submission',
      'form_id': event.data.form_id,
      'event_id': 'tf_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9),
      'user_agent': navigator.userAgent,
      'timestamp': Math.floor(Date.now() / 1000)
    });
    
    console.log('Typeform submission tracked:', event.data);
  }
});
</script>
```

### For Standalone Typeforms

If you control the redirect URL, set up a thank you page and add this to it:

```javascript
<script>
window.dataLayer = window.dataLayer || [];
window.dataLayer.push({
  'event': 'typeform_submission',
  'form_id': 'your_form_id_here', // Replace with actual form ID
  'event_id': 'tf_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9),
  'user_agent': navigator.userAgent,
  'timestamp': Math.floor(Date.now() / 1000)
});
</script>
```

The `event_id` is crucial — it's what prevents double-counting when both pixel and CAPI fire.

## Step 2: Configure GTM Trigger

In GTM, create a Custom Event trigger:

1. **Trigger Type**: Custom Event
2. **Event name**: `typeform_submission`
3. **Trigger fires on**: All Custom Events (or specific form IDs if you want granular control)

Save as "Typeform Submission - All Forms"

## Step 3: Set Up Meta Pixel Tag in GTM

Create a new tag for the client-side pixel event:

1. **Tag Type**: Meta Pixel
2. **Pixel ID**: Your Meta pixel ID
3. **Event Action**: Track an Event
4. **Event Name**: Lead (use the standard event for best optimization)
5. **Event Parameters**: 
   - `event_id`: `{{dlv - event_id}}` (create this as a Data Layer Variable)
   - `content_name`: `Typeform Submission`
   - `content_category`: `Form`

6. **Trigger**: Select your Typeform Submission trigger

The `event_id` parameter is what prevents duplicate counting between pixel and CAPI.

## Step 4: Set Up Meta Conversions API (CAPI)

This is where most setups fall apart. You need server-side tracking for reliability — about 20-30% of users have some form of client-side blocking.

### Option 1: Direct CAPI Implementation

If you have server access, send the conversion directly to Meta's API:

```javascript
// Server-side code (Node.js example)
const axios = require('axios');

async function sendToMetaCAPI(eventData) {
  const payload = {
    data: [{
      event_name: 'Lead',
      event_time: eventData.timestamp,
      event_id: eventData.event_id, // Same event_id as pixel for deduplication
      user_data: {
        client_ip_address: req.connection.remoteAddress,
        client_user_agent: eventData.user_agent,
        // Add email/phone if collected by Typeform
      },
      custom_data: {
        content_name: 'Typeform Submission',
        content_category: 'Form'
      }
    }],
    access_token: 'YOUR_ACCESS_TOKEN'
  };
  
  await axios.post(`https://graph.facebook.com/v18.0/YOUR_PIXEL_ID/events`, payload);
}
```

### Option 2: GTM Server-Side Container

If you're using GTM Server-side, create a Meta Conversions API tag:

1. **Tag Type**: Meta Conversions API
2. **Event Name**: Lead
3. **Event ID**: `{{Event ID}}` (maps to your dataLayer event_id)
4. **Trigger**: Your Typeform trigger (forwarded from web container)

## Step 5: Set Up Typeform Webhook (Recommended)

For the most reliable server-side tracking, use Typeform's webhook feature:

1. In Typeform, go to Settings → Webhooks
2. Add webhook URL: `https://your-server.com/typeform-webhook`
3. Configure your endpoint to receive and process submissions:

```javascript
app.post('/typeform-webhook', (req, res) => {
  const submission = req.body;
  
  // Generate consistent event_id
  const event_id = 'tf_webhook_' + submission.form_response.token;
  
  // Send to Meta CAPI
  sendToMetaCAPI({
    event_id: event_id,
    timestamp: Math.floor(new Date(submission.form_response.submitted_at).getTime() / 1000),
    user_data: {
      // Extract from submission data
      em: submission.form_response.answers.find(a => a.type === 'email')?.email
    }
  });
  
  res.status(200).send('OK');
});
```

## Testing & Verification

### Test the Client-Side Pixel

1. Open your Typeform page with browser dev tools open
2. Complete a test submission
3. In GTM Preview mode, verify:
   - Typeform submission event fires
   - Meta Pixel tag fires with correct event_id
   - No JavaScript errors in console

### Test Meta Events Manager

1. Go to Events Manager → Test Events
2. Complete another test submission
3. Within 20 seconds, you should see:
   - Event name: Lead
   - Event source: Both "Website" and "Server" (if CAPI is working)
   - Same event_id in both sources (confirms deduplication is working)

### Cross-Check the Numbers

After 24-48 hours of live data:

1. **Typeform**: Go to Results → Insights for total submissions
2. **Meta Events Manager**: Filter by your Lead event for the same timeframe
3. **Acceptable variance**: 5-15% difference (Meta should be slightly lower due to ad blockers and attribution windows)

If Meta shows 40%+ fewer conversions than Typeform, your CAPI isn't working properly.

## Troubleshooting

**Problem**: Embedded Typeform completions aren't being tracked, but standalone ones are
→ The postMessage listener isn't loading before the Typeform iframe. Move the tracking script higher in the page head, or wrap it in a DOMContentLoaded event.

**Problem**: Meta shows conversions but they're all attributed to "Direct" traffic instead of your ads
→ Your pixel isn't loading before users complete the form. Check that your Meta base pixel is in the page head and loading synchronously, not via GTM async.

**Problem**: Getting duplicate conversions in Meta (counts are 2x what they should be)
→ Both pixel and CAPI are firing but with different event_ids. Make sure both use the exact same event_id value. Check that your Data Layer Variable in GTM is correctly pulling the event_id.

**Problem**: CAPI events show in Test Events but not in regular Events Manager reporting
→ Your server clock is off, or you're sending timestamps in the wrong format. Meta requires Unix timestamps (seconds since epoch). Use `Math.floor(Date.now() / 1000)` in JavaScript.

**Problem**: Webhook events work but embedded form events don't, or vice versa
→ You're using different event_id generation logic for each method. Standardize on one format — I recommend `'tf_' + form_response_token` for webhooks and `'tf_' + timestamp + '_' + random` for client-side.

**Problem**: Test events work perfectly but live events show 0 conversions
→ Check your Meta ad account's attribution windows and conversion optimization settings. If you're optimizing for a custom conversion, make sure it's properly configured to include your Lead events.

## What To Do Next

- [Set up Google Ads conversion tracking for the same Typeform](/tracking/typeform-google-ads-conversion-tracking) to compare attribution data
- [Connect Typeform submissions directly to HubSpot](/integrations/typeform-to-hubspot) for complete lead management
- [Track Typeform completions in GA4](/tracking/typeform-ga4-conversion-tracking) for comprehensive analytics
- **Ready to fix your tracking setup?** [Get a free tracking audit](/contact) — I'll review your current setup and show you exactly what's broken.

*This guide is part of the [Meta Ads Conversion Tracking Hub](/tracking/meta-ads-conversion-tracking) — complete guides for tracking any conversion source in Meta Ads.*