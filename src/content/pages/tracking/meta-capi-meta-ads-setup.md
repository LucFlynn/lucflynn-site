---
title: "Meta CAPI for Meta Ads: Complete Setup Guide (2026)"
slug: "meta-capi-meta-ads-setup"
description: "Complete guide to setting up Meta CAPI for Meta Ads. Step-by-step configuration, testing, and troubleshooting."
category: "tracking"
date: "2026-03-24"
hub_page: "/tracking/meta-capi"
page_type: "spoke"
---

# Meta CAPI + Meta Ads Setup Guide

Most accounts I audit are losing 20-30% of their conversion data because they're only running pixel tracking. iOS 17.4+ blocks the Meta pixel for about 35% of users, and that percentage keeps climbing. I've seen ROAS improve by 15-25% just from getting server-side conversion data flowing properly through CAPI.

The tricky part isn't the concept — it's getting the infrastructure right so your server-side events match your client-side events, and Meta's deduplication actually works instead of double-counting everything.

## What You'll Have Working By The End

- Meta CAPI container running on Google Cloud Run (or your preferred platform)
- Client-side pixel events flowing to your server container, then to Meta
- Server-side events with proper event_id matching for deduplication  
- Purchase, lead, and custom conversion events tracked server-side with full attribution data
- Event matching quality scores above 7.0 in Meta Events Manager
- 95%+ event delivery success rate verified in CAPI Gateway

## Prerequisites

- [ ] Meta Business Manager admin access
- [ ] Meta Ads account with active campaigns
- [ ] Meta pixel already installed and firing events
- [ ] Google Cloud Platform account (or AWS/other cloud provider)
- [ ] Basic command line familiarity for container deployment
- [ ] Access to modify your website's tracking code

## Step 1: Generate CAPI Access Token and Dataset ID

In Meta Business Manager, go to Events Manager → your pixel → Settings → Conversions API.

Click "Generate Access Token" and copy it. You'll also need your Dataset ID (pixel ID) from the same page.

**Store these securely** — the access token has write access to your conversion data. I usually store them as environment variables in whatever cloud platform I'm using.

The access token format looks like: `EAAxxxxxxxxx|xxxxxxxxxxxxxxxxxxxxxxxxxx`
Your Dataset ID is the numeric pixel ID, like: `1234567890123456`

## Step 2: Deploy CAPI Container Infrastructure

I use Google Cloud Run for most CAPI deployments because it's simple and scales automatically. Here's the Docker setup I use:

Create a `Dockerfile`:

```dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 8080
CMD ["node", "server.js"]
```

And the core `server.js`:

```javascript
const express = require('express');
const axios = require('axios');
const crypto = require('crypto');

const app = express();
app.use(express.json());

const CAPI_ENDPOINT = 'https://graph.facebook.com/v19.0/{DATASET_ID}/events';
const ACCESS_TOKEN = process.env.META_ACCESS_TOKEN;
const DATASET_ID = process.env.META_DATASET_ID;

app.post('/capi', async (req, res) => {
  try {
    const { events } = req.body;
    
    const payload = {
      data: events.map(event => ({
        event_name: event.event_name,
        event_time: Math.floor(Date.now() / 1000),
        event_id: event.event_id,
        action_source: 'website',
        event_source_url: event.event_source_url,
        user_data: {
          em: event.user_data?.email ? hashData(event.user_data.email) : undefined,
          ph: event.user_data?.phone ? hashData(event.user_data.phone) : undefined,
          client_ip_address: req.ip,
          client_user_agent: req.headers['user-agent'],
          fbc: event.user_data?.fbc,
          fbp: event.user_data?.fbp
        },
        custom_data: event.custom_data || {}
      })),
      access_token: ACCESS_TOKEN
    };

    const response = await axios.post(
      CAPI_ENDPOINT.replace('{DATASET_ID}', DATASET_ID),
      payload
    );

    res.json({ success: true, meta_response: response.data });
  } catch (error) {
    console.error('CAPI Error:', error.response?.data || error.message);
    res.status(500).json({ error: error.message });
  }
});

function hashData(data) {
  return crypto.createHash('sha256').update(data.toLowerCase().trim()).digest('hex');
}

app.listen(8080, () => {
  console.log('CAPI server running on port 8080');
});
```

Deploy to Cloud Run:

```bash
gcloud run deploy meta-capi \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars META_ACCESS_TOKEN=your_token,META_DATASET_ID=your_pixel_id
```

Your container URL will be something like: `https://meta-capi-xxx-uc.a.run.app`

## Step 3: Configure Client-Side Event Collection

You need to modify your existing pixel implementation to send events to both Meta directly AND your CAPI container.

Here's the JavaScript I use to capture pixel events and forward them server-side:

```javascript
// Enhanced pixel setup with CAPI forwarding
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window,document,'script',
'https://connect.facebook.net/en_US/fbevents.js');

fbq('init', 'YOUR_PIXEL_ID');
fbq('track', 'PageView');

// CAPI forwarding function
const CAPI_ENDPOINT = 'https://your-container-url.run.app/capi';

function sendToCAPI(eventName, eventData = {}) {
  const eventId = crypto.randomUUID();
  
  // Send to pixel with event_id for deduplication
  fbq('track', eventName, eventData, { event_id: eventId });
  
  // Send to CAPI container
  const capiEvent = {
    events: [{
      event_name: eventName,
      event_id: eventId,
      event_source_url: window.location.href,
      user_data: {
        email: eventData.email,
        phone: eventData.phone,
        fbc: getCookie('_fbc'),
        fbp: getCookie('_fbp')
      },
      custom_data: eventData
    }]
  };
  
  fetch(CAPI_ENDPOINT, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(capiEvent)
  }).catch(err => console.error('CAPI send failed:', err));
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

// Usage for purchases
sendToCAPI('Purchase', {
  value: 99.99,
  currency: 'USD',
  content_ids: ['product-123'],
  content_type: 'product'
});
```

