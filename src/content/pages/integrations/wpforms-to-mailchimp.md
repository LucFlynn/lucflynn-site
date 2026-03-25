---
title: "How to Send WPForms Leads to Mailchimp (Setup Guide)"
slug: "wpforms-to-mailchimp"
description: "Connect WPForms to Mailchimp so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/mailchimp"
page_type: "spoke"
---

# WPForms → Mailchimp Integration Guide

I see this integration requested in about 60% of WordPress lead gen setups I audit. WPForms makes it relatively painless, but most people skip the field mapping step and end up with incomplete contact records. Then they wonder why their email campaigns aren't converting.

The good news: WPForms has a native Mailchimp addon that handles 90% of use cases without touching code.

## What You'll Have Working By The End

- Every WPForms submission automatically creates or updates a Mailchimp contact
- Custom field data (phone, company, lead source) properly mapped to Mailchimp fields
- Tag-based segmentation so you know which forms generated which leads
- Duplicate handling that updates existing contacts instead of creating errors
- Testing workflow to verify new submissions are reaching Mailchimp correctly

## Prerequisites

- [ ] WPForms Pro license (the Mailchimp addon requires Pro)
- [ ] WordPress admin access to install/configure plugins
- [ ] Mailchimp account with API key access
- [ ] At least one Mailchimp audience/list already created
- [ ] Custom fields created in Mailchimp if you need them (phone, company, etc.)

## Step 1: Install the WPForms Mailchimp Addon

The native integration is your best bet here. I've seen it handle 50,000+ submissions per month without issues.

In your WordPress admin:
1. Go to **WPForms → Addons**
2. Find "Mailchimp" and click **Install Addon**
3. Once installed, click **Activate Addon**

If you don't see the Mailchimp addon, you're likely on WPForms Lite. The Mailchimp integration requires a Pro license.

## Step 2: Connect WPForms to Your Mailchimp Account

1. Navigate to **WPForms → Settings → Integrations**
2. Click the **Mailchimp** tab
3. Click **Connect to Mailchimp**
4. You'll be redirected to Mailchimp to authorize the connection
5. After authorization, you'll see "Connected" status in WPForms

**Alternative API Key Method:**
If the OAuth redirect isn't working (happens with some hosting setups):
1. Get your Mailchimp API key from **Account → Extras → API Keys**
2. In WPForms, click **Manually Enter API Key**
3. Paste your API key and click **Connect**

## Step 3: Configure Mailchimp Integration on Your Form

This is where most people mess up the field mapping. Take your time here.

1. Edit your WPForms form (**Forms → [Your Form] → Edit**)
2. Go to **Settings → Marketing → Mailchimp**
3. **Enable Mailchimp integration** toggle
4. Select your **Mailchimp List/Audience**
5. **Map your form fields:**

**Essential Field Mapping:**
- Email Address: Map to your email field (obviously)
- First Name: Map to your first name field
- Last Name: Map to your last name field

**Custom Field Mapping:**
If you collect phone, company, etc., you need custom fields in Mailchimp first:
- Go to your Mailchimp audience → **Settings → Audience fields and |MERGE| tags**
- Create custom fields with these exact types:
  - Phone: Text field
  - Company: Text field
  - Lead Source: Text field
- Back in WPForms, map these to your corresponding form fields

**Tags for Form Identification:**
Add a tag to identify which form generated the lead:
- **Tags** field: Enter something like "contact-form" or "homepage-lead"
- This lets you segment by form source in Mailchimp campaigns

## Step 4: Set Up Double Opt-in (Important)

Most people skip this and wonder why their deliverability sucks.

In the Mailchimp integration settings:
- **Double Opt-in**: Leave enabled unless you have a specific reason to disable
- **Update Existing Subscribers**: Enable this to update existing contacts instead of creating duplicates
- **Replace Interest Groups**: Usually leave disabled unless you're managing complex segmentation

**When to disable double opt-in:**
- B2B forms where you need immediate follow-up
- Forms that already include explicit consent language
- Internal lead forms (not public-facing)

## Step 5: Test the Integration

Don't skip this. I've seen "working" integrations that haven't sent a lead in months.

