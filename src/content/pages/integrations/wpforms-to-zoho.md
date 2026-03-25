---
title: "How to Send WPForms Leads to Zoho CRM (Setup Guide)"
slug: "wpforms-to-zoho"
description: "Connect WPForms to Zoho CRM so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/zoho"
page_type: "spoke"
---

# WPForms → Zoho CRM Integration Guide

You filled out a test form on your site three hours ago, but there's no lead in Zoho CRM. Now you're wondering how many prospects have slipped through the cracks while you assumed this integration was working. I see this exact scenario in about 30% of the WordPress + Zoho setups I audit.

## What You'll Have Working By The End

- Every WPForms submission creates a lead in Zoho CRM automatically
- Form fields mapped to the correct Zoho lead fields (no data ending up in the wrong places)
- Duplicate prevention so returning visitors don't create multiple lead records
- Failed submission alerts so you know immediately when something breaks
- A testing process to verify new leads are flowing correctly

## Prerequisites

- [ ] WordPress site with WPForms installed (Lite or Pro)
- [ ] Active Zoho CRM account with admin access
- [ ] Ability to create new forms or edit existing WPForms
- [ ] If using webhooks: basic understanding of WordPress functions.php or ability to install code snippets

## Method 1: WPForms + Zapier (Recommended for Most Setups)

WPForms doesn't have a direct Zoho CRM integration, so Zapier becomes your most reliable option. It handles the field mapping well and gives you good error reporting when things break.

### Set Up the WPForms Trigger

1. In Zapier, create a new Zap and select **WPForms** as your trigger app
2. Choose **New Form Entry** as the trigger event
3. Connect your WordPress site using your admin login credentials
4. Select the specific form you want to connect (Zapier will pull all your WPForms)
5. Test the trigger by submitting your form — Zapier needs sample data to map fields

### Configure the Zoho CRM Action

