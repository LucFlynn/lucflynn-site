---
title: "How to Send Contact Form 7 Leads to Mailchimp (Setup Guide)"
slug: "contact-form-7-to-mailchimp"
description: "Connect Contact Form 7 to Mailchimp so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/mailchimp"
page_type: "spoke"
---

# Contact Form 7 → Mailchimp Integration Guide

I see this integration break all the time because people set it up thinking Contact Form 7 plays nicely with third-party services out of the box. It doesn't. CF7 is lightweight by design — it captures form data and emails it to you, then forgets it ever existed. Getting those leads into Mailchimp requires bridging that gap properly.

The main issue I run into is people installing random plugins that claim to connect these two, then wondering why 30% of their form submissions never make it to their email list. Or worse, they're manually copying emails from their inbox into Mailchimp like it's 2015.

## What You'll Have Working By The End

- Contact Form 7 submissions automatically creating Mailchimp contacts
- Proper field mapping so first name, last name, and custom data flows correctly
- Tag assignment to identify which form the lead came from
- Error handling so you know when submissions fail to sync
- Testing workflow to verify the integration works before going live

## Prerequisites

- [ ] WordPress admin access to install plugins
- [ ] Mailchimp account with at least one audience created
- [ ] Mailchimp API key (Account → Profile → Extras → API keys)
- [ ] Contact Form 7 plugin installed and at least one form created
- [ ] Basic understanding of WordPress plugin installation

## Step 1: Choose Your Integration Method

There are three approaches that actually work. I'll walk through them in order of reliability.

**Method 1: CF7 Mailchimp Extension (Recommended)**
This is a dedicated plugin that hooks into Contact Form 7's native submission process. Most reliable because it doesn't depend on external services.

**Method 2: Zapier Integration**
Good if you're already using Zapier for other automations. Adds a potential point of failure but gives you more flexibility for complex workflows.

**Method 3: Custom Webhook + API**
For developers who want full control. More work to set up but completely customizable.

For most people, I recommend Method 1 unless you specifically need Zapier's advanced features.

## Step 2: Install and Configure CF7 Mailchimp Extension

Install the "CF7 Mailchimp Extension" plugin from the WordPress repository. After activation, you'll see a "Mailchimp" tab in your Contact Form 7 form editor.

Go to any Contact Form 7 form and click the "Mailchimp" tab. Here's the configuration:

**API Key**: Paste your Mailchimp API key
**Audience**: Select the Mailchimp list where contacts should be added
**Double Opt-in**: I recommend leaving this unchecked for lead generation forms (people expect immediate access to your content)
**Update Existing**: Check this to update contact info if email already exists
**Tags**: Add a tag like "website-contact" to identify the source

**Field Mapping Section:**
This is where most people mess up. Contact Form 7 uses field names like `your-name` and `your-email`. Map these to Mailchimp merge fields:

- `your-email` → EMAIL (required)
- `your-name` → FNAME or leave blank if you have separate first/last fields
- `first-name` → FNAME
- `last-name` → LNAME
- `your-company` → COMPANY (if you have this merge field in Mailchimp)
- `your-phone` → PHONE

If you have custom fields in Contact Form 7, you'll need to create corresponding merge fields in Mailchimp first. Go to Audience → Settings → Audience fields and *|MERGE|* tags to add them.

## Step 3: Set Up Zapier Integration (Alternative Method)

If you're going the Zapier route instead, create a new Zap with these settings:

**Trigger**: Contact Form 7 → New Form Submission
**Action**: Mailchimp → Add/Update Subscriber

