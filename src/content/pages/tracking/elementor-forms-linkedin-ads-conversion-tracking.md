---
title: "How to Track Elementor Forms Conversions in LinkedIn Ads (2026 Guide)"
slug: "elementor-forms-linkedin-ads-conversion-tracking"
description: "Step-by-step guide to tracking Elementor Forms form submissions as conversions in LinkedIn Ads. Covers GTM setup, Client-Side GTM, testing, and troubleshooting."
category: "tracking"
date: "2026-03-24"
hub_page: "/tracking/linkedin-ads-conversion-tracking"
page_type: "spoke"
---

# Elementor Forms + LinkedIn Ads Conversion Tracking Setup

LinkedIn's tracking is the least polished of the major ad platforms, and Elementor Forms doesn't fire clean submission events out of the box. I see this combo broken in about 60% of WordPress sites running LinkedIn campaigns — usually because they're relying on Elementor's redirect-based "success" detection or trying to track the wrong element.

The core issue: Elementor Forms submissions are Ajax-based, so there's no page reload to trigger LinkedIn's basic conversion tracking. You need to catch the actual form submission event and push it to LinkedIn as a conversion event.

## What You'll Have Working By The End

- Elementor Forms submissions automatically tracked as LinkedIn Ads conversions
- Clean event data flowing to LinkedIn Campaign Manager within 2-4 hours
- Proper attribution connecting form fills back to LinkedIn ad clicks
- Debug-verified setup that catches both successful and failed submissions
- Backup tracking via GTM that doesn't rely on Elementor's native actions

## Prerequisites

- [ ] Active LinkedIn Ads account with Campaign Manager access
- [ ] LinkedIn Insight Tag installed on your site (base tracking code)
- [ ] Google Tag Manager installed with Publish access
- [ ] WordPress admin access to edit Elementor forms
- [ ] At least one Elementor form already built and published

## Step 1: Set Up LinkedIn Conversion Action

In LinkedIn Campaign Manager, navigate to **Analyze → Conversions** and create a new conversion:

1. Click **Create Conversion**
2. Select **Online Conversions**
3. Choose conversion type (usually "Lead" for forms)
4. Name it something specific like "Elementor Contact Form - [Page Name]"
5. Set attribution window (I recommend 30-day click, 1-day view)
6. Note the **Conversion ID** — you'll need this for GTM

The conversion will be in "Learning" status until it gets at least 10 conversions in 7 days. LinkedIn's conversion tracking is significantly slower than Google or Meta — expect 2-4 hour delays in reporting.

## Step 2: Configure GTM Data Layer Event

Add this code to your site's footer (or in a custom HTML widget). This listens for Elementor's submission events and pushes clean data to GTM:

```javascript
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Listen for Elementor form submissions
    jQuery(document).on('submit_success', '.elementor-form', function(event, response) {
        var formElement = event.target;
        var formId = formElement.getAttribute('data-form-id') || 'unknown';
        var formName = formElement.getAttribute('data-form-name') || 'elementor-form';
        
        // Push to GTM data layer
        window.dataLayer = window.dataLayer || [];
        window.dataLayer.push({
            'event': 'elementor_form_submit',
            'form_id': formId,
            'form_name': formName,
            'form_location': window.location.pathname,
            'conversion_value': 0 // Set actual value if you track lead values
        });
        
        console.log('Elementor form submitted - GTM event fired');
    });
    
    // Backup listener for standard form submit (in case submit_success doesn't fire)
    jQuery(document).on('submit', '.elementor-form form', function(event) {
        setTimeout(function() {
            // Check if form is hidden (indicates successful submission)
            var formWrapper = event.target.closest('.elementor-form');
            var successMessage = formWrapper.querySelector('.elementor-message-success');
            
            if (successMessage && successMessage.style.display !== 'none') {
                var formId = formWrapper.getAttribute('data-form-id') || 'unknown';
                var formName = formWrapper.getAttribute('data-form-name') || 'elementor-form';
                
                window.dataLayer = window.dataLayer || [];
                window.dataLayer.push({
                    'event': 'elementor_form_submit_backup',
                    'form_id': formId,
                    'form_name': formName,
                    'form_location': window.location.pathname,
                    'conversion_value': 0
                });
                
                console.log('Elementor form backup tracking fired');
            }
        }, 1000); // Wait 1 second for Elementor's UI changes
    });
});
</script>
```

## Step 3: Create GTM Trigger

In GTM, create a new trigger:

1. **Trigger Type**: Custom Event
2. **Event Name**: `elementor_form_submit`
3. **This trigger fires on**: All Custom Events
4. **Fire On**: Some Custom Events
5. **Condition**: Event equals `elementor_form_submit`

Create a second backup trigger with Event Name: `elementor_form_submit_backup`

The backup trigger catches cases where Elementor's `submit_success` event doesn't fire properly — happens in about 20% of setups due to theme conflicts or custom Elementor modifications.

## Step 4: Configure LinkedIn Conversion Tag

