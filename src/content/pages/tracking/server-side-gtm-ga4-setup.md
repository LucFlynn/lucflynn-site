---
title: "Server-Side GTM for GA4: Complete Setup Guide (2026)"
slug: "server-side-gtm-ga4-setup"
description: "Complete guide to setting up Server-Side GTM for GA4. Step-by-step configuration, testing, and troubleshooting."
category: "tracking"
date: "2026-03-24"
hub_page: "/tracking/server-side-gtm"
page_type: "spoke"
---

# Server-Side GTM + GA4 Setup Guide

I see broken server-side GA4 setups in about 60% of the accounts I audit. The most common issue? Teams think they can just "flip a switch" to server-side tracking without understanding the data flow architecture. Then they wonder why their attribution is broken and their GA4 data looks nothing like their client-side setup.

Server-side GTM for GA4 isn't just moving tags to a server — it's fundamentally changing how user data flows from your website to Google Analytics.

## What You'll Have Working By The End

- **Complete server-side GA4 implementation** with all core events (page_view, session_start, purchase, etc.)
- **First-party data collection** that bypasses ad blockers and ITP restrictions
- **Enhanced measurement events** flowing correctly through your server container
- **Attribution models working properly** with server-side session stitching
- **Cross-domain tracking** maintained through server-side processing

## Prerequisites

- [ ] GA4 property with admin access
- [ ] Google Tag Manager account with server container permissions
- [ ] Cloud hosting setup (Cloud Run, AWS Lambda, or dedicated server)
- [ ] Custom domain for your server endpoint (e.g., analytics.yourdomain.com)
- [ ] Basic understanding of HTTP requests and JSON payloads

## Step 1: Set Up Your Server-Side Container

First, create your server-side GTM container. This is separate from your web container — you'll need both.

In GTM, create a new container and select "Server" as the target platform. Google will provision you a Cloud Run instance by default, but I recommend setting up your own custom domain immediately.

**Critical configuration:**
- Server URL: `https://analytics.yourdomain.com` (never use the default appspot domain)
- Container ID: This will be different from your web container ID
- Transport URL: Configure this in your web container to send data to your server

Here's the client-side configuration to send data to your server:

```javascript
// In your web container's GA4 Configuration tag
gtag('config', 'GA_MEASUREMENT_ID', {
  'server_container_url': 'https://analytics.yourdomain.com',
  'transport_url': 'https://analytics.yourdomain.com'
});
```

**Which hosting should you use?** For most businesses, Cloud Run is fine for the first 100K events per month. Above that, I usually recommend AWS Lambda or a dedicated server for better cost control and performance.

## Step 2: Configure the GA4 Client

In your server container, you need a GA4 Client to receive data from your website. This acts as the entry point for all GA4 events.

Create a new Client with these settings:
- **Client Type:** GA4
- **Request Path:** `/g/collect` (this is where GA4 events will be sent)
- **Measurement Protocol API Secret:** Generate this in your GA4 property settings

The GA4 client automatically parses incoming requests and makes the data available to your server-side tags. It handles the complex work of converting the HTTP request into usable event data.

## Step 3: Set Up Server-Side GA4 Tags

Now configure your server-side GA4 tag to send events to Google Analytics. This replaces your client-side GA4 tag for server-processed events.

**Server-Side GA4 Configuration Tag:**
```
Tag Type: GA4
Measurement ID: G-XXXXXXXXXX
Event Name: {{Event Name}} (built-in variable)
Event Parameters: {{Event Parameters}} (built-in variable)
```

**Critical server-side parameters to preserve:**
- `client_id`: User identifier for session stitching
- `session_id`: Maintains session continuity
- `page_location`: Full URL for attribution
- `page_referrer`: Previous page for funnel analysis
- `user_id`: Your internal user identifier (if using)

Here's how session stitching works: The client-side sends a `client_id` with each event. Your server-side tag must forward this exact same `client_id` to GA4, or you'll break user journey tracking.

**Enhanced Ecommerce events require specific formatting:**
```javascript
// Purchase event structure
{
  "event_name": "purchase",
  "client_id": "1234567890.1234567890",
  "event_parameters": {
    "transaction_id": "T_12345",
    "value": 25.99,
    "currency": "USD",
    "items": [{
      "item_id": "SKU_123",
      "item_name": "Product Name",
      "category": "Electronics",
      "quantity": 1,
      "price": 25.99
    }]
  }
}
```

## Step 4: Configure User-ID and Cross-Domain Tracking

Server-side tracking gives you better control over user identification, but you need to configure it properly.

**User-ID Configuration:**
If you're using User-ID, set it in both your client-side and server-side configurations:

```javascript
// Client-side (in web container)
gtag('config', 'GA_MEASUREMENT_ID', {
  'user_id': userId,
  'server_container_url': 'https://analytics.yourdomain.com'
});
```

