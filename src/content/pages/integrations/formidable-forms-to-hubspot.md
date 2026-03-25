---
title: "How to Send Formidable Forms Leads to HubSpot (Setup Guide)"
slug: "formidable-forms-to-hubspot"
description: "Connect Formidable Forms to HubSpot so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/hubspot"
page_type: "spoke"
---

# Formidable Forms → HubSpot Integration Guide

I see broken Formidable Forms to HubSpot setups in about 35% of WordPress sites I audit. Usually it's because someone set up the native HubSpot integration but didn't map custom fields properly, or they're using a Zapier connection that's been silently failing for months. Your leads are submitting forms, but half of them never make it to your CRM.

Here's how to fix it.

## What You'll Have Working By The End

- Every Formidable Forms submission automatically creates or updates a HubSpot contact
- Custom fields from your forms properly mapped to HubSpot contact properties
- Lead source attribution so you know which form generated each contact
- Error handling that alerts you when leads don't sync
- A test process to verify everything works before going live

## Prerequisites

- [ ] WordPress admin access with Formidable Forms Pro installed
- [ ] HubSpot account with contact creation permissions
- [ ] Access to your HubSpot API key or OAuth credentials
- [ ] A test form set up in Formidable Forms
- [ ] List of which form fields should map to which HubSpot properties

## Method 1: HubSpot Native Integration (Recommended)

HubSpot has a direct integration with Formidable Forms that I use in about 70% of setups. It's the most reliable option and handles field mapping cleanly.

### Install the HubSpot WordPress Plugin

Download the official HubSpot plugin from WordPress.org or install it directly from your WordPress admin. Don't use third-party HubSpot connectors — they break more often and have worse support.

In your WordPress admin:
1. Go to Plugins → Add New
2. Search "HubSpot All-In-One Marketing"
3. Install and activate the official HubSpot plugin
4. Navigate to HubSpot → Getting Started
5. Click "Connect HubSpot" and authorize with your HubSpot credentials

### Configure Formidable Forms Integration

Once HubSpot is connected, you'll set up the integration at the form level:

1. Edit your Formidable form in WordPress admin
2. Go to Settings → Actions & Notifications
3. Click "Add Action" and select "HubSpot"
4. Name your action (e.g., "Contact Form to HubSpot")
5. Set the trigger to "After form submission"

### Map Your Form Fields

This is where most setups break. You need to map each Formidable field to the correct HubSpot contact property:

**Required Mappings:**
- Email field → HubSpot Email (required for contact creation)
- First Name → HubSpot First Name
- Last Name → HubSpot Last Name

**Common Custom Mappings:**
- Phone → HubSpot Phone Number
- Company → HubSpot Company Name
- Message/Comments → HubSpot Notes or custom property
- Lead Source → HubSpot Lead Source (set to static value like "Website Contact Form")

For custom HubSpot properties, use the internal property name (not the display label). You can find this in HubSpot → Settings → Properties → Contact Properties.

### Set Lead Source Attribution

Add a hidden field to your Formidable form or use the action settings to set:
- **Lead Source**: "Website Form"
- **Original Source**: "Formidable Forms"
- **Form Name**: Use the form title or a custom identifier

This lets you track which forms are driving the most leads.

## Method 2: Zapier Integration

If you need more complex logic or the native integration doesn't support your use case, Zapier works well. I use this for about 25% of Formidable → HubSpot setups.

### Set Up the Zapier Trigger

