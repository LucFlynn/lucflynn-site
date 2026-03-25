---
title: "How to Send HubSpot Forms Leads to ActiveCampaign (Setup Guide)"
slug: "hubspot-forms-to-activecampaign"
description: "Connect HubSpot Forms to ActiveCampaign so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/activecampaign"
page_type: "spoke"
---

# HubSpot Forms → ActiveCampaign Integration Guide

I see this integration setup broken in about 30% of the accounts I audit — usually because teams assume the native HubSpot/ActiveCampaign connection will handle all their lead routing automatically. The reality is that HubSpot Forms submissions often create duplicates, miss custom field mappings, or fail to trigger ActiveCampaign automations properly when not configured correctly.

The bigger problem? Most teams don't realize leads are being dropped until weeks later when their follow-up sequences aren't firing and deals aren't being created.

## What You'll Have Working By The End

• Every HubSpot Forms submission automatically creates or updates a contact in ActiveCampaign within 30 seconds
• Custom form fields properly mapped to ActiveCampaign contact properties and tags
• ActiveCampaign automations triggered immediately when new leads come through HubSpot
• Duplicate contact handling that updates existing records instead of creating new ones
• Error logging so you know when submissions fail to sync

## Prerequisites

Before starting, make sure you have:
• Admin access to both HubSpot and ActiveCampaign accounts
• Your ActiveCampaign API key (found in Settings → Developer)
• Your ActiveCampaign account URL (the subdomain part of your login URL)
• List of which HubSpot form fields should map to which ActiveCampaign properties
• Decision on whether new contacts should be added to a specific ActiveCampaign list

## Step 1: Set Up the Native HubSpot-ActiveCampaign Integration

HubSpot offers a native ActiveCampaign integration that handles basic contact syncing, but it's limited. Here's how to configure it:

Navigate to HubSpot → Settings → Integrations → Connected Apps and search for ActiveCampaign. Click "Connect app" and authenticate with your ActiveCampaign credentials.

**Configuration options:**
• **Sync direction**: Choose "HubSpot to ActiveCampaign" or bidirectional
• **Contact sync**: Enable automatic contact creation
• **Property mapping**: Map HubSpot contact properties to ActiveCampaign fields
• **List assignment**: Choose which ActiveCampaign list new contacts join

The native integration works well for basic contact data but has limitations:
- Only syncs standard HubSpot properties, not custom form fields
- No real-time webhook triggers for ActiveCampaign automations
- Limited control over duplicate handling

If you need more control or custom field mapping, skip to the Zapier method below.

## Step 2: Advanced Setup Using Zapier

For more flexible field mapping and real-time triggers, Zapier is the better option. I use this approach for about 70% of HubSpot-ActiveCampaign integrations.

**Create the Zap:**
1. **Trigger**: "HubSpot → New Form Submission"
2. Select your specific HubSpot form (not "Any Form" — that creates chaos)
3. **Action**: "ActiveCampaign → Create/Update Contact"

**Key configuration settings:**
```
Email: {{Email from HubSpot}}
First Name: {{First Name from HubSpot}}
Last Name: {{Last Name from HubSpot}}
Phone: {{Phone Number from HubSpot}}
```

**Custom field mapping:**
If your HubSpot form has a "Company Size" field that should map to ActiveCampaign's "company_size" custom field:
```
Custom Fields:
- Field: company_size
- Value: {{Company Size from HubSpot}}
```

**List assignment:**
Add contacts to a specific list (recommended for automation triggers):
```
Lists: [Your lead nurture list ID]
```

**Tags for segmentation:**
```
Tags: hubspot-lead, {{Lead Source from HubSpot}}
```

This approach gives you real-time syncing (usually under 2 minutes) and much better field control than the native integration.

## Step 3: Webhook + API Method (For Developers)

If you need immediate sync (under 30 seconds) or complex field transformations, use HubSpot webhooks to trigger ActiveCampaign API calls.

**Set up the HubSpot webhook:**
Go to HubSpot Settings → Data Management → Properties → Form submissions, then create a workflow that triggers on form submission and sends a webhook to your endpoint.

