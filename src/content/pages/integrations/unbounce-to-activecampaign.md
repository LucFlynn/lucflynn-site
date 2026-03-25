---
title: "How to Send Unbounce Leads to ActiveCampaign (Setup Guide)"
slug: "unbounce-to-activecampaign"
description: "Connect Unbounce to ActiveCampaign so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/activecampaign"
page_type: "spoke"
---

# Unbounce → ActiveCampaign Integration Guide

Most Unbounce → ActiveCampaign integrations I audit are losing 10-20% of form submissions because they're using the wrong connection method or have broken field mapping. The most common issue? Leads are flowing into ActiveCampaign but without the source tracking or custom field data that makes them actionable.

I see this setup in about 60% of accounts I audit — working but not working *well*. You're getting the leads, but you can't tell which campaign generated them, or half the form fields are empty in ActiveCampaign.

## What You'll Have Working By The End

• Every Unbounce form submission automatically creates a contact in ActiveCampaign with full source attribution
• Custom form fields mapping correctly to ActiveCampaign contact properties
• Automation triggers firing immediately when new leads arrive
• Duplicate handling that prevents the same person from creating multiple contacts
• Testing process to verify your integration is capturing every submission

## Prerequisites

Before you start, you need:
- [ ] Admin access to your Unbounce account
- [ ] Admin access to your ActiveCampaign account  
- [ ] The specific ActiveCampaign list(s) where you want leads to go
- [ ] ActiveCampaign API key (found under Settings → Developer)
- [ ] If using Zapier: Premium Zapier account for webhooks

## Step 1: Choose Your Integration Method

ActiveCampaign doesn't have a native Unbounce integration, so you have three options:

**Zapier** (recommended for most setups): Reliable, handles errors well, built-in duplicate detection. Works with all Unbounce form fields.

**Webhook + API** (for technical teams): More control, faster response times, can handle complex field mapping logic. Requires custom code.

**Direct API calls** (advanced): Unbounce Scripts can call ActiveCampaign API directly on form submit. Fastest but hardest to debug.

For 90% of businesses, Zapier is the right choice. It's reliable and handles the edge cases that break custom webhook setups.

## Step 2: Set Up the Zapier Integration

In Zapier, create a new Zap:

**Trigger: Unbounce → Form Submission**
1. Connect your Unbounce account
2. Select the specific landing page and form
3. Test the trigger with a sample submission

**Action: ActiveCampaign → Create/Update Contact**
1. Connect your ActiveCampaign account using your API key
2. Choose "Create/Update Contact" (not just "Create Contact")
3. Set the contact list where leads should go

**Field Mapping** (this is where most setups break):
```
Unbounce Field → ActiveCampaign Field
First Name → First Name
Last Name → Last Name  
Email → Email (required)
Phone → Phone
Company → Company
Job Title → Job Title (custom field)
Message/Comments → Notes field
Landing Page → Custom field "Lead Source Page"
```

**Critical Settings:**
- Set "Update if exists" to YES (prevents duplicates)
- Map the Unbounce page URL to a custom field for source tracking
- Add the campaign name as a tag or custom field

## Step 3: Configure Webhook Method (Alternative)

If you prefer webhooks, here's the setup:

In Unbounce, go to your form settings:
1. Click "Webhooks" tab
2. Add webhook URL: `https://hooks.zapier.com/hooks/catch/xxxxx/` (from your Zapier webhook trigger)
3. Set method to POST
4. Include all form fields

**Direct ActiveCampaign API webhook** (for developers):

```javascript
// Unbounce Script - fires on form submit
lp.jQuery(document).ready(function($) {
    $('#lp-pom-form-123').submit(function(e) {
        var formData = $(this).serialize();
        
        // Send to ActiveCampaign API
        $.ajax({
            url: 'https://yourapp.api-us1.com/api/3/contacts',
            method: 'POST',
            headers: {
                'Api-Token': 'YOUR_API_KEY',
                'Content-Type': 'application/json'
            },
            data: JSON.stringify({
                "contact": {
                    "email": $('#email').val(),
                    "firstName": $('#first_name').val(),
                    "lastName": $('#last_name').val(),
                    "phone": $('#phone').val(),
                    "fieldValues": [
                        {
                            "field": "1", // Custom field ID for source
                            "value": window.location.href
                        }
                    ]
                }
            })
        });
    });
});
```

Replace `#lp-pom-form-123` with your actual form ID from Unbounce.

## Step 4: Handle Source Attribution

This is where most setups fail. You're getting leads, but you don't know which campaign drove them.

