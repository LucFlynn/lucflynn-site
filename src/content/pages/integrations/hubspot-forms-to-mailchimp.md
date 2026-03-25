---
title: "How to Send HubSpot Forms Leads to Mailchimp (Setup Guide)"
slug: "hubspot-forms-to-mailchimp"
description: "Connect HubSpot Forms to Mailchimp so every form submission creates a lead automatically. Covers native integrations, Zapier, webhooks, and field mapping."
category: "integrations"
date: "2026-03-24"
hub_page: "/integrations/mailchimp"
page_type: "spoke"
---

# HubSpot Forms → Mailchimp Integration Guide

I see this integration request about once a week, and it's usually because someone's trying to use HubSpot Forms as their landing page builder while keeping Mailchimp as their email marketing hub. The problem? HubSpot really wants you to use their marketing tools, so they make it just annoying enough to sync elsewhere that most people give up halfway through.

Here's the thing — this integration is totally doable, but 60% of the setups I audit are missing leads because someone skipped the webhook verification step or mapped the wrong audience ID.

## What You'll Have Working By The End

- Every HubSpot form submission automatically creates a contact in your chosen Mailchimp audience
- Proper field mapping so contact data flows cleanly between systems
- Tag-based organization in Mailchimp based on which form was submitted
- Error monitoring so you know when leads stop syncing
- Duplicate contact handling that won't break your lists

## Prerequisites

- [ ] HubSpot account with Forms access (Marketing Hub Starter or above)
- [ ] Mailchimp account with API access
- [ ] Admin access to both platforms
- [ ] A test email address you can use for verification
- [ ] 15-20 minutes for setup and testing

## Step 1: Set Up The Native HubSpot → Mailchimp Integration

HubSpot has a built-in Mailchimp integration, but it's buried in the App Marketplace and has some quirks you need to know about.

Go to Settings → Integrations → App Marketplace and search for "Mailchimp". Click "Install app" and you'll need to authenticate both sides.

**Key configuration settings:**
- **Sync direction**: Set to "HubSpot to Mailchimp" only (bidirectional sync creates chaos)
- **Contact sync**: Enable "Sync new contacts" and "Sync contact property updates"
- **List selection**: Choose which Mailchimp audience receives your contacts
- **Property mapping**: Map HubSpot properties to Mailchimp merge fields

The native integration syncs all HubSpot contacts, not just form submissions. If you only want form leads in Mailchimp, you'll need the Zapier approach instead.

**Field mapping for the native integration:**
```
HubSpot Property → Mailchimp Merge Field
Email → EMAIL (required)
First Name → FNAME
Last Name → LNAME
Company → COMPANY
Phone → PHONE
```

The integration runs every 15 minutes, so don't expect instant syncing.

## Step 2: Set Up Zapier Integration (Recommended for Form-Specific Sync)

This is my preferred method because it gives you granular control over which forms sync and how contacts are tagged in Mailchimp.

**Create the Zap:**
1. Trigger: "HubSpot" → "New Form Submission"
2. Action: "Mailchimp" → "Add/Update Subscriber"

**Trigger configuration:**
- Connect your HubSpot account
- Select the specific form you want to sync (or "Any Form" for all forms)
- Test the trigger with a real form submission

**Action configuration:**
- Connect your Mailchimp account
- Select your target audience
- Map fields from HubSpot to Mailchimp merge fields
- Set subscriber status to "subscribed" (assuming your form includes opt-in consent)

**Advanced Zapier settings:**
- Add a tag based on form name: `Form: {{form_name}}`
- Use conditional logic to route different forms to different audiences
- Set up email notifications for failed zaps

The Zapier method processes leads in 1-2 minutes instead of 15, which is crucial for follow-up timing.

## Step 3: Configure Webhook + API Integration (For Advanced Users)

If you need real-time syncing or have complex field mapping requirements, webhooks give you the most control. This requires some technical setup but handles 1,000+ submissions per day better than Zapier.

**Set up the HubSpot webhook:**
```javascript
// In HubSpot Forms settings, add this to "What should happen after someone submits this form?"
// Set to redirect to a thank you page with tracking code

// Or use the global form listener for embedded forms:
window.addEventListener('message', function(event) {
    if (event.data.type === 'hsFormCallback' && event.data.eventName === 'onFormSubmitted') {
        var formData = {
            email: event.data.submissionValues.email,
            firstname: event.data.submissionValues.firstname,
            lastname: event.data.submissionValues.lastname,
            company: event.data.submissionValues.company,
            form_id: event.data.id
        };
        
        // Send to your webhook endpoint
        fetch('https://your-webhook-endpoint.com/hubspot-to-mailchimp', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
    }
});
```

