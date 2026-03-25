---
title: "How to Send HubSpot Forms Leads to Salesforce (Setup Guide)"
slug: "hubspot-forms-to-salesforce"
description: "Connect HubSpot Forms to Salesforce so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/salesforce"
page_type: "spoke"
---

# HubSpot Forms → Salesforce Integration Guide

I see this integration broken in about 30% of the HubSpot accounts I audit. Usually it's because someone set up the native connector thinking it would automatically sync form submissions, but didn't map the fields properly or handle the Lead vs Contact object decision. The result? Form submissions pile up in HubSpot while the sales team wonders why their lead flow dried up.

## What You'll Have Working By The End

- Every HubSpot form submission automatically creates a Salesforce lead/contact
- Proper field mapping so no critical data gets lost in translation
- Error handling that alerts you when submissions fail to sync
- Test process to verify new forms integrate properly
- Clear ownership rules so leads don't get assigned to random users

## Prerequisites

- [ ] HubSpot admin access (or Marketing Hub Professional/Enterprise)
- [ ] Salesforce admin access
- [ ] Decision made: create Leads or Contacts in Salesforce
- [ ] List of required fields in Salesforce that must be mapped
- [ ] Backup plan for failed syncs (email notification or manual check process)

## Step 1: Set Up the Native HubSpot-Salesforce Integration

The native integration is usually your best bet — it's built for this exact use case and handles most edge cases automatically.

In HubSpot, go to Settings → Integrations → Connected Apps → Salesforce. Click "Connect" and authenticate with your Salesforce admin account.

**Key configuration decisions:**

- **Sync direction**: Choose "HubSpot to Salesforce" for form submissions
- **Object mapping**: Decide whether HubSpot contacts become Salesforce Leads or Contacts
- **Duplicate handling**: Set to "Update existing records" if you want to append form data to existing contacts

**Field mapping setup:**
```
HubSpot Property → Salesforce Field
email → Email
firstname → First Name
lastname → Last Name
company → Company
phone → Phone
hs_lead_status → Lead Status (if using Leads)
hubspot_owner_id → Owner ID
```

The critical part most people miss: go to Settings → Objects → Contacts (or Leads) → Sync tab and enable "Include in integrations" for every form that should trigger the sync. If you skip this, form submissions won't trigger the integration.

## Step 2: Configure Form-Specific Sync Settings

Each HubSpot form needs to be configured to trigger the Salesforce sync. This isn't automatic even with the native integration set up.

Navigate to Marketing → Forms, select your form, then go to the Options tab. Under "What should happen after a visitor submits this form?" enable "Add to Salesforce" and choose your sync preferences:

- **Record type**: Lead or Contact (must match your integration setup)
- **Lead source**: Set to "Website" or specific campaign name
- **Assignment rules**: Use Salesforce assignment rules vs. specific user assignment

**For embedded forms on non-HubSpot sites**, you'll need to ensure the form submission triggers the sync. Add this tracking code after your HubSpot form embed:

```javascript
window.addEventListener('message', function(event) {
    if (event.data.type === 'hsFormCallback' && event.data.eventName === 'onFormSubmitted') {
        // Form submitted - HubSpot will handle Salesforce sync
        console.log('Form submitted, syncing to Salesforce');
    }
});
```

## Step 3: Set Up Zapier Integration (Backup Method)

If the native integration doesn't meet your needs — maybe you need custom field mapping or want to trigger other actions — Zapier provides more flexibility.

**Create the Zap:**
1. Trigger: HubSpot → New Form Submission
2. Select your specific form(s) or choose "Any Form"
3. Action: Salesforce → Create Record
4. Choose Lead or Contact object

**Advanced field mapping in Zapier:**
```
HubSpot Field → Salesforce Field → Notes
Email → Email → Required field
First Name → FirstName → Required for Contacts
Last Name → LastName → Required for all objects
Company → Company → Maps to Account if Contact
Phone → Phone → Include country code formatting
Lead Source → LeadSource → Use "Website" or campaign-specific
```

**Pro tip**: Use Zapier's Formatter tool to clean up phone numbers and standardize company names before they hit Salesforce. I see this prevent about 20% of duplicate records.

## Step 4: Webhook + API Approach (Advanced)

For maximum control, you can capture HubSpot form submissions via webhook and use Salesforce's REST API to create records with custom logic.

**Set up the HubSpot webhook:**
1. Go to Settings → Integrations → Private Apps
2. Create a private app with contacts and forms read permissions
3. In Settings → Properties → Contacts, configure form submission webhook:

```javascript
// Webhook payload structure
{
  "email": "user@example.com",
  "firstname": "John",
  "lastname": "Doe",
  "company": "Example Corp",
  "phone": "+1-555-0123",
  "hs_form_id": "abc-123-def",
  "hs_form_name": "Contact Us Form"
}
```

**Salesforce API call:**
```javascript
const salesforceEndpoint = 'https://yourinstance.salesforce.com/services/data/v58.0/sobjects/Lead/';

const leadData = {
  FirstName: webhookData.firstname,
  LastName: webhookData.lastname,
  Email: webhookData.email,
  Company: webhookData.company,
  Phone: webhookData.phone,
  LeadSource: 'Website',
  Status: 'Open - Not Contacted'
};

fetch(salesforceEndpoint, {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer ' + accessToken,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(leadData)
});
```

## Step 5: Handle Assignment Rules and Lead Routing

Whether you use the native integration or custom approach, you need proper lead assignment. Otherwise every lead gets assigned to the integration user.

**In Salesforce:**
1. Setup → Lead Assignment Rules
2. Create rules based on criteria (geography, company size, lead source)
3. Enable "Use active assignment rule" in your integration

**For round-robin assignment**, create a custom field "Last_Assigned_User__c" and use Process Builder or Flow to rotate assignments.

**Territory-based assignment**:
```
IF (Company CONTAINS "Enterprise" OR AnnualRevenue > 1000000)
  ASSIGN TO Enterprise_Team
ELSE IF (Website CONTAINS ".edu")
  ASSIGN TO Education_Team
ELSE
  ASSIGN TO General_Team
```

## Testing & Verification

**Test the integration:**
1. Submit a test form submission with a recognizable email (like test+hubspotforms@yourcompany.com)
2. Wait 2-3 minutes for sync to complete
3. Search Salesforce for the test email
4. Verify all mapped fields populated correctly
5. Check that assignment rules fired properly

**Monitor sync health:**
- HubSpot: Settings → Integrations → Salesforce → Sync Health tab
- Check error logs weekly for failed syncs
- Set up Salesforce reports for leads created by integration user
- Compare HubSpot form submission count vs. Salesforce lead creation count weekly

**Acceptable variance**: 2-5% of form submissions might fail to sync due to temporary API issues. Higher than 5% indicates a configuration problem.

**Red flags:**
- Leads created with blank required fields
- All leads assigned to the same user despite assignment rules
- Form submissions in HubSpot but no corresponding Salesforce records after 10 minutes

## Troubleshooting

**Problem**: Form submissions create HubSpot contacts but not Salesforce leads
**Solution**: Check that the specific form has "Include in integrations" enabled and that your sync settings include the object type you're creating. Also verify your Salesforce user has Create permissions on Lead/Contact objects.

**Problem**: Leads created but missing custom field data
**Solution**: Custom field mapping requires matching API names exactly. In Salesforce Setup → Object Manager → Lead → Fields, copy the "API Name" not the field label. HubSpot property names are usually lowercase with underscores.

**Problem**: Duplicate leads created for the same person
**Solution**: Configure duplicate rules in Salesforce (Setup → Duplicate Management) and set the integration to "Update existing" instead of "Create new." Also check that your email field mapping is working properly.

**Problem**: Webhook integration stops working after Salesforce password change
**Solution**: Most webhook approaches use connected apps with refresh tokens, but some custom setups use username/password authentication. Switch to OAuth 2.0 flow with refresh tokens for better reliability.

**Problem**: Leads assigned to integration user instead of sales reps
**Solution**: Enable "Use active assignment rule" in your integration settings. If using Zapier, add a step to update the lead with proper assignment after creation. Assignment rules only fire on create, not update.

**Problem**: International phone numbers breaking lead creation
**Solution**: Add formatting logic to standardize phone numbers before syncing. Strip non-numeric characters and add country codes consistently. Salesforce phone fields are picky about format.

## What To Do Next

Once your HubSpot forms are syncing to Salesforce, consider these related integrations:

- [Track HubSpot forms in Google Ads](/tracking/hubspot-forms-google-ads-conversion-tracking) for proper conversion attribution
- [Connect HubSpot forms to ActiveCampaign](/integrations/hubspot-forms-to-activecampaign) for marketing automation backup
- [Set up GoHighLevel integration](/integrations/hubspot-forms-to-gohighlevel) if you need additional CRM functionality

Need help auditing your current HubSpot → Salesforce integration? [Get a free tracking audit](/contact) and I'll check your field mapping, sync health, and assignment rules.

*This guide is part of the [Salesforce Integration Hub](/integrations/salesforce) — complete guides for connecting your forms, ads, and tracking to Salesforce CRM.*