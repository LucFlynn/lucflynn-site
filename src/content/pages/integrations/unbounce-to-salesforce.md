---
title: "How to Send Unbounce Leads to Salesforce (Setup Guide)"
slug: "unbounce-to-salesforce"
description: "Connect Unbounce to Salesforce so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/salesforce"
page_type: "spoke"
---

# Unbounce → Salesforce Integration Guide

Your Unbounce forms are converting, but you're manually copying leads into Salesforce. I see this in about 30% of landing page setups I audit — especially with agencies running multiple campaigns where manual lead entry becomes impossible to scale.

The disconnect happens because Unbounce operates as its own ecosystem with unique form handling, and Salesforce expects data in specific object formats. Without proper integration, you're either losing leads or spending hours on data entry.

## What You'll Have Working By The End

- Every Unbounce form submission automatically creates a Salesforce Lead
- Form fields correctly mapped to Salesforce Lead fields (including custom fields)
- Failed submissions logged and retried (no lost leads)
- Test form working so you can verify the connection before going live
- Lead source attribution showing "Unbounce" or your specific campaign name

## Prerequisites

- [ ] Unbounce account with form-building permissions
- [ ] Salesforce account with Lead creation permissions
- [ ] Salesforce System Administrator access (for Web-to-Lead setup)
- [ ] API access enabled in Salesforce (for webhook approach)
- [ ] List of required fields in your Salesforce Lead object

## Step 1: Choose Your Integration Method

I'll cover three approaches in order of reliability:

**Salesforce Web-to-Lead** (recommended for most setups): Native Salesforce feature, handles up to 500 leads/day, free, built-in duplicate detection.

**Zapier/Make** (best for complex field mapping): Third-party automation, costs $20+/month, handles complex logic and multiple objects.

**Direct Webhook + API** (for high-volume): Custom development required, unlimited volume, full control over error handling.

For most landing page campaigns, I start with Web-to-Lead unless you're processing 500+ leads daily or need complex lead routing.

## Step 2: Set Up Salesforce Web-to-Lead

In Salesforce, go to Setup → Web-to-Lead:

1. Click "Create Web-to-Lead Form"
2. Select your required fields (minimum: Last Name, Company, Email)
3. Add any custom fields you're capturing in Unbounce
4. Set the Return URL to your Unbounce thank-you page
5. Generate the HTML code

Salesforce gives you an HTML form that looks like this:

```html
<form action="https://webto.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8" method="POST">
<input type="hidden" name="oid" value="00D000000000000">
<input type="hidden" name="retURL" value="http://your-thanks-page.html">

<label for="first_name">First Name</label>
<input id="first_name" maxlength="40" name="first_name" size="20" type="text" />

<label for="last_name">Last Name</label>
<input id="last_name" maxlength="80" name="last_name" size="20" type="text" />

<label for="email">Email</label>
<input id="email" maxlength="80" name="email" size="20" type="text" />

<input type="submit" name="submit">
</form>
```

Copy the `oid` value and field names — you'll need these for Unbounce.

## Step 3: Configure Unbounce Form Integration

In Unbounce, edit your landing page and select your form:

1. Go to Form Behavior → Integrations
2. Choose "Webhook" or "Form Action URL"
3. Set the Action URL to: `https://webto.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8`
4. Set Method to POST
5. Add hidden field: `oid` with your Salesforce organization ID

**Field Mapping** (critical step):
Your Unbounce field names must match Salesforce's expected names:

- Unbounce "First Name" → `first_name`
- Unbounce "Last Name" → `last_name` 
- Unbounce "Email Address" → `email`
- Unbounce "Company Name" → `company`
- Unbounce "Phone Number" → `phone`

In Unbounce's form builder, click each field and update the "Name" property to match Salesforce's expected field names exactly.

For custom fields, Salesforce uses format like `00N5000000DjFGD` — get these from your Web-to-Lead form code.

## Step 4: Alternative Setup Using Zapier

If Web-to-Lead feels limiting, Zapier handles more complex scenarios:

1. Create new Zap: Unbounce → Salesforce
2. Select "New Form Submission" as Unbounce trigger
3. Choose your Unbounce page and form
4. Test the trigger with a sample submission

For the Salesforce action:
1. Choose "Create Lead in Salesforce"
2. Connect your Salesforce account
3. Map fields:
   - First Name: `{{First Name}}`
   - Last Name: `{{Last Name}}`
   - Email: `{{Email}}`
   - Company: `{{Company}}`
   - Lead Source: Set to "Unbounce" or your campaign name

**Advanced Zapier Setup**: Add a Filter step to prevent duplicate leads by checking if email already exists. Add a Formatter step to clean phone numbers or standardize company names.

I use this approach when clients need leads in both Leads and Contacts objects, or when they're doing complex lead scoring based on form responses.

## Step 5: Set Up Lead Source Tracking

This is where most setups fail — you get the leads but lose attribution.

**For Web-to-Lead**: Add hidden field to your Unbounce form:
- Field Name: `lead_source`
- Default Value: "Unbounce Landing Page" or specific campaign name

**For Zapier**: Set Lead Source field manually in the Salesforce action to track campaign performance.

I also add UTM parameters as hidden fields when possible:
- `00N5000000DjFGD` (custom field for UTM Source)  
- `00N5000000DjFGE` (custom field for UTM Campaign)

This lets you track which ads are driving the best leads, not just which landing pages.

## Testing & Verification

Before going live, test the complete flow:

1. **Submit test form**: Use a unique email like test+[timestamp]@yourcompany.com
2. **Check Unbounce**: Verify submission appears in Unbounce's Leads dashboard
3. **Check Salesforce**: Look for new Lead with your test email
4. **Verify field mapping**: All form fields should populate correct Lead fields
5. **Test redirect**: Ensure thank-you page loads after submission

**Numbers to watch**: Web-to-Lead typically processes submissions within 60 seconds. Zapier takes 2-15 minutes depending on your plan.

**Red flags**:
- Form submits but no Salesforce lead created
- Lead created but missing required fields
- Multiple leads created for same submission
- Thank-you page doesn't load (breaks conversion tracking)

## Troubleshooting

**Problem**: Form submits successfully but no lead appears in Salesforce
**Solution**: Check your organization ID (`oid`) is correct. Verify your Web-to-Lead daily limit isn't exceeded (500/day). Check if leads are going to a queue you can't see.

**Problem**: Leads created but missing form data
**Solution**: Field name mismatch. Unbounce field names must exactly match Salesforce API names. Check for extra spaces or capitalization differences.

**Problem**: Duplicate leads being created
**Solution**: Enable duplicate rules in Salesforce Setup. Or add email uniqueness check in Zapier before creating lead.

**Problem**: Zapier showing "Failed" status
**Solution**: Check required fields are mapped. Salesforce often requires Company field even if not obvious. Verify Salesforce connection hasn't expired.

**Problem**: Leads appearing as "Website" source instead of "Unbounce"
**Solution**: Add lead_source hidden field to your form with explicit value, or set it in your integration tool.

**Problem**: Integration works in test but fails with real traffic
**Solution**: Check Web-to-Lead daily limits. High-traffic pages hit the 500/day limit fast. Switch to API-based solution for volume over 500 daily submissions.

## What To Do Next

Once your Unbounce → Salesforce integration is working, set up these related connections:

- [Unbounce to HubSpot](/integrations/unbounce-to-hubspot) — Alternative CRM approach with built-in marketing automation
- [Unbounce Google Ads Conversion Tracking](/tracking/unbounce-google-ads-conversion-tracking) — Track which ads drive leads, not just form submissions
- [Unbounce to GoHighLevel](/integrations/unbounce-to-gohighlevel) — All-in-one CRM and marketing automation
- [Contact us](/contact) for a free audit of your current tracking setup — I'll identify gaps in your lead attribution that are costing you money

*This guide is part of the [Salesforce Integrations Hub](/integrations/salesforce) — complete guides for connecting every major marketing tool to Salesforce automatically.*