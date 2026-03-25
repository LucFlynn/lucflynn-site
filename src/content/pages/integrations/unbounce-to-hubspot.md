---
title: "How to Send Unbounce Leads to HubSpot (Setup Guide)"
slug: "unbounce-to-hubspot"
description: "Connect Unbounce to HubSpot so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/hubspot"
page_type: "spoke"
---

# Unbounce → HubSpot Integration Guide

I see Unbounce-to-HubSpot integrations break in about 30% of the accounts I audit. Usually it's because someone set up a native integration months ago, then changed form fields without updating the field mappings, so half the lead data just disappears into the void. The client thinks their landing pages aren't converting when really their CRM just isn't receiving the leads.

The other common failure is using Zapier without error handling. Zapier fails silently about 2-3% of the time, so you lose leads without knowing it until you manually cross-check your numbers.

## What You'll Have Working By The End

- Every Unbounce form submission automatically creates a HubSpot contact
- Form fields mapped correctly (name, email, phone, custom fields, UTM parameters)
- Proper error handling so you know when integrations break
- Lead source attribution showing which Unbounce pages generated which contacts
- Testing workflow to verify submissions are reaching HubSpot

## Prerequisites

- [ ] Admin access to your Unbounce account
- [ ] Admin access to your HubSpot account (or Marketing Hub Professional/Enterprise)
- [ ] List of all form fields you want to capture
- [ ] HubSpot contact properties already created for any custom fields

## Method 1: Native HubSpot Integration

This is the most reliable option and what I recommend for 90% of setups. Unbounce has a direct integration with HubSpot that handles the heavy lifting.

### Set Up the Integration

In your Unbounce account:

1. Go to **Integrations** → **Connect Your Tools**
2. Find **HubSpot** and click **Connect**
3. Authorize Unbounce to access your HubSpot account
4. Select which HubSpot portal to connect to (if you have multiple)

Now configure it at the page level:

1. Open your Unbounce landing page in the builder
2. Click on your form element
3. Go to **Form Settings** → **Integrations**
4. Enable **HubSpot** and configure field mapping

### Field Mapping Setup

Map your Unbounce form fields to HubSpot contact properties:

**Standard Fields:**
- First Name → `firstname`
- Last Name → `lastname` 
- Email → `email`
- Phone → `phone`
- Company → `company`

**UTM Parameter Mapping:**
- UTM Source → `utm_source`
- UTM Medium → `utm_medium` 
- UTM Campaign → `utm_campaign`
- UTM Content → `utm_content`
- UTM Term → `utm_term`

**Custom Fields:**
If you have custom form fields (like "Budget Range" or "Project Timeline"), make sure you've already created the corresponding contact properties in HubSpot first. Go to **Settings** → **Properties** → **Contact Properties** in HubSpot to create them.

The integration will capture the page URL as `hs_landing_page` automatically.

## Method 2: Zapier Connection

Use this if you need more complex logic or data transformations that the native integration can't handle.

### Zapier Setup

1. Create a new Zap with **Unbounce** as the trigger
2. Choose **New Submission** as the trigger event
3. Connect your Unbounce account and select the specific page
4. Test the trigger by submitting your form

For the action:

1. Choose **HubSpot** as the action app
2. Select **Create/Update Contact** as the action event
3. Map the fields exactly like in Method 1
4. **Important**: Set up error handling in Zapier settings

### Error Handling Configuration

In your Zap settings, enable:
- **Error notifications** sent to your email
- **Auto-replay** for temporary failures
- **Filter** to exclude test submissions (add a condition to ignore submissions where email contains "test" or similar)

This is critical because Zapier fails silently by default. You won't know leads are being lost unless you set up notifications.

## Method 3: Webhook + API Approach

This is for developers who want full control over the integration logic. You'll set up a webhook in Unbounce that calls your own endpoint, which then uses HubSpot's API.

### Unbounce Webhook Setup

1. In your Unbounce page builder, click the form
2. Go to **Form Settings** → **Webhooks**
3. Add your webhook URL (e.g., `https://yourserver.com/unbounce-webhook`)
4. Select **POST** method
5. Configure the payload to include all form fields plus UTM parameters