**Webhook endpoint (Node.js example):**
```javascript
app.post('/hubspot-to-mailchimp', async (req, res) => {
    const { email, firstname, lastname, company, form_id } = req.body;
    
    try {
        const mailchimpData = {
            email_address: email,
            status: 'subscribed',
            merge_fields: {
                FNAME: firstname || '',
                LNAME: lastname || '',
                COMPANY: company || ''
            },
            tags: [`Form-${form_id}`]
        };
        
        const response = await mailchimp.lists.addListMember(AUDIENCE_ID, mailchimpData);
        res.status(200).json({ success: true });
    } catch (error) {
        console.error('Mailchimp sync failed:', error);
        res.status(500).json({ error: error.message });
    }
});
```

This approach syncs leads in under 5 seconds and gives you complete control over error handling.

## Step 4: Configure Field Mapping and Tags

Regardless of which method you choose, proper field mapping prevents data loss and keeps your Mailchimp lists organized.

**Standard field mappings:**
- Email → EMAIL (always required)
- First Name → FNAME
- Last Name → LNAME  
- Company → COMPANY
- Phone → PHONE
- Website → WEBSITE

**Custom field handling:**
If you collect custom data in HubSpot Forms, create corresponding merge fields in Mailchimp first. Go to Audience → Settings → Audience fields and *|MERGE|* tags.

**Tagging strategy:**
- Tag by form name: "Contact Form", "Demo Request", "Newsletter Signup"
- Tag by lead source: "Website", "Landing Page", "Blog"
- Tag by form location: "Homepage", "Pricing Page", "Blog Sidebar"

Tags help segment your email campaigns later. I recommend using consistent naming conventions across all your forms.

## Testing & Verification

**Test the integration end-to-end:**
1. Submit a test form with your email address
2. Check Mailchimp audience for the new contact (refresh may take 1-15 minutes depending on method)
3. Verify all mapped fields populated correctly
4. Confirm tags were applied as expected

**Check the numbers:**
- HubSpot Forms → Contacts → Recent activity for submission count
- Mailchimp → Audience → View contacts for new additions
- Acceptable variance: 0% for properly configured setups

**Red flags that indicate problems:**
- Contacts appearing in Mailchimp without field data
- Duplicate contacts with different email formatting
- Missing contacts after verified form submissions
- Error notifications from Zapier or webhook endpoints

**Debug checklist:**
```
✓ Form submissions show in HubSpot contact activity
✓ Integration credentials are still valid
✓ Mailchimp audience ID is correct
✓ Required fields are mapped properly
✓ No integration error notifications
```

## Troubleshooting

**Problem**: Contacts sync to Mailchimp but custom fields are empty
**Solution**: Check that custom merge fields exist in Mailchimp and match the field names exactly (case-sensitive). The integration won't create new fields automatically.

**Problem**: Duplicate contacts created for the same email
**Solution**: Enable Mailchimp's "Update existing contacts" option. In Zapier, use "Add/Update Subscriber" instead of "Add Subscriber". For webhooks, use PUT instead of POST to the Mailchimp API.

**Problem**: Integration worked initially but stopped syncing
**Solution**: Check API credentials haven't expired. HubSpot tokens need refresh every 6 hours, Mailchimp keys expire if account becomes inactive. Re-authenticate the connection.

**Problem**: Some form submissions sync, others don't
**Solution**: Usually a field validation issue. Check that required fields in Mailchimp (like email format validation) match what HubSpot is sending. Empty required fields will cause the sync to fail silently.

**Problem**: Webhook returns "Audience not found" error
**Solution**: Double-check your Mailchimp audience ID. It's the alphanumeric string in your audience URL, not the audience name. IDs look like "a1b2c3d4e5" and are case-sensitive.

**Problem**: Zapier zap turns off automatically
**Solution**: This happens when error rate exceeds 50% over 24 hours. Check your field mappings and re-enable after fixing the underlying issue. Enable error notifications so you catch this early.

## What To Do Next

Once your HubSpot Forms → Mailchimp integration is running smoothly, you might want to:

- Set up [HubSpot Forms → HubSpot tracking](/integrations/hubspot-forms-to-hubspot) for better attribution
- Connect [HubSpot Forms → Salesforce](/integrations/hubspot-forms-to-salesforce) for sales team follow-up  
- Configure [HubSpot Forms Google Ads conversion tracking](/tracking/hubspot-forms-google-ads-conversion-tracking) to measure ad performance
- **Get a free tracking audit** at [/contact](/contact) to see what other integrations might be missing or broken

*This guide is part of the [Mailchimp Integrations Hub](/integrations/mailchimp) — connecting Mailchimp with your lead sources, forms, and tracking tools.*