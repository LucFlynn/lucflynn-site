---
title: "How to Send Calendly Leads to ActiveCampaign (Setup Guide)"
slug: "calendly-to-activecampaign"
description: "Connect Calendly to ActiveCampaign so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/activecampaign"
page_type: "spoke"
---

# Calendly → ActiveCampaign Integration Guide

I see broken Calendly → ActiveCampaign integrations in about 30% of the accounts I audit. Usually it's missed appointments that never made it to ActiveCampaign, or duplicate contacts getting created because the integration wasn't set up to handle existing contacts properly.

The most common failure point? People set up the integration but don't map the custom fields correctly, so all the qualification data from their booking form just disappears into the void.

## What You'll Have Working By The End

- Every Calendly booking automatically creates or updates a contact in ActiveCampaign
- Custom booking form fields mapped to ActiveCampaign custom fields  
- Automated follow-up sequences triggered when someone books
- Test process to verify leads are flowing correctly
- Error handling for when the integration breaks

## Prerequisites

- [ ] Admin access to your Calendly account (need webhook/integration permissions)
- [ ] Admin access to your ActiveCampaign account
- [ ] API key from ActiveCampaign (under Settings → Developer)
- [ ] Zapier account (for Method 2) OR development resources (for Method 3)
- [ ] Custom fields already created in ActiveCampaign if you need them

## Method 1: Native ActiveCampaign Integration

Calendly has a direct integration with ActiveCampaign that handles the basic contact creation. This is the cleanest approach for most setups.

Go to your Calendly Integrations page (`calendly.com/integrations`) and search for ActiveCampaign. Click "Connect" and you'll be prompted to enter:

- **ActiveCampaign Account URL**: Your ActiveCampaign subdomain (e.g., `yourcompany.activehosted.com`)
- **API Key**: Found in ActiveCampaign under Settings → Developer → API Access

Once connected, configure these settings:

**Contact Creation Rules:**
- **Create new contact**: Always (recommended)
- **Update existing contact**: Yes (prevents duplicates)
- **Add to list**: Select your main lead list
- **Apply tags**: I usually add a "Calendly-Booking" tag for segmentation

**Field Mapping:**
The native integration automatically maps:
- Calendly Name → ActiveCampaign First Name + Last Name
- Calendly Email → ActiveCampaign Email
- Event Type → ActiveCampaign custom field (if you create one called "Event Type")

**Custom Field Mapping:**
If you're collecting additional data through Calendly's booking form questions, you'll need to create matching custom fields in ActiveCampaign first:

1. In ActiveCampaign: Lists → Manage Fields → Add Custom Field
2. Create fields with the exact same names as your Calendly questions
3. The integration will auto-map fields with matching names

Common custom fields I see:
- Company Size
- Budget Range  
- Current Solution
- Timeline
- Phone Number

## Method 2: Zapier Integration

The Zapier route gives you more control over the data flow and automation triggers. I use this when clients need complex conditional logic or want to create deals simultaneously.

**Zapier Setup:**

1. Create new Zap with Calendly as trigger app
2. Choose "Invitee Created" trigger (fires when someone books)
3. Connect your Calendly account and test the trigger

**ActiveCampaign Action:**
1. Add ActiveCampaign as action app
2. Choose "Create/Update Contact" action
3. Map the fields:

```
Email: {{Invitee Email}}
First Name: {{Invitee First Name}}
Last Name: {{Invitee Last Name}}
Phone: {{Invitee Phone Number}}
```

**Custom Field Mapping:**
For each custom field, use Zapier's field mapping:
```
Company Size: {{Invitee Answers Company Size}}
Budget: {{Invitee Answers Budget Range}}
Timeline: {{Invitee Answers Timeline}}
```

**Additional Actions:**
Most clients want to trigger an automation sequence, so add a second action:
1. ActiveCampaign → Add Contact to Automation
2. Select your follow-up sequence
3. This fires immediately after the contact is created

**Deal Creation (Optional):**
If you track each booking as a deal:
1. Add third action: ActiveCampaign → Create Deal
2. Map deal fields:
```
Contact: {{Contact ID from previous step}}
Title: "{{Event Type}} - {{Invitee Name}}"
Value: 0 (or expected deal value)
Pipeline: Your sales pipeline
Stage: "Scheduled" or "Initial Meeting"
```

## Method 3: Webhook + API Approach

For advanced setups or when you need real-time processing without Zapier's delays, use Calendly webhooks with ActiveCampaign's API.

**Calendly Webhook Setup:**
1. Go to Integrations → Webhooks & API Keys
2. Create new webhook with endpoint: `https://yourdomain.com/calendly-webhook`
3. Subscribe to events: `invitee.created`, `invitee.canceled`

