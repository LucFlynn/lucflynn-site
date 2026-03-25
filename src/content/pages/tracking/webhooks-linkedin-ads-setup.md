---
title: "Webhooks / Direct API for LinkedIn Ads: Complete Setup Guide (2026)"
slug: "webhooks-linkedin-ads-setup"
description: "Complete guide to setting up Webhooks / Direct API for LinkedIn Ads. Step-by-step configuration, testing, and troubleshooting."
category: "tracking"
date: "2026-03-24"
hub_page: "/tracking/webhooks"
page_type: "spoke"
---

# Webhooks / Direct API + LinkedIn Ads Setup Guide

I see webhook implementations to LinkedIn break in about 60% of setups I audit. Usually it's because LinkedIn's Conversions API requires specific field mappings that aren't obvious, or because people try to send conversion events without proper user matching. The result? Your LinkedIn campaigns optimize on maybe 30% of your actual conversions.

LinkedIn's webhook implementation is actually one of the more forgiving ones to work with, but the devil is in the details — especially around user identity resolution and event deduplication.

## What You'll Have Working By The End

- Server-side conversion events flowing directly to LinkedIn's Conversions API
- Proper user matching using hashed emails, LinkedIn member IDs, and click IDs
- Event deduplication between client-side pixel and server-side webhook events  
- Real-time conversion verification in LinkedIn's Events Manager
- Backup tracking that works even when users block the LinkedIn Insight Tag

## Prerequisites

- [ ] LinkedIn Campaign Manager access with conversion tracking permissions
- [ ] Active LinkedIn Insight Tag already installed and firing
- [ ] Server infrastructure that can receive webhooks and make API calls (Cloud Run, AWS Lambda, etc.)
- [ ] Ability to capture user email addresses or LinkedIn member tokens
- [ ] LinkedIn Conversions API access token from your Campaign Manager account

## Architecture Overview

Here's how the data flows in a proper webhook setup:

1. User converts on your site/form
2. Your server captures the conversion data and user identifiers
3. Webhook endpoint receives the data and formats it for LinkedIn's API
4. Server makes POST request to LinkedIn's Conversions API
5. LinkedIn matches the user and attributes the conversion to the right campaign

The key is that everything happens server-to-server after step 1, so ad blockers can't interfere.

## Step 1: Set Up LinkedIn Conversions API Access

First, you need API credentials from LinkedIn Campaign Manager:

1. Go to Campaign Manager → Account Assets → Conversions
2. Click on your existing conversion action (or create one)
3. Navigate to "Conversions API" tab
4. Generate an access token and copy the conversion URN

Your conversion URN will look like: `urn:li:llaConversion:12345678`

Store both the access token and conversion URN — you'll need them for the webhook endpoint.

## Step 2: Build Your Webhook Endpoint

Here's a basic webhook endpoint that receives form data and sends it to LinkedIn:

```javascript
// Cloud Run / Express.js example
const express = require('express');
const crypto = require('crypto');
const axios = require('axios');

const app = express();
app.use(express.json());

const LINKEDIN_ACCESS_TOKEN = process.env.LINKEDIN_ACCESS_TOKEN;
const CONVERSION_URN = process.env.LINKEDIN_CONVERSION_URN;

app.post('/linkedin-webhook', async (req, res) => {
  try {
    const { email, first_name, last_name, company, phone, click_id, conversion_value } = req.body;
    
    // Hash the email for LinkedIn's API
    const hashedEmail = crypto.createHash('sha256').update(email.toLowerCase().trim()).digest('hex');
    
    const conversionData = {
      conversion: CONVERSION_URN,
      conversionHappenedAt: Date.now(),
      conversionValue: {
        currencyCode: 'USD',
        amount: conversion_value || '0'
      },
      userInfo: {
        hashedEmails: [hashedEmail]
      }
    };

    // Add click ID if available (best for attribution)
    if (click_id) {
      conversionData.userInfo.linkedinFirstPartyAdsTrackingUUID = click_id;
    }

    // Add additional user data for better matching
    if (first_name) conversionData.userInfo.hashedFirstNames = [crypto.createHash('sha256').update(first_name.toLowerCase().trim()).digest('hex')];
    if (last_name) conversionData.userInfo.hashedLastNames = [crypto.createHash('sha256').update(last_name.toLowerCase().trim()).digest('hex')];
    if (phone) conversionData.userInfo.hashedPhoneNumbers = [crypto.createHash('sha256').update(phone.replace(/\D/g, '')).digest('hex')];

    // Send to LinkedIn Conversions API
    await axios.post('https://api.linkedin.com/rest/conversions', conversionData, {
      headers: {
        'Authorization': `Bearer ${LINKEDIN_ACCESS_TOKEN}`,
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
      }
    });

    res.status(200).json({ success: true });
  } catch (error) {
    console.error('LinkedIn webhook error:', error.response?.data || error.message);
    res.status(500).json({ error: 'Failed to process conversion' });
  }
});

app.listen(8080);
```

Deploy this to your preferred platform. I typically use Google Cloud Run because it's simple and scales automatically.

## Step 3: Configure Your Form/CRM Integration

Your form needs to send data to your webhook endpoint when someone converts. Here are the key fields LinkedIn needs:

**Required:**
- `email` — User's email address (will be hashed)
- Conversion timestamp (auto-generated in the webhook)

**Highly Recommended:**
- `click_id` — LinkedIn's first-party tracking UUID (captured from URL parameters)
- `first_name` and `last_name` — Improves user matching rates
- `conversion_value` — For value-based bidding

