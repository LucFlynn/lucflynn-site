---
title: "How to Send Typeform Leads to ActiveCampaign (Setup Guide)"
slug: "typeform-to-activecampaign"
description: "Connect Typeform to ActiveCampaign so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/activecampaign"
page_type: "spoke"
---

# Typeform → ActiveCampaign Integration Guide

I see this integration broken in about 35% of the setups I audit. Usually it's working for a few weeks, then silently fails when someone changes a field name in Typeform or the Zapier connection times out. You're getting leads, but they're not making it into your CRM — which means your sales team is flying blind and your follow-up sequences never trigger.

The most common failure point? Field mapping. Typeform uses dynamic field IDs, ActiveCampaign expects specific contact properties, and when these don't align perfectly, submissions just disappear into the void.

## What You'll Have Working By The End

- Every Typeform submission automatically creates a contact in ActiveCampaign
- Custom fields from your form (company, phone, etc.) mapped to the right ActiveCampaign properties
- Automatic tagging based on form responses to trigger the right automation sequences
- Error handling so you know when submissions fail to sync
- A testing process to verify everything's flowing correctly

## Prerequisites

- [ ] Admin access to your Typeform account (to create webhooks and view integrations)
- [ ] Admin access to ActiveCampaign (to create API keys and configure automation)
- [ ] Your ActiveCampaign API URL and key (found in Settings → Developer)
- [ ] List of which Typeform fields should map to which ActiveCampaign properties
- [ ] Zapier account if you're going the automation route (recommended for most setups)

## Method 1: Native ActiveCampaign Integration (Recommended)

Typeform has a direct integration with ActiveCampaign that handles the heavy lifting. This is the most reliable option for 90% of use cases.

In your Typeform, go to **Connect** tab → **Email Marketing** → **ActiveCampaign**. You'll need your ActiveCampaign API URL and key.

Your API URL looks like `https://youraccountname.api-us1.com` (find it in AC under Settings → Developer). Your API key is a long string in the same section.

Once connected, configure these settings:

- **Add to list**: Choose your main lead list or create a "Typeform Leads" list
- **Tags**: Add tags like "Typeform-Lead" and any form-specific tags
- **Field mapping**: This is where most setups break

For field mapping, match your Typeform questions to ActiveCampaign fields:
- Email question → Email (required)
- Name question → First Name or Full Name
- Company question → Company custom field
- Phone question → Phone custom field

The integration creates a new contact if the email doesn't exist, or updates the existing contact if it does. Tags get added either way.

**Key limitation**: The native integration doesn't support conditional logic based on form responses. If you need "add tag X only if they answered Y," you'll need Zapier.

## Method 2: Zapier Integration (Most Flexible)

This is what I recommend for complex forms or when you need conditional tagging/automation triggers.

Create a new Zap with:
- **Trigger**: Typeform → New Entry
- **Action**: ActiveCampaign → Create or Update Contact

In the trigger setup, connect your Typeform account and select your specific form. Zapier will pull in all your form fields automatically.

For the ActiveCampaign action:
- **Email**: Map to your email field (usually just "Email" from Typeform)
- **First Name**: Map to your name field
- **Last Name**: Split if you collected full name, or leave blank if you only have first name
- **Phone**: Map to phone field
- **Company**: Map to company field

Under **Tags**, you can add static tags like "Typeform-Lead" or dynamic tags based on responses. For example, if you have a dropdown asking about company size, you could add a tag like "Company-Size-{{Company Size}}" which would create tags like "Company-Size-1-10" or "Company-Size-50+".

**Custom Fields**: ActiveCampaign custom fields need to exist before you can map to them. Create them first in AC (Lists → Manage Fields) then map your Typeform fields to them in Zapier.

For conditional logic, add a **Filter** step between the trigger and action. For example, only create contacts if they selected "Yes" to a qualification question.

Turn on the Zap and test it with a real form submission.

## Method 3: Webhook + API Setup (For Developers)

If you need real-time syncing or want to avoid Zapier costs, you can use Typeform webhooks to push directly to ActiveCampaign's API.

In Typeform, go to your form → Connect → Webhooks. Set the endpoint URL to your server endpoint that will handle the webhook.

