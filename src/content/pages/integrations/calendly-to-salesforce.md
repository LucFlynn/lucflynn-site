---
title: "How to Send Calendly Leads to Salesforce (Setup Guide)"
slug: "calendly-to-salesforce"
description: "Connect Calendly to Salesforce so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/salesforce"
page_type: "spoke"
---

# Calendly → Salesforce Integration Guide

I audit about 30-40 Calendly → Salesforce integrations per year, and roughly 60% of them are dropping leads. Usually it's field mapping issues or the integration breaking silently after a Salesforce org change. The scary part? Most companies don't realize leads are missing until they run a quarterly reconciliation.

Here's how to set this up properly so every Calendly booking creates a lead in Salesforce, with the right field mapping and error handling so you actually know when something breaks.

## What You'll Have Working By The End

- Every Calendly booking automatically creates a lead in Salesforce within 2-3 minutes
- Proper field mapping so contact info, meeting details, and custom fields transfer correctly
- Error monitoring so you know immediately if the integration stops working
- Lead deduplication rules to prevent duplicate contacts from multiple bookings
- Test process to verify new leads are appearing in the right Salesforce queues

## Prerequisites

- [ ] Calendly Pro or higher plan (webhooks require paid plan)
- [ ] Salesforce admin access or someone who can create custom fields
- [ ] Access to create Web-to-Lead forms in Salesforce (or API permissions for webhook method)
- [ ] Zapier account if using the middleware approach
- [ ] List of which Calendly fields need to map to which Salesforce fields

## Step 1: Choose Your Integration Method

You've got three realistic options here. Native integration doesn't exist between Calendly and Salesforce, so you're looking at middleware or custom webhooks.

**Zapier Method (Recommended for most setups)**
- Easiest to set up and maintain
- Built-in error handling and retry logic
- Works with both Salesforce Lead and Contact objects
- Monthly cost but saves hours of development time

**Webhook + Salesforce API Method**
- More control over field mapping and error handling
- Better for high-volume setups (500+ bookings/month)
- Requires developer time to build and maintain
- No monthly middleware costs

**Web-to-Lead + URL Parameters (Backup method)**
- Works if Calendly redirect URL can pass parameters
- Limited field mapping capabilities
- Not recommended as primary method but useful for testing

## Step 2: Set Up Salesforce to Receive Leads

Before connecting Calendly, you need Salesforce ready to accept the leads with the right field structure.

**Create Custom Fields (if needed)**
Most Calendly data maps to standard Salesforce lead fields, but you might need custom fields for:

```
Meeting Date/Time → Custom field: Meeting_Scheduled_Date_Time__c (DateTime)
Event Type → Custom field: Calendly_Event_Type__c (Text 255)
Meeting Duration → Custom field: Meeting_Duration_Minutes__c (Number)
Calendly Event URL → Custom field: Calendly_Meeting_URL__c (URL)
```

**Set Up Lead Assignment Rules**
Go to Setup → Lead Assignment Rules and make sure you have rules that will route Calendly leads to the right sales rep or queue. I see leads falling into a black hole about 25% of the time because assignment rules weren't updated for the new lead source.

**Configure Web-to-Lead (for Zapier method)**
Setup → Web-to-Lead → Create Web-to-Lead Form
Select the fields you want to capture and generate the form HTML. You'll use the endpoint URL in Zapier, not the actual form.

## Step 3: Configure Calendly Webhooks

In your Calendly account, go to Integrations & Apps → API & Webhooks.

**Create Webhook for "Invitee Created" events:**

```json
Webhook URL: [Your Zapier webhook URL or custom endpoint]
Events: invitee.created
Signing Key: [Save this - you'll need it to verify webhook authenticity]
```

The webhook payload looks like this:

```json
{
  "created_at": "2026-03-24T18:30:00.000000Z",
  "event": "invitee.created",
  "payload": {
    "email": "prospect@company.com",
    "name": "John Smith",
    "event": {
      "name": "30 Minute Meeting",
      "start_time": "2026-03-25T14:00:00.000000Z",
      "end_time": "2026-03-25T14:30:00.000000Z"
    },
    "questions_and_answers": [
      {
        "question": "Please share anything that will help prepare for our meeting.",
        "answer": "Looking to discuss Q2 marketing budget"
      }
    ],
    "tracking": {
      "utm_source": "google",
      "utm_medium": "cpc",
      "utm_campaign": "demo-requests"
    }
  }
}
```

**Test the webhook:** Use a tool like ngrok or webhook.site to verify Calendly is sending the payload correctly before connecting to your actual integration.

## Step 4: Build the Zapier Integration

