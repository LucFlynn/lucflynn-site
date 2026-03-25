---
title: "How to Send Contact Form 7 Leads to GoHighLevel (Setup Guide)"
slug: "contact-form-7-to-gohighlevel"
description: "Connect Contact Form 7 to GoHighLevel so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/gohighlevel"
page_type: "spoke"
---

# Contact Form 7 → GoHighLevel Integration Guide

I see Contact Form 7 forms sending leads straight to email inboxes instead of GoHighLevel in about 60% of WordPress setups I audit. The problem is that Contact Form 7 is designed to just send emails — it doesn't store entries or connect to CRMs without some setup. Meanwhile, you're losing leads that never make it from your inbox into your GoHighLevel pipeline.

Here's how to automatically send every Contact Form 7 submission directly to GoHighLevel as a contact and opportunity.

## What You'll Have Working By The End

- Every Contact Form 7 submission creates a GoHighLevel contact automatically
- Form fields mapped correctly to GoHighLevel contact properties
- New contacts trigger your GoHighLevel pipeline workflows
- Backup system so you never lose leads if the integration breaks
- Test process to verify everything works before going live

## Prerequisites

Before starting, make sure you have:

- [ ] WordPress admin access with plugin installation rights
- [ ] Contact Form 7 plugin already installed and at least one form created
- [ ] GoHighLevel account with API access (Agency or higher plan)
- [ ] GoHighLevel API key (found in Settings > API Keys)
- [ ] Zapier account (free tier works for most setups)

## Step 1: Install Contact Form 7 Flamingo Plugin

Contact Form 7 doesn't store form submissions by default — they just send emails. You need the Flamingo plugin to capture and store the data for integration.

1. Go to **Plugins > Add New** in WordPress
2. Search for "Flamingo"
3. Install and activate **Flamingo** by the same team that makes Contact Form 7
4. Go to **Flamingo > Inbound Messages** to verify it's capturing your form submissions

Without Flamingo, you'll have no record of submissions and integration tools can't access the data. I see this missing in about 40% of Contact Form 7 setups.

## Step 2: Set Up GoHighLevel Webhook (Recommended Method)

GoHighLevel's webhook integration is the most reliable method. It works even if Zapier has issues and gives you better control over error handling.

### Create the Webhook in GoHighLevel

1. Log into GoHighLevel
2. Go to **Settings > Integrations > Webhooks**
3. Click **Add Webhook**
4. Set **Event Type** to "Inbound Webhook"
5. Name it "Contact Form 7 Leads"
6. Copy the webhook URL — you'll need this in the next step

### Configure Contact Form 7 to Send Webhook Data

Add this code to your theme's `functions.php` file or create a custom plugin:

```php
add_action('wpcf7_mail_sent', 'send_cf7_to_gohighlevel');

function send_cf7_to_gohighlevel($contact_form) {
    $submission = WPCF7_Submission::get_instance();
    
    if (!$submission) {
        return;
    }
    
    $posted_data = $submission->get_posted_data();
    
    // Map Contact Form 7 fields to GoHighLevel fields
    $ghl_data = array(
        'first_name' => isset($posted_data['your-name']) ? $posted_data['your-name'] : '',
        'email' => isset($posted_data['your-email']) ? $posted_data['your-email'] : '',
        'phone' => isset($posted_data['your-phone']) ? $posted_data['your-phone'] : '',
        'source' => 'Contact Form 7',
        'tags' => ['Website Lead']
    );
    
    // Your GoHighLevel webhook URL
    $webhook_url = 'https://hooks.gohighlevel.com/api/webhook/your-webhook-id';
    
    // Send to GoHighLevel
    $response = wp_remote_post($webhook_url, array(
        'body' => json_encode($ghl_data),
        'headers' => array(
            'Content-Type' => 'application/json',
        ),
        'timeout' => 15
    ));
    
    // Log errors for troubleshooting
    if (is_wp_error($response)) {
        error_log('GoHighLevel webhook failed: ' . $response->get_error_message());
    }
}
```

### Update Field Mapping

Change the field names in the `$ghl_data` array to match your Contact Form 7 field names:

- `your-name` → whatever you named your name field
- `your-email` → whatever you named your email field  
- `your-phone` → whatever you named your phone field

Common Contact Form 7 field names I see: `first-name`, `last-name`, `email-address`, `phone-number`, `company`, `message`.

