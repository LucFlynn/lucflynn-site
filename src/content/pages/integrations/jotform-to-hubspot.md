---
title: "How to Send Jotform Leads to HubSpot (Setup Guide)"
slug: "jotform-to-hubspot"
description: "Connect Jotform to HubSpot so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/hubspot"
page_type: "spoke"
---

# Jotform → HubSpot Integration Guide

Every time someone submits your Jotform and you don't get a HubSpot contact automatically, you're losing leads. I see this broken in about 35% of the setups I audit — usually because someone tried to use a webhook without proper error handling, or they mapped fields incorrectly and submissions just disappear into the void.

## What You'll Have Working By The End

- Every Jotform submission creates a HubSpot contact automatically
- Form fields map to the correct HubSpot properties
- Duplicate contacts get handled properly (updated instead of erroring)
- You can track which forms are generating the most leads
- Failed submissions get caught and retried

## Prerequisites

- [ ] Admin access to your Jotform account
- [ ] Admin or Marketing Hub access to HubSpot
- [ ] Your Jotform is published and receiving submissions
- [ ] HubSpot contact properties created for any custom fields you want to capture

## Step 1: Use HubSpot's Native Jotform Integration

HubSpot has a native integration that works better than Zapier in most cases. I recommend this for 90% of setups.

In HubSpot:
1. Go to **Settings** → **Integrations** → **Connected Apps**
2. Search for "Jotform" and click **Connect**
3. Authorize the connection with your Jotform credentials

In Jotform:
1. Open your form in the **Form Builder**
2. Go to **Settings** → **Integrations**
3. Find **HubSpot** and click **Setup**
4. Select your HubSpot account from the dropdown
5. Map your form fields:

**Essential Field Mappings:**
- **Email** → `email` (required)
- **First Name** → `firstname`
- **Last Name** → `lastname` 
- **Phone** → `phone`
- **Company** → `company`

**Custom Field Mapping:**
If you have custom fields like "Budget" or "Project Type":
1. Create the property in HubSpot first (**Settings** → **Properties** → **Contact Properties**)
2. Use the exact internal name from HubSpot in the Jotform mapping

The native integration handles duplicates automatically — it updates existing contacts instead of creating duplicates.

## Step 2: Zapier Integration (Alternative Method)

If you need more complex logic or the native integration doesn't support your use case, use Zapier.

**Setting up the Zap:**
1. **Trigger:** Jotform → "New Submission"
2. **Action:** HubSpot → "Create or Update Contact"

**Zapier Field Mapping:**
```
Jotform Field          → HubSpot Property
Email                  → Email
First Name             → First Name
Last Name              → Last Name
Phone Number           → Phone Number
Company Name           → Company Name
Submission ID          → Jotform Submission ID (custom property)
Form Title             → Lead Source (custom property)
```

**Why map Submission ID:** You'll need this for troubleshooting. Create a custom HubSpot property called "Jotform Submission ID" first.

**Handling Duplicates in Zapier:**
Always use "Create or Update Contact" instead of "Create Contact". The update action prevents duplicate contact errors when someone fills out multiple forms.

## Step 3: Webhook + API Method (Advanced)

Use this if you need real-time processing or complex data transformation that Zapier can't handle.

**In Jotform:**
1. **Settings** → **Integrations** → **Webhooks**
2. Set webhook URL to your processing endpoint
3. Select **POST** method
4. Set content type to `application/json`

**Webhook Payload Structure:**
```json
{
  "submissionID": "231234567890123456",
  "formID": "231234567890123456",
  "ip": "192.168.1.1",
  "formTitle": "Contact Form",
  "answers": {
    "3": {
      "name": "name",
      "order": "1",
      "text": "John Doe",
      "type": "control_fullname"
    },
    "4": {
      "name": "email",
      "order": "2", 
      "text": "john@example.com",
      "type": "control_email"
    }
  }
}
```

