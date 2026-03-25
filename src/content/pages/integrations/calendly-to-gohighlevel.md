---
title: "How to Send Calendly Leads to GoHighLevel (Setup Guide)"
slug: "calendly-to-gohighlevel"
description: "Connect Calendly to GoHighLevel so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/gohighlevel"
page_type: "spoke"
---

# Calendly → GoHighLevel Integration Guide

I see this specific integration in about 30% of agency accounts I audit, and it's broken more often than it should be. Usually it's duplicate contacts piling up, webhooks that stopped firing three months ago, or — my personal favorite — leads going into GoHighLevel but not triggering the agency's automation sequences.

Most people set this up once, test it with their own email, see it work, and never check again. Then they wonder why their follow-up sequences feel inconsistent.

## What You'll Have Working By The End

- Every Calendly booking automatically creates a contact in GoHighLevel (no duplicates)
- All event details (date, time, event type) properly mapped to custom fields
- Leads automatically enter your nurture pipeline or automation sequence
- Webhook monitoring so you know when something breaks
- Fallback system for when the primary integration fails

## Prerequisites

- [ ] Admin access to your Calendly account (Professional plan or higher for webhooks)
- [ ] Agency or higher access to your GoHighLevel account
- [ ] Basic understanding of webhooks and API keys
- [ ] Access to Zapier account (if using that method)
- [ ] Test email address that isn't already in your GoHighLevel database

## Method 1: Native GoHighLevel Integration (Recommended)

Calendly has a direct integration with GoHighLevel that handles most use cases without third-party tools.

**Step 1: Connect in GoHighLevel**

1. In GoHighLevel, navigate to Settings → Integrations
2. Find "Calendly" in the available integrations list
3. Click "Connect" and authorize with your Calendly credentials
4. Select which Calendly events should sync to GoHighLevel
5. Map the event types to specific GoHighLevel pipelines

**Step 2: Configure Field Mapping**

The native integration handles basic fields automatically, but you'll want to customize:

- Event Name → Custom Field: "Event Type"
- Event Date/Time → Custom Field: "Appointment Date"
- Meeting URL → Custom Field: "Meeting Link"
- UTM parameters (if present) → Source/Medium fields

**Step 3: Pipeline Assignment**

In the integration settings, assign each Calendly event type to the appropriate GoHighLevel pipeline:

```
Sales Call → "Qualified Leads" pipeline, "New Appointment" stage
Demo Request → "Demo Pipeline", "Scheduled" stage
Support Call → "Customer Success", "Support Scheduled" stage
```

This is where most people mess up — they dump everything into the same pipeline and lose track of lead intent.

## Method 2: Zapier Integration (Most Flexible)

If you need more control over the data flow or the native integration doesn't cover your use case.

**Step 1: Create the Zap**

1. New Zap: Calendly "Invitee Created" → GoHighLevel "Create Contact"
2. Connect your Calendly account (requires Professional plan)
3. Select the specific event type(s) to monitor
4. Test the trigger with a recent booking

**Step 2: Configure GoHighLevel Action**

Map these fields carefully:

```javascript
// Required Fields
First Name: {{first_name}}
Last Name: {{last_name}}
Email: {{email}}
Phone: {{phone}} // if collected

// Custom Fields
Event Type: {{event_type_name}}
Event Date: {{start_time}}
Event Duration: {{duration}}
Meeting URL: {{join_url}}
Booking Source: "Calendly"
UTM Source: {{utm_source}} // if available
UTM Campaign: {{utm_campaign}} // if available
```

**Step 3: Add to Pipeline**

In the same Zap action:
- Pipeline: Select your target pipeline
- Stage: Set to "New Appointment" or equivalent
- Assigned User: Set to the meeting host or round-robin

**Step 4: Enable Error Handling**

Add a filter step: Only continue if email address is not empty. I've seen too many Zaps create contacts with no email because someone tested with incomplete data.

## Method 3: Webhook + API Integration (Advanced)

For agencies managing multiple clients or needing real-time sync without Zapier costs.

**Step 1: Set Up Calendly Webhook**

1. In Calendly, go to Integrations & Apps → Webhooks
2. Create new webhook endpoint: `https://your-server.com/calendly-webhook`
3. Subscribe to these events:
   - `invitee.created`
   - `invitee.canceled` (to handle cancellations)

**Step 2: Webhook Handler Code**

