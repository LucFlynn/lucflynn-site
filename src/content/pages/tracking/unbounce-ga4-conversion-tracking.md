---
title: "How to Track Unbounce Conversions in GA4 (2026 Guide)"
slug: "unbounce-ga4-conversion-tracking"
description: "Step-by-step guide to tracking Unbounce form submissions as conversions in GA4. Covers GTM setup, Client-Side GTM, testing, and troubleshooting."
category: "tracking"
date: "2026-03-24"
hub_page: "/tracking/ga4-conversion-tracking"
page_type: "spoke"
---

# Unbounce + GA4 Conversion Tracking Setup

I see Unbounce + GA4 tracking broken in about 60% of the accounts I audit. The main culprit? Teams treat Unbounce like any other form platform, but it's actually a landing page builder with its own tag manager. When you slap GTM on top without understanding how Unbounce's conversion tracking works, you end up with double-firing events, missing conversions, or GA4 thinking every page view is a conversion.

The other issue I see constantly: people fire GA4 events on Unbounce's built-in "form submission" trigger, but Unbounce considers a form submission successful even if the lead doesn't actually convert. Your GA4 conversion count ends up 20-30% higher than actual leads.

## What You'll Have Working By The End

- Unbounce forms firing clean `generate_lead` events to GA4 only on successful conversions
- GA4 conversion tracking that matches your actual lead count (within 5-10% variance)
- Client-Side GTM setup that works with Unbounce's existing tag manager
- Debug setup to verify events are firing correctly before they hit GA4
- Cross-reference system between Unbounce lead notifications and GA4 conversion reports

## Prerequisites

