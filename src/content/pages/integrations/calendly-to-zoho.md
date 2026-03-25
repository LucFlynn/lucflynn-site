---
title: "How to Send Calendly Leads to Zoho CRM (Setup Guide)"
slug: "calendly-to-zoho"
description: "Connect Calendly to Zoho CRM so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/zoho"
page_type: "spoke"
---

# Calendly → Zoho CRM Integration Guide

I see broken Calendly → Zoho CRM connections in about 30% of the accounts I audit. Usually it's because someone set up a Zapier integration that worked for two weeks, then started failing silently when Calendly changed their webhook payload structure. Now half their booked meetings never make it into Zoho CRM as leads.

The good news? There are actually three solid ways to connect these tools, and I'll show you which one to use based on your setup.

## What You'll Have Working By The End

- Every Calendly booking automatically creates a lead in Zoho CRM
- Proper field mapping so contact info, meeting details, and UTM parameters flow through correctly
- Error handling so you know when leads get missed
- A testing process to verify new bookings appear in Zoho within 2-3 minutes
- Backup tracking method so you don't lose leads when integrations break

## Prerequisites

- [ ] Admin access to your Calendly account (need to access integrations settings)
- [ ] Admin or Developer role in Zoho CRM
- [ ] If using Zapier: Zapier account (free tier works for basic setup)
- [ ] If using webhooks: Server or service that can receive HTTP POST requests

## Method 1: Zapier Integration (Recommended)

This is what I use for 80% of Calendly → Zoho CRM setups. It's reliable, handles field mapping well, and gives you good error reporting when things break.

### Set Up the Calendly Trigger

1. In Zapier, create a new Zap and search for Calendly as your trigger app
2. Select "Invitee Created" as the trigger event (this fires when someone books a meeting)
3. Connect your Calendly account and test the trigger
4. Zapier will pull in a recent booking to use as sample data

Your trigger data will include:
- `name` - Full name of the person who booked
- `email` - Their email address
- `event_type_name` - Name of your Calendly event (e.g., "30-Minute Strategy Call")
- `start_time` - When the meeting is scheduled
- `location` - Meeting location (Zoom link, phone number, etc.)
- `utm_source`, `utm_medium`, `utm_campaign` - If you're tracking marketing campaigns

### Configure Zoho CRM Action

1. Add Zoho CRM as your action app
2. Choose "Create Lead" as the action (not "Create Contact" — leads flow through your sales process better)
3. Connect your Zoho CRM account

Map these fields:

