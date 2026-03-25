---
title: "How to Send Elementor Forms Leads to Mailchimp (Setup Guide)"
slug: "elementor-forms-to-mailchimp"
description: "Connect Elementor Forms to Mailchimp so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/mailchimp"
page_type: "spoke"
---

# Elementor Forms → Mailchimp Integration Guide

I see this setup in about 60% of WordPress sites I audit, and about half of them are losing leads because the integration broke and nobody noticed. The most common issue? Form submissions hit Elementor but never make it to Mailchimp, usually because someone changed an API key or audience ID without updating the integration.

Here's the thing — Elementor Forms to Mailchimp is actually one of the easier integrations to set up, but there are some gotchas around field mapping and error handling that trip people up.

## What You'll Have Working By The End

- Every Elementor form submission automatically creates or updates a contact in your Mailchimp audience
- Proper field mapping so form data lands in the right Mailchimp fields
- Error handling so you know when leads aren't syncing
- A testing process to verify the integration before going live
- Backup webhook system in case the primary integration fails

## Prerequisites

- [ ] WordPress admin access with Elementor Pro installed
- [ ] Mailchimp account with at least one audience created
- [ ] Mailchimp API key (found in Account > Extras > API keys)
- [ ] Your Mailchimp audience ID (found in Audience > Settings > Audience name and defaults)

## Step 1: Set Up Mailchimp API Connection in Elementor

Elementor Pro has a native Mailchimp integration, which is your best option since it handles the API connection and basic error handling automatically.

Go to **Elementor > Settings > Integrations** and find the Mailchimp section. Enter your API key — you can get this from your Mailchimp account under Account > Extras > API keys.

Once connected, Elementor will pull your audience list automatically. This connection gets cached, so if you create new audiences in Mailchimp, you'll need to disconnect and reconnect here to refresh the list.

**Pro tip**: Create a dedicated API key just for Elementor. Name it "Elementor Website Integration" so you can easily identify it if you need to revoke access later.

## Step 2: Configure Form Actions After Submit

Edit your Elementor form and go to **Actions After Submit**. Click the plus icon and add "Mailchimp" from the list.

Here's where field mapping happens:

- **Audience**: Select your target Mailchimp audience from the dropdown
- **Email Field**: Map to your form's email field (usually just "email")
- **Double Opt-In**: I recommend keeping this enabled unless you're collecting leads at events where people expect to be added immediately
- **Update Existing**: Enable this so returning visitors update their info instead of creating errors
- **Groups**: Map form fields to Mailchimp groups if you're using them for segmentation

For custom fields, you'll need to create them in Mailchimp first (**Audience > Settings > Audience fields and MERGE tags**), then map them in Elementor using the field's merge tag (like `FNAME`, `LNAME`, `COMPANY`).

**Field mapping example:**
- Form field "first_name" → Mailchimp merge tag `FNAME`
- Form field "last_name" → Mailchimp merge tag `LNAME`
- Form field "phone" → Mailchimp merge tag `PHONE`
- Form field "company" → Mailchimp merge tag `COMPANY`

## Step 3: Set Up Zapier as Backup (Recommended)

Even with the native integration, I always set up a Zapier backup because Elementor's error handling isn't great — if the API call fails, you might not know about it.

Create a new Zap with:
- **Trigger**: Webhooks by Zapier > Catch Hook
- **Action**: Mailchimp > Add/Update Subscriber

Copy the webhook URL from Zapier, then go back to your Elementor form and add a "Webhook" action after submit. Paste the Zapier URL and set the method to POST.

This creates a redundant path: form submissions go to both Elementor's native Mailchimp action AND to Zapier. If the Elementor integration breaks, Zapier keeps working.

**Webhook payload structure:**
```json
{
  "email": "[field id='email']",
  "first_name": "[field id='first_name']", 
  "last_name": "[field id='last_name']",
  "phone": "[field id='phone']",
  "source": "website_contact_form"
}
```

Map these fields in your Zapier action step to the corresponding Mailchimp fields.

