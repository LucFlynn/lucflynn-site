---
title: "How to Send Calendly Leads to HubSpot (Setup Guide)"
slug: "calendly-to-hubspot"
description: "Connect Calendly to HubSpot so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/hubspot"
page_type: "spoke"
---

# Calendly → HubSpot Integration Guide

I see this connection broken in about 30% of the accounts I audit — usually because someone set it up once and never tested what happens when Calendly fields change or HubSpot properties get updated. You're booking meetings but losing the lead data, or worse, creating duplicate contacts that mess up your attribution.

## What You'll Have Working By The End

- Every Calendly booking automatically creates or updates a contact in HubSpot
- Meeting details, custom questions, and UTM parameters flowing into the right HubSpot properties
- Lead source attribution showing Calendly as the origin
- Automated workflows triggered by new bookings
- A testing process to verify leads aren't getting lost

## Prerequisites

- [ ] Admin access to your Calendly account (Professional plan or higher for webhooks)
- [ ] Super Admin or Marketing Hub Admin access in HubSpot
- [ ] Access to your Zapier account (if using method 2)
- [ ] Developer access if going the webhook route
- [ ] List of custom fields you're collecting in Calendly that need to map to HubSpot

## Method 1: Native HubSpot Integration

Calendly has a direct integration with HubSpot that handles most use cases. Start here unless you need custom field mapping that the native connector doesn't support.

In your Calendly account:

1. Go to **Integrations** → **CRM & Sales**
2. Click **Connect** next to HubSpot
3. Authenticate with your HubSpot account (use an admin account)
4. Choose which event types to sync — I recommend starting with all of them
5. Map your Calendly questions to HubSpot contact properties

The field mapping is where most people mess this up. Here's what I typically see:

- **Name** → `firstname` and `lastname` (HubSpot auto-splits)
- **Email** → `email` 
- **Phone** → `phone`
- **Company** → `company`
- **Custom Question 1** → Create a custom property in HubSpot first

For lead source tracking, the integration automatically sets:

- **Original Source** → "Other Campaigns"
- **Lead Source** → "Calendly"
- **Source** → The specific Calendly event type name

Test this by booking a test meeting with yourself using a different email. The contact should appear in HubSpot within 2-3 minutes with all the mapped fields populated.

## Method 2: Zapier Connection

Use this if the native integration doesn't support your field mapping needs or if you want more control over the workflow.

### Setting Up the Zap

1. **Trigger**: Calendly → "Invitee Created"
2. **Action**: HubSpot → "Create or Update Contact"

In the Zapier trigger setup:

- Connect your Calendly account
- Choose "Any Event Type" unless you only want specific events
- Test the trigger by booking a meeting

In the HubSpot action:

Map these fields (customize based on your Calendly questions):

```
Email: {{invitee_email}}
First Name: {{invitee_first_name}}
Last Name: {{invitee_last_name}}
Phone: {{invitee_phone_number}}
Lead Source: Calendly
Meeting Date: {{event_start_time}}
Meeting Type: {{event_type_name}}
Calendly Link: {{invitee_cancel_url}}
```

For custom properties, you'll need to create them in HubSpot first. Go to **Settings** → **Properties** → **Contact Properties** and create properties that match your Calendly questions.

The Zapier approach gives you more flexibility for data transformation. For example, if Calendly collects "Budget Range" but you want to store it as a numeric value in HubSpot, you can add a Formatter step.

## Method 3: Webhook + API Integration

This is for teams with development resources who need real-time data flow and complex field mapping logic.

### Calendly Webhook Setup

In Calendly, go to **Integrations** → **API & Webhooks**:

1. Create a new webhook subscription
2. Set the endpoint URL to your server
3. Subscribe to `invitee.created` and `invitee.canceled` events
4. Save the webhook signing key for verification

### Webhook Payload Example

When someone books a meeting, Calendly sends this payload:

```json
{
  "created_at": "2026-03-24T15:30:45.123456Z",
  "created_by": "https://api.calendly.com/users/ABCD1234",
  "event": "invitee.created",
  "payload": {
    "email": "lead@company.com",
    "first_name": "John",
    "last_name": "Doe",
    "name": "John Doe",
    "status": "active",
    "timezone": "America/New_York",
    "event": {
      "uuid": "EVENT123",
      "assigned_to": ["https://api.calendly.com/users/ABCD1234"],
      "event_type": {
        "name": "Discovery Call",
        "slug": "discovery-call"
      },
      "start_time": "2026-03-24T16:00:00.000000Z",
      "end_time": "2026-03-24T16:30:00.000000Z"
    },
    "questions_and_answers": [
      {
        "question": "What's your biggest challenge?",
        "answer": "Lead generation"
      }
    ],
    "tracking": {
      "utm_campaign": "google-ads",
      "utm_source": "google",
      "utm_medium": "cpc"
    }
  }
}
```

