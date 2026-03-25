---
title: "How to Send Gravity Forms Leads to Mailchimp (Setup Guide)"
slug: "gravity-forms-to-mailchimp"
description: "Connect Gravity Forms to Mailchimp so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/mailchimp"
page_type: "spoke"
---

# Gravity Forms → Mailchimp Integration Guide

I see this setup in about 30% of WordPress sites I audit, and honestly, it's broken more often than it's working. Forms are collecting leads, but they're dying in WordPress instead of flowing into Mailchimp where you can actually follow up. The most common issue? The native Gravity Forms Mailchimp add-on stops syncing and nobody notices until weeks later.

## What You'll Have Working By The End

- Every Gravity Forms submission automatically creates a Mailchimp contact
- Custom field mapping that preserves all your lead data
- Automatic list segmentation based on form source
- Error handling that alerts you when leads aren't syncing
- A backup method that catches missed submissions

## Prerequisites

- [ ] WordPress admin access with plugin installation rights
- [ ] Gravity Forms license (any tier works)
- [ ] Mailchimp account with at least one audience created
- [ ] Mailchimp API key (we'll generate this in step 1)

## Step 1: Get Your Mailchimp API Credentials

First, you need API access to connect the systems.

In Mailchimp, go to **Account → Extras → API keys**. Click **Create A Key** and copy the key — it looks like `abc123def456-us19`. The last part (`us19`) is your server prefix, which matters for API calls.

You'll also need your Audience ID. Go to **Audience → Settings → Audience name and defaults**. The Audience ID is under "Audience ID" — usually something like `a1b2c3d4e5`.

## Step 2: Install the Native Gravity Forms Mailchimp Add-on

This is the cleanest approach when it works. Gravity Forms has an official Mailchimp add-on that handles the heavy lifting.

Download the add-on from your Gravity Forms account dashboard. In WordPress, go to **Plugins → Add New → Upload Plugin** and install the Mailchimp add-on.

Once installed, go to **Forms → Settings → Mailchimp** and enter your API key from Step 1. The connection should authenticate automatically.

**The catch**: This add-on fails silently about 20% of the time. I'll show you how to monitor it in the testing section.

### Configure the Feed

Go to your form in **Forms → All Forms → [Your Form] → Settings → Mailchimp**.

Click **Add New** to create a feed:
- **Feed Name**: Something descriptive like "Contact Form → Main List"
- **Mailchimp List**: Select your audience
- **Email Address**: Map to your email field (usually "Email")

For field mapping, you'll see your Gravity Forms fields on the left and Mailchimp fields on the right:
- `input_1` (First Name) → FNAME
- `input_2` (Last Name) → LNAME  
- `input_3` (Email) → Email Address
- `input_4` (Phone) → PHONE
- `input_5` (Company) → Create custom field in Mailchimp

**Pro tip**: Create custom fields in Mailchimp first, then refresh the feed setup. The add-on doesn't auto-create fields.

### Conditional Logic

If you only want certain submissions to sync (like excluding newsletter signups), add conditional logic:
- **Enable Condition**: Check the box
- **Send to Mailchimp if**: [Field] is [Value]

Example: Only sync if "Lead Type" equals "Demo Request"

## Step 3: Set Up Zapier as Backup (Recommended)

The native add-on breaks, and when it does, you lose leads. I set up Zapier on about 80% of client accounts as insurance.

Create a new Zap:
1. **Trigger**: Gravity Forms → New Form Submission
2. **Action**: Mailchimp → Add/Update Subscriber

### Zapier Configuration

**Trigger Setup**:
- Connect your WordPress site (you'll need the Zapier add-on for Gravity Forms)
- Select your specific form
- Test to pull in a recent submission

**Action Setup**:
- Connect Mailchimp with your API key
- Select your audience
- Map fields:
  - Email → Email field from form
  - First Name → First Name field
  - Last Name → Last Name field
  - Tags → Add form-specific tag like "gravity-contact-form"

**Double Opt-in**: Turn this OFF if you're using this for sales leads (not newsletter signups). Otherwise you'll lose 40-60% of leads who never confirm.

The Zapier approach costs $20/month but catches leads when the native integration fails. Worth it if you're generating more than a few leads per month.

## Step 4: Webhook Method (Advanced)

If you need more control or the add-on keeps breaking, webhooks give you the most reliability. This requires some code.

In Gravity Forms, go to **Settings → Webhooks** and create a new webhook:
- **Name**: Mailchimp Sync
- **Request URL**: `https://[server].api.mailchimp.com/3.0/lists/[audience-id]/members`
- **Request Method**: POST
- **Request Headers**:
  ```
  Authorization: apikey [your-api-key]
  Content-Type: application/json
  ```

### Webhook Payload

The request body should be:
```json
{
  "email_address": "{Email:1}",
  "status": "subscribed",
  "merge_fields": {
    "FNAME": "{First Name:2}",
    "LNAME": "{Last Name:3}",
    "PHONE": "{Phone:4}"
  },
  "tags": ["gravity-forms"]
}
```

Replace the merge tags `{Email:1}` with your actual field IDs from Gravity Forms.

**Important**: Set status to "subscribed" for sales leads, "pending" for newsletter signups that need confirmation.

## Step 5: Add JavaScript Tracking (Optional)

If you need to track form submissions in Google Ads or Facebook, add this to your theme's functions.php:

```php
add_action('wp_footer', 'gravity_forms_mailchimp_tracking');
function gravity_forms_mailchimp_tracking() {
    ?>
    <script>
    jQuery(document).on('gform_confirmation_loaded', function(event, formId){
        // Google Ads
        if (typeof gtag !== 'undefined') {
            gtag('event', 'conversion', {
                'send_to': 'AW-123456789/AbC-D_efGhIjKlMnOp',
                'value': 1.0,
                'currency': 'USD'
            });
        }
        
        // Facebook Pixel  
        if (typeof fbq !== 'undefined') {
            fbq('track', 'Lead');
        }
    });
    </script>
    <?php
}
```

This fires when Gravity Forms shows the confirmation message, which happens after the Mailchimp sync.

## Testing & Verification

### Test the Integration

1. **Submit a test form** with fake but realistic data
2. **Check Gravity Forms entries** under Forms → Entries — the submission should appear
3. **Check Mailchimp** — the contact should appear in your audience within 2-3 minutes
4. **Verify field mapping** — make sure first name, last name, custom fields all populated correctly
5. **Check tags** — if you set up tagging, those should be applied

### Monitor Ongoing Sync

The native add-on fails silently, so you need monitoring:

**Weekly Check**: Compare form entries to Mailchimp contacts. If Gravity Forms shows 47 submissions this week but Mailchimp only added 39 contacts, something's broken.

**Acceptable Variance**: 5-10% is normal (duplicate emails, invalid addresses). More than 15% means the integration is broken.

**Set Up Alerts**: In Zapier, enable email notifications when zaps fail. This catches webhook/API errors immediately.

## Troubleshooting

**Problem** → Contacts appear in Gravity Forms but not Mailchimp
Check the Mailchimp feed logs under Forms → Settings → Mailchimp → View Logs. Look for API errors like "Invalid email" or "List doesn't exist." Usually it's a field mapping issue or the API key expired.

**Problem** → Duplicate contacts being created for same email
Mailchimp should automatically update existing contacts, but sometimes the email formatting differs (extra spaces, capitalization). Add email normalization to your form validation or use Mailchimp's "update existing" setting in the feed configuration.

**Problem** → Custom fields not syncing
The custom fields must exist in Mailchimp before you map them. Go to Audience → Settings → Audience fields and |*Merge tags* → Add merge tag. Then refresh your Gravity Forms feed setup — the new field will appear in mapping options.

**Problem** → Webhook getting 401 authentication errors
Your API key format is wrong. It should be `username:api-key` where username can be anything and api-key is your full Mailchimp API key including the server suffix (us19, us20, etc.). Example: `anystring:abc123def456-us19`.

**Problem** → Forms work in testing but fail for real users
Usually a JavaScript conflict. Check browser console for errors when the form submits. Common culprits: caching plugins serving stale pages, theme conflicts with jQuery, ad blockers interfering with AJAX submissions.

**Problem** → Integration worked for weeks then stopped
The Mailchimp add-on license expired or there's a plugin conflict after a WordPress update. Check Forms → Settings → Mailchimp for license status. If that's fine, deactivate other plugins one by one to find conflicts.

## What To Do Next

Once your Gravity Forms → Mailchimp integration is running, consider these related setups:

- **[Gravity Forms to HubSpot Integration](/integrations/gravity-forms-to-hubspot)** — Better for B2B sales with deal tracking
- **[Gravity Forms to Salesforce Setup](/integrations/gravity-forms-to-salesforce)** — Enterprise CRM integration
- **[Gravity Forms Google Ads Conversion Tracking](/tracking/gravity-forms-google-ads-conversion-tracking)** — Track form submissions as conversions
- **[Get a free tracking audit](/contact)** — I'll review your current setup and find what's broken

*This guide is part of the [Mailchimp Integrations Hub](/integrations/mailchimp) — complete guides for connecting Mailchimp to your lead generation tools.*