**Server-side User-ID tag configuration:**
- Set `user_id` parameter: `{{User ID}}` (create this as a custom variable)
- Ensure the User-ID flows through to your server container via the Event Data

**Cross-domain tracking** becomes simpler with server-side — your server can process events from multiple domains and maintain consistent `client_id` values.

## Step 5: Set Up Enhanced Measurement Events

GA4's Enhanced Measurement (scroll, outbound clicks, file downloads, video engagement) needs special handling in server-side setups.

Create separate triggers for each Enhanced Measurement event:
- **Scroll Trigger:** Fire when scroll depth data is received
- **File Download Trigger:** Fire on file_download events
- **Video Engagement Trigger:** Fire on video_start, video_progress events

**Important:** Enhanced Measurement events from client-side GA4 won't automatically work server-side. You need to explicitly send these events through your server container.

Example scroll tracking configuration:
```javascript
// Client-side event
gtag('event', 'scroll', {
  'percent_scrolled': 90,
  'send_to': 'server'  // Ensures event goes to server container
});
```

## Step 6: Configure Consent Mode and Privacy Settings

Server-side tracking improves compliance but requires proper consent handling.

**Consent Mode Configuration:**
```javascript
// Client-side consent setup
gtag('consent', 'default', {
  'ad_storage': 'denied',
  'analytics_storage': 'granted',
  'ad_user_data': 'denied',
  'ad_personalization': 'denied'
});
```

**Server-side consent handling:**
In your server container, create a Consent variable that reads the consent state and adjusts which tags fire accordingly.

The server-side advantage: You can still collect essential business metrics even when consent is denied for advertising cookies, by processing first-party data server-side.

## Testing & Verification

**1. Server Container Preview Mode**
Use GTM's server-side preview to verify events are being received and processed correctly. Look for:
- GA4 Client receiving events properly
- Event parameters being parsed correctly
- Tags firing with correct data

**2. GA4 Debug View**
Enable Debug Mode in GA4 to see server-side events in real-time:
- Events should show up within 30-60 seconds
- Verify `client_id` consistency between client and server events
- Check that Enhanced Measurement events are appearing

**3. GA4 Real-time Reports**
Monitor the real-time reports to confirm:
- User counts match expectations (accounting for ad blocker bypass)
- Event volumes are consistent with client-side baseline
- Attribution is working properly for conversion events

**4. Data Quality Checks**
Compare your server-side data to client-side for these metrics:
- **Session counts:** Should increase by 15-25% due to ad blocker bypass
- **Bounce rate:** May decrease slightly due to better event capture
- **Conversion attribution:** Should improve, especially for Safari users

**Acceptable variance:** Up to 5-10% difference in most metrics is normal during the transition period.

## Troubleshooting

**Problem:** Events showing up in server preview but not in GA4
→ Check your Measurement Protocol API Secret is correctly configured in the server-side GA4 tag. Also verify the Measurement ID matches exactly.

**Problem:** Client_ID mismatches causing duplicate users
→ Ensure your client-side gtag is sending the same `client_id` to both client-side and server-side destinations. Use GTM's built-in GA4 Client ID variable.

**Problem:** Enhanced Measurement events not working
→ Enhanced Measurement only works client-side by default. You need to explicitly configure server-side tags for scroll, file downloads, and video events.

**Problem:** Cross-domain tracking broken after server-side implementation
→ Verify that your server container is receiving the `client_id` parameter from all domains and forwarding it consistently to GA4.

**Problem:** Server container timing out or returning errors
→ Check your Cloud Run or server configuration for memory/CPU limits. GA4 events with large payloads (especially ecommerce) can cause timeouts.

**Problem:** Attribution windows shortened or broken
→ Ensure you're preserving the original timestamp and `page_referrer` information when processing events server-side.

## What To Do Next

Your server-side GA4 foundation is ready, but tracking gets more powerful when you layer in additional platforms:

- **[Server-Side GTM + Facebook Ads Setup](/tracking/server-side-gtm-facebook-ads)** — Send high-quality conversion data that bypasses iOS restrictions
- **[Server-Side GTM + Google Ads Setup](/tracking/server-side-gtm-google-ads)** — Improve attribution accuracy and conversion volume
- **[Server-Side GTM + LinkedIn Ads Setup](/tracking/server-side-gtm-linkedin-ads)** — Essential for B2B tracking with enhanced data quality

Need help auditing your current GA4 setup or implementing server-side tracking? [Get a free tracking audit](/contact) — I'll review your implementation and identify the biggest opportunities for improvement.

*This guide is part of the [Server-Side GTM Hub](/tracking/server-side-gtm) — your complete resource for implementing server-side tracking across all major platforms.*