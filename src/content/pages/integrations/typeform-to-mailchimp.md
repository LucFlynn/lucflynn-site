---
title: "How to Send Typeform Leads to Mailchimp (Setup Guide)"
slug: "typeform-to-mailchimp"
description: "Connect Typeform to Mailchimp so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/mailchimp"
page_type: "spoke"
---

# Typeform → Mailchimp Integration Guide

I see this integration broken in about 30% of the Typeform accounts I audit. Usually it's because someone set up the native integration months ago, then changed their Mailchimp audience structure without updating the form mapping. Suddenly half their leads are landing in the wrong list or getting tagged incorrectly.

The other common failure mode? Zapier connections that worked fine for 6 months, then quietly started failing because someone hit their task limit or the authentication expired. Meanwhile, nobody noticed because the form still "worked" — it just stopped sending leads anywhere.

## What You'll Have Working By The End

- Every Typeform submission automatically creates or updates a contact in your chosen Mailchimp audience
- Proper field mapping so form data lands in the right Mailchimp fields and tags
- Error handling so you know when leads aren't making it through
- A testing process to verify the integration after any changes

## Prerequisites

- [ ] Admin access to your Typeform account
- [ ] Admin access to your Mailchimp account (need to create integrations)
- [ ] At least one published Typeform ready to connect
- [ ] The Mailchimp audience/list where you want leads to go

## Step 1: Set Up The Native Typeform → Mailchimp Integration

Typeform has a native Mailchimp integration that works for most basic setups. Start here unless you need complex field mapping or conditional logic.

In your Typeform:

1. Go to **Connect** tab → **Email marketing** → **Mailchimp**
2. Click **Connect account** and authenticate with Mailchimp
3. Select your target audience from the dropdown
4. Map your form fields to Mailchimp fields:
   - Email question → Email Address (required)
   - Name questions → First Name/Last Name merge fields
   - Phone → Phone Number merge field
   - Custom questions → Custom merge fields (create these in Mailchimp first)

5. Set up tags if needed — these help segment your leads
6. Choose **Double opt-in** setting (I recommend enabling this for compliance)

The native integration handles about 80% of standard lead capture needs. It breaks when you need conditional field mapping, multiple audience routing, or complex data transformation.

**When to skip the native integration:** If you need leads to go to different Mailchimp audiences based on form responses, or if you're collecting data that needs processing before hitting Mailchimp (like splitting full names into first/last).

## Step 2: Alternative — Zapier Integration Setup

If the native integration doesn't meet your needs, Zapier gives you more control over field mapping and routing logic.

Create a new Zap:

1. **Trigger:** Typeform → "New Entry"
2. Connect your Typeform account and select the specific form
3. **Action:** Mailchimp → "Add/Update Subscriber"
4. Connect Mailchimp and select your audience

**Field Mapping in Zapier:**
- Map Email from Typeform to Email Address in Mailchimp
- Map other fields to corresponding merge fields
- Use Zapier's formatter if you need to transform data (like extracting first name from a full name field)

**Advanced Zapier Setup:**
- Add **Filter** steps to route different responses to different audiences
- Use **Paths** to handle conditional logic (e.g., B2B leads go to one list, B2C to another)
- Add **Delay** if you're hitting API rate limits

I see Zapier integrations fail most often due to authentication expiring or task limits being hit. Set up email notifications for Zap failures.

## Step 3: Webhook + API Approach (For Developers)

If you need real-time processing or custom logic, use Typeform webhooks with Mailchimp's API.

**Typeform Webhook Setup:**

1. In Typeform, go to **Connect** → **Webhooks**
2. Add your endpoint URL (e.g., `https://yourserver.com/typeform-webhook`)
3. Select which events to send (usually just "form_response")

**Webhook Payload Example:**
```json
{
  "event_id": "01234567890",
  "event_type": "form_response",
  "form_response": {
    "form_id": "abc123",
    "submitted_at": "2026-03-24T10:30:00Z",
    "definition": {
      "fields": [
        {
          "id": "field_1",
          "title": "Email address",
          "type": "email"
        }
      ]
    },
    "answers": [
      {
        "field": {
          "id": "field_1",
          "type": "email"
        },
        "email": "test@example.com"
      }
    ]
  }
}
```