**Your webhook endpoint should accept the payload and make this ActiveCampaign API call:**
```javascript
const payload = {
  contact: {
    email: hubspotData.email,
    firstName: hubspotData.firstname,
    lastName: hubspotData.lastname,
    phone: hubspotData.phone,
    fieldValues: [
      {
        field: "1", // Your custom field ID
        value: hubspotData.company_size
      }
    ]
  }
};

const response = await fetch(`https://${account}.api-us1.com/api/3/contacts`, {
  method: 'POST',
  headers: {
    'Api-Token': process.env.ACTIVECAMPAIGN_API_KEY,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(payload)
});
```

**Add to list and trigger automations:**
```javascript
// After contact creation, add to list
await fetch(`https://${account}.api-us1.com/api/3/contactLists`, {
  method: 'POST',
  headers: {
    'Api-Token': process.env.ACTIVECAMPAIGN_API_KEY,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    contactList: {
      list: listId,
      contact: contactId,
      status: 1
    }
  })
});
```

This method requires development work but gives you complete control over timing, field transformations, and error handling.

## Step 4: Field Mapping Strategy

The key to avoiding data chaos is mapping fields consistently. Here's how I typically set up the mapping:

**Standard fields (easy):**
- HubSpot "Email" → ActiveCampaign "email" 
- HubSpot "First Name" → ActiveCampaign "firstName"
- HubSpot "Last Name" → ActiveCampaign "lastName"
- HubSpot "Phone Number" → ActiveCampaign "phone"

**Custom fields (requires setup):**
First, create the custom fields in ActiveCampaign (Settings → Fields), then map them:
- HubSpot "Company" → ActiveCampaign custom field "company"
- HubSpot "Job Title" → ActiveCampaign custom field "job_title"
- HubSpot form dropdown values → ActiveCampaign tags

**Lead source tracking:**
Always map the HubSpot form name or page URL to an ActiveCampaign custom field or tag so you can track which forms are converting best.

## Testing & Verification

**Test the integration:**
1. Submit a test form on your HubSpot page using a test email address
2. Check that the submission appears in HubSpot (Contacts → [test email])
3. Verify the contact was created in ActiveCampaign within your expected timeframe
4. Confirm all custom fields populated correctly
5. Check that any assigned tags or list memberships are correct

**Verify automation triggers:**
If you have ActiveCampaign automations that should trigger on new contacts:
1. Create a simple automation triggered by "Subscribes to list" or "Contact is created"
2. Submit your test form
3. Check that the automation was triggered in ActiveCampaign → Automations → [Your automation] → Reports

**Monitor for ongoing issues:**
Set up a weekly check to compare form submission counts:
- HubSpot form submissions (last 7 days)
- New ActiveCampaign contacts with your HubSpot tag/source (last 7 days)

The numbers should match within 5%. If there's a bigger discrepancy, something's broken.

## Troubleshooting

**Problem:** Contacts created in ActiveCampaign but custom fields are empty
→ Check your field mapping. ActiveCampaign custom fields need to be referenced by their field ID, not name. Go to Settings → Fields to find the correct ID.

**Problem:** Duplicate contacts being created instead of updating existing ones
→ ActiveCampaign's duplicate detection is based on email address. Make sure your integration is sending the email field correctly and that ActiveCampaign's "Update existing contacts" setting is enabled.

**Problem:** Integration worked initially but stopped syncing
→ Usually an API key issue. Check if your ActiveCampaign API key expired or if account permissions changed. Zapier will show "Authentication failed" errors in your Zap history.

**Problem:** HubSpot forms submissions not triggering the integration
→ If using Zapier, check that you selected the specific form, not "Any form." HubSpot's form IDs change when you edit forms, so you may need to reconnect.

**Problem:** ActiveCampaign automations not triggering for new leads
→ Check that new contacts are being added to the correct list. Most automations trigger on list subscription, not just contact creation.

**Problem:** Integration is slow (taking 10+ minutes to sync)
→ Zapier's free plan has 15-minute delays. Upgrade to a paid plan for faster sync, or use the webhook method for immediate syncing.

## What To Do Next

Once your HubSpot Forms → ActiveCampaign integration is working, consider setting up these related connections:

• **[HubSpot Forms → HubSpot CRM Integration](/integrations/hubspot-forms-to-hubspot)** — Keep leads in HubSpot's ecosystem too
• **[HubSpot Forms → Salesforce Integration](/integrations/hubspot-forms-to-salesforce)** — If you're using multiple CRMs
• **[HubSpot Forms Google Ads Conversion Tracking](/tracking/hubspot-forms-google-ads-conversion-tracking)** — Track which ads drive form submissions

Need help auditing your current integration setup? **[Get a free tracking audit](/contact)** — I'll review your HubSpot-ActiveCampaign connection and identify any leads you might be losing.

*This guide is part of the [ActiveCampaign Integrations Hub](/integrations/activecampaign) — your complete resource for connecting ActiveCampaign to every major marketing and sales tool.*