---
title: "How to Send Elementor Forms Leads to Salesforce (Setup Guide)"
slug: "elementor-forms-to-salesforce"
description: "Connect Elementor Forms to Salesforce so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/salesforce"
page_type: "spoke"
---

# Elementor Forms → Salesforce Integration Guide

I see this integration broken in about 30% of the WordPress sites I audit. Either they're using a third-party plugin that randomly stops working, or they're manually copying leads from form notifications (which means about 20% of leads never make it to Salesforce). Here's how to set it up properly.

## What You'll Have Working By The End

- Every Elementor form submission automatically creates a lead in Salesforce
- Proper field mapping between your form fields and Salesforce lead fields
- Lead source attribution so you know which forms are driving conversions
- Duplicate lead prevention (or at least proper handling)
- A backup system when the primary integration fails

## Prerequisites

- [ ] WordPress admin access with ability to install plugins
- [ ] Elementor Pro license (required for form Actions After Submit)
- [ ] Salesforce admin access or ability to create Web-to-Lead forms
- [ ] Access to your Salesforce API if going the webhook route
- [ ] Zapier account (if using the Zapier method)

## Method 1: Salesforce Web-to-Lead (Easiest)

This is my go-to for most setups because it's bulletproof. Salesforce handles the heavy lifting, and there's no middle service to break.

### Set Up Web-to-Lead in Salesforce

1. Go to Setup → Feature Settings → Marketing → Web-to-Lead
2. Click "Create Web-to-Lead Form"
3. Select the fields you want to capture:
   - First Name (required)
   - Last Name (required)
   - Email (required)
   - Company
   - Phone
   - Lead Source (set this to "Website Form" or similar)
4. Click "Generate" and copy the HTML form code

You'll get something like this:

```html
<form action="https://webto.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8" method="POST">
<input type="hidden" name="oid" value="00D000000000000">
<input type="hidden" name="retURL" value="http://yoursite.com/thank-you">
<label for="first_name">First Name</label><input id="first_name" maxlength="40" name="first_name" size="20" type="text" />
<label for="last_name">Last Name</label><input id="last_name" maxlength="80" name="last_name" size="20" type="text" />
<label for="email">Email</label><input id="email" maxlength="80" name="email" size="20" type="text" />
<input type="submit" name="submit">
</form>
```

### Configure Elementor Form Actions

1. Edit your Elementor form
2. Go to Content → Actions After Submit
3. Add "Webhook" action
4. Set URL to: `https://webto.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8`
5. Set Method to "POST"
6. Map your fields:

```json
{
  "oid": "00D000000000000",
  "first_name": "[field id='first_name']",
  "last_name": "[field id='last_name']", 
  "email": "[field id='email']",
  "company": "[field id='company']",
  "phone": "[field id='phone']",
  "lead_source": "Website Form"
}
```

Replace `00D000000000000` with your actual Organization ID from the Salesforce form code.

The field IDs in brackets must match your actual Elementor form field IDs exactly.

## Method 2: Zapier Integration (Most Flexible)

Use this when you need custom logic, lead scoring, or want to send data to multiple systems.

### Create the Zap

1. Create new Zap with "Webhooks by Zapier" as trigger
2. Copy the webhook URL Zapier provides
3. In your Elementor form, add Webhook action pointing to that Zapier URL
4. Submit a test form to get the field structure
5. Add "Salesforce" as action step
6. Choose "Create Lead" or "Create/Update Lead"
7. Map fields:
   - First Name → first_name from webhook
   - Last Name → last_name from webhook
   - Email → email from webhook
   - Lead Source → "Website Form" (static value)

### Advanced Zapier Setup

Add filter steps to:
- Skip obvious spam submissions (empty required fields, suspicious email patterns)
- Route different forms to different Salesforce campaigns
- Add lead scoring based on form completion patterns

I typically add a filter that skips leads where email contains common spam domains or where first name is longer than 50 characters.

## Method 3: Custom Webhook + Salesforce API

This is what I use for high-volume sites or when you need real-time lead scoring.

### Set Up Salesforce Connected App

1. Go to Setup → Apps → App Manager
2. Click "New Connected App"
3. Fill basic info and enable OAuth settings
4. Add these OAuth scopes:
   - Full access (full)
   - Perform requests at any time (refresh_token, offline_access)
5. Note your Consumer Key and Consumer Secret

### Create the Webhook Endpoint

You'll need a server endpoint that can receive POST data from Elementor and send it to Salesforce. Here's the basic PHP structure:

