---
title: "How to Send WPForms Leads to HubSpot (Setup Guide)"
slug: "wpforms-to-hubspot"
description: "Connect WPForms to HubSpot so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/hubspot"
page_type: "spoke"
---

# WPForms → HubSpot Integration Guide

I see broken WPForms → HubSpot setups in about 35% of the WordPress sites I audit. The most common issue? People set up the native integration but don't map their custom fields properly, so they're only getting name and email while missing phone numbers, company info, and lead source data. You end up with half-empty contact records and sales teams asking "where did this lead come from?"

The good news is WPForms has one of the cleanest HubSpot integrations available for WordPress forms. When set up correctly, every form submission creates a properly formatted contact with all your custom fields mapped.

## What You'll Have Working By The End

- Every WPForms submission automatically creates or updates a HubSpot contact
- Custom form fields (company, phone, lead source) properly mapped to HubSpot properties
- Form submissions trigger HubSpot workflows for immediate follow-up
- Failed submissions logged so you never lose a lead
- Test process to verify leads are flowing correctly

## Prerequisites

- [ ] WPForms Pro license (native HubSpot integration requires paid version)
- [ ] HubSpot account with API access
- [ ] WordPress admin access to install/configure plugins
- [ ] HubSpot admin permissions to create custom properties
- [ ] Forms already built in WPForms (if not, create them first)

## Step 1: Install and Configure the Native WPForms HubSpot Integration

WPForms has a built-in HubSpot addon that handles the heavy lifting. This is your best option — it's more reliable than Zapier and doesn't require webhook management.

Go to **WPForms → Addons** and install the "HubSpot Addon." Once activated, go to **WPForms → Settings → Integrations** and click "HubSpot."

You'll need your HubSpot API key. In HubSpot, go to **Settings → Integrations → API Key** and generate a new key if you don't have one. Copy this into the WPForms HubSpot settings.

Click "Connect to HubSpot" and authorize the connection. You should see a green "Connected" status.

Now go to any existing form in **WPForms → All Forms** and edit it. Click the **Settings** tab, then **Marketing**, then **HubSpot**. Enable the integration for this form.

## Step 2: Map Your Form Fields to HubSpot Properties

This is where most setups break. WPForms will auto-map basic fields (first name, last name, email), but your custom fields need manual mapping.

In the HubSpot integration settings for your form, you'll see a field mapping section. Here's how to handle the most common field types:

**Standard Fields:**
- WPForms "Name" field → HubSpot "First Name" and "Last Name"
- WPForms "Email" field → HubSpot "Email"
- WPForms "Phone" field → HubSpot "Phone Number"

**Custom Fields:**
If you have a "Company" field in WPForms, map it to HubSpot's "Company Name" property. For lead source tracking, create a Hidden field in WPForms with a default value like "Website Contact Form" and map it to HubSpot's "Lead Source" property.

If you need a HubSpot property that doesn't exist, create it first. Go to **HubSpot → Settings → Properties → Contact Properties** and create a new custom property. Then return to WPForms and it'll appear in the mapping dropdown.

**Pro tip:** For multi-option fields (dropdowns, checkboxes), make sure the values in WPForms exactly match the options in your HubSpot property. Mismatched values will cause the integration to fail silently.

## Step 3: Configure Workflow Triggers in HubSpot

Once contacts are flowing into HubSpot, set up workflows to handle new form submissions automatically.

In HubSpot, go to **Automation → Workflows** and create a new contact-based workflow. Set the enrollment trigger to "Form Submission" and select your WPForms.

Common workflow actions I set up:
- Send internal notification email to sales team
- Add contact to specific list based on form submitted
- Set lead status to "New" 
- Assign to specific sales rep based on form field (like territory or product interest)

You can also trigger workflows based on the "Lead Source" property if you're tracking multiple forms separately.

## Step 4: Set Up Zapier as Backup (Optional but Recommended)

Even with the native integration, I always recommend a Zapier backup for critical forms. It catches leads if the primary integration fails and gives you more advanced routing options.

Create a new Zap with WPForms as the trigger. You'll need to set up a webhook in WPForms first — go to **Settings → Notifications** and add a new notification with "Webhook" as the type.

The webhook URL will be provided by Zapier when you set up the trigger. Test the connection by submitting your form and verifying Zapier catches the data.

For the action, choose "Create or Update Contact in HubSpot." Map the fields the same way you did in the native integration. 

**Which should you use?** Native integration as primary, Zapier as backup. The native integration is faster and more reliable, but Zapier gives you more flexibility for complex routing or data transformation.

## Testing & Verification

Submit a test form with realistic data — use a real email address you can access, include phone and company if those fields exist.

**In WPForms:** Check the Entries section to confirm the submission was recorded. Look for any error messages in the entry details.

**In HubSpot:** Go to Contacts and search for the email address you used. The contact should appear within 30 seconds with all mapped fields populated. If using workflows, check that those triggered correctly too.

**Cross-check the data:** Compare the form entry in WPForms to the contact record in HubSpot. Every mapped field should have transferred correctly. Missing data usually means a mapping issue.

If you set up Zapier backup, check the Zap history to see if it triggered. Even if the native integration worked, the Zapier should have fired too.

I typically see a 1-2 minute delay for workflow triggers, but contact creation should be nearly instant. If contacts aren't appearing after 5 minutes, something's broken.

## Troubleshooting Common Issues

**Problem:** Form submissions appear in WPForms but not in HubSpot → Check your API key hasn't expired. Go to WPForms → Settings → Integrations → HubSpot and test the connection. If it fails, regenerate your HubSpot API key and reconnect.

**Problem:** Contacts created but custom fields are empty → Field mapping issue. Go back to your form's HubSpot integration settings and verify each custom field is mapped to the correct HubSpot property. Make sure the HubSpot property exists and accepts the data type you're sending.

**Problem:** Duplicate contacts being created for same email → HubSpot should automatically dedupe by email, but if you have multiple email properties or are sending to a custom email field, this can break. Check that you're mapping to HubSpot's primary "Email" property, not a custom email field.

**Problem:** Integration worked then stopped → Usually an API rate limit or expired key. Check WPForms error logs in **WPForms → Tools → Logs**. HubSpot's free tier has API limits that paid accounts don't hit.

**Problem:** Phone numbers not formatting correctly → HubSpot expects phone numbers in a specific format. If you're getting errors, add phone number validation to your WPForms field or set up data formatting in Zapier.

**Problem:** Checkbox/dropdown values not transferring → The values in WPForms must exactly match the options in your HubSpot property. Case-sensitive. If your WPForms dropdown says "Small Business" but HubSpot expects "small_business", it'll fail.

## What To Do Next

Now that leads are flowing into HubSpot, you'll want to track which forms are driving the best conversions. Check out [WPForms Google Ads Conversion Tracking](/tracking/wpforms-google-ads-conversion-tracking) to measure form performance in your ad campaigns.

For other CRM integrations, see [WPForms → Salesforce](/integrations/wpforms-to-salesforce), [WPForms → GoHighLevel](/integrations/wpforms-to-gohighlevel), or [WPForms → ActiveCampaign](/integrations/wpforms-to-activecampaign).

Want me to audit your current setup? I'll check your field mapping, test your integration, and identify any missed leads. [Get a free tracking audit here](/contact).

*This guide is part of the [HubSpot Integrations Hub](/integrations/hubspot) — connect your forms, ads, and tracking tools to HubSpot for complete lead visibility.*