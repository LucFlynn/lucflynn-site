---
title: "How to Send Typeform Leads to Zoho CRM (Setup Guide)"
slug: "typeform-to-zoho"
description: "Connect Typeform to Zoho CRM so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/zoho"
page_type: "spoke"
---

# Typeform → Zoho CRM Integration Guide

I see this setup requested a lot, and honestly, about 60% of the time it's configured wrong. The leads are either going to the wrong module (Contacts instead of Leads), missing critical fields, or worse — creating duplicates every time someone fills out the form twice. Here's how to actually make Typeform and Zoho CRM talk to each other properly.

## What You'll Have Working By The End

- Every Typeform submission automatically creates a lead in Zoho CRM
- Proper field mapping so nothing gets lost in translation
- Duplicate prevention so you don't spam your sales team
- Error handling that catches failed submissions
- A testing workflow to verify everything's working before you go live

## Prerequisites

- [ ] Typeform Pro account (webhooks require paid plan)
- [ ] Zoho CRM account with API access
- [ ] Admin access to both platforms
- [ ] A test form you can submit without consequences

## Step 1: Choose Your Integration Method

You've got three realistic options here. Skip the native integration — Typeform and Zoho don't have one that's worth using.

**Zapier (Recommended for most setups)**: Easiest to configure, handles errors gracefully, costs about $20/month for most volumes.

**Webhook + API (For developers)**: More control, no monthly fee after setup, but you're building the error handling yourself.

**Make.com**: Similar to Zapier but cheaper. Interface is more complex but the price point is better for high-volume forms.

For this guide, I'll cover Zapier first since it's what 80% of my clients end up using, then the webhook approach for the technical folks.

## Step 2: Set Up the Zapier Connection

Create a new Zap with Typeform as the trigger and Zoho CRM as the action.

**Typeform Trigger Setup:**
1. Select "New Entry" as the trigger event
2. Connect your Typeform account
3. Choose your specific form from the dropdown
4. Test the trigger by submitting your form once

**Zoho CRM Action Setup:**
1. Select "Create Lead" as the action (not "Create Contact" — that's a different module)
2. Connect your Zoho CRM account
3. Map the fields correctly (this is where most people mess up):

```
Typeform Field → Zoho CRM Field
Email → Email
Name → Last Name (required field in Zoho)
Company → Company
Phone → Phone
Message → Description
```

**Critical field mapping notes:**
- Zoho requires Last Name for leads. If your form only collects full name, use Zapier's formatter to split it
- Map the largest text field to Description — that's where detail responses should go
- Don't map to custom fields unless you've already created them in Zoho
- Leave Lead Source as "Web Form" or create a custom source called "Typeform"

## Step 3: Configure Duplicate Prevention

In the Zapier action settings, enable "Find or Create Lead" instead of just "Create Lead". Set the search field to Email — this prevents duplicate leads when someone submits multiple times.

Set the search logic to:
- If lead with this email exists: Update the existing record
- If no lead exists: Create new lead

This alone will save your sales team from 20-30% duplicate cleanup work.

## Step 4: Webhook + API Setup (Advanced)

If you're going the custom route, here's the setup:

**In Typeform:**
1. Go to your form's Connect panel
2. Add a webhook endpoint: `https://yourdomain.com/typeform-webhook`
3. Select "New submission" as the trigger

**Webhook payload structure:**
```json
{
  "event_id": "123456789",
  "event_type": "form_response",
  "form_response": {
    "form_id": "your_form_id",
    "submitted_at": "2024-01-15T10:30:00Z",
    "answers": [
      {
        "field": {
          "id": "field_id",
          "type": "short_text"
        },
        "text": "John Doe"
      }
    ]
  }
}
```

**Zoho CRM API call:**
```javascript
const createLead = async (formData) => {
  const response = await fetch('https://www.zohoapis.com/crm/v2/Leads', {
    method: 'POST',
    headers: {
      'Authorization': `Zoho-oauthtoken ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      data: [{
        'Last_Name': formData.name,
        'Email': formData.email,
        'Company': formData.company || 'Unknown',
        'Phone': formData.phone,
        'Description': formData.message,
        'Lead_Source': 'Typeform'
      }]
    })
  });
  
  return response.json();
};
```

Handle the OAuth token refresh — Zoho tokens expire every hour. Most integrations break because people forget this part.

## Step 5: Set Up Error Notifications

**For Zapier users:**
Enable email notifications for failed Zaps. Set up a filter that emails you when a Zap fails more than 3 times in a day.

**For webhook users:**
Log failed API calls and set up monitoring. Here's a simple error handler:

```javascript
const handleWebhook = async (req, res) => {
  try {
    const result = await createLead(req.body);
    if (result.data[0].status === 'error') {
      // Log error and notify
      console.error('Zoho API error:', result.data[0].message);
      notifyAdmin(result.data[0].message);
    }
    res.status(200).send('OK');
  } catch (error) {
    console.error('Webhook error:', error);
    res.status(500).send('Error');
  }
};
```

## Testing & Verification

Submit a test form with obvious fake data (email like test@test.com, name like "Test User"). Then verify:

1. **In Zapier**: Check the task history — did it show successful completion?
2. **In Zoho CRM**: Look for the lead in the Leads module. Check that all fields populated correctly.
3. **Field accuracy**: Verify the email went to Email field, not Description. This is surprisingly common.
4. **Duplicate test**: Submit the same form twice. The second submission should update the existing lead, not create a new one.

**Acceptable variance**: You should see 100% of test submissions in Zoho within 2-3 minutes. Anything less means something's broken.

**Red flags:**
- Leads appearing in Contacts instead of Leads module
- Empty required fields (Last Name showing as blank)
- New leads created every time instead of updating existing ones
- Submissions from 2+ minutes ago not appearing in Zoho

## Troubleshooting

**Problem**: Zap fails with "Required field missing" error  
**Solution**: Zoho requires Last Name for leads. If your form only collects full name, add a Zapier formatter step to split the name, or map the full name to Last Name field.

**Problem**: Leads going to Contacts module instead of Leads  
**Solution**: In your Zapier action, make sure you selected "Create Lead" not "Create Contact". These are different modules in Zoho and most people pick the wrong one.

**Problem**: Webhook receiving submissions but no leads appearing in Zoho  
**Solution**: Check your OAuth token — it probably expired. Zoho tokens last 1 hour. Implement proper token refresh or you'll get authentication errors.

**Problem**: Multiple leads created for same person  
**Solution**: Enable "Find or Create Lead" in Zapier, or implement duplicate checking in your webhook code. Search by email before creating new leads.

**Problem**: Custom fields not populating  
**Solution**: Custom fields in Zoho need to be created first, then you can map to them. You can't create fields through the API — they have to exist in your CRM setup already.

**Problem**: Zap works in test but fails on live submissions  
**Solution**: Usually a field mapping issue. Live submissions often have different data types (empty fields, longer text) than your test data. Add error handling for empty required fields.

## What To Do Next

Now that your Typeform leads are flowing into Zoho, you might want to set up [Typeform Google Ads conversion tracking](/tracking/typeform-google-ads-conversion-tracking) so you know which campaigns are driving your best leads. You can also explore other Typeform integrations like [Typeform to HubSpot](/integrations/typeform-to-hubspot) if you're considering switching CRMs.

If you're running into issues with this integration or want to set up tracking for your other lead sources, [contact me for a free audit](/contact) — I'll take a look at your setup and tell you what's broken.

*This guide is part of the [Zoho CRM Integration Hub](/integrations/zoho) — complete setup guides for connecting Zoho CRM to your lead sources and tracking tools.*