Typeform sends webhook data in this format:
```json
{
  "event_id": "01GX2TACBYQBX8QJ6N3QX8N8R8",
  "event_type": "form_response",
  "form_response": {
    "form_id": "abc123",
    "token": "def456",
    "submitted_at": "2024-03-24T15:30:00Z",
    "definition": {...},
    "answers": [
      {
        "field": {"id": "field_1", "type": "email"},
        "email": "user@example.com"
      },
      {
        "field": {"id": "field_2", "type": "short_text"},
        "text": "John Doe"
      }
    ]
  }
}
```

Your webhook endpoint needs to parse this data and POST to ActiveCampaign's contact API:

```javascript
// Basic webhook handler (Node.js example)
app.post('/typeform-webhook', async (req, res) => {
  const formResponse = req.body.form_response;
  
  // Extract field values
  const answers = formResponse.answers;
  const email = answers.find(a => a.field.type === 'email')?.email;
  const name = answers.find(a => a.field.id === 'field_2')?.text; // adjust field ID
  
  // Send to ActiveCampaign
  const acData = {
    contact: {
      email: email,
      firstName: name,
      fieldValues: [
        {
          field: "1", // Your custom field ID
          value: "Typeform Lead"
        }
      ]
    }
  };
  
  const response = await fetch(`${AC_API_URL}/api/3/contacts`, {
    method: 'POST',
    headers: {
      'Api-Token': AC_API_KEY,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(acData)
  });
  
  res.status(200).send('OK');
});
```

This approach requires server infrastructure but gives you complete control over the data flow and error handling.

## Testing & Verification

Submit a test entry to your Typeform with fake but realistic data. Within 30 seconds (native integration) or 2-5 minutes (Zapier), you should see:

1. **In ActiveCampaign**: New contact appears in your designated list with the correct field values and tags
2. **In Zapier** (if using): Check the Zap history to see the successful run
3. **In your email**: If you have an automation triggered by the tags, you should get the welcome email

Cross-check the field mapping by comparing what you submitted in Typeform to what appears in the ActiveCampaign contact record. Every mapped field should have the correct value.

**Acceptable delay**: Native integration is usually under 30 seconds. Zapier can take 2-15 minutes depending on your plan. Webhooks should be near-instant.

**Red flags**: If it takes longer than 15 minutes, something's broken. If fields are empty or contain placeholder text like "{{field_name}}", your mapping is misconfigured.

## Troubleshooting

**Problem**: Contact gets created but custom fields are empty  
Map your Typeform field to an existing ActiveCampaign custom field. If the AC field doesn't exist, create it first in Lists → Manage Fields. Field types must match (text to text, number to number).

**Problem**: Duplicate contacts being created instead of updating existing ones  
ActiveCampaign matches on email address. If your form collects email in a weird format (like "John <john@company.com>") or has extra spaces, it won't match. Use Zapier's Formatter to clean the email field before sending to AC.

**Problem**: Zapier says "Contact created" but nothing appears in ActiveCampaign  
Check if you're adding the contact to a specific list in your Zap action. If you don't specify a list, AC creates the contact but doesn't add them to any lists, making them hard to find. Always specify a list.

**Problem**: Integration worked for a week then stopped  
Usually this is Typeform field IDs changing when someone edits the form. If you reference fields by ID in Zapier, they break when the form is modified. Use field labels instead, or re-map after form changes.

**Problem**: Some submissions sync, others don't  
Probably hitting API rate limits or validation errors. In Zapier, check the error details in Zap history. Common issues: missing required fields, invalid phone number format, or email addresses that don't pass AC's validation.

**Problem**: Webhook endpoint receiving data but AC contact not being created  
Check your API request format against ActiveCampaign's v3 API docs. Most common issue: forgetting to wrap the contact data in a "contact" object, or using the wrong field IDs for custom fields.

## What To Do Next

Once your basic integration is working, consider these next steps:

- Set up [Typeform to HubSpot integration](/integrations/typeform-to-hubspot) if you're comparing CRMs
- Add [Typeform Google Ads conversion tracking](/tracking/typeform-google-ads-conversion-tracking) to measure form performance
- Configure similar flows for [Typeform to Salesforce](/integrations/typeform-to-salesforce) or [Typeform to GoHighLevel](/integrations/typeform-to-gohighlevel)
- Get a [free tracking audit](/contact) to identify other integration gaps in your funnel

*This guide is part of the [ActiveCampaign Integrations Hub](/integrations/activecampaign) — covering connections between ActiveCampaign and major form tools, landing page builders, and tracking systems.*