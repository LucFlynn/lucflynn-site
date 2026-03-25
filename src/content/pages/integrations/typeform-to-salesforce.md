---
title: "How to Send Typeform Leads to Salesforce (Setup Guide)"
slug: "typeform-to-salesforce"
description: "Connect Typeform to Salesforce so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/salesforce"
page_type: "spoke"
---

# Typeform → Salesforce Integration Guide

I see this integration broken in about 30% of the Salesforce orgs I audit. Usually it's field mapping gone wrong — Typeform sends "email" but Salesforce expects "Email__c", or someone set up the integration to create Contacts instead of Leads and screwed up the sales funnel.

The good news is there are three solid ways to connect these tools, and I'll walk you through each one so you can pick what fits your technical comfort level.

## What You'll Have Working By The End

- Every Typeform submission automatically creates a Lead in Salesforce
- Custom fields from your Typeform mapped to the right Salesforce fields  
- Lead source tracking so you know which forms are converting
- Error handling so you don't lose leads when something breaks
- A testing process to verify everything works before going live

## Prerequisites

- [ ] Admin access to your Salesforce org
- [ ] Admin access to your Typeform account (Professional plan or higher for webhooks)
- [ ] Your Salesforce Lead object field API names (Setup → Object Manager → Lead → Fields)
- [ ] Decision made: creating Leads or Contacts? (Leads is usually right for marketing forms)

## Method 1: Native Typeform → Salesforce Integration

Typeform has a native Salesforce integration, but it's buried in the integrations menu and honestly pretty limited.

Go to your Typeform dashboard → Connect → Salesforce. You'll need to authenticate your Salesforce org and grant permissions.

The native integration only maps to standard Salesforce fields:
- First Name → FirstName
- Last Name → LastName  
- Email → Email
- Phone → Phone
- Company → Company

**Problem with this approach:** No custom field mapping, no lead source tracking, and it creates Leads by default (which might be what you want, but you can't change it).

I only recommend this for dead-simple setups. If you need custom fields or lead source attribution, skip to Method 2.

## Method 2: Zapier Integration (Recommended)

This is what I set up for most clients. More flexible than native, easier than webhooks.

### Setting Up the Zap

Create a new Zap with Typeform as trigger, Salesforce as action.

**Trigger Setup:**
1. Choose "New Entry" as your trigger
2. Connect your Typeform account  
3. Select your specific form from the dropdown
4. Test the trigger by submitting a test form entry

**Action Setup:**
1. Choose "Create Record" in Salesforce
2. Set Object Type to "Lead" (not Contact, unless you have a specific reason)
3. Map your fields:

```
Typeform Field → Salesforce Field
First Name → First Name
Last Name → Last Name
Email → Email
Phone → Phone
Company → Company
Lead Source → "Typeform - [Form Name]"
```

**Custom Field Mapping:**
This is where most people mess up. You need the API names from Salesforce, not the display names.

In Salesforce: Setup → Object Manager → Lead → Fields & Relationships

Find your custom field and copy the API Name. It'll look like `Custom_Field__c`.

In Zapier, scroll down to find your custom fields in the dropdown. If you don't see them, click "Show all fields" or type the API name manually.

### Lead Source Best Practices

Set up your Lead Source field like this:
- Static text: "Typeform"  
- Dynamic text: Form title from Typeform
- Result: "Typeform - Contact Us Form"

This gives you clean reporting in Salesforce later.

Turn on the Zap and test it with a real form submission.

## Method 3: Webhook + Salesforce API

For high-volume forms or complex field mapping, webhooks give you the most control.

### Setting Up Typeform Webhooks

In your Typeform: Connect → Webhooks → Add webhook

Your webhook URL will be your server endpoint that receives the POST data and sends it to Salesforce.

Typeform sends data in this format:
```json
{
  "event_id": "abc123",
  "event_type": "form_response",
  "form_response": {
    "form_id": "xyz789",
    "answers": [
      {
        "field": {"id": "field_id", "type": "short_text"},
        "text": "John Doe"
      }
    ]
  }
}
```

### Processing the Webhook

Your server needs to:
1. Receive the POST from Typeform
2. Parse the answers array to extract field values
3. Map to Salesforce fields
4. Send to Salesforce REST API

Here's the Salesforce API call structure:
```javascript
const leadData = {
  FirstName: extractedFirstName,
  LastName: extractedLastName,
  Email: extractedEmail,
  Company: extractedCompany,
  LeadSource: 'Typeform - Contact Form'
};

fetch(`https://yourinstance.salesforce.com/services/data/v52.0/sobjects/Lead/`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(leadData)
});
```

You'll need OAuth authentication with Salesforce. Set up a Connected App in Salesforce first.

**Which should you use?** Zapier for most setups. Webhooks only if you need custom processing logic or are already handling webhooks for other tools.

## Testing & Verification

### In Typeform
Submit a test form with fake but realistic data. Use a real email address you control.

### In Salesforce  
1. Go to Leads tab → Recent Items
2. Look for your test lead with the mapped data
3. Check that all fields populated correctly
4. Verify Lead Source shows your expected value

### Cross-Check Numbers
After 24 hours of live traffic:
- Typeform Responses count: Found in form analytics
- Salesforce Leads created: Use a report filtered by Lead Source
- Acceptable variance: 2-5% is normal (some people abandon mid-form)

**Red flags:** More than 10% variance means something's broken. Usually field validation errors in Salesforce preventing lead creation.

## Troubleshooting

**Problem:** Leads aren't appearing in Salesforce at all  
Check your integration logs (Zapier history, webhook server logs, or Salesforce debug logs). Usually it's an authentication issue or the integration is paused.

**Problem:** Duplicate leads being created for same person  
Salesforce duplicate rules are blocking or merging leads. Check Setup → Duplicate Management. You might need to adjust rules or use Contact matching instead of Lead creation.

**Problem:** Custom fields showing as blank in Salesforce  
Field API names don't match, or the field has validation rules blocking the data. Check Setup → Object Manager → Lead → Fields to verify API names and validation rules.

**Problem:** Zapier shows "Error: Required field missing"  
Usually Email or LastName field is empty in the Typeform submission. Add field validation to your Typeform to require these fields, or set up default values in your Zap.

**Problem:** Integration worked then stopped  
Typeform webhook endpoints change if you regenerate API keys. Zapier connections can expire and need re-authentication. Check your integration platform's error logs first.

**Problem:** Form submissions timing out or failing  
If using webhooks, your server might be too slow responding to Typeform. Typeform expects a 200 response within 30 seconds. Process the data asynchronously after sending the 200 response.

## What To Do Next

Once your Typeform leads are flowing into Salesforce, set up tracking to measure which forms convert to actual revenue:

- [Typeform Google Ads Conversion Tracking](/tracking/typeform-google-ads-conversion-tracking) - Track form submissions as Google Ads conversions
- [Typeform to HubSpot Integration](/integrations/typeform-to-hubspot) - Alternative CRM integration
- [Typeform to GoHighLevel](/integrations/typeform-to-gohighlevel) - For agencies using GHL
- Need help with a custom integration? [Get a free tracking audit](/contact) and I'll review your setup

*This guide is part of the [Salesforce Integration Hub](/integrations/salesforce) — connecting Salesforce to marketing tools, analytics platforms, and advertising systems.*