**Add these tracking fields to every integration:**

```
Source Page: {Unbounce page URL}
UTM Campaign: {utm_campaign parameter}
UTM Medium: {utm_medium parameter}  
UTM Source: {utm_source parameter}
Referrer: {document.referrer}
Landing Date: {current timestamp}
```

In Zapier, use the "Formatter" step to extract UTM parameters from the page URL. In webhooks, parse the referrer URL to grab UTM values.

**ActiveCampaign Custom Fields Setup:**
Go to Settings → Fields and create:
- Lead Source Page (text)
- UTM Campaign (text) 
- UTM Medium (text)
- Landing Date (date)

## Step 5: Set Up Automation Triggers

In ActiveCampaign, create automations that trigger when contacts are added to your Unbounce list:

1. Go to Automations → New Automation
2. Start from scratch → "Contact Added to List"
3. Select your Unbounce leads list
4. Add your welcome sequence, lead scoring, or sales notifications

**Pro tip**: Tag contacts based on the landing page they came from. This lets you segment your automations by campaign type.

## Step 6: Configure Error Handling

When integrations break (and they will), you need to know immediately.

**Zapier Error Notifications:**
- Set up email alerts for failed Zaps
- Create a backup webhook that logs failed submissions
- Monitor your Zap health daily for the first week

**Webhook Error Handling:**
Add a fallback in your Unbounce Scripts:

```javascript
$.ajax({
    url: 'primary-webhook-url',
    method: 'POST',
    data: formData,
    timeout: 5000
}).fail(function() {
    // Fallback webhook
    $.ajax({
        url: 'backup-webhook-url',
        method: 'POST',
        data: formData
    });
});
```

## Testing & Verification

Here's how to verify everything is working:

**1. Test Form Submission:**
- Fill out your Unbounce form with a unique test email
- Submit the form
- Check Zapier task history (should show successful)
- Look for the contact in ActiveCampaign within 2-3 minutes

**2. Verify Field Mapping:**
- Submit test with all fields filled out
- Check that custom fields populated correctly in ActiveCampaign
- Confirm UTM parameters captured if present in URL

**3. Check Automation Triggers:**
- Verify the contact was added to the correct list
- Confirm any automations triggered (check automation reports)
- Test with a real email address to verify welcome emails fire

**4. Cross-Check Numbers:**
After a week, compare:
- Unbounce form submissions (Conversion Center)  
- ActiveCampaign new contacts from that list
- Should match within 2-5% (some will be spam/test submissions)

If you're seeing more than 10% variance, something's broken.

## Troubleshooting

**Problem**: Leads appearing in ActiveCampaign but all custom fields are empty.
**Solution**: Field mapping issue. Check that your custom field names in ActiveCampaign exactly match what you mapped in Zapier. Field names are case-sensitive.

**Problem**: Getting duplicate contacts for the same email address.
**Solution**: Change your Zapier action to "Create or Update Contact" instead of "Create Contact". Or enable duplicate checking in your webhook logic.

**Problem**: Zapier shows successful but no contact appears in ActiveCampaign.
**Solution**: The contact might be unsubscribed or in a different list than expected. Check your ActiveCampaign activity log for that email address.

**Problem**: Integration worked for a week then stopped.
**Solution**: Usually API key expiration or Unbounce form ID change. Check your Zapier error log first, then verify the API key is still active in ActiveCampaign.

**Problem**: UTM parameters not capturing correctly.
**Solution**: Make sure your Unbounce page URL includes the UTM parameters when the form is submitted. Use the Formatter step in Zapier to extract them from the full URL.

**Problem**: Webhooks timing out or failing intermittently.
**Solution**: ActiveCampaign API can be slow during peak hours. Increase your timeout to 10+ seconds and add retry logic for 5xx errors.

## What To Do Next

Now that your leads are flowing into ActiveCampaign, you'll want to set up proper tracking for your ad campaigns:

- [Unbounce Google Ads Conversion Tracking](/tracking/unbounce-google-ads-conversion-tracking) — Track which ads are generating your best leads
- [Unbounce to HubSpot Integration](/integrations/unbounce-to-hubspot) — If you need a more robust CRM alternative  
- [Unbounce to Salesforce Integration](/integrations/unbounce-to-salesforce) — For enterprise sales teams
- [Free tracking audit](/contact) — I'll review your setup and find what's missing 10-15% of your leads

*This guide is part of the [ActiveCampaign Integration Hub](/integrations/activecampaign) — complete guides for connecting ActiveCampaign to every major form tool and landing page builder.*