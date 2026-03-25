---
title: "How to Send Elementor Forms Leads to GoHighLevel (Setup Guide)"
slug: "elementor-forms-to-gohighlevel"
description: "Connect Elementor Forms to GoHighLevel so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/gohighlevel"
page_type: "spoke"
---

# Elementor Forms → GoHighLevel Integration Guide

I've seen way too many agencies lose leads because their Elementor forms weren't properly connected to GoHighLevel. One client came to me after discovering 3 weeks of form submissions were sitting in their WordPress database while their sales team had no idea these leads existed.

The good news? Once you get this integration right, every form submission flows directly into your GHL pipeline without you touching anything. I'll walk you through the three methods that actually work reliably.

## What You'll Have Working By The End

- Every Elementor form submission automatically creates a new contact in GoHighLevel
- Lead source tracking showing which forms and pages generated each lead
- Proper field mapping so no data gets lost or corrupted
- Error handling so you know immediately if the integration breaks
- Test workflow to verify everything works before going live

## Prerequisites

- [ ] WordPress site with Elementor Pro installed (free version doesn't include forms)
- [ ] GoHighLevel account with API access enabled
- [ ] Admin access to both platforms
- [ ] At least one Elementor form already created and live on your site

## Method 1: GoHighLevel WordPress Plugin (Recommended)

GoHighLevel has an official WordPress plugin that handles this integration natively. This is the most reliable method I've tested — it works in about 95% of setups without any custom code.

### Install the GHL WordPress Plugin

1. In your GoHighLevel account, go to **Sites** → **WordPress Plugin**
2. Download the plugin file or copy the installation code
3. In WordPress, go to **Plugins** → **Add New** → **Upload Plugin**
4. Upload the GHL plugin and activate it
5. Go to **Settings** → **GoHighLevel** and enter your API key

To get your API key:
- In GHL, go to **Settings** → **Integrations** → **API Keys**
- Create a new key with "Contacts: Write" permissions
- Copy the key to your WordPress plugin settings

### Configure Elementor Forms Integration

1. Edit your Elementor form
2. Go to **Actions After Submit**
3. Add the **GoHighLevel** action (it appears after installing the plugin)
4. Map your form fields:

```
Elementor Field → GoHighLevel Field
Name → firstName
Email → email
Phone → phone
Company → companyName
Message → notes
```

5. Set your **Pipeline** and **Source** values
6. Save the form

The plugin handles duplicate detection automatically — if someone submits the form twice with the same email, it updates the existing contact instead of creating a duplicate.

## Method 2: Zapier Integration

If the native plugin doesn't work in your setup, Zapier is the next best option. I use this for about 25% of client implementations, usually when there are complex field mapping requirements.

### Create the Zapier Connection

1. Create a new Zap with **Elementor Forms** as the trigger
2. Choose **New Form Submission** as the trigger event
3. Connect your WordPress site (you'll need to install the Zapier plugin on WordPress)
4. Test the trigger by submitting your Elementor form

### Set Up GoHighLevel Action

1. Add **GoHighLevel** as the action app
2. Choose **Create Contact** as the action event
3. Connect your GHL account using your API credentials
4. Map the fields:

```json
{
  "firstName": "{{Name}}",
  "email": "{{Email}}",
  "phone": "{{Phone}}",
  "companyName": "{{Company}}",
  "source": "Website Form",
  "tags": ["Elementor Lead"],
  "customFields": {
    "form_name": "{{Form Name}}",
    "page_url": "{{Page URL}}"
  }
}
```

5. Set your pipeline assignment in the **Pipeline** section
6. Test the action to make sure it creates a contact correctly

The Zapier method gives you more flexibility for complex field mapping, but it adds a 1-15 minute delay depending on your Zapier plan.

## Method 3: Webhook + API Setup

For maximum control and instant lead delivery, you can set up a custom webhook. This requires some technical setup but gives you the most reliable integration.

### Configure Elementor Form Webhook

1. Edit your Elementor form
2. Go to **Actions After Submit**
3. Add **Webhook** action
4. Set the webhook URL to your processing script: `https://yoursite.com/ghl-webhook.php`
5. Choose **POST** method
6. Leave other settings as default

### Create the Webhook Processing Script

Create a PHP file called `ghl-webhook.php` in your website root:

```php
<?php
// Webhook processor for Elementor → GoHighLevel
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    exit('Method not allowed');
}

// Get form data
$formData = $_POST;

// GoHighLevel API configuration
$ghlApiKey = 'YOUR_GHL_API_KEY';
$ghlLocation = 'YOUR_LOCATION_ID';

// Map Elementor fields to GHL contact structure
$contactData = [
    'firstName' => $formData['form_fields']['name'] ?? '',
    'email' => $formData['form_fields']['email'] ?? '',
    'phone' => $formData['form_fields']['phone'] ?? '',
    'source' => 'Elementor Form',
    'tags' => ['Website Lead'],
    'customFields' => [
        'form_name' => $formData['form_name'] ?? '',
        'page_url' => $_SERVER['HTTP_REFERER'] ?? ''
    ]
];

// Send to GoHighLevel API
$curl = curl_init();
curl_setopt_array($curl, [
    CURLOPT_URL => "https://rest.gohighlevel.com/v1/contacts/",
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST => true,
    CURLOPT_HTTPHEADER => [
        'Authorization: Bearer ' . $ghlApiKey,
        'Content-Type: application/json'
    ],
    CURLOPT_POSTFIELDS => json_encode($contactData)
]);

$response = curl_exec($curl);
$httpCode = curl_getinfo($curl, CURLINFO_HTTP_CODE);
curl_close($curl);

// Log the result
if ($httpCode === 201) {
    error_log('GHL Contact Created: ' . $response);
    echo 'Success';
} else {
    error_log('GHL API Error: ' . $response);
    echo 'Error';
}
?>
```

Replace `YOUR_GHL_API_KEY` and `YOUR_LOCATION_ID` with your actual credentials from GoHighLevel.

This method delivers leads instantly and gives you complete control over error handling and field mapping.

## Testing & Verification

### Test Form Submission

1. Submit a test lead through your Elementor form
2. Use fake but realistic data: "Test User", "test@yourcompany.com", etc.
3. Check that the form submits successfully without errors

### Verify in GoHighLevel

1. Go to **Contacts** in your GHL dashboard
2. Search for your test contact by email
3. Verify all fields mapped correctly:
   - Name appears in firstName field
   - Phone number formatted properly
   - Source shows "Elementor Form" or your custom source
   - Tags applied correctly

### Check Integration Health

- **Zapier**: Check your Zap runs history for any failed attempts
- **Webhook**: Monitor your server error logs for API failures
- **Plugin**: Check WordPress admin for any GHL sync errors

Acceptable delay times:
- **Native Plugin**: Instant (under 10 seconds)
- **Zapier**: 1-15 minutes depending on plan
- **Webhook**: Instant (under 5 seconds)

If you're seeing delays longer than these ranges, something is misconfigured.

## Troubleshooting

**Problem**: Form submits successfully but no contact appears in GoHighLevel
**Solution**: Check your API key permissions. It needs "Contacts: Write" access, not just read access. Also verify your location ID is correct if using the webhook method.

**Problem**: Contact created but missing phone number or other fields
**Solution**: Check your field mapping. Elementor field names are case-sensitive and must match exactly. Use browser dev tools to inspect the form submission and see the actual field names being sent.

**Problem**: Duplicate contacts created for the same email address
**Solution**: GoHighLevel's duplicate detection works on exact email match. If your form is submitting emails with extra spaces or different capitalization, it creates duplicates. Add email normalization to your webhook script or use Zapier's built-in formatter.

**Problem**: Webhook returns 401 Unauthorized error
**Solution**: Your API key is either invalid or expired. Generate a new key in GoHighLevel and make sure you're using the v1 API endpoint, not v2. Also check that your location ID is correct.

**Problem**: Integration worked for a few days then stopped
**Solution**: Usually an API key expiration issue. Some GHL API keys expire after 30-90 days depending on your plan. Check the key status in your GHL settings and regenerate if needed.

**Problem**: Form data appears garbled or in wrong fields in GoHighLevel
**Solution**: Field mapping mismatch. Elementor sometimes changes internal field names when you edit forms. Re-check your mapping and test again. Also verify you're not trying to send arrays or objects to simple text fields.

## What To Do Next

Once your Elementor → GoHighLevel integration is working, set up these related automations:

- [Elementor Forms to HubSpot Integration](/integrations/elementor-forms-to-hubspot) — if you're using multiple CRMs
- [Elementor Forms Google Ads Conversion Tracking](/tracking/elementor-forms-google-ads-conversion-tracking) — to optimize your ad campaigns
- [GoHighLevel Lead Source Attribution](/integrations/gohighlevel) — complete lead tracking setup

Need help with a complex integration setup? [Get a free tracking audit](/contact) and I'll review your current setup and recommend the best approach for your specific situation.

*This guide is part of the [GoHighLevel Integrations Hub](/integrations/gohighlevel) — covering all the ways to connect your lead sources to GHL for automated follow-up.*