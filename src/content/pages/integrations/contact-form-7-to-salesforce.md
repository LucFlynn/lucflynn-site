---
title: "How to Send Contact Form 7 Leads to Salesforce (Setup Guide)"
slug: "contact-form-7-to-salesforce"
description: "Connect Contact Form 7 to Salesforce so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/salesforce"
page_type: "spoke"
---

# Contact Form 7 → Salesforce Integration Guide

Contact Form 7 dumps all its submissions into email by default — which means you're manually copying leads into Salesforce or watching them disappear into your inbox. I've audited dozens of WordPress sites where leads are getting lost in this gap, and the fix is straightforward once you know which method actually works for your setup.

The problem with most CF7-to-Salesforce tutorials is they assume you want to build a custom API integration from scratch. Most people just want their form submissions to show up as Salesforce leads without breaking their site or hiring a developer.

## What You'll Have Working By The End

- Every Contact Form 7 submission automatically creates a Salesforce lead
- Form fields mapped to the correct Salesforce fields (first name, last name, email, company, etc.)
- Error handling so you know when leads aren't making it through
- A test process to verify submissions are flowing correctly
- Backup method so no leads get lost if the integration breaks

## Prerequisites

- [ ] WordPress site with Contact Form 7 plugin installed and active
- [ ] Salesforce account with lead creation permissions
- [ ] Admin access to both WordPress and Salesforce
- [ ] Contact Form 7 Database Addon (CFDB7) plugin installed (recommended for backup)
- [ ] Your Salesforce Web-to-Lead URL or API credentials ready

## Step 1: Choose Your Integration Method

There's no official native integration between Contact Form 7 and Salesforce, so you have three realistic options:

**Salesforce Web-to-Lead** (easiest, works for 80% of setups): Salesforce generates HTML forms that you modify to work with CF7. Best for simple lead capture.

**Zapier integration** (most reliable): Connects CF7 submissions to Salesforce automatically. Costs $20/month but handles error retry and field mapping well.

**Webhook + REST API** (most flexible): Custom code that sends CF7 submissions to Salesforce API. Requires development work but gives you complete control.

For most businesses, I recommend starting with Zapier unless you have specific requirements that need the API approach.

## Step 2: Set Up Salesforce Web-to-Lead (Recommended First Try)

In Salesforce, go to Setup → Web-to-Lead and generate your HTML form code. You'll get something that looks like this:

```html
<form action="https://webto.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8" method="POST">
<input type=hidden name="oid" value="00D000000000000">
<input type="text" name="first_name">
<input type="text" name="last_name">
<input type="email" name="email">
<input type="text" name="company">
<input type="submit" value="Submit">
</form>
```

Now you need to modify your Contact Form 7 form to send to this endpoint. Add this to your CF7 form's Additional Settings tab:

```
on_sent_ok: "document.getElementById('salesforce-form').submit();"
```

Then create a hidden form on your page that matches the Salesforce structure:

```html
<form id="salesforce-form" action="https://webto.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8" method="POST" style="display:none;">
<input type="hidden" name="oid" value="YOUR_ORG_ID">
<input type="hidden" name="first_name" id="sf-first-name">
<input type="hidden" name="last_name" id="sf-last-name">
<input type="hidden" name="email" id="sf-email">
<input type="hidden" name="company" id="sf-company">
</form>
```

The problem with this approach: CF7 submissions don't automatically populate those hidden fields. You need JavaScript to copy the values:

```javascript
document.addEventListener('wpcf7mailsent', function(event) {
    // Map CF7 fields to Salesforce fields
    document.getElementById('sf-first-name').value = event.detail.inputs.find(input => input.name === 'your-name').value;
    document.getElementById('sf-last-name').value = event.detail.inputs.find(input => input.name === 'your-surname').value;
    document.getElementById('sf-email').value = event.detail.inputs.find(input => input.name === 'your-email').value;
    document.getElementById('sf-company').value = event.detail.inputs.find(input => input.name === 'your-company').value;
    
    // Submit to Salesforce
    document.getElementById('salesforce-form').submit();
}, false);
```

This works, but it's fragile. If your CF7 field names change or the JavaScript breaks, leads stop flowing. That's why I usually recommend Zapier instead.

## Step 3: Set Up Zapier Integration (Most Reliable)

Install the CF7 Database Addon (CFDB7) plugin first — Zapier needs somewhere to pull the form submissions from since CF7 doesn't store them by default.

Create a new Zap in Zapier:

1. **Trigger**: Contact Form 7 → New Form Submission
2. **Action**: Salesforce → Create Record

Connect your WordPress site to Zapier using the webhook URL they provide. In your CF7 form's Additional Settings, add:

```
additional_headers: "Content-Type: application/json"
on_sent_ok: "zapier_webhook_url"
```

Actually, that's not how CF7 webhooks work. You need to use a different approach. Install the "Zapier for Contact Form 7" plugin, or use this PHP code in your theme's functions.php:

```php
add_action('wpcf7_mail_sent', 'send_to_zapier');

function send_to_zapier($contact_form) {
    $submission = WPCF7_Submission::get_instance();
    $posted_data = $submission->get_posted_data();
    
    $zapier_webhook = 'https://hooks.zapier.com/hooks/catch/YOUR_WEBHOOK_ID/';
    
    wp_remote_post($zapier_webhook, array(
        'body' => json_encode($posted_data),
        'headers' => array('Content-Type' => 'application/json')
    ));
}
```

In Zapier, map your CF7 fields to Salesforce fields:

- `your-name` → First Name
- `your-surname` → Last Name  
- `your-email` → Email
- `your-company` → Company
- `your-message` → Description

