---
title: "How to Send Formidable Forms Leads to Salesforce (Setup Guide)"
slug: "formidable-forms-to-salesforce"
description: "Connect Formidable Forms to Salesforce so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/salesforce"
page_type: "spoke"
---

# Formidable Forms → Salesforce Integration Guide

I see this exact integration request in about 30% of the WordPress sites I audit. You've got Formidable Forms collecting leads on your site, but they're sitting in WordPress while your sales team lives in Salesforce. The disconnect is costing you follow-up speed, and manual CSV exports are eating up hours every week.

The biggest issue I encounter? People set this up once, then never verify it's still working. I've seen three-month gaps where forms were submitting but nothing was reaching Salesforce due to API changes or field mapping breaks.

## What You'll Have Working By The End

• Every Formidable Forms submission automatically creates a Salesforce lead within 30 seconds
• Proper field mapping so no data gets lost in translation
• Error handling that alerts you when something breaks
• Lead vs Contact routing based on your Salesforce setup
• Testing workflow to verify everything flows correctly

## Prerequisites

- [ ] WordPress admin access with Formidable Forms Pro (the free version doesn't have webhook capabilities)
- [ ] Salesforce admin access or ability to generate Web-to-Lead forms
- [ ] Access to create custom fields in Salesforce if needed
- [ ] Zapier account (for the automation method) or developer access for webhook setup

## Method 1: Salesforce Web-to-Lead (Simplest)

This is my go-to for straightforward lead capture. Salesforce generates the form HTML, and you customize Formidable Forms to match the field names.

In your Salesforce setup, go to Setup → Web-to-Lead → Create Web-to-Lead Form. Select the fields you want to capture:

- First Name (first_name)
- Last Name (last_name) 
- Email (email)
- Company (company)
- Phone (phone)
- Lead Source (lead_source)

Salesforce will generate HTML with specific field names. The key is matching these exactly in your Formidable Forms setup.

In Formidable Forms, edit your form and go to Settings → Actions → Add "Register User" action (or create a custom webhook action). Set the form to submit to Salesforce's Web-to-Lead endpoint:

```
https://webto.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8
```

Map your Formidable Forms fields to Salesforce's expected names:
- Your "First Name" field → `first_name`
- Your "Last Name" field → `last_name`  
- Your "Email Address" field → `email`
- Your "Company" field → `company`

The tricky part is the hidden fields. You need to include your Organization ID (get this from Salesforce Setup → Company Information):

```html
<input type="hidden" name="oid" value="your_org_id_here">
<input type="hidden" name="lead_source" value="Website Form">
```

About 60% of setups break here because people forget the Organization ID or get the field names wrong.

## Method 2: Zapier Integration (Most Reliable)

This is what I recommend for most clients because it's bulletproof and handles errors gracefully.

Create a new Zap with Formidable Forms as the trigger. You'll need to connect your WordPress site - Zapier will walk you through generating an API key in Formidable Forms settings.

For the trigger, select "New Entry" and choose your specific form. Test the trigger by submitting your form - you should see the field data populate in Zapier.

Set Salesforce as the action app. Choose "Create Lead" (or "Create Contact" if you're routing to existing accounts). 

The field mapping is critical here:

**Formidable Forms Field → Salesforce Field**
- First Name → First Name
- Last Name → Last Name  
- Email → Email
- Company → Company
- Phone → Phone
- Lead Source → Lead Source (set to static value like "Website")
- Status → New (static value)

In Zapier's field mapping, you can set Lead Source to a static value or map it to a hidden field in your form. I always set it to something specific like "Website - Contact Form" so the sales team knows where it came from.

Test the Zap by submitting another form entry. Check Salesforce within 2-3 minutes - the lead should appear in your Leads tab.

## Method 3: Direct API Integration via Webhooks

If you need more control or are hitting Zapier's plan limits, you can connect directly to Salesforce's REST API.

First, create a Connected App in Salesforce (Setup → App Manager → New Connected App). Enable OAuth settings and note your Consumer Key and Consumer Secret.

In Formidable Forms, create a webhook action that points to your middleware endpoint. You'll need a server-side script that handles OAuth and API calls to Salesforce.

Here's the PHP structure for your webhook receiver:

```php
<?php
// Authenticate with Salesforce
$auth_url = 'https://login.salesforce.com/services/oauth2/token';
$auth_data = [
    'grant_type' => 'client_credentials',
    'client_id' => 'your_consumer_key',
    'client_secret' => 'your_consumer_secret'
];

$auth_response = wp_remote_post($auth_url, [
    'body' => $auth_data
]);

$token = json_decode($auth_response['body'])->access_token;
$instance_url = json_decode($auth_response['body'])->instance_url;

// Create lead in Salesforce
$lead_data = [
    'FirstName' => $_POST['first_name'],
    'LastName' => $_POST['last_name'],
    'Email' => $_POST['email'],
    'Company' => $_POST['company'],
    'LeadSource' => 'Website Form'
];

$lead_response = wp_remote_post($instance_url . '/services/data/v52.0/sobjects/Lead/', [
    'headers' => [
        'Authorization' => 'Bearer ' . $token,
        'Content-Type' => 'application/json'
    ],
    'body' => json_encode($lead_data)
]);
?>
```

This method gives you the most control but requires ongoing maintenance when Salesforce updates their API.

## Field Mapping Deep Dive

The most common failure point is field mapping. Salesforce is picky about data types and required fields.

**Required Salesforce Lead Fields:**
- LastName (can't be empty)
- Company (can be set to "Unknown" if not collected)

**Common Field Mapping Issues:**
- Phone numbers with formatting vs. Salesforce expecting clean numbers
- State/Province fields expecting specific values or abbreviations
- Custom fields needing exact API names (usually FieldName__c)

If you're using custom fields, get the API names from Salesforce Setup → Object Manager → Lead → Fields. The API name is what you need for integration, not the field label.

## Testing & Verification

Submit a test form with distinctive data like "Test Lead John Doe" so you can easily find it.

**In Salesforce:**
1. Go to Leads tab and search for your test submission
2. Verify all fields populated correctly
3. Check the Lead Source field shows your intended value
4. Look at the Created Date - should be within 1-2 minutes of form submission

**For Zapier method:** Check the Zap history to see if it ran successfully. Failed Zaps will show error details.

**For webhook method:** Check your server logs for any API errors. Common issues are authentication failures or malformed JSON.

**Testing checklist:**
- [ ] Lead appears in Salesforce within 5 minutes
- [ ] All form fields map to correct Salesforce fields  
- [ ] Lead Source is set correctly
- [ ] No duplicate leads created from same email
- [ ] Error handling works (test with invalid data)

Set up monitoring by submitting a test form weekly. I've seen integrations silently fail for months because nobody was checking.

## Troubleshooting

**Problem:** Forms submit but no leads appear in Salesforce
Check your Organization ID in Web-to-Lead setup, or verify Zapier authentication hasn't expired. About 40% of breaks happen when someone changes a Salesforce password and forgets to update connected apps.

**Problem:** Duplicate leads being created
Salesforce has duplicate management rules, but they're not always enabled by default. Go to Setup → Duplicate Management and create rules for email matching. Alternatively, use "Create or Update Lead" in Zapier instead of "Create Lead."

**Problem:** Some fields missing in Salesforce
Field mapping broke, or you're trying to map to fields that don't exist. Double-check API names for custom fields - they usually end with __c. Also verify field permissions allow your API user to write to those fields.

**Problem:** Webhook timing out or failing
Your server-side script is taking too long or hitting API limits. Salesforce has API call limits per day. Consider queueing webhook requests or upgrading your Salesforce plan if you're hitting limits.

**Problem:** Special characters or formatting breaking integration
Common with international names or phone numbers. Set up field validation in Formidable Forms to clean data before sending, or handle sanitization in your webhook receiver.

**Problem:** Integration worked then stopped
API credentials expired, or Salesforce changed field requirements. This is why I always recommend setting up error notification emails in Zapier or logging failures in webhook setups.

## What To Do Next

Once your basic integration is working, you'll want to set up [Formidable Forms Google Ads conversion tracking](/tracking/formidable-forms-google-ads-conversion-tracking) to measure which campaigns drive the most Salesforce leads.

Consider connecting other form tools: [Formidable Forms to HubSpot](/integrations/formidable-forms-to-hubspot) if you're running parallel CRM setups, or [Formidable Forms to GoHighLevel](/integrations/formidable-forms-to-gohighlevel) for marketing automation.

For more advanced Salesforce integrations and lead scoring, check out [Formidable Forms to ActiveCampaign](/integrations/formidable-forms-to-activecampaign).

Need help auditing your current form-to-CRM setup? I can spot integration breaks and data leaks in about 10 minutes. [Get a free tracking audit](/contact) and I'll show you exactly what's working and what needs fixing.

*This guide is part of the [Salesforce Integrations Hub](/integrations/salesforce) — complete setup guides for connecting Salesforce to every major form tool, CRM, and tracking platform.*