The Contact Form 7 trigger requires the Flamingo plugin to store form submissions (CF7 doesn't store them by default). Install Flamingo, then connect your WordPress site to Zapier using the webhook URL Zapier provides.

In your Contact Form 7 form, add this to the additional settings:
```
on_sent_ok: "gtag('event', 'generate_lead'); fetch('https://hooks.zapier.com/hooks/catch/YOUR_ZAPIER_WEBHOOK_ID', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({email: '[your-email]', name: '[your-name]', form_id: 'contact-form'})});"
```

Replace `YOUR_ZAPIER_WEBHOOK_ID` with your actual webhook ID from Zapier.

**Field Mapping in Zapier:**
- Email Address: Map to the email field from CF7
- First Name: Map to name field (or first-name if separate)
- Tags: Add a static tag like "website-lead"
- Status: Set to "subscribed" (not "pending" unless you want double opt-in)

## Step 4: Custom Webhook Implementation (Developer Method)

For full control, you can send form data directly to Mailchimp's API. Add this to your theme's `functions.php`:

```php
add_action('wpcf7_mail_sent', 'send_to_mailchimp');

function send_to_mailchimp($contact_form) {
    $submission = WPCF7_Submission::get_instance();
    $posted_data = $submission->get_posted_data();
    
    // Extract form data
    $email = $posted_data['your-email'];
    $fname = $posted_data['first-name'] ?? '';
    $lname = $posted_data['last-name'] ?? '';
    
    // Mailchimp API call
    $api_key = 'your-mailchimp-api-key';
    $list_id = 'your-audience-id';
    $datacenter = substr($api_key, strpos($api_key, '-') + 1);
    
    $url = "https://{$datacenter}.api.mailchimp.com/3.0/lists/{$list_id}/members";
    
    $data = array(
        'email_address' => $email,
        'status' => 'subscribed',
        'merge_fields' => array(
            'FNAME' => $fname,
            'LNAME' => $lname
        ),
        'tags' => array('website-contact')
    );
    
    $response = wp_remote_post($url, array(
        'headers' => array(
            'Authorization' => 'Basic ' . base64_encode('user:' . $api_key),
            'Content-Type' => 'application/json'
        ),
        'body' => json_encode($data),
        'timeout' => 30
    ));
    
    // Log errors for troubleshooting
    if (is_wp_error($response)) {
        error_log('Mailchimp API Error: ' . $response->get_error_message());
    }
}
```

This fires every time a CF7 form is successfully submitted and sends the data to Mailchimp immediately.

## Step 5: Configure Error Handling

Regardless of which method you use, you need to know when the integration breaks. Most people discover missing leads weeks later when they wonder why their email list isn't growing.

**For CF7 Mailchimp Extension:**
The plugin logs errors to your WordPress debug log. Enable debugging in `wp-config.php`:
```php
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
```

**For Zapier:**
Check your Zap history regularly. Zapier will email you when Zaps fail, but only if you have notifications enabled.

**For Custom Implementation:**
The code above logs errors to your WordPress error log. Check `/wp-content/debug.log` for API failures.

Set up a simple monitoring email for critical errors. You can modify the custom code to email you when API calls fail:

```php
if (is_wp_error($response)) {
    wp_mail('you@yoursite.com', 'Mailchimp Integration Failed', 'Form submission failed to sync: ' . $response->get_error_message());
}
```

## Testing & Verification

Here's how to verify everything works before trusting it with real leads:

1. **Submit a test form** using an email address you can check
2. **Check Mailchimp immediately** — the contact should appear in your audience within 30 seconds
3. **Verify field mapping** — check that first name, last name, and any custom fields populated correctly
4. **Confirm tags were applied** — look for the tag you specified in the contact's profile
5. **Test duplicate handling** — submit the same email again and verify it updates rather than creates a duplicate

**Red flags that indicate problems:**
- Contact appears in Mailchimp but missing first/last name (field mapping issue)
- 2-5 minute delay before contacts appear (API timeout/retry issues)  
- Some form submissions sync but others don't (intermittent API failures)
- Contacts appear without tags (tag configuration not working)

I consider 95%+ sync rate acceptable. If you're missing more than 5% of submissions, something's configured wrong.

## Troubleshooting

**Problem**: Form submissions aren't creating Mailchimp contacts at all
The API key is wrong or the audience ID doesn't exist. Double-check both in Mailchimp. Also verify that Contact Form 7 is actually firing the submission event — install Flamingo to confirm forms are being submitted successfully.

**Problem**: Contacts are created but missing first/last names
Your field mapping doesn't match your actual form field names. Contact Form 7 uses `your-name`, `your-email` by default, but your form might use `first-name`, `email-address`. Check the form shortcodes to see exact field names.

**Problem**: Getting "Member Exists" errors in logs
This happens when you try to add someone who's already in the audience. Set the integration to "update existing" rather than "add new only." For the API method, use PUT instead of POST to the members endpoint.

**Problem**: Integration worked for a few days then stopped
Usually an API key that expired or got regenerated. Mailchimp API keys don't expire automatically, but if you regenerated one for security, you need to update it everywhere. Check your Mailchimp account for any security changes.

**Problem**: Contacts appear in Mailchimp but tags aren't being applied
Tag names are case-sensitive and can't have spaces. Use "website-contact" not "Website Contact". Also check that you have permission to add tags to the audience.

**Problem**: Zapier integration missing random submissions
Zapier has processing limits on free plans and can miss webhooks during high traffic. Upgrade to a paid plan or switch to the direct plugin method. Also check that Flamingo is storing all form submissions — if CF7 isn't storing them, Zapier can't see them.

## What To Do Next

Now that your Contact Form 7 submissions are flowing into Mailchimp, consider setting up [Contact Form 7 to HubSpot integration](/integrations/contact-form-7-to-hubspot) if you need more robust CRM features, or [Contact Form 7 Google Ads conversion tracking](/tracking/contact-form-7-google-ads-conversion-tracking) to measure which campaigns are driving form submissions.

You might also want to explore [other Mailchimp integrations](/integrations/mailchimp) to connect additional lead sources to the same email list.

Not sure if your integration is capturing all leads? I audit tracking and integration setups for free — [contact me](/contact) and I'll take a look.

*This guide is part of the [Mailchimp Integration Hub](/integrations/mailchimp) — covering how to connect various lead sources and marketing tools to your Mailchimp audience.*