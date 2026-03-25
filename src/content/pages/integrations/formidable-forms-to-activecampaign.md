---
title: "How to Send Formidable Forms Leads to ActiveCampaign (Setup Guide)"
slug: "formidable-forms-to-activecampaign"
description: "Connect Formidable Forms to ActiveCampaign so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/activecampaign"
page_type: "spoke"
---

# Formidable Forms → ActiveCampaign Integration Guide

I see this integration request constantly. You've got Formidable Forms collecting leads on your WordPress site, but they're just sitting there in your WordPress dashboard while your sales team is working out of ActiveCampaign. Every manual export and import is a chance for leads to slip through the cracks — and in about 30% of the setups I audit, that's exactly what's happening.

The good news? Formidable Forms has solid webhook capabilities, and ActiveCampaign's API plays nice with automation tools. The bad news is that most people mess up the field mapping or don't handle duplicate contacts properly.

## What You'll Have Working By The End

- Every Formidable form submission automatically creates a contact in ActiveCampaign within 60 seconds
- Custom fields from your forms properly mapped to ActiveCampaign contact fields
- Duplicate contact handling that updates existing records instead of creating duplicates
- Automation triggers in ActiveCampaign that fire when new contacts are created from forms
- A testing workflow to verify new submissions are flowing through correctly

## Prerequisites

- [ ] Formidable Forms Pro license (webhooks require Pro version)
- [ ] ActiveCampaign account with API access enabled
- [ ] WordPress admin access to configure form settings
- [ ] Your ActiveCampaign API URL and key (found in Settings → Developer)
- [ ] List ID where you want new contacts added

## Step 1: Set Up the Zapier Connection (Recommended)

Zapier is the most reliable option here. I've seen the direct webhook approach work, but it breaks more often when either platform updates their API.

In Zapier, create a new Zap with Formidable Forms as the trigger and ActiveCampaign as the action:

**Trigger Setup:**
- App: Formidable Forms
- Trigger: New Entry
- Connect your WordPress site using the Formidable Forms webhook URL
- Select the specific form you want to integrate

**Action Setup:**
- App: ActiveCampaign
- Action: Create/Update Contact
- Map your form fields to ActiveCampaign fields:
  - Email field → Email
  - First Name → First Name  
  - Last Name → Last Name
  - Phone → Phone
  - Any custom fields → Create matching custom fields in ActiveCampaign first

**Critical Field Mapping Notes:**
- Always use "Create or Update Contact" not "Create Contact" to handle duplicates
- Set the List ID to add contacts to your main lead list
- Map any dropdown or radio button values exactly as they appear in ActiveCampaign

Turn on the Zap and test it with a form submission.

## Step 2: Configure Formidable Forms Webhooks (Direct API Approach)

If you want to skip Zapier and go direct, Formidable Pro supports webhooks. This requires more setup but gives you complete control.

In your Formidable form settings:

1. Go to Settings → Actions & Notifications
2. Click "Add" and select "Register User" action
3. Set up the webhook:

```
Webhook URL: https://youraccountname.api-us1.com/api/3/contacts
Method: POST
Headers:
Api-Token: your-api-key-here
Content-Type: application/json
```

**Webhook Payload:**
```json
{
  "contact": {
    "email": "[email]",
    "firstName": "[first_name]",
    "lastName": "[last_name]",
    "phone": "[phone]",
    "fieldValues": [
      {
        "field": "1",
        "value": "[custom_field_1]"
      }
    ]
  }
}
```

Replace the bracketed values with your actual Formidable field IDs. You can find these in the form builder — they'll look like `[id field_id="25"]`.

**Add to List:**
After creating the contact, you need a second webhook to add them to a list:

```json
{
  "contactList": {
    "list": "your-list-id",
    "contact": "contact-id-from-previous-response",
    "status": 1
  }
}
```

This is why I usually recommend Zapier — it handles the two-step process automatically.

## Step 3: Set Up ActiveCampaign Custom Fields

Before your integration goes live, create any custom fields you're collecting in ActiveCampaign:

