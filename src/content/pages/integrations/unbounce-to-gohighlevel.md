---
title: "How to Send Unbounce Leads to GoHighLevel (Setup Guide)"
slug: "unbounce-to-gohighlevel"
description: "Connect Unbounce to GoHighLevel so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/gohighlevel"
page_type: "spoke"
---

# Unbounce → GoHighLevel Integration Guide

I see this integration broken in about 30% of the agencies I work with. Usually it's because they tried to set up the native integration, it looked like it worked, but leads have been silently failing for weeks. The client keeps asking why their "high-converting" landing pages aren't generating pipeline, and nobody thought to check if the leads actually made it into GoHighLevel.

The webhook approach is most reliable here — GoHighLevel's webhook system is solid, and Unbounce's form handlers play nice with external APIs. But there are three ways to do this, and I'll walk you through each one.

## What You'll Have Working By The End

- Every Unbounce form submission creates a contact in GoHighLevel automatically
- Leads assigned to the correct pipeline and stage based on landing page source
- Custom fields mapped properly (UTM parameters, landing page name, form source)
- Duplicate prevention working so the same email doesn't create multiple contacts
- Error handling in place so you know when leads are getting dropped

## Prerequisites

- [ ] Admin access to your Unbounce account
- [ ] Agency or higher permissions in GoHighLevel
- [ ] Access to create webhooks and API keys in GoHighLevel
- [ ] Zapier account (if using the Zapier method)
- [ ] Test email address you can use to verify the integration

## Step 1: Choose Your Integration Method

You've got three realistic options here. Skip the native integration unless you're dealing with a very simple use case — it breaks too often.

**Zapier (Recommended for most setups):** Easiest to set up and maintain. Built-in error handling and retry logic. Costs $20-50/month depending on volume but worth it for reliability.

**Direct Webhook:** Most reliable for high-volume setups. Requires some technical comfort but gives you complete control over field mapping and error handling.

**Native GoHighLevel Integration:** Exists in Unbounce's integrations panel, but I've seen it fail silently when GoHighLevel updates their API. Only use this for low-stakes testing.

I'm starting with Zapier because it works for 80% of setups, then covering webhooks for the technical folks.

## Step 2: Set Up GoHighLevel to Receive Leads

First, you need somewhere for the leads to go. In GoHighLevel:

1. Go to **Settings → Integrations → Webhooks**
2. Click **Create Webhook**
3. Name it "Unbounce Leads" or similar
4. Set the **Type** to "Contact"
5. Choose your default **Pipeline** and **Stage** for new leads
6. Copy the webhook URL — you'll need this in Unbounce

The webhook URL looks like: `https://services.leadconnectorhq.com/hooks/webhook-key-here`

**Field mapping setup:** In the webhook settings, map these fields if you want UTM data:
- `utm_source` → Custom Field "Lead Source"
- `utm_campaign` → Custom Field "Campaign"
- `landing_page` → Custom Field "Landing Page"

Don't skip this — knowing which landing page generated each lead is crucial for reporting.

## Step 3: Configure Unbounce Form Submission

In your Unbounce landing page editor:

1. Select your form element
2. Go to **Form Confirmation** in the right panel
3. Choose **Go to URL** (not "Show Confirmation Dialog")
4. Set the URL to your GoHighLevel webhook URL
5. Check **Include form data in URL**

This sends the form data as URL parameters to your webhook. The webhook URL becomes:
```
https://services.leadconnectorhq.com/hooks/webhook-key-here?email=john@example.com&first_name=John&phone=555-123-4567
```

**Alternative webhook approach:** If you want more control, use Unbounce Scripts instead:

1. Go to **Landing Pages → [Your Page] → Scripts**
2. Add this to **Before Body End Tag:**

```javascript
<script>
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('lp-pom-form-1');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            const data = {
                email: formData.get('email'),
                first_name: formData.get('name'), // Adjust field names
                phone: formData.get('phone'),
                utm_source: getUrlParameter('utm_source'),
                utm_campaign: getUrlParameter('utm_campaign'),
                landing_page: window.location.pathname
            };
            
            fetch('YOUR_GOHIGHLEVEL_WEBHOOK_URL', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            }).then(() => {
                window.location.href = '/thank-you'; // Your thank you page
            });
        });
    }
});

function getUrlParameter(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name) || '';
}
</script>
```

This gives you better error handling and lets you include UTM parameters automatically.

## Step 4: Zapier Integration (Alternative Method)

If you prefer Zapier over direct webhooks:

1. Create new Zap: **Unbounce → GoHighLevel**
2. **Trigger:** "New Lead in Unbounce"
3. Connect your Unbounce account and select your landing page
4. **Action:** "Create Contact in GoHighLevel"
5. Connect your GoHighLevel account

