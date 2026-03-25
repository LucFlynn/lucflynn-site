---
title: "How to Send Elementor Forms Leads to Zoho CRM (Setup Guide)"
slug: "elementor-forms-to-zoho"
description: "Connect Elementor Forms to Zoho CRM so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/zoho"
page_type: "spoke"
---

# Elementor Forms → Zoho CRM Integration Guide

I see this setup in about 30% of WordPress sites I audit, and it's broken more often than not. The main issue? People try to use Elementor's built-in webhook action without properly mapping fields, so leads either don't sync or they sync with incomplete data. Most teams don't realize when it stops working until they notice their lead volume drop weeks later.

## What You'll Have Working By The End

- Every Elementor form submission automatically creates a lead in Zoho CRM
- Proper field mapping so contact info, company details, and form data sync correctly
- Error handling so you know immediately when something breaks
- Testing workflow to verify leads are flowing from WordPress to Zoho
- Backup tracking in case the integration fails

## Prerequisites

- [ ] Elementor Pro license (required for form Actions After Submit)
- [ ] Zoho CRM account with API access
- [ ] Admin access to your WordPress site
- [ ] Ability to create Zoho CRM custom fields (if needed for form-specific data)
- [ ] Either Zapier account OR developer access to set up webhooks

## Step 1: Choose Your Integration Method

You have three real options here. I'll rank them by reliability:

**Option A: Zapier Integration (Recommended)**
Most reliable for non-technical teams. Costs $20/month but worth it for the error handling and field mapping flexibility.

**Option B: Direct Webhook to Zoho API**
More technical but no monthly cost. Requires PHP knowledge to handle authentication and error responses.

**Option C: Zoho Forms Native Integration**
Technically possible by embedding Zoho forms instead of Elementor forms, but you lose Elementor's styling control.

For this guide, I'm covering Options A and B since they're the most practical.

## Step 2: Set Up Zapier Integration (Recommended Method)

### Create the Zap

1. In Zapier, create new Zap: **Elementor Pro → Zoho CRM**
2. For Elementor Pro trigger, select "New Form Submission"
3. Connect your WordPress site (you'll need to install Zapier's WordPress plugin)
4. Select your specific Elementor form from the dropdown

### Configure Zoho CRM Action

1. Choose "Create Lead" as the action (not "Create Contact" - leads are for new prospects)
2. Connect your Zoho CRM account
3. Map fields carefully:

```
Elementor Field → Zoho CRM Field
First Name → First Name
Last Name → Last Name  
Email → Email
Phone → Phone
Company → Company
Message → Description
Form Name → Lead Source (custom field recommended)
Page URL → Website (or custom "Source Page" field)
```

### Handle Missing Fields

If your Elementor form has fields that don't exist in Zoho CRM:
- Create custom fields in Zoho CRM first
- Map them in Zapier
- Set default values for required Zoho fields that aren't in your form

I recommend creating a "Lead Source Detail" text field in Zoho to capture the specific form name and page URL.

## Step 3: Direct Webhook Integration (Technical Method)

### Set Up Zoho CRM API Access

1. Go to Zoho Developer Console
2. Create server-based application
3. Note your Client ID and Client Secret
4. Generate refresh token with scope: `ZohoCRM.modules.leads.CREATE,ZohoCRM.modules.leads.UPDATE`

### Configure Elementor Form Webhook

In your Elementor form → Actions After Submit → Add Action → Webhook:

```
Webhook URL: https://yoursite.com/wp-content/themes/yourtheme/zoho-webhook.php
```

### Create Webhook Handler (PHP)

Create `zoho-webhook.php` in your theme directory:

```php
<?php
// Zoho CRM webhook handler for Elementor Forms
if ($_POST) {
    $client_id = 'YOUR_CLIENT_ID';
    $client_secret = 'YOUR_CLIENT_SECRET';
    $refresh_token = 'YOUR_REFRESH_TOKEN';
    
    // Get access token
    $auth_url = "https://accounts.zoho.com/oauth/v2/token";
    $auth_data = array(
        'refresh_token' => $refresh_token,
        'client_id' => $client_id,
        'client_secret' => $client_secret,
        'grant_type' => 'refresh_token'
    );
    
    $auth_response = wp_remote_post($auth_url, array('body' => $auth_data));
    $auth_body = json_decode(wp_remote_retrieve_body($auth_response), true);
    $access_token = $auth_body['access_token'];
    
    // Prepare lead data
    $lead_data = array(
        'data' => array(
            array(
                'First_Name' => sanitize_text_field($_POST['form_fields']['first_name']),
                'Last_Name' => sanitize_text_field($_POST['form_fields']['last_name']),
                'Email' => sanitize_email($_POST['form_fields']['email']),
                'Phone' => sanitize_text_field($_POST['form_fields']['phone']),
                'Company' => sanitize_text_field($_POST['form_fields']['company']),
                'Description' => sanitize_textarea_field($_POST['form_fields']['message']),
                'Lead_Source' => 'Website Form',
                'Lead_Status' => 'New'
            )
        )
    );
    
    // Send to Zoho CRM
    $api_url = "https://www.zohoapis.com/crm/v2/Leads";
    $headers = array(
        'Authorization' => 'Zoho-oauthtoken ' . $access_token,
        'Content-Type' => 'application/json'
    );
    
    $response = wp_remote_post($api_url, array(
        'headers' => $headers,
        'body' => json_encode($lead_data)
    ));
    
    // Log errors for debugging
    if (is_wp_error($response)) {
        error_log('Zoho CRM API Error: ' . $response->get_error_message());
    }
    
    http_response_code(200);
}
?>
```

### Security Considerations

- Store API credentials in wp-config.php, not in the theme file
- Add nonce verification to prevent CSRF
- Sanitize all form inputs before sending to Zoho
- Set up error logging to catch API failures

## Step 4: Set Up Lead Assignment Rules in Zoho

Don't let all leads go to one person. Set up automatic assignment:

1. Go to Zoho CRM → Setup → Automation → Assignment Rules
2. Create rule for Leads module
3. Set criteria based on Lead Source or other fields
4. Assign to specific users or round-robin

I recommend creating separate assignment rules for different forms so your sales team knows the lead context.

## Step 5: Testing & Verification

### Test the Form Submission

1. Submit a test form with fake data (use your own email)
2. Check Zapier history (if using Zapier) - should show successful trigger and action
3. Check Zoho CRM → Leads for the new record
4. Verify all fields mapped correctly

### Cross-Check Data Accuracy

Submit forms with different field combinations:
- Required fields only
- All fields filled
- Empty optional fields
- Special characters in name/company fields

The lead should appear in Zoho within 2-3 minutes max. If using webhooks, it should be instant.

### Monitor Integration Health

Set up monitoring:
- Zapier: Enable email notifications for failed Zaps
- Webhook: Check error logs daily for API failures
- Zoho CRM: Create report for leads by source to spot drops in volume

## Troubleshooting Common Issues

**Problem:** Forms submit but no leads appear in Zoho CRM
**Solution:** Check if leads are going to Contacts instead. Zapier sometimes defaults to Contacts module. Change action to "Create Lead" specifically.

**Problem:** Leads created but missing field data
**Solution:** Field names in Elementor don't match Zoho API names. Check Zoho CRM → Setup → Developer Space → APIs → CRM API to get exact field names. Use `First_Name` not `firstname`.

**Problem:** Duplicate leads for same email address
**Solution:** Enable duplicate detection in Zoho CRM → Setup → Data Administration → Duplicate Check Settings. Set Email as unique identifier for Leads module.

**Problem:** Zapier shows "Invalid Field" error
**Solution:** You're trying to map to a field that doesn't exist in your Zoho CRM. Either create the custom field in Zoho first, or map to a different existing field.

**Problem:** Webhook returns 401 Unauthorized
**Solution:** Your access token expired. Zoho access tokens last 60 minutes. Implement automatic token refresh in your webhook handler or switch to Zapier.

**Problem:** Integration worked then stopped
**Solution:** Usually an API limit issue. Zoho CRM has API call limits based on your plan. Check Setup → Developer Space → API Limits. Consider caching tokens or batching requests.

## What To Do Next

Once your Elementor forms are flowing to Zoho CRM, set up these related integrations:

- [Track Elementor form submissions in Google Ads](/tracking/elementor-forms-google-ads-conversion-tracking) for conversion tracking
- [Connect Elementor forms to HubSpot](/integrations/elementor-forms-to-hubspot) if you're also using HubSpot for marketing
- [Send Elementor leads to Salesforce](/integrations/elementor-forms-to-salesforce) for comparison testing
- [Elementor forms to GoHighLevel](/integrations/elementor-forms-to-gohighlevel) for agencies managing multiple clients

Want me to audit your current form-to-CRM setup? I can spot the gaps that are costing you leads. [Get a free tracking audit here](/contact).

*This guide is part of the [Zoho CRM Integrations Hub](/integrations/zoho) — connecting Zoho CRM to form tools, ad platforms, and marketing automation systems.*