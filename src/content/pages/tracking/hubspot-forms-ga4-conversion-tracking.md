---
title: "How to Track HubSpot Forms Conversions in GA4 (2026 Guide)"
slug: "hubspot-forms-ga4-conversion-tracking"
description: "Step-by-step guide to tracking HubSpot Forms form submissions as conversions in GA4. Covers GTM setup, Client-Side GTM, testing, and troubleshooting."
category: "tracking"
date: "2026-03-24"
hub_page: "/tracking/ga4-conversion-tracking"
page_type: "spoke"
---

# HubSpot Forms + GA4 Conversion Tracking Setup

Here's the thing — most people think HubSpot forms automatically track in GA4 just because both tools are running on the site. I see this broken in about 60% of the HubSpot accounts I audit. HubSpot's native tracking handles their internal analytics, but getting clean conversion data into GA4 requires a proper GTM setup that listens for HubSpot's form submission events.

The main issue is that HubSpot forms fire their completion events after the page interaction, but GA4 needs to receive a properly formatted conversion event with the right parameters to count it as a lead generation event.

## What You'll Have Working By The End

- HubSpot form submissions automatically tracked as GA4 conversion events
- Proper 'generate_lead' events firing with form details in GA4
- Clean conversion data flowing from GA4 to Google Ads (if connected)
- Real-time verification working in GA4 DebugView
- Accurate lead volume reporting in GA4 that matches your HubSpot form submission count

## Prerequisites

Before starting, make sure you have:
- [ ] Admin access to your GTM container
- [ ] Edit access to your GA4 property
- [ ] HubSpot forms already embedded and functional on your site
- [ ] GA4 base tracking already installed via GTM
- [ ] Access to your website's developer tools for testing

## Step 1: Set Up the HubSpot Form Submission Listener

First, we need GTM to listen for HubSpot's form submission events. HubSpot fires `hsFormCallback` and `onFormSubmitted` events that we can capture.

In GTM, create a new Custom HTML tag:

```html
<script>
window.addEventListener('message', function(event) {
    if (event.data.type === 'hsFormCallback' && event.data.eventName === 'onFormSubmitted') {
        dataLayer.push({
            'event': 'hubspot_form_submit',
            'form_id': event.data.id,
            'form_title': event.data.formTitle || 'HubSpot Form',
            'page_url': window.location.href,
            'timestamp': new Date().toISOString()
        });
    }
});

// Fallback for older HubSpot embedded forms
if (typeof hbspt !== 'undefined') {
    hbspt.forms.create({
        portalId: "YOUR_PORTAL_ID", // Replace with your HubSpot portal ID
        formId: "YOUR_FORM_ID",     // Replace with your form ID
        onFormSubmit: function($form) {
            dataLayer.push({
                'event': 'hubspot_form_submit',
                'form_id': $form.find('input[name="formId"]').val(),
                'form_title': 'HubSpot Contact Form',
                'page_url': window.location.href,
                'timestamp': new Date().toISOString()
            });
        }
    });
}
</script>
```

Set this tag to fire on "All Pages" so it's available whenever a HubSpot form loads.

**Important:** Replace `YOUR_PORTAL_ID` and `YOUR_FORM_ID` with your actual HubSpot IDs if you're using the fallback method. You can find these in your HubSpot form embed code.

## Step 2: Create the GTM Trigger

Now create a Custom Event trigger in GTM:

1. Go to Triggers → New
2. Choose "Custom Event" as trigger type
3. Event name: `hubspot_form_submit`
4. Save as "HubSpot Form Submission"

This trigger will fire whenever our listener code pushes the `hubspot_form_submit` event to the data layer.

## Step 3: Configure the GA4 Conversion Event Tag

Create a new GA4 Event tag in GTM:

1. Tag Type: Google Analytics: GA4 Event
2. Configuration Tag: Select your GA4 config tag
3. Event Name: `generate_lead`
4. Event Parameters:
   - `form_location`: `{{Page URL}}`
   - `form_id`: `{{dlv - form_id}}` (create this as a Data Layer Variable)
   - `form_title`: `{{dlv - form_title}}` (create this as a Data Layer Variable)

You'll need to create those Data Layer Variables first:
- Variable Type: Data Layer Variable
- Data Layer Variable Name: `form_id` (and `form_title` for the second one)

Set this tag to fire on your "HubSpot Form Submission" trigger.

## Step 4: Mark the Event as a Conversion in GA4