**Test Submission:**
1. Submit your form with real data (use a test email you control)
2. Check **WPForms → Entries** to confirm the submission recorded
3. Check your Mailchimp audience for the new contact
4. Verify all custom fields populated correctly
5. Confirm the tag was applied

**Check Integration Logs:**
1. Go to **WPForms → Tools → Logs**
2. Look for Mailchimp-related entries
3. Any errors will show here with specific failure reasons

## Testing & Verification

**Verify in WPForms:**
- New submissions appear in **Forms → [Your Form] → Entries**
- No error messages in the entry details
- Integration status shows "Completed" for Mailchimp

**Verify in Mailchimp:**
- Contact appears in the correct audience
- All mapped fields contain the expected data
- Tags are applied correctly
- Activity shows "Added via WPForms" or similar

**Cross-Check Numbers:**
- WPForms entries count should match Mailchimp new contacts (minus any that were already subscribers)
- Acceptable variance: 2-5% due to spam submissions or validation failures

**Red Flags:**
- No new contacts in Mailchimp after confirmed form submissions
- Contacts missing custom field data
- Multiple duplicate contacts for the same email
- Integration logs showing repeated API errors

## Troubleshooting

**Problem:** Form submissions aren't reaching Mailchimp at all
Check your API connection in **WPForms → Settings → Integrations → Mailchimp**. If it shows "Disconnected," re-authenticate. Also check if your Mailchimp account has been suspended or if you've hit API rate limits.

**Problem:** Contacts are created but custom fields are empty
Your Mailchimp custom fields probably don't match the field types WPForms expects. Go to your Mailchimp audience settings and ensure custom fields are set as "Text" type, not "Number" or "Date" unless specifically needed.

**Problem:** Getting duplicate contacts instead of updates
Enable "Update Existing Subscribers" in your form's Mailchimp settings. If still creating dupes, check that you're using the exact same email format (some forms add extra spaces or formatting).

**Problem:** Integration worked then stopped
Check **WPForms → Tools → Logs** for recent errors. Common causes: Mailchimp API key expired, audience was deleted/archived, or you hit Mailchimp's contact limits. Also verify the form's Mailchimp integration is still enabled.

**Problem:** Form submissions show errors about "invalid resource"
Your selected Mailchimp list/audience was probably deleted or archived. Edit your form's Mailchimp settings and select a different active audience.

**Problem:** Double opt-in emails aren't sending
Check your Mailchimp audience settings. If double opt-in is disabled at the audience level, WPForms can't override it. Also verify your Mailchimp sending domain is properly authenticated.

## Alternative: Zapier Integration

If you need more complex logic or the native integration isn't cutting it:

1. Create a Zapier account and new Zap
2. **Trigger:** WPForms → New Form Entry
3. Connect your WordPress site (you'll need the Zapier addon for WPForms)
4. **Action:** Mailchimp → Add/Update Subscriber
5. Map fields between WPForms and Mailchimp
6. Add filters/formatting as needed

**Zapier Benefits:**
- More complex field mapping options
- Conditional logic (only add certain types of leads)
- Multi-step workflows (add to Mailchimp AND your CRM)

**Zapier Drawbacks:**
- Costs money after the free tier
- Slight delay (usually 1-15 minutes)
- Another point of failure in your stack

## What To Do Next

Once your WPForms → Mailchimp integration is working:

- Set up [WPForms conversion tracking for Google Ads](/tracking/wpforms-google-ads-conversion-tracking) to measure which campaigns drive form submissions
- Consider connecting WPForms to a proper CRM like [HubSpot](/integrations/wpforms-to-hubspot) or [GoHighLevel](/integrations/wpforms-to-gohighlevel) for better lead management
- Explore other [Mailchimp integrations](/integrations/mailchimp) to centralize your lead sources

Need help auditing your current setup? I'll review your WPForms → Mailchimp integration and identify any gaps for free → [Get your free audit](/contact)

*This guide is part of the [Mailchimp Integrations Hub](/integrations/mailchimp) — covering how to connect your lead sources to Mailchimp for automated email marketing.*