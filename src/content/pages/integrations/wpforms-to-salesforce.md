---
title: "How to Send WPForms Leads to Salesforce (Setup Guide)"
slug: "wpforms-to-salesforce"
description: "Connect WPForms to Salesforce so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/salesforce"
page_type: "spoke"
---

# WPForms → Salesforce Integration Guide

Most WordPress sites I audit have WPForms collecting leads that just sit in the admin dashboard. The sales team is checking WordPress instead of working in Salesforce where their pipeline lives. This creates gaps where leads get missed, delayed, or double-entered.

I see this exact scenario in about 35% of WordPress-based businesses I work with. The disconnect between marketing (WPForms) and sales (Salesforce) kills momentum on warm leads.

## What You'll Have Working By The End

- Every WPForms submission automatically creates a Salesforce Lead
- Form fields properly mapped to standard Salesforce fields (First Name, Last Name, Email, Company, Phone)
- Custom fields flowing from WPForms to Salesforce custom objects
- Real-time sync with error handling when Salesforce is down
- Test submissions verified in your Salesforce org

## Prerequisites

- [ ] WPForms Pro license (native Salesforce addon requires Pro)
- [ ] WordPress admin access to install plugins/addons
- [ ] Salesforce admin access or user with API permissions
- [ ] Access to your Salesforce API credentials (if using webhook method)
- [ ] Zapier account (if using Zapier method)

## Method 1: WPForms Salesforce Addon (Recommended)

The WPForms Salesforce addon handles the heavy lifting. This is the cleanest approach if you have WPForms Pro.

Install the addon from your WPForms account downloads. Upload and activate it in WordPress.

Go to **WPForms → Settings → Integrations → Salesforce**. You'll need:
- **Username**: Your Salesforce login email
- **Password**: Your Salesforce password
- **Security Token**: Get this from Salesforce Setup → My Personal Information → Reset Security Token

The security token gets appended to your password in the connection string. If your password is "mypass123" and token is "ABC123", enter "mypass123ABC123" in the password field.

Click **Connect to Salesforce** and test the connection.

Now edit your WPForms form. Go to **Settings → Marketing → Salesforce**. Enable the integration and map your fields:

**Required Field Mapping:**
- **First Name** → `{field_id="1"}` (your name field)
- **Last Name** → `{field_id="1"}` (same name field if single field, or separate last name field)
- **Email** → `{field_id="2"}` (your email field)
- **Company** → `{field_id="3"}` (company field)

**Common Optional Mappings:**
- **Phone** → `{field_id="4"}`
- **Website** → `{field_id="5"}`
- **Lead Source** → Set to "Website Form" or dynamic value
- **Description** → `{field_id="6"}` (message/comments field)

Set **Lead Status** to "New" or whatever status your sales team expects for form leads.

The addon creates Salesforce **Lead** objects by default. If you need **Contact** objects instead, you'll need a custom solution.

## Method 2: Zapier Integration

When the native addon won't work (WPForms Lite, need Contact objects, complex field mapping), Zapier is the next best option.

Create a Zapier account and set up a new Zap with **WPForms** as the trigger and **Salesforce** as the action.

For the WPForms trigger, choose **New Form Entry**. Connect your WordPress site using your site URL and the API key from **WPForms → Settings → General → API**.

Select your specific form from the dropdown. Zapier will pull in all your form fields.

For the Salesforce action, choose **Create Lead** or **Create Contact** depending on your needs. Connect your Salesforce account using OAuth.

**Field Mapping in Zapier:**
- **First Name** → WPForms First Name field
- **Last Name** → WPForms Last Name field  
- **Email** → WPForms Email field
- **Company** → WPForms Company field
- **Phone** → WPForms Phone field
- **Lead Source** → Set to "WPForms" or custom value
- **Description** → WPForms Message field

For custom fields, you'll need the Salesforce API name (like `Custom_Field__c`). Find these in Salesforce Setup → Object Manager → Lead/Contact → Fields & Relationships.

**Which should you use?** Zapier if you need more flexibility with field mapping, conditional logic, or want to create Contact objects instead of Leads. The native addon if you just need basic Lead creation and have WPForms Pro.

## Method 3: Webhook + API Setup

This method gives you full control but requires technical setup. Use this when you need complex data transformation or the other methods don't meet your requirements.

First, set up the webhook endpoint. You'll need a server script that can receive POST data from WPForms and send it to Salesforce's REST API.

Here's a basic PHP webhook receiver:

