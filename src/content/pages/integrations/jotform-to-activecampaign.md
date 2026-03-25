---
title: "How to Send Jotform Leads to ActiveCampaign (Setup Guide)"
slug: "jotform-to-activecampaign"
description: "Connect Jotform to ActiveCampaign so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/activecampaign"
page_type: "spoke"
---

# Jotform → ActiveCampaign Integration Guide

I see this integration broken in about 30% of the ActiveCampaign accounts I audit. Usually it's because someone set up the connection but never mapped the custom fields properly, or they're using the wrong automation trigger. The form submissions are coming through as "Unknown" contacts with empty deal records.

The good news? Jotform has solid native integration with ActiveCampaign, so you don't need to mess around with Zapier unless you want advanced field mapping or multi-step workflows.

## What You'll Have Working By The End

- Every Jotform submission automatically creates an ActiveCampaign contact
- Custom form fields map to your ActiveCampaign contact fields (name, email, phone, company, etc.)
- Deal records created automatically with form submission data
- Automation sequences triggered when leads come from specific forms
- Test process to verify submissions are flowing correctly

## Prerequisites

- [ ] Jotform account with form publishing rights
- [ ] ActiveCampaign account (any plan level works)
- [ ] Admin access to ActiveCampaign integrations
- [ ] Your ActiveCampaign API URL and key (found in Settings → Developer)

## Step 1: Set Up the Native Integration

The native integration is the most reliable option. I use this for 80% of my Jotform → ActiveCampaign setups.

In your Jotform builder:

1. Go to Settings → Integrations
2. Search for "ActiveCampaign" 
3. Click "Add Integration"
4. Enter your ActiveCampaign API URL (looks like: `https://youraccountname.api-us1.com`)
5. Enter your ActiveCampaign API key
6. Click "Authenticate"

Once connected, configure the integration:

1. **List Selection**: Choose which ActiveCampaign list receives these contacts
2. **Contact Fields**: Map your form fields to ActiveCampaign contact fields
   - Email field (required) → Email
   - First Name field → First Name  
   - Last Name field → Last Name
   - Phone field → Phone
   - Company field → Company (if you have this custom field)
3. **Deal Creation**: Enable "Create Deal" if you want deal records
4. **Deal Pipeline**: Select your pipeline and stage for new deals
5. **Double Opt-in**: Leave disabled unless you specifically need confirmed opt-ins

**Field Mapping Example:**
```
Jotform Field          →  ActiveCampaign Field
"Email Address"        →  Email
"First Name"           →  First Name  
"Last Name"            →  Last Name
"Phone Number"         →  Phone
"Company Name"         →  Company
"Message"              →  Notes (or custom field)
"Lead Source"          →  Lead Source (custom field)
```

Click "Save Integration" and you're done with the basic setup.

## Step 2: Configure Advanced Field Mapping

This is where most people screw it up. ActiveCampaign has specific field types, and if your mapping doesn't match, the data gets dropped.

**For Custom Fields in ActiveCampaign:**

1. Go to ActiveCampaign → Contacts → Manage Fields
2. Note the exact field names (case sensitive)
3. In Jotform integration settings, map to these exact field names
4. **Important**: Use the field NAME, not the label. If your custom field is labeled "Company Size" but named "company_size", use "company_size"

**Common Custom Fields to Set Up:**
- Lead Source (text field)
- Budget Range (dropdown or text)
- Timeline (text or date)
- Industry (dropdown)
- How They Found You (text)

**For Deal Fields:**
- Deal Title: Use a combination like "{First Name} {Last Name} - {Company}"
- Deal Value: Map to a form field or set a default value
- Deal Description: Map to your message/comments field

## Step 3: Set Up Automation Triggers

Here's how to trigger automations when Jotform leads come in:

1. Go to ActiveCampaign → Automations → Create New
2. Choose "Starts when a contact is added to a list"
3. Select the list you mapped in Step 1
4. Add condition: "Contact was added via Integration" → "Jotform"

**Pro tip**: Create different automations for different forms by using tags. In your Jotform integration, add a unique tag for each form (like "jotform-contact-page" or "jotform-pricing-inquiry").

## Step 4: Alternative Method - Zapier Integration

Use this if you need more complex field mapping or want to connect to multiple ActiveCampaign lists based on form responses.

**Zapier Setup:**

1. Create new Zap: Jotform (trigger) → ActiveCampaign (action)
2. **Trigger**: "New Submission" in Jotform
3. Select your specific form
4. **Action**: "Create/Update Contact" in ActiveCampaign
5. Map fields exactly like the native integration
6. **Additional Action** (optional): "Create Deal" in ActiveCampaign

