---
title: "How to Track Unbounce Conversions in LinkedIn Ads (2026 Guide)"
slug: "unbounce-linkedin-ads-conversion-tracking"
description: "Step-by-step guide to tracking Unbounce form submissions as conversions in LinkedIn Ads. Covers GTM setup, Client-Side GTM, testing, and troubleshooting."
category: "tracking"
date: "2026-03-24"
hub_page: "/tracking/linkedin-ads-conversion-tracking"
page_type: "spoke"
---

# Unbounce + LinkedIn Ads Conversion Tracking Setup

I see broken Unbounce + LinkedIn tracking in about 60% of B2B accounts I audit. The main culprit? Most people try to stuff the LinkedIn Insight Tag directly into Unbounce's script manager and wonder why conversions either don't fire or fire multiple times per session. Unbounce's form system doesn't play nice with LinkedIn's event-based tracking without proper data layer setup.

Here's the issue: Unbounce forms submit via AJAX by default, so there's no page load event to trigger your LinkedIn conversion. You need to catch the form submission event and push it to your data layer for GTM to pick up.

## What You'll Have Working By The End

- Unbounce form submissions firing as LinkedIn Ad conversions within 15 minutes
- Clean data layer events that GTM can reliably catch 100% of the time
- Proper attribution back to your LinkedIn campaigns in Campaign Manager
- Form submission counts in Unbounce matching conversion counts in LinkedIn (within 5-10% variance)
- Debug-ready setup so you can verify everything is firing correctly

## Prerequisites

- [ ] LinkedIn Campaign Manager access with conversion tracking permissions
- [ ] Google Tag Manager container with Publish access
- [ ] Unbounce account with Script Manager access on your landing pages
- [ ] LinkedIn Insight Tag already installed (either via GTM or Unbounce Scripts)
- [ ] At least one active LinkedIn ad campaign to test with

## Step 1: Create the LinkedIn Conversion Action

First, set up the conversion action in LinkedIn Campaign Manager:

1. Go to **Campaign Manager → Analyze → Conversions**
2. Click **Create Conversion**
3. Choose **Online Conversion**
4. Fill in your conversion details:
   - **Conversion name**: "Unbounce Lead Form" (or whatever makes sense for your business)
   - **Category**: Lead
   - **Attribution window**: 30 days view, 30 days click (standard B2B settings)
   - **Value**: Set to your average lead value or leave at $1
5. Copy the **Conversion ID** — you'll need this for GTM

The conversion tracking code LinkedIn shows you can be ignored. We're handling this through GTM instead.

## Step 2: Install GTM on Your Unbounce Page

If you don't already have GTM on your Unbounce pages:

1. In your Unbounce page builder, go to **Scripts → Head Scripts**
2. Add your GTM head snippet:

```html
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-XXXXXXX');</script>
<!-- End Google Tag Manager -->
```

3. Go to **Scripts → Body Scripts** and add the noscript portion:

```html
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-XXXXXXX"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
```

Replace `GTM-XXXXXXX` with your actual GTM container ID.

## Step 3: Add the Data Layer Push Script

Here's where most setups break. Unbounce forms need a custom script to push form submissions to the data layer. In Unbounce, go to **Scripts → Body Scripts** and add this after your GTM noscript:

```html
<script>
// Wait for form to be ready
window.addEventListener('load', function() {
    // Find all Unbounce forms on the page
    var unbounceforms = document.querySelectorAll('form[id^="lp-pom-form-"]');
    
    unbounceforms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            // Push to data layer
            window.dataLayer = window.dataLayer || [];
            window.dataLayer.push({
                'event': 'unbounce_form_submit',
                'form_id': form.id,
                'page_url': window.location.href,
                'page_title': document.title
            });
            
            // Debug log (remove in production)
            console.log('Unbounce form submitted:', form.id);
        });
    });
});
</script>
```

This script catches any form submission on the page (Unbounce forms have IDs starting with `lp-pom-form-`) and pushes a clean event to the data layer.

## Step 4: Configure GTM Tags and Triggers

Now set up GTM to catch these events and fire LinkedIn conversions:

### Create the Trigger

1. In GTM, go to **Triggers → New**
2. Choose **Custom Event**
3. **Event name**: `unbounce_form_submit`
4. **This trigger fires on**: All Custom Events
5. Name it "Unbounce Form Submission"

### Create the LinkedIn Conversion Tag

1. Go to **Tags → New**
2. Choose **LinkedIn Insight Tag** (if available) or **Custom HTML**

If using Custom HTML (more reliable in my experience):