### HubSpot API Integration

Send the lead data to HubSpot using their Contacts API:

```javascript
const hubspotContact = {
  properties: {
    email: payload.email,
    firstname: payload.first_name,
    lastname: payload.last_name,
    phone: payload.phone_number,
    company: getAnswerByQuestion('Company Name'),
    hs_lead_status: 'NEW',
    calendly_event_type: payload.event.event_type.name,
    calendly_meeting_time: payload.event.start_time,
    utm_campaign: payload.tracking.utm_campaign,
    utm_source: payload.tracking.utm_source,
    utm_medium: payload.tracking.utm_medium
  }
};

// Create or update contact
const response = await fetch('https://api.hubapi.com/crm/v3/objects/contacts', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${hubspotAccessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(hubspotContact)
});
```

The webhook approach lets you handle complex logic like:
- Creating deals automatically based on meeting type
- Setting different lead sources based on UTM parameters  
- Triggering custom workflows based on answers to specific questions

## Testing & Verification

### Verify in Calendly
1. Book a test meeting using a unique email address
2. Check the webhook logs (if using Method 3) or Zapier task history (if using Method 2)
3. Confirm the event fired and data was captured

### Verify in HubSpot
1. Search for the test contact by email
2. Check that all mapped fields populated correctly
3. Verify the contact source shows "Calendly" 
4. Confirm any automated workflows triggered

### Cross-Check the Data
Book 5 test meetings and verify all 5 appear in HubSpot. Acceptable sync time:
- **Native integration**: 2-5 minutes
- **Zapier**: 1-15 minutes depending on your plan
- **Webhook**: Near real-time (under 30 seconds)

If you're missing more than 5% of bookings after 24 hours, something's broken.

### Red Flags
- Contacts created without email addresses (usually a field mapping issue)
- Multiple contacts for the same person (duplicate detection not working)
- Missing UTM parameters (tracking data not flowing through)
- No activity timeline showing the Calendly booking

## Troubleshooting

**Problem**: Contacts are being created but custom question answers aren't mapping
→ Check that you've created the custom properties in HubSpot first. The integration can't create properties on the fly — they need to exist before mapping.

**Problem**: Getting duplicate contacts instead of updating existing ones
→ In HubSpot, go to **Settings** → **Objects** → **Contacts** and verify that email is set as the primary unique identifier. Also check if you have multiple Calendly integrations running simultaneously.

**Problem**: Zapier shows successful but contact doesn't appear in HubSpot
→ Check the Zapier task details for HubSpot API errors. Usually it's a field type mismatch (trying to send text to a number field) or required fields not being populated.

**Problem**: Webhooks stop working after a few weeks
→ Calendly webhooks expire if they return errors consistently. Check your webhook endpoint logs for 4xx/5xx responses. Common cause: SSL certificate expired or server went down.

**Problem**: Meeting attendee info updates in Calendly but not HubSpot
→ Most integrations only trigger on `invitee.created`, not `invitee.updated`. You'll need to subscribe to both webhook events or manually sync updates.

**Problem**: UTM parameters from the booking page aren't flowing through
→ Make sure you're capturing tracking data in your Calendly embed code and that your integration is mapping the `tracking` object fields to HubSpot UTM properties.

## What To Do Next

Once your Calendly leads are flowing into HubSpot, you'll want to set up proper attribution tracking. Check out [Calendly Google Ads Conversion Tracking](/tracking/calendly-google-ads-conversion-tracking) to connect your bookings back to ad spend.

For other CRM connections, see [Calendly to Salesforce](/integrations/calendly-to-salesforce), [Calendly to GoHighLevel](/integrations/calendly-to-gohighlevel), or [Calendly to ActiveCampaign](/integrations/calendly-to-activecampaign).

Need help auditing your current setup? I offer a [free tracking audit](/contact) where I'll check for missing leads, duplicate contacts, and broken attribution.

*This guide is part of the [HubSpot Integrations Hub](/integrations/hubspot) — complete setup guides for connecting your forms, surveys, and lead capture tools to HubSpot.*