**When to Use Zapier Instead:**
- You need conditional logic (different lists based on form responses)
- You want to create multiple records (contact + deal + task)
- You need data formatting (like splitting full name into first/last)
- You want to delay the contact creation

**Zapier Field Mapping:**
```
Email: {Email Address}
First Name: {First Name}
Last Name: {Last Name} 
Phone: {Phone Number}
Company: {Company Name}
Tags: jotform-lead,website-contact
```

## Step 5: Webhook Method (Advanced)

Only use this if you need real-time processing or want to add custom logic between Jotform and ActiveCampaign.

**Set up Webhook in Jotform:**

1. Settings → Integrations → Webhook
2. Webhook URL: Your server endpoint that processes the data
3. Set to POST method
4. Enable "Send Full Submission Data"

**Sample webhook processing code (PHP):**
```php
<?php
$submissionData = json_decode(file_get_contents('php://input'), true);

$ac_contact = [
    'email' => $submissionData['q3_email'],
    'first_name' => $submissionData['q1_firstName'],
    'last_name' => $submissionData['q2_lastName'],
    'phone' => $submissionData['q4_phone'],
    'fieldValues' => [
        ['field' => 'COMPANY', 'value' => $submissionData['q5_company']]
    ]
];

// Send to ActiveCampaign API
$ch = curl_init('https://youraccountname.api-us1.com/api/3/contacts');
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode(['contact' => $ac_contact]));
curl_setopt($ch, CURLOPT_HTTPHEADER, ['Api-Token: YOUR_API_KEY']);
curl_exec($ch);
?>
```

## Testing & Verification

**Test in Jotform:**
1. Submit your form with real test data (use your own email)
2. Check Jotform submissions to confirm it recorded
3. Wait 2-3 minutes for processing

**Verify in ActiveCampaign:**
1. Go to Contacts and search for your test email
2. Check that all mapped fields populated correctly
3. If you enabled deal creation, verify the deal exists in your pipeline
4. Check that any automation triggered properly

**Cross-Check the Numbers:**
- Compare Jotform submission count to ActiveCampaign contact creation count
- Acceptable variance: 5-10% (some submissions fail due to duplicate emails or validation issues)
- **Red flag**: If more than 15% of submissions aren't creating contacts, something's broken

**Real-Time Testing:**
Submit form → immediately check ActiveCampaign. Native integration typically processes within 30-60 seconds. If it takes longer than 5 minutes, check your API credentials.

## Troubleshooting

**Problem**: Submissions show in Jotform but no contacts in ActiveCampaign
**Solution**: Check your API credentials. Go to ActiveCampaign Settings → Developer and regenerate your API key. Re-authenticate in Jotform.

**Problem**: Contacts created but all custom fields are empty
**Solution**: Field name mismatch. In ActiveCampaign, go to Contacts → Manage Fields and copy the exact field names (not labels). Update your Jotform field mapping to use these exact names.

**Problem**: Getting duplicate contacts for same email address
**Solution**: This is normal ActiveCampaign behavior. The integration updates existing contacts rather than creating duplicates. If you're seeing true duplicates, check if you have multiple integrations running.

**Problem**: Deals not being created even though contacts are
**Solution**: Check your deal pipeline permissions. Go to ActiveCampaign Settings → Deal Pipelines and ensure the API has permission to create deals in your selected pipeline.

**Problem**: Automation not triggering for Jotform leads
**Solution**: Your automation trigger is probably too broad. Use "Contact is added to list" AND "Contact has tag" (set a unique tag in your Jotform integration). This ensures only Jotform leads trigger the automation.

**Problem**: Form fields showing as "undefined" in ActiveCampaign
**Solution**: Jotform sends field data as q1_fieldname, q2_fieldname, etc. If using webhooks, map the actual question IDs, not the field labels.

## What To Do Next

Now that your Jotform leads are flowing into ActiveCampaign, here's what to set up next:

- **Track Form Conversions**: Set up [Jotform Google Ads conversion tracking](/tracking/jotform-google-ads-conversion-tracking) to measure your form performance
- **Expand Your CRM Setup**: Connect other lead sources with our [ActiveCampaign integrations guide](/integrations/activecampaign)
- **Compare CRM Options**: See how this compares to [Jotform → HubSpot](/integrations/jotform-to-hubspot) or [Jotform → Salesforce](/integrations/jotform-to-salesforce) setups
- **Get a Free Audit**: I'll review your entire lead tracking setup and find what's broken — [book your free audit call](/contact)

*This guide is part of the [ActiveCampaign Integrations Hub](/integrations/activecampaign) — complete guides for connecting your lead sources, tracking tools, and automation workflows.*