```php
<?php
// webhook-receiver.php
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    exit('Method not allowed');
}

$form_data = json_decode(file_get_contents('php://input'), true);

// Extract WPForms data
$first_name = $form_data['fields'][1]['value'] ?? '';
$last_name = $form_data['fields'][1]['value_raw'] ?? ''; // For full name fields
$email = $form_data['fields'][2]['value'] ?? '';
$company = $form_data['fields'][3]['value'] ?? '';
$phone = $form_data['fields'][4]['value'] ?? '';

// Salesforce API call
$salesforce_data = [
    'FirstName' => $first_name,
    'LastName' => $last_name,
    'Email' => $email,
    'Company' => $company,
    'Phone' => $phone,
    'LeadSource' => 'Website'
];

// Send to Salesforce (you'll need OAuth token handling)
$result = send_to_salesforce($salesforce_data);

if ($result) {
    http_response_code(200);
    echo 'Success';
} else {
    http_response_code(500);
    echo 'Failed to create Salesforce lead';
}
?>
```

In WPForms, go to **Settings → Notifications** and add a new notification. Choose **Webhook** as the type and enter your webhook URL.

The webhook payload will include all form field data in JSON format. Field IDs correspond to your form builder (field 1 = first field, etc.).

## Testing & Verification

Submit a test form entry with recognizable data ("Test Lead John Doe", email "test@example.com").

**Verify in WPForms:**
Check **WPForms → Entries** to confirm the submission was recorded.

**Verify in Salesforce:**
Go to **Leads** tab (or **Contacts** if using Contact objects) and search for your test entry. It should appear within 1-2 minutes.

Check that all mapped fields populated correctly:
- Name fields split properly (if using single name field)
- Email address is clean
- Phone number formatted correctly
- Custom fields have the right values

**Check Activity Timeline:**
The lead should show creation via "API" or "Web-to-Lead" in the activity history.

**Acceptable sync time:** 30 seconds to 2 minutes depending on method. Native addon is fastest, Zapier adds 1-2 minutes, webhooks depend on your server response time.

If leads appear after 5+ minutes, something's wrong with the integration.

## Troubleshooting

**Problem:** Form submits but no Salesforce lead appears
Check WPForms entry logs for error messages. Common causes: invalid Salesforce credentials, required field missing, or API limits exceeded. Verify your Salesforce user has Lead creation permissions.

**Problem:** Duplicate leads created for same person  
Salesforce has duplicate rules that may block or merge leads. Check **Setup → Duplicate Management** to see active rules. You may need to adjust the rules or use Contact objects instead of Leads if your org has strict duplicate prevention.

**Problem:** Name field not splitting correctly into First/Last Name
If using a single "Name" field in WPForms, the integration may not split "John Doe" into First="John", Last="Doe". Either use separate First Name/Last Name fields in WPForms, or handle the split in your webhook code.

**Problem:** Phone numbers formatted incorrectly  
Salesforce expects clean phone formats. WPForms may pass "(555) 123-4567" but Salesforce wants "5551234567" or "+15551234567". Add phone formatting in your integration or use Salesforce's phone field validation rules.

**Problem:** Custom fields not syncing
Verify the Salesforce API names in your field mapping. Custom fields end with `__c` (like `Lead_Score__c`). Check that your Salesforce user has field-level security access to write these fields.

**Problem:** "INSUFFICIENT_ACCESS" errors from Salesforce  
Your connected Salesforce user doesn't have permissions to create Leads or write to specific fields. Have your Salesforce admin check the user's Profile and Permission Sets. API integrations need "API Enabled" permission plus object-level create/edit access.

## What To Do Next

Once leads are flowing into Salesforce, consider setting up [WPForms Google Ads conversion tracking](/tracking/wpforms-google-ads-conversion-tracking) to measure which campaigns drive the best leads.

You might also want to connect other forms to Salesforce: [WPForms to HubSpot](/integrations/wpforms-to-hubspot) for marketing automation, [WPForms to GoHighLevel](/integrations/wpforms-to-gohighlevel) for agency workflows, or [WPForms to ActiveCampaign](/integrations/wpforms-to-activecampaign) for email nurturing.

Need help auditing your current form-to-CRM setup? I offer [free tracking audits](/contact) where I'll identify gaps in your lead flow and recommend the best integration approach for your specific WordPress + Salesforce setup.

*This guide is part of the [Salesforce Integrations Hub](/integrations/salesforce) — connecting your favorite tools to Salesforce CRM for better lead management and sales pipeline tracking.*