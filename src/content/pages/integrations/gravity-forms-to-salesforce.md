---
title: "How to Send Gravity Forms Leads to Salesforce (Setup Guide)"
slug: "gravity-forms-to-salesforce"
description: "Connect Gravity Forms to Salesforce so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/salesforce"
page_type: "spoke"
---

# Gravity Forms → Salesforce Integration Guide

I see Gravity Forms → Salesforce setups broken in about 30% of the WordPress sites I audit. Usually it's field mapping issues or the integration just... stops working and nobody notices for weeks. You're getting form submissions on your site, but your sales team is wondering where all the leads went.

The good news: once you get this right, it's bulletproof. Every form fill creates a Salesforce lead automatically, with proper field mapping and error handling.

## What You'll Have Working By The End

- Every Gravity Forms submission creates a Salesforce lead in real-time
- Custom field mapping between your form fields and Salesforce Lead object
- Duplicate detection so you don't create multiple leads for the same person
- Error logging when submissions fail to sync
- Test process to verify leads are flowing correctly

## Prerequisites

- [ ] WordPress site with Gravity Forms installed (version 2.4+ recommended)
- [ ] Salesforce account with API access (Professional edition or higher)
- [ ] Admin access to both WordPress and Salesforce
- [ ] For webhook method: basic understanding of REST APIs

## Step 1: Choose Your Integration Method

I rank these by reliability and maintenance overhead:

**Native Salesforce Add-On (Recommended)**
- $99/year but worth every penny for the reliability
- Built-in field mapping, error handling, and duplicate detection
- Handles Salesforce API changes automatically

**Zapier Connection**
- Good middle ground if you're already using Zapier
- $20/month minimum, can get expensive with volume
- Reliable but adds another service dependency

**Webhook + Custom API**
- Free but requires development work
- Full control over the integration
- You're responsible for API changes and error handling

**Web-to-Lead (Quick & Dirty)**
- Salesforce's simplest option
- No real-time confirmation of success
- Limited field mapping and no error handling

Skip the manual CSV export method. If you're doing that, you don't need this guide.

## Step 2: Set Up Salesforce Lead Object

Before connecting anything, make sure your Salesforce Lead object has the fields you need.

Go to Setup → Object Manager → Lead → Fields & Relationships. You'll need at minimum:
- Email (standard field)
- First Name (standard field)  
- Last Name (standard field)
- Company (standard field)
- Lead Source (standard field)

For custom fields, note the API names. They'll look like `Custom_Field__c`. You'll need these exact names for field mapping.

**Pro tip:** Set a default Lead Source value like "Website Form" so you can track which leads came from Gravity Forms vs. other sources.

## Step 3A: Native Salesforce Add-On Setup (Recommended Path)

Purchase and install the Gravity Forms Salesforce Add-On from the Gravity Forms website.

**Configure Salesforce Connection:**
1. In WordPress admin, go to Forms → Settings → Salesforce
2. Click "Add New" to create a Salesforce account connection
3. Enter your Salesforce credentials or use OAuth (OAuth is more secure)
4. Test the connection — you should see "Valid" status

**Set Up Feed on Your Form:**
1. Edit your Gravity Form
2. Go to Settings → Salesforce
3. Click "Add New" to create a feed
4. Choose "Lead" as the Salesforce Object
5. Map your form fields:

```
Form Field → Salesforce Field
First Name (field ID 1) → First Name
Last Name (field ID 2) → Last Name  
Email (field ID 3) → Email
Company (field ID 4) → Company
Phone (field ID 5) → Phone
Message (field ID 6) → Description
```

**Important:** Use the "Conditional Logic" section if you only want certain submissions to sync (like excluding spam or test submissions).

## Step 3B: Zapier Integration Setup

If you're going the Zapier route:

**Create the Zap:**
1. New Zap → Gravity Forms trigger → "Form Submission"
2. Connect your WordPress site (you'll need the Zapier Add-On for Gravity Forms)
3. Select your specific form
4. Test trigger with a real form submission

**Configure Salesforce Action:**
1. Add Salesforce app → "Create Record" action
2. Choose "Lead" as the record type
3. Map fields from Gravity Forms to Salesforce:

```javascript
// Example field mapping in Zapier
First Name: {{1. First Name}}
Last Name: {{1. Last Name}}
Email: {{1. Email}}
Company: {{1. Company}}
Lead Source: "Website Form"
Description: {{1. Message}}
```

**Set up error handling:** In Zapier's error settings, choose "Continue on error" and send error notifications to your email.

## Step 3C: Webhook + API Method

For the webhook approach, you'll need custom code. Add this to your theme's functions.php:

```php
add_action('gform_after_submission', 'send_to_salesforce', 10, 2);

function send_to_salesforce($entry, $form) {
    // Only process specific form (replace 1 with your form ID)
    if ($form['id'] != 1) return;
    
    $salesforce_data = array(
        'FirstName' => rgar($entry, '1'), // Field ID 1
        'LastName' => rgar($entry, '2'),  // Field ID 2
        'Email' => rgar($entry, '3'),     // Field ID 3
        'Company' => rgar($entry, '4'),   // Field ID 4
        'Phone' => rgar($entry, '5'),     // Field ID 5
        'Description' => rgar($entry, '6'), // Field ID 6
        'LeadSource' => 'Website Form'
    );
    
    $response = wp_remote_post('https://yourinstance.salesforce.com/services/data/v52.0/sobjects/Lead/', array(
        'headers' => array(
            'Authorization' => 'Bearer ' . get_salesforce_access_token(),
            'Content-Type' => 'application/json'
        ),
        'body' => json_encode($salesforce_data)
    ));
    
    // Log errors
    if (is_wp_error($response)) {
        error_log('Salesforce sync failed: ' . $response->get_error_message());
    }
}
```

You'll also need OAuth handling for the access token. This is getting complex — honestly, just buy the native add-on.

## Step 4: Configure Field Mapping

This is where most setups break. Here's how to map common form fields:

**Standard Lead Fields:**
- `FirstName` → First name input
- `LastName` → Last name input
- `Email` → Email input
- `Company` → Company input
- `Phone` → Phone input
- `LeadSource` → Set to "Website Form" or similar

**Custom Fields (use exact API names):**
- `Website__c` → Website URL input
- `How_Did_You_Hear__c` → Dropdown/radio selection
- `Budget__c` → Budget range field
- `Timeline__c` → Timeline field

**Multi-value fields:** For checkboxes that allow multiple selections, Salesforce expects comma-separated values like "Option 1, Option 2, Option 3".

## Step 5: Set Up Duplicate Detection

In Salesforce, go to Setup → Duplicate Management → Duplicate Rules. Create a rule for Leads that checks:
- Email (exact match)
- First Name + Last Name + Company (fuzzy match)

Choose "Block" for exact email matches and "Allow but alert" for name/company matches.

## Testing & Verification

**Test the Integration:**
1. Fill out your form with a test email (use something like test+timestamp@yourdomain.com)
2. Submit the form
3. Check Salesforce within 30 seconds — the lead should appear
4. Verify all fields mapped correctly
5. Check that Lead Source is set properly

**For Native Add-On:** Check Forms → Entries → View entry → Salesforce section for sync status.

**For Zapier:** Check your Zap history for successful runs.

**For Webhooks:** Check your error logs for any PHP errors.

**Ongoing monitoring:** Set up a weekly check. Search Salesforce for leads with source "Website Form" from the past week and compare to your Gravity Forms entries count. They should match within 5%.

## Troubleshooting

**Problem:** Form submits but no lead appears in Salesforce
→ Check your field mapping. Email is required for Salesforce leads. Also verify your Salesforce connection is still active — API tokens expire.

**Problem:** Leads created but custom fields are empty
→ Double-check the API field names in Salesforce. Custom fields end with `__c`. The name "Budget Range" becomes API name `Budget_Range__c`.

**Problem:** Getting "REQUIRED_FIELD_MISSING" errors
→ Salesforce requires Email, LastName, and Company fields. Make sure these form fields are marked as required and mapping correctly.

**Problem:** Integration worked, then stopped
→ Usually an expired API token or Salesforce password change. Reconnect your integration. With the native add-on, go to Forms → Settings → Salesforce and reconnect your account.

**Problem:** Duplicate leads being created
→ Set up Salesforce duplicate rules (see Step 5) or add conditional logic to your integration to check for existing leads with the same email first.

**Problem:** Webhook failing with 401 errors
→ Your Salesforce access token expired. You need proper OAuth refresh token handling. Seriously, just buy the native add-on — it handles this automatically.

## What To Do Next

Now that leads are flowing into Salesforce, you might want to:
- [Track Gravity Forms conversions in Google Ads](/tracking/gravity-forms-google-ads-conversion-tracking) so you know which campaigns drive the best leads
- Set up [Gravity Forms → HubSpot integration](/integrations/gravity-forms-to-hubspot) if you're using both CRMs
- Connect [Gravity Forms → ActiveCampaign](/integrations/gravity-forms-to-activecampaign) for email marketing automation
- Get a [free tracking audit](/contact) to see what other lead sources you might be missing

*This guide is part of the [Salesforce Integration Hub](/integrations/salesforce) — connecting your lead sources to Salesforce so nothing falls through the cracks.*