Once the tag is firing, you need to tell GA4 that `generate_lead` is a conversion:

1. Go to your GA4 property → Admin
2. Click "Conversions" under Data display
3. Click "New conversion event"
4. Enter event name: `generate_lead`
5. Save

GA4 will start counting these as conversions within 24 hours, but you'll see the events immediately in DebugView.

## Step 5: Client-Side GTM Setup Considerations

Since we're using client-side GTM, keep these points in mind:

- **Ad blockers impact:** About 15-25% of users block client-side tags, so your GA4 count will be lower than your HubSpot form submission count
- **Loading order:** Make sure your Custom HTML tag fires before users can submit forms. Set it to fire on DOM Ready or Page View
- **Multiple forms:** If you have multiple HubSpot forms on one page, this setup captures all of them

**Which approach should you use?** Stick with client-side GTM unless you're seeing >20% data loss from ad blockers. For most B2B sites, client-side is fine because your audience typically doesn't block analytics as aggressively.

## Testing & Verification

Here's how to verify everything is working:

### Real-Time Testing in GA4:
1. Open GA4 → Reports → Realtime
2. In another tab, submit your HubSpot form
3. You should see the `generate_lead` event appear within 30 seconds
4. Check that the form_id and form_title parameters are populated correctly

### Debug View Testing:
1. Enable GA4 DebugView for your test traffic (install GA4 Debugger extension)
2. Submit a form while DebugView is active
3. Look for the `generate_lead` event with proper parameters
4. Verify the event shows up as a conversion in the Conversions section

### Cross-Reference Check:
Compare your numbers:
- **Source of truth:** HubSpot Contacts → Forms → Submissions (last 7 days)
- **GA4 count:** GA4 → Reports → Conversions (filter by generate_lead)
- **Acceptable variance:** 5-15% lower in GA4 due to ad blockers and tracking prevention

## Troubleshooting

**Problem:** Events firing but not showing as conversions in GA4  
**Solution:** Check that you marked `generate_lead` as a conversion in GA4 Admin. It takes up to 24 hours to retroactively count existing events as conversions.

**Problem:** Multiple events firing for one form submission  
**Solution:** Add a debounce mechanism to your Custom HTML tag. Wrap the dataLayer.push in a setTimeout and clear any existing timeout before setting a new one.

**Problem:** No events firing at all  
**Solution:** Check that your HubSpot forms are actually embedded correctly. Use browser dev tools to verify the hsFormCallback events are firing. If not, your forms might be using an older embed method that needs the fallback code.

**Problem:** Form_id showing as undefined in GA4  
**Solution:** HubSpot's form ID might be nested differently in the event data. Add `console.log(event.data)` to your listener code to see the actual structure and adjust your data layer push accordingly.

**Problem:** Events firing on wrong forms  
**Solution:** Add form ID filtering to your listener. Modify the code to only push events for specific form IDs: `if (event.data.id === 'your-target-form-id')`.

**Problem:** GA4 count is 40%+ lower than HubSpot count  
**Solution:** This suggests either significant ad blocker usage or a technical issue. Check your GTM Preview mode to see if tags are firing consistently. Consider implementing server-side tracking for critical conversion measurement.

## What To Do Next

Now that your HubSpot forms are tracking in GA4, consider these related setups:

- [HubSpot Forms + Google Ads Conversion Tracking](/tracking/hubspot-forms-google-ads-conversion-tracking) — Import these GA4 conversions into Google Ads for campaign optimization
- [HubSpot Forms + Meta Ads Conversion Tracking](/tracking/hubspot-forms-meta-ads-conversion-tracking) — Set up parallel Facebook Pixel tracking for your Meta campaigns  
- [HubSpot Forms + LinkedIn Ads Conversion Tracking](/tracking/hubspot-forms-linkedin-ads-conversion-tracking) — Track LinkedIn campaign performance with form submissions
- [HubSpot Forms to HubSpot CRM Integration](/integrations/hubspot-forms-to-hubspot) — Ensure your form data flows cleanly into your CRM workflows

Want me to audit your current tracking setup for free? I'll spot-check your GTM configuration and GA4 conversion counting to make sure everything's accurate. **[Get your free tracking audit here](/contact)**.

*This guide is part of the [GA4 Conversion Tracking Hub](/tracking/ga4-conversion-tracking) — complete setup guides for tracking any conversion in Google Analytics 4.*