### HubSpot API Integration

Your webhook endpoint needs to call HubSpot's Contacts API:

```javascript
// Example webhook handler (Node.js)
app.post('/unbounce-webhook', async (req, res) => {
  const formData = req.body;
  
  const hubspotPayload = {
    properties: {
      firstname: formData.first_name,
      lastname: formData.last_name,
      email: formData.email,
      phone: formData.phone,
      utm_source: formData.utm_source,
      utm_medium: formData.utm_medium,
      utm_campaign: formData.utm_campaign,
      hs_landing_page: formData.page_url
    }
  };
  
  try {
    const response = await axios.post(
      'https://api.hubapi.com/crm/v3/objects/contacts',
      hubspotPayload,
      {
        headers: {
          'Authorization': `Bearer ${HUBSPOT_ACCESS_TOKEN}`,
          'Content-Type': 'application/json'
        }
      }
    );
    
    console.log('Contact created:', response.data.id);
    res.status(200).send('OK');
  } catch (error) {
    console.error('HubSpot API error:', error.response.data);
    res.status(500).send('Error creating contact');
  }
});
```

You'll need to handle duplicate contacts by searching for existing emails first, then updating instead of creating.

## Testing & Verification

### Test the Integration

1. Submit a test form on your Unbounce page using a real email address
2. Check your integration method's logs:
   - **Native**: Look in Unbounce dashboard under Recent Submissions
   - **Zapier**: Check Zap History for successful runs
   - **Webhook**: Monitor your server logs

### Verify in HubSpot

1. Go to **Contacts** → **Contacts** in HubSpot
2. Search for your test email address
3. Open the contact record and verify:
   - All form fields populated correctly
   - UTM parameters captured
   - Original source shows "Offline sources"
   - Landing page URL captured

### Cross-Check Numbers

Pull submission counts from both systems:
- **Unbounce**: Dashboard shows total submissions per page
- **HubSpot**: Create a contact list filtered by "Original source = Offline sources" and Landing page contains your Unbounce domain

Acceptable variance is 2-5%. If you're seeing 10%+ variance, something is broken.

## Troubleshooting

**Problem**: Contacts created but missing custom field data  
→ Check that custom properties exist in HubSpot before form submission. Create the properties first, then resubmit a test form.

**Problem**: Duplicate contacts being created  
→ HubSpot uses email as the unique identifier. If your integration creates contacts instead of updating existing ones, you'll get duplicates. Switch to "Create or Update" logic.

**Problem**: Zapier stopped working and no error notification  
→ Zapier doesn't email you by default when zaps break. Go to your Zap settings and enable error notifications. Also check your usage limits.

**Problem**: UTM parameters not capturing  
→ Unbounce passes UTMs in the form submission data, but you need to explicitly map them to HubSpot UTM fields. Don't map them to custom properties - use the built-in UTM fields.

**Problem**: Integration works for some pages but not others  
→ The native Unbounce integration is configured per-page, not account-wide. Go into each landing page and enable the HubSpot integration separately.

**Problem**: Leads appearing with "Offline sources" instead of proper attribution  
→ This is normal for form integrations. HubSpot can't track the original ad click through Unbounce's direct submission. Set up [Unbounce Google Ads conversion tracking](/tracking/unbounce-google-ads-conversion-tracking) separately for attribution.

## What To Do Next

Once your Unbounce leads are flowing into HubSpot, consider setting up these related integrations:

- [Unbounce to Salesforce](/integrations/unbounce-to-salesforce) if you're using Salesforce as your primary CRM
- [Unbounce to GoHighLevel](/integrations/unbounce-to-gohighlevel) for all-in-one marketing automation  
- [Unbounce to ActiveCampaign](/integrations/unbounce-to-activecampaign) for email marketing workflows

Need help auditing your current Unbounce tracking setup? I'll review your integration configuration and find any missing leads. [Get a free tracking audit here](/contact).

*This guide is part of the [HubSpot Integrations Hub](/integrations/hubspot) — covering every major tool that connects to HubSpot CRM.*