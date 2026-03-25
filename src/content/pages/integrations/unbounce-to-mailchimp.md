---
title: "How to Send Unbounce Leads to Mailchimp (Setup Guide)"
slug: "unbounce-to-mailchimp"
description: "Connect Unbounce to Mailchimp so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/mailchimp"
page_type: "spoke"
---

# Unbounce → Mailchimp Integration Guide

I see this setup broken in about 60% of the Unbounce accounts I audit. The issue isn't that the integration is hard — it's that people either skip testing entirely or don't realize Mailchimp treats duplicate emails differently depending on how they're submitted. One misconfigured field and you're sending 300 leads to a "Test Audience" instead of your main list.

The other thing that trips people up is Unbounce's form system. Unlike most landing page builders, Unbounce has its own built-in form handler, but also lets you bypass it entirely with custom code. Most people don't realize which approach they're using until leads start going missing.

## What You'll Have Working By The End

- Every Unbounce form submission creates or updates a Mailchimp contact automatically
- Lead data flowing to the correct Mailchimp audience with proper field mapping
- Duplicate handling configured so returning visitors don't break your automation
- Test process to verify leads are arriving with all the data you expect
- Error monitoring so you know when the integration stops working

## Prerequisites

- [ ] Unbounce account with page editing permissions
- [ ] Mailchimp account with API access (all paid plans include this)
- [ ] Access to your Mailchimp audience ID and API key
- [ ] If using Zapier: Premium Zapier account (free tier won't handle webhook triggers reliably)

## Step 1: Choose Your Integration Method

Unbounce doesn't have a direct native integration with Mailchimp anymore (they removed it in 2023), so you've got three real options:

**Zapier connection** — Most reliable for non-technical teams. Handles retries automatically but costs $20/month minimum.

**Webhook + Mailchimp API** — Free but requires some technical setup. I use this for clients who run high-volume campaigns where Zapier costs add up.

**Direct API from form script** — Advanced option if you need real-time processing or custom logic.

For most setups, I recommend Zapier unless you're processing 5,000+ leads per month or need custom field transformations.

## Step 2: Set Up Zapier Integration (Recommended)

Log into Zapier and create a new Zap:

1. **Trigger: Unbounce → Form Submission**
   - Connect your Unbounce account
   - Select your specific landing page
   - Choose the form by name (if you have multiple forms on one page)

2. **Action: Mailchimp → Add/Update Subscriber**
   - Connect your Mailchimp account 
   - Select your audience (not a campaign — the audience where contacts live)
   - Set status to "subscribed" (unless you're doing double opt-in)

3. **Field Mapping:**
   ```
   Unbounce Field → Mailchimp Field
   Email → Email Address
   First Name → First Name
   Last Name → Last Name
   Phone → Phone Number
   Company → Organization (if using)
   ```

4. **Test the zap** with a real form submission before turning it on.

The key thing here: Mailchimp will reject the entire submission if you map a field that doesn't exist in your audience. Go to your Mailchimp audience settings and verify all your merge fields exist before mapping them.

## Step 3: Webhook Integration (Technical Alternative)

If you're going the webhook route, you'll need to set up both sides:

### Unbounce Webhook Configuration

1. In your Unbounce page editor, go to **Form → Integrations**
2. Add webhook URL: `https://your-webhook-handler.com/unbounce-mailchimp`
3. Select "POST" method
4. Test webhook to make sure it's receiving data

### Mailchimp API Handler

You'll need a server endpoint to receive the webhook and forward to Mailchimp. Here's the basic structure:

```javascript
// Example webhook handler (Node.js)
const mailchimp = require('@mailchimp/mailchimp_marketing');

mailchimp.setConfig({
  apiKey: 'your-api-key',
  server: 'us19' // Your server prefix
});

app.post('/unbounce-mailchimp', async (req, res) => {
  const { email, first_name, last_name, phone } = req.body;
  
  try {
    const response = await mailchimp.lists.addListMember('audience_id', {
      email_address: email,
      status: 'subscribed',
      merge_fields: {
        FNAME: first_name,
        LNAME: last_name,
        PHONE: phone
      }
    });
    
    res.status(200).json({ success: true });
  } catch (error) {
    console.error('Mailchimp API error:', error);
    res.status(500).json({ success: false });
  }
});
```

This approach gives you more control but requires hosting and maintenance.

## Step 4: Configure Advanced Field Mapping

Most people mess this up because Mailchimp's field names aren't obvious:

### Standard Mailchimp Merge Fields:
- `FNAME` = First Name
- `LNAME` = Last Name  
- `PHONE` = Phone Number
- `BIRTHDAY` = Birthday (MM/DD format)

### Custom Fields:
If you've created custom fields in Mailchimp, check their exact merge field tags in **Audience → Settings → Audience fields and *|MERGE|* tags**. 

Common mistake: Using the field label instead of the merge tag. If your field is called "Company Name" but the merge tag is `COMPANY`, use `COMPANY` in your integration.

### Unbounce Hidden Fields:
You can pass additional data by adding hidden fields to your Unbounce form:
- `utm_source`
- `utm_campaign` 
- `landing_page_url`
- `submission_date`

Map these to custom Mailchimp fields to track campaign performance.

## Step 5: Set Up Duplicate Handling

Mailchimp handles duplicate emails differently depending on how they arrive:

**Via API (or Zapier):** By default, it updates the existing contact with new field values. This is usually what you want.

**Via form integrations:** Some setups create a new contact every time, leading to duplicates.

In your Mailchimp integration settings:
1. Set update existing contacts to "Yes"
2. Choose which fields to update vs. preserve
3. Decide on tag behavior for returning subscribers

I typically configure it to update all fields except email preferences and subscription date.

## Step 6: Testing & Verification

Here's how to verify everything is working:

### Test Form Submission:
1. Fill out your Unbounce form with test data
2. Use a real email address you control
3. Include data in all mapped fields

### Verify in Mailchimp:
1. Check your audience for the new contact (can take 30-60 seconds)
2. Open the contact record and verify all fields populated correctly
3. Check the contact's activity timeline for the subscription event

### Cross-Check Integration Logs:
- **Zapier:** Check the Zap history for successful/failed runs
- **Webhook:** Monitor your server logs for incoming requests and API responses

### Volume Test:
Submit 10-15 test forms over a few minutes to make sure the integration doesn't break under load. I've seen webhooks fail when multiple submissions arrive simultaneously.

Acceptable processing time: Under 2 minutes from form submission to Mailchimp contact creation. If it's taking longer, something's wrong with the integration.

## Troubleshooting

**Problem:** Forms submit successfully but no contacts appear in Mailchimp
- Check if you're sending to the correct audience ID (not campaign ID)
- Verify your Mailchimp API key has write permissions to that audience
- Look for hard bounced emails — Mailchimp won't add them

**Problem:** Only email addresses arrive, other fields are blank
- Field mapping issue. Check that Unbounce form field names exactly match what you've mapped
- Verify custom Mailchimp merge fields exist and are spelled correctly
- Test with simple field names first (no spaces or special characters)

**Problem:** Integration worked initially but stopped processing leads
- Zapier: Check if your account is over its monthly task limit
- Webhook: Server might be down or API rate limits exceeded
- Mailchimp: API key could have expired or permissions changed

**Problem:** Getting duplicate contacts despite update settings
- Multiple integrations running simultaneously (Zapier + webhook)
- Email addresses have different formatting (spaces, cases)
- Check if you're creating contacts in multiple audiences accidentally

**Problem:** Webhook returns 400 error from Mailchimp
- Required field missing from the payload (email is always required)
- Invalid email format
- Audience ID doesn't exist or API key doesn't have access to it

**Problem:** Form fields not showing up in integration options
- Unbounce form fields need names, not just labels
- In form editor, click each field and set the "Field Name" property
- Wait a few minutes for integrations to recognize new fields

## What To Do Next

Once your basic integration is working, consider these improvements:

- Set up [Unbounce → HubSpot integration](/integrations/unbounce-to-hubspot) for more advanced CRM features
- Add [Google Ads conversion tracking](/tracking/unbounce-google-ads-conversion-tracking) to measure campaign performance
- Connect additional CRMs like [Salesforce](/integrations/unbounce-to-salesforce) or [GoHighLevel](/integrations/unbounce-to-gohighlevel)
- [Get a free tracking audit](/contact) to see what else might be broken in your setup

*This guide is part of the [Mailchimp Integration Hub](/integrations/mailchimp) — complete setup guides for connecting Mailchimp to every major marketing tool and CRM.*