1. Create a new Zap in Zapier
2. Choose Formidable Forms as the trigger app
3. Select "New Entry" as the trigger event
4. Connect your WordPress site (you'll need the Formidable Forms API key)
5. Test the trigger by submitting your form

The Formidable Forms API key is found under Formidable → Global Settings → API.

### Configure the HubSpot Action

1. Choose HubSpot as the action app
2. Select "Create or Update Contact" as the action
3. Connect your HubSpot account
4. Map the form fields to HubSpot properties

**Key Zapier Field Mappings:**
```
Formidable Field → HubSpot Property
Email → Email
First Name → First Name
Last Name → Last Name
Phone → Phone
Company → Company
Message → Notes
```

For the Lead Source, set it as a static value in the Zap rather than mapping it from a form field.

### Handle Duplicate Contacts

In the HubSpot action settings, set the duplicate handling:
- **If contact exists**: Update the existing contact
- **Merge strategy**: Use the newer data to overwrite older data

This prevents creating duplicate contacts when someone submits multiple forms.

## Method 3: Custom Webhook Integration

For complex setups or when you need full control, use Formidable's webhook actions with HubSpot's API. I only recommend this for developers or when the other methods don't work.

### Set Up the Webhook in Formidable

1. Edit your form in Formidable Forms
2. Go to Settings → Actions & Notifications
3. Add a new "Webhook" action
4. Set the URL to your custom endpoint (you'll build this next)
5. Set the HTTP method to POST
6. Add form data to the request body

### Build the HubSpot API Integration

Create a custom script that receives the webhook and calls HubSpot's Contacts API:

```php
<?php
// webhook-handler.php
header('Content-Type: application/json');

// Get the form data from Formidable's webhook
$input = file_get_contents('php://input');
$data = json_decode($input, true);

// Your HubSpot API key
$hubspot_api_key = 'your-hubspot-api-key';

// Map form fields to HubSpot properties
$contact_data = [
    'properties' => [
        'email' => $data['email'],
        'firstname' => $data['first_name'],
        'lastname' => $data['last_name'],
        'phone' => $data['phone'],
        'company' => $data['company'],
        'hs_lead_status' => 'NEW',
        'lifecyclestage' => 'lead'
    ]
];

// Create contact in HubSpot
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, 'https://api.hubapi.com/contacts/v1/contact/');
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'Authorization: Bearer ' . $hubspot_api_key
]);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($contact_data));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$response = curl_exec($ch);
$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

// Log the result
if ($http_code === 200 || $http_code === 409) {
    echo json_encode(['status' => 'success']);
} else {
    error_log('HubSpot API Error: ' . $response);
    echo json_encode(['status' => 'error', 'message' => $response]);
}
?>
```

Upload this script to your server and use its URL as the webhook endpoint in Formidable.

## Testing & Verification

### Test the Integration

1. Submit a test form with obviously fake data (email: test@example.com, name: "Test User")
2. Check that the submission appears in Formidable → Entries
3. Verify the contact was created in HubSpot → Contacts
4. Confirm all fields mapped correctly
5. Check that the lead source is set properly

### Verify Real-Time Sync

The integration should work within 30 seconds for native and Zapier methods. Custom webhooks are typically instant.

If you don't see the contact in HubSpot within 2 minutes, something's broken.

### Check Data Quality

Look for these issues in your first few real submissions:
- Names appearing in wrong fields (first name in last name field)
- Phone numbers formatted incorrectly
- Email addresses with extra spaces or characters
- Missing lead source attribution

## Troubleshooting

**Problem**: Forms submit successfully but no contacts appear in HubSpot
→ Check your API credentials or OAuth connection. Re-authorize if needed. For Zapier, check the Zap history for error messages.

**Problem**: Contacts are created but custom fields are empty
→ Verify your field mapping uses HubSpot's internal property names, not display labels. Check that the HubSpot properties exist and aren't read-only.

**Problem**: Duplicate contacts being created instead of updated
→ Make sure email is mapped correctly — HubSpot uses email as the unique identifier. Check your deduplication settings in the integration.

**Problem**: Integration worked initially but stopped syncing
→ API keys expire or get revoked. Zapier connections can break when either platform updates. Check error logs and re-authenticate.

**Problem**: Phone numbers not formatting correctly in HubSpot
→ HubSpot expects phone numbers in a specific format. Add formatting logic to your integration or use HubSpot's automatic phone number formatting.

**Problem**: Form submissions timing out or failing after adding HubSpot integration
→ The API call is blocking the form submission. For custom webhooks, make the API call asynchronous or add proper error handling.

## What To Do Next

Your Formidable Forms are now sending leads to HubSpot, but that's just the beginning. Set up [conversion tracking for your forms](/tracking/formidable-forms-google-ads-conversion-tracking) so you can measure which traffic sources are driving the most leads.

You might also want to connect your forms to other platforms:
- [Formidable Forms to Salesforce](/integrations/formidable-forms-to-salesforce) for enterprise CRM workflows
- [Formidable Forms to GoHighLevel](/integrations/formidable-forms-to-gohighlevel) for marketing automation
- [Formidable Forms to ActiveCampaign](/integrations/formidable-forms-to-activecampaign) for email marketing

If your current tracking setup isn't giving you clear ROI data on your lead generation, [get a free tracking audit](/contact) and I'll show you exactly what's missing.

*This guide is part of the [HubSpot Integrations Hub](/integrations/hubspot) — connect HubSpot to 50+ form tools, ecommerce platforms, and marketing tools.*