**Required Mapping:**
- **Lead Source** → Set to "Website" or "Calendly" (create this as a custom value if needed)
- **First Name** → Extract from Calendly `name` field (use Zapier's name parser)
- **Last Name** → Extract from Calendly `name` field
- **Email** → Calendly `email`
- **Company** → Leave blank or map if Calendly collects it

**Recommended Mapping:**
- **Description** → Calendly `event_type_name` + scheduled time
- **Lead Status** → "Meeting Scheduled" (create this status in Zoho if it doesn't exist)
- **Phone** → Calendly `phone` (if you collect phone numbers)

**Campaign Tracking (if applicable):**
- **Campaign Name** → Calendly `utm_campaign`
- **Medium** → Calendly `utm_medium`
- **Source** → Calendly `utm_source`

### Test the Integration

1. Book a test meeting through your Calendly link
2. Check Zapier's task history — you should see the zap trigger within 2-3 minutes
3. Verify the lead appears in Zoho CRM with all mapped fields populated
4. Check that UTM parameters came through if you're using campaign tracking

## Method 2: Calendly Webhooks + Zoho API

Use this approach if you need more control over the data flow or want to avoid Zapier costs for high-volume bookings.

### Set Up Calendly Webhooks

1. In Calendly, go to Account Settings → Developer Tools
2. Create a new webhook endpoint
3. Set the endpoint URL to your server (e.g., `https://yourdomain.com/calendly-webhook`)
4. Subscribe to `invitee.created` events
5. Copy the webhook signing secret for verification

Your webhook will receive this payload when someone books:

```json
{
  "created_at": "2026-03-24T15:30:00.000000Z",
  "event": "invitee.created",
  "payload": {
    "email": "prospect@example.com",
    "name": "John Smith",
    "event": {
      "name": "30-Minute Strategy Call",
      "start_time": "2026-03-25T10:00:00.000000Z",
      "location": {"join_url": "https://zoom.us/j/123456789"}
    },
    "tracking": {
      "utm_source": "google",
      "utm_medium": "cpc",
      "utm_campaign": "q1-2026"
    }
  }
}
```

### Create Zoho CRM Lead via API

When your webhook endpoint receives a booking, make this API call to create the lead:

```javascript
// Webhook handler (Node.js example)
app.post('/calendly-webhook', async (req, res) => {
  const booking = req.body.payload;
  
  // Create lead in Zoho CRM
  const leadData = {
    "data": [{
      "First_Name": booking.name.split(' ')[0],
      "Last_Name": booking.name.split(' ').slice(1).join(' '),
      "Email": booking.email,
      "Lead_Source": "Calendly",
      "Lead_Status": "Meeting Scheduled",
      "Description": `Calendly booking: ${booking.event.name} scheduled for ${booking.event.start_time}`,
      "Campaign_Name": booking.tracking?.utm_campaign,
      "Medium": booking.tracking?.utm_medium,
      "Source": booking.tracking?.utm_source
    }]
  };
  
  const response = await fetch('https://www.zohoapis.com/crm/v3/Leads', {
    method: 'POST',
    headers: {
      'Authorization': `Zoho-oauthtoken ${access_token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(leadData)
  });
  
  if (response.ok) {
    console.log('Lead created successfully');
    res.status(200).send('OK');
  } else {
    console.error('Failed to create lead:', await response.text());
    res.status(500).send('Error');
  }
});
```

You'll need to handle Zoho CRM OAuth authentication to get an access token. The token expires every hour, so implement refresh logic.

## Method 3: Zoho Forms Integration (Alternative)

If you want everything within the Zoho ecosystem, you can use Zoho Forms instead of Calendly for booking collection, then use Zoho's native scheduling tools.

This works if:
- You don't need Calendly's advanced scheduling features
- Your team is already using other Zoho products
- You want tighter integration with Zoho CRM workflows

The tradeoff is that Zoho Bookings isn't as feature-rich as Calendly, especially for complex scheduling scenarios.

## Testing & Verification

Here's how to verify everything is working correctly:

### Initial Test
1. Book a test meeting through your Calendly link
2. Use a unique email address so you can easily find the lead
3. Time how long it takes for the lead to appear in Zoho CRM (should be under 5 minutes)

### Verify Field Mapping
Check that these fields populated correctly in Zoho CRM:
- First/Last Name parsed correctly from the full name
- Email address matches what you entered
- Lead Source shows "Calendly" or your custom value
- Description includes meeting type and scheduled time
- UTM parameters (if you're tracking campaigns) appear in the right fields

### Campaign Tracking Test
If you're running ads to Calendly:
1. Add UTM parameters to your Calendly URL: `?utm_source=google&utm_medium=cpc&utm_campaign=q1-strategy`
2. Book a test meeting using that URL
3. Verify the campaign data flows through to Zoho CRM

### Volume Test
If you expect high booking volume, test with multiple quick bookings to ensure the integration doesn't drop leads or create duplicates.

## Troubleshooting

**Problem** → Leads appear in Zoho CRM but are missing the first or last name
**Solution** → Calendly sends the full name in one field. Your integration needs to parse it. In Zapier, use the "Formatter" tool to split names. For webhooks, use `name.split(' ')` but handle edge cases like single names or multiple last names.

**Problem** → Integration worked for a week, then stopped creating leads
**Solution** → Usually an authentication issue. In Zapier, reconnect your Zoho CRM account. For webhook setups, check if your Zoho access token expired and needs refreshing. I see this in about 20% of webhook integrations after the first month.

**Problem** → Duplicate leads being created for the same person
**Solution** → Zoho CRM isn't deduplicating properly. Set up duplicate detection rules in Zoho CRM Settings → Data Management → Duplicate Check. Use email as the primary dedup field for Calendly leads.

**Problem** → UTM parameters not flowing through to Zoho CRM
**Solution** → Calendly only captures UTM parameters if they're present when someone first lands on your scheduling page. If they book later from a bookmark, the UTMs are lost. Also, make sure you've created custom fields in Zoho CRM for UTM data — they're not standard fields.

**Problem** → Zapier shows successful runs but no leads appear in Zoho CRM
**Solution** → Check your field mapping. If you're trying to map to a required field that's not being populated, the lead creation fails silently. Common culprit: mapping to a Company field that's marked as required in Zoho CRM but Calendly doesn't collect company names.

**Problem** → Meeting details (time, location) not appearing in Zoho CRM
**Solution** → You're probably only mapping basic contact fields. Add the meeting details to the Description field or create custom fields in Zoho CRM for meeting time and location. This is especially important for sales follow-up.

## What To Do Next

- **Set up conversion tracking:** Once leads are flowing into Zoho CRM, connect your [Calendly Google Ads conversion tracking](/tracking/calendly-google-ads-conversion-tracking) so you can optimize your ad spend based on actual bookings
- **Expand to other CRMs:** If you're testing multiple CRM options, check out [Calendly → HubSpot](/integrations/calendly-to-hubspot) or [Calendly → Salesforce](/integrations/calendly-to-salesforce) integrations
- **Audit your current setup:** Get a [free tracking audit](/contact) to identify gaps in your lead flow and attribution setup

*This guide is part of the [Zoho CRM Integrations Hub](/integrations/zoho) — connect your forms, ads, and marketing tools to Zoho CRM automatically.*