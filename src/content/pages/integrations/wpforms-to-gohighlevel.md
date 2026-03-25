---
title: "How to Send WPForms Leads to GoHighLevel (Setup Guide)"
slug: "wpforms-to-gohighlevel"
description: "Connect WPForms to GoHighLevel so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/gohighlevel"
page_type: "spoke"
---

# WPForms → GoHighLevel Integration Guide

I see agencies running WPForms on client sites but manually copying leads into GoHighLevel. That stops working the moment you scale past 5-10 leads per day. The good news is that GoHighLevel's webhook system is actually more reliable than most CRMs — once you get it configured correctly.

Every month, I audit setups where leads are falling through the cracks because someone set up the integration wrong six months ago and never tested it. Don't be that person.

## What You'll Have Working By The End

- Every WPForms submission creates a GoHighLevel contact automatically
- Custom field values map correctly (phone, company, lead source, etc.)
- New contacts get added to the right pipeline with the proper stage
- Failed submissions get logged so you can catch missed leads
- Test submissions work reliably before you go live

## Prerequisites

- [ ] WPForms Pro (webhooks require the paid version)
- [ ] GoHighLevel account with API access
- [ ] WordPress admin access on the site with your forms
- [ ] Basic understanding of field mapping (matching form fields to CRM fields)

## Step 1: Get Your GoHighLevel Webhook URL

GoHighLevel makes this easier than most CRMs. You'll create a webhook that can handle inbound lead data.

Log into your GoHighLevel account and go to **Settings → Integrations → Webhooks**. Click **Create Webhook** and select **Inbound Webhook**.

Set these options:
- **Webhook Name**: WPForms Lead Capture
- **Method**: POST
- **Response Type**: JSON
- **Pipeline**: Select your main lead pipeline
- **Stage**: Usually "New Lead" or whatever your first stage is called

Copy the webhook URL that GoHighLevel generates. It'll look like:
```
https://hooks.gohighlevel.com/hooks/webhook_id_here
```

Save this — you'll need it in the next step.

## Step 2: Configure WPForms Webhook

In your WordPress dashboard, go to **WPForms → Settings → Integrations** and find the **Webhooks** option. If you don't see it, you're on WPForms Lite and need to upgrade.

Create a new webhook connection:
- **Webhook URL**: Paste your GoHighLevel webhook URL
- **Request Method**: POST
- **Request Format**: JSON

The field mapping is where most people screw this up. GoHighLevel expects specific field names. Here's the mapping that works:

**Standard Fields:**
- `name` → Contact Name (or map `first_name` and `last_name` separately)
- `email` → Email address
- `phone` → Phone number
- `company` → Company name

**Custom Fields:**
- Map any WPForms custom fields to GoHighLevel custom fields using the exact field IDs from GoHighLevel

Your JSON payload should look like this:
```json
{
  "name": "{field_1} {field_2}",
  "email": "{field_3}",
  "phone": "{field_4}",
  "company": "{field_5}",
  "source": "Website Form"
}
```

Replace the `{field_X}` placeholders with your actual WPForms field IDs.

## Step 3: Set Up Zapier (Alternative Method)

If the webhook approach feels too technical, Zapier is more forgiving but costs monthly. 

In Zapier, create a new Zap:
1. **Trigger**: WPForms → New Form Entry
2. **Action**: GoHighLevel → Create Contact

Connect your WPForms account by entering your WordPress site URL and API key (found in WPForms → Settings → General).

For GoHighLevel, you'll need your API key from Settings → Company Settings → API Keys.

The field mapping in Zapier is drag-and-drop:
- WPForms "Name" field → GoHighLevel "Name"
- WPForms "Email" field → GoHighLevel "Email" 
- WPForms "Phone" field → GoHighLevel "Phone"

Set the pipeline and stage in the Zapier action. Test the Zap with a sample submission before turning it on.

## Step 4: Configure Pipeline Automation (Optional)

Once leads are flowing into GoHighLevel, you can set up automation to handle them.

Go to **Automation → Workflows** and create a new workflow with the trigger **Contact Added to Pipeline**.

Common automations I set up:
- Send an internal notification email when a new lead comes in
- Add a tag based on the form source
- Assign the lead to a specific team member
- Send an auto-response email to the lead

The workflow builder is visual — drag the actions you want and connect them.

## Testing & Verification

Never go live without testing. I've seen too many setups that looked right but weren't actually working.

**Test the Integration:**
1. Submit a test form entry with fake but realistic data
2. Check GoHighLevel contacts within 2-3 minutes
3. Verify all fields mapped correctly
4. Check that the contact landed in the right pipeline/stage

**Check the Webhook Logs:**
In GoHighLevel, go to Settings → Integrations → Webhooks and click on your webhook. You'll see a log of all requests. Failed requests show up in red with error details.

**Cross-Reference the Numbers:**
After a week, compare your WPForms submission count to your GoHighLevel contact count for the same period. They should match within 2-3 entries (some people submit test forms).

If you're seeing more than 5% variance, something is broken and you need to troubleshoot.

## Troubleshooting

**Problem**: Webhook shows 400 error in GoHighLevel logs  
**Solution**: Check your field mapping. GoHighLevel is picky about field names. Use `name` not `full_name`, use `phone` not `phone_number`.

**Problem**: Contacts created but missing custom field data  
**Solution**: Your custom field IDs don't match between WPForms and GoHighLevel. In GoHighLevel, go to Settings → Custom Fields and copy the exact field key (it's usually something like `custom.lead_source`).

**Problem**: Duplicate contacts being created  
**Solution**: Enable GoHighLevel's duplicate detection in Settings → General Settings → Duplicate Contact Detection. Set it to merge on email address.

**Problem**: Zapier shows "Contact already exists" error  
**Solution**: Change the Zapier action from "Create Contact" to "Create or Update Contact". This handles duplicates gracefully.

**Problem**: Some form submissions not triggering the webhook  
**Solution**: Check if users are abandoning the form before completion. WPForms only fires webhooks on successful submissions. Also verify that WPForms Pro is active — webhooks don't work on the free version.

**Problem**: GoHighLevel webhook timing out  
**Solution**: This is usually a field mapping issue causing validation errors. Check the webhook logs in GoHighLevel for specific error messages. The most common issue is sending invalid phone number formats.

## What To Do Next

Once your WPForms → GoHighLevel integration is working, consider these related setups:

- [WPForms → HubSpot Integration](/integrations/wpforms-to-hubspot) if you're using HubSpot as your secondary CRM
- [WPForms Google Ads Conversion Tracking](/tracking/wpforms-google-ads-conversion-tracking) to track which ads generate your best leads
- [WPForms → ActiveCampaign Integration](/integrations/wpforms-to-activecampaign) for email marketing automation
- [Contact me](/contact) for a free tracking audit if you want me to verify your setup is bulletproof

*This guide is part of the [GoHighLevel Integrations Hub](/integrations/gohighlevel) — complete setup guides for connecting your favorite tools to GoHighLevel's CRM and marketing platform.*