**Webhook Processing Code (Node.js example):**

```javascript
app.post('/calendly-webhook', async (req, res) => {
  const { event, payload } = req.body;
  
  if (event === 'invitee.created') {
    const invitee = payload;
    
    // Extract custom field answers
    const customFields = {};
    if (invitee.questions_and_answers) {
      invitee.questions_and_answers.forEach(qa => {
        customFields[qa.question] = qa.answer;
      });
    }
    
    // Create contact in ActiveCampaign
    const contact = {
      email: invitee.email,
      firstName: invitee.name.split(' ')[0],
      lastName: invitee.name.split(' ').slice(1).join(' '),
      phone: invitee.text_reminder_number,
      fieldValues: [
        { field: 'EVENTTYPE', value: invitee.event.name },
        { field: 'COMPANYSIZE', value: customFields['Company Size'] || '' },
        { field: 'BUDGET', value: customFields['Budget Range'] || '' }
      ]
    };
    
    try {
      const response = await fetch(`${AC_BASE_URL}/api/3/contacts`, {
        method: 'POST',
        headers: {
          'Api-Token': process.env.AC_API_KEY,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ contact })
      });
      
      if (!response.ok) {
        throw new Error(`AC API error: ${response.statusText}`);
      }
      
      console.log('Contact created successfully');
    } catch (error) {
      console.error('Failed to create contact:', error);
      // Add to retry queue or send alert
    }
  }
  
  res.status(200).json({ received: true });
});
```

## Testing & Verification

**Test the Integration:**
1. Book a test appointment on your Calendly link
2. Use a unique email address (like `test+[timestamp]@yourcompany.com`)
3. Fill out all custom fields with recognizable test data

**Verify in ActiveCampaign:**
1. Check Contacts → search for your test email
2. Verify all fields mapped correctly:
   - Standard fields (name, email, phone)
   - Custom fields match your booking form answers
   - Tags applied correctly
   - Added to correct list

**Check Automation Triggers:**
If you have follow-up sequences, verify the test contact entered the automation. Go to Automations → [Your Sequence] → Contacts to see recent entries.

**Timing Verification:**
- Native integration: Usually 1-3 minutes delay
- Zapier: 2-15 minutes depending on your plan
- Webhooks: Near real-time (under 30 seconds)

Acceptable delay is under 15 minutes for most business use cases. If it's longer, something's broken.

## Troubleshooting

**Problem: Contacts not appearing in ActiveCampaign**
Check your Calendly integration logs (Integrations → ActiveCampaign → View Activity). Common issues:
- Invalid ActiveCampaign API key
- ActiveCampaign account URL wrong (needs full subdomain)
- Contact already exists and integration set to "skip duplicates"

**Problem: Duplicate contacts being created**
The integration isn't matching existing contacts properly. In ActiveCampaign integration settings:
- Enable "Update existing contact" 
- Set email as the unique identifier
- Make sure the integration has permission to update contacts

**Problem: Custom fields not mapping**
Field names must match exactly between Calendly questions and ActiveCampaign custom fields. Check:
- ActiveCampaign field names (Lists → Manage Fields)
- Calendly question names (Event Types → Questions)
- Case sensitivity matters ("Company Size" ≠ "company size")

**Problem: Zapier integration failing**
Check the Zap history for error details. Most common:
- ActiveCampaign API rate limits (max 5 requests/second)
- Invalid field values (e.g., trying to put text in a number field)
- Contact missing required fields

**Problem: Webhook endpoint not receiving data**
Verify the webhook URL is publicly accessible:
- Test with `curl -X POST https://yourdomain.com/calendly-webhook`
- Check server logs for incoming requests
- Calendly webhook logs show delivery attempts and response codes

**Problem: Integration worked then stopped**
Usually an API key issue or permission change:
- ActiveCampaign API key expired or was regenerated
- Account permissions changed (integration needs admin access)
- ActiveCampaign account suspended or over limits

## What To Do Next

- [ActiveCampaign Integration Hub](/integrations/activecampaign) — all ActiveCampaign integration guides
- [Calendly → HubSpot Integration](/integrations/calendly-to-hubspot) — similar setup for HubSpot users
- [Calendly → Salesforce Integration](/integrations/calendly-to-salesforce) — enterprise CRM alternative
- [Calendly Google Ads Conversion Tracking](/tracking/calendly-google-ads-conversion-tracking) — track bookings as Google Ads conversions

Need help auditing your current tracking setup? [Get a free tracking audit](/contact) — I'll review your integration and identify what's breaking or missing.

*This guide is part of the [ActiveCampaign Integration Hub](/integrations/activecampaign) — complete guides for connecting ActiveCampaign to your marketing stack.*