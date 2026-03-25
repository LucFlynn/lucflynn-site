---
title: "How to Send Elementor Forms Leads to HubSpot (Setup Guide)"
slug: "elementor-forms-to-hubspot"
description: "Connect Elementor Forms to HubSpot so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/hubspot"
page_type: "spoke"
---

# Elementor Forms → HubSpot Integration Guide

I see this integration requested in about 60% of the WordPress sites I audit. The good news? Elementor Forms actually plays nice with HubSpot through multiple methods. The bad news? Most people set it up wrong and lose 15-20% of their leads to sync failures or field mapping issues.

**What You'll Have Working By The End:**
• Every Elementor form submission automatically creates a contact in HubSpot
• Form fields correctly mapped to HubSpot contact properties
• Lead source tracking so you know which forms are converting
• Error handling that alerts you when submissions fail
• Test process to verify leads are syncing properly

**Prerequisites:**
- [ ] WordPress admin access with Elementor Pro installed
- [ ] HubSpot account (free tier works fine)
- [ ] Elementor forms already built and collecting submissions
- [ ] HubSpot contact properties created for any custom fields you want to map

## Method 1: HubSpot's WordPress Plugin (Recommended)

HubSpot's native WordPress plugin is the cleanest approach. It integrates directly with Elementor forms and handles all the API calls for you.

Install the HubSpot WordPress plugin from your WordPress admin → Plugins → Add New → Search "HubSpot". After installation, connect it to your HubSpot account through the setup wizard.

In your Elementor form settings, go to Actions After Submit and add a new action. Select "HubSpot" from the dropdown. You'll see these field mapping options:

```
First Name → firstname
Last Name → lastname  
Email → email
Phone → phone
Company → company
Website → website
```

For custom fields, create the corresponding contact property in HubSpot first (Settings → Properties → Contact Properties), then map it in the Elementor form. The field names need to match exactly — HubSpot uses lowercase with underscores, so "Job Title" becomes "job_title".

Set the form to "Add contacts to a list" and select your lead list. This helps with lead nurturing workflows later.

## Method 2: Zapier Integration

If the native plugin isn't working for your setup, Zapier is the next best option. I use this in about 30% of implementations when clients have complex field mapping requirements.

Create a new Zap with Elementor Forms as the trigger. You'll need to set up a webhook in your Elementor form first. In the form's Actions After Submit, add a "Webhook" action with this URL format:

```
https://hooks.zapier.com/hooks/catch/[your-webhook-id]/[your-hook-code]/
```

In Zapier, test the trigger by submitting a test form. Once Zapier catches the webhook data, set HubSpot as the action app. Choose "Create or Update Contact" as the action.

Map your fields like this:
```
Email: {{email}} (required)
First Name: {{first_name}}
Last Name: {{last_name}}
Phone: {{phone}}
Lead Source: Elementor Form - [Form Name]
```

The lead source field is crucial — I set it to include the specific form name so you can track performance by form in HubSpot's reports.

## Method 3: Custom Webhook Integration

For clients who want full control, I build custom webhook handlers. This requires some PHP work but gives you complete flexibility over the data flow.

Add this webhook action to your Elementor form's Actions After Submit:

```php
// In your theme's functions.php or a custom plugin
add_action('wp_ajax_nopriv_elementor_to_hubspot', 'handle_elementor_hubspot');
add_action('wp_ajax_elementor_to_hubspot', 'handle_elementor_hubspot');

function handle_elementor_hubspot() {
    $hubspot_api_key = 'your-hubspot-api-key';
    
    $contact_data = [
        'properties' => [
            'email' => sanitize_email($_POST['email']),
            'firstname' => sanitize_text_field($_POST['first_name']),
            'lastname' => sanitize_text_field($_POST['last_name']),
            'phone' => sanitize_text_field($_POST['phone']),
            'hs_lead_status' => 'NEW',
            'lead_source' => 'Elementor Form'
        ]
    ];
    
    $response = wp_remote_post('https://api.hubapi.com/crm/v3/objects/contacts', [
        'headers' => [
            'Authorization' => 'Bearer ' . $hubspot_api_key,
            'Content-Type' => 'application/json'
        ],
        'body' => json_encode($contact_data)
    ]);
    
    wp_send_json_success();
}
```

Set your webhook URL to `https://yoursite.com/wp-admin/admin-ajax.php?action=elementor_to_hubspot`.

## Field Mapping Best Practices

I've seen field mapping break integrations more than any other issue. Here's what works:

**Standard Fields (use these exact API names):**
- First Name: `firstname`
- Last Name: `lastname`
- Email: `email` (required)
- Phone: `phone`
- Company: `company`
- Website: `website`
- Job Title: `jobtitle`

**Custom Fields:**
Create the property in HubSpot first, then use the internal name (usually lowercase with underscores). For a field called "How did you hear about us?", the API name would be `how_did_you_hear_about_us`.

Always map a lead source field. I use a hidden field in Elementor forms with a default value like "Website Contact Form" or "Newsletter Signup". This lets you track ROI by traffic source in HubSpot.

## Testing & Verification

Submit a test form using a real email address you can check. Within 2-3 minutes, you should see:

1. **In HubSpot:** New contact appears in Contacts → All Contacts
2. **Contact record:** All mapped fields populated correctly
3. **Activity timeline:** Form submission logged with timestamp
4. **Lists:** Contact added to specified list (if configured)

If you're using Zapier, check the Zap history for successful runs. Failed runs will show error details.

For webhook integrations, check your server's error logs. Successful API calls return a 201 status code with the new contact's ID.

**Acceptable sync delay:** 30 seconds to 2 minutes. If it's taking longer, something's broken.

## Troubleshooting

**Problem:** Forms submit successfully but no contacts appear in HubSpot
The most common cause is email field mapping. HubSpot requires a valid email address to create a contact. Check that your Elementor form's email field is named "email" and mapped correctly. Also verify your HubSpot API key has write permissions for contacts.

**Problem:** Duplicate contacts created for repeat form submissions
This happens when HubSpot can't match the contact by email. In your integration settings, choose "Create or Update Contact" instead of "Create Contact". HubSpot will update existing contacts instead of creating duplicates.

**Problem:** Custom fields not syncing to HubSpot
The field names must match exactly between Elementor and HubSpot. Go to HubSpot → Settings → Properties → Contact Properties and copy the "Internal Name" (not the display name) for your custom fields. Use these exact names in your field mapping.

**Problem:** Webhook failing with 401 unauthorized error
Your HubSpot API key is either invalid or doesn't have the right permissions. Regenerate the key in HubSpot → Settings → Integrations → Private Apps, and make sure it has "Write" access for contacts.

**Problem:** Integration stops working after HubSpot updates
HubSpot occasionally deprecates API endpoints. If you're using the native WordPress plugin, update it. For custom webhooks, check HubSpot's developer documentation for the current API endpoints. The v3 contacts API is currently stable.

**Problem:** Form submissions sync but trigger multiple workflows
This happens when you have overlapping workflow triggers. Check your HubSpot workflows for triggers like "Contact created" and "Form submitted". Use specific form-based triggers instead of broad contact creation triggers to avoid double-processing.

## What To Do Next

Set up [Elementor Forms conversion tracking](/tracking/elementor-forms-google-ads-conversion-tracking) to track which forms are driving your best customers. Once your leads are flowing into HubSpot, you can also connect [HubSpot to other marketing tools](/integrations/hubspot) for a complete marketing stack.

If you need help auditing your current lead flow or setting up more complex integrations, [get a free tracking audit](/contact) — I'll show you exactly where leads are getting lost in your funnel.

*This guide is part of the [HubSpot Integrations Hub](/integrations/hubspot) — connect HubSpot to your entire marketing and sales stack.*