The key is using the same `event_id` for both the pixel event and the CAPI event. That's how Meta deduplicates them.

## Step 4: Configure GTM Container (If Using GTM)

If you're using Google Tag Manager, create a Custom HTML tag for CAPI forwarding:

**Tag Type:** Custom HTML
**Trigger:** Same triggers as your Meta pixel events

```html
<script>
function sendEventToCAPI(eventName, eventData) {
  const eventId = 'evt_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
  
  // Update pixel event to include event_id
  if (typeof fbq !== 'undefined') {
    fbq('track', eventName, eventData, { event_id: eventId });
  }
  
  // Send to CAPI
  fetch('https://your-container-url.run.app/capi', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      events: [{
        event_name: eventName,
        event_id: eventId,
        event_source_url: {{Page URL}},
        user_data: {
          em: {{Email Hash}}, // Create variables for these
          ph: {{Phone Hash}},
          fbc: {{Click ID}},
          fbp: {{Browser ID}}
        },
        custom_data: eventData
      }]
    })
  });
}

// Trigger based on your event
sendEventToCAPI('{{Event Name}}', {
  value: {{Purchase Value}},
  currency: 'USD'
});
</script>
```

Create variables for the hashed email, phone, etc. The email hash variable should use this custom JavaScript:

```javascript
function() {
  const email = {{Form Email}}; // Your email variable
  if (!email) return undefined;
  
  return CryptoJS.SHA256(email.toLowerCase().trim()).toString();
}
```

## Step 5: Set Up Event Matching and Data Quality

Meta's event matching quality determines how well they can attribute your server-side events. You want quality scores above 7.0.

**Required fields for good matching:**
- `client_ip_address` (automatically captured from request)
- `client_user_agent` (from request headers)  
- `fbc` (Facebook click ID from URL)
- `fbp` (Facebook browser ID from cookie)

**High-value optional fields:**
- Hashed email (`em`)
- Hashed phone number (`ph`)
- `external_id` (your internal user ID, hashed)

The email and phone must be SHA256 hashed and lowercase. Don't send plain text — Meta will reject the events.

Here's how I handle the hashing server-side:

```javascript
function processUserData(userData) {
  const processed = {};
  
  if (userData.email) {
    processed.em = crypto.createHash('sha256')
      .update(userData.email.toLowerCase().trim())
      .digest('hex');
  }
  
  if (userData.phone) {
    // Remove non-digits, add country code if missing
    let phone = userData.phone.replace(/\D/g, '');
    if (phone.length === 10) phone = '1' + phone; // Assume US
    
    processed.ph = crypto.createHash('sha256')
      .update(phone)
      .digest('hex');
  }
  
  return processed;
}
```

## Step 6: Testing and Verification

**Test in CAPI Gateway:**
Go to Events Manager → Test Events → your pixel. You should see server events flowing in with your test event IDs.

**Check Event Matching Quality:**
Events Manager → Data Sources → your pixel → Diagnostics. Look for "Event Matching" scores. Anything below 6.0 needs improvement.

**Verify Deduplication:**
Send the same event via pixel and CAPI with identical event_ids. In the Test Events tool, you should see one event with source "Browser and Server" — that means deduplication worked.

**Attribution Testing:**
Run a small test campaign and compare attributed conversions in Ads Manager against your source-of-truth conversion count. I expect 5-15% variance due to attribution windows and view-through conversions.

**Server Health:**
Monitor your container's logs and response times. I typically see 50-100ms response times for CAPI requests. Anything over 500ms indicates infrastructure issues.

## Troubleshooting

**Problem:** Events showing in Test Events but not attributed to campaigns
Your event_time might be off. CAPI events must happen within Meta's attribution window (default 7 days view, 1 day click). Check that your server's system clock is accurate and you're using Unix timestamps.

**Problem:** Low event matching quality scores (below 6.0)
You're missing key matching parameters. Add `fbc` and `fbp` from the client side, and include hashed email/phone when available. The `client_ip_address` and `client_user_agent` are critical — make sure they're from the actual user's browser, not your server.

**Problem:** CAPI events firing but pixel events not deduplicating
Your event_ids don't match between client and server. Make sure you generate the event_id client-side and pass it to both the pixel and your CAPI endpoint. The event_id format should be consistent (I use UUID v4).

**Problem:** High error rates in CAPI Gateway
Check your access token permissions and dataset ID. Also verify your event payload structure — Meta is strict about field types. Values should be numbers, currencies should be strings like "USD", and arrays should contain strings.

**Problem:** Container deployment failing or timing out
Cloud Run has memory and CPU limits. For high-volume accounts (>10k events/day), bump the memory to 1GB and set max instances to 100. Also add request batching to reduce API calls to Meta.

**Problem:** Events appearing delayed in Meta (2+ hours)
This is usually infrastructure lag. Check your container's performance metrics. If you're on the free tier of cloud services, upgrade to get guaranteed resources. Meta typically processes CAPI events within 15-30 minutes.

## What To Do Next

- [Complete Meta CAPI Setup Hub](/tracking/meta-capi) — covers all CAPI implementations across different platforms
- [Contact me for a free tracking audit](/contact) — I'll review your current setup and identify what's costing you conversions
- Set up CAPI for other platforms once you have Meta working smoothly

*This guide is part of the [Meta CAPI Setup Hub](/tracking/meta-capi) — covering server-side conversion tracking implementation across all major ad platforms using Meta's Conversions API.*