```html
<script>
window.lintrk = window.lintrk || function(a,b){window.lintrk.q.push([a,b])};
window.lintrk.q = window.lintrk.q || [];
window.lintrk('track', { conversion_id: YOUR_CONVERSION_ID });
</script>
```

Replace `YOUR_CONVERSION_ID` with the conversion ID from Step 1.

3. Set the trigger to your "Unbounce Form Submission" trigger
4. Name it "LinkedIn - Unbounce Lead Conversion"

### Create a GA4 Event Tag (Optional but Recommended)

I always set up a parallel GA4 event for cross-verification:

1. **Tags → New → GA4 Event**
2. **Event Name**: `unbounce_lead_submit`
3. **Parameters**:
   - `form_id`: `{{DLV - form_id}}`
   - `page_location`: `{{Page URL}}`
4. Set the same trigger: "Unbounce Form Submission"

You'll need to create the Data Layer Variable `DLV - form_id` first (Variables → New → Data Layer Variable → Variable Name: `form_id`).

## Step 5: Testing & Verification

This is crucial — I see too many setups that look right but don't actually work.

### Test in GTM Preview Mode

1. Enable **Preview mode** in GTM
2. Open your Unbounce page with `?gtm_debug=1` in the URL
3. Fill out and submit your form
4. In the GTM debug panel, verify:
   - The `unbounce_form_submit` event fires
   - Your LinkedIn conversion tag fires with it
   - No errors in the console

### Verify in LinkedIn Campaign Manager

Within 30 minutes of your test submission:

1. Go to **Campaign Manager → Analyze → Conversions**
2. Click on your conversion action
3. Check **Test Events** — your test conversion should appear here
4. Status should show "Attributed" or "Not Attributed" (both are fine for testing)

### Cross-Check the Numbers

After running for 24-48 hours:

1. **Unbounce**: Go to your page stats and note form submission count
2. **LinkedIn**: Check total conversions for the same time period
3. **GA4** (if you set it up): Check the `unbounce_lead_submit` event count

Acceptable variance is 5-15%. LinkedIn's attribution window means some conversions might not show up immediately, and ad blockers will prevent some tracking.

## Troubleshooting

**Problem**: GTM debug shows the event firing but no conversions in LinkedIn
→ Check that your LinkedIn Insight Tag base code is installed. The conversion event won't work without the base tag. Also verify your conversion ID is correct — I've seen people use campaign IDs by mistake.

**Problem**: Form submits but no `unbounce_form_submit` event in GTM debug
→ The form selector might be wrong. Open browser dev tools and inspect your form element. Some Unbounce themes use different form ID patterns. Update the `querySelectorAll` selector to match your actual form IDs.

**Problem**: Multiple conversion events firing for one form submission
→ Usually caused by having the LinkedIn tracking code in both Unbounce Scripts and GTM. Pick one location. I recommend GTM for better control and debugging.

**Problem**: Conversions showing in test events but not attributing to campaigns
→ Test from a different browser/device where you've actually clicked on a LinkedIn ad recently. LinkedIn's attribution requires the user to have been cookied by a LinkedIn ad within the attribution window.

**Problem**: Script errors about `dataLayer` not defined
→ Make sure GTM is loading before your custom script. Move your form tracking script below the GTM noscript snippet, or wrap it in a `window.addEventListener('load')` to ensure GTM has initialized.

**Problem**: High variance between Unbounce submissions and LinkedIn conversions (>20%)
→ Check your form validation. If users are submitting invalid forms that Unbounce rejects, your script might still fire the conversion event. Add form validation checks to your event listener.

## What To Do Next

Once you've got Unbounce + LinkedIn tracking working, you'll probably want to expand your tracking setup:

- **[Unbounce + Google Ads Conversion Tracking](/tracking/unbounce-google-ads-conversion-tracking)** — Same concepts but different tag configuration
- **[Unbounce + Meta Ads Conversion Tracking](/tracking/unbounce-meta-ads-conversion-tracking)** — Facebook's Conversions API integration
- **[Unbounce + GA4 Conversion Tracking](/tracking/unbounce-ga4-conversion-tracking)** — Complete Google Analytics 4 setup
- **[Unbounce to HubSpot Integration](/integrations/unbounce-to-hubspot)** — Connect your leads to your CRM automatically

Need someone to audit your tracking setup? I offer **[free tracking audits](/contact)** where I'll review your current configuration and identify what's broken (usually takes 15 minutes to spot the main issues).

*This guide is part of the [LinkedIn Ads Conversion Tracking Hub](/tracking/linkedin-ads-conversion-tracking) — complete guides for tracking LinkedIn conversions across all major form builders and landing page tools.*