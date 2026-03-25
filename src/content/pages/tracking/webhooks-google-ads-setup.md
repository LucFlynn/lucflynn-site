---
title: "Webhooks / Direct API for Google Ads: Complete Setup Guide (2026)"
slug: "webhooks-google-ads-setup"
description: "Complete guide to setting up Webhooks / Direct API for Google Ads. Step-by-step configuration, testing, and troubleshooting."
category: "tracking"
date: "2026-03-24"
hub_page: "/tracking/webhooks"
page_type: "spoke"
---

# Webhooks / Direct API + Google Ads Setup Guide

I audit 50+ accounts per quarter, and about 30% of them have some half-broken webhook setup that's sending garbage data to Google Ads. The conversion numbers look good in the interface, but when you dig into the quality — missing transaction IDs, duplicated conversions, completely wrong attribution windows — it's a mess.

The good news? Once you set this up correctly, you get the most reliable conversion tracking possible. No client-side blocking, no iOS 14.5 headaches, no "why did my conversions drop 40% overnight?" panic calls.

## What You'll Have Working By The End

- Server-side conversion events flowing directly to Google Ads Conversion API
- Real-time webhook triggers firing on every conversion action
- Proper deduplication between server-side and client-side events
- Cross-reference validation showing your numbers match between your database and Google Ads
- Backup client-side tracking for users who complete actions without triggering your webhook

## Prerequisites

- [ ] Google Ads account with admin access
- [ ] Server infrastructure that can receive and process webhooks (or serverless functions)
- [ ] Google Ads API access and conversion tracking setup
- [ ] Development environment for testing webhook endpoints
- [ ] SSL certificate for your webhook receiver (HTTPS required)

## Architecture Overview

Here's how the data flows in a proper webhook setup:

1. **User converts** → form submit, purchase, signup, etc.
2. **Your application** processes the conversion and stores it in your database
3. **Webhook fires** immediately to your conversion handler endpoint
4. **Server validates** the data and formats it for Google Ads API
5. **API call** sends conversion data directly to Google Ads
6. **Client-side backup** (optional) fires for deduplication coverage

This gives you conversion data that's immune to ad blockers, iOS tracking prevention, and browser privacy updates.

## Step 1: Set Up Google Ads Conversion Actions

First, create the conversion actions you'll be sending data to. You need these setup before you start building webhooks.

In Google Ads, go to Tools & Settings → Conversions → Create new conversion action.

**Key settings for webhook-driven conversions:**
- **Source**: Website
- **Category**: Choose the most relevant (Purchase, Sign-up, etc.)
- **Value**: Use different values for each conversion if you're tracking purchases
- **Count**: "One" for most actions, "Every" for purchases
- **Attribution window**: 30 days click, 1 day view (standard for server-side)
- **Include in Conversions**: Yes

Make note of the **Conversion Action ID** — you'll need this for the API calls. You can find it in the URL when viewing the conversion action details, or use the Google Ads API to list all conversion actions.

## Step 2: Google Ads API Setup and Authentication

You'll need API access to send conversion data. Here's the setup:

**Create a Google Cloud Project:**
1. Go to Google Cloud Console
2. Create a new project or select existing
3. Enable Google Ads API
4. Create credentials (OAuth 2.0 or Service Account)

**Generate OAuth 2.0 credentials** (recommended for most setups):
```json
{
  "client_id": "your-client-id.googleusercontent.com",
  "client_secret": "your-client-secret",
  "refresh_token": "your-refresh-token",
  "developer_token": "your-developer-token"
}
```

Store these securely — you'll use them in your webhook handler to authenticate API calls.

## Step 3: Build Your Webhook Receiver Endpoint

Here's a basic webhook receiver that processes conversion events and sends them to Google Ads. I'm using Node.js, but the principles work in any language:

```javascript
const express = require('express');
const { GoogleAdsApi } = require('google-ads-api');
const app = express();

// Google Ads API client
const client = new GoogleAdsApi({
  client_id: process.env.GOOGLE_ADS_CLIENT_ID,
  client_secret: process.env.GOOGLE_ADS_CLIENT_SECRET,
  developer_token: process.env.GOOGLE_ADS_DEVELOPER_TOKEN,
});

const customer = client.Customer({
  customer_id: 'YOUR_CUSTOMER_ID',
  refresh_token: process.env.GOOGLE_ADS_REFRESH_TOKEN,
});

app.use(express.json());

app.post('/webhook/conversion', async (req, res) => {
  try {
    const { email, phone, conversion_action, conversion_value, order_id, gclid, timestamp } = req.body;
    
    // Validate required fields
    if (!email && !phone) {
      return res.status(400).json({ error: 'Email or phone required' });
    }
    
    if (!conversion_action || !gclid) {
      return res.status(400).json({ error: 'Conversion action and gclid required' });
    }

    // Hash email and phone for enhanced conversions
    const hashedEmail = email ? hashEmail(email) : null;
    const hashedPhone = phone ? hashPhone(phone) : null;

    const conversionData = {
      conversion_action: `customers/${customer_id}/conversionActions/${conversion_action}`,
      conversion_date_time: timestamp || new Date().toISOString(),
      conversion_value: parseFloat(conversion_value) || 0,
      currency_code: 'USD',
      order_id: order_id,
      gclid: gclid,
    };

    // Add enhanced conversion data if available
    if (hashedEmail || hashedPhone) {
      conversionData.user_identifiers = [];
      if (hashedEmail) {
        conversionData.user_identifiers.push({
          hashed_email: hashedEmail
        });
      }
      if (hashedPhone) {
        conversionData.user_identifiers.push({
          hashed_phone_number: hashedPhone
        });
      }
    }

    // Send to Google Ads
    const result = await customer.conversionUploads.uploadClickConversions({
      customer_id: customer_id,
      conversions: [conversionData],
      partial_failure: true
    });

    console.log('Conversion uploaded:', result);
    res.status(200).json({ success: true, result: result });
    
  } catch (error) {
    console.error('Webhook error:', error);
    res.status(500).json({ error: 'Failed to process conversion' });
  }
});

function hashEmail(email) {
  // Use SHA256 hashing as required by Google Ads
  const crypto = require('crypto');
  return crypto.createHash('sha256').update(email.toLowerCase().trim()).digest('hex');
}

function hashPhone(phone) {
  // Format phone number and hash
  const crypto = require('crypto');
  const cleanPhone = phone.replace(/\D/g, '');
  return crypto.createHash('sha256').update(cleanPhone).digest('hex');
}

app.listen(3000, () => {
  console.log('Webhook server listening on port 3000');
});
```

**Deploy this to your server infrastructure.** I typically use Google Cloud Run for webhook handlers because it auto-scales and you only pay for requests, but AWS Lambda, Railway, or any VPS works fine.

## Step 4: Configure Your Application to Fire Webhooks

In your main application (wherever conversions happen), add webhook calls that fire immediately when a conversion occurs:

```javascript
// In your conversion handler (after saving to database)
async function triggerConversionWebhook(conversionData) {
  try {
    const webhookPayload = {
      email: conversionData.user_email,
      phone: conversionData.user_phone,
      conversion_action: 'YOUR_CONVERSION_ACTION_ID',
      conversion_value: conversionData.order_total,
      order_id: conversionData.order_id,
      gclid: conversionData.gclid, // From form or session storage
      timestamp: new Date().toISOString()
    };

    await fetch('https://your-webhook-endpoint.com/webhook/conversion', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer your-webhook-secret'
      },
      body: JSON.stringify(webhookPayload)
    });
    
    console.log('Conversion webhook fired');
  } catch (error) {
    console.error('Webhook failed:', error);
    // Log to error tracking service
  }
}
```

**Critical implementation detail:** You need to capture the `gclid` parameter when users land on your site from Google Ads and store it with the user session. Most setups store this in a cookie or session storage, then include it in form submissions.

## Step 5: Set Up Client-Side Backup Tracking

Even with webhooks, I always set up client-side backup tracking. About 5-10% of webhook events can fail due to server issues, and you want deduplication coverage.