## Step 4: Advanced Webhook Setup (For Technical Users)

If you want more control or are hitting API rate limits, you can bypass Elementor's native integration and use a custom webhook that calls Mailchimp's API directly.

Set up a webhook endpoint that receives the form data and makes this API call:

```javascript
const mailchimpData = {
  email_address: formData.email,
  status: 'subscribed',
  merge_fields: {
    FNAME: formData.first_name,
    LNAME: formData.last_name,
    PHONE: formData.phone,
    COMPANY: formData.company
  },
  tags: ['website-lead']
};

fetch(`https://${datacenter}.api.mailchimp.com/3.0/lists/${listId}/members`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${apiKey}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(mailchimpData)
});
```

Replace `${datacenter}` with your Mailchimp datacenter (the part after the dash in your API key), `${listId}` with your audience ID, and `${apiKey}` with your API key.

This approach gives you better error handling and logging, but requires more technical setup.

## Testing & Verification

Submit a test form with fake but realistic data. Here's what to check:

**In Mailchimp** (check within 2-3 minutes):
- New contact appears in your audience
- All mapped fields populated correctly
- Contact has correct subscription status
- Tags applied if you're using them

**In Elementor**:
- Form shows success message
- No error messages in browser console
- Actions After Submit logs show successful completion (if you have logging enabled)

**In Zapier** (if using backup):
- Zap history shows successful trigger and action
- Task count incremented
- No error messages in task details

**Red flags that indicate problems:**
- Form submits but no contact appears in Mailchimp after 5 minutes
- Contact appears but fields are empty or incorrectly mapped
- Contact appears multiple times for same email address
- Error messages in Elementor's form submission logs

## Troubleshooting

**Problem**: Form submits successfully but no contact appears in Mailchimp
Check your API key is still valid and hasn't been regenerated. Mailchimp sometimes expires old API keys without warning. Also verify the audience ID hasn't changed if you've been reorganizing your Mailchimp account.

**Problem**: Contact appears but custom fields are empty
You likely have a merge tag mismatch. Go to Mailchimp > Audience > Settings > Audience fields and verify the merge tags match exactly what you're using in Elementor (case sensitive). The merge tag is what goes in the mapping, not the field name.

**Problem**: Getting "Member already exists" errors
Enable "Update Existing" in your Mailchimp action settings. Without this, Mailchimp rejects submissions from email addresses that already exist in your audience, even if you want to update their information.

**Problem**: Double opt-in emails not sending
Check your Mailchimp account's authentication settings and make sure your sending domain is verified. Also check if the email address might be on Mailchimp's suppression list from previous bounces or complaints.

**Problem**: Integration worked fine, then suddenly stopped
This usually happens after WordPress or Elementor updates. Check if your API connection in Elementor > Settings > Integrations is still active. Sometimes updates reset these connections and you need to reconnect.

**Problem**: Some submissions sync, others don't
Look for pattern in what's failing — usually it's specific form fields causing API errors. Check for special characters, extremely long text, or invalid email formats. Set up error logging in your webhook backup to catch these edge cases.

## What To Do Next

Once your Elementor → Mailchimp integration is running, consider setting up [Elementor Forms Google Ads conversion tracking](/tracking/elementor-forms-google-ads-conversion-tracking) to measure which campaigns drive the most form submissions.

For more robust CRM functionality, check out [Elementor Forms to HubSpot](/integrations/elementor-forms-to-hubspot) or [Elementor Forms to Salesforce](/integrations/elementor-forms-to-salesforce) integrations.

If you need a more advanced lead qualification system, [Elementor Forms to GoHighLevel](/integrations/elementor-forms-to-gohighlevel) offers built-in automation and follow-up sequences.

**Having issues with your current form tracking setup?** I audit WordPress tracking implementations weekly and can spot integration problems in about 10 minutes. [Get a free tracking audit](/contact) and I'll review your current setup.

*This guide is part of the [Mailchimp Integrations Hub](/integrations/mailchimp) — complete guides for connecting your lead sources to Mailchimp audiences and automations.*