**Server-Side Processing (Node.js example):**
```javascript
app.post('/typeform-webhook', async (req, res) => {
  const response = req.body.form_response;
  
  // Extract email and other fields
  const email = response.answers.find(a => a.field.type === 'email')?.email;
  const firstName = response.answers.find(a => a.field.id === 'field_2')?.text;
  
  // Send to Mailchimp
  const mailchimpData = {
    email_address: email,
    status: 'subscribed',
    merge_fields: {
      FNAME: firstName
    }
  };
  
  try {
    await mailchimp.lists.addListMember(audienceId, mailchimpData);
    res.status(200).send('OK');
  } catch (error) {
    console.error('Mailchimp error:', error);
    res.status(500).send('Error');
  }
});
```

This approach gives you complete control but requires maintaining server infrastructure and error handling.

## Step 4: Field Mapping Best Practices

**Standard Field Mapping:**
- Typeform Email → Mailchimp Email Address
- Typeform Short Text "First Name" → Mailchimp FNAME
- Typeform Short Text "Last Name" → Mailchimp LNAME  
- Typeform Phone Number → Mailchimp PHONE
- Typeform Website → Mailchimp custom merge field

**For Complex Forms:**
Create custom merge fields in Mailchimp first, then map them. Go to **Audience** → **Settings** → **Audience fields and merge tags** to add custom fields.

Common custom fields I set up:
- COMPANY (Company name)
- JOBTITLE (Job title)
- BUDGET (Budget range from dropdown)
- SOURCE (UTM source if you're tracking it)

**Tagging Strategy:**
Use tags to segment leads based on form responses. For example:
- Form response "Budget: $10k+" → Mailchimp tag "high-value-lead"  
- Form response "Industry: SaaS" → Mailchimp tag "saas-prospect"

## Testing & Verification

**Test the integration every time you make changes:**

1. Submit a test form entry with fake but realistic data
2. Check Mailchimp within 5 minutes — native integration is usually instant, Zapier can take 1-15 minutes
3. Verify the contact landed in the right audience with correct field data
4. Check that tags were applied correctly

**Cross-check the numbers weekly:**
Compare Typeform submission count vs. new Mailchimp subscribers. They should match within 5-10% (some variance is normal due to duplicates and bounced emails).

**Red flags that indicate problems:**
- Submissions in Typeform but no new Mailchimp contacts
- Contacts created but missing field data
- All contacts ending up with identical tag sets
- Sudden drop in integration volume without corresponding drop in form traffic

## Troubleshooting

**Problem:** Forms are submitting but no contacts appear in Mailchimp
Check if the integration is still connected. Native integrations can disconnect if someone changes passwords or permissions. In Typeform, go to Connect tab and look for any authentication warnings.

**Problem:** Contacts are created but missing field data  
Field mapping broke, usually because someone renamed fields in either Typeform or Mailchimp. Re-map the fields in your integration settings. For Zapier, check if any custom merge fields were deleted in Mailchimp.

**Problem:** Getting duplicate contacts for the same email
Mailchimp should automatically handle duplicates, but if you're seeing multiple entries, check if you have multiple integrations running simultaneously (e.g., both native integration AND Zapier). Turn off the duplicate connection.

**Problem:** Webhook integration stopped working
Check your webhook endpoint logs for errors. Common issues: server downtime, API rate limiting, or webhook URL changed. Typeform will show webhook delivery failures in the Connect tab.

**Problem:** Only some form fields are syncing
Usually a field mapping issue. Check that all Typeform fields are mapped to existing Mailchimp merge fields. If you're using conditional logic, verify that all paths have proper field mapping configured.

**Problem:** Double opt-in emails not sending
Check Mailchimp's compliance settings and your audience double opt-in configuration. If you enabled double opt-in in the integration but disabled it at the audience level, contacts will be added as "pending" and never confirmed.

## What To Do Next

Now that your Typeform leads are flowing into Mailchimp, consider these related integrations:

- **[Typeform → HubSpot Integration](/integrations/typeform-to-hubspot)** — Better for complex lead scoring and sales handoff
- **[Typeform → Salesforce Integration](/integrations/typeform-to-salesforce)** — If you need full CRM functionality beyond email marketing
- **[Typeform → GoHighLevel Integration](/integrations/typeform-to-gohighlevel)** — All-in-one CRM and marketing automation

Want me to audit your current tracking setup for free? **[Get a tracking audit](/contact)** — I'll check for integration gaps and missed conversion opportunities.

Also check out **[Typeform Google Ads Conversion Tracking](/tracking/typeform-google-ads-conversion-tracking)** to make sure you're tracking these form submissions as conversions for your ad campaigns.

*This guide is part of the [Mailchimp Integrations Hub](/integrations/mailchimp) — comprehensive guides for connecting your lead sources to Mailchimp's email marketing platform.*