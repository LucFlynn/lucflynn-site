---
title: "How to Send HubSpot Forms Leads to HubSpot (Setup Guide)"
slug: "hubspot-forms-to-hubspot"
description: "Connect HubSpot Forms to HubSpot so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/hubspot"
page_type: "spoke"
---

# HubSpot Forms → HubSpot Integration Guide

I see this question come up more often than you'd think — people assume HubSpot Forms automatically sync to HubSpot CRM, but that's not always the case depending on your setup. If you're embedding HubSpot forms on external sites or have a complex multi-domain setup, leads can slip through the cracks without proper configuration.

The good news? When set up correctly, this is one of the most reliable form → CRM integrations you can have. HubSpot's native tools handle 95% of the heavy lifting.

## What You'll Have Working By The End

- Every HubSpot form submission automatically creates or updates a contact in your HubSpot CRM
- Complete field mapping from form fields to contact properties
- Automatic lead source attribution and campaign tracking
- Workflow triggers that fire immediately when forms are submitted
- Proper duplicate handling that merges data instead of creating duplicates

## Prerequisites

- [ ] HubSpot account with CRM access (free tier works)
- [ ] Admin access to your HubSpot portal
- [ ] Access to edit forms in HubSpot
- [ ] If using external sites: ability to embed HubSpot tracking code
- [ ] If using Zapier: active Zapier account

## Step 1: Verify Your HubSpot Forms Are Connected

If you created your forms directly in HubSpot and they're hosted on HubSpot pages, they should already be connected to your CRM. But I've seen setups where this breaks, especially after portal migrations or domain changes.

**Check your current connection:**

1. Go to Marketing → Lead Capture → Forms in your HubSpot portal
2. Click on any form to edit it
3. Look for the "Options" tab
4. Under "What should happen after a visitor submits this form?" make sure it's not set to "Display a thank you message" only

**If the form isn't connected:**

1. In the form editor, go to Options
2. Set "Create contact" to "Always create contact for new email address" 
3. Under "Lifecycle stage," choose "Lead" (or whatever stage makes sense for your funnel)
4. Save the form

**For embedded forms on external sites:**

Make sure the HubSpot tracking code is installed on every page where you embed HubSpot forms. Without it, form submissions won't link to the contact timeline properly.

Add this to your site's `<head>` section:

```javascript
<!-- Start of HubSpot Embed Code -->
<script type="text/javascript" id="hs-script-loader" async defer src="//js.hs-scripts.com/YOUR-HUB-ID.js"></script>
<!-- End of HubSpot Embed Code -->
```

Replace `YOUR-HUB-ID` with your actual HubSpot portal ID (find this in Settings → Account Setup → Account Defaults).

## Step 2: Configure Contact Properties and Field Mapping

HubSpot automatically maps standard form fields (email, first name, last name, company, phone) to corresponding contact properties. But custom fields need manual mapping.

**Create custom contact properties for non-standard fields:**

1. Go to Settings → Properties → Contact properties
2. Click "Create property"
3. Match the internal name to your form field names exactly (this makes mapping automatic)
4. Set the field type to match your form field (single-line text, dropdown, etc.)

**Map form fields to properties:**

1. Edit your form in Marketing → Lead Capture → Forms
2. Click on each form field
3. In the right panel, check that "Contact property to store this in" is set correctly
4. For custom fields, select the property you just created

**Essential field mappings I always verify:**
- Email → Email (required for contact creation)
- First Name → First Name  
- Last Name → Last Name
- Company → Company name
- Phone → Phone number
- Lead Source → Lead source (for attribution)

## Step 3: Set Up Lead Source Tracking

This is where most people mess up — they get the contacts created but lose all attribution data about where the leads came from.

**Configure automatic lead source tracking:**