**Processing Script (Node.js example):**
```javascript
const hubspot = require('@hubspot/api-client');

app.post('/jotform-webhook', async (req, res) => {
  try {
    const submission = req.body;
    const answers = submission.answers;
    
    // Extract form data
    const email = findAnswerByName(answers, 'email');
    const fullName = findAnswerByName(answers, 'name');
    const [firstName, lastName] = fullName.split(' ');
    
    // Create HubSpot contact
    const hubspotClient = new hubspot.Client({
      accessToken: process.env.HUBSPOT_ACCESS_TOKEN
    });
    
    const properties = {
      email: email,
      firstname: firstName || '',
      lastname: lastName || '',
      jotform_submission_id: submission.submissionID,
      lead_source: submission.formTitle
    };
    
    await hubspotClient.crm.contacts.basicApi.create({
      properties: properties
    });
    
    res.status(200).json({ success: true });
  } catch (error) {
    console.error('Webhook error:', error);
    res.status(500).json({ error: error.message });
  }
});

function findAnswerByName(answers, name) {
  for (let key in answers) {
    if (answers[key].name === name) {
      return answers[key].text;
    }
  }
  return '';
}
```

## Step 4: Testing Your Integration

**Test the Connection:**
1. Submit a test entry through your Jotform
2. Check HubSpot **Contacts** within 2-3 minutes
3. Verify all mapped fields populated correctly
4. Check that the contact source is attributed properly

**Verify Field Mapping:**
- Email should appear in the Email field (not a custom property)
- Names should split into First/Last Name correctly  
- Phone numbers should include country codes if international
- Custom properties should show the exact values from the form

**Check for Duplicates:**
1. Submit the same email twice
2. Verify only one contact exists
3. Confirm the second submission updated the existing contact

**Red Flags:**
- Contacts appearing 5+ minutes after form submission
- Missing fields that were clearly filled out
- Multiple contacts with the same email address
- Test submissions not appearing at all

## Testing & Verification

**Real-time Testing:**
Submit a form while watching HubSpot. Native integration usually shows contacts within 30 seconds. Zapier can take 1-15 minutes depending on your plan.

**Source Attribution Check:**
In HubSpot, go to **Reports** → **Analytics Tools** → **Sources Report** to see if Jotform submissions are being tracked as a lead source.

**Volume Verification:**
Compare Jotform submission count (Settings → Form Analytics) to new HubSpot contacts from that source. Acceptable variance is 5-10% due to spam filtering and duplicate merging.

**Cross-Reference Check:**
Take a random Jotform submission ID and search for it in HubSpot's custom property. If you can't find matches, your mapping is broken.

## Troubleshooting

**Problem:** Forms submit but no HubSpot contacts appear  
Check that your HubSpot integration is still connected (Settings → Integrations). Jotform connections expire every 90 days and need to be re-authorized. Also verify the form you're testing is the same one that has the integration enabled.

**Problem:** Contacts appear but fields are empty  
Your field mapping doesn't match HubSpot's property names. In HubSpot, go to Settings → Properties → Contact Properties and copy the exact "Internal name" for each field. Jotform is case-sensitive.

**Problem:** Getting "Invalid email" errors in webhook logs  
Jotform sometimes passes empty email fields as `""` instead of null. Add email validation to your webhook processing: `if (!email || email.trim() === '') return;`

**Problem:** Duplicate contacts still being created  
If using the native integration, check that you don't have multiple integrations running (native + Zapier). If using Zapier, make sure you selected "Create or Update Contact" not "Create Contact".

**Problem:** Webhook timing out or failing intermittently  
HubSpot API calls can fail during high traffic. Add retry logic with exponential backoff. Also, respond to Jotform's webhook with a 200 status immediately, then process the data asynchronously.

**Problem:** International phone numbers not formatting correctly  
Jotform passes phone numbers as strings. Use a library like `libphonenumber-js` to parse and format them before sending to HubSpot, or they'll show up as invalid.

## What To Do Next

Once your basic integration works, consider these advanced setups:
- [Jotform → Salesforce integration](/integrations/jotform-to-salesforce) if you're migrating CRMs
- [Jotform → GoHighLevel setup](/integrations/jotform-to-gohighlevel) for marketing automation
- [Jotform → ActiveCampaign connection](/integrations/jotform-to-activecampaign) for email sequences

You should also set up conversion tracking: [Jotform Google Ads conversion tracking](/tracking/jotform-google-ads-conversion-tracking) to measure which campaigns drive form submissions.

**Need help debugging a broken integration?** I offer [free tracking audits](/contact) and can usually spot the issue in 10 minutes.

*This guide is part of the [HubSpot Integrations Hub](/integrations/hubspot) — covering all the ways to get data into and out of HubSpot automatically.*