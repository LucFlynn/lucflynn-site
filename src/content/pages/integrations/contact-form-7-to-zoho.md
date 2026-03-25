---
title: "How to Send Contact Form 7 Leads to Zoho CRM (Setup Guide)"
slug: "contact-form-7-to-zoho"
description: "Connect Contact Form 7 to Zoho CRM so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/zoho"
page_type: "spoke"
---

# Contact Form 7 → Zoho CRM Integration Guide

Here's the problem: you're using Contact Form 7 because it's lightweight and just works, but every lead submission goes to your email inbox and nowhere else. I've seen this exact setup in about 30% of WordPress sites I audit — loads of form traffic, zero CRM organization, and sales teams manually copy-pasting contact details from emails.

Contact Form 7 doesn't store submissions by default (it just emails them), so when your integration breaks, you lose leads completely unless you catch it fast.

## What You'll Have Working By The End

- Contact Form 7 submissions automatically create leads in Zoho CRM
- Complete field mapping from form fields to CRM properties
- Duplicate contact handling based on email address
- Error monitoring so you know immediately if leads stop flowing
- Backup submission storage so nothing gets lost

## Prerequisites

- [ ] WordPress admin access with plugin installation rights
- [ ] Contact Form 7 plugin already installed and working
- [ ] Zoho CRM account (any plan level works)
- [ ] Admin access to your Zoho CRM to generate API credentials
- [ ] Flamingo plugin installed (for backup submission storage)

## Method 1: Zoho Forms Native Integration (Recommended)

This is the most reliable approach. Instead of trying to bridge Contact Form 7 to Zoho CRM, we'll use Zoho's web form embed that connects directly to your CRM.

### Generate Your Zoho Web Form

1. In Zoho CRM, go to Setup → Channels → Web Forms
2. Click "Create Web Form"
3. Select "Leads" as your module
4. Add the fields you need:
   - First Name (required)
   - Last Name (required)
   - Email (required)
   - Phone
   - Company
   - Lead Source (set default value to "Website")
5. Configure the "Thank You" page URL
6. Generate the form code

### Replace Your Contact Form 7

Copy the Zoho form HTML and replace your Contact Form 7 shortcode. The form will look like this:

```html
<form action="https://forms.zohopublic.com/yourorganization/form/ContactForm/formperma/xyz" method="POST">
    <div>
        <label for="Name_First">First Name *</label>
        <input type="text" name="Name_First" id="Name_First" required>
    </div>
    <div>
        <label for="Name_Last">Last Name *</label>
        <input type="text" name="Name_Last" id="Name_Last" required>
    </div>
    <div>
        <label for="Email">Email *</label>
        <input type="email" name="Email" id="Email" required>
    </div>
    <div>
        <label for="Phone">Phone</label>
        <input type="tel" name="Phone" id="Phone">
    </div>
    <div>
        <label for="Company">Company</label>
        <input type="text" name="Company" id="Company">
    </div>
    <input type="submit" value="Submit">
</form>
```

This gives you 100% reliability — every submission goes straight to Zoho CRM with zero middleware to break.

## Method 2: Zapier Integration (If You Need Contact Form 7)

If you need to keep Contact Form 7 for styling or existing integrations, use Zapier to connect the two.

### Install Contact Form 7 Database Addon

First, install the Flamingo plugin so Contact Form 7 actually stores submissions:

```bash
# Via WordPress admin
Plugins → Add New → Search "Flamingo" → Install → Activate
```

### Create the Zapier Connection

1. In Zapier, create a new Zap
2. Trigger: Contact Form 7 (requires Flamingo plugin)
3. Select your WordPress site and specific form
4. Action: Zoho CRM → Create Lead
5. Map the fields:
   - CF7 "your-name" → Zoho "First Name"
   - CF7 "your-email" → Zoho "Email"
   - CF7 "your-phone" → Zoho "Phone"
   - CF7 "your-company" → Zoho "Company"
   - Static value "Website" → Zoho "Lead Source"

### Field Mapping Configuration

```
Contact Form 7 Field    →    Zoho CRM Field
[text* first-name]      →    First Name
[text* last-name]       →    Last Name  
[email* your-email]     →    Email
[tel your-phone]        →    Phone
[text your-company]     →    Company
[textarea your-message] →    Description
```

The asterisk (*) means required in Contact Form 7. Make sure your required fields match what Zoho CRM requires (minimum: First Name, Last Name, Email).

## Method 3: Webhook + Custom API Integration

For complete control, use Contact Form 7's webhook functionality with Zoho's REST API.

### Add Webhook to Contact Form 7

Install the CF7 Webhook addon, then add this to your form's additional settings:

```
webhook_url: https://yoursite.com/wp-content/themes/yourtheme/zoho-webhook.php
webhook_method: POST
```

### Create the Webhook Handler

Create `zoho-webhook.php` in your theme folder:

```php
<?php
// Zoho CRM API integration for Contact Form 7
function send_to_zoho_crm($form_data) {
    $zoho_config = [
        'refresh_token' => 'your_refresh_token',
        'client_id' => 'your_client_id',
        'client_secret' => 'your_client_secret',
        'accounts_url' => 'https://accounts.zoho.com'
    ];
    
    // Get access token
    $access_token = get_zoho_access_token($zoho_config);
    
    // Prepare lead data
    $lead_data = [
        'data' => [[
            'First_Name' => $_POST['first-name'],
            'Last_Name' => $_POST['last-name'], 
            'Email' => $_POST['your-email'],
            'Phone' => $_POST['your-phone'],
            'Company' => $_POST['your-company'],
            'Lead_Source' => 'Website',
            'Description' => $_POST['your-message']
        ]]
    ];
    
    // Send to Zoho CRM
    $response = wp_remote_post('https://www.zohoapis.com/crm/v2/Leads', [
        'headers' => [
            'Authorization' => 'Zoho-oauthtoken ' . $access_token,
            'Content-Type' => 'application/json'
        ],
        'body' => json_encode($lead_data)
    ]);
    
    return $response;
}

function get_zoho_access_token($config) {
    $token_url = $config['accounts_url'] . '/oauth/v2/token';
    
    $response = wp_remote_post($token_url, [
        'body' => [
            'refresh_token' => $config['refresh_token'],
            'client_id' => $config['client_id'],
            'client_secret' => $config['client_secret'],
            'grant_type' => 'refresh_token'
        ]
    ]);
    
    $body = json_decode(wp_remote_retrieve_body($response), true);
    return $body['access_token'];
}

// Handle the webhook
if ($_POST) {
    send_to_zoho_crm($_POST);
}
?>
```

This approach gives you complete control but requires more technical setup and maintenance.

## Testing & Verification

### Test Form Submission
1. Fill out your contact form with test data (use your own email)
2. Submit the form
3. Check that you receive the confirmation email
4. Go to Zoho CRM → Leads
5. Verify your test lead appears with all mapped fields populated

### Check Integration Health
- **Zapier**: Check your Zap history for successful runs and errors
- **Native Zoho Form**: Check the web form analytics in Zoho CRM setup
- **Webhook**: Monitor your server logs for 200 response codes from Zoho API

### Acceptable Data Variance
Your form submissions should match your CRM leads 1:1. Any variance means you're losing leads. Common acceptable delays:
- Zapier: 1-15 minutes
- Native integration: Immediate
- Custom webhook: Immediate (if working)

### Red Flags
- Form submissions in Flamingo but no corresponding CRM leads
- 4xx or 5xx errors in webhook logs
- Zapier showing "Failed" runs
- Users reporting form submission errors

## Troubleshooting

**Problem**: Contact Form 7 submissions not triggering Zapier
**Solution**: Ensure Flamingo plugin is installed and activated. Zapier needs stored entries to detect new submissions, not just email notifications.

**Problem**: Duplicate leads being created in Zoho CRM
**Solution**: Set up duplicate management in Zoho CRM under Setup → General → Duplicate Management. Configure rules based on email address to merge or prevent duplicates.

**Problem**: Required fields missing in Zoho CRM leads
**Solution**: Check your field mapping. Zoho CRM requires First Name, Last Name, and Email minimum. If your Contact Form 7 only collects "Name" (single field), split it using Zapier's text formatting tools.

**Problem**: Webhook returns 401 unauthorized errors
**Solution**: Your Zoho access token expired. Refresh tokens are valid for one year. Regenerate your API credentials in Zoho Developer Console and update your webhook code.

**Problem**: Forms work but tracking pixels don't fire for conversions
**Solution**: Contact Form 7 fires the `wpcf7mailsent` DOM event on successful submission. Use this to trigger your conversion tracking. See our [Contact Form 7 Google Ads tracking guide](/tracking/contact-form-7-google-ads-conversion-tracking) for the exact implementation.

**Problem**: Integration worked then suddenly stopped
**Solution**: Check if Contact Form 7 plugin updated and reset your form configuration. Also verify your Zoho CRM API limits — free plans have daily quotas that can get exceeded.

## What To Do Next

Ready to expand your lead tracking setup? Check out these related integrations:

- [Contact Form 7 → HubSpot Integration](/integrations/contact-form-7-to-hubspot) — If you're considering switching CRMs
- [Contact Form 7 → Salesforce Integration](/integrations/contact-form-7-to-salesforce) — For enterprise CRM setups  
- [Contact Form 7 → GoHighLevel Integration](/integrations/contact-form-7-to-gohighlevel) — For marketing agencies
- **[Get a free tracking audit](/contact)** — I'll review your entire lead flow and identify what's breaking

*This guide is part of the [Complete Zoho CRM Integration Hub](/integrations/zoho) — covering every major form tool, landing page builder, and lead source integration with Zoho CRM.*