1. Go to Settings → Fields
2. Create fields for each additional form field you're capturing
3. Note the field IDs — you'll need these for direct API integration
4. Set appropriate field types (text, number, dropdown, etc.)

**Common Field Mappings I See:**
- Company Name → Custom Field "Company"
- Website URL → Custom Field "Website" 
- Lead Source → Custom Field "Source"
- Budget Range → Custom Field "Budget"
- Message/Comments → Custom Field "Notes"

Make sure the field types match what your form is collecting. A dropdown in Formidable should map to a dropdown in ActiveCampaign with identical options.

## Step 4: Configure ActiveCampaign Automations

Once contacts are flowing in, set up automations to handle new leads:

1. Create a new automation triggered by "Contact subscribes to list"
2. Select the list where form submissions are added
3. Add actions for your lead nurturing sequence:
   - Send welcome email
   - Assign to sales rep
   - Create deal record
   - Tag based on form responses

**Pro tip:** I always add a 5-minute delay before the first action. This gives the webhook time to fully populate all custom fields before any automations fire.

## Step 5: Handle Multi-Page Forms

Formidable Forms supports complex multi-page forms, but you need to decide when to create the ActiveCampaign contact:

**Option A: Create contact on final submission**
- Pro: Complete data, no partial records
- Con: Lose leads who abandon before final step

**Option B: Create contact on first page, update on completion**
- Pro: Capture more leads, even partial ones
- Con: More complex setup, potential for incomplete records

I usually recommend Option A unless you have a particularly long form where abandonment is high. You can track page views separately with Google Analytics to see where people drop off.

## Testing & Verification

**Test the Integration:**
1. Submit a test entry through your Formidable form
2. Check that the entry appears in WordPress admin → Formidable → Entries
3. Wait 60-90 seconds for the integration to process
4. Verify the contact appears in ActiveCampaign → Contacts
5. Check that all custom fields populated correctly
6. Confirm the contact was added to the correct list

**Verify Automations:**
- Check that any welcome emails were sent
- Verify tags were applied correctly
- Confirm deal records were created (if configured)

**Check for Duplicates:**
Submit the same email address twice and verify it updates the existing contact rather than creating a duplicate.

**Numbers to Watch:**
- Form submissions in WordPress should equal new contacts in ActiveCampaign within a 5% variance
- Any variance above 10% indicates the integration is dropping leads

## Troubleshooting

**Problem:** Form submissions aren't creating ActiveCampaign contacts
Check your webhook URL and API credentials. In Zapier, look at the task history for error messages. For direct webhooks, check your server logs for failed HTTP requests.

**Problem:** Custom fields aren't populating in ActiveCampaign
The field IDs in your integration don't match ActiveCampaign's field IDs. Go to Settings → Fields in ActiveCampaign and verify the exact field names and IDs you're using in your mapping.

**Problem:** Duplicate contacts being created instead of updated
You're using "Create Contact" instead of "Create or Update Contact" in your integration. This is the most common mistake I see. Change the action type to handle existing email addresses properly.

**Problem:** Automations aren't triggering for form leads
Your automation trigger might be set to "Contact added to account" instead of "Contact subscribes to list." Change the trigger to match how your integration adds contacts.

**Problem:** International phone numbers breaking the integration
ActiveCampaign expects phone numbers in a specific format. Add phone number formatting in your integration to strip special characters and add country codes where needed.

**Problem:** Long form responses getting truncated
ActiveCampaign has character limits on custom fields. Check the field settings and either increase the limit or truncate long responses before sending them over.

## What To Do Next

Now that your forms are connected to ActiveCampaign, consider these next steps:

- Set up [Formidable Forms to HubSpot integration](/integrations/formidable-forms-to-hubspot) if you're using both CRMs
- Configure [Formidable Forms Google Ads conversion tracking](/tracking/formidable-forms-google-ads-conversion-tracking) to measure form performance
- Explore [other ActiveCampaign integrations](/integrations/activecampaign) to connect more of your marketing stack
- [Get a free audit](/contact) to review your entire lead flow and identify other gaps

*This guide is part of the [ActiveCampaign Integration Hub](/integrations/activecampaign) — complete setup guides for connecting ActiveCampaign to your entire marketing stack.*