```javascript
// Express.js webhook handler
app.post('/calendly-webhook', async (req, res) => {
  const event = req.body;
  
  if (event.event === 'invitee.created') {
    const invitee = event.payload;
    
    // Prepare GoHighLevel contact data
    const contactData = {
      firstName: invitee.first_name,
      lastName: invitee.last_name,
      email: invitee.email,
      phone: invitee.phone || '',
      customFields: {
        'Event Type': invitee.event_type_name,
        'Event Date': invitee.start_time,
        'Meeting URL': invitee.join_url,
        'Booking Source': 'Calendly'
      }
    };
    
    // Send to GoHighLevel
    await createGHLContact(contactData);
  }
  
  res.status(200).send('OK');
});

async function createGHLContact(data) {
  const response = await fetch(`https://rest.gohighlevel.com/v1/contacts/`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.GHL_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  });
  
  return response.json();
}
```

**Step 3: Handle Duplicates**

GoHighLevel will create duplicates by default. Add a check:

```javascript
// Check if contact exists first
const existingContact = await fetch(`https://rest.gohighlevel.com/v1/contacts/lookup?email=${data.email}`, {
  headers: { 'Authorization': `Bearer ${process.env.GHL_API_KEY}` }
});

if (existingContact.status === 200) {
  // Update existing contact instead
  await updateGHLContact(existingContact.id, data);
} else {
  // Create new contact
  await createGHLContact(data);
}
```

## Testing & Verification

**Test the Integration:**

1. Book a test appointment using an email not in your GoHighLevel database
2. Check that the contact appears in GoHighLevel within 2-3 minutes
3. Verify all custom fields populated correctly
4. Confirm the contact entered the right pipeline/stage
5. Test a cancellation to ensure it updates the contact status

**Check the Numbers:**

Compare Calendly bookings vs GoHighLevel contacts over a 7-day period:
- Acceptable variance: 5-10% (some people book and immediately cancel)
- Red flag: More than 15% variance indicates integration issues
- Check for duplicate contacts with the same email but different capitalization

**Monitor Webhook Health:**

If using webhooks, monitor the endpoint response codes:
- 200 responses: Integration working
- 4xx/5xx errors: Check authentication and endpoint availability
- Missing webhooks: Calendly stops sending after 10 consecutive failures

## Troubleshooting

**Problem:** Contacts appear in GoHighLevel but don't enter automation sequences.

Check your pipeline settings — automation triggers need to be set to "Contact enters stage" not just "Contact created." Most agencies forget this step.

**Problem:** Duplicate contacts being created for the same person.

GoHighLevel matches on exact email. If someone books with "john@company.com" and later with "John@Company.com", you'll get duplicates. Add email normalization to your webhook handler or use Zapier's formatter step.

**Problem:** Custom fields showing as empty even though data exists in Calendly.

Field mapping case sensitivity. GoHighLevel custom field names must match exactly. "Event Type" ≠ "event type" ≠ "Event_Type".

**Problem:** Webhooks stopped working and leads aren't syncing.

Calendly disables webhook endpoints after 10 consecutive failures. Check your server logs for 500 errors around the time it stopped working. Re-enable the webhook in Calendly after fixing the endpoint.

**Problem:** UTM parameters not capturing properly.

Calendly only passes UTM parameters if they were present when the booking page loaded. If someone shares a direct Calendly link without UTMs, you won't capture the source. Consider adding a hidden field to your booking form for lead source.

**Problem:** Time zone confusion in GoHighLevel appointments.

Calendly sends times in UTC. Make sure your GoHighLevel automation accounts for time zone conversion, especially if you're triggering reminder sequences based on appointment time.

## What To Do Next

Once your Calendly → GoHighLevel integration is running smoothly, consider these related setups:

- [GoHighLevel Integration Hub](/integrations/gohighlevel) — Connect other lead sources to GHL
- [Calendly to HubSpot Integration](/integrations/calendly-to-hubspot) — Alternative CRM setup
- [Calendly Google Ads Conversion Tracking](/tracking/calendly-google-ads-conversion-tracking) — Track booking conversions
- [Get a free tracking audit](/contact) — I'll review your current integration setup

*This guide is part of the [GoHighLevel Integration Hub](/integrations/gohighlevel) — step-by-step guides for connecting your lead sources to GoHighLevel's CRM and automation platform.*