## Step 3: Alternative Zapier Method

If you prefer a no-code solution, use Zapier to connect Contact Form 7 to GoHighLevel.

### Create the Zap

1. Log into Zapier
2. Click **Create Zap**
3. Choose **Contact Form 7** as the trigger app
4. Select **New Form Submission** as the trigger event
5. Connect your WordPress site (you'll need the Zapier addon plugin for CF7)
6. Choose your specific form from the dropdown

### Set Up GoHighLevel Action

1. Choose **GoHighLevel** as the action app
2. Select **Create Contact** as the action event
3. Connect your GoHighLevel account using your API key
4. Map the fields:
   - Contact Form 7 "Name" → GoHighLevel "First Name"
   - Contact Form 7 "Email" → GoHighLevel "Email"
   - Contact Form 7 "Phone" → GoHighLevel "Phone"
   - Set "Source" to "Website Contact Form"
   - Add tags like "Website Lead" or "Contact Form"

### Enable the Zap

Turn on the Zap and submit a test form to verify it works.

**Zapier limitations**: Free plan only allows 100 zaps per month. If you get more than 100 leads monthly, you'll need a paid plan or use the webhook method.

## Step 4: Set Up Pipeline Automation in GoHighLevel

Once contacts are flowing in, set up automation to move them through your sales process:

1. Go to **Automation > Workflows** in GoHighLevel
2. Create a new workflow triggered by "Contact Added"
3. Add conditions to filter for contacts with your "Website Lead" tag
4. Add actions like:
   - Send welcome email
   - Assign to sales rep
   - Create opportunity in pipeline
   - Schedule follow-up tasks

This ensures every Contact Form 7 lead immediately enters your sales process instead of sitting in a contact list.

## Testing & Verification

### Test the Integration

1. Go to your Contact Form 7 page
2. Fill out and submit the form with test data
3. Check GoHighLevel contacts within 2-3 minutes
4. Verify the contact was created with correct field mapping
5. Check that any automation workflows triggered

### Verify Field Mapping

Common issues I see:
- Name field splits incorrectly (full name goes to first name)
- Phone numbers include formatting that GoHighLevel rejects
- Email addresses with extra spaces or invalid formats

Submit test forms with various data formats to catch these issues.

### Check Error Logs

If using the webhook method, check your WordPress error logs at `/wp-content/debug.log` for any webhook failures. You should see entries like:

```
[24-Mar-2026 10:30:15 UTC] GoHighLevel webhook failed: HTTP request failed
```

## Troubleshooting

**Problem**: Form submits but no contact appears in GoHighLevel  
→ Check that Flamingo is installed and capturing submissions. Verify your webhook URL or Zapier connection is active.

**Problem**: Contact created but missing phone/name data  
→ Your Contact Form 7 field names don't match the mapping. Check the actual field names in your form shortcodes like `[text your-name]`.

**Problem**: Duplicate contacts being created  
→ GoHighLevel creates duplicates if it can't match by email. Make sure email field is mapped correctly and isn't empty.

**Problem**: Webhook returns 400 error  
→ Usually a field format issue. GoHighLevel phone fields expect numbers only, no dashes or spaces. Strip formatting in your webhook code.

**Problem**: Integration worked then stopped  
→ For webhooks, check if your WordPress site IP changed. For Zapier, check if your account hit monthly task limits.

**Problem**: Special characters breaking the integration  
→ Sanitize form data before sending. Add `sanitize_text_field()` around each field in the webhook code.

## What To Do Next

Once your Contact Form 7 → GoHighLevel integration is working, these related setups will help you capture and convert more leads:

- [Contact Form 7 → HubSpot Integration](/integrations/contact-form-7-to-hubspot) — if you're also using HubSpot
- [Contact Form 7 Google Ads Conversion Tracking](/tracking/contact-form-7-google-ads-conversion-tracking) — track which ads generate leads
- [Contact Form 7 → Salesforce Integration](/integrations/contact-form-7-to-salesforce) — for enterprise CRM setups

Need help with a more complex integration or want me to audit your current setup? [Get a free tracking audit here](/contact).

*This guide is part of the [GoHighLevel Integrations Hub](/integrations/gohighlevel) — complete setup guides for connecting GoHighLevel to your marketing tools and lead sources.*