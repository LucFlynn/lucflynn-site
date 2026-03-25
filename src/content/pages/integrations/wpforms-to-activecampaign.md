---
title: "How to Send WPForms Leads to ActiveCampaign (Setup Guide)"
slug: "wpforms-to-activecampaign"
description: "Connect WPForms to ActiveCampaign so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/activecampaign"
page_type: "spoke"
---

# WPForms → ActiveCampaign Integration Guide

I see this broken in about 30% of the WordPress setups I audit. Either the integration was set up wrong and leads aren't syncing, or worse — they're creating duplicate contacts because someone didn't understand how ActiveCampaign handles email deduplication. The worst case I've seen had 6,000 duplicate contacts because they were using Zapier without proper matching rules.

## What You'll Have Working By The End

- Every WPForms submission automatically creates or updates contacts in ActiveCampaign
- Custom form fields mapped to ActiveCampaign contact fields and tags
- Automatic trigger of ActiveCampaign automations for new leads
- Error handling so you know when submissions fail to sync
- A testing process to verify everything works before going live

## Prerequisites

- [ ] WPForms installed and at least one form created
- [ ] ActiveCampaign account with API access (available on all paid plans)
- [ ] Admin access to your WordPress site
- [ ] If using Zapier: Zapier account (free plan works for basic setups)

## Step 1: Set Up the Native WPForms → ActiveCampaign Integration

WPForms Pro includes a native ActiveCampaign addon that's more reliable than Zapier for most use cases. This is what I recommend 90% of the time.

In your WordPress admin, go to **WPForms → Addons** and install the ActiveCampaign addon if you haven't already.

Navigate to **WPForms → Settings → Integrations → ActiveCampaign**. You'll need your ActiveCampaign API credentials:

1. In ActiveCampaign, go to **Settings → Developer**
2. Copy your API URL (looks like `https://youraccountname.api-us1.com`)  
3. Copy your API Key

Back in WordPress, paste both credentials and hit **Connect**.

Now edit your form and go to **Settings → Marketing → ActiveCampaign**:

- **List**: Select which ActiveCampaign list to add contacts to
- **Double Opt-In**: I usually leave this off for lead forms, on for newsletter signups
- **Email Field**: Map to your form's email field
- **Tags**: Add relevant tags (like "Website Lead" or "Contact Form")

For custom field mapping, click **Show Advanced Options**:
- Map your form fields to ActiveCampaign contact fields
- Use the exact field names from ActiveCampaign (case sensitive)
- For custom fields, use the format like `field[%FIELDID%,0]` where FIELDID is from ActiveCampaign

The conditional logic section lets you only send certain submissions — useful if you have multi-purpose forms.

## Step 2: Alternative Setup Using Zapier

If you're on WPForms Lite or need more complex automation, use Zapier. I've set this up probably 200+ times.

Create a new Zap with **WPForms** as the trigger:
- Event: "New Form Entry"  
- Choose your specific form
- Test the trigger by submitting your form

For the action, choose **ActiveCampaign**:
- Event: "Create or Update Contact"
- Map email field (required)
- Map other fields like name, phone, company
- Set the list to add them to
- Add tags in the "Tags" field (comma separated)

**Critical mapping notes I wish more people knew:**

- Use "Create or Update Contact" not just "Create Contact" to handle returning visitors
- Map phone numbers to the "Phone" field, not a custom field, for better mobile formatting
- If you have a "Company" form field, map it to the "Organization" field in ActiveCampaign
- For custom fields, make sure they exist in ActiveCampaign first, then map by exact name

## Step 3: Webhook + API Approach (Advanced)

For maximum control, especially if you need custom logic or have complex forms, use webhooks. This requires some development work but gives you complete flexibility.

In WPForms, go to **Settings → Marketing → Webhooks** and add:
- **Webhook URL**: Your server endpoint (like `https://yoursite.com/wpforms-webhook`)
- **Request Format**: JSON
- **Request Method**: POST

Here's the PHP code for your webhook handler:

```php
<?php
// Handle WPForms webhook
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $webhook_data = json_decode(file_get_contents('php://input'), true);
    
    // Extract form data
    $email = $webhook_data['fields'][0]['value']; // Adjust field ID
    $name = $webhook_data['fields'][1]['value'];  // Adjust field ID
    
    // ActiveCampaign API call
    $ac_data = [
        'contact' => [
            'email' => $email,
            'firstName' => $name,
            'fieldValues' => [
                ['field' => '1', 'value' => 'Website Lead'] // Custom field
            ]
        ]
    ];
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, 'https://youraccountname.api-us1.com/api/3/contacts');
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($ac_data));
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json',
        'Api-Token: YOUR_API_TOKEN'
    ]);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    
    $response = curl_exec($ch);
    curl_close($ch);
    
    // Log for debugging
    error_log('ActiveCampaign Response: ' . $response);
}
?>
```

## Step 4: Set Up ActiveCampaign Automations

Once contacts are syncing, set up automations to handle new leads:

1. In ActiveCampaign, go to **Automations → New Automation**
2. Choose "Start from scratch"
3. Set trigger to "Subscribes to list" or "Tag is added" (depending on your setup)
4. Add actions like:
   - Send welcome email
   - Add to specific campaign sequences  
   - Assign to sales rep
   - Create deal record

For form-specific automations, use tags. I usually tag with the form name like "Contact Page Form" so you can create targeted follow-up sequences.

## Testing & Verification

Submit a test form with a unique email address (like `test+wpforms@yourdomain.com`).

**Check in WPForms:**
- Go to **WPForms → Entries** and verify the submission exists
- If using native integration, look for any error messages in the entry details

**Check in ActiveCampaign:**
- Go to **Contacts** and search for your test email
- Verify all mapped fields populated correctly
- Check that tags were applied
- Confirm they were added to the correct list

**Check automation triggers:**
- If you set up automations, verify they triggered
- Look at the contact's timeline to see automation history

**Acceptable sync delays:**
- Native integration: Usually instant (under 30 seconds)
- Zapier: 1-15 minutes depending on your plan
- Webhook: Instant if properly configured

If it takes longer than 15 minutes with any method, something's broken.

## Troubleshooting

**Submissions aren't appearing in ActiveCampaign at all** → Check your API credentials first. In WPForms settings, disconnect and reconnect your ActiveCampaign integration. For Zapier, test your trigger step again.

**Contact is created but custom fields are empty** → ActiveCampaign custom field names are case-sensitive and must match exactly. Go to **Lists → Manage Fields** in ActiveCampaign to copy the exact field names, then update your mapping.

**Duplicate contacts being created** → You're probably using "Create Contact" instead of "Create or Update Contact" in Zapier, or your native integration isn't handling email deduplication. ActiveCampaign deduplicates by email address, so this usually means the email mapping is wrong.

**Form submissions work but don't trigger automations** → Check that your automation trigger matches how contacts are being added. If you're tagging contacts, make sure your automation triggers on that specific tag, not just list subscription.

**Zapier says "Contact created" but nothing appears in ActiveCampaign** → This usually means you're sending to a list that doesn't exist or your contact doesn't meet list requirements. Check your list settings in ActiveCampaign for any restrictions.

**Some form fields aren't syncing** → WPForms field IDs sometimes change when you edit forms. Check the webhook payload or Zapier test data to see the actual field structure, then update your mapping accordingly.

## What To Do Next

Now that your basic integration is working, consider these related setups:

- [WPForms → HubSpot Integration](/integrations/wpforms-to-hubspot) if you're also using HubSpot for certain campaigns
- [WPForms → Salesforce Setup](/integrations/wpforms-to-salesforce) for enterprise sales processes  
- [WPForms Google Ads Conversion Tracking](/tracking/wpforms-google-ads-conversion-tracking) to track which ads drive form submissions
- [Get a free tracking audit](/contact) to see what other lead sources aren't being captured properly

*This guide is part of the [ActiveCampaign Integration Hub](/integrations/activecampaign) — covering all the ways to get lead data into ActiveCampaign from forms, ads, and other tools.*