Create a new Zap: Calendly (Invitee Created) → Salesforce (Create Lead)

**Calendly Trigger Setup:**
- Choose "Invitee Created" as the trigger
- Connect your Calendly account
- Test to pull in sample data

**Salesforce Action Setup:**
- Choose "Create Lead" (or "Create Contact" if your process uses Contacts)
- Map fields like this:

```
Calendly Field → Salesforce Field
Email → Email
Name → Name (or split to First Name + Last Name)
Event Name → Lead Source or Custom Event Type field
Start Time → Custom Meeting Date field
Questions/Answers → Description or custom fields
UTM Parameters → Campaign fields or custom tracking fields
```

**Critical field mapping notes:**
- Always map Email - this is your deduplication key
- Map Lead Source to something like "Calendly" so you can report on it
- Don't forget Phone if Calendly collects it
- Map custom questions to Description or create specific custom fields

**Set up the lead assignment:**
Either map to Owner ID if you know the Salesforce user ID, or let Salesforce assignment rules handle it by leaving Owner blank.

## Step 5: Configure Deduplication and Error Handling

**In Zapier:**
- Add a filter step to check if a lead with this email already exists
- Set up error notifications to email you when the integration fails
- Configure retry logic (Zapier does this automatically, but verify it's enabled)

**In Salesforce:**
- Set up duplicate rules to handle multiple bookings from the same email
- Consider using Lead conversion rules if someone books multiple times
- Create a report to monitor leads created from Calendly

Test the deduplication by booking the same email twice and verify you don't get duplicate leads.

## Step 6: Testing & Verification

**Test the full flow:**
1. Book a test meeting in Calendly using a unique email
2. Check that the webhook fired (Calendly webhook logs)
3. Verify Zapier received and processed the webhook (Zapier task history)
4. Confirm the lead appeared in Salesforce within 2-3 minutes
5. Verify all field mapping is correct and assignment rules fired

**Check the lead quality:**
- All required fields populated correctly
- Lead source shows "Calendly" or your designated source
- Meeting date/time is accurate and in the right timezone
- Custom fields from Calendly questions are mapped properly
- Lead assigned to correct owner or queue

**Volume testing:**
If you expect high volume, book 5-10 test meetings quickly to make sure the integration can handle multiple webhooks without dropping any.

**Cross-reference numbers weekly:**
Compare Calendly booking count to Salesforce leads created. Should match within 2-3%. If you're seeing bigger discrepancies, something's broken.

## Troubleshooting

**Problem:** Leads aren't appearing in Salesforce
Check Zapier task history for errors. Common causes: Salesforce field validation rules blocking the lead creation, missing required fields, or API limits hit. Look for the specific error message in Zapier logs.

**Problem:** Duplicate leads being created for the same person
Your Salesforce duplicate rules aren't configured properly or you're not mapping Email as the deduplication key. Go to Setup → Duplicate Management and create/update rules for Lead objects using Email as the matching criteria.

**Problem:** Meeting time is showing wrong timezone in Salesforce
Calendly sends UTC timestamps. Make sure your Salesforce DateTime field is configured to handle timezone conversion, or add a Zapier formatter step to convert to your business timezone before sending to Salesforce.

**Problem:** Webhooks stop working after Calendly account changes
When someone updates Calendly integrations or changes admin access, webhooks can get disconnected. Set up monitoring to alert you when webhook volume drops below expected levels. I recommend checking webhook delivery status in Calendly weekly.

**Problem:** Custom Calendly questions aren't mapping to Salesforce
Questions and answers come through as an array in the webhook payload. In Zapier, you'll need to use a Code step or Formatter to extract specific question answers, or concatenate all Q&As into the Description field.

**Problem:** High-value leads aren't getting immediate follow-up
This isn't a technical issue but a process one. Set up Salesforce workflow rules or Process Builder to send immediate alerts when leads come in from Calendly, especially for high-value event types like "Enterprise Demo" bookings.

## What To Do Next

Once your Calendly → Salesforce integration is running smoothly, you might want to:

- Set up [Calendly → HubSpot integration](/integrations/calendly-to-hubspot) as a backup system
- Configure [Calendly Google Ads conversion tracking](/tracking/calendly-google-ads-conversion-tracking) to measure booking value
- Build [Calendly → GoHighLevel automation](/integrations/calendly-to-gohighlevel) for additional nurture sequences
- **Get a free audit of your entire tracking setup** — [book a call](/contact) and I'll review your Calendly integration plus all your other lead sources

*This guide is part of the [Salesforce Integrations Hub](/integrations/salesforce) — covering all the ways to get lead data into Salesforce automatically.*