```php
<?php
// webhook-to-salesforce.php

// Salesforce OAuth
$client_id = 'your_consumer_key';
$client_secret = 'your_consumer_secret';
$username = 'your_salesforce_username';
$password = 'your_salesforce_password_plus_security_token';

// Get access token
$oauth_url = 'https://login.salesforce.com/services/oauth2/token';
$oauth_data = array(
    'grant_type' => 'password',
    'client_id' => $client_id,
    'client_secret' => $client_secret,
    'username' => $username,
    'password' => $password
);

$oauth_response = curl_post($oauth_url, $oauth_data);
$access_token = $oauth_response['access_token'];
$instance_url = $oauth_response['instance_url'];

// Get form data
$form_data = $_POST;

// Create lead in Salesforce
$lead_data = array(
    'FirstName' => $form_data['first_name'],
    'LastName' => $form_data['last_name'],
    'Email' => $form_data['email'],
    'Company' => $form_data['company'] ?: 'Unknown',
    'LeadSource' => 'Website Form'
);

$create_url = $instance_url . '/services/data/v54.0/sobjects/Lead/';
$headers = array('Authorization: Bearer ' . $access_token);

$result = curl_post($create_url, json_encode($lead_data), $headers);

if ($result['success']) {
    http_response_code(200);
    echo json_encode(['status' => 'success', 'lead_id' => $result['id']]);
} else {
    http_response_code(400);
    echo json_encode(['status' => 'error', 'message' => $result['errors']]);
}
?>
```

### Configure Elementor Form

Point your webhook action to your custom endpoint. Make sure to handle the response properly — if your webhook returns an error, Elementor should know about it.

## Field Mapping Guide

These are the most common field mappings I use:

| Elementor Field | Salesforce API Name | Required |
|----------------|-------------------|----------|
| first_name | FirstName | Yes |
| last_name | LastName | Yes |
| email | Email | Yes |
| company | Company | Yes |
| phone | Phone | No |
| message | Description | No |
| website | Website | No |

**Important**: Salesforce requires Company field for leads, but most contact forms don't ask for it. Set a default value like "Unknown" or "Website Visitor" to avoid errors.

## Testing & Verification

### Test the Integration

1. Submit a test form with your own contact info
2. Check Salesforce within 2-3 minutes for the new lead
3. Verify all mapped fields populated correctly
4. Check that Lead Source is set properly

### Check Lead Assignment Rules

If your test lead didn't get assigned to the right person, check:
- Setup → Feature Settings → Marketing → Lead Assignment Rules
- Make sure your Web-to-Lead or API submissions trigger assignment rules
- Test with different email domains if you have territory-based assignment

### Monitor Integration Health

Set up Salesforce reports to track:
- Leads created in last 24 hours with Lead Source = "Website Form"
- Failed Web-to-Lead submissions (Setup → Monitoring → Email Log Files)
- API call usage if using custom webhooks

I typically see 5-10% of Web-to-Lead submissions fail due to validation errors or duplicate rules. That's normal.

## Troubleshooting

**Problem**: Form submits successfully but no lead appears in Salesforce
→ Check your Organization ID in the Web-to-Lead setup. A single wrong character will cause silent failures. Also verify your Salesforce email settings aren't blocking the notifications.

**Problem**: Leads are created but assigned to the wrong person
→ Your Lead Assignment Rules aren't firing. Go to Setup → Lead Assignment Rules and make sure "Use active assignment rule" is checked in your Web-to-Lead setup.

**Problem**: Getting "Required field missing" errors
→ Usually the Company field. Elementor forms rarely ask for company, but Salesforce requires it for leads. Add a hidden field with a default value like "Website Visitor" or modify your lead creation process to set a default.

**Problem**: Duplicate leads being created for the same person
→ Check your Salesforce Duplicate Rules (Setup → Duplicate Management). You might want to allow duplicates from forms since people often fill out multiple forms over time, but update the Contact record instead of creating a new Lead.

**Problem**: Webhook timeouts with Zapier method
→ Zapier webhooks timeout after 30 seconds. If your form has redirect actions or other slow processes, they might conflict. Set webhook actions to fire first in your Actions After Submit list.

**Problem**: API rate limits with custom webhook approach
→ Salesforce has API call limits. If you're hitting them, implement queuing on your webhook endpoint or switch to bulk API calls for high-volume forms.

## What To Do Next

Now that your leads are flowing into Salesforce, you'll want to:

- Set up [Elementor Forms → Google Ads conversion tracking](/tracking/elementor-forms-google-ads-conversion-tracking) to measure your form performance
- Consider [Elementor Forms → HubSpot integration](/integrations/elementor-forms-to-hubspot) if you need more marketing automation
- Explore [Elementor Forms → GoHighLevel](/integrations/elementor-forms-to-gohighlevel) for SMS follow-up capabilities
- Get a [free tracking audit](/contact) to make sure your lead attribution is working properly

*This guide is part of the [Salesforce Integrations Hub](/integrations/salesforce) — connecting your forms, landing pages, and websites to Salesforce CRM.*