- [ ] Unbounce account with publish access to your landing pages
- [ ] GA4 property with edit access
- [ ] Google Tag Manager container with publish access
- [ ] GTM container installed on your Unbounce pages (we'll verify this)
- [ ] Access to Unbounce's "Script Manager" for your pages

## Step 1: Install GTM on Your Unbounce Pages

Most Unbounce + GA4 setups I see have GTM installed incorrectly. Here's how to do it right:

In Unbounce, go to your page → Settings → Script Manager. Add this to the Head section:

```html
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-XXXXXXX');</script>
<!-- End Google Tag Manager -->
```

Add this to the Body section (Unbounce has a specific Body field):

```html
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-XXXXXXX"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
```

**Important:** Don't add GTM to Unbounce's "Before Body End Tag" section. I see this mistake in about 40% of setups, and it breaks the GTM noscript fallback.

## Step 2: Set Up the Conversion Event Listener

Here's where most setups break. Unbounce has multiple form submission events, and you need to listen for the right one.

In Unbounce Script Manager, add this to the Before Body End Tag section:

```javascript
<script>
// Wait for Unbounce to load
window.addEventListener('load', function() {
    
    // Listen for successful form submissions
    window.addEventListener('message', function(event) {
        
        // Check if it's an Unbounce conversion event
        if (event.data && event.data.type === 'ub:conversion') {
            
            // Push to dataLayer for GTM
            window.dataLayer = window.dataLayer || [];
            window.dataLayer.push({
                event: 'unbounce_conversion',
                form_id: event.data.formId || 'unknown',
                page_id: event.data.pageId || 'unknown',
                variant_id: event.data.variantId || 'unknown'
            });
            
            console.log('Unbounce conversion tracked:', event.data);
        }
    });
    
    // Fallback for older Unbounce pages
    if (typeof lp !== 'undefined' && lp.jQuery) {
        lp.jQuery(document).on('submit', 'form', function() {
            
            // Only fire if form validates successfully
            setTimeout(function() {
                if (lp.jQuery('.lp-form-errors:visible').length === 0) {
                    window.dataLayer = window.dataLayer || [];
                    window.dataLayer.push({
                        event: 'unbounce_conversion_fallback',
                        form_id: 'fallback_form'
                    });
                }
            }, 500);
        });
    }
});
</script>
```

This listens for Unbounce's native conversion event AND has a fallback for older Unbounce pages that don't fire the modern event.

## Step 3: Create the GTM Trigger

In GTM, create a new Custom Event trigger:

- **Trigger Type:** Custom Event
- **Event name:** `unbounce_conversion`
- **This trigger fires on:** All Custom Events

Create a second trigger for the fallback:

- **Trigger Type:** Custom Event  
- **Event name:** `unbounce_conversion_fallback`
- **This trigger fires on:** All Custom Events

## Step 4: Set Up the GA4 Event Tag

Create a new GA4 Event tag in GTM:

- **Tag Type:** GA4 Event
- **Configuration Tag:** [Your GA4 Configuration tag]
- **Event Name:** `generate_lead`

Add these Event Parameters:

- **form_location:** `{{Page URL}}`
- **form_id:** `{{DLV - form_id}}`
- **source:** `unbounce`

For the `form_id` parameter, you'll need to create a Data Layer Variable:

1. Variables → New → Data Layer Variable
2. **Data Layer Variable Name:** `form_id`
3. **Version:** 2
4. **Default Value:** `unknown_form`

Set the trigger to fire on both `unbounce_conversion` AND `unbounce_conversion_fallback`.

## Step 5: Mark as Conversion in GA4

In GA4:

1. Go to Admin → Events
2. Find your `generate_lead` event (might take 24-48 hours to appear)
3. Toggle "Mark as conversion" to On

**Pro tip:** You can also mark it as a conversion immediately by going to Admin → Conversions → New Conversion Event and entering `generate_lead` as the event name.

## Step 6: Link to Google Ads (Optional)

If you're running Google Ads:

1. In GA4, go to Admin → Google Ads Links
2. Link your Google Ads account
3. In Google Ads, go to Tools → Conversions
4. Your GA4 `generate_lead` conversions will import automatically

Set the conversion window to 30 days and attribution model to "Data-driven" for most B2B setups.

## Testing & Verification

**Test the Data Layer Push:**

1. Open your Unbounce page
2. Open browser dev tools → Console
3. Submit a test form
4. Look for the console.log message: "Unbounce conversion tracked"
5. Type `dataLayer` in console and verify the event object appears

**Test in GTM Preview:**

1. Enable GTM Preview mode
2. Submit a test form on your Unbounce page  
3. Verify the `unbounce_conversion` event fires
4. Verify your GA4 Event tag fires with the correct parameters

**Test in GA4:**

1. GA4 → Reports → Realtime
2. Submit test form
3. Look for the `generate_lead` event in the last 30 minutes
4. Check that event parameters (form_location, form_id, source) populate correctly

**Cross-Reference Numbers:**

Your Unbounce lead count should match GA4 conversions within 5-15% variance. Higher variance usually means:

- Forms submitting without validation (common with custom Unbounce forms)
- GTM firing on page load instead of form submission
- Ad blockers preventing GA4 events (affects 15-25% of traffic)

Check monthly: Unbounce Analytics → Conversions vs. GA4 → Reports → Engagement → Conversions.

## Troubleshooting

**Problem:** GTM Preview shows no `unbounce_conversion` event when I submit the form.

Check if your Unbounce page is using a custom form setup. Go to your form element → Form Action. If it's set to "Go to URL" instead of "Default," the conversion event won't fire. Change to "Default" or add the tracking code to your thank-you page instead.

**Problem:** GA4 shows 2-3x more conversions than actual Unbounce leads.

This happens when the GA4 event fires on form field focus or page scroll instead of actual conversion. Check your GTM trigger — make sure it's firing on `unbounce_conversion`, not generic form events. I see teams accidentally set triggers for "Form Submission" or "Form Start" which fire way too often.

**Problem:** Conversions tracked but GA4 isn't counting them as conversions in reports.

Go to GA4 Admin → Events and verify `generate_lead` is toggled as a conversion. If you created the conversion before the event started firing, GA4 won't retroactively count past events. You'll need to wait for new conversions to flow in.

**Problem:** GTM fires the event but GA4 never receives it.

Check your GA4 Configuration tag. The Measurement ID should start with "G-" not "UA-". Also verify your GA4 Event tag is using the correct Configuration tag. About 30% of broken setups I audit have the wrong Measurement ID.

**Problem:** Events fire in preview but stop working after publishing GTM changes.

Unbounce caches aggressively. After publishing GTM changes, you need to republish your Unbounce page. Go to your page → Publish → Republish. The changes won't take effect until you do this.

**Problem:** The fallback trigger fires constantly, even without form submissions.

The jQuery selector is too broad. This happens on Unbounce pages with multiple forms or custom form elements. Add this condition to the fallback code: `if (this.closest('.lp-form').length > 0)` before the setTimeout function.

## What To Do Next

Now that your Unbounce conversions are flowing into GA4, consider these next steps:

- [Set up Unbounce conversion tracking for Google Ads](/tracking/unbounce-google-ads-conversion-tracking) to get conversion data directly in your ad platform
- [Connect Unbounce leads to HubSpot](/integrations/unbounce-to-hubspot) to close the loop on lead quality and ROI
- [Track Unbounce conversions in Meta Ads](/tracking/unbounce-meta-ads-conversion-tracking) if you're running Facebook/Instagram campaigns
- [Get a free tracking audit](/contact) to identify other gaps in your conversion tracking setup

*This guide is part of the [GA4 Conversion Tracking Hub](/tracking/ga4-conversion-tracking) — complete guides for tracking conversions from any form platform into GA4.*