**Optional but Helpful:**
- `phone` — Additional matching signal
- `company` — Can improve B2B matching

Example form submission that triggers the webhook:

```javascript
// Capture LinkedIn click ID from URL
const urlParams = new URLSearchParams(window.location.search);
const linkedinClickId = urlParams.get('li_fat_id');

// Form submission handler
document.getElementById('lead-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const formData = {
    email: document.getElementById('email').value,
    first_name: document.getElementById('first_name').value,
    last_name: document.getElementById('last_name').value,
    company: document.getElementById('company').value,
    phone: document.getElementById('phone').value,
    click_id: linkedinClickId,
    conversion_value: '100' // Your lead value
  };

  // Send to your webhook
  await fetch('https://your-webhook-url.run.app/linkedin-webhook', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(formData)
  });
  
  // Continue with normal form submission
});
```

## Step 4: Set Up Event Deduplication

If you're running both the LinkedIn pixel and webhooks (which you should), you need deduplication to prevent double-counting conversions.

Add an `eventId` parameter to both your pixel and webhook events:

```javascript
// Client-side pixel event with event ID
_linkedin_partner_id = "your_partner_id";
window._linkedin_data_partner_ids = window._linkedin_data_partner_ids || [];
window._linkedin_data_partner_ids.push(_linkedin_partner_id);

// Generate unique event ID
const eventId = 'conv_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);

lintrk('track', { 
  conversion_id: your_conversion_id,
  event_id: eventId
});
```

Then include the same `eventId` in your webhook payload:

```javascript
const conversionData = {
  conversion: CONVERSION_URN,
  conversionHappenedAt: Date.now(),
  eventId: req.body.event_id, // Same ID from client-side
  // ... rest of data
};
```

LinkedIn will automatically deduplicate events with the same `eventId`.

## Step 5: Handle LinkedIn Member Token (Advanced)

For the highest match rates on LinkedIn, capture the member token if available:

```javascript
// Capture LinkedIn member token (if user is logged into LinkedIn)
if (window.IN && IN.User) {
  IN.User.authorize(() => {
    const memberToken = IN.User.getMemberToken();
    if (memberToken) {
      formData.linkedin_member_token = memberToken;
    }
  });
}
```

Add this to your webhook processing:

```javascript
if (linkedin_member_token) {
  conversionData.userInfo.linkedinMemberToken = linkedin_member_token;
}
```

## Testing & Verification

**Test the webhook endpoint first:**
```bash
curl -X POST https://your-webhook-url.run.app/linkedin-webhook \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "conversion_value": "100"
  }'
```

**Check LinkedIn Events Manager:**
1. Go to Campaign Manager → Account Assets → Conversions
2. Click on your conversion action
3. Check "Recent Events" tab — webhook conversions should appear within 5-10 minutes
4. Look for "API" source in the event details

**Verify user matching:**
Good user matching rates for LinkedIn webhooks are 70-85%. If you're seeing below 60%, you probably need better user identifiers (especially click IDs or member tokens).

**Check attribution in Campaign Reports:**
Your webhook conversions should start appearing in campaign performance within 24 hours. Cross-check the numbers:
- Acceptable variance between webhook events sent and LinkedIn conversions recorded: 15-25%
- If you're losing more than 30%, check your user matching setup

## Troubleshooting

**Problem:** Webhook returns 401 "Unauthorized" error
→ Your access token expired or doesn't have conversion API permissions. Generate a new token in Campaign Manager and make sure it's for the right ad account.

**Problem:** Events send successfully but don't appear in LinkedIn Events Manager  
→ Check your conversion URN format. It should be `urn:li:llaConversion:12345678`, not just the number. Also verify the conversion action is active and not paused.

**Problem:** Low user matching rates (below 60%)
→ You're probably missing click IDs. Make sure you're capturing `li_fat_id` from URL parameters and including it as `linkedinFirstPartyAdsTrackingUUID`. Also ensure emails are being hashed correctly (lowercase, trimmed, SHA256).

**Problem:** Webhook times out or fails intermittently
→ LinkedIn's API can be slow sometimes. Add retry logic with exponential backoff, and consider processing webhooks asynchronously (queue the data, then send to LinkedIn in a background job).

**Problem:** Getting "Invalid conversion value" errors
→ LinkedIn expects conversion values as strings, not numbers. Make sure you're sending `"100"` not `100`. Also check that your currency code matches your ad account's default currency.

**Problem:** Duplicate conversions appearing despite event IDs
→ Make sure you're generating the event ID on the client-side and passing it through your form to the webhook. If the webhook generates its own event ID, deduplication won't work.

## What To Do Next

Now that you have LinkedIn webhook tracking working, consider expanding your server-side setup:

- [Facebook Conversions API Webhook Setup](/tracking/webhooks-facebook-ads-setup) — Similar implementation for Meta ads
- [Google Ads Enhanced Conversions via Webhooks](/tracking/webhooks-google-ads-setup) — Google's server-side solution  
- [Multi-Platform Webhook Architecture](/tracking/webhooks-multi-platform-setup) — Send one webhook to multiple ad platforms

Want me to audit your current LinkedIn tracking setup? I'll check your pixel implementation, webhook configuration, and user matching rates for free. [Get your tracking audit here](/contact).

*This guide is part of the [Webhooks & Direct API Tracking Hub](/tracking/webhooks) — comprehensive guides for implementing server-side conversion tracking across all major ad platforms.*