**Field mapping in Zapier:**
- Email (Unbounce) → Email (GoHighLevel)
- Name or First Name (Unbounce) → First Name (GoHighLevel)
- Phone (Unbounce) → Phone (GoHighLevel)
- Add these custom fields:
  - Landing Page → Custom Field "Lead Source"
  - Form Name → Custom Field "Form Name"

**Zapier pros:** Built-in retry logic, error notifications, easy to modify field mapping.
**Zapier cons:** Costs money, adds delay (usually 1-15 minutes), less control over error handling.

For agencies running multiple campaigns, Zapier is worth the cost. For single landing page setups, direct webhook is fine.

## Step 5: Field Mapping Configuration

This is where most integrations break. Unbounce form field names need to match what GoHighLevel expects.

**Standard Unbounce fields:**
- `email` → Email
- `name` or `first_name` → First Name  
- `phone` → Phone
- `company` → Company Name

**Custom fields you should add:**
- Landing page URL (auto-populated via script)
- UTM source/medium/campaign (auto-populated from URL params)
- Form submission timestamp
- Lead score or source priority

In GoHighLevel, create these custom fields first (**Settings → Custom Fields → Contact Fields**) before setting up the integration. Name them clearly: "Landing Page Source", "UTM Campaign", etc.

**Pro tip:** I always add a "Lead Source" field with the exact landing page URL. Makes it easy to track which pages are converting and debug integration issues.

## Testing & Verification

Never assume this integration works without testing. Here's how to verify:

1. **Submit a test form** on your Unbounce page using a unique email
2. **Check GoHighLevel contacts** within 30 seconds (webhook) or 15 minutes (Zapier)
3. **Verify field mapping** — are custom fields populated correctly?
4. **Test duplicate handling** — submit the same email twice, should update existing contact
5. **Check pipeline assignment** — is the lead in the correct pipeline and stage?

**Webhook testing:** Check the webhook logs in GoHighLevel (**Settings → Integrations → Webhooks → View Logs**). You should see successful POST requests with 200 status codes.

**Red flags:**
- Leads appearing but missing phone numbers or custom fields
- Multiple contacts created for the same email address
- Leads not assigned to any pipeline
- Webhook logs showing 400 or 500 errors

If you see any of these, the integration isn't working correctly even if leads are coming through.

## Troubleshooting

**Problem:** Leads submitting but not appearing in GoHighLevel
Check your webhook URL is correct and the webhook is active. Test the URL directly in a browser — you should get a GoHighLevel response, not a 404. Also verify the landing page is actually sending data to the webhook (check browser dev tools Network tab).

**Problem:** Duplicate contacts being created for repeat submissions
Enable duplicate prevention in GoHighLevel webhook settings. Set it to match on email address and update existing contacts instead of creating new ones. This is under the webhook configuration "Duplicate Check" setting.

**Problem:** Custom fields (UTM data, landing page) not populating
The custom fields need to exist in GoHighLevel before the webhook can populate them. Create them first in Settings → Custom Fields, then update your webhook field mapping to include them.

**Problem:** Phone numbers not formatting correctly
GoHighLevel expects phone numbers in E.164 format (+1234567890). If Unbounce is sending (123) 456-7890 format, add a formatter in your webhook or Zapier step to clean it up.

**Problem:** Integration worked initially but stopped
Usually means GoHighLevel API credentials expired or webhook was accidentally deleted. Check the webhook still exists and is active. If using Zapier, reconnect your GoHighLevel account — the connection probably expired.

**Problem:** High volume causing webhook timeouts
GoHighLevel webhooks can handle ~10 requests per second. If you're pushing more volume than that, implement a queue system or switch to their REST API with proper rate limiting. This is rare unless you're running major traffic campaigns.

## What To Do Next

Once your Unbounce leads are flowing into GoHighLevel, you'll want to set up proper conversion tracking to measure which landing pages are generating your best leads:

- [Unbounce Google Ads Conversion Tracking](/tracking/unbounce-google-ads-conversion-tracking) — Track form submissions back to your ad campaigns
- [Unbounce to HubSpot Integration](/integrations/unbounce-to-hubspot) — Alternative CRM integration if you're comparing platforms
- [Unbounce to Salesforce Integration](/integrations/unbounce-to-salesforce) — Enterprise CRM alternative

Need help auditing your current lead flow setup? I'll check your integrations and tracking for free — [contact me here](/contact).

*This guide is part of the [GoHighLevel Integrations Hub](/integrations/gohighlevel) — complete setup guides for connecting GoHighLevel to your marketing tools and tracking infrastructure.*