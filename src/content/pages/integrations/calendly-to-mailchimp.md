---
title: "How to Send Calendly Leads to Mailchimp (Setup Guide)"
slug: "calendly-to-mailchimp"
description: "Connect Calendly to Mailchimp so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/mailchimp"
page_type: "spoke"
---

# Calendly → Mailchimp Integration Guide

I've seen this integration break in about 30% of Calendly setups I audit, usually because people set up the connection but never map the custom fields properly. You end up with contacts in Mailchimp but none of the qualifying information from your Calendly intake form — which makes follow-up emails completely generic.

The other issue? Most people use the basic Zapier connection without realizing Calendly has native webhook capabilities that are way more reliable for high-volume booking flows.

## What You'll Have Working By The End

- Every Calendly booking automatically creates or updates a contact in your target Mailchimp audience
- Custom intake form fields (company, revenue, pain points) flowing to Mailchimp tags or custom fields
- Automatic segmentation based on event type (demo calls vs. support calls)
- Backup tracking method in case your primary integration fails
- Test process to verify leads are flowing correctly

## Prerequisites

- [ ] Calendly Pro, Premium, or Teams account (required for webhooks and advanced field mapping)
- [ ] Mailchimp account with API access
- [ ] Admin access to both platforms
- [ ] At least one active Calendly event type with intake form questions configured
- [ ] Target Mailchimp audience already created

## Step 1: Set Up Native Calendly → Mailchimp Integration

Calendly has a native Mailchimp integration that's more reliable than Zapier for basic setups. Start here unless you need advanced field mapping.

In your Calendly admin:
1. Go to Integrations → Email Marketing → Mailchimp
2. Click "Connect" and authenticate with your Mailchimp account
3. Select your target audience (not a campaign — the actual subscriber list)
4. Configure field mapping:
   - **Email** → Email Address (auto-mapped)
   - **Name** → First Name + Last Name fields
   - **Phone** → Phone Number (if you collect it)
   - **Company** → COMPANY tag or custom field
   - **Event Type** → EVENT_TYPE tag

The native integration only supports basic field mapping. If you're collecting revenue, team size, or other qualifying data in your Calendly intake form, you'll need the Zapier method instead.

**Which should you use?** Native integration for simple setups (name, email, phone). Zapier if you need custom field mapping or advanced segmentation.

## Step 2: Alternative Method - Zapier Integration

This gives you much more control over field mapping and allows for complex workflows like adding different tags based on event type or sending different email sequences.

### Create the Zap
1. New Zap → Calendly as trigger app
2. Choose "Invitee Created" trigger (fires when someone books)
3. Connect your Calendly account and select your event type
4. Test the trigger with a real booking to see available fields

### Configure Mailchimp Action
1. Choose Mailchimp as action app
2. Select "Add/Update Subscriber" action
3. Map fields:
   - **Email** → `{{email}}`
   - **First Name** → `{{first_name}}`
   - **Last Name** → `{{last_name}}`
   - **Phone** → `{{phone_number}}`
   - **Tags** → Combine event name + custom responses

### Advanced Field Mapping
For Calendly intake form responses, you'll see them as `{{question_and_responses}}` in a JSON format. Use Zapier's formatter to parse these:

```
Calendly Response: "What's your company size?" → "50-100 employees"
Mailchimp Tag: COMPANY_SIZE_50_100
```

Set up a Formatter step to clean the responses into usable tags:
1. Add Formatter → Text → Replace
2. Replace spaces with underscores
3. Convert to uppercase
4. Prepend with category (COMPANY_SIZE_, BUDGET_, etc.)

## Step 3: Webhook + API Method (Advanced)

For high-volume booking flows or when you need real-time processing, webhooks are the most reliable option. This requires basic development work.

### Set Up Calendly Webhook
1. Calendly admin → Integrations → Webhooks
2. Add webhook URL (your server endpoint)
3. Select events: `invitee.created` and `invitee.canceled`
4. Save and note your webhook signing key

### Sample Webhook Handler (Node.js)
```javascript
app.post('/calendly-webhook', (req, res) => {
  const payload = req.body;
  
  if (payload.event === 'invitee.created') {
    const contact = {
      email_address: payload.payload.email,
      status: 'subscribed',
      merge_fields: {
        FNAME: payload.payload.first_name,
        LNAME: payload.payload.last_name,
        PHONE: payload.payload.phone_number
      },
      tags: [
        payload.payload.event_type.name.replace(/\s+/g, '_').toUpperCase(),
        'CALENDLY_LEAD'
      ]
    };
    
    // Add to Mailchimp via API
    addToMailchimp(contact);
  }
  
  res.status(200).send('OK');
});
```

