---
title: "How to Send Unbounce Leads to Zoho CRM (Setup Guide)"
slug: "unbounce-to-zoho"
description: "Connect Unbounce to Zoho CRM so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/zoho"
page_type: "spoke"
---

# Unbounce → Zoho CRM Integration Guide

Most Unbounce-to-Zoho setups I audit are either completely broken or creating duplicate leads because someone tried to set up three different integration methods at once. The webhook usually times out, Zapier creates contacts instead of leads, and nobody realizes half their submissions are vanishing until they run the numbers at month-end.

Here's how to connect them properly so every Unbounce form submission flows into Zoho CRM as a qualified lead, with proper field mapping and error handling.

## What You'll Have Working By The End

- Every Unbounce form submission automatically creates a lead in Zoho CRM
- Proper field mapping from Unbounce custom fields to Zoho lead fields
- Duplicate detection that updates existing leads instead of creating duplicates
- Error handling that catches failed submissions and retries them
- Testing workflow to verify everything works before going live

## Prerequisites

- [ ] Admin access to your Unbounce account
- [ ] Admin or user management access to Zoho CRM
- [ ] Ability to create custom fields in Zoho CRM if needed
- [ ] Access to create Zapier account (for method #2)
- [ ] Developer access to your landing pages if using webhooks

## Step 1: Choose Your Integration Method

There are three ways to connect Unbounce to Zoho CRM. I recommend them in this order:

**Option 1: Zapier (Recommended)** - Most reliable, handles errors well, easy troubleshooting. About 95% success rate in my experience.

**Option 2: Zoho CRM Web Forms** - Embed Zoho's form directly in Unbounce. Works but limits your design flexibility.

**Option 3: Webhook to API** - Most flexible but requires development work. Only go this route if you need complex field transformations.

Skip the native integrations list in Unbounce — there's no direct Zoho CRM connector there, just Zoho Forms which is different.

## Step 2: Set Up Zapier Integration

This is the method I use in about 80% of Unbounce-Zoho setups.

### Create the Zap

1. Create new Zap in Zapier
2. Choose **Unbounce** as trigger app
3. Select **New Form Submission** as trigger event
4. Connect your Unbounce account (you'll need to authorize)
5. Choose your specific landing page and form

### Configure Unbounce Trigger

1. Select the landing page containing your form
2. If you have multiple forms on one page, choose the correct form ID
3. Test the trigger by submitting a test form submission
4. Zapier should pull in all your form fields — this is your field mapping reference

### Set Up Zoho CRM Action

1. Add Zoho CRM as action app
2. Choose **Create Lead** as the action event (not Create Contact)
3. Authorize your Zoho CRM account
4. Map your fields:

**Essential Field Mapping:**
- Unbounce "Email" → Zoho CRM "Email"
- Unbounce "First Name" → Zoho CRM "First Name"
- Unbounce "Last Name" → Zoho CRM "Last Name"
- Unbounce "Phone" → Zoho CRM "Phone" (format as needed)
- Set Lead Source to "Unbounce" (static value)
- Set Lead Status to your default (usually "New" or "Unqualified")

**Advanced Mapping:**
- Company field → Account Name
- Comments/Message → Description
- UTM parameters → custom fields if you're tracking them
- Page URL → Website field

### Handle Duplicates

In the Zoho CRM action, look for **"What should Zapier do if lead already exists?"** 

Set this to **"Update existing record"** rather than skip or create duplicate. Map the update fields to ensure existing leads get refreshed data.

## Step 3: Alternative - Zoho CRM Web Forms Method

If Zapier isn't an option, you can embed Zoho's web form directly in your Unbounce page.

### Create Zoho Web Form

1. Go to Setup → Channels → Web Forms in Zoho CRM
2. Click **Create Web Form**
3. Add the fields you want to collect
4. Set up auto-response and assignment rules
5. Generate the form code

### Embed in Unbounce

1. In Unbounce page builder, delete your existing form
2. Add HTML widget where form was located
3. Paste the Zoho web form embed code
4. Style it to match your page design (limited options here)

This method works but you lose Unbounce's form functionality like conditional fields, custom validation, and form analytics.

## Step 4: Webhook + API Method (Advanced)

Only use this if you need complex field transformations or have a developer available.

### Set Up Unbounce Webhook

1. In Unbounce, go to your landing page settings
2. Find **Form Actions** section
3. Add **Webhook** action
4. Set URL to your endpoint (you'll build this)
5. Choose POST method

### Build the API Endpoint

Your webhook receiver needs to:

1. Accept POST data from Unbounce
2. Transform fields as needed
3. Send to Zoho CRM API

**Sample API payload for Zoho CRM:**

```json
{
  "data": [
    {
      "First_Name": "John",
      "Last_Name": "Smith",
      "Email": "john@example.com",
      "Phone": "555-123-4567",
      "Lead_Source": "Unbounce",
      "Lead_Status": "New"
    }
  ]
}
```

**API endpoint:** `https://www.zohoapis.com/crm/v2/Leads`

Include authentication header with your Zoho access token.

## Step 5: Testing & Verification

Never assume it's working. Test everything.

### Test Form Submission

1. Submit a test form with fake data you can easily identify
2. Check that submission appears in Unbounce lead notifications
3. For Zapier: check Zap history to see if it triggered successfully
4. Check Zoho CRM Leads module for your test submission

### Verify Field Mapping

Look at your test lead in Zoho CRM:
- All mapped fields populated correctly?
- Lead Source showing "Unbounce"?
- Lead Status set to your default?
- No fields cut off or formatted incorrectly?

### Check for Duplicates

Submit the same email address twice:
- Should update existing lead, not create new one
- Check timestamp on lead to confirm it updated
- If creating duplicates, fix your duplicate handling settings

### Monitor Error Rates

First 48 hours after setup:
- Check Zapier error logs daily
- Monitor Zoho CRM import logs for failures
- Acceptable error rate is under 5%
- Anything above 10% means something's broken

## Troubleshooting

**Problem:** Zapier shows "Lead already exists" and skips creation
→ Change duplicate handling to "Update existing record" instead of "Skip"

**Problem:** Phone numbers not formatting correctly in Zoho
→ Add formatter step in Zapier to clean phone number format. Use "Phone Number" formatter to convert to standard format.

**Problem:** Unbounce webhook timing out or failing
→ Check your endpoint response time. Must respond within 30 seconds. Add retry logic for API failures.

**Problem:** UTM parameters not passing through
→ Unbounce doesn't capture UTMs by default. Add hidden form fields with JavaScript to capture them, or use URL parameters method.

**Problem:** Some leads missing Lead Source designation
→ Check your static field mapping. Lead Source should be hardcoded to "Unbounce", not mapped to a form field that might be empty.

**Problem:** Integration worked for a few days then stopped
→ Usually an authentication issue. Check if Zoho access tokens expired (they do every 90 days). Reauthorize connection in Zapier.

## What To Do Next

Most Unbounce setups also need proper conversion tracking for your ads. Check out [Unbounce Google Ads Conversion Tracking](/tracking/unbounce-google-ads-conversion-tracking) to make sure you're measuring ROI correctly.

If you're running other form tools, see [Unbounce to HubSpot](/integrations/unbounce-to-hubspot) or [Unbounce to Salesforce](/integrations/unbounce-to-salesforce) for similar setups.

For other Zoho CRM integrations, browse the [complete Zoho integration library](/integrations/zoho).

Need help auditing your current setup? [Get a free tracking audit](/contact) — I'll check your integration and show you what's breaking.

*This guide is part of the [Zoho CRM Integration Hub](/integrations/zoho) — complete guides for connecting every major form tool and marketing platform to Zoho CRM.*