---
title: "How to Send Gravity Forms Leads to HubSpot (Setup Guide)"
slug: "gravity-forms-to-hubspot"
description: "Connect Gravity Forms to HubSpot so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/hubspot"
page_type: "spoke"
---

# Gravity Forms → HubSpot Integration Guide

I've set up this exact integration in probably 150+ WordPress sites over the years. The good news? HubSpot actually provides a native Gravity Forms add-on that works reliably. The bad news? Most people either don't know about it or configure the field mapping wrong, leading to incomplete contact records or duplicate entries.

Here's what drives me crazy: I'll audit a site where they're paying for HubSpot, have Gravity Forms collecting leads, but zero connection between the two. Meanwhile, they're manually importing CSV files or worse — just letting leads sit in WordPress with no follow-up.

## What You'll Have Working By The End

- Every Gravity Forms submission automatically creates or updates a HubSpot contact
- Proper field mapping so all form data flows to the right HubSpot properties
- Lead source tracking so you know which forms are converting
- Automated workflows triggered by specific form submissions
- Testing process to verify leads are flowing correctly

## Prerequisites

- [ ] WordPress admin access to install plugins
- [ ] Gravity Forms license (any tier works)
- [ ] HubSpot account (free tier is fine for basic lead capture)
- [ ] HubSpot admin permissions to create integrations
- [ ] Access to your HubSpot API key or ability to connect via OAuth

## Install the Native HubSpot Add-On

The fastest way is using HubSpot's official Gravity Forms add-on. I use this method in about 80% of setups because it's reliable and handles the heavy lifting.

First, install the HubSpot plugin from your WordPress dashboard:

1. Go to **Plugins** → **Add New**
2. Search for "HubSpot All-In-One Marketing"
3. Install and activate the plugin
4. Navigate to **HubSpot** → **Settings** in your WordPress admin

Connect your HubSpot account by clicking **Connect HubSpot Account**. You'll authenticate via OAuth — don't use API keys unless you specifically need them for a custom setup.

Once connected, the plugin automatically adds HubSpot as a feed option in Gravity Forms. Here's where most people mess up the configuration.

## Configure the Gravity Forms Feed

Go to **Forms** → select your form → **Settings** → **HubSpot**.

Click **Add New** to create a feed. Here's the configuration that actually works:

**Feed Name**: Use something descriptive like "Contact Form - Main Site" or "Demo Request Form"

**Contact Properties Mapping**:
- Email: Map to your email field (usually input_2 or input_3)
- First Name: Map to your first name field
- Last Name: Map to your last name field
- Phone: Map to your phone field if you have one
- Company: Map to company field if collecting it

**Important**: Don't leave the email field unmapped. HubSpot requires an email to create a contact, and if this mapping is wrong, the entire submission fails silently.

**Advanced Settings**:
- **Lead Source**: Set this to something specific like "Website Contact Form" or "Product Demo Request"
- **Create Contact**: Set to "Always" unless you specifically want to update existing contacts only
- **Assign to Owner**: Leave blank unless you have specific routing rules

The feed setup should look like this in your form settings:

```
Feed Name: Contact Form Lead Capture
Email: {Email:2}
First Name: {First Name:1}  
Last Name: {Last Name:3}
Phone: {Phone:4}
Lead Source: Website Contact Form
```

Save the feed and you're connected.

## Set Up Zapier Integration (Alternative Method)

If you can't use the native integration or need more complex logic, Zapier works well. I use this when clients need leads to go to multiple systems or have custom field requirements.

**Trigger Setup**:
1. Choose Gravity Forms as your trigger app
2. Select "New Form Submission" as the trigger event
3. Connect your WordPress site (you'll need to install the Zapier add-on for Gravity Forms)
4. Select the specific form you want to connect

**Action Setup**:
1. Choose HubSpot as your action app
2. Select "Create Contact" as the action event
3. Map your Gravity Forms fields to HubSpot contact properties:

```
Email → Email
First Name → First Name
Last Name → Last Name  
Phone → Phone Number
Company → Company Name
Message → Notes (or create a custom property)
```

**Pro tip**: Create a custom HubSpot property for "Lead Source" and map it to a static value like "Contact Form - Zapier". This helps with attribution later.

Test the Zap with a real form submission before turning it on.

## Direct Webhook Integration (For Developers)

When I need maximum control or the client has complex routing logic, I'll build a custom webhook integration. This requires PHP development but gives you complete flexibility.

Add this to your theme's functions.php or a custom plugin:

```php
add_action('gform_after_submission', 'send_to_hubspot', 10, 2);

function send_to_hubspot($entry, $form) {
    
    // Only process form ID 1 (adjust as needed)
    if ($form['id'] != 1) {
        return;
    }
    
    $hubspot_api_key = 'your-hubspot-api-key';
    $portal_id = 'your-portal-id';
    
    // Map Gravity Forms fields to HubSpot properties
    $contact_data = array(
        'properties' => array(
            array(
                'property' => 'email',
                'value' => rgar($entry, '2') // Adjust field ID
            ),
            array(
                'property' => 'firstname', 
                'value' => rgar($entry, '1') // Adjust field ID
            ),
            array(
                'property' => 'lastname',
                'value' => rgar($entry, '3') // Adjust field ID
            ),
            array(
                'property' => 'phone',
                'value' => rgar($entry, '4') // Adjust field ID
            ),
            array(
                'property' => 'lead_source',
                'value' => 'Website Contact Form'
            )
        )
    );
    
    // Send to HubSpot
    $url = "https://api.hubapi.com/contacts/v1/contact/?hapikey=" . $hubspot_api_key;
    
    $response = wp_remote_post($url, array(
        'headers' => array(
            'Content-Type' => 'application/json',
        ),
        'body' => json_encode($contact_data),
        'timeout' => 30
    ));
    
    // Log errors for debugging
    if (is_wp_error($response)) {
        error_log('HubSpot API Error: ' . $response->get_error_message());
    }
}
```

**Important**: Replace the field IDs (the numbers in `rgar($entry, '2')`) with your actual Gravity Forms field IDs. You can find these by editing your form and looking at the field settings.

## Testing & Verification

Here's how I test every integration to make sure it's actually working:

1. **Submit a test form** with a real email address (use your own email for testing)
2. **Check HubSpot contacts** within 2-3 minutes — the contact should appear with all mapped fields populated
3. **Verify lead source attribution** — check that your lead source field shows the correct value
4. **Test duplicate handling** — submit the same email twice and verify HubSpot either updates the existing contact or creates a new one based on your settings

**What working looks like**:
- Contact appears in HubSpot within 5 minutes
- All form fields are mapped to the correct HubSpot properties
- Lead source shows your specified value
- No error messages in WordPress debug log

**Red flags**:
- Contact appears but missing key fields (field mapping issue)
- No contact created at all (authentication or email mapping problem)
- Contacts created but no lead source (attribution problem)
- PHP errors in your WordPress error log

## Troubleshooting

**Contact created but missing fields** → Check your field mapping in the feed settings. The most common issue is mapping to the wrong Gravity Forms field ID. Edit your form and verify the actual field IDs match your configuration.

**No contacts being created at all** → Usually an email field mapping problem. HubSpot requires a valid email to create a contact. Check that your email field is correctly mapped and actually contains an email address when submitted.

**Duplicate contacts being created** → HubSpot's default behavior is to update existing contacts when the email matches. If you're getting duplicates, check your HubSpot duplicate management settings or verify you're not sending slightly different email formats (spaces, capitalization).

**Integration worked then stopped** → API authentication expired. If using the native plugin, try disconnecting and reconnecting your HubSpot account. If using webhooks, verify your API key is still valid.

**Gravity Forms submissions show "Error" status** → Enable WordPress debug logging and check your error log. Usually indicates a PHP error in custom webhook code or a network timeout reaching HubSpot's API.

**Leads showing up hours later** → Network or server performance issue. The native integration should be near real-time. Check your hosting provider's external API restrictions or consider switching to Zapier for more reliable delivery.

## What To Do Next

Now that your leads are flowing into HubSpot, consider setting up [Gravity Forms conversion tracking for Google Ads](/tracking/gravity-forms-google-ads-conversion-tracking) to measure which campaigns are driving form submissions.

You might also want to explore other CRM integrations: [Gravity Forms to Salesforce](/integrations/gravity-forms-to-salesforce), [Gravity Forms to GoHighLevel](/integrations/gravity-forms-to-gohighlevel), or [Gravity Forms to ActiveCampaign](/integrations/gravity-forms-to-activecampaign).

If your current setup isn't capturing leads properly or you're missing attribution data, I can audit your entire tracking infrastructure. [Get a free tracking audit here](/contact) — I'll identify exactly what's broken and how to fix it.

*This guide is part of the [HubSpot Integrations Hub](/integrations/hubspot) — complete setup guides for connecting HubSpot to every major form, ecommerce, and tracking tool.*