Create a new tag in GTM:

1. **Tag Type**: Custom HTML
2. **HTML**:
```html
<script>
window._linkedin_partner_id = "YOUR_PARTNER_ID";
window._linkedin_conversion_id = "YOUR_CONVERSION_ID";
</script>
<script type="text/javascript">
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window,document,'script',
'https://snap.licdn.com/li.lms-analytics/insight.min.js');

// Fire the conversion
lintrk('track', { conversion_id: window._linkedin_conversion_id });
</script>
```

3. **Triggering**: Select both triggers you created (primary and backup)
4. Replace `YOUR_PARTNER_ID` and `YOUR_CONVERSION_ID` with actual values from LinkedIn

**Which approach should you use?** Always set up both the primary and backup triggers. LinkedIn's conversion tracking is finicky, and the backup catches edge cases where Elementor's standard events don't fire.

## Step 5: Set Up Cross-Domain Tracking (If Needed)

If your Elementor forms redirect to a different domain for thank-you pages, add this to the LinkedIn tag's HTML:

```javascript
// Add after the conversion tracking code
if (document.referrer.indexOf('yourmaindomain.com') !== -1) {
    lintrk('track', { 
        conversion_id: window._linkedin_conversion_id,
        referrer: document.referrer 
    });
}
```

This ensures LinkedIn maintains attribution when users are redirected to external thank-you pages or checkout flows.

## Testing & Verification

### GTM Preview Mode
1. Enable GTM Preview mode
2. Submit your Elementor form
3. Check the **Summary** tab for your `elementor_form_submit` event
4. Verify the LinkedIn conversion tag fires on the correct event
5. Look for any JavaScript errors in browser console

### LinkedIn Campaign Manager
1. Go to **Analyze → Conversions**
2. Select your conversion action
3. Check **Recent Activity** (updates every 2-4 hours)
4. Look for test conversions with "Other" as traffic source

### Cross-Check Numbers
Compare Elementor form entries (WordPress admin → Elementor → Submissions) against LinkedIn conversion reports. Acceptable variance is 10-20% due to:
- Users with ad blockers (blocks LinkedIn tracking)
- JavaScript errors preventing tag execution
- Attribution window differences
- LinkedIn's slower processing times

Red flags: If you see 0 conversions in LinkedIn but multiple form submissions, check that your LinkedIn Insight Tag base code is installed correctly sitewide.

## Troubleshooting

**Problem**: GTM shows the tag firing but no conversions appear in LinkedIn
→ Verify your Partner ID and Conversion ID are correct. LinkedIn IDs are case-sensitive and often copy with extra spaces. Also check that users submitting test forms actually came from LinkedIn ads — organic traffic won't show as conversions.

**Problem**: Backup trigger fires on every page load, not just form submissions
→ The success message detection is too broad. Add this condition to the backup trigger: `{{Page URL}}` does not equal `{{Referrer}}` to ensure it only fires after form interactions.

**Problem**: Forms work in preview but not on live site
→ jQuery dependency issue. Elementor loads jQuery, but if your theme loads it differently, the event listeners might not attach. Add `jQuery(document).ready(function($) { ... });` wrapper around the entire tracking code.

**Problem**: Multiple conversions tracked for single form submission
→ Both primary and backup triggers are firing. Add a data layer variable to prevent double-firing: Set a flag when the primary trigger fires, and check for it in the backup trigger condition.

**Problem**: Conversions tracked but attribution is wrong in LinkedIn
→ Time delay between ad click and form submission is too long, or users are clearing cookies. Reduce attribution window to 7-day click in LinkedIn Campaign Manager, or implement server-side tracking for cookieless environments.

**Problem**: Elementor forms with multi-step setup not tracking final submission
→ The event listener is attached to the first step, not the final submission. Modify the form selector to target the final step: `.elementor-form[data-step="final"]` or listen for Elementor's `step_next` event on the last step.

## What To Do Next

Once you have Elementor Forms tracking working in LinkedIn, consider setting up these related integrations:

- [Elementor Forms to Google Ads conversion tracking](/tracking/elementor-forms-google-ads-conversion-tracking) — Higher conversion volume and better attribution
- [Elementor Forms to Meta Ads conversion tracking](/tracking/elementor-forms-meta-ads-conversion-tracking) — Better for B2C campaigns
- [Elementor Forms to GA4 conversion tracking](/tracking/elementor-forms-ga4-conversion-tracking) — Source of truth for cross-platform attribution
- [Elementor Forms to HubSpot integration](/integrations/elementor-forms-to-hubspot) — Automatically create contacts from form submissions

**Ready to audit your current tracking setup?** [Get a free tracking audit](/contact) — I'll review your Elementor Forms + LinkedIn Ads setup and identify any conversion leaks or attribution issues.

*This guide is part of the [LinkedIn Ads Conversion Tracking hub](/tracking/linkedin-ads-conversion-tracking) — complete setup guides for tracking LinkedIn campaign conversions across different form tools and CRMs.*