1. In your form editor, go to the Options tab
2. Enable "Set lifecycle stage" and choose "Lead"
3. Under "Contact properties to set," add these mappings:
   - Lead source = "Organic search" (or whatever's appropriate)
   - Original source = "Form submission"
   - First conversion = Form name
   - Recent conversion = Form name

**For campaign-specific tracking:**

Add hidden fields to your forms with UTM parameter values:

```javascript
// Add this to pages with HubSpot forms to capture UTM data
window.addEventListener('message', function(event) {
    if (event.data.type === 'hsFormCallback' && event.data.eventName === 'onFormReady') {
        // Populate hidden UTM fields
        const form = document.querySelector(`#${event.data.id}`);
        const utmSource = new URLSearchParams(window.location.search).get('utm_source');
        const utmCampaign = new URLSearchParams(window.location.search).get('utm_campaign');
        
        if (utmSource) {
            const sourceField = form.querySelector('input[name="utm_source"]');
            if (sourceField) sourceField.value = utmSource;
        }
        
        if (utmCampaign) {
            const campaignField = form.querySelector('input[name="utm_campaign"]');
            if (campaignField) campaignField.value = utmCampaign;
        }
    }
});
```

## Step 4: Configure Workflows and Notifications

Native HubSpot forms trigger workflows immediately upon submission — but only if you set them up correctly.

**Create a workflow for new form submissions:**

1. Go to Automation → Workflows
2. Click "Create workflow" → "Contact-based" → "Blank workflow"
3. Set enrollment trigger to "Contact has filled out [Your Form Name] on any page"
4. Add actions like:
   - Send internal notification email
   - Add to specific lists
   - Set contact owner
   - Create deal (if appropriate)

**Essential workflow I set up for every client:**

```
Trigger: Contact submits any form
Actions:
1. Set contact owner (based on lead source or territory)
2. Send slack/email notification to sales team
3. Add to "New Leads This Month" list
4. Wait 5 minutes (let other data populate)
5. Create deal if company size > 50 employees
```

## Step 5: Alternative Integration Methods

If native integration isn't working or you need more complex logic, here are backup approaches.

**Zapier Integration:**

1. In Zapier, create new zap: "HubSpot Forms" → "HubSpot CRM"
2. Connect your HubSpot account (use same account for both)
3. Choose "New Form Submission" as trigger
4. Select your specific form
5. For action, choose "Create or Update Contact"
6. Map fields manually in the Zapier interface

**Webhook + API Approach:**

For custom handling, set up a webhook in your form:

1. In form Options, enable "Redirect to external URL"
2. Set up webhook endpoint that receives form data
3. Use HubSpot API to create/update contacts:

```javascript
// Example webhook handler
const hubspot = require('@hubspot/api-client');

async function handleFormSubmission(formData) {
    const hubspotClient = new hubspot.Client({accessToken: 'YOUR_ACCESS_TOKEN'});
    
    const contactObj = {
        properties: {
            email: formData.email,
            firstname: formData.first_name,
            lastname: formData.last_name,
            company: formData.company,
            hs_lead_status: 'NEW'
        }
    };
    
    try {
        await hubspotClient.crm.contacts.basicApi.create(contactObj);
    } catch (error) {
        console.error('Failed to create contact:', error);
    }
}
```

## Testing & Verification

**Test the integration:**

1. Submit a test form with a unique email address (use yourname+test@domain.com)
2. Check that contact appears in HubSpot within 30 seconds
3. Verify all mapped fields populated correctly
4. Confirm workflow actions triggered (notifications, list additions)

**Monitor in real-time:**

1. Go to Contacts → All contacts
2. Filter by "Create date is today"
3. Look for your test submission
4. Check the contact timeline shows form submission activity

**Cross-check your numbers:**

- Form analytics (Marketing → Reports → Marketing) should match contact creation numbers
- Acceptable variance: 0-2% (HubSpot native integration is very reliable)
- If you're seeing 5%+ variance, something's broken

**Red flags that indicate problems:**

- Contacts created without lead source data
- Form submissions in analytics but no corresponding contacts
- Workflows not triggering consistently
- Duplicate contacts being created instead of merged

## Troubleshooting

**Problem → Forms submit but no contacts are created**

Check that your HubSpot tracking code is installed on the page hosting the form. Without it, HubSpot can't link the submission to your portal. Also verify the form is set to "Always create contact" in the Options tab.

**Problem → Contacts are created but workflows don't trigger**

Workflow enrollment criteria might be too specific. Change the trigger from "Contact has filled out [Specific Form]" to "Contact has filled out any form" and add a filter for the specific form name if needed.

**Problem → Duplicate contacts instead of merging**

HubSpot should automatically merge contacts with the same email address, but this fails if the email format doesn't match exactly. Check for extra spaces, different capitalization, or special characters. Also verify your deduplication settings in Settings → Properties → Contact properties → Email.

**Problem → Custom form fields aren't mapping**

The contact property internal name must match the form field name exactly. If your form field is "company_size" but the contact property is "companysize", the mapping fails. Edit either the form field name or the contact property internal name to match.

**Problem → Lead source data is missing**

Add hidden fields to your forms for utm_source, utm_medium, and utm_campaign, then map these to the corresponding contact properties. Without these, you lose all attribution data about where leads came from.

**Problem → Forms work on HubSpot pages but not on external sites**

The HubSpot tracking code isn't installed on your external site, or it's installed incorrectly. The tracking code must be in the `<head>` section and use your correct HubSpot portal ID. Also check that the form embed code includes the portal ID.

## What To Do Next

Once your HubSpot Forms are flowing into HubSpot CRM, consider these related integrations:

- [HubSpot Forms → Salesforce](/integrations/hubspot-forms-to-salesforce) if you're using Salesforce as your primary CRM
- [HubSpot Forms → GoHighLevel](/integrations/hubspot-forms-to-gohighlevel) for agencies managing multiple client funnels  
- [HubSpot Forms Google Ads Conversion Tracking](/tracking/hubspot-forms-google-ads-conversion-tracking) to close the loop on your ad spend
- [Contact me](/contact) for a free tracking audit if you're seeing data discrepancies

*This guide is part of the [HubSpot Integrations Hub](/integrations/hubspot) — your complete resource for connecting HubSpot to every tool in your marketing stack.*