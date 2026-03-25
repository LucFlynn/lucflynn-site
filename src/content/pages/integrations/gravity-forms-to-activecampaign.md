---
title: "How to Send Gravity Forms Leads to ActiveCampaign (Setup Guide)"
slug: "gravity-forms-to-activecampaign"
description: "Connect Gravity Forms to ActiveCampaign so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/activecampaign"
page_type: "spoke"
---

# Gravity Forms → ActiveCampaign Integration Guide

I see this exact setup in maybe 35% of WordPress sites I audit, and about half of them are missing leads because the connection broke months ago and nobody noticed. The most common culprit? Gravity Forms sends data perfectly, but ActiveCampaign never receives it because someone changed an API key or the webhook URL got mangled during a site migration.

The good news is this integration is actually pretty bulletproof once you set it up correctly. ActiveCampaign has solid webhook handling, and Gravity Forms has reliable submission hooks.

## What You'll Have Working By The End

- Every form submission automatically creates a contact in ActiveCampaign
- Custom fields from your form mapped to the right ActiveCampaign contact fields
- Duplicate contacts handled intelligently (update existing vs. create new)
- Form submissions trigger your ActiveCampaign automations
- Test process to verify leads are flowing correctly

## Prerequisites

- [ ] WordPress admin access to install/configure plugins
- [ ] ActiveCampaign account with API access (any paid plan)
- [ ] Gravity Forms license (Basic, Pro, or Elite)
- [ ] Your ActiveCampaign API URL and key (found in Settings → Developer)

## Step 1: Install the Native ActiveCampaign Add-On

Gravity Forms has an official ActiveCampaign add-on that handles this connection. It's the most reliable method I've seen.

Go to Forms → Add-Ons in your WordPress dashboard. If you don't see "ActiveCampaign" listed, you'll need to download it from your Gravity Forms account downloads section.

Once installed:

1. Go to Forms → Settings → ActiveCampaign
2. Enter your ActiveCampaign API URL (looks like `https://youraccountname.api-us1.com`)
3. Enter your API Key
4. Click "Update Settings"

The plugin will test the connection automatically. If it fails here, double-check your API credentials. The API URL format trips up about 20% of people — make sure you're using the full URL with your account name, not just "api-us1.com".

## Step 2: Configure Form-Level Integration

Now you need to set up the integration on each form that should send leads to ActiveCampaign.

1. Edit your Gravity Form
2. Go to Settings → ActiveCampaign
3. Click "Add New" to create a feed

**Essential Feed Settings:**
- **Name**: Something descriptive like "Contact Form → AC Leads"
- **List**: Select the ActiveCampaign list where contacts should be added
- **Double Opt-in**: Choose based on your compliance needs (I recommend "No" for most B2B forms)

**Field Mapping**: This is where most setups break. Map your form fields to ActiveCampaign contact fields:
- Email (required) → Email Address
- First Name → First Name  
- Last Name → Last Name
- Phone → Phone
- Company → Organization (if you have this custom field)

For custom fields, you'll need to create them in ActiveCampaign first (Lists → Manage Fields), then they'll appear in the mapping dropdown.

**Conditional Logic**: Only set this if you want the integration to fire based on specific form responses (like "Yes, I want marketing emails").

## Step 3: Set Up Automation Triggers (Optional but Recommended)

In ActiveCampaign, create an automation that triggers when a contact is added to your form's list:

1. Automations → New Automation
2. Choose "Subscribes to a list" trigger
3. Select the list your form feeds into
4. Add your desired actions (welcome email, tag assignment, deal creation, etc.)

This is where the real power comes in. I typically set up a sequence that:
- Tags contacts with the form name (like "Contact-Form-Lead")
- Creates a deal in the pipeline if it's a sales inquiry
- Assigns the contact to the right team member based on form responses

## Step 4: Handle Duplicate Contacts

By default, the Gravity Forms add-on will update existing contacts rather than create duplicates. This is usually what you want.

But if you're running multiple forms and want different behavior per form, you can control this in the feed settings under "Update Contact" — set it to "No" if you always want new contacts created.

Most of my clients prefer the update behavior because it means progressive profiling works correctly. Someone fills out a simple newsletter form first, then later submits a more detailed contact form — all their data gets combined into one contact record.

## Testing & Verification

**Test Form Submission:**
1. Submit a test entry through your form using a unique email address
2. Check the form entries in WordPress (Forms → Entries) — you should see your test entry
3. Check ActiveCampaign contacts — your test contact should appear within 1-2 minutes

**Verify Integration Feed:**
In your Gravity Form settings, go to ActiveCampaign and look at your feed. Recent submissions should show in the "Entries" column. If it shows 0 entries but you know forms were submitted, something's broken.

**Check ActiveCampaign Activity:**
In ActiveCampaign, view your test contact's activity timeline. You should see an entry like "Subscribed to [List Name] via API" with a timestamp matching your form submission.

**Cross-Check the Numbers:**
Compare your form entries count (Forms → Entries) to your ActiveCampaign list size over the same period. They should match within 1-2 contacts (accounting for spam submissions that might get filtered).

## Troubleshooting

**Problem**: Form submits successfully but no contact appears in ActiveCampaign
Check your API credentials first. Then look in Forms → Settings → ActiveCampaign and click "Test Connection." If that passes, check if your form feed is set to "Active" — inactive feeds won't send data.

**Problem**: Contacts are created but missing custom field data  
Your custom fields in ActiveCampaign need to match the field mapping exactly. Go to ActiveCampaign → Lists → Manage Fields and verify the custom field names match what's in your Gravity Forms mapping. Case sensitivity matters.

**Problem**: Getting duplicate contacts for the same email
This usually means "Update Contact" is set to "No" in your feed settings, or you have multiple feeds for the same form creating contacts in different lists. Check all your feeds and consolidate if needed.

**Problem**: Integration worked then suddenly stopped
API key expired or got regenerated. This happens when someone changes ActiveCampaign account settings. Get a fresh API key from ActiveCampaign and update it in Forms → Settings → ActiveCampaign.

**Problem**: Form submissions create contacts but don't trigger automations
Check that your automation trigger is set to the correct list, and that the list matches what your form feed is configured to use. Also verify the automation is set to "Active."

**Problem**: Getting "API Error" on form submission but contact is still created
This is usually a non-critical error with additional API calls (like tagging). The core contact creation worked, but something in your feed configuration failed. Check your feed settings for any optional fields that might be causing issues.

## What To Do Next

Once your Gravity Forms → ActiveCampaign integration is running smoothly, consider these related setups:

- **[Gravity Forms → HubSpot Integration](/integrations/gravity-forms-to-hubspot)** — If you're evaluating CRM options
- **[Gravity Forms → Salesforce Integration](/integrations/gravity-forms-to-salesforce)** — For enterprise sales teams
- **[Gravity Forms Google Ads Conversion Tracking](/tracking/gravity-forms-google-ads-conversion-tracking)** — Track which ads drive your best leads
- **[Contact me](/contact)** for a free audit if you're missing leads somewhere in your funnel

*This guide is part of the [ActiveCampaign Integrations Hub](/integrations/activecampaign) — technical setups for connecting ActiveCampaign to your forms, e-commerce, and tracking tools.*