**GTM Tag Configuration:**
- **Tag Type**: Google Ads Conversion Tracking
- **Conversion ID**: Your Google Ads account ID
- **Conversion Label**: The label from your conversion action
- **Transaction ID**: `{{Order ID}}` (for deduplication)
- **Conversion Value**: `{{Purchase Value}}`

**Deduplication strategy**: Use the same `order_id` in both webhook and client-side events. Google Ads will automatically deduplicate based on transaction ID, keeping whichever conversion arrives first (usually the webhook).

## Testing & Verification

**1. Test your webhook endpoint directly:**
```bash
curl -X POST https://your-webhook-endpoint.com/webhook/conversion \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "conversion_action": "YOUR_CONVERSION_ACTION_ID",
    "conversion_value": 49.99,
    "order_id": "test_order_123",
    "gclid": "test_gclid"
  }'
```

**2. Check Google Ads conversion import status:**
- Go to Tools & Settings → Conversions
- Click on your conversion action
- Check "Recent activity" for successful imports
- Look for any error messages in the import log

**3. Verify conversion attribution:**
- Run a test conversion with a real gclid from a Google Ads click
- Check that the conversion appears in Google Ads within 3-6 hours
- Verify the conversion value and attribution match your expectations

**4. Monitor API quota usage:**
- Google Ads API has daily request limits
- Check your quota usage in Google Cloud Console
- Each conversion upload counts as one API call

**Acceptable performance:** 95%+ of webhook conversion events should successfully reach Google Ads within 15 minutes. If you're seeing lower success rates or longer delays, there's likely an infrastructure or authentication issue.

## Troubleshooting

**Problem** → Your webhook returns 200 OK but conversions aren't showing in Google Ads.
**Solution**: Check the Google Ads API response for partial_failure errors. Common issues: invalid conversion_action ID, malformed gclid, or missing required fields. Enable detailed API logging to see specific error messages.

**Problem** → Conversions are being attributed to the wrong campaigns or ad groups.
**Solution**: Verify that your gclid values are accurate and not being corrupted in storage. Test with fresh gclids from actual Google Ads clicks. Old or invalid gclids (>30 days) won't attribute correctly.

**Problem** → Duplicate conversions appearing even with transaction IDs.
**Solution**: Check that your transaction IDs are truly unique across all conversion actions. If you're using the same order ID for multiple conversion types (purchase + newsletter signup), Google sees them as duplicates. Use prefixed transaction IDs like `purchase_12345` and `signup_12345`.

**Problem** → Webhook endpoint randomly failing with timeout errors.
**Solution**: Add retry logic to your webhook calls and implement a dead letter queue for failed events. Google Ads API can be slow (2-10 seconds response time), so set webhook timeouts to at least 30 seconds.

**Problem** → Enhanced conversions not matching despite having email/phone data.
**Solution**: Verify your hashing implementation. Email addresses must be lowercased and trimmed before hashing. Phone numbers must be in E.164 format (+1234567890) before hashing. Test your hash values against Google's documentation.

**Problem** → API authentication failing with "unauthorized" errors.
**Solution**: Your refresh token has likely expired. Re-run the OAuth flow to generate a new refresh token. Also check that your developer token is approved and not in "test" mode if you're running production traffic.

## What To Do Next

Once your webhook setup is solid, consider expanding to [Enhanced Conversions for Web](/tracking/enhanced-conversions-web) to improve attribution accuracy, or setting up [Server-Side Tracking with Google Tag Manager](/tracking/server-side-gtm) if you need more sophisticated event processing.

For complex e-commerce setups, check out the [Webhooks for Shopify Forms](/tracking/webhooks-shopify-forms) guide for platform-specific implementation details.

If you're getting stuck on any of these API integrations or want someone to audit your current webhook setup, [get a free tracking audit](/contact) — I'll review your implementation and point out any issues that could be costing you attribution accuracy.

*This guide is part of the [Webhooks / Direct API Tracking Hub](/tracking/webhooks) — comprehensive guides for implementing server-side conversion tracking across all major ad platforms and marketing tools.*