1. Add **Zoho CRM** as your action app
2. Choose **Create Lead** as the action event
3. Connect your Zoho CRM account (you'll need to authorize Zapier)
4. Map your form fields to Zoho lead fields:

**Essential Field Mapping:**
- WPForms Name → Zoho "Last Name" (required field)
- WPForms Email → Zoho "Email"  
- WPForms Phone → Zoho "Phone"
- WPForms Company → Zoho "Company"
- WPForms Message → Zoho "Description"

**Pro tip:** Zoho requires "Last Name" but most forms collect "Full Name." Use Zapier's formatter to split the name field, or map the entire name to "Last Name" — it's ugly but functional.

### Handle Lead Source Tracking

Set these static values in Zapier to track where leads came from:
- Lead Source: "Website"
- Lead Status: "Not Contacted" 
- Rating: "Not Rated"

## Method 2: Direct Webhook Integration (For Custom Setups)

If you need more control or want to avoid Zapier costs, you can use WPForms' webhook addon with Zoho's REST API.

### Enable WPForms Webhooks

1. Install the WPForms Webhooks addon (requires Pro license)
2. Edit your form and go to **Settings > Webhooks**
3. Add webhook URL: `https://yoursite.com/wp-json/custom/v1/zoho-webhook`
4. Set method to **POST**
5. Leave authentication empty for now

### Create the Webhook Handler

Add this to your theme's `functions.php` or use a code snippets plugin:

```php
add_action('rest_api_init', function () {
    register_rest_route('custom/v1', '/zoho-webhook', array(
        'methods' => 'POST',
        'callback' => 'handle_wpforms_to_zoho',
        'permission_callback' => '__return_true'
    ));
});

function handle_wpforms_to_zoho($request) {
    $form_data = $request->get_json_params();
    
    // Extract form fields
    $lead_data = array(
        'Last_Name' => $form_data['wpforms']['fields']['1'], // Name field ID
        'Email' => $form_data['wpforms']['fields']['2'],     // Email field ID  
        'Phone' => $form_data['wpforms']['fields']['3'],     // Phone field ID
        'Company' => $form_data['wpforms']['fields']['4'],   // Company field ID
        'Description' => $form_data['wpforms']['fields']['5'], // Message field ID
        'Lead_Source' => 'Website Form'
    );
    
    // Send to Zoho CRM
    $zoho_response = wp_remote_post('https://www.zohoapis.com/crm/v2/Leads', array(
        'headers' => array(
            'Authorization' => 'Zoho-oauthtoken YOUR_ACCESS_TOKEN',
            'Content-Type' => 'application/json'
        ),
        'body' => json_encode(array('data' => array($lead_data)))
    ));
    
    if (is_wp_error($zoho_response)) {
        error_log('Zoho webhook failed: ' . $zoho_response->get_error_message());
        return new WP_Error('webhook_failed', 'Integration error', array('status' => 500));
    }
    
    return new WP_REST_Response('Success', 200);
}
```

**Note:** You'll need to set up Zoho OAuth2 authentication to get a valid access token. This involves creating a Zoho app, getting authorization codes, and refreshing tokens — it's complex enough that most people should stick with Zapier.

### Get Your Form Field IDs

To map the correct fields, inspect your form submission data:
1. Submit your form
2. Check your webhook endpoint logs
3. Note the field IDs (they'll be numbers like `fields.1`, `fields.2`)
4. Update your webhook code with the correct IDs

## Method 3: CSV Export + Manual Import (Last Resort)

If automation isn't working and you need leads in Zoho immediately:

1. In WPForms, go to **Forms > Entries**
2. Select your form and click **Export**
3. Download as CSV
4. In Zoho CRM, go to **Leads > Import Leads**
5. Upload your CSV and map columns to lead fields
6. Review duplicates and import

This obviously doesn't scale, but I've used it to rescue leads while fixing broken integrations.

## Testing & Verification

### Verify the Integration is Working

1. **Submit a test form** with fake but realistic data
2. **Check Zapier activity** (if using Zapier) — you should see the zap triggered successfully
3. **Look for the lead in Zoho CRM** within 2-3 minutes
4. **Verify field mapping** — check that form data ended up in the right Zoho fields
5. **Test duplicate handling** — submit the same email twice and confirm only one lead exists

### Cross-Check Your Numbers

About once a week, compare:
- WPForms entries count (Forms > Entries)  
- Leads created in Zoho from "Website" source
- Zapier task usage (if applicable)

These numbers won't match exactly (spam submissions get filtered, some people submit multiple times), but they should be in the same ballpark. If WPForms shows 50 submissions but Zoho only has 20 leads, something's broken.

### Set Up Failure Alerts

In Zapier, enable email notifications when zaps fail. For webhook integrations, log errors and set up monitoring:

```php
// Add to your webhook handler
if (is_wp_error($zoho_response)) {
    wp_mail(
        'admin@yoursite.com',
        'Zoho Integration Failed',
        'Lead submission failed: ' . print_r($form_data, true)
    );
}
```

## Troubleshooting

**Problem:** Zapier shows "Required field 'Last Name' is missing" → **Solution:** Zoho requires Last Name but your form probably collects "Full Name." Use Zapier's formatter to extract the last word from the full name, or map the entire name to Last Name field.

**Problem:** Leads are created but phone numbers have weird formatting → **Solution:** Use Zapier's formatter to clean phone numbers. Remove all non-numeric characters except + for international numbers.

**Problem:** Form submissions create leads, but they're all assigned to the same Zoho user → **Solution:** In your Zapier action, map Lead Owner to a specific user or use round-robin assignment if you have multiple sales reps.

**Problem:** Integration worked for weeks, now suddenly stopped → **Solution:** Check if your Zoho access token expired (common with webhook integrations). With Zapier, check if your WordPress login credentials changed or if WPForms updated.

**Problem:** Duplicate leads are created when people submit forms multiple times → **Solution:** In Zapier, add a "Find Lead" step before "Create Lead." If a lead with the same email exists, update it instead of creating new one.

**Problem:** Test submissions work but real leads aren't showing up → **Solution:** Check if your form has spam protection enabled. Sometimes legitimate submissions get marked as spam and don't trigger integrations. Review WPForms entries to see if submissions are being recorded at all.

## What To Do Next

Set up [WPForms Google Ads conversion tracking](/tracking/wpforms-google-ads-conversion-tracking) so you know which ads are generating your best leads. If you're using other CRMs, check out [WPForms to HubSpot](/integrations/wpforms-to-hubspot) or [WPForms to Salesforce](/integrations/wpforms-to-salesforce) integration guides. For other Zoho CRM connections, see the [complete Zoho integration hub](/integrations/zoho).

Having trouble with any of these steps? I'll audit your current setup for free and show you exactly what's broken. [Get your free tracking audit here](/contact).

*This guide is part of the [Zoho CRM Integration Hub](/integrations/zoho) — complete setup guides for connecting every major form builder, e-commerce platform, and marketing tool to Zoho CRM.*