### Process Custom Questions
Calendly webhooks include intake form responses in the `questions_and_responses` array:
```javascript
const responses = payload.payload.questions_and_responses;
responses.forEach(qa => {
  const tag = `${qa.question.replace(/[^a-zA-Z0-9]/g, '_')}_${qa.answer.replace(/[^a-zA-Z0-9]/g, '_')}`.toUpperCase();
  contact.tags.push(tag);
});
```

## Step 4: Set Up Tracking for Embedded Calendly

If you're embedding Calendly on your website and want to track bookings as conversions, add this JavaScript alongside your integration:

```javascript
window.addEventListener('message', function(e) {
  if (e.origin !== 'https://calendly.com') return;
  
  if (e.data.event === 'calendly.event_scheduled') {
    // Track conversion
    gtag('event', 'calendly_booking', {
      event_category: 'engagement',
      event_label: e.data.event_details.event_type_name
    });
    
    // Optional: Send to other tracking tools
    fbq('track', 'Lead');
  }
});
```

This lets you track Calendly bookings in Google Analytics alongside your Mailchimp integration.

## Testing & Verification

### Test the Integration
1. Book a test appointment using a unique email address
2. Complete the intake form with dummy data
3. Wait 2-3 minutes for processing
4. Check Mailchimp audience for the new contact

### Verify Field Mapping
Your test contact should have:
- ✅ Correct name and email
- ✅ Phone number (if collected)
- ✅ Tags for event type and custom responses
- ✅ Proper audience assignment

### Check Integration Health
Monitor these metrics weekly:
- **Calendly bookings** vs. **Mailchimp new contacts** (should be 1:1 ratio)
- **Failed webhook deliveries** in Calendly admin
- **API error rate** in Mailchimp reports

Acceptable variance is under 5%. If you're missing more than 5% of bookings, something's broken.

## Troubleshooting

**Problem** → Contacts appear in Mailchimp but without custom field data
**Solution** → Your field mapping is incorrect. Check that Calendly question names exactly match your Mailchimp field names. Spaces and special characters cause mapping failures.

**Problem** → Duplicate contacts being created for the same person
**Solution** → Mailchimp is matching on email address. Check that you're using "Add/Update Subscriber" not "Add Subscriber" in Zapier, or set `update_existing: true` in your API calls.

**Problem** → Integration works for some bookings but not others
**Solution** → Usually a timezone or scheduling conflict issue. Check that your webhook/Zapier trigger isn't filtering out certain event types. Also verify that incomplete bookings (no-shows who don't finish the form) aren't triggering the integration.

**Problem** → Webhook endpoint receiving data but Mailchimp API calls failing
**Solution** → Check your Mailchimp API key permissions and rate limits. Mailchimp allows 10 requests per second. If you're processing bulk bookings, add retry logic with exponential backoff.

**Problem** → Tags not appearing correctly in Mailchimp
**Solution** → Mailchimp tags can't contain spaces or special characters. Your formatter should convert "What's your budget?" → "WHATS_YOUR_BUDGET" before sending to the API.

**Problem** → Integration breaks when switching Calendly event types
**Solution** → Event type changes often reset webhook configurations. After modifying events, re-test your integration and update any hardcoded event type names in your Zapier filters or webhook handlers.

## What To Do Next

Once your Calendly → Mailchimp integration is flowing properly, set up these related integrations:

- **[Calendly → HubSpot](/integrations/calendly-to-hubspot)** — For full CRM functionality and deal tracking
- **[Calendly → Salesforce](/integrations/calendly-to-salesforce)** — Enterprise sales pipeline management
- **[Calendly → GoHighLevel](/integrations/calendly-to-gohighlevel)** — All-in-one marketing automation

You should also track Calendly bookings as conversion events: **[Calendly Google Ads Conversion Tracking](/tracking/calendly-google-ads-conversion-tracking)** — Essential if you're running paid traffic to your booking page.

**Need help auditing your current integration setup?** [Get a free tracking audit](/contact) — I'll check your Calendly → Mailchimp flow and identify any missed leads or broken field mapping.

*This guide is part of the [Mailchimp Integrations Hub](/integrations/mailchimp) — complete setup guides for connecting Mailchimp to every major form tool and CRM platform.*