Set the Salesforce record type to "Lead" and make sure required fields are mapped. Salesforce requires Last Name and either Email or Company for lead creation.

## Step 4: Field Mapping and Data Cleanup

Your Salesforce fields have specific API names that might not match what you expect:

- First Name = `FirstName`
- Last Name = `LastName` (required)
- Email = `Email`
- Company = `Company`
- Phone = `Phone`
- Lead Source = `LeadSource`

In CF7, your field names probably look like `[text* your-name]`. The data flows through as:

Contact Form 7 field → Integration → Salesforce API name

Make sure your integration handles these conversions correctly. If you're using Zapier, it shows you the available Salesforce fields in a dropdown.

Set a default Lead Source value like "Website Form" so you can track where leads came from. This is crucial for ROI reporting later.

For phone numbers, format them consistently. Salesforce accepts most formats, but clean data is better data:

```javascript
// Clean phone number format
function cleanPhone(phone) {
    return phone.replace(/\D/g, '').replace(/(\d{3})(\d{3})(\d{4})/, '($1) $2-$3');
}
```

## Step 5: Error Handling and Backup

Contact Form 7 doesn't tell you when external integrations fail. The user sees "Message sent successfully" even if Salesforce rejected the lead.

Install CFDB7 (Contact Form DB) to store all submissions locally as backup. Even if your Salesforce integration breaks, you won't lose leads.

For Zapier users, check your Zap history regularly. Failed zaps show up with error messages like "Required field missing" or "Invalid email format."

For webhook integrations, add error logging:

```php
add_action('wpcf7_mail_sent', 'send_to_salesforce_with_logging');

function send_to_salesforce_with_logging($contact_form) {
    $submission = WPCF7_Submission::get_instance();
    $posted_data = $submission->get_posted_data();
    
    $response = wp_remote_post($salesforce_endpoint, array(
        'body' => json_encode($posted_data),
        'headers' => array('Content-Type' => 'application/json')
    ));
    
    if (is_wp_error($response)) {
        error_log('Salesforce integration failed: ' . $response->get_error_message());
    } else {
        $response_code = wp_remote_retrieve_response_code($response);
        if ($response_code !== 200) {
            error_log('Salesforce returned error code: ' . $response_code);
        }
    }
}
```

Check your WordPress error logs weekly for integration failures.

## Testing & Verification

Submit a test form with fake but realistic data:

- Name: Test User
- Email: test@yourdomain.com (use your domain so it doesn't look like spam)
- Company: Test Company
- Message: This is a test submission

**In Contact Form 7**: You should see the success message and receive the email notification.

**In Salesforce**: Check Leads → Recent Items. Your test lead should appear within 2-5 minutes. Look for:
- Correct name and email mapping
- Lead Source = "Website Form" (or whatever you set)
- All custom fields populated correctly

**In Zapier** (if using): Check Zap History. Successful zaps show green checkmarks. Failed zaps show red X's with error details.

If the lead doesn't appear in Salesforce, check these first:
- Salesforce Lead assignment rules (lead might be assigned to inactive user)
- Required field validation (LastName and Email/Company required)
- Duplicate lead rules (Salesforce might be merging with existing record)

The acceptable delay is 2-5 minutes for most integrations. If leads take longer than 10 minutes to appear, something's wrong with your setup.

## Troubleshooting

**Problem**: Form submits successfully but no lead appears in Salesforce
Check your Salesforce Lead assignment rules. If leads are assigned to inactive users, they might not show up in your view. Go to Setup → Assignment Rules and verify active user assignment.

**Problem**: Getting "Required field missing" errors in Zapier
Salesforce requires LastName and either Email or Company for lead creation. Make sure these CF7 fields are mapped and not empty. Add field validation to your CF7 form: `[text* your-name class:required]`

**Problem**: Duplicate leads created for same email address
Salesforce has duplicate management rules that you can configure. Go to Setup → Duplicate Management and set up rules to merge or block duplicate leads based on email address.

**Problem**: Special characters breaking the integration
CF7 submissions with quotes, apostrophes, or non-English characters can break JSON formatting. Sanitize the data before sending:

```php
function sanitize_for_salesforce($data) {
    return array_map(function($value) {
        return is_string($value) ? sanitize_text_field($value) : $value;
    }, $data);
}
```

**Problem**: Integration worked then stopped working
Check if your Salesforce API limits were exceeded. Free Salesforce accounts have daily API call limits. Paid accounts have higher limits but can still be exceeded. Monitor usage in Setup → System Overview.

**Problem**: Leads appearing with wrong Lead Source
Your Lead Source field mapping might be overridden by Salesforce automation. Check Setup → Process Builder and Flows for any rules that modify Lead Source on new leads. Make sure your integration sets Lead Source last, or disable conflicting automation.

## What To Do Next

Once your Contact Form 7 leads are flowing to Salesforce, consider these related integrations:

- Set up [Contact Form 7 → HubSpot integration](/integrations/contact-form-7-to-hubspot) for marketing automation
- Connect [Contact Form 7 → GoHighLevel](/integrations/contact-form-7-to-gohighlevel) for sales funnel tracking  
- Add [Contact Form 7 → ActiveCampaign](/integrations/contact-form-7-to-activecampaign) for email sequences
- Configure [Contact Form 7 Google Ads conversion tracking](/tracking/contact-form-7-google-ads-conversion-tracking) to measure ad performance

Need help auditing your current tracking setup? I offer [free tracking audits](/contact) where I'll review your integrations and identify gaps that are costing you leads.

*This guide is part of the [Salesforce Integrations Hub](/integrations/salesforce) — complete guides for connecting Salesforce to every major form tool and marketing platform.*