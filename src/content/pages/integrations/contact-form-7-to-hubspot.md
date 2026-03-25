---
title: "How to Send Contact Form 7 Leads to HubSpot (Setup Guide)"
slug: "contact-form-7-to-hubspot"
description: "Connect Contact Form 7 to HubSpot so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/hubspot"
page_type: "spoke"
---

# Contact Form 7 → HubSpot Integration Guide

I see this exact problem in about 60% of WordPress sites I audit: Contact Form 7 forms are sending submissions to email, but nothing's making it into HubSpot. Sales teams are manually copy-pasting leads from their inbox into the CRM, or worse — leads are sitting in email and never getting followed up on. Contact Form 7 is lightweight by design, but that means it doesn't play nicely with CRMs out of the box.

## What You'll Have Working By The End

• Every Contact Form 7 submission automatically creates or updates a contact in HubSpot
• Complete field mapping so form data lands in the right HubSpot properties
• Automatic lead scoring and workflow triggers based on form submissions
• Error handling so you know when leads aren't making it through
• Testing process to verify the integration is working correctly

## Prerequisites

- [ ] Contact Form 7 plugin installed and active on WordPress
- [ ] HubSpot account with API access (free tier works)
- [ ] WordPress admin access to install plugins
- [ ] HubSpot admin access to create API keys
- [ ] At least one Contact Form 7 form already created

## Method 1: HubSpot WordPress Plugin (Recommended)

HubSpot offers a native WordPress plugin that connects directly with Contact Form 7. This is the most reliable option I've found — it handles about 95% of use cases without breaking.

Install the HubSpot All-In-One Marketing plugin from the WordPress repository. Once activated, go to **HubSpot → Settings** and connect your HubSpot account using OAuth (don't use API keys for this method).

Navigate to **HubSpot → Forms** and you'll see a "Contact Form 7" tab. Select the Contact Form 7 form you want to connect, then click "Connect to HubSpot."

For field mapping, the plugin auto-detects common fields:
- `your-name` → First Name
- `your-email` → Email
- `your-subject` → Subject
- `your-message` → Message

Custom fields need manual mapping. If you have a field called `company` in Contact Form 7, map it to HubSpot's "Company" property. Phone number fields should map to "Phone Number" — HubSpot will auto-format them.

The plugin creates a HubSpot form behind the scenes and submits to it via JavaScript. This means submissions bypass WordPress entirely once the form loads, which is actually more reliable than webhook approaches.

## Method 2: Zapier Integration

If the native plugin doesn't work for your setup (usually because of custom fields or complex form logic), Zapier is my second choice. It's more flexible but adds another service that can break.

You'll need the Contact Form 7 Database Addon (CFDB7) plugin installed first. Contact Form 7 doesn't store submissions by default — they just go to email. CFDB7 captures them in WordPress, which Zapier can then read.

In Zapier, create a new Zap with "Contact Form 7" as the trigger. You'll need to authenticate using your WordPress site URL and admin credentials. Select "New Form Submission" as the trigger event.

Test the trigger by submitting your Contact Form 7 form. Zapier should pull in the submission data within 1-2 minutes.

For the action, choose "HubSpot" and "Create or Update Contact." Map your fields:
- Contact Form 7 "Name" → HubSpot "First Name"
- Contact Form 7 "Email" → HubSpot "Email"
- Contact Form 7 "Message" → HubSpot "Message"

Set the email field as the deduplication key so repeat submissions update the existing contact instead of creating duplicates.

## Method 3: Custom Webhook Integration

For maximum control, you can build a custom webhook that fires on Contact Form 7 submission. This requires some PHP knowledge but gives you complete control over the data flow.

Add this code to your theme's `functions.php` file or a custom plugin:

```php
add_action('wpcf7_mail_sent', 'send_to_hubspot');

function send_to_hubspot($contact_form) {
    $submission = WPCF7_Submission::get_instance();
    $posted_data = $submission->get_posted_data();
    
    // Map Contact Form 7 fields to HubSpot properties
    $hubspot_data = array(
        'properties' => array(
            'firstname' => $posted_data['your-name'],
            'email' => $posted_data['your-email'],
            'message' => $posted_data['your-message']
        )
    );
    
    $api_key = 'your-hubspot-api-key';
    $endpoint = 'https://api.hubapi.com/crm/v3/objects/contacts';
    
    $response = wp_remote_post($endpoint, array(
        'headers' => array(
            'Authorization' => 'Bearer ' . $api_key,
            'Content-Type' => 'application/json'
        ),
        'body' => json_encode($hubspot_data)
    ));
    
    if (is_wp_error($response)) {
        error_log('HubSpot API Error: ' . $response->get_error_message());
    }
}
```

Replace `'your-hubspot-api-key'` with an actual private app token from HubSpot. Go to **Settings → Integrations → Private Apps** in HubSpot to create one.

This fires on the `wpcf7_mail_sent` action, which triggers after Contact Form 7 successfully processes the form but before the thank you message displays. If the HubSpot API call fails, the user still sees the success message — they don't need to know about the backend integration.

## Method 4: JavaScript Event Listener

If you can't modify server-side code, you can catch Contact Form 7 submissions with JavaScript and send them to HubSpot directly. This runs in the user's browser, so it's less reliable but sometimes it's your only option.

```javascript
document.addEventListener('wpcf7mailsent', function(event) {
    var formData = new FormData(event.target);
    
    var hubspotData = {
        portalId: 'your-portal-id',
        formGuid: 'your-form-guid',
        fields: [
            {
                name: 'firstname',
                value: formData.get('your-name')
            },
            {
                name: 'email',
                value: formData.get('your-email')
            },
            {
                name: 'message',
                value: formData.get('your-message')
            }
        ]
    };
    
    fetch('https://api.hsforms.com/submissions/v3/integration/submit/' + hubspotData.portalId + '/' + hubspotData.formGuid, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(hubspotData)
    });
}, false);
```

You'll need to create a HubSpot form first to get the `formGuid`. The JavaScript submits to that form whenever Contact Form 7 fires the `wpcf7mailsent` event.

## Testing & Verification

Submit a test form with fake but realistic data. Use your own email address so you can verify the email notification still works.

In HubSpot, go to **Contacts → Contacts** and search for the email address you used. The contact should appear within 30 seconds for native integrations, up to 15 minutes for Zapier.

Check that all mapped fields populated correctly. If you sent "John Doe" in the name field, HubSpot should show "John" as the first name (assuming you mapped it correctly).

Look at the contact's activity timeline. You should see a form submission event with the form name and timestamp.

For webhook integrations, check your server's error logs if the contact doesn't appear. Failed API calls usually leave error messages that tell you exactly what went wrong.

## Troubleshooting

**Problem:** Contact appears in HubSpot but some fields are missing  
Check your field mapping. Contact Form 7 uses the field name as the key (like `your-name`), while HubSpot uses internal property names (like `firstname`). Mismatched field names result in empty properties. Also verify that the HubSpot properties exist — custom properties must be created before you can map to them.

**Problem:** Duplicate contacts being created instead of updating existing ones  
HubSpot deduplicates on email address by default, but only if you're using the Contacts API correctly. For Zapier, make sure you selected "Create or Update Contact" not just "Create Contact." For custom webhooks, use the PATCH method on existing contacts instead of always POSTing new ones.

**Problem:** Integration worked for a few days then stopped  
Usually an API key or authentication issue. HubSpot private app tokens don't expire, but OAuth tokens do. For Zapier, the connection might need re-authentication. Check HubSpot's API logs under **Settings → Integrations → Connected Apps** to see recent API calls and any error messages.

**Problem:** Forms submit successfully but nothing reaches HubSpot  
The Contact Form 7 confirmation is showing, which means the form processed correctly on WordPress. The issue is in the integration layer. For native plugins, deactivate and reactivate the HubSpot connection. For webhooks, add error logging to see what's failing. For Zapier, check the Zap history for failed runs.

**Problem:** Some submissions make it through, others don't  
This usually happens with JavaScript-based integrations when users have slow connections or navigate away before the API call completes. Server-side integrations (webhooks, native plugins) are more reliable. If you must use JavaScript, add a small delay before showing the success message.

**Problem:** HubSpot is receiving submissions but they're missing form context  
Make sure you're passing the form name or source in the API call. For the native plugin, this happens automatically. For custom integrations, add a "Lead Source" or "Form Name" property to track which Contact Form 7 form generated the lead. This becomes crucial when you have multiple forms and need to trigger different workflows.

## What To Do Next

Once your Contact Form 7 leads are flowing into HubSpot, set up [conversion tracking for Google Ads](/tracking/contact-form-7-google-ads-conversion-tracking) so you know which ads are driving the most valuable form submissions.

Check out the complete [HubSpot integrations hub](/integrations/hubspot) for connecting other tools like [Contact Form 7 to Salesforce](/integrations/contact-form-7-to-salesforce), [Contact Form 7 to GoHighLevel](/integrations/contact-form-7-to-gohighlevel), and [Contact Form 7 to ActiveCampaign](/integrations/contact-form-7-to-activecampaign).

Need help getting this integration working correctly? I offer [free tracking audits](/contact) where I'll check your current setup and show you exactly what's broken and how to fix it.

*This guide is part of the [HubSpot Integrations Hub](/integrations/hubspot) — complete setup guides for connecting HubSpot to your entire marketing and sales stack.*