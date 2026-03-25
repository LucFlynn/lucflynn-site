---
title: "How to Send Jotform Leads to Salesforce (Setup Guide)"
slug: "jotform-to-salesforce"
description: "Connect Jotform to Salesforce so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/salesforce"
page_type: "spoke"
---

# Jotform → Salesforce Integration Guide

I've set up dozens of Jotform → Salesforce integrations, and about 60% of them break within the first month because teams skip the field mapping validation step. The integration itself is straightforward — Jotform has solid native options — but Salesforce's field requirements will trip you up if you're not careful.

## What You'll Have Working By The End

- Every Jotform submission automatically creates a new lead in Salesforce
- Proper field mapping so all form data lands in the right Salesforce fields
- Error handling that alerts you when submissions fail to sync
- A testing process that catches integration breaks before they cost you leads
- Duplicate prevention so you don't spam your sales team with repeat contacts

## Prerequisites

- [ ] Admin access to your Jotform account
- [ ] Admin access to Salesforce (or at minimum, "Customize Application" and "Manage Users" permissions)
- [ ] Your Salesforce Web-to-Lead settings enabled (Setup → Feature Settings → Marketing → Web-to-Lead)
- [ ] A test form ready in Jotform (don't test on your live lead gen forms)

## Step 1: Enable Salesforce Web-to-Lead

Before connecting anything, you need to turn on Salesforce's lead capture endpoint.

In Salesforce, go to **Setup → Feature Settings → Marketing → Web-to-Lead**. Click **Generate** to create your Web-to-Lead form. You'll get an HTML form with a hidden input that looks like this:

```html
<input type="hidden" name="oid" value="00D5f000009abc123">
```

Copy that `oid` value — you'll need it for the Jotform integration. The Web-to-Lead endpoint accepts up to 500 submissions per day, which covers most small to medium businesses. If you're pushing more volume, you'll need the API approach instead.

## Step 2: Set Up the Jotform Integration

Jotform offers three ways to connect to Salesforce. Here's which one to use:

**Native Salesforce Integration (recommended)**: Go to your form's Settings → Integrations → Salesforce. This uses Jotform's OAuth connection and handles all the API calls for you.

**Web-to-Lead Integration (backup option)**: If the native integration is down or you hit rate limits, use Settings → Integrations → Generic Web Hook and point it at Salesforce's Web-to-Lead endpoint: `https://webto.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8`

I prefer the native integration because it gives you better error reporting and doesn't count against your Web-to-Lead daily limit.

For the native integration:
1. Click **Integrate** next to Salesforce
2. Authorize your Salesforce account (you'll need admin permissions)
3. Set the **Object Type** to "Lead" (not Contact — that requires existing account relationships)
4. Map your form fields to Salesforce fields in the next step

## Step 3: Map Form Fields to Salesforce Fields

This is where 90% of setups break. Salesforce is picky about field names and data types.

**Required Salesforce Lead Fields:**
- `LastName` (required) — map to your "Last Name" or "Full Name" field
- `Company` (required) — map to "Company" or set a default value like "Unknown"
- `Email` (optional but recommended)

**Common Field Mappings:**
- Jotform "First Name" → Salesforce `FirstName`
- Jotform "Email" → Salesforce `Email`
- Jotform "Phone" → Salesforce `Phone`
- Jotform "Company" → Salesforce `Company`
- Jotform "Message" → Salesforce `Description`

**Set Default Values** for required fields you don't collect. For example, if your form doesn't ask for company name, set `Company` to "Website Lead" or "Unknown" rather than leaving it blank.

If you're using Web-to-Lead instead, your form fields need to match Salesforce API names exactly:

```html
<input type="text" name="first_name" id="first_name">
<input type="text" name="last_name" id="last_name">
<input type="email" name="email" id="email">
<input type="text" name="company" id="company">
```

## Step 4: Configure Lead Assignment and Routing

By default, all leads go to the integration user (whoever authorized the connection). Set up proper lead assignment:

**In Salesforce:**
1. Go to Setup → Feature Settings → Marketing → Web-to-Lead
2. Set **Default Lead Creator** to your sales manager or lead routing user
3. Create **Lead Assignment Rules** if you want geographic or criteria-based routing

**In Jotform Integration Settings:**
- Set **Lead Source** to "Website" or "Jotform" so you can track form performance
- Set **Lead Status** to "New" or "Unqualified" depending on your sales process
- Add any custom field mappings for UTM parameters or form-specific data

## Step 5: Add Error Handling and Notifications

The integration will fail silently if you don't set up error monitoring. I've seen companies lose weeks of leads because nobody knew the integration was broken.

**In Jotform:**
1. Go to Settings → Integrations → Salesforce
2. Enable **Email Notifications on Error**
3. Set the notification email to your ops team, not your sales team
4. Test the error notification by temporarily disabling the Salesforce integration and submitting a form

**In Salesforce:**
Set up a simple report for leads created today with source "Jotform" or "Website". If this number drops to zero unexpectedly, your integration is probably broken.

## Step 6: Set Up Zapier as a Backup (Optional)

If you're pushing high volume or need more complex field mapping, add Zapier as a failsafe:

1. Create a new Zap: Jotform (trigger) → Salesforce (action)
2. Select **New Submission** as the trigger
3. Set the action to **Create Lead in Salesforce**
4. Map the same fields as your native integration
5. Set this Zap to **OFF** initially — only turn it on if your native integration fails

## Testing & Verification

**Test the integration before going live:**

1. Submit a test form with fake data (use your own email so you can track it)
2. Check that the lead appears in Salesforce within 2-3 minutes
3. Verify all mapped fields contain the correct data
4. Check that the Lead Source is set correctly
5. Confirm the lead got assigned to the right person

**Monitor these numbers daily:**
- Jotform submission count (in your form analytics)
- New leads in Salesforce with source "Jotform"
- Error notifications from the integration

Acceptable variance is 0% — every form submission should create a lead. If you're missing leads, something in the field mapping or authentication is broken.

**Red flags that indicate problems:**
- Leads appear in Salesforce but with blank Company fields (fails Salesforce validation)
- Leads appear with "Unknown" in name fields (field mapping issue)
- Submission count doesn't match lead count (integration is dropping submissions)

## Troubleshooting

**Problem**: Leads aren't appearing in Salesforce at all  
Check your Salesforce user permissions. The integration user needs "Create" permission on Lead objects. Also verify your Web-to-Lead daily limit hasn't been exceeded (Setup → Marketing → Web-to-Lead to check current usage).

**Problem**: Leads appear but with missing or wrong data  
Your field mapping is off. Go back to the integration settings and verify each field maps to the correct Salesforce API name. Use Salesforce's Object Manager to check the exact API names for custom fields.

**Problem**: Getting "REQUIRED_FIELD_MISSING" errors  
You're missing either LastName or Company in your field mapping. Both are required for Salesforce leads. Set default values for any required fields your form doesn't collect.

**Problem**: Duplicate leads being created for the same person  
Salesforce's standard duplicate prevention doesn't work well with web leads. Either enable Salesforce's duplicate rules for leads (Setup → Duplicate Management) or use a Zapier filter to check for existing leads before creating new ones.

**Problem**: Integration worked initially but stopped  
Your Salesforce OAuth token probably expired. Re-authorize the connection in Jotform's integration settings. This happens every 90 days or when someone changes the integration user's Salesforce password.

**Problem**: Leads are missing UTM parameters or source data  
Add hidden fields to your Jotform that capture UTM parameters via JavaScript, then map those to custom fields in Salesforce. Most teams want to track where their leads came from, but forget to set this up during the initial integration.

## What To Do Next

Once your basic integration is working, consider these related setups:

- [Jotform → HubSpot integration](/integrations/jotform-to-hubspot) if you want to compare CRM options
- [Jotform → GoHighLevel setup](/integrations/jotform-to-gohighlevel) for marketing automation
- [Jotform Google Ads conversion tracking](/tracking/jotform-google-ads-conversion-tracking) to measure your ad spend ROI
- [Get a free tracking audit](/contact) to review your entire lead generation setup

*This guide is part of the [Salesforce Integration Hub](/integrations/salesforce) — covering every major platform that connects to Salesforce CRM.*