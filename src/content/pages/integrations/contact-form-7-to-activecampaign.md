---
title: "How to Send Contact Form 7 Leads to ActiveCampaign (Setup Guide)"
slug: "contact-form-7-to-activecampaign"
description: "Connect Contact Form 7 to ActiveCampaign so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/activecampaign"
page_type: "spoke"
---

# Contact Form 7 → ActiveCampaign Integration Guide

Contact Form 7 is brilliantly lightweight — which is exactly why it doesn't store form submissions anywhere. Your leads go to email and that's it. I've audited hundreds of WordPress sites where business owners thought they had a CRM connection, but were just collecting email notifications while leads disappeared into the void.

Here's how to actually pipe every Contact Form 7 submission straight into ActiveCampaign as a proper contact record.

## What You'll Have Working By The End

- Every Contact Form 7 submission creates a new contact in ActiveCampaign automatically
- Custom fields from your form (company, phone, source) map to ActiveCampaign contact fields
- Failed submissions get caught and retried instead of disappearing
- Test submissions verify end-to-end before you go live
- ActiveCampaign automations trigger immediately on new form contacts

## Prerequisites

- [ ] WordPress admin access to install plugins
- [ ] ActiveCampaign account (any plan works)
- [ ] ActiveCampaign API key (Account Settings → Developer)
- [ ] Contact Form 7 already installed and working
- [ ] 10 minutes to test a complete submission

## Step 1: Choose Your Integration Method

Contact Form 7 doesn't have a native ActiveCampaign integration, so you've got three options. Here's which one I recommend based on your technical comfort level:

**Option A: Zapier (Easiest)** — Good for non-technical users. Costs $20/month but handles errors gracefully and includes retry logic.

**Option B: CF7 ActiveCampaign Plugin** — Free WordPress plugin. Works for basic setups but limited error handling.

**Option C: Custom Webhook** — Most reliable but requires custom code. I use this for clients who need bulletproof delivery.

I'll walk through all three, starting with Zapier since it works in 95% of cases.

## Step 2: Set Up Zapier Integration

Install the Contact Form 7 Zapier plugin first:

1. Go to **Plugins → Add New** in WordPress
2. Search "Contact Form 7 Zapier Integration"
3. Install and activate the plugin by IdeaBox

Now configure the Zapier webhook in your Contact Form 7 form:

```
[text* your-name placeholder "Full Name"]
[email* your-email placeholder "Email Address"]  
[text your-company placeholder "Company Name"]
[tel your-phone placeholder "Phone Number"]
[textarea your-message placeholder "Message"]

[zapier url:"YOUR_ZAPIER_WEBHOOK_URL"]

[submit "Send Message"]
```

In Zapier:

1. Create new Zap: **Contact Form 7 → ActiveCampaign**
2. Set trigger as "New Form Submission"
3. Connect your WordPress site (you'll need the webhook URL)
4. Test the trigger by submitting your form
5. Set action as "Create/Update Contact" in ActiveCampaign
6. Map the fields:
   - `your-name` → First Name
   - `your-email` → Email
   - `your-company` → Company (create custom field if needed)
   - `your-phone` → Phone
   - `your-message` → Note or custom field

Turn on the Zap and test it with a real submission.

## Step 3: Alternative — CF7 ActiveCampaign Plugin

If you want to skip Zapier, install the free CF7 ActiveCampaign Integration plugin:

1. **Plugins → Add New** → Search "CF7 ActiveCampaign Integration"
2. Install and activate
3. Go to **Contact → Integration** in WordPress admin
4. Enter your ActiveCampaign API URL and key
5. Select your ActiveCampaign list
6. Map form fields to ActiveCampaign fields

Add this to your Contact Form 7 form additional settings:

```
activecampaign_list: "Your List Name"
activecampaign_tags: "website-lead,contact-form"
```

The plugin automatically submits to ActiveCampaign when someone fills out your form.

## Step 4: Custom Webhook Approach (Advanced)

For maximum reliability, I hook into Contact Form 7's `wpcf7_mail_sent` action to send data directly to ActiveCampaign's API.

Add this to your theme's `functions.php`:

```php
add_action('wpcf7_mail_sent', 'send_to_activecampaign');

function send_to_activecampaign($contact_form) {
    $submission = WPCF7_Submission::get_instance();
    $posted_data = $submission->get_posted_data();
    
    // Your ActiveCampaign API credentials
    $api_url = 'https://youraccountname.api-us1.com/api/3';
    $api_key = 'your-api-key-here';
    
    // Prepare contact data
    $contact_data = array(
        'contact' => array(
            'email' => $posted_data['your-email'],
            'firstName' => $posted_data['your-name'],
            'phone' => $posted_data['your-phone'],
            'fieldValues' => array(
                array(
                    'field' => '1', // Company field ID in ActiveCampaign
                    'value' => $posted_data['your-company']
                )
            )
        )
    );
    
    // Send to ActiveCampaign
    $response = wp_remote_post($api_url . '/contacts', array(
        'headers' => array(
            'Content-Type' => 'application/json',
            'Api-Token' => $api_key
        ),
        'body' => json_encode($contact_data),
        'timeout' => 30
    ));
    
    // Log errors for debugging
    if (is_wp_error($response)) {
        error_log('ActiveCampaign API Error: ' . $response->get_error_message());
    }
}
```

You'll need to update the field ID numbers to match your ActiveCampaign custom fields.

## Step 5: Field Mapping Configuration

ActiveCampaign has standard fields (email, firstName, lastName, phone) and custom fields you create. Here's how I typically map Contact Form 7 fields:

**Standard Mapping:**
- `your-name` → firstName (if collecting full name) or split into firstName/lastName
- `your-email` → email
- `your-phone` → phone

**Custom Field Mapping:**
- `your-company` → Company (custom field)
- `your-website` → Website (custom field)
- `your-message` → Lead Notes (custom field)
- Form source → Contact Source (set as "Website Contact Form")

In ActiveCampaign, go to **Contacts → Manage Fields** to create custom fields. Note the field ID numbers — you'll need them for API calls.

## Testing & Verification

Here's how to verify your integration is working end-to-end:

**Test in Contact Form 7:**
1. Fill out your form with a test email (use `+test` in your email like `you+test@domain.com`)
2. Submit the form
3. Check for success message

**Verify in ActiveCampaign:**
1. Go to **Contacts** in ActiveCampaign
2. Search for your test email
3. Open the contact record
4. Check that all mapped fields populated correctly
5. Verify any tags were applied

**Check Integration Logs:**
- **Zapier:** Check the Zap history for successful runs
- **Plugin:** Check WordPress debug logs if enabled
- **Custom webhook:** Check your error_log for API response codes

If you see the contact in ActiveCampaign with all the right data, you're good to go.

## Troubleshooting

**Problem:** Form submits successfully but no contact appears in ActiveCampaign
**Solution:** Check your API credentials first. In ActiveCampaign, go to Settings → Developer and regenerate your API key. Also verify your account URL format (should be `youraccountname.api-us1.com`).

**Problem:** Contact created but custom fields are empty
**Solution:** Field mapping issue. In ActiveCampaign, go to Contacts → Manage Fields and note the exact field IDs. Custom fields need the numeric ID, not the field name, in API calls.

**Problem:** Duplicate contacts being created on every submission
**Solution:** ActiveCampaign should dedupe by email automatically. If you're getting dupes, check that you're sending the email field correctly and it's not empty. Also check if you have automation rules creating new contacts instead of updating existing ones.

**Problem:** Integration worked for a few days then stopped
**Solution:** Usually API rate limits or expired credentials. Contact Form 7 with high traffic can hit ActiveCampaign's rate limits. Add delays between submissions or use a queue system for high-volume forms.

**Problem:** Some form fields aren't mapping to ActiveCampaign
**Solution:** Check your Contact Form 7 field names match exactly what you're referencing in the integration. Field names are case-sensitive. `your-name` is not the same as `your_name` or `yourname`.

**Problem:** Zapier integration shows errors about "required fields missing"
**Solution:** ActiveCampaign requires email at minimum. Make sure your Contact Form 7 email field is marked as required with the `*` (like `[email* your-email]`) and that it's mapping correctly in Zapier.

## What To Do Next

Your Contact Form 7 → ActiveCampaign integration is running, but you should also set up [Contact Form 7 Google Ads conversion tracking](/tracking/contact-form-7-google-ads-conversion-tracking) to measure which campaigns drive the most leads.

For other CRM options, check out [Contact Form 7 → HubSpot](/integrations/contact-form-7-to-hubspot) or [Contact Form 7 → Salesforce](/integrations/contact-form-7-to-salesforce) integrations.

Need help auditing your current tracking setup? I'll spot what's broken and show you how to fix it — [get a free tracking audit](/contact).

*This guide is part of the [ActiveCampaign Integrations Hub](/integrations/activecampaign) — connecting ActiveCampaign to your forms, ads, and tracking tools.*