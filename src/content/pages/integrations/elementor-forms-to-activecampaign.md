---
title: "How to Send Elementor Forms Leads to ActiveCampaign (Setup Guide)"
slug: "elementor-forms-to-activecampaign"
description: "Connect Elementor Forms to ActiveCampaign so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/activecampaign"
page_type: "spoke"
---

# Elementor Forms → ActiveCampaign Integration Guide

I see this exact problem in about 60% of WordPress sites I audit: beautiful Elementor forms that generate leads but dump them into a black hole. The form works, the thank you page shows up, but the lead never makes it to ActiveCampaign where your sales team can actually work it.

The biggest issue? Most people try to use Elementor's native "Actions After Submit" integration, which breaks silently when ActiveCampaign changes their API, leaving you with weeks of missed leads before anyone notices.

## What You'll Have Working By The End

- Elementor form submissions automatically create new contacts in ActiveCampaign
- Custom form fields mapped to the right ActiveCampaign fields (including custom fields)
- Failed submissions logged so you don't lose leads when the API is down
- Test process to verify every new form is connected before going live

## Prerequisites

- [ ] WordPress site with Elementor Pro (the free version doesn't have form actions)
- [ ] ActiveCampaign account with API access
- [ ] Admin access to both your WordPress dashboard and ActiveCampaign settings
- [ ] Your ActiveCampaign API key and account URL (found under Settings → Developer)

## Method 1: Zapier Integration (Recommended)

Zapier is the most reliable method because it handles API changes, provides error logging, and works with Elementor's webhook action without custom code.

### Set Up the Elementor Webhook

In your WordPress dashboard, edit the Elementor form and go to Actions After Submit:

1. Add a new action and select "Webhook"
2. Set the Webhook URL to your Zapier webhook URL (we'll generate this next)
3. In the "Advanced" section, set Request Format to "JSON"
4. Leave all other fields at defaults

### Create the Zapier Integration

1. In Zapier, create a new Zap with "Webhooks by Zapier" as the trigger
2. Choose "Catch Hook" and copy the webhook URL
3. Paste this URL back into your Elementor webhook action
4. Submit a test form to send sample data to Zapier

For the action step:
1. Search for and select "ActiveCampaign"
2. Choose "Create/Update Contact" as the action
3. Connect your ActiveCampaign account using your API key and account URL
4. Map the form fields:
   - `form_fields[email]` → Email
   - `form_fields[name]` → First Name (or split into First/Last)
   - `form_fields[phone]` → Phone
   - `form_fields[company]` → Company (if you have this field)

### Field Mapping for Custom Fields

If you're using custom fields in Elementor, you'll need to map them to ActiveCampaign custom fields:

1. In ActiveCampaign, go to Settings → Custom Fields and note the field names
2. In Zapier's field mapping, scroll to the "Custom Fields" section
3. Map using this format: `form_fields[field_id]` where `field_id` is your Elementor field's CSS ID

Common custom field mappings:
- `form_fields[budget]` → Budget (number field)
- `form_fields[message]` → Message (textarea field)
- `form_fields[source]` → Lead Source (dropdown)

## Method 2: Direct API Integration (Advanced)

If you want more control and don't mind maintaining custom code, you can integrate directly with ActiveCampaign's API using Elementor's webhook action.

### Set Up the Webhook Handler

Create a new PHP file in your theme's directory (e.g., `activecampaign-webhook.php`):

```php
<?php
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    exit('Method not allowed');
}

$data = json_decode(file_get_contents('php://input'), true);

// ActiveCampaign API credentials
$api_url = 'https://YOUR-ACCOUNT.api-us1.com';
$api_key = 'YOUR-API-KEY';

// Map form fields
$contact_data = [
    'contact' => [
        'email' => $data['form_fields']['email'] ?? '',
        'firstName' => $data['form_fields']['name'] ?? '',
        'phone' => $data['form_fields']['phone'] ?? '',
        'fieldValues' => []
    ]
];

// Add custom fields if they exist
if (!empty($data['form_fields']['company'])) {
    $contact_data['contact']['fieldValues'][] = [
        'field' => 'COMPANY_FIELD_ID', // Replace with your field ID
        'value' => $data['form_fields']['company']
    ];
}

// Send to ActiveCampaign
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $api_url . '/api/3/contacts');
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($contact_data));
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Api-Token: ' . $api_key,
    'Content-Type: application/json'
]);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$response = curl_exec($ch);
$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

// Log the result
error_log("ActiveCampaign API Response: " . $response);

http_response_code($http_code >= 200 && $http_code < 300 ? 200 : 500);
?>
```

### Configure Elementor to Use Your Webhook

1. In Elementor, set your webhook URL to `https://yoursite.com/path/to/activecampaign-webhook.php`
2. Set Request Format to "JSON"
3. Make sure your server has cURL enabled

## Method 3: WordPress Plugin Integration

Several plugins can bridge Elementor Forms to ActiveCampaign without custom code.

### Using WP Webhooks

1. Install the WP Webhooks plugin
2. Go to WP Webhooks → Send Data and create a new webhook
3. Set the trigger to "Elementor Form Submit"
4. Configure the webhook URL as ActiveCampaign's API endpoint
5. Add authentication headers with your API key

This method gives you a middle ground between Zapier's simplicity and custom code's control.

## Testing & Verification

### Test the Integration

1. Fill out your Elementor form with test data (use a real email you can access)
2. Submit the form and check for the success message
3. Check your webhook logs (Zapier activity, PHP error logs, or plugin logs)

### Verify in ActiveCampaign

1. Go to Contacts in your ActiveCampaign dashboard
2. Search for the email address you used in testing
3. Open the contact and verify all fields populated correctly
4. Check that any custom fields contain the right data

### Check the Numbers

Compare form submissions to new contacts over a 24-hour period. You should see:
- 90%+ of form submissions create new contacts
- Existing contacts get updated (not duplicated)
- Custom fields populate correctly
- Any failed submissions logged for review

## Troubleshooting

**Problem: Form submits but no contact appears in ActiveCampaign**
Check your API credentials first. Test them by making a direct API call outside of the form integration. Also verify your webhook URL is accessible and returning HTTP 200.

**Problem: Contact created but fields are blank**
This usually means field mapping is wrong. Check that your Elementor field IDs match what you're sending in the webhook. Use browser dev tools to inspect the form and confirm field names.

**Problem: Duplicate contacts being created**
ActiveCampaign should dedupe by email automatically, but if you're seeing duplicates, check that the email field is properly mapped and contains valid email addresses. Some setups accidentally map the name field to email.

**Problem: Webhook timeout errors**
ActiveCampaign's API can be slow during peak hours. Increase your webhook timeout to 30 seconds and implement retry logic if using custom code. Zapier handles retries automatically.

**Problem: Special characters breaking the integration**
If form submissions contain quotes, apostrophes, or Unicode characters, they might break JSON parsing. Ensure your webhook handler properly escapes data before sending to ActiveCampaign.

**Problem: Integration works but stops after a few days**
This typically happens with custom API integrations when ActiveCampaign updates their API. Monitor your error logs and have a fallback method ready. Zapier integrations rarely break this way.

## What To Do Next

Once your Elementor forms are flowing into ActiveCampaign, set up tracking to measure the ROI of your lead generation:

- [Elementor Forms Google Ads Conversion Tracking](/tracking/elementor-forms-google-ads-conversion-tracking) — Track which ads generate the most leads
- [Elementor Forms to HubSpot](/integrations/elementor-forms-to-hubspot) — Compare CRM performance
- [Elementor Forms to Salesforce](/integrations/elementor-forms-to-salesforce) — Enterprise CRM alternative
- [Get a free tracking audit](/contact) — I'll review your entire lead flow and find what's broken

*This guide is part of the [ActiveCampaign Integrations Hub](/integrations/activecampaign